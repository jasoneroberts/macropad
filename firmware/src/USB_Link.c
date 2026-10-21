#include "USB_Link.h"

#include <errno.h>
#include <string.h>

#include <sample_usbd.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>
#include <zephyr/sys/atomic.h>
#include <zephyr/usb/class/usbd_hid.h>
#include <zephyr/usb/usbd.h>

#include "HID_Engine.h"

LOG_MODULE_REGISTER(usb_link, LOG_LEVEL_INF);

/* CONSTANTS */
enum usb_state_bit {
	USB_STATE_READY,       /* host has configured the interface */
	USB_STATE_SUSPENDED,   /* host is asleep (bus suspended) */
};

/* TYPES */
static const struct device *hid_dev;
static struct usbd_context *usbd;
static atomic_t usb_state;

/* The USB controller reads reports straight from RAM (EasyDMA), so the buffers
 * have to be static and suitably aligned: UDC_STATIC_BUF_DEFINE does both.
 * One extra byte for the report ID in front. */
UDC_STATIC_BUF_DEFINE(kb_buf, 1 + KEYBOARD_REPORT_LEN);
UDC_STATIC_BUF_DEFINE(cc_buf, 1 + CONSUMER_REPORT_LEN);

static void hid_iface_ready(const struct device *dev, const bool ready)
{
	ARG_UNUSED(dev);
	LOG_INF("USB HID interface %s", ready ? "ready" : "not ready");
	atomic_set_bit_to(&usb_state, USB_STATE_READY, ready);
	hid_engine_link_changed();
}

/* Hosts may ask for the current input report (Get_Report). We have nothing
 * useful to add, so report "no keys" for the keyboard and refuse the rest. */
static int hid_get_report(const struct device *dev, const uint8_t type, const uint8_t id,
			  const uint16_t len, uint8_t *const buf)
{
	ARG_UNUSED(dev);

	if (type == HID_REPORT_TYPE_INPUT && id == REPORT_ID_KEYBOARD &&
	    len >= 1 + KEYBOARD_REPORT_LEN) {
		buf[0] = REPORT_ID_KEYBOARD;
		memset(&buf[1], 0, KEYBOARD_REPORT_LEN);
		return 1 + KEYBOARD_REPORT_LEN;
	}

	return -ENOTSUP;
}

static const struct hid_device_ops hid_ops = {
	.iface_ready = hid_iface_ready,
	.get_report = hid_get_report,
};

/* USB stack messages: cable in/out and host sleep/wake */
static void usbd_msg_cb(struct usbd_context *const ctx, const struct usbd_msg *msg)
{
	switch (msg->type) {
	case USBD_MSG_VBUS_READY:
		/* Cable plugged in: only now switch the USB controller on, which
		 * keeps it off (and saves battery) while running on the LiPo */
		if (usbd_can_detect_vbus(ctx) && usbd_enable(ctx) != 0) {
			LOG_ERR("Failed to enable USB");
		}
		break;
	case USBD_MSG_VBUS_REMOVED:
		if (usbd_can_detect_vbus(ctx) && usbd_disable(ctx) != 0) {
			LOG_ERR("Failed to disable USB");
		}
		break;
	case USBD_MSG_SUSPEND:
		atomic_set_bit(&usb_state, USB_STATE_SUSPENDED);
		hid_engine_link_changed();
		break;
	case USBD_MSG_RESUME:
		atomic_clear_bit(&usb_state, USB_STATE_SUSPENDED);
		hid_engine_link_changed();
		break;
	default:
		break;
	}
}

int usb_link_init(void)
{
	int ret;

	hid_dev = DEVICE_DT_GET_ONE(zephyr_hid_device);
	if (!device_is_ready(hid_dev)) {
		LOG_ERR("HID device is not ready");
		return -EIO;
	}

	ret = hid_device_register(hid_dev, hid_report_desc, hid_report_desc_len, &hid_ops);
	if (ret != 0) {
		LOG_ERR("Failed to register HID device, %d", ret);
		return ret;
	}

	/* Builds the device from every USB class in devicetree: the HID keyboard,
	 * plus the CDC ACM log port on the Pro Micro */
	usbd = sample_usbd_init_device(usbd_msg_cb);
	if (usbd == NULL) {
		LOG_ERR("Failed to initialize USB device");
		return -ENODEV;
	}

	/* Controllers that cannot see VBUS get switched on now; the nRF52840 can,
	 * so it waits for USBD_MSG_VBUS_READY instead */
	if (!usbd_can_detect_vbus(usbd)) {
		ret = usbd_enable(usbd);
		if (ret != 0) {
			LOG_ERR("Failed to enable USB, %d", ret);
			return ret;
		}
	}

	LOG_INF("USB HID ready to enumerate");
	return 0;
}

bool usb_link_is_ready(void)
{
	return atomic_test_bit(&usb_state, USB_STATE_READY);
}

int usb_link_send(enum hid_report report, const uint8_t *payload)
{
	uint8_t *buf = (report == HID_REPORT_KEYBOARD) ? kb_buf : cc_buf;
	uint8_t len = hid_report_len(report);

	if (!usb_link_is_ready()) {
		return -ENOTCONN;
	}

	if (atomic_test_bit(&usb_state, USB_STATE_SUSPENDED)) {
		/* Works only if the host enabled remote wake-up for this device */
		if (IS_ENABLED(CONFIG_SAMPLE_USBD_REMOTE_WAKEUP) && usbd_wakeup_request(usbd) == 0) {
			LOG_INF("Asked the host to wake up");
		}
		return -EAGAIN;
	}

	buf[0] = hid_report_id(report);
	memcpy(&buf[1], payload, len);

	return hid_device_submit_report(hid_dev, 1 + len, buf);
}
