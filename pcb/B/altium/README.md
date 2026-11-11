# Macropad concept B main board: Altium package

This folder takes the concept B main board into Altium Designer 19 as a **finished design**: schematic drawn, every part placed, every track routed, ground poured on both sides. You import it once with Altium's Import Wizard, check it, set the rules, repour, run the design rule check and make the Gerbers for JLCPCB.

Rough time: 30 minutes for the library and the import, 20 minutes for checks and rules, 10 minutes for Gerbers.

| | |
|---|---|
| Board | 95.3 x 110.45 mm, 2 layers, 1.6 mm, hand-soldered (0805, SOD-123, through-hole and the SuperMini on headers) |
| Parts | 40: U1 SuperMini nRF52840, 12 hot-swap sockets, 13 diodes, ENC1 encoder, power switch, reset switch, JST battery header, LCD wire pads, 3 capacitors, 2 test pads, 4 mounting holes |
| Nets | 35 |
| Copper | 253 track segments, 9 vias, a GND pour on each side. Every connection, ground included, is a track; the pours add shielding on top. KiCad's checks: 0 unrouted connections, 0 copper rule errors |
| Coordinates | mm in the case's plate frame: origin at the case's front-left corner, x to the right, y toward the screen end. The board's own bottom-left corner is at (2.85, 2.85) |

## What's in this folder

| Folder / file | What it is |
|---|---|
| `import-eagle/macropad_B.sch`, `macropad_B.brd` | **The design**, as EAGLE files for Altium 19's Import Wizard (Step 2). |
| `library/JR.lbr` | The whole JR component library (22 parts, the macropad's and the trackball carrier's) for Step 1. The same file is in `pcb/library/` in the repo. |
| `library/JR_parts.csv` | The library's part list: symbol, footprint, value, description, manufacturer, part number, LCSC number. |
| `reference/macropad_B-schematic.pdf` | The schematic (A3), to read alongside the imported one. |
| `reference/macropad_B-board.pdf` | The board from the top: red = top copper, blue = bottom copper, shaded = pours. |
| `reference/placement.csv` | Every part's side, X, Y, rotation and pin 1 position. |
| `reference/connections.csv` | Every pin and the net it's on. |
| `reference/BOM.csv`, `reference/order-list.csv` | Parts list, and what to buy where, with LCSC numbers. |
| `reference/gerbers-reference/` | Gerbers and drill files made by KiCad from the same board. Compare Altium's against these (Step 6). |

## How this design was made, and why it reaches Altium as EAGLE files

The design lives in the repo as Python (`pcb/board/`): `design_b.py` holds the parts, the nets, the pin map and where each part must sit for the case; `build_board.py` places the parts and draws the outline from the case model; `route.py` routes it with Freerouting and pours the ground; `schematic.py` draws the schematic. KiCad 7 is the engine underneath: it holds the board while it's built and runs the design rule check.

Altium 19 has no KiCad importer (it arrived in Altium 20.1), but it does import EAGLE. EAGLE files are plain XML, so `export_altium.py` writes the board and the schematic in EAGLE's format, and two checks run on them before they reach you:

- `check_eagle.py` reads the two files the way Altium will: every schematic pin sits on the end of a wire of its own net, nothing touches a pin of another net, and the nets built from the schematic are exactly the board's nets (35 nets, 104 pins; the only unconnected pins are U1's spare P0.08 and the power switch's unused third pin).
- KiCad's own EAGLE importer reads the board back: all 172 pads, 253 tracks and 9 vias land within 0.003 mm of the original, on the right nets.

EAGLE has a few rules that shape what you'll see after the import. None of them change the circuit:

- **Surface-mount pads have to be on the top of an EAGLE footprint.** Parts that sit on the bottom of this board are stored the normal way and placed *mirrored* (EAGLE rotation `MR...`). Altium turns that into a part on the Bottom Layer. The hot-swap socket footprint is drawn from the socket's side for the same reason; see "Library notes" below.
- **Pin names must be unique.** The SuperMini's three GND pins arrive as `GND`, `GND@4` and `GND@23`. Pin numbers (Altium's pin *designators*) are unaffected.
- **Through-hole pads can only be round or square.** Oval pads arrive round at their narrow width: the slide switch's pins (1.5 mm) and mounting legs (2.2 mm), and the battery header's pins (1.2 mm). They're still big enough to solder; Step 4.7 says how to make them oval again.
- **There are no slots.** The encoder's two mounting-lug slots arrive as round 1.5 mm holes, with the slot's outline drawn on a mechanical layer. Step 4.6 turns them back into 2.8 x 1.5 mm slots. This one matters: the lugs won't fit a round hole.

## Before you start

1. **Unzip or copy the package** to a short path, for example `C:\Users\jason\OneDrive\Documents\Projects\WirelessTrackballProject\PCB\macropad-altium\`.
2. **Close the Gameball carrier project** in Altium if it's open, so nothing from it gets mixed in.
3. **Units:** press `Q` in any PCB view until the status bar shows mm.

## Step 1: Install the JR library (once, for every design)

The JR library is your own component library: one symbol per kind of part (a resistor, a diode, the SuperMini), one footprint per package, and one *component* per orderable part that ties a symbol to a footprint and carries the part data (value, description, manufacturer, part number, LCSC number). The macropad and the carrier both use it, and new designs can too. It lives in `C:\Users\jason\OneDrive\Documents\Projects\AltiumLibrary\`.

In Altium terms you end up with:

- `JR.SchLib` (schematic symbols) and `JR.PcbLib` (footprints): the source files you edit.
- `JR.LibPkg`: an *integrated library package*, a small project that lists those two files.
- `JR.IntLib`: the compiled, read-only library that designs place parts from. You recompile it after every edit.

Steps:

1. **File » Import Wizard » Next**, pick **EAGLE Projects and Designs**, **Next**.
2. **Design files:** add nothing. **Next.**
3. **Library files:** **Add** `library\JR.lbr`. **Next.**
4. **Settings page:** tick **Log All Errors / Warnings / Events**. Set the **output directory** to `...\Projects\AltiumLibrary\`. **Next**, then **Finish**.
5. You now have `JR.SchLib` and `JR.PcbLib` in that folder (open them from **File » Open** if the wizard didn't). Open the SchLib, pick a few components in the **SCH Library** panel, and check:
   - the **Parameters** list has `MANUFACTURER`, `MPN`, `LCSC` and `DESCRIPTION` (and the **Comment** shows the value, for example `1N4148W`);
   - the **Models** list has a footprint with the same name as in `JR_parts.csv`, and its preview shows the footprint.
6. **Make the package:** **File » New » Project**, type **Integrated Library**, name `JR`, location `...\Projects\AltiumLibrary\`. Right-click `JR.LibPkg` in the **Projects** panel » **Add Existing to Project** » pick `JR.SchLib` and `JR.PcbLib`. **File » Save All.**
7. **Compile it:** right-click `JR.LibPkg` » **Compile Integrated Library JR.LibPkg**. The Messages panel should show no errors. Altium writes `Project Outputs for JR\JR.IntLib` and adds it to the **Components** panel. If the panel doesn't list it: **Components panel » ☰ » File-based Libraries Preferences » Installed » Install** and pick the `.IntLib`.
8. **Optional tidy-up**, which you can do any time (recompile afterwards):
   - Rename the parameters to Altium's usual names with **Tools » Parameter Manager** in the SchLib: `MANUFACTURER` → `Manufacturer`, `MPN` → `Manufacturer Part Number`, `DESCRIPTION` → the component's **Description** field.
   - Give the SuperMini's GND pins plain names (`GND@4` → `GND`).

*Why an IntLib and not just the two files?* The compiled library carries the symbol, footprint and parameters together, and Altium checks on compile that every symbol pin has a pad to go to. Designs then link to `JR.IntLib`, so a change you make once (a footprint fix, a new LCSC number) reaches every design with **Tools » Update From Libraries**.

## Step 2: Import the design

1. **File » Import Wizard » Next**, pick **EAGLE Projects and Designs**, **Next**.
2. **Design files:** **Add** `import-eagle\macropad_B.sch` and `import-eagle\macropad_B.brd` (Ctrl-click both, or one after the other). **Next.**
3. **Library files:** add nothing (the design files carry their own copy of the parts). **Next.**
4. **Layer mapping** (if your version shows the grid; otherwise Altium uses its defaults and you check the result in Step 3):

   | EAGLE layer | Altium layer | What's on it |
   |---|---|---|
   | 1 Top / 16 Bottom | Top Layer / Bottom Layer | Tracks, pads, the two GND pours |
   | 20 Dimension | Mechanical 1 | **Board outline** |
   | 21 tPlace / 22 bPlace | Top Overlay / Bottom Overlay | Silkscreen |
   | 25 tNames / 26 bNames | Top Overlay / Bottom Overlay | Designators |
   | 27 tValues / 28 bValues | Top Overlay / Bottom Overlay | Values (hidden) |
   | 41 tRestrict / 42 bRestrict | Keep-Out (top / bottom copper) | No copper round the four M2 screw holes |
   | 46 Milling | a spare mechanical layer, for example Mechanical 4 | Outline of the encoder's two lug slots |
   | 51 tDocu / 52 bDocu | Mechanical 13 / Mechanical 14 | Part bodies (assembly drawing) |

5. **Settings page:**
   - **General:** tick **Log All Errors / Warnings / Events**.
   - **Schematic:** **untick Recognize powerports and Recognize ports.** This design connects everything by wires and net labels; with these ticked, Altium can turn parts whose names match its patterns into port symbols.
   - **PCB:** leave **Generate 3D body** unticked.
   - **Output directory:** a new empty folder, for example `...\macropad-altium\altium-project\`.
6. **Next**, wait, **Finish**. Read the log: font and unused-layer warnings are fine; tell me about anything else.
7. **One project:** if the Projects panel shows two projects (one with the `.SchDoc`, one with the `.PcbDoc`), right-click the one with the `.SchDoc` » **Add Existing to Project** » pick the `.PcbDoc`, then close the other project. **File » Save All.**
8. **Link schematic and PCB parts:** EAGLE files don't carry Altium's hidden Unique IDs, so link them once by designator. Open the `.PcbDoc`, **Project » Component Links**, **Add Pairs Matched By** with *Designator* ticked, check all 40 parts are in the matched list, **Perform Update**. **File » Save All.**

## Step 3: Check the import (10 minutes)

1. **Compile:** **Project » Compile PCB Project**. Open **Messages**. No errors expected. EAGLE has no no-connect markers, so U1 pin 2 (P0.08) and SW_PWR pin 3 may be listed as unconnected: that's correct. Put **Place » Directives » Generic No ERC** on them for a clean list.
2. **Schematic and PCB agree:** in the `.PcbDoc`, **Design » Update PCB Document**. After Step 2.8 the list should be empty, or only offer *Rooms* and *Component Classes* (untick those). If it wants to change nets or replace parts, click **Cancel** and tell me what it lists.
3. **Board shape:** press `2`. The board is the L shape: full width at the front (keys), only the right-hand strip at the back (controller and knob), with the big opening for the screen at the back left and a dip round the screen clamp's pillar. Four corner notches clear the case's screw bosses. If the board area is a plain rectangle: click the outline on Mechanical 1, press `Tab` to select all of it, **Design » Board Shape » Define from selected objects**.
4. **Origin:** the EAGLE coordinates are the case's plate frame, so Altium's origin should already be the case's front-left corner, 2.85 mm below and left of the board's corner. If the numbers below don't match, **Edit » Origin » Set** and type or click (0, 0) accordingly.
5. **Spot-check five parts.** Click the part, read X, Y and Layer in **Properties**; then click its pin 1 pad and check the pad's position. Pin 1 is the unambiguous check for bottom-side parts, because Altium and EAGLE count rotation differently for mirrored parts.

   | Part | Layer | X | Y | Pin 1 at |
   |---|---|---|---|---|
   | U1 | Bottom | 82.000 | 96.250 | (89.620, 110.220), square pad, back right |
   | ENC1 | Top | 82.000 | 87.650 | pin A (79.500, 80.150), square pad |
   | SW1 | Bottom | 21.925 | 55.625 | pad 1 (14.840, 58.165) |
   | J2 | Bottom | 93.600 | 105.140 | pin 1 (93.600, 105.140), square pad, back end |
   | SW_RST | Bottom | 74.500 | 66.125 | pad 1 (71.500, 64.250) |

   `reference/placement.csv` has the rest.
6. **Nets:** **PCB panel » Nets**: 35 nets. 3V3_SW, COL0-COL4, DBG_TX, ENC_A, ENC_B, GND, K1-K12, K_PUSH, LCD_BL, LCD_CS, LCD_DC, LCD_MOSI, LCD_RST, LCD_SCK, NRST, ROW0-ROW2, VBAT, VBAT_SW. `reference/connections.csv` lists every pin.
7. **Tracks:** compare with `reference/macropad_B-board.pdf`. Nearly all routing is on the bottom, so the top stays one solid ground plane under the keys.

## Step 4: Rules, pours and the two fix-ups

Open **Design » Rules**. These are the values the board was routed and checked with in KiCad, with margin over JLCPCB's standard limits.

1. **Net class:** **Design » Classes » Net Classes** should have `power` with GND, VBAT, VBAT_SW and 3V3_SW. Add it if the import didn't.
2. **Electrical » Clearance:** 0.2 mm. Add a second Clearance rule, scope *InPolygon* to *All*, 0.3 mm, priority above the first: the pours keep 0.3 mm from everything else, as they did in KiCad.
3. **Routing » Width:** default min 0.2, preferred 0.25, max 1.0 mm. Second rule, scope *InNetClass('power')*: min 0.3, preferred 0.4, max 1.0 mm, priority above the default.
4. **Routing » Routing Via Style:** diameter 0.6 mm, hole 0.3 mm.
5. **Manufacturing:** **Hole Size** min 0.3, max 4.1 mm (the MX switch centre holes are 4.0 mm). **Board Outline Clearance** 0.3 mm. **Hole To Hole Clearance** 0.25 mm. **Minimum Annular Ring** 0.15 mm.
6. **Encoder lug slots.** Do this in the library so every design gets it: open `JR.PcbLib`, footprint `RotaryEncoder_EC11_Switch_NPTH`. Double-click each of the two unnamed holes at (0, ±5.6): **Hole Type: Slot**, **Hole Size 1.5 mm**, **Length 2.8 mm**, **Rotation 0**, **Plated: off**. Pad size equal to the hole, no copper. Save, recompile `JR.LibPkg`. In the design, in the `.PcbDoc`: **Tools » Update From PCB Libraries**, pick ENC1 only. On the board the slots then run front to back at x = 76.4 and 87.6, between U1's two pin rows, 0.42 mm from U1's pads. Delete the slot outlines on the milling layer afterwards (they were only there to show where the slots go).
7. **Oval pads (optional):** in the PcbLib, `SW_Slide_SPDT_Angled_CK_OS102011MA1Q` pins 1-3 back to 1.5 x 2.5 mm *Round* (Altium draws that as an oval) and MP1/MP2 to 2.2 x 3.5 mm; `JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal` pins to 1.2 x 1.75 mm. Update the design from the library as in item 6.
8. **Pours:** the two GND polygons (top and bottom) came in with the design, already shaped: inset 0.3 mm from the edge, and with a gap over the whole SuperMini so no copper sits near its antenna. Check each one's net is `GND`, **Pour Over All Same Net Objects**, **Remove Dead Copper** ticked. Then **Tools » Polygon Pours » Repour All**.
9. **Pour connections:** **Plane » Polygon Connect Style:** *Relief Connect*, 4 entries, conductor width 0.4 mm, air gap 0.3 mm. That's what KiCad used. Repour again if you changed it.
10. **Screw-hole keep-outs:** the four M2 holes (H1-H4) each have a round keep-out on both copper layers, 2.6 mm radius, so the screw heads underneath can't touch copper. Check they came through (they show on the Keep-Out layer). If not, draw a 5.2 mm keep-out circle round each hole on Top and Bottom.

## Step 5: Design rule check

**Tools » Design Rule Check » Run Design Rule Check.** Expected:

- **0 Un-Routed Net Constraint** violations. All 12 ground pads have ground tracks, so this holds even before the pours are filled; if Altium reports a pour as unconnected *dead copper*, the Remove Dead Copper option in Step 4.8 takes it out.
- **0 clearance, width, short-circuit or hole-size violations.**
- **Silkscreen warnings are fine:** some stock footprints draw silk across their pads (the hot-swap socket and the slide switch, for example), and the SuperMini's outline runs off the board at the back-right notch. JLCPCB clips silk off pads and the board edge. Fix them if you like the board tidy.

## Step 6: Gerbers and drill files for JLCPCB

1. **Gerbers:** **File » Fabrication Outputs » Gerber Files**. Units *Millimeters*, format *4:4* (or *Inches 2:4*, both fine for JLC). **Layers** tab: **Plot Layers » Used On**; among the mechanical layers tick **only Mechanical 1** (the outline). **OK**.
2. **Drill:** **File » Fabrication Outputs » NC Drill Files**, same units and format. Tick **Generate separate NC Drill files for plated & non-plated holes**. **OK**, and **OK** on the drill-size pop-up.
3. **Compare with the reference:** open both sets in a Gerber viewer (JLCPCB's upload preview, or Altium's **File » Open** on the `.GTL` etc., which opens CAMtastic). Things to see in Altium's set: the L-shaped outline with four boss notches; the encoder's two **slots** (not round holes) in the non-plated drill file; 9 vias; no copper under the SuperMini; the GND pour on both sides.
4. **Zip** the Gerber and drill files from `Project Outputs for ...`.
5. **Order at JLCPCB:** 2 layers, 1.6 mm, 5 boards, any colour, HASL with lead (easiest to hand-solder). The board is over 100 mm in one direction, so it costs a few pounds more than the 100 x 100 mm price.

`reference/gerbers-reference/` is a complete set from KiCad (plate-frame coordinates, slots in the NPTH drill file). If Altium's output ever disagrees with it, ask me before ordering.

## Step 7: Check before ordering boards

A mistake in any of these means a new board. Print the board 1:1 first (**File » Page Setup**, *Scaled Print*, scale 1.00; check the board measures 95.3 mm across) and lay real parts on the paper.

1. **SuperMini at the back right, under the board.** U1 hangs under the board on its headers with its components facing down toward the desk (its plain back toward the PCB), USB-C toward the back wall. Turn the print over and lay a SuperMini on the bottom view, components up: its pin labels must match the schematic (pin 1 = P0.06 at the back right seen from the top, B+ at the back left), and USB must point at the back edge. The pin positions are the standard Pro Micro ones (rows 15.24 mm apart, 2.54 mm pitch).
2. **Encoder.** Fit a real PEC11R-4220F-S0024 through the print: 5 pins (A, C, B on one side; S1, S2 on the other) and the two lugs on the slots. The lugs and pins are trimmed flush on the bottom before U1 goes on, because U1 sits right under them.
3. **Power switch reach.** The OS102011MA1QN1's actuator should stick 0.9 mm out of the right-hand wall at y = 72. The case slot has been adjusted to the switch's 2 x 4 mm actuator; print the case's right wall section if you want to try it before the PCB arrives.
4. **Battery polarity.** J1 pin 1 (square pad, the one nearer the front) is `VBAT` (+), pin 2 is GND; the plug goes in from the left. LiPo leads come both ways round: check yours before plugging in, and swap the pins in the plug if it's reversed.
5. **LCD cable order.** J2 pins 1-8 are VCC, GND, DIN, CLK, CS, DC, RST, BL from the back, which is the Waveshare cable order. Check the colours on your cable against the module's labels when it arrives.
6. **Heights.** U1 on 2.5 mm low-profile headers; nothing on the top side may poke up more than 2 mm (the gap under the case skin), so trim every through-hole joint flush on the top.

## Assembly order

1. Diodes D1-D13 and capacitors C1-C3 (bottom).
2. Hot-swap sockets SW1-SW12 (bottom).
3. SW_RST, SW_PWR, J1 (bottom).
4. ENC1 from the top; **trim its five pins and two lugs flush underneath**, and put Kapton tape over the area.
5. U1 on its low-profile headers (bottom). Trim the pins flush on the top.
6. LCD cable into J2 from the bottom, solder on the top, trim flush.

## Library notes

- **The hot-swap socket footprint is drawn from the socket's side.** EAGLE (and so the import) only allows surface-mount pads on top, so `SW_Kailh_MX_Hotswap` has its pads on the top layer and is mirrored left-to-right. Placed on the **bottom** layer it comes out right: the holes line up with the switch above, the pads land on the bottom copper where the socket is soldered. Always place it on the bottom. If you'd rather have it the Altium way (drawn from the top, pads on the bottom layer), redraw it in the PcbLib.
- The JR library also holds the carrier's parts (XIAO nRF52840, SS14, DMG2305UX, 0805 resistors and capacitors, the connectors). The carrier project stays linked to its own imported library until you decide to switch it over.
- To add a part later: draw the symbol in `JR.SchLib` (or reuse one: every resistor uses `R`), the footprint in `JR.PcbLib`, set the parameters (`Manufacturer`, `Manufacturer Part Number`, `LCSC`, `Description`), recompile. `JR_parts.csv` shows the pattern.

## What changed elsewhere with this board

- **Controller pin map:** footprint pins 5-10 now carry the LCD's six signals in the Waveshare cable order (P0.17 MOSI, P0.20 SCK, P0.22 CS, P0.24 DC, P1.00 RST, P0.11 backlight), so they run straight across to J2. Rows 0 and 1 moved to P1.15 and P0.02. The firmware's board overlay, `pcb/generate.py` and `pcb/README.md` are updated to match, and the firmware rebuilt.
- **Case:** knob moved 1 mm left to x = 82 (centred over the SuperMini, so the encoder's lug slots fall between its pin rows); the PCB outline opens the screen cut-out to the back and left edges and clears the screen clamp pillar by 0.5 mm; boss notches 8.8 mm across; the case trims 0.4 mm round the PCB edge at board height; USB-C opening raised for the SuperMini's mid-mount connector; power switch modelled as the OS102011MA1QN1.

## Rebuilding this package

Everything here is generated. After changing the design, from the repo root on a machine with KiCad 7 and Freerouting:

```
/usr/bin/python3 pcb/library/src/build_library.py            # JR library
/usr/bin/python3 pcb/board/build_board.py pcb/B/kicad        # place parts, outline, pours
/usr/bin/python3 pcb/board/route.py pcb/B/kicad freerouting-1.9.0.jar
/usr/bin/python3 pcb/board/check.py pcb/B/kicad/macropad_B.kicad_pcb
/usr/bin/python3 pcb/board/export_altium.py pcb/B/kicad pcb/B/altium
python3 pcb/board/check_eagle.py pcb/B/altium/import-eagle
```

Once you've imported into Altium and started editing there, the Altium project is the master copy and these files are history.
