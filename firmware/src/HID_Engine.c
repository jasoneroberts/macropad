#include "HID_Engine.h"

#include <errno.h>
#include <stdlib.h>
#include <string.h>

#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>
#include <zephyr/sys/byteorder.h>
#include <zephyr/sys/util.h>

#include "BT.h"
#include "Display_UI.h"
#include "HID_Desc.h"
#include "Keymap.h"
#include "Pad_Input.h"
#include "USB_Link.h"

LOG_MODULE_REGISTER(hid_engine, LOG_LEVEL_INF);

#if defined(CONFIG_BOARD_PROMICRO_NRF52840_NRF52840_UF2)
#include <hal/nrf_power.h>
#include <zephyr/sys/reboot.h>
#endif

/* CONSTANTS */
#define KB_MODS_IDX  0
#define KB_KEYS_IDX  2
#define KB_KEYS_MAX  6

BUILD_ASSERT(KEY_TOTAL <= 32, "pressed_keys is a 32-bit mask");

/* TYPES */
static uint32_t pressed_keys;                 /* bit n set while key n is held */
static uint8_t kb_sent[KEYBOARD_REPORT_LEN];  /* last keyboard report the host got */

#if defined(CONFIG_BOARD_PROMICRO_NRF52840_NRF52840_UF2)
/* Hold the top-left key and the knob push for 3 s to restart into the board's UF2
 * bootloader (what a double-tap on reset does), so new firmware can be dragged onto
 * the USB drive without opening the case. The Adafruit bootloader checks the
 * GPREGRET register at start-up; it survives a soft reset. */
#define UF2_BOOT_MAGIC  0x57   /* DFU_MAGIC_UF2_RESET in Adafruit_nRF52_Bootloader */
#define BOOTLOADER_HOLD K_SECONDS(3)
#define BOOTLOADER_KEYS (BIT(0) | BIT(KEY_KNOB_PUSH))

static void bootloader_work_handler(struct k_work *work)
{
	ARG_UNUSED(work);
	LOG_WRN("Restarting into the UF2 bootloader");
	nrf_power_gpregret_set(NRF_POWER, 0, UF2_BOOT_MAGIC);
	sys_reboot(SYS_REBOOT_WARM);
}

static K_WORK_DELAYABLE_DEFINE(bootloader_work, bootloader_work_handler);

static void bootloader_combo_check(void)
{
	if ((pressed_keys & BOOTLOADER_KEYS) == BOOTLOADER_KEYS) {
		/* schedule, not reschedule: other keys must not restart the 3 s */
		k_work_schedule(&bootloader_work, BOOTLOADER_HOLD);
	} else {
		k_work_cancel_delayable(&bootloader_work);
	}
}
#else
static void bootloader_combo_check(void)
{
}
#endif

/* USB wins while a PC has configured it; otherwise Bluetooth if connected */
static int hid_send(enum hid_report report, const uint8_t *payload)
{
	int ret;

	if (usb_link_is_ready()) {
		ret = usb_link_send(report, payload);
	} else if (bt_hid_is_connected()) {
		ret = bt_hid_send(report, payload);
	} else {
		ret = -ENOTCONN;
	}

	if (ret != 0 && ret != -ENOTCONN && ret != -EAGAIN) {
		LOG_WRN("Report %d not sent (%d)", report, ret);
	}

	return ret;
}

/* Add one keyboard action to a report: OR in its modifiers, put its key in a free slot */
static void kb_add(uint8_t rep[KEYBOARD_REPORT_LEN], const struct pad_action *a)
{
	rep[KB_MODS_IDX] |= a->mods;

	if (a->usage == 0) {
		return;   /* modifier-only action */
	}

	for (int i = KB_KEYS_IDX; i < KB_KEYS_IDX + KB_KEYS_MAX; i++) {
		if (rep[i] == a->usage) {
			return;   /* already held by another key */
		}

		if (rep[i] == 0) {
			rep[i] = (uint8_t)a->usage;
			return;
		}
	}
	/* More than six keys held: like any keyboard, the extra ones are ignored */
}

/* The keyboard report for whatever is held right now */
static void kb_build(uint8_t rep[KEYBOARD_REPORT_LEN])
{
	memset(rep, 0, KEYBOARD_REPORT_LEN);

	for (uint8_t k = 0; k < KEY_TOTAL; k++) {
		const struct pad_action *a = keymap_key(k);

		if ((pressed_keys & BIT(k)) && a->type == ACTION_KEY) {
			kb_add(rep, a);
		}
	}
}

static void kb_send(const uint8_t rep[KEYBOARD_REPORT_LEN])
{
	(void)hid_send(HID_REPORT_KEYBOARD, rep);
	memcpy(kb_sent, rep, KEYBOARD_REPORT_LEN);
}

static void kb_sync(void)
{
	uint8_t rep[KEYBOARD_REPORT_LEN];

	kb_build(rep);
	if (memcmp(rep, kb_sent, sizeof(rep)) != 0) {
		kb_send(rep);
	}
}

static void cc_send(uint16_t usage)
{
	uint8_t rep[CONSUMER_REPORT_LEN];

	sys_put_le16(usage, rep);   /* HID values are little-endian */
	(void)hid_send(HID_REPORT_CONSUMER, rep);
}

/* Press and release in one go (knob clicks) */
static void tap(const struct pad_action *a)
{
	uint8_t rep[KEYBOARD_REPORT_LEN];

	switch (a->type) {
	case ACTION_CONSUMER:
		cc_send(a->usage);
		cc_send(0);
		break;
	case ACTION_KEY:
		kb_build(rep);
		kb_add(rep, a);
		kb_send(rep);
		kb_build(rep);
		kb_send(rep);
		break;
	default:
		break;
	}
}

static void handle_key(uint8_t key, bool pressed)
{
	const struct pad_action *a = keymap_key(key);

	if (key >= KEY_TOTAL) {
		return;
	}

	LOG_DBG("Key %u (%s) %s", key, a->label, pressed ? "down" : "up");
	WRITE_BIT(pressed_keys, key, pressed);
	display_ui_key(key, pressed);
	bootloader_combo_check();

	switch (a->type) {
	case ACTION_KEY:
		/* Held for as long as the key is held, so auto-repeat works */
		kb_sync();
		break;
	case ACTION_CONSUMER:
		cc_send(pressed ? a->usage : 0);
		break;
	default:
		break;
	}
}

static void handle_knob(int clicks)
{
	int dir = (clicks > 0) ? 1 : -1;
	const struct pad_action *a = keymap_knob(dir);

	display_ui_knob(dir);

	for (int i = 0; i < abs(clicks); i++) {
		tap(a);
	}
}

void hid_engine_link_changed(void)
{
	display_ui_link(usb_link_is_ready(), bt_hid_is_connected(), bt_hid_is_advertising());
}

void hid_engine_run(void)
{
	struct pad_event evt;

	hid_engine_link_changed();

	while (true) {
		(void)pad_event_get(&evt, K_FOREVER);

		switch (evt.type) {
		case PAD_EVT_KEY:
			handle_key(evt.key, evt.value != 0);
			break;
		case PAD_EVT_KNOB:
			if (evt.value != 0) {
				handle_knob(evt.value);
			}
			break;
		default:
			break;
		}
	}
}
