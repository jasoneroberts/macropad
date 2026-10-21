#ifndef KEYMAP_H
#define KEYMAP_H

#include <stdint.h>

/* CONSTANTS */
#define KEY_ROWS       CONFIG_MACROPAD_KEY_ROWS
#define KEY_COLS       CONFIG_MACROPAD_KEY_COLS
#define KEY_COUNT      (KEY_ROWS * KEY_COLS)
#define KEY_KNOB_PUSH  16                 /* the knob's push switch, the same on every pad */
#define KEY_TOTAL      (KEY_KNOB_PUSH + 1)

/* Consumer page usages (HID Usage Tables, page 0x0C) */
#define CC_SCAN_NEXT   0x00B5
#define CC_SCAN_PREV   0x00B6
#define CC_PLAY_PAUSE  0x00CD
#define CC_MUTE        0x00E2
#define CC_VOLUME_UP   0x00E9
#define CC_VOLUME_DOWN 0x00EA
#define CC_CALCULATOR  0x0192

/* TYPES */
enum action_type {
	ACTION_NONE = 0,
	ACTION_KEY,        /* keyboard shortcut: modifiers + one key usage */
	ACTION_CONSUMER,   /* media / volume key */
};

struct pad_action {
	uint8_t type;       /* enum action_type */
	uint8_t mods;       /* HID_KBD_MODIFIER_* bits, ACTION_KEY only */
	uint16_t usage;     /* keyboard usage (ACTION_KEY) or consumer usage */
	const char *icon;   /* LVGL symbol shown on the tile */
	const char *label;  /* short name shown on the tile */
};

/* key: 0 .. KEY_COUNT - 1 for the MX keys (row * KEY_COLS + col), KEY_KNOB_PUSH (16) for the knob */
const struct pad_action *keymap_key(uint8_t key);

/* dir: +1 for one click clockwise, -1 for anticlockwise */
const struct pad_action *keymap_knob(int dir);

#endif /* KEYMAP_H */
