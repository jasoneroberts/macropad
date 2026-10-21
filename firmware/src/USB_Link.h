#ifndef USB_LINK_H
#define USB_LINK_H

#include <stdbool.h>
#include <stdint.h>

#include "HID_Desc.h"

int usb_link_init(void);

/* True once a host has configured the HID interface */
bool usb_link_is_ready(void);

/* Send one input report (payload without the report ID). Blocks until the host
 * has collected it, about 1 ms. If the PC is asleep it asks it to wake instead
 * and returns -EAGAIN. Call from one thread only. */
int usb_link_send(enum hid_report report, const uint8_t *payload);

#endif /* USB_LINK_H */
