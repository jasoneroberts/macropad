"""Schematic symbols of the JR library, drawn in code.

Every symbol is a plain description (mm, y up, origin at the symbol's centre) that two writers turn into a
KiCad symbol (jr_kicad.py) and an EAGLE symbol (eagle.py), so both libraries show the same drawing.

Conventions (chosen to survive the EAGLE route into Altium 19):
  - Pin connection points sit on the 2.54 mm (100 mil) grid, so wires snap in Altium.
  - Pin lengths are EAGLE's fixed lengths: 2.54 mm ("short") or 5.08 mm ("middle").
  - Every pin is passive. EAGLE "pwr"/"sup" pins join nets by name without a wire, which hides connections.
  - A pin's "dir" is the direction from its connection point into the body: 0 = right, 90 = up, 180 = left, 270 = down
    (the same as a KiCad pin's rotation and an EAGLE pin's R0/R90/R180/R270).
  - Pin names must be unique in EAGLE; a repeated name (GND on three pins) is written "GND@<pin number>" there, which
    EAGLE and Altium display as "GND".
"""

G = 2.54  # grid


class Sym:
    def __init__(self, name, prefix, desc, hide_pin_names=False, hide_pin_numbers=False):
        self.name, self.prefix, self.desc = name, prefix, desc
        self.items = []          # ("rect", x0, y0, x1, y1, filled) | ("poly", [(x, y)...], filled) | ("circle", x, y, r, filled)
                                 # | ("arc", (sx, sy), (mx, my), (ex, ey)) | ("text", s, x, y, size)
        self.pins = []           # (number, name, x, y, dir, length)
        self.hide_pin_names, self.hide_pin_numbers = hide_pin_names, hide_pin_numbers
        self.ref_at = (0, 0, "left")      # x, y, justify of the designator
        self.val_at = (0, 0, "left")      # and of the value

    def rect(self, x0, y0, x1, y1, filled=False): self.items.append(("rect", x0, y0, x1, y1, filled)); return self
    def poly(self, pts, filled=False): self.items.append(("poly", list(pts), filled)); return self
    def line(self, *pts): return self.poly(pts)
    def circle(self, x, y, r, filled=False): self.items.append(("circle", x, y, r, filled)); return self
    def arc(self, s, m, e): self.items.append(("arc", s, m, e)); return self
    def text(self, s, x, y, size=1.27): self.items.append(("text", s, x, y, size)); return self
    def pin(self, num, name, x, y, d, length=G):
        assert abs(x / G - round(x / G)) < 1e-6 and abs(y / G - round(y / G)) < 1e-6, (self.name, num, x, y)
        assert length in (G, 2 * G), length
        self.pins.append((str(num), name, x, y, d, length)); return self
    def fields(self, ref, val): self.ref_at, self.val_at = ref, val; return self


def resistor():
    s = Sym("R", "R", "Resistor", hide_pin_names=True, hide_pin_numbers=True)
    s.rect(-1.016, -2.54, 1.016, 2.54)
    s.pin(1, "1", 0, 2 * G, 270).pin(2, "2", 0, -2 * G, 90)
    return s.fields((2.032, 0.762, "left"), (2.032, -1.524, "left"))


def capacitor():
    s = Sym("C", "C", "Capacitor", hide_pin_names=True, hide_pin_numbers=True)
    s.line((0, 2.54), (0, 0.635)).line((0, -2.54), (0, -0.635))
    s.rect(-1.524, 0.508, 1.524, 0.762, True).rect(-1.524, -0.762, 1.524, -0.508, True)
    s.pin(1, "1", 0, 2 * G, 270).pin(2, "2", 0, -2 * G, 90)
    return s.fields((2.032, 0.762, "left"), (2.032, -1.524, "left"))


def diode(schottky=False):
    s = Sym("D_Schottky" if schottky else "D", "D", "Schottky diode" if schottky else "Diode",
            hide_pin_names=True, hide_pin_numbers=True)
    s.line((-2.54, 0), (2.54, 0))
    s.poly([(-1.27, 1.27), (-1.27, -1.27), (1.27, 0)], True)
    if schottky:
        s.line((1.778, 1.016), (1.778, 1.27), (1.27, 1.27), (1.27, -1.27), (0.762, -1.27), (0.762, -1.016))
    else:
        s.line((1.27, 1.27), (1.27, -1.27))
    # KiCad/IPC numbering: pad 1 = cathode, pad 2 = anode (the SOD-123 and SMA footprints mark pad 1 with the bar)
    s.pin(1, "K", 2 * G, 0, 180).pin(2, "A", -2 * G, 0, 0)
    return s.fields((0, 2.286, "center"), (0, -2.794, "center"))


