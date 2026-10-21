/*
 * Battery level on the Pro Micro boards. On the SuperMini (and nice!nano) the LiPo
 * feeds the nRF52840's VDDH pin, so the SAADC can measure it with no divider: the
 * ADC input VDDHDIV5 is VDDH / 5. Devicetree (zephyr,user io-channels) says which
 * ADC channel to use; boards without it get no battery reporting.
 *
 * While USB is plugged in, the SuperMini feeds VDDH from USB (about 5 V) instead,
 * so the battery cannot be measured then. A reading above any LiPo voltage means
 * "on USB, charging"; Windows keeps the last level until USB is unplugged.
 */

#include "Battery.h"

#include <errno.h>

#include <zephyr/devicetree.h>
#include <zephyr/drivers/adc.h>
#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>
#include <zephyr/sys/util.h>

#include "BT.h"
#include "Display_UI.h"

LOG_MODULE_REGISTER(battery, LOG_LEVEL_INF);

#if DT_NODE_HAS_PROP(DT_PATH(zephyr_user), io_channels)

/* CONSTANTS */
#define VDDH_DIVIDER   5
#define READ_PERIOD    K_SECONDS(60)
#define ON_USB_MV      4400 /* a full LiPo is 4200 mV */

static const struct adc_dt_spec vbat = ADC_DT_SPEC_GET(DT_PATH(zephyr_user));

/* TYPES */
struct lipo_point {
	uint16_t mv;
	uint8_t percent;
};

/* Rough resting curve for a single LiPo cell, highest first */
static const struct lipo_point lipo_curve[] = {
	{ 4200, 100 }, { 4100, 90 }, { 4000, 78 }, { 3900, 62 }, { 3800, 46 },
	{ 3750, 35 },  { 3700, 22 }, { 3650, 12 }, { 3600, 6 },  { 3500, 2 },
	{ 3300, 0 },
};

static uint8_t lipo_percent(int mv)
{
	if (mv >= lipo_curve[0].mv) {
		return 100;
	}

	for (size_t i = 1; i < ARRAY_SIZE(lipo_curve); i++) {
		const struct lipo_point *hi = &lipo_curve[i - 1];
		const struct lipo_point *lo = &lipo_curve[i];

		if (mv >= lo->mv) {
			/* straight line between the two neighbouring points */
			return lo->percent + (mv - lo->mv) * (hi->percent - lo->percent) /
					     (hi->mv - lo->mv);
		}
	}

	return 0;
}

static int battery_read_mv(void)
{
	int16_t raw;
	int32_t mv;
	struct adc_sequence seq = {
		.buffer = &raw,
		.buffer_size = sizeof(raw),
	};
	int ret;

	(void)adc_sequence_init_dt(&vbat, &seq);
	ret = adc_read_dt(&vbat, &seq);
	if (ret != 0) {
		return ret;
	}

	mv = raw;
	ret = adc_raw_to_millivolts_dt(&vbat, &mv);
	if (ret != 0) {
		return ret;
	}

	return mv * VDDH_DIVIDER + CONFIG_MACROPAD_BATTERY_OFFSET_MV;
}

static void battery_work_handler(struct k_work *work);
static K_WORK_DELAYABLE_DEFINE(battery_work, battery_work_handler);

static void battery_work_handler(struct k_work *work)
{
	int mv = battery_read_mv();

	ARG_UNUSED(work);

	if (mv > ON_USB_MV) {
		LOG_INF("On USB power (VDDH %d mV)", mv);
		display_ui_battery(DISPLAY_UI_ON_USB);
	} else if (mv > 0) {
		uint8_t percent = lipo_percent(mv);

		LOG_INF("Battery %d mV, about %u %%", mv, percent);
		bt_set_battery_level(percent);
		display_ui_battery(percent);
	} else {
		LOG_WRN("Battery read failed (%d)", mv);
	}

	k_work_schedule(&battery_work, READ_PERIOD);
}

int battery_init(void)
{
	int ret;

	if (!adc_is_ready_dt(&vbat)) {
		LOG_ERR("ADC is not ready");
		return -ENODEV;
	}

	ret = adc_channel_setup_dt(&vbat);
	if (ret != 0) {
		LOG_ERR("ADC channel setup failed (%d)", ret);
		return ret;
	}

	k_work_schedule(&battery_work, K_SECONDS(2));
	return 0;
}

#else /* no battery channel in devicetree */

int battery_init(void)
{
	return -ENOTSUP;
}

#endif
