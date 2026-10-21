#ifndef HID_DESC_H
#define HID_DESC_H

#include <stddef.h>
#include <stdint.h>

/* CONSTANTS */
#define REPORT_ID_KEYBOARD  0x01
#define REPORT_ID_CONSUMER  0x02
#define KEYBOARD_REPORT_LEN 8   /* modifier bits, reserved byte, 6 key codes */
#define CONSUMER_REPORT_LEN 2   /* one 16-bit consumer usage, 0 = released */

/* TYPES */
/* Our two input reports. The enum value is also the report's index in the
 * Bluetooth HIDS input report group (BT.c registers them in this order). */
enum hid_report {
	HID_REPORT_KEYBOARD = 0,
	HID_REPORT_CONSUMER = 1,
	HID_REPORT_COUNT,
};

/* One report descriptor for both transports: USB sends it in the HID class
 * descriptor, Bluetooth serves it as the HIDS Report Map. */
extern const uint8_t hid_report_desc[];
extern const size_t hid_report_desc_len;

static inline uint8_t hid_report_id(enum hid_report r)
{
	return (r == HID_REPORT_KEYBOARD) ? REPORT_ID_KEYBOARD : REPORT_ID_CONSUMER;
}

static inline uint8_t hid_report_len(enum hid_report r)
{
	return (r == HID_REPORT_KEYBOARD) ? KEYBOARD_REPORT_LEN : CONSUMER_REPORT_LEN;
}

#endif /* HID_DESC_H */
