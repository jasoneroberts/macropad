#include "Keymap.h"

#include <lvgl.h>
#include <zephyr/sys/util.h>
#include <zephyr/usb/class/hid.h>

/* MACROS */
#define CTRL  HID_KBD_MODIFIER_LEFT_CTRL
#define SHIFT HID_KBD_MODIFIER_LEFT_SHIFT
#define ALT   HID_KBD_MODIFIER_LEFT_ALT
#define WIN   HID_KBD_MODIFIER_LEFT_UI

#define KEY(m, k, i, l)  { .type = ACTION_KEY, .mods = (m), .usage = (k), .icon = (i), .label = (l) }
#define MEDIA(u, i, l)   { .type = ACTION_CONSUMER, .usage = (u), .icon = (i), .label = (l) }

/* CONSTANTS */
/* Default layout for Windows, written for the largest pad (4 x 4, concept C).
 * Smaller pads use the top-left corner: B drops the last row, A also drops the
 * last column. Row 0 is the back row, nearest the screen. The config app will
 * replace this table from settings later; for now edit it here. */
static const struct pad_action layout[4][4] = {
	{
		KEY(CTRL, HID_KEY_C, LV_SYMBOL_COPY, "Copy"),
		KEY(CTRL, HID_KEY_V, LV_SYMBOL_PASTE, "Paste"),
		KEY(CTRL, HID_KEY_Z, LV_SYMBOL_LEFT, "Undo"),
		KEY(CTRL, HID_KEY_Y, LV_SYMBOL_RIGHT, "Redo"),
	},
	{
		KEY(WIN | SHIFT, HID_KEY_S, LV_SYMBOL_IMAGE, "Snip"),
		KEY(WIN, HID_KEY_D, LV_SYMBOL_HOME, "Desktop"),
		KEY(WIN, HID_KEY_TAB, LV_SYMBOL_LIST, "Tasks"),
		KEY(WIN, HID_KEY_L, LV_SYMBOL_EYE_CLOSE, "Lock"),
	},
	{
		MEDIA(CC_SCAN_PREV, LV_SYMBOL_PREV, "Prev"),
		MEDIA(CC_PLAY_PAUSE, LV_SYMBOL_PLAY, "Play"),
		MEDIA(CC_SCAN_NEXT, LV_SYMBOL_NEXT, "Next"),
		/* Windows 11: mute the mic in the call app */
		KEY(WIN | ALT, HID_KEY_K, LV_SYMBOL_AUDIO, "Mic"),
	},
	{
		MEDIA(CC_CALCULATOR, LV_SYMBOL_PLUS, "Calc"),
		KEY(WIN, HID_KEY_E, LV_SYMBOL_DIRECTORY, "Files"),
		KEY(WIN, HID_KEY_I, LV_SYMBOL_SETTINGS, "Settings"),
		KEY(WIN, HID_KEY_DOT, LV_SYMBOL_KEYBOARD, "Emoji"),
	},
};

static const struct pad_action knob_push = MEDIA(CC_MUTE, LV_SYMBOL_MUTE, "Mute");
static const struct pad_action knob_cw = MEDIA(CC_VOLUME_UP, LV_SYMBOL_VOLUME_MAX, "Vol +");
static const struct pad_action knob_ccw = MEDIA(CC_VOLUME_DOWN, LV_SYMBOL_VOLUME_MID, "Vol -");
static const struct pad_action no_action = { .type = ACTION_NONE, .icon = "", .label = "" };

BUILD_ASSERT(KEY_ROWS <= 4 && KEY_COLS <= 4, "layout[][] covers up to 4 x 4 keys");

const struct pad_action *keymap_key(uint8_t key)
{
	if (key == KEY_KNOB_PUSH) {
		return &knob_push;
	}

	if (key >= KEY_COUNT) {
		return &no_action;
	}

	return &layout[key / KEY_COLS][key % KEY_COLS];
}

const struct pad_action *keymap_knob(int dir)
{
	return (dir > 0) ? &knob_cw : &knob_ccw;
}
