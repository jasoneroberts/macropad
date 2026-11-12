# JR component library

Jase's shared parts library: the macropad's parts, the Gameball carrier's parts, and room for later boards. It's built for hand-soldered boards ordered from JLCPCB with parts from LCSC, so every part is leaded (0805, SOD-123, SMA, SOT-23, through-hole) and carries its LCSC number where LCSC stocks it.

Its home on Jase's PC is `D:\Jase\Nas\Engineering\PCB Design\Altium\Libraries\`. This folder is the source it's generated from.

## How it's organised

Three layers, the same in Altium and KiCad:

| Layer | What it is | Example |
|---|---|---|
| **Symbol** | The schematic drawing and its pins. One per kind of part, shared by every value. | `R`, `D`, `SW_Key`, `SuperMini_nRF52840` |
| **Footprint** | The copper pads, holes, silkscreen and outline on the PCB. One per package. | `R_0805_2012Metric`, `D_SOD-123` |
| **Component** (part) | One orderable part: a symbol plus a footprint plus its data. This is what you place. | `R_100k_0805` = symbol `R` + footprint `R_0805_2012Metric` + value 100k + YAGEO/UNI-ROYAL part number + LCSC C149504 |

Every component has the same parameters: **Value** (the Comment in Altium), **Description**, **Manufacturer**, **Manufacturer Part Number** and **LCSC**. Altium's BOM report and JLCPCB's parts matching read these. In the EAGLE file they're called `MANUFACTURER`, `MPN`, `LCSC` and `DESCRIPTION`, because EAGLE attribute names can't have spaces; the macropad's Altium guide shows how to rename them after the import.

Component names say what you'd search for: type, then value or part number, then package (`C_10u_0805`, `D_1N4148W_SOD-123`, `Q_DMG2305UX_SOT-23`). Designator prefixes follow the usual letters: R, C, D, Q, U, J (connectors you plug into), CN (board-to-board), SW, ENC, TP, H.

## One library for every project

JR is the only library to place parts from, on every board (the macropad, the Gameball carrier and anything later). A fix (a footprint, an LCSC number) is then made once and every board picks it up with Tools » Update From Libraries.

