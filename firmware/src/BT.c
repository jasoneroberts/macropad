/*
 * Copyright (c) 2018 Nordic Semiconductor ASA
 *
 * SPDX-License-Identifier: LicenseRef-Nordic-5-Clause
 */

/*
 * Bluetooth LE HID keyboard + consumer control, built on the NCS HIDS service.
 * Based on the NCS peripheral_hids_keyboard sample, cut down to one host at a
 * time and Just Works pairing.
 */

#include "BT.h"

#include <errno.h>

#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/conn.h>
#include <zephyr/bluetooth/gatt.h>
#include <zephyr/bluetooth/hci.h>
#include <zephyr/bluetooth/services/bas.h>
#include <zephyr/bluetooth/uuid.h>
#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>
#include <zephyr/settings/settings.h>

#include <bluetooth/services/hids.h>

#include "HID_Engine.h"

LOG_MODULE_REGISTER(bt_hid, LOG_LEVEL_INF);

/* CONSTANTS */
#define DEVICE_NAME     CONFIG_BT_DEVICE_NAME
#define DEVICE_NAME_LEN (sizeof(DEVICE_NAME) - 1)

#define BASE_USB_HID_SPEC_VERSION 0x0101

/* Advertise fast for a short while (quick to find when pairing), then slowly
 * to save battery while nobody is connecting. */
#define ADV_FAST_TIME K_SECONDS(30)

/* Per-connection storage for every report we declare: keyboard + consumer */
BT_HIDS_DEF(hids_obj, KEYBOARD_REPORT_LEN, CONSUMER_REPORT_LEN);

static const struct bt_data ad[] = {
	BT_DATA_BYTES(BT_DATA_GAP_APPEARANCE,
		      (CONFIG_BT_DEVICE_APPEARANCE >> 0) & 0xff,
		      (CONFIG_BT_DEVICE_APPEARANCE >> 8) & 0xff),
	BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
	BT_DATA_BYTES(BT_DATA_UUID16_ALL, BT_UUID_16_ENCODE(BT_UUID_HIDS_VAL),
		      BT_UUID_16_ENCODE(BT_UUID_BAS_VAL)),
};

static const struct bt_data sd[] = {
	BT_DATA(BT_DATA_NAME_COMPLETE, DEVICE_NAME, DEVICE_NAME_LEN),
};

/* TYPES */
static struct bt_conn *host_conn;
static atomic_t advertising;
static bool adv_slow;

static void adv_work_handler(struct k_work *work);
static K_WORK_DEFINE(adv_work, adv_work_handler);
static void adv_slow_handler(struct k_work *work);
static K_WORK_DELAYABLE_DEFINE(adv_slow_work, adv_slow_handler);

static void advertising_start(bool slow)
{
	int err;
	const struct bt_le_adv_param *param = slow ?
		BT_LE_ADV_PARAM(BT_LE_ADV_OPT_CONN, BT_GAP_ADV_SLOW_INT_MIN,
				BT_GAP_ADV_SLOW_INT_MAX, NULL) :
		BT_LE_ADV_PARAM(BT_LE_ADV_OPT_CONN, BT_GAP_ADV_FAST_INT_MIN_2,
				BT_GAP_ADV_FAST_INT_MAX_2, NULL);

	err = bt_le_adv_start(param, ad, ARRAY_SIZE(ad), sd, ARRAY_SIZE(sd));
	if (err == -EALREADY) {
		return;
	}

	if (err != 0) {
		LOG_ERR("Advertising failed to start (err %d)", err);
		return;
	}

	atomic_set(&advertising, 1);
	adv_slow = slow;
	LOG_INF("Advertising (%s) as \"%s\"", slow ? "slow" : "fast", DEVICE_NAME);
	if (!slow) {
		k_work_reschedule(&adv_slow_work, ADV_FAST_TIME);
	}
	hid_engine_link_changed();
}

static void adv_work_handler(struct k_work *work)
{
	ARG_UNUSED(work);
	advertising_start(false);
}

static void adv_slow_handler(struct k_work *work)
{
	ARG_UNUSED(work);

	if (!atomic_get(&advertising) || adv_slow) {
		return;
	}

	(void)bt_le_adv_stop();
	advertising_start(true);
}

