#ifndef BATTERY_H
#define BATTERY_H

/* Reads the LiPo voltage once a minute and reports it to the Battery Service and
 * the screen. Returns -ENOTSUP on boards without a battery channel (the DK). */
int battery_init(void);

#endif /* BATTERY_H */
