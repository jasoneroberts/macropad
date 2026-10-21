#ifndef PAD_INPUT_H
#define PAD_INPUT_H

#include <stdint.h>
#include <zephyr/kernel.h>

/* TYPES */
enum pad_event_type {
	PAD_EVT_KEY,    /* key: index, value: 1 pressed / 0 released */
	PAD_EVT_KNOB,   /* value: clicks turned, + clockwise */
};

struct pad_event {
	uint8_t type;
	uint8_t key;
	int8_t value;
};

/* Wait for the next key or knob event (filled in by the input subsystem's thread) */
int pad_event_get(struct pad_event *evt, k_timeout_t timeout);

#endif /* PAD_INPUT_H */
