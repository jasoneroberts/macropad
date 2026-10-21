/*
 * The screen: a grid of tiles that mirrors the keys under it, plus a status bar.
 *
 * LVGL is not thread-safe, so exactly one thread (ui_thread) calls it. Everyone
 * else posts a small message to ui_q and the UI thread applies it between frames.
 */

#include "Display_UI.h"

#include <errno.h>

#include <lvgl.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/display.h>
#include <zephyr/drivers/led.h>
#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>
#include <zephyr/sys/util.h>

#include "Keymap.h"

LOG_MODULE_REGISTER(display_ui, LOG_LEVEL_INF);

/* CONSTANTS */
#define UI_STACK_SIZE   4096
#define UI_PRIORITY     7        /* below the HID engine (main, priority 0) */
#define STATUS_H        24       /* status bar height, px */
#define GAP             3        /* space between tiles, px */
#define INFO_SHOW_MS    1500     /* how long "Vol +" stays in the status bar */
#define SMALL_TILE_W    60       /* below this, tiles show the icon only */

#define COL_BG          0x101418
#define COL_TILE        0x262c33
#define COL_TILE_DOWN   0x0b6e74 /* the knob's teal from the case renders */
#define COL_TEXT        0xf4f3ef
#define COL_DIM         0x9aa3ad

static const struct device *const display_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_display));

#if DT_NODE_EXISTS(DT_ALIAS(backlight))
static const struct led_dt_spec backlight = LED_DT_SPEC_GET(DT_ALIAS(backlight));
#define HAS_BACKLIGHT 1
#else
#define HAS_BACKLIGHT 0
#endif

/* TYPES */
enum ui_evt_type {
	UI_EVT_KEY,
	UI_EVT_KNOB,
	UI_EVT_LINK,
	UI_EVT_BATTERY,
};

struct ui_evt {
	uint8_t type;
	uint8_t key;
	int8_t value;
};

#define LINK_USB BIT(0)
#define LINK_BLE BIT(1)
#define LINK_ADV BIT(2)

K_MSGQ_DEFINE(ui_q, sizeof(struct ui_evt), 16, 4);
K_THREAD_STACK_DEFINE(ui_stack, UI_STACK_SIZE);
static struct k_thread ui_thread_data;

static lv_obj_t *tiles[KEY_COUNT];
static lv_obj_t *link_label;
static lv_obj_t *info_label;
static lv_obj_t *battery_label;
static bool screen_on;
static int64_t last_input_ms;
static int64_t info_until_ms;

static void ui_post(uint8_t type, uint8_t key, int8_t value)
{
	struct ui_evt evt = { .type = type, .key = key, .value = value };

	/* Dropping a UI update is harmless; blocking the HID engine is not */
	(void)k_msgq_put(&ui_q, &evt, K_NO_WAIT);
}

void display_ui_key(uint8_t key, bool pressed)
{
	ui_post(UI_EVT_KEY, key, pressed ? 1 : 0);
}

void display_ui_knob(int dir)
{
	ui_post(UI_EVT_KNOB, 0, (int8_t)dir);
}

void display_ui_link(bool usb, bool ble, bool advertising)
{
	ui_post(UI_EVT_LINK, 0, (int8_t)((usb ? LINK_USB : 0) | (ble ? LINK_BLE : 0) |
					 (advertising ? LINK_ADV : 0)));
}

void display_ui_battery(int percent)
{
	ui_post(UI_EVT_BATTERY, 0, (int8_t)CLAMP(percent, DISPLAY_UI_ON_USB, 100));
}

static void backlight_set(bool on)
{
#if HAS_BACKLIGHT
	(void)led_set_brightness_dt(&backlight, on ? CONFIG_MACROPAD_BACKLIGHT_PERCENT : 0);
#else
	ARG_UNUSED(on);
#endif
}

static void screen_set(bool on)
{
	if (on == screen_on) {
		return;
	}

	screen_on = on;
	if (on) {
		(void)display_blanking_off(display_dev);
		backlight_set(true);
	} else {
		/* Backlight first, so the panel going dark is never visible */
		backlight_set(false);
		(void)display_blanking_on(display_dev);
	}
}

