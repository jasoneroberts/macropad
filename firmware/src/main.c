#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>

#include "BT.h"
#include "Battery.h"
#include "Display_UI.h"
#include "HID_Engine.h"
#include "Keymap.h"
#include "USB_Link.h"

LOG_MODULE_REGISTER(main, LOG_LEVEL_INF);

int main(void)
{
	int ret;

	LOG_INF("Macropad: %d x %d keys + knob", KEY_ROWS, KEY_COLS);

	/* Screen first, so link and battery messages from the others land on it */
	ret = display_ui_init();
	if (ret != 0) {
		LOG_WRN("No screen, carrying on without it (%d)", ret);
	}

	/* Either link on its own is enough to be useful, so neither is fatal */
	ret = bt_init();
	if (ret != 0) {
		LOG_ERR("Bluetooth failed to start (%d), USB only", ret);
	}

	ret = usb_link_init();
	if (ret != 0) {
		LOG_ERR("USB failed to start (%d), Bluetooth only", ret);
	}

	ret = battery_init();
	if (ret != 0 && ret != -ENOTSUP) {
		LOG_WRN("Battery reading unavailable (%d)", ret);
	}

	hid_engine_run();   /* never returns */
	return 0;
}
