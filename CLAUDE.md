# CLAUDE.md

Guidance for Claude Code working in this repository.

## Project

A wireless macropad: 12 MX hot-swap keys (4 x 3), an EC11 knob with push, a 2.0″ ST7789 LCD (320 x 240, landscape) that shows one tile per key, a LiPo, a 3D-printed case and a hand-soldered 2-layer PCB. The controller is a SuperMini nRF52840 (a nice!nano v2 clone), Zephyr board `promicro_nrf52840/nrf52840/uf2`. Concept B is the one being built; concepts A (3 x 3, 1.69″) and C (4 x 4, round 1.28″ GC9A01) are kept compiling and in the model.

- The owner is Jase (UK): prices in GBP, plain UK English in docs. Jase hand-solders, so parts must be leaded (0805, SOT-23, SOD-123); no QFN, DFN or LGA. The PCB is drawn in Altium from the files in `pcb/`.
- Nothing has run on hardware yet. Screen, knob and battery details come from datasheets and listings; `firmware/README.md` lists what to check on first power-up.
- Sister project: the trackball firmware in `jasoneroberts/NordicMouseProject` (same SDK, same `sample_usbd` USB helper).

## Layout and rebuild order

- `scad/macropad.scad` is the parametric case model. `tools/build.py` makes the STLs, `dxf/pcb_outline_<c>.dxf`, `build/report_<c>.json`, the GLB viewers and the fit check; then `tools/drawings.py`, `pcb/generate.py`, `tools/make_page.py`. Needs OpenSCAD 2021.01+, `pip install trimesh manifold3d numpy scipy networkx shapely`.
- `stl/<c>/view/` and `page/` are generated and git-ignored; `stl/<c>/print/`, `dxf/`, `build/` and `pcb/<c>/` are generated but committed so they can be used without the tools.
- `firmware/` is the Zephyr app (NCS v3.3.0). `firmware/prebuilt/` holds the concept B images and must match the source: rebuild it after firmware changes.

## Firmware build

From the repo root, in an NCS v3.3.0 toolchain shell:

```
west build -p -b nrf52840dk/nrf52840 -d build_dk firmware
west build -p -b promicro_nrf52840/nrf52840/uf2 -d build_pm firmware
# concepts A / C: add  -- -DEXTRA_CONF_FILE=concepts/a.conf -DEXTRA_DTC_OVERLAY_FILE=concepts/a.overlay
# (on the DK use concepts/a_display.overlay or c_display.overlay, which change only the screen)
```

On Linux, `bash tools/build_firmware.sh setup` installs NCS, and `bash tools/build_firmware.sh` builds all six variants and refreshes `firmware/prebuilt/`. CI (`.github/workflows/firmware.yml`) runs the same script on every change under `firmware/`. The one expected warning per build is "Experimental symbol MIPI_DBI is enabled". There are no unit tests.

The build depends on `${ZEPHYR_BASE}/samples/subsys/usb/common` (`sample_usbd_init_device()`, `CONFIG_SAMPLE_USBD_*`), like the trackball.

## Firmware architecture

- `Pad_Input.c`: an input callback queues key and knob events. Key n arrives as `INPUT_KEY_F13 + n` (n = row * cols + col); the knob push is key 16 on every concept; the knob is `INPUT_REL_WHEEL` from `gpio-qdec`.
- `HID_Engine.c`: keeps the held keys, builds the 8-byte keyboard report (ID 1) and 2-byte consumer report (ID 2), sends over USB when the interface is ready, otherwise Bluetooth. On the Pro Micro, holding key 0 and the knob push for 3 s restarts into the UF2 bootloader (GPREGRET 0x57).
- `HID_Desc.c`: one report descriptor for both links. USB reports carry the report ID in front; Bluetooth ones do not.
- `USB_Link.c` (not `USB_HID`: `usb_hid_init` clashes with Zephyr's legacy USB stack), `BT.c` (NCS HIDS, one host, Just Works, bonds in settings), `Keymap.c` (the layout table), `Battery.c` (VDDH / 5 on the SAADC; above 4.4 V means USB power).
- `Display_UI.c` owns LVGL: only its thread may call LVGL; everything else posts to its queue.
- `sysbuild.conf` sets `SB_CONFIG_PARTITION_MANAGER=n` so the app stays at 0x26000, where the UF2 bootloader expects it.
- `boards/promicro_nrf52840_nrf52840_uf2.*`: key matrix, LCD on SPIM3, P0.13 VCC regulator (the SuperMini's VCC pin is off until it is high), battery ADC, RC 32 kHz clock (some SuperMini crystals are faulty). `boards/nrf52840dk_nrf52840.*`: breadboard wiring and RTT logs.

## Keep in step

- The controller pin map is in `firmware/boards/promicro_nrf52840_nrf52840_uf2.overlay`, `pcb/generate.py` (`u1_pins`, `LCD_PINS`) and `pcb/README.md`. Change them together and rerun `pcb/generate.py`.
- Matrix: rows are inputs (pull-up, active low), columns are driven low; each diode's anode is on the switch/row side, cathode to the column. Row 0 is the back row next to the screen and the top row of tiles; SW1 (back-left) is key 0.
- Nordic's "low frequency I/O only" pins (P0.02/03, P0.09/10, P0.28-31, P1.01-07, P1.10-15) must not carry the LCD's SPI clock or data.

## Conventions

- Same as the trackball: module files are PascalCase with underscores (`Display_UI.c`) with a matching header exposing `<module>_init` / `<module>_*`; functions return 0 or a negative errno; section comments such as `/* CONSTANTS */` and `/* TYPES */`.
- App options live in `firmware/Kconfig` under the "Macropad" menu (`CONFIG_MACROPAD_*`).
- `firmware/src/BT.c` keeps Nordic's copyright line and `LicenseRef-Nordic-5-Clause`; files based on other samples keep their upstream licence lines (texts in `LICENSES/`).
