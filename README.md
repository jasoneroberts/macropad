# Macropad with a screen

A wireless macropad with MX keys, an EC11 knob and a small LCD that shows what each key does. It is built on the same nRF52840 / Zephyr / nRF Connect SDK stack as the [trackball](https://github.com/jasoneroberts/NordicMouseProject), with a 3D-printed case and a hand-soldered PCB. Started 2026-10-20.

Status 2026-10-21: concept B (12 keys, 2.0″ screen) and the SuperMini nRF52840 controller are chosen. The case model, firmware and PCB inputs exist for all three concepts; the firmware compiles but has not run on hardware yet, and nothing has been printed. Next: buy the screen and an EC11 knob and try the firmware on the nRF52840 DK.

| | A · Pocket | B · Studio (chosen) | C · Deck |
|---|---|---|---|
| Keys | 3 × 3 MX hot-swap | 4 × 3 MX hot-swap | 4 × 4 MX hot-swap |
| Knob (EC11) | Ø26 | Ø28 | Ø36 |
| Screen | 1.69″ ST7789V2 240 × 280, portrait | 2.0″ ST7789 320 × 240, landscape | 1.28″ GC9A01 240 × 240, round |
| Footprint on desk | 76 × 122 mm | 101 × 118 mm | 92 × 142 mm |
| Height front / rear | 12.5 / 25.1 mm | 12.5 / 24.6 mm | 12.5 / 29.5 mm |
| Tilt | 6° | 6° | 7° |
| LiPo | 603040 | 603040 | 803040 |

Heights are without the 10 mm rubber feet (add about 2 mm).

## Folder

| Path | What |
|---|---|
| `scad/macropad.scad` | The parametric model. Every dimension is a named parameter at the top. |
| `stl/<A,B,C>/print/` | `top`, `bottom`, `knob`, `clamp`, already oriented for the printer bed. |
| `stl/<A,B,C>/view/` | Every part and dummy component (PCB, switches, display, controller, battery) in the assembled position. Made by `tools/build.py`; not kept in git. |
| `stl/test_coupon.stl` | Print this first: switch holes 13.9 / 14.0 / 14.1 / 14.2 (1 to 4 dots) and two insert holes. |
| `dxf/pcb_outline_<c>.dxf` | Main PCB outline with MX centre holes (Ø4) and pillar holes (Ø2.2), for Altium. Plate-frame mm, origin at the case's front-left corner. |
| `build/report_<c>.json` | Dimensions and positions of everything, plus the fit-check result. |
| `build/viewer_<c>.glb` | Coloured assembly. Opens in Windows 3D Viewer. |
| `build/fitcheck.txt` | Overlap check between all parts. Should say `OK` for each concept. |
| `page/index.html` | The concept comparison page with 3D viewers. Made by `tools/make_page.py`; not kept in git. |
| `tools/` | `build.py` (STLs, DXF, report, fit check, GLB), `drawings.py` (plan and section SVGs), `make_page.py` + `page_template.html`, `build_firmware.sh` (Linux: installs NCS v3.3.0 and builds all six firmware variants; CI runs it too). |
| `firmware/` | Zephyr / NCS v3.3.0 app: keys, knob, LVGL screen, USB + Bluetooth HID. See `firmware/README.md`. |
| `firmware/prebuilt/` | Ready-to-flash concept B images: `macropad_B_promicro.uf2` and `macropad_B_dk.hex`. GitHub Actions also builds them on every firmware change (the run's "Artifacts"). |
| `pcb/` | `generate.py` and, per concept, BOM, netlist, placement and outline for Altium. See `pcb/README.md`. |
| `SHOPPING.md` | What to buy for B (UK prices) and what to measure when it arrives. |
| `LICENSES/` | Upstream licences for the files based on Nordic and Zephyr samples (see "Licences" below). |

## Rebuild after changing a parameter

Needs OpenSCAD 2021.01 or newer, Python 3 and `pip install trimesh manifold3d numpy scipy networkx`.

From the repo root:

```
python tools/build.py          # all concepts (or: build.py B)
python tools/drawings.py
python pcb/generate.py         # needs pip install shapely
python tools/make_page.py page
```

To export one part by hand: `openscad -D 'concept="B"' -D 'part="top_print"' -o top.stl scad/macropad.scad`. Open the file in the OpenSCAD GUI to use the Customizer for `concept` and `part`.

## Measure before printing

These come from listings or datasheets, not from parts on the bench:

- Display glass outline, thickness and where the active area sits on the glass (`LCD169`, `LCD200`, `GC9A01` tables). Board sizes and active areas are from Waveshare; glass outlines are estimates.
- EC11 body height above the PCB (`enc_body_h`, 6.5) and shaft length (`enc_shaft_l`, 15).
- Heat-set insert hole (`insert_d` 4.0, `insert_len` 4.0 for M3 × 4 short inserts).
- LiPo size (`LIPO_603040`, `LIPO_803040`).
- Switch hole (`sw_hole` 14.0): use the test coupon.

## How it's built

- Top shell = switch plate. 3 mm skin: 1.5 mm lip with the 14 mm hole, 15 mm pocket below for the MX clips. PCB top 5.0 mm below the plate top (MX standard), Kailh sockets under the PCB.
- The top surface is tilted, the bottom plate is flat, so the inside gets deeper toward the back. LiPo, controller and display stack live under the rear band.
- Display: window = active area + 0.4 mm with a 45° chamfer through a 1 mm bezel; glass in a pocket; printed clamp with two M2 screws holds the module board. Main PCB has a cut-out there; 8 wires to the module.
- Controller: SuperMini nRF52840 (chosen 2026-10-21; a nice!nano v2 also fits) on 2.5 mm headers under the PCB, component side down, USB-C through a 13 × 7.5 mm rear opening.
- Four M3 countersunk screws into M3 heat-set inserts in the corner bosses; M2 self-tapping screws for the PCB pillars and the display clamp; slide switch slot in the right wall.
- Prints without supports: top shell face down, bottom plate and clamp flat, knob top face down. Largest part is C's top shell, 92 × 140 mm.

## Licences

No licence has been chosen for the project as a whole yet, so the default applies (all rights reserved). Two kinds of file keep their upstream licence, named by the `SPDX-License-Identifier` line at the top of the file:

- `firmware/src/BT.c` is based on Nordic's `peripheral_hids_keyboard` sample: `LicenseRef-Nordic-5-Clause` (`LICENSES/LicenseRef-Nordic-5-Clause.txt`), which allows use only with Nordic chips.
- `firmware/CMakeLists.txt` and `firmware/Kconfig` come from Zephyr's USB samples: Apache-2.0 (`LICENSES/Apache-2.0.txt`).