def pmos_gsd():
    s = Sym("Q_PMOS_GSD", "Q", "P-channel MOSFET, SOT-23 pinout 1 G, 2 S, 3 D", hide_pin_names=True)
    s.line((-2.54, 0), (-1.016, 0)).line((-1.016, -1.778), (-1.016, 1.778))
    for y in (-1.524, 0, 1.524):
        s.line((-0.508, y - 0.508), (-0.508, y + 0.508))
    s.line((-0.508, 1.524), (2.54, 1.524), (2.54, 2.54))        # source up
    s.line((-0.508, -1.524), (2.54, -1.524), (2.54, -2.54))     # drain down
    s.line((-0.508, 0), (2.54, 0), (2.54, 1.524))
    s.poly([(1.27, 0), (0.508, 0.381), (0.508, -0.381)], True)   # arrow away from the channel (P-channel)
    s.pin(1, "G", -2 * G, 0, 0).pin(2, "S", G, 2 * G, 270).pin(3, "D", G, -2 * G, 90)
    return s.fields((3.556, 0.762, "left"), (3.556, -1.524, "left"))


def key_switch():
    s = Sym("SW_Key", "SW", "Key switch (MX socket)", hide_pin_names=True, hide_pin_numbers=True)
    s.line((-2.54, 0), (-1.524, 0)).line((2.54, 0), (1.524, 0))
    s.circle(-1.27, 0, 0.254).circle(1.27, 0, 0.254)
    s.line((-1.27, 0.508), (1.524, 1.524)).line((0, 1.016), (0, 2.032)).line((-0.762, 2.032), (0.762, 2.032))
    s.pin(1, "1", -2 * G, 0, 0).pin(2, "2", 2 * G, 0, 180)
    return s.fields((0, 3.048, "center"), (0, -2.032, "center"))


def push_4pin():
    s = Sym("SW_Push_4pin", "SW", "Tactile switch, 4 pads: 1 and 2 are one side, 3 and 4 the other",
            hide_pin_names=True)
    s.line((-2.54, 2.54), (-2.54, -2.54)).line((2.54, 2.54), (2.54, -2.54))
    s.line((-2.54, 0), (-1.524, 0)).line((2.54, 0), (1.524, 0))
    s.circle(-1.27, 0, 0.254).circle(1.27, 0, 0.254)
    s.line((-1.524, 0.762), (1.524, 0.762)).line((0, 0.762), (0, 1.778)).line((-0.762, 1.778), (0.762, 1.778))
    s.pin(1, "1", -2 * G, G, 0).pin(2, "2", -2 * G, -G, 0).pin(3, "3", 2 * G, G, 180).pin(4, "4", 2 * G, -G, 180)
    return s.fields((0, 3.302, "center"), (0, -3.81, "center"))


def spdt():
    s = Sym("SW_SPDT", "SW", "Slide switch, SPDT: pin 2 is common", hide_pin_names=True)
    s.line((-2.54, 0), (-1.524, 0)).circle(-1.27, 0, 0.254)
    s.line((2.54, 2.54), (1.524, 2.54)).circle(1.27, 2.54, 0.254)
    s.line((2.54, -2.54), (1.524, -2.54)).circle(1.27, -2.54, 0.254)
    s.line((-1.016, 0.254), (1.27, 2.032))
    s.pin(2, "COM", -2 * G, 0, 0).pin(1, "1", 2 * G, G, 180).pin(3, "3", 2 * G, -G, 180)
    return s.fields((0, 4.064, "center"), (0, -4.318, "center"))


def encoder_switch():
    s = Sym("RotaryEncoder_Switch", "ENC", "Rotary encoder with push switch: A, B, C = common; S1, S2 = switch")
    s.rect(-5.08, -5.08, 5.08, 5.08)
    s.circle(0, 0, 1.778)
    s.line((-0.635, 1.778), (0.635, 2.286)).line((-0.635, -1.778), (0.635, -2.286))
    s.pin("A", "A", -10.16, G, 0, 2 * G).pin("C", "C", -10.16, 0, 0, 2 * G).pin("B", "B", -10.16, -G, 0, 2 * G)
    s.pin("S1", "S1", 10.16, G, 180, 2 * G).pin("S2", "S2", 10.16, -G, 180, 2 * G)
    return s.fields((-5.08, 6.096, "left"), (-5.08, -6.858, "left"))


