# Macropad firmware (starter)

Zephyr / nRF Connect SDK v3.3.0 app for the macropad: MX keys and an EC11 knob in, keyboard and media keys out over USB or Bluetooth, and a screen of tiles that mirrors the keys. Same SDK, USB helper and Bluetooth HID service as the trackball.

It compiles for six targets (checked 2026-10-21 in a clean NCS v3.3.0 install, no warnings from this code):

| Target | Flash | RAM |
|---|---|---|
| nRF52840 DK, concept B screen | 526 KB (50 %) | 108 KB (41 %) |
| Pro Micro nRF52840, concept B | 529 KB (65 % of the 792 KB app area) | 108 KB (41 %) |
| Pro Micro, concept A / C | 529 KB | 104 / 101 KB |
| DK, concept A / C screen | 527 KB | 105 / 102 KB |

Nothing has run on hardware yet. Ready-made images for concept B are in `prebuilt/`.

## What it does

- **Keys** send Windows shortcuts or media keys (table below). Holding a key holds the shortcut, so auto-repeat works.
- **Knob** turns volume up and down; pressing it mutes.
- **Screen** shows one tile per key in the same layout, lit while the key is held; the status bar shows the link (USB, Bluetooth, waiting), the knob action and the battery level. The backlight goes off after 60 s without input and comes back on the next key or turn.
- **USB** wins whenever a PC has the macropad configured; otherwise reports go over **Bluetooth** to the paired PC. A key press while the PC is asleep asks it to wake up (USB remote wake-up).
- **Battery** level (Pro Micro only) is read once a minute and shown to Windows through the Battery Service.
- **Firmware update without opening the case** (Pro Micro): hold the top-left key and press the knob for 3 s. The board restarts as a USB drive; copy `zephyr.uf2` onto it.

## Default layout

Row 0 is the back row, next to the screen. Concept B uses rows 0-2, A uses rows 0-2 and columns 0-2, C uses everything.

| | col 0 | col 1 | col 2 | col 3 |
|---|---|---|---|---|
| row 0 | Copy (Ctrl+C) | Paste (Ctrl+V) | Undo (Ctrl+Z) | Redo (Ctrl+Y) |
| row 1 | Snip (Win+Shift+S) | Desktop (Win+D) | Task view (Win+Tab) | Lock (Win+L) |
| row 2 | Previous track | Play / pause | Next track | Mic mute (Win+Alt+K) |
| row 3 | Calculator | Explorer (Win+E) | Settings (Win+I) | Emoji (Win+.) |

Knob: volume up / down, push = mute. Change them in `src/Keymap.c`; later the config app will edit them and store them in settings, as on the trackball.

## Build and flash

From an NCS v3.3.0 toolchain shell (nRF Connect for VS Code terminal, or `nrfutil toolchain-manager launch`), in the folder that holds `firmware`:

```
# nRF52840 DK (breadboard set-up, wiring at the top of boards/nrf52840dk_nrf52840.overlay)
west build -p -b nrf52840dk/nrf52840 -d build_dk firmware
west flash -d build_dk

# SuperMini nRF52840 (Zephyr calls it the Pro Micro), concept B
west build -p -b promicro_nrf52840/nrf52840/uf2 -d build_pm firmware
```

To flash the Pro Micro, double-tap its RST pin to GND (or use the key combo once this firmware is on it). A USB drive appears; copy `build_pm/firmware/zephyr/zephyr.uf2` onto it. The board restarts into the new firmware by itself. The UF2 bootloader that ships on these boards stays in place, so there is no MCUboot or signing key on this project yet.

Concepts A and C add a config fragment and an overlay:

```
west build -p -b promicro_nrf52840/nrf52840/uf2 -d build_a firmware -- -DEXTRA_CONF_FILE=concepts/a.conf -DEXTRA_DTC_OVERLAY_FILE=concepts/a.overlay
west build -p -b nrf52840dk/nrf52840 -d build_c_dk firmware -- -DEXTRA_CONF_FILE=concepts/c.conf -DEXTRA_DTC_OVERLAY_FILE=concepts/c_display.overlay
```

(`a_display.overlay` / `c_display.overlay` change only the screen, for the DK; `a.overlay` / `c.overlay` add the key matrix for the Pro Micro.)

