#include "Pad_Input.h"

#include <zephyr/input/input.h>
#include <zephyr/logging/log.h>
#include <zephyr/sys/util.h>

#include "Keymap.h"

LOG_MODULE_REGISTER(pad_input, LOG_LEVEL_INF);

/* CONSTANTS */
/* Devicetree gives every key the code INPUT_KEY_F13 + its index (gpio-keys on the
 * DK, input-keymap on the matrix), so both boards look the same from here. */
#define KEY_CODE_FIRST INPUT_KEY_F13
#define KEY_CODE_LAST  (INPUT_KEY_F13 + KEY_KNOB_PUSH)

K_MSGQ_DEFINE(pad_q, sizeof(struct pad_event), 16, 4);

/* Runs on the input subsystem's thread for every event from every input device.
 * It only translates and queues, so the HID work happens on the engine thread. */
static void input_cb(struct input_event *evt, void *user_data)
{
	struct pad_event pe;

	ARG_UNUSED(user_data);

	if (evt->type == INPUT_EV_KEY && evt->code >= KEY_CODE_FIRST && evt->code <= KEY_CODE_LAST) {
		pe.type = PAD_EVT_KEY;
		pe.key = (uint8_t)(evt->code - KEY_CODE_FIRST);
		pe.value = evt->value ? 1 : 0;
	} else if (evt->type == INPUT_EV_REL && evt->code == INPUT_REL_WHEEL) {
		pe.type = PAD_EVT_KNOB;
		pe.key = 0;
		pe.value = (int8_t)CLAMP(evt->value, INT8_MIN, INT8_MAX);
	} else {
		/* e.g. the matrix's raw row/column events, which input-keymap turns into keys */
		return;
	}

	if (k_msgq_put(&pad_q, &pe, K_NO_WAIT) != 0) {
		LOG_WRN("Input queue full, event dropped");
	}
}

INPUT_CALLBACK_DEFINE(NULL, input_cb, NULL);

int pad_event_get(struct pad_event *evt, k_timeout_t timeout)
{
	return k_msgq_get(&pad_q, evt, timeout);
}