def conn_1xn(n):
    s = Sym(f"Conn_01x{n:02d}", "J", f"Connector or wire pads, 1 x {n}", hide_pin_names=True)
    ys = [G * (n // 2 - i) for i in range(n)]
    s.rect(-1.27, ys[-1] - 1.27, 1.27, ys[0] + 1.27)
    for i, y in enumerate(ys, 1):
        s.pin(i, str(i), -2 * G, y, 0, G)
        s.rect(-1.27, y - 0.127, 0, y + 0.127, True)
    return s.fields((-1.27, ys[0] + 2.032, "left"), (-1.27, ys[-1] - 2.794, "left"))


def conn_2xn(n):
    s = Sym(f"Conn_02x{n:02d}_Odd_Even", "CN", f"Connector, 2 x {n}, odd pins left, even right", hide_pin_names=True)
    ys = [G * (n // 2 - i) for i in range(n)]
    s.rect(-2.54, ys[-1] - 1.27, 2.54, ys[0] + 1.27)
    for i, y in enumerate(ys):
        s.pin(2 * i + 1, str(2 * i + 1), -3 * G, y, 0, G).pin(2 * i + 2, str(2 * i + 2), 3 * G, y, 180, G)
        s.rect(-2.54, y - 0.127, -1.27, y + 0.127, True).rect(1.27, y - 0.127, 2.54, y + 0.127, True)
    return s.fields((-2.54, ys[0] + 2.032, "left"), (-2.54, ys[-1] - 2.794, "left"))


def test_point():
    s = Sym("TestPoint", "TP", "Test pad", hide_pin_names=True, hide_pin_numbers=True)
    s.circle(0, 2.54 + 0.762, 0.762)
    s.pin(1, "1", 0, 0, 90, G)
    return s.fields((1.524, 3.81, "left"), (1.524, 2.032, "left"))


def mounting_hole():
    s = Sym("MountingHole", "H", "Mounting hole, no connection")
    s.circle(0, 0, 1.27).circle(0, 0, 2.032)
    return s.fields((3.048, 0.508, "left"), (3.048, -1.27, "left"))


def module(name, desc, left, right, width=15.24):
    """A module drawn like its board: left = [(pin, name)] top to bottom, right = [(pin, name)] top to bottom."""
    s = Sym(name, "U", desc)
    n = max(len(left), len(right))
    top = G * (n // 2)
    h = (n - 1) * G
    x = width / 2
    s.rect(-x, top - h - G, x, top + G)
    for i, (p, nm) in enumerate(left):
        s.pin(p, nm, -x - 2 * G, top - i * G, 0, 2 * G)
    for i, (p, nm) in enumerate(right):
        s.pin(p, nm, x + 2 * G, top - i * G, 180, 2 * G)
    return s.fields((-x, top + G + 1.016, "left"), (-x, top - h - G - 2.54, "left"))


def supermini():
    # Pro Micro numbering seen from the module's component side, USB-C at the top
    left = [(1, "P0.06"), (2, "P0.08"), (3, "GND"), (4, "GND"), (5, "P0.17"), (6, "P0.20"), (7, "P0.22"),
            (8, "P0.24"), (9, "P1.00"), (10, "P0.11"), (11, "P1.04"), (12, "P1.06")]
    right = [(24, "BAT+"), (23, "GND"), (22, "RST"), (21, "VCC"), (20, "P0.31"), (19, "P0.29"), (18, "P0.02"),
             (17, "P1.15"), (16, "P1.13"), (15, "P1.11"), (14, "P0.10"), (13, "P0.09")]
    s = module("SuperMini_nRF52840", "SuperMini nRF52840 (nice!nano v2 pinout), Pro Micro 24-pin", left, right)
    s.text("USB-C", 0, G * 6 + 1.27, 1.27)
    return s


def xiao():
    # Seeed numbering: 1-7 = D0-D6 down the left edge, 8-14 = D7-D10, 3V3, GND, 5V up the right edge (top view, USB up)
    # pin names carry both labels, as the carrier's schematic and firmware overlay use them (D0/P0.02, ...)
    left = [(1, "D0/P0.02"), (2, "D1/P0.03"), (3, "D2/P0.28"), (4, "D3/P0.29"), (5, "D4/P0.04"), (6, "D5/P0.05"),
            (7, "D6/P1.11"), (15, "SWDIO"), (16, "SWCLK"), (17, "RST"), (18, "GND")]
    right = [(14, "5V"), (13, "GND"), (12, "3V3"), (11, "D10/P1.15"), (10, "D9/P1.14"), (9, "D8/P1.13"),
             (8, "D7/P1.12"), (19, "BAT+"), (20, "BAT-")]
    return module("XIAO_nRF52840", "Seeed XIAO nRF52840, castellated, with SWD and battery pads", left, right)


def all_symbols():
    syms = [resistor(), capacitor(), diode(), diode(True), pmos_gsd(), key_switch(), push_4pin(), spdt(),
            encoder_switch(), conn_1xn(2), conn_1xn(8), conn_2xn(4), conn_2xn(5), test_point(), mounting_hole(),
            supermini(), xiao()]
    return {s.name: s for s in syms}