**Logs:** on the DK, the J-Link serial port and RTT, like the trackball. On the Pro Micro, a second USB device appears next to the keyboard: a serial port carrying the log (any baud rate). Logging starts 4 s after power-up so there is time to open the port.

## Check on first power-up

These come from datasheets and demo code, not from parts on the bench:

1. **Screen orientation.** If the tiles are mirrored or upside down, change `mdac` in the overlay (0x70, 0xa0, 0x60, 0xc0 are the four landscape options).
2. **Colours.** If they look inverted (white background), add `inversion-off;` to the `lcd` node.
3. **Knob direction.** If clockwise turns the volume down, swap the two `gpios` lines in the `knob` node.
4. **LCD power on the Pro Micro.** If the backlight never comes on, measure the VCC pin: it should be 3.3 V once the firmware runs (P0.13 high).
5. **Battery reading.** Unplug USB, compare the log's "Battery ... mV" with a multimeter across the LiPo, and put the difference in `CONFIG_MACROPAD_BATTERY_OFFSET_MV` (prj.conf). The percentage comes from a rough LiPo curve in `src/Battery.c`.

**Test a SuperMini before soldering it:** plug it into the PC on its own and copy `prebuilt/macropad_B_promicro.uf2` onto it (double-tap RST to GND first if no USB drive appears). It should show up as a keyboard plus a serial port carrying the log, and advertise over Bluetooth as "Macropad". Pairing it with the PC proves the radio and clock; a dud board fails here, before it is soldered in.

## How it is put together

```
input subsystem thread          main thread (priority 0)           UI thread (priority 7)
gpio-kbd-matrix ─┐                                                  owns LVGL, nobody else
  input-keymap ──┼─ Pad_Input.c ─ pad_q ─> HID_Engine.c ──> USB_Link.c ──> PC (USB)
gpio-qdec ───────┘   (codes F13+n)          builds reports  └─> BT.c ──────> PC (Bluetooth)
                                            │
                                            └─ ui_q ─────────> Display_UI.c ──> ST7789 / GC9A01
```

- `boards/*.overlay` describe the hardware: which pins are rows and columns, the knob, the LCD and its SPI bus, the backlight PWM, the battery ADC channel. Devicetree gives every key the input code `INPUT_KEY_F13 + n` (knob push = key 16), so the C code is the same on the DK (gpio-keys) and on the matrix (input-keymap).
- `Pad_Input.c` listens to every input event and queues just the key and knob ones. Input callbacks run on the input subsystem's thread, so it does no real work there.
- `HID_Engine.c` keeps the set of held keys and turns it into reports: the 8-byte keyboard report (modifier bits, six key slots) and a 2-byte consumer report (one media usage). It decides USB or Bluetooth per report.
- `HID_Desc.c` is the one report descriptor both links use. USB puts the report ID in front of each report; Bluetooth carries it in the characteristic instead, which is why the send functions take the payload without the ID.
- `USB_Link.c` registers the HID device with the same `sample_usbd` helper as the trackball, and switches the USB controller on only while a cable is plugged in.
- `BT.c` is the NCS keyboard sample cut down: one host at a time, Just Works pairing, fast advertising for 30 s then slow to save battery, bonds kept in settings.
- `Display_UI.c` builds the tiles from the keymap, and is the only code that touches LVGL (LVGL is not thread-safe). Other code posts small messages to it.
- `Battery.c` reads VDDH / 5 with the SAADC. On the SuperMini the LiPo feeds VDDH, so no resistor divider is needed. While USB is plugged in VDDH comes from USB (about 5 V) instead, so the battery can't be read then: the status bar shows "USB" with a charge symbol, and Windows keeps the last level.
- `boards/promicro_nrf52840_nrf52840_uf2.conf` runs Bluetooth's 32 kHz clock from the chip's own RC oscillator. Some SuperMini batches have a faulty 32.768 kHz crystal, and the symptom (Bluetooth that never connects or keeps dropping) is hard to trace back to it. The RC clock costs a few microamps; delete the `K32SRC_RC` line to try the crystal.
- `sysbuild.conf` turns off NCS's Partition Manager so the devicetree flash layout is used. That keeps the Pro Micro app at 0x26000, where its UF2 bootloader expects it.

## Next steps

Keymap in settings and editable from the config app (a vendor HID report like the trackball's), the pairing passkey shown on the screen, profiles (a different layout per app), and MCUboot with Bluetooth updates once the hardware works.
