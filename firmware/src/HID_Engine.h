#ifndef HID_ENGINE_H
#define HID_ENGINE_H

/* Turns key and knob events into HID reports and sends them over USB when a PC
 * is plugged in, otherwise over Bluetooth. Never returns. */
void hid_engine_run(void);

/* Called by USB_Link.c and BT.c when a link comes up or goes down */
void hid_engine_link_changed(void);

#endif /* HID_ENGINE_H */