static lv_obj_t *make_label(lv_obj_t *parent, const lv_font_t *font, uint32_t colour)
{
	lv_obj_t *label = lv_label_create(parent);

	lv_obj_set_style_text_font(label, font, 0);
	lv_obj_set_style_text_color(label, lv_color_hex(colour), 0);
	lv_label_set_text(label, "");
	return label;
}

static void build_ui(void)
{
	lv_obj_t *scr = lv_screen_active();
	int32_t w = lv_display_get_horizontal_resolution(NULL);
	int32_t h = lv_display_get_vertical_resolution(NULL);
	int32_t inset = CONFIG_MACROPAD_UI_INSET;
	int32_t grid_x = inset;
	int32_t grid_y = inset + STATUS_H;
	int32_t grid_w = w - 2 * inset;
	int32_t grid_h = h - 2 * inset - STATUS_H;
	int32_t tile_w = (grid_w - GAP * (KEY_COLS + 1)) / KEY_COLS;
	int32_t tile_h = (grid_h - GAP * (KEY_ROWS + 1)) / KEY_ROWS;
	bool small = tile_w < SMALL_TILE_W;

	LOG_INF("Screen %d x %d, tiles %d x %d px", w, h, tile_w, tile_h);

	lv_obj_set_style_bg_color(scr, lv_color_hex(COL_BG), 0);
	lv_obj_set_style_bg_opa(scr, LV_OPA_COVER, 0);
	lv_obj_remove_flag(scr, LV_OBJ_FLAG_SCROLLABLE);

	/* Status bar: link on the left, knob feedback in the middle, battery on the right */
	link_label = make_label(scr, &lv_font_montserrat_12, COL_TEXT);
	lv_obj_align(link_label, LV_ALIGN_TOP_LEFT, inset + 6, inset + 5);
	info_label = make_label(scr, &lv_font_montserrat_12, COL_DIM);
	lv_obj_align(info_label, LV_ALIGN_TOP_MID, 0, inset + 5);
	battery_label = make_label(scr, &lv_font_montserrat_12, COL_DIM);
	lv_obj_align(battery_label, LV_ALIGN_TOP_RIGHT, -(inset + 6), inset + 5);

	/* One tile per key, laid out like the keys: row 0 (back row) at the top */
	for (uint8_t k = 0; k < KEY_COUNT; k++) {
		const struct pad_action *a = keymap_key(k);
		int32_t col = k % KEY_COLS;
		int32_t row = k / KEY_COLS;
		lv_obj_t *tile = lv_obj_create(scr);
		lv_obj_t *icon;

		lv_obj_set_size(tile, tile_w, tile_h);
		lv_obj_set_pos(tile, grid_x + GAP + col * (tile_w + GAP),
			       grid_y + GAP + row * (tile_h + GAP));
		lv_obj_set_style_bg_color(tile, lv_color_hex(COL_TILE), 0);
		lv_obj_set_style_border_width(tile, 0, 0);
		lv_obj_set_style_radius(tile, 6, 0);
		lv_obj_set_style_pad_all(tile, 2, 0);
		lv_obj_remove_flag(tile, LV_OBJ_FLAG_SCROLLABLE);

		icon = make_label(tile, &lv_font_montserrat_16, COL_TEXT);
		lv_label_set_text(icon, a->icon);

		if (small) {
			lv_obj_center(icon);
		} else {
			lv_obj_t *name = make_label(tile, &lv_font_montserrat_12, COL_DIM);

			lv_label_set_text(name, a->label);
			lv_obj_align(icon, LV_ALIGN_CENTER, 0, -9);
			lv_obj_align(name, LV_ALIGN_CENTER, 0, 12);
		}

		tiles[k] = tile;
	}
}

