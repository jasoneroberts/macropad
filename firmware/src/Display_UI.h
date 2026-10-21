#ifndef DISPLAY_UI_H
#define DISPLAY_UI_H

#include <stdbool.h>
#include <stdint.h>

/* Starts the UI thread, which owns LVGL. Returns -ENODEV without a display. */
int display_ui_init(void);

/* Safe to call from any thread: these only queue a message for the UI thread */
void display_ui_key(uint8_t key, bool pressed);
void display_ui_knob(int dir);
void display_ui_link(bool usb, bool ble, bool advertising);
/* percent is 0-100, or DISPLAY_UI_ON_USB while USB powers the board (charging) */
#define DISPLAY_UI_ON_USB (-1)
void display_ui_battery(int percent);

#endif /* DISPLAY_UI_H */