- **Source of truth for the parts:** the generator in `src/` (this repo). It writes `JR.lbr`, which Altium 19 imports. Ask Claude to add or change a part and it rebuilds `JR.lbr`, `JR_parts.csv` and `JR_preview.pdf`.
- **After the first Altium import:** the Altium files (`JR.SchLib`, `JR.PcbLib`, `JR.IntLib` in `D:\Jase\Nas\Engineering\PCB Design\Altium\Libraries\`) are the master for anything you edit there. Tell Claude what you changed and it is carried back to the generator, so the two never drift.
- **Install it once, for all projects:** in Altium, Components panel, the menu at the top right, **File-based Libraries Preferences**, **Installed**, **Install**, pick `JR.IntLib`. It then appears in every project.
- **New board:** make a new PCB project, place parts from the JR library in the Components panel. A part that isn't in it yet: ask for it (with the LCSC number if you have one) rather than drawing it inside the board, so it joins the library.
- **Checking it:** `check_boards.py` compares every footprint on a board with the JR footprint of the same name (pad numbers, positions, sizes, drills). It reports 0 differences for the macropad (40 parts) and the Gameball carrier (15 parts), so relinking either board to JR does not move or change a pad.
- **The Gameball carrier** was built before JR existed, so its parts are generic (`R` with a value, `C`, and so on). `carrier-relink.csv` says which JR part each designator becomes. Do it after the carrier is routed: it changes nothing on the copper, only which library each part comes from, and adds the manufacturer part number and LCSC number to its BOM. The XIAO symbol now shows `D0/P0.02`-style pin names like the carrier's schematic.

Version log: 2026-11-11, 22 parts for the macropad and the carrier (XIAO pins named D0/P0.02 etc.).

## Parts

| Part | Footprint | LCSC | Used on |
|---|---|---|---|
| SuperMini_nRF52840 | SuperMini_nRF52840 | (AliExpress) | macropad |
| XIAO_nRF52840 | XIAO_nRF52840_SMD | (The Pi Hut) | carrier |
| SW_Kailh_MX_Hotswap | SW_Kailh_MX_Hotswap | C2803348 | macropad |
| Encoder_PEC11R-4220F-S0024 | RotaryEncoder_EC11_Switch_NPTH | C143797 | macropad |
| SW_Slide_OS102011MA1QN1 | SW_Slide_SPDT_Angled_CK_OS102011MA1Q | C226259 | macropad |
| SW_Tact_TS-1187A-B-A-B | SW_Push_1P1T_XKB_TS-1187A | C318884 | macropad |
| D_1N4148W_SOD-123 | D_SOD-123 | C81598 | macropad |
| D_SS14_SMA | D_SMA | C2480 | carrier |
| Q_DMG2305UX_SOT-23 | SOT-23 | C150470 | carrier |
| R_2k2_0805, R_100k_0805 | R_0805_2012Metric | C114561, C149504 | carrier |
| C_10n_0805, C_1u_0805, C_10u_0805 | C_0805_2012Metric | C1710, C28323, C15850 | macropad, carrier |
| Conn_JST_PH_S2B_Horizontal | JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal | C173752 | macropad |
| Conn_JST_PH_B2B_Vertical | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | C131337 | carrier |
| Conn_Wire_Pads_1x08, _1x02 | PinHeader_1x08 / 1x02_P2.54mm_Vertical | | macropad, carrier |
| Conn_2x05_1.27mm_Shrouded | PinHeader_2x05_P1.27mm_Vertical | | carrier |
| Conn_2x04_2.00mm_Socket | PinHeader_2x04_P2.00mm_Vertical | | carrier |
| TestPoint_Pad_1.5mm | TestPoint_Pad_D1.5mm | | macropad, carrier |
| MountingHole_M2 | MountingHole_2.2mm_M2 | | macropad |

`JR_parts.csv` has the full data and `JR_preview.pdf` shows each part's symbol, footprint and parameters on its own page.

## Footprint notes

- **SuperMini_nRF52840:** the standard Pro Micro 24-pin pattern (two rows 15.24 mm apart, 2.54 mm pitch, 1.0 mm holes), drawn from the module's component side with USB-C at the top. Placed on the bottom layer it comes out right for a module hanging under the board with its components facing down (its back toward the PCB), as on the macropad. The three inner pins at the far end are not used and have no holes.
- **SW_Kailh_MX_Hotswap:** drawn from the socket side with its two pads on the top copper, because EAGLE can only hold surface-mount pads on top. **Always place it on the bottom layer**: the holes then line up under the switch and the pads land on the bottom copper. Hole and pad positions are Kailh's (same as the keyswitch-kicad-library footprint).
- **RotaryEncoder_EC11_Switch_NPTH:** EC11 pin pattern (A, C, B at 2.5 mm; S1, S2 5 mm apart), with *unplated* 2.8 x 1.5 mm slots for the mounting lugs. Unplated because on the macropad the controller sits right underneath and the lugs are trimmed flush. EAGLE can't hold slots, so after an EAGLE import they arrive as round 1.5 mm holes: turn them into slots in the PcbLib (the macropad guide, Step 4.6).
- **SW_Slide_SPDT_Angled_CK_OS102011MA1Q** and the two JST footprints have oval pads in KiCad; EAGLE stores them round at the narrow width. Make them oval again in the PcbLib if you like.
- **XIAO_nRF52840_SMD:** castellated edge pads plus the BAT+/BAT- and SWD holes, checked against Seeed's own layout on 2026-11-10 (see the carrier package).

## Using it in Altium 19

1. **File » Import Wizard » EAGLE Projects and Designs**, add `JR.lbr` as a *library file* only, output to the `D:\Jase\Nas\Engineering\PCB Design\Altium\Libraries` folder. You get `JR.SchLib` and `JR.PcbLib`.
2. **File » New » Project » Integrated Library** named `JR`, add the two files, **Compile Integrated Library**. That makes `JR.IntLib` and installs it in the Components panel.
3. Place parts from the **Components** panel. To change a part for every design: edit the SchLib/PcbLib, recompile, then in each design **Tools » Update From Libraries**.

The macropad guide (`pcb/B/altium/README.md`, Step 1) has the same steps with what to check at each one.

## Rebuilding

The library is generated, so it can be checked and rebuilt in the cloud as well as edited in Altium:

```
/usr/bin/python3 pcb/library/src/build_library.py       # JR.lbr, JR.pretty, JR.kicad_sym, JR_parts.csv (needs KiCad 7's pcbnew)
python3 pcb/library/src/preview.py                      # JR_preview.pdf (needs kicad-cli, cairosvg, matplotlib)
/usr/bin/python3 pcb/library/src/check_boards.py       # every footprint on the macropad and carrier boards still equals JR's
```

- `src/jr_parts.py`: the part table (symbol, footprint, value, description, manufacturer, part number, LCSC).
- `src/jr_symbols.py`: the symbols, pins on the 2.54 mm grid.
- `src/jr_footprints.py`: the footprints drawn here (SuperMini, hot-swap socket, encoder) and the ones copied from KiCad's stock libraries.
- `src/eagle.py`: writes EAGLE XML, shared with the board export.

Once the library lives in Altium and you edit it there, the Altium files are the master. Tell me if you want a change carried back here.
