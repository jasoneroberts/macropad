# Shopping list: concept B "Studio", one AliExpress order (UK)

Everything for concept B comes from AliExpress in one basket. Delivery from RS, Farnell, Mouser or DigiKey costs more than the encoder and sockets themselves, and every part here is a common AliExpress item.

**Prices are rough estimates, not checked.** They are typical AliExpress UK prices including VAT, but AliExpress pages could not be read when this list was written (2026-10-26). The one price checked is the screen's, on Waveshare's own site. Use the "Check on the listing" column before adding each item; several of those details decide whether the part fits the case or works with the firmware.

- For orders up to £135, AliExpress charges UK VAT at checkout, so there is nothing to pay on delivery.
- Items from different sellers arrive as separate parcels. "Choice" listings are combined into one parcel, so prefer them where the listing still passes the checks.
- Some sellers will not ship lithium cells to the UK. If the LiPo listing refuses at checkout, pick another seller.

## The basket

**DK test** marks what you need to try the screen and knob on the nRF52840 DK before the PCB exists (wiring at the top of `firmware/boards/nrf52840dk_nrf52840.overlay`).

| # | Item | Buy (used) | Search for | Check on the listing | Est. £ (unchecked) |
|---|---|---|---|---|---|
| 1 | SuperMini nRF52840 | 3 (1) | `SuperMini nRF52840` | USB-C, "nice!nano v2 compatible", UF2 bootloader already on it. Two 12-pin headers in the bag: their 2.5 mm plastic is the gap the case is designed around. Two spares because buyers report the odd dud batch; test each one before soldering (`firmware/README.md`). | 9-14 for 3 |
| 2 | Waveshare 2inch LCD Module (**DK test**) | 1 | `Waveshare 2inch LCD Module`, from the Waveshare official store | Waveshare part 17344: ST7789V(W), 240 x 320 IPS, SPI, 3.3/5 V, board 58 x 35 mm, with the 8-wire PH2.0 cable. The case window and clamp are sized for this board; a generic "2.0 inch ST7789" module has a different board and pin order and will not fit. | 10-13 (Waveshare's own price is US$10.99, checked 2026-10-26) |
| 3 | EC11 rotary encoder with push switch (**DK test**) | pack of 5 (1, plus 1 for the DK) | `EC11 rotary encoder 20mm half shaft with switch` | 5 pins (3 encoder + 2 switch). **20 detents and 20 pulses per turn**: a 30-detent / 15-pulse one makes the firmware step only every second click. 6 mm D ("half") shaft, 20 mm long: cut it to fit the knob (the model assumes 15 mm above the body); too long can be cut, too short cannot. | 2-4 |
| 4 | Kailh MX hot-swap sockets | 20 (12) | `Kailh hot swap socket MX` | Kailh CPG151101S11, MX type (not Choc). | 2-4 |
| 5 | MX-style switches | about 15 (12) | `Gateron MX switches`, `KTT switches` or `Outemu switches` | MX cross stem. Linear, tactile or clicky is your choice. 3-pin switches fit any PCB; 5-pin ones need the two extra peg holes in the footprint, or clip the pegs off. | 5-12 |
| 6 | 1u keycaps | 12 or more (12) | `relegendable keycaps 1u MX` or `DSA blank keycaps 1u` | MX cross stem, 1u. Relegendable (clear two-piece) caps take a paper label; the screen shows the labels anyway. | 3-8 |
| 7 | 1N4148W diodes | 100 (13) | `1N4148W SOD-123` | SOD-123 (marked T4). Not SOD-323, which is smaller than the PCB footprint. | about 1 |
| 8 | 0805 capacitors, 10 nF and 10 µF | 50-100 of each (2 and 1) | `0805 capacitor 10nF`, `0805 capacitor 10uF` | 0805 size, 10 µF rated 10 V or more. Skip if you have them from the trackball. | about 2 for both |
| 9 | JST PH 2-pin straight header | pack of 10 (1) | `JST PH 2.0 2P straight pin header` | PH, 2.0 mm pitch (not XH 2.5 mm or ZH 1.5 mm), vertical through-hole. Packs with housings and crimps are handy for making leads. | about 1 |
| 10 | LiPo 603040, about 800 mAh | 1 (1) | `603040 lipo 800mAh PH2.0` | No bigger than 6 x 30 x 40 mm, or it will not fit the cradle under the screen. Protection board, JST PH 2.0 lead. Before plugging in, check the red wire lands on J1 pin 1 (BAT+); lead polarity varies, so swap the crimps in the housing if it does not. | 3-6 |
| 11 | SK12D07VG4 slide switch | pack of 10 (1) | `SK12D07VG4` | SPDT, right-angle, 2.54 mm pin pitch, 4 mm actuator. Check the actuator reaches through the 2.4 mm wall before ordering PCBs. | about 1 |
| 12 | 6 x 3.5 mm tact switch | pack of 10-20 (1) | `6x3.5 tact switch SMD 2 pin` | 6 x 3.5 mm body (PTS636 size), 2-pin SMD. Reset button, only for recovery. | about 1 |
| 13 | M3 heat-set inserts | 50 (4) | `M3 heat set insert M3x4x4.2` | M3 thread, 4 mm long or shorter (the corner bosses are sized for 4 mm), outside diameter about 4.2 mm. Print the test coupon: it tries 3.8 and 4.0 mm holes. | 2-3 |
| 14 | M3 x 8 countersunk screws | 20 (4) | `M3x8 countersunk hex socket DIN 7991` | 90° countersunk (DIN 7991 / ISO 10642), head about 6 mm. Bottom plate to the corner inserts. | 1-2 |
| 15 | M2 x 5 self-tapping screws | 50-100 (6) | `M2x5 self tapping screw pan head` | Pan head, M2 x 5 mm. 4 for the PCB, 2 for the display clamp. | about 1 |
| 16 | 10 mm rubber feet | 1 sheet (4) | `10mm self adhesive rubber feet` | 10 mm round, 2-3 mm tall. They sit in 10.6 mm recesses, 1 mm deep, so they add about 2 mm to the heights on the page. | about 1 |
| 17 | Dupont jumper wires (**DK test**) | 40 female-female and 40 male-female, 20 cm | `dupont jumper wire female female 20cm` | For the knob on the DK. The screen's cable already ends in Dupont sockets that fit the DK's headers. | 1-3 |
| 18 | Mini breadboard (**DK test**, optional) | 1 | `mini breadboard 170` | Somewhere to plug the EC11 in while testing; bend its two mounting lugs flat. | about 1 |

**Basket total:** about £45-80, unchecked. Most of it is the switches, the keycaps and the screen; the electronics on the board itself are under £10.

## Not in this basket

- **Main PCB** (2 layers, 95 x 110 mm, 5 boards): JLCPCB or PCBWay once the board is drawn in Altium, about £10-20 delivered. It is over 100 mm long, so it misses the cheapest 100 x 100 mm price band.
- **Filament** (PLA or PETG, about 100 g): once the printer is chosen.
- **Soldering iron tip for the inserts:** setting M3 heat-set inserts needs a tip that fits them, or a dedicated insert tip.

## Measure when the parts arrive

The case model uses datasheet and listing numbers for these. Measure them and change the named values at the top of `scad/macropad.scad`, then rebuild:

- Screen glass outline and thickness, and where the visible area sits on it (`LCD200` table).
- EC11 body height above the PCB (`enc_body_h`) and shaft length (`enc_shaft_l`).
- Heat-set insert outside diameter and length (`insert_d`, `insert_len`), using the printed test coupon.
- LiPo size (`LIPO_603040`).
- Switch hole fit (`sw_hole`), using the test coupon's four sizes.

## Printer

The largest B part is the top shell, 101 x 116 mm and 22 mm tall, printed face down without supports. Any printer with a 180 mm bed is enough for all three concepts (C's top shell is 92 x 140 mm). A 0.4 mm nozzle and PETG or PLA are fine.
