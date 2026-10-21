#include "HID_Desc.h"

#include <zephyr/usb/class/hid.h>

/* CONSTANTS */
#define HID_USAGE_PAGE_CONSUMER     0x0C
#define HID_USAGE_CONSUMER_CONTROL  0x01

const uint8_t hid_report_desc[] = {
	/* Keyboard, report ID 1: the usual 8-byte keyboard layout */
	HID_USAGE_PAGE(HID_USAGE_GEN_DESKTOP),
	HID_USAGE(HID_USAGE_GEN_DESKTOP_KEYBOARD),
	HID_COLLECTION(HID_COLLECTION_APPLICATION),
		HID_REPORT_ID(REPORT_ID_KEYBOARD),
		/* Byte 0: one bit per modifier, usages 0xE0 (left Ctrl) to 0xE7 (right GUI) */
		HID_USAGE_PAGE(HID_USAGE_GEN_KEYBOARD),
		HID_USAGE_MIN8(0xE0),
		HID_USAGE_MAX8(0xE7),
		HID_LOGICAL_MIN8(0),
		HID_LOGICAL_MAX8(1),
		HID_REPORT_SIZE(1),
		HID_REPORT_COUNT(8),
		HID_INPUT(0x02),
		/* Byte 1: reserved */
		HID_REPORT_SIZE(8),
		HID_REPORT_COUNT(1),
		HID_INPUT(0x01),
		/* Bytes 2-7: up to six key usages held at once. 0..0xE7 so F13-F24
		 * (0x68-0x73) are available to the keymap too. */
		HID_REPORT_SIZE(8),
		HID_REPORT_COUNT(6),
		HID_LOGICAL_MIN8(0),
		HID_LOGICAL_MAX16(0xE7, 0x00),
		HID_USAGE_MIN8(0),
		HID_USAGE_MAX8(0xE7),
		HID_INPUT(0x00),
	HID_END_COLLECTION,

	/* Consumer control (media keys, volume), report ID 2: one 16-bit usage */
	HID_USAGE_PAGE(HID_USAGE_PAGE_CONSUMER),
	HID_USAGE(HID_USAGE_CONSUMER_CONTROL),
	HID_COLLECTION(HID_COLLECTION_APPLICATION),
		HID_REPORT_ID(REPORT_ID_CONSUMER),
		HID_LOGICAL_MIN8(0),
		HID_LOGICAL_MAX16(0xFF, 0x03),
		HID_USAGE_MIN8(0),
		HID_USAGE_MAX16(0xFF, 0x03),
		HID_REPORT_SIZE(16),
		HID_REPORT_COUNT(1),
		HID_INPUT(0x00),
	HID_END_COLLECTION,
};

const size_t hid_report_desc_len = sizeof(hid_report_desc);