static void connected(struct bt_conn *conn, uint8_t err)
{
	char addr[BT_ADDR_LE_STR_LEN];

	bt_addr_le_to_str(bt_conn_get_dst(conn), addr, sizeof(addr));

	if (err != 0) {
		LOG_WRN("Failed to connect to %s, 0x%02x %s", addr, err, bt_hci_err_to_str(err));
		return;
	}

	LOG_INF("Connected %s", addr);

	/* Connectable advertising stops by itself once a host connects */
	atomic_set(&advertising, 0);
	k_work_cancel_delayable(&adv_slow_work);

	if (bt_hids_connected(&hids_obj, conn) != 0) {
		LOG_ERR("Failed to notify HIDS about the connection");
	}

	host_conn = bt_conn_ref(conn);
	hid_engine_link_changed();
}

static void disconnected(struct bt_conn *conn, uint8_t reason)
{
	LOG_INF("Disconnected, reason 0x%02x %s", reason, bt_hci_err_to_str(reason));

	if (bt_hids_disconnected(&hids_obj, conn) != 0) {
		LOG_ERR("Failed to notify HIDS about the disconnection");
	}

	if (host_conn == conn) {
		bt_conn_unref(host_conn);
		host_conn = NULL;
	}

	hid_engine_link_changed();
}

/* The connection object is free again: only now can advertising restart */
static void recycled(void)
{
	if (host_conn == NULL) {
		k_work_submit(&adv_work);
	}
}

static void security_changed(struct bt_conn *conn, bt_security_t level, enum bt_security_err err)
{
	ARG_UNUSED(conn);

	if (err != 0) {
		LOG_WRN("Security failed: level %u err %d %s", level, err, bt_security_err_to_str(err));
		return;
	}

	LOG_INF("Security level %u", level);
}

BT_CONN_CB_DEFINE(conn_callbacks) = {
	.connected = connected,
	.disconnected = disconnected,
	.recycled = recycled,
	.security_changed = security_changed,
};

static int hids_setup(void)
{
	struct bt_hids_init_param init = {0};
	struct bt_hids_inp_rep *rep;

	init.rep_map.data = hid_report_desc;
	init.rep_map.size = hid_report_desc_len;
	init.info.bcd_hid = BASE_USB_HID_SPEC_VERSION;
	init.info.b_country_code = 0x00;
	init.info.flags = BT_HIDS_REMOTE_WAKE | BT_HIDS_NORMALLY_CONNECTABLE;

	/* Input reports in enum hid_report order, so the enum is the report index */
	rep = &init.inp_rep_group_init.reports[HID_REPORT_KEYBOARD];
	rep->size = KEYBOARD_REPORT_LEN;
	rep->id = REPORT_ID_KEYBOARD;
	init.inp_rep_group_init.cnt++;

	rep = &init.inp_rep_group_init.reports[HID_REPORT_CONSUMER];
	rep->size = CONSUMER_REPORT_LEN;
	rep->id = REPORT_ID_CONSUMER;
	init.inp_rep_group_init.cnt++;

	return bt_hids_init(&hids_obj, &init);
}

int bt_init(void)
{
	int err;

	err = hids_setup();
	if (err != 0) {
		LOG_ERR("HIDS init failed (err %d)", err);
		return err;
	}

	err = bt_enable(NULL);
	if (err != 0) {
		LOG_ERR("Bluetooth init failed (err %d)", err);
		return err;
	}

	/* Bonds (pairing keys) live in settings, so a paired PC reconnects after a reset */
	if (IS_ENABLED(CONFIG_SETTINGS)) {
		settings_load();
	}

	advertising_start(false);
	return 0;
}

bool bt_hid_is_connected(void)
{
	return host_conn != NULL;
}

bool bt_hid_is_advertising(void)
{
	return atomic_get(&advertising) != 0;
}

int bt_hid_send(enum hid_report report, const uint8_t *payload)
{
	struct bt_conn *conn = host_conn;

	if (conn == NULL) {
		return -ENOTCONN;
	}

	return bt_hids_inp_rep_send(&hids_obj, conn, (uint8_t)report, payload,
				    hid_report_len(report), NULL);
}

void bt_set_battery_level(uint8_t percent)
{
	(void)bt_bas_set_battery_level(percent);
}