static void show_link(uint8_t link)
{
	if (link & LINK_USB) {
		lv_label_set_text(link_label, LV_SYMBOL_USB " USB");
	} else if (link & LINK_BLE) {
		lv_label_set_text(link_label, LV_SYMBOL_BLUETOOTH " Bluetooth");
	} else if (link & LINK_ADV) {
		lv_label_set_text(link_label, LV_SYMBOL_BLUETOOTH " Waiting for PC");
	} else {
		lv_label_set_text(link_label, "No connection");
	}
}

static void show_battery(int8_t percent)
{
	if (percent == DISPLAY_UI_ON_USB) {
		lv_label_set_text(battery_label, "USB " LV_SYMBOL_CHARGE);
		return;
	}

	const char *sym = percent > 80 ? LV_SYMBOL_BATTERY_FULL :
			  percent > 55 ? LV_SYMBOL_BATTERY_3 :
			  percent > 30 ? LV_SYMBOL_BATTERY_2 :
			  percent > 10 ? LV_SYMBOL_BATTERY_1 : LV_SYMBOL_BATTERY_EMPTY;

	lv_label_set_text_fmt(battery_label, "%d%% %s", percent, sym);
}

static void handle_evt(const struct ui_evt *evt)
{
	switch (evt->type) {
	case UI_EVT_KEY:
		last_input_ms = k_uptime_get();
		if (evt->key < KEY_COUNT) {
			lv_obj_set_style_bg_color(tiles[evt->key],
				lv_color_hex(evt->value ? COL_TILE_DOWN : COL_TILE), 0);
		} else if (evt->value) {
			lv_label_set_text_fmt(info_label, "%s %s", keymap_key(evt->key)->icon,
					      keymap_key(evt->key)->label);
			info_until_ms = last_input_ms + INFO_SHOW_MS;
		}
		break;
	case UI_EVT_KNOB: {
		const struct pad_action *a = keymap_knob(evt->value);

		last_input_ms = k_uptime_get();
		lv_label_set_text_fmt(info_label, "%s %s", a->icon, a->label);
		info_until_ms = last_input_ms + INFO_SHOW_MS;
		break;
	}
	case UI_EVT_LINK:
		show_link((uint8_t)evt->value);
		break;
	case UI_EVT_BATTERY:
		show_battery(evt->value);
		break;
	default:
		break;
	}
}

static void ui_thread(void *p1, void *p2, void *p3)
{
	struct ui_evt evt;

	ARG_UNUSED(p1);
	ARG_UNUSED(p2);
	ARG_UNUSED(p3);

	build_ui();
	show_link(0);
	lv_timer_handler();   /* draw the first frame before the backlight comes on */
	last_input_ms = k_uptime_get();
	screen_set(true);

	while (true) {
		uint32_t wait_ms = MIN(lv_timer_handler(), 100U);

		if (k_msgq_get(&ui_q, &evt, K_MSEC(wait_ms)) == 0) {
			do {
				handle_evt(&evt);
			} while (k_msgq_get(&ui_q, &evt, K_NO_WAIT) == 0);
		}

		int64_t now = k_uptime_get();

		if (info_until_ms != 0 && now > info_until_ms) {
			lv_label_set_text(info_label, "");
			info_until_ms = 0;
		}

		if (CONFIG_MACROPAD_SCREEN_TIMEOUT_S > 0) {
			screen_set(now - last_input_ms < CONFIG_MACROPAD_SCREEN_TIMEOUT_S * 1000LL);
		}
	}
}

int display_ui_init(void)
{
	if (!device_is_ready(display_dev)) {
		LOG_ERR("Display %s is not ready", display_dev->name);
		return -ENODEV;
	}

#if HAS_BACKLIGHT
	if (!led_is_ready_dt(&backlight)) {
		LOG_WRN("Backlight is not ready, the screen may stay dark");
	}
#endif

	k_thread_create(&ui_thread_data, ui_stack, K_THREAD_STACK_SIZEOF(ui_stack), ui_thread,
			NULL, NULL, NULL, UI_PRIORITY, 0, K_NO_WAIT);
	k_thread_name_set(&ui_thread_data, "ui");
	return 0;
}
