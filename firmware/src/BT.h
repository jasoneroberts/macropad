#ifndef BT_H
#define BT_H

#include <stdbool.h>
#include <stdint.h>

#include "HID_Desc.h"

int bt_init(void);

/* True while a host is connected */
bool bt_hid_is_connected(void);

/* True while advertising (waiting for a host to connect or pair) */
bool bt_hid_is_advertising(void);

/* Notify the connected host(s) of an input report (payload without the report
 * ID; Bluetooth carries the ID in the characteristic). Call from one thread only. */
int bt_hid_send(enum hid_report report, const uint8_t *payload);

/* Battery level for the Battery Service, 0-100 */
void bt_set_battery_level(uint8_t percent);

#endif /* BT_H */
