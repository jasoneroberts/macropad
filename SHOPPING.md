# Shopping list: concept B "Studio" (UK, October 2026)

Prices are estimates in GBP from typical UK and AliExpress listings, not quotes. Check stock and price before ordering. Quantities include a few spares where parts are tiny or cheap.

## Order now: needed to try the firmware on the DK

| Item | Qty | Est. £ | Where to look | Notes |
|---|---|---|---|---|
| Waveshare 2inch LCD Module (ST7789V, 240 x 320) | 1 | 11-14 | The Pi Hut, Amazon UK, Waveshare | Comes with an 8-wire PH2.0 to Dupont cable. Measure the glass and board once it arrives (see "Measure" below). |
| EC11 rotary encoder with push switch, 20 detents, 15-20 mm D-shaft | 2 | 2-4 | Mouser / Farnell (Alps EC11E15244G1), or AliExpress packs | One for the breadboard, one for the build. |
| Breadboard jumper wires (female-female / male-female) | 1 pack | 3 | Anything | For the DK wiring in `firmware/boards/nrf52840dk_nrf52840.overlay`. |

With these and the DK you can run the screen, the knob and four keys (the DK buttons) over USB and Bluetooth.

## Order next: the macropad itself

| Item | Qty | Est. £ | Where to look | Notes |
|---|---|---|---|---|
| SuperMini nRF52840 (nice!nano v2 clone, USB-C) | 3 | 12-15 | AliExpress | **Chosen.** One for the build, two spares, because buyers report the odd dud batch. Pick a listing that says "nice!nano v2 compatible" with the UF2 bootloader. Boards made since April 2024 have the fix for a battery drain when VCC is switched off. |
| Low-profile header pins or 2.5 mm "Mill-Max" style sockets for the controller | 1 set | 2-6 | Mechboards, AliExpress | Sets the 2.5 mm gap the case is designed around. |
| MX-style switches | 14 | 6-12 | Mechboards, Amazon UK | 12 + 2 spares. Any 3- or 5-pin MX switch; hot-swap means you can change later. |
| 1u keycaps, MX stem, blank or relegendable | 12 | 5-15 | Mechboards, AliExpress | Relegendable caps let you label the keys; the screen does that too. |
| Kailh MX hot-swap sockets (CPG151101S11) | 15 | 3-5 | Mechboards, AliExpress | |
| 1N4148W diodes, SOD-123 | 1 pack (100) | 2 | AliExpress, Mouser | 13 used. |
| 0805 capacitors, 10 nF and 10 uF | a few | 1 | any assortment kit | Probably already in the drawer from the trackball. |
| JST PH 2-pin vertical THT header (B2B-PH-K-S) | 2 | 1 | Mouser, kits | Check the LiPo's lead polarity against it before plugging in. |
| LiPo 603040, 3.7 V, ~800 mAh, JST-PH lead, with protection board | 1 | 6-8 | The Pi Hut, Amazon UK | 6 x 30 x 40 mm. Larger cells will not fit under the screen. |
| Right-angle SPDT slide switch (SK12D07VG4 style) | 3 | 1-2 | AliExpress | Check the actuator reaches through the 2.4 mm wall; the case slot may need adjusting. |
| 6 x 3.5 mm tact switch (C&K PTS636 or similar) | 2 | 1 | Mouser, Farnell | Reset, only for recovery. |
| M3 heat-set inserts, short (M3 x 4, about 4 mm OD) | 1 pack | 4-6 | Amazon UK (Ruthex / CNC Kitchen style) | 4 used. Print the test coupon to check the hole size. |
| M3 x 8 countersunk screws (ISO 10642) | 4 | 2 | Accu, Amazon UK | Bottom plate to the corner inserts. |
| M2 x 5 self-tapping pan-head screws | 6 | 2 | Accu, Amazon UK | 4 for the PCB, 2 for the display clamp. |
| 10 mm round rubber feet | 4 | 2 | Amazon UK | Add about 2 mm to the heights on the page. |
| Main PCB, 2 layers, 95 x 110 mm | 5 | 10-20 | JLCPCB / PCBWay, delivered | Bare board only; everything is hand-soldered. Over 100 mm long, so it misses the cheapest 100 x 100 price band. |
| Filament (PLA or PETG) | ~100 g | 2 | | Top shell, bottom plate, knob, clamp. |

**Rough total for concept B:** about £60-90 including the spare controller, switches, keycaps and PCBs, or about £35 for one unit's parts if switches and keycaps come from what you have. The electronics on the board itself are about £9, plus £11 for the screen and £6 for the LiPo.

## Measure when the parts arrive

The case model uses datasheet and listing numbers for these. Measure them and change the named values at the top of `scad/macropad.scad`, then rebuild:

- Screen glass outline and thickness, and where the visible area sits on it (`LCD200` table).
- EC11 body height above the PCB (`enc_body_h`) and shaft length (`enc_shaft_l`).
- Heat-set insert outside diameter and length (`insert_d`, `insert_len`), using the printed test coupon.
- LiPo size (`LIPO_603040`).
- Switch hole fit (`sw_hole`), using the test coupon's four sizes.

## Printer

The largest B part is the top shell, 101 x 116 mm and 22 mm tall, printed face down without supports. Any printer with a 180 mm bed is enough for all three concepts (C's top shell is 92 x 140 mm). A 0.4 mm nozzle and PETG or PLA are fine; heat-set inserts need a soldering iron tip that fits M3 inserts.
