"""Footprints of the JR library.

Three sources:
  - generated here, from datasheet dimensions (the parts KiCad has no exact footprint for, or where this design needs
    a change): SuperMini_nRF52840, SW_Kailh_MX_Hotswap, RotaryEncoder_EC11_Switch_NPTH;
  - KiCad's stock library (/usr/share/kicad/footprints), copied and renamed where EAGLE needs unique pad numbers;
  - the Gameball carrier's verified footprints (/mnt/project-files/pcb/kicad/...), copied unchanged, so the carrier
    keeps the pad numbers and positions that were checked pin by pin against the original board.

All coordinates are KiCad's: mm, y down, origin at the footprint's reference point.
"""
import math
import os

KICAD_FP = "/usr/share/kicad/footprints"
CARRIER = os.environ.get("JR_CARRIER_FP", "/mnt/project-files/pcb/kicad")


def _n(v):
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class Fp:
    """Writes a KiCad 7 .kicad_mod."""

    def __init__(self, name, descr, tags="", smd=False):
        self.name, self.descr, self.tags, self.smd = name, descr, tags, smd
        self.items = []

    def line(self, a, b, layer="F.SilkS", w=0.12):
        self.items.append(f'(fp_line (start {_n(a[0])} {_n(a[1])}) (end {_n(b[0])} {_n(b[1])}) '
                          f'(stroke (width {_n(w)}) (type solid)) (layer "{layer}"))')
        return self

    def poly(self, pts, layer="F.SilkS", w=0.12, closed=True):
        for i in range(len(pts) - (0 if closed else 1)):
            self.line(pts[i], pts[(i + 1) % len(pts)], layer, w)
        return self

    def rect(self, x0, y0, x1, y1, layer="F.Fab", w=0.1):
        return self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], layer, w)

    def circle(self, c, r, layer="F.Fab", w=0.1):
        self.items.append(f'(fp_circle (center {_n(c[0])} {_n(c[1])}) (end {_n(c[0] + r)} {_n(c[1])}) '
                          f'(stroke (width {_n(w)}) (type solid)) (fill none) (layer "{layer}"))')
        return self

    def arc(self, s, m, e, layer="F.SilkS", w=0.12):
        self.items.append(f'(fp_arc (start {_n(s[0])} {_n(s[1])}) (mid {_n(m[0])} {_n(m[1])}) (end {_n(e[0])} {_n(e[1])}) '
                          f'(stroke (width {_n(w)}) (type solid)) (layer "{layer}"))')
        return self

    def text(self, s, at, layer="F.SilkS", size=1.0):
        self.items.append(f'(fp_text user "{s}" (at {_n(at[0])} {_n(at[1])}) (layer "{layer}") '
                          f'(effects (font (size {_n(size)} {_n(size)}) (thickness {_n(size * 0.15)}))))')
        return self

    def tht(self, num, at, size, drill, shape="circle"):
        self.items.append(f'(pad "{num}" thru_hole {shape} (at {_n(at[0])} {_n(at[1])}) (size {_n(size)} {_n(size)}) '
                          f'(drill {_n(drill)}) (layers "*.Cu" "*.Mask"))')
        return self

    def smd_pad(self, num, at, size, rratio=0.1, layers=('F.Cu', 'F.Paste', 'F.Mask')):
        lay = " ".join(f'"{l}"' for l in layers)
        self.items.append(f'(pad "{num}" smd roundrect (at {_n(at[0])} {_n(at[1])}) (size {_n(size[0])} {_n(size[1])}) '
                          f'(layers {lay}) (roundrect_rratio {_n(rratio)}))')
        return self

    def hole(self, at, d):
        self.items.append(f'(pad "" np_thru_hole circle (at {_n(at[0])} {_n(at[1])}) (size {_n(d)} {_n(d)}) '
                          f'(drill {_n(d)}) (layers "*.Cu" "*.Mask"))')
        return self

    def slot(self, at, sx, sy):
        """Unplated slot, sx x sy mm (the long side is the slot's length)."""
        self.items.append(f'(pad "" np_thru_hole oval (at {_n(at[0])} {_n(at[1])}) (size {_n(sx)} {_n(sy)}) '
                          f'(drill oval {_n(sx)} {_n(sy)}) (layers "*.Cu" "*.Mask"))')
        return self

    def write(self, lib_dir, ref_at=(0, -3), val_at=(0, 3)):
        attr = "smd" if self.smd else "through_hole"
        body = "\n  ".join(self.items)
        text = (f'(footprint "{self.name}" (version 20221018) (generator pcbnew)\n  (layer "F.Cu")\n'
                f'  (descr "{self.descr}")\n  (tags "{self.tags}")\n  (attr {attr})\n'
                f'  (fp_text reference "REF**" (at {_n(ref_at[0])} {_n(ref_at[1])}) (layer "F.SilkS") '
                f'(effects (font (size 1 1) (thickness 0.15))))\n'
                f'  (fp_text value "{self.name}" (at {_n(val_at[0])} {_n(val_at[1])}) (layer "F.Fab") '
                f'(effects (font (size 1 1) (thickness 0.15))))\n  {body}\n)\n')
        open(os.path.join(lib_dir, self.name + ".kicad_mod"), "w").write(text)


# ---------------------------------------------------------------------------------------------------------------
def supermini(lib):
    """SuperMini nRF52840 / nice!nano v2 (Pro Micro size). Drawn from the module's component side, USB-C up.

    24 pins on two rows 15.24 mm apart, 2.54 mm pitch, pins centred on the module (18 x 33 mm board).
    The three inner pins at the far end (P1.01, P1.02, P1.07) are not used and have no holes.
    Placed on the bottom layer (module hanging under the board, components facing away from it), Altium/KiCad mirror it: pin 1 lands on the right
    in the top view, with USB still at the top.
    """
    f = Fp("SuperMini_nRF52840", "SuperMini nRF52840 / nice!nano v2, Pro Micro 24-pin, 2.54 mm, rows 15.24 mm. "
           "Module outline 18 x 33 mm, USB-C at the top edge", "nRF52840 pro micro supermini nice!nano")
    for i in range(12):
        y = -13.97 + i * 2.54
        f.tht(i + 1, (-7.62, y), 1.7, 1.0, "rect" if i == 0 else "circle")
        f.tht(24 - i, (7.62, y), 1.7, 1.0)
    f.rect(-9, -16.5, 9, 16.5, "F.Fab", 0.1)
    f.rect(-4.47, -17.6, 4.47, -11.25, "F.Fab", 0.1)                     # USB-C receptacle, overhangs ~1 mm
    f.text("USB-C", (0, -14.3), "F.Fab", 1.0)
    f.rect(-9.12, -16.62, 9.12, 16.62, "F.SilkS", 0.12)
    f.poly([(-9.12, -15.3), (-10.2, -14.7), (-10.2, -15.9)], "F.SilkS", 0.12)   # pin 1 arrow
    f.rect(-9.5, -18.0, 9.5, 17.0, "F.CrtYd", 0.05)
    f.write(lib, (0, -19), (0, 18.2))


def kailh_mx_hotswap(lib):
    """Kailh MX hot-swap socket CPG151101S11 under an MX switch.

    Dimensions from Kailh's drawing (the same numbers as the keyswitch-kicad-library footprint): MX centre post
    4.0 mm, PCB-mount pegs 1.75 mm at +/-5.08, switch pin holes 3.05 mm at (-3.81, -2.54) and (2.54, -5.08) in the
    switch's top view; socket pads 2.55 x 2.5 mm at (-7.085, -2.54) and (5.842, -5.08).

    The footprint is drawn as seen from the socket side (x mirrored from the switch's top view) with the pads on the
    front copper. Place it on the BOTTOM layer: the mirror puts every hole back under the switch, and the pads on the
    bottom copper where the socket is soldered. (EAGLE only allows SMD pads on the top of a package, so this is the
    only way the socket survives the EAGLE route into Altium.)
    """
    f = Fp("SW_Kailh_MX_Hotswap", "Kailh MX hot-swap socket CPG151101S11, drawn from the socket side: place on the "
           "BOTTOM layer, switch centre at the origin, switch pins toward -y", "kailh mx hotswap socket keyboard",
           smd=True)
    m = lambda p: (-p[0], p[1])                                               # top view -> socket side
    f.hole((0, 0), 4.0).hole((-5.08, 0), 1.75).hole((5.08, 0), 1.75)
    f.hole(m((-3.81, -2.54)), 3.05).hole(m((2.54, -5.08)), 3.05)
    f.smd_pad(1, m((-7.085, -2.54)), (2.55, 2.5)).smd_pad(2, m((5.842, -5.08)), (2.55, 2.5))
    # Socket body (top-view outline from the keyswitch library, mirrored)
    body = [(-4, -6.8), (4.8, -6.8), (4.8, -2.8), (-0.3, -2.8)]
    for layer, w in (("F.Fab", 0.12), ("F.CrtYd", 0.05)):
        f.poly([m(p) for p in body], layer, w, closed=False)
        f.arc(m((-0.3, -2.8)), m((-0.3 - 2 * math.sin(math.pi / 4), -0.8 - 2 * math.cos(math.pi / 4))), m((-2.3, -0.8)), layer, w)
        f.line(m((-2.3, -0.8)), m((-6, -0.8)), layer, w).line(m((-6, -0.8)), m((-6, -4.8)), layer, w)
        f.arc(m((-6, -4.8)), m((-4 - 2 * math.cos(math.pi / 4), -4.8 - 2 * math.sin(math.pi / 4))), m((-4, -6.8)), layer, w)
    f.line(m((-4.1, -6.9)), m((1, -6.9)), "F.SilkS").line(m((-0.2, -2.7)), m((4.9, -2.7)), "F.SilkS")
    f.line(m((-6.1, -0.7)), m((-6.1, -4.8)), "F.SilkS")
    # The switch itself, on the other side of the board: B.Fab here, which lands on the top fab layer when placed
    f.rect(-7, -7, 7, 7, "B.Fab", 0.1)
    f.write(lib, (0, -8.2), (0, 8.2))


def ec11_npth(lib):
    """EC11-size encoder with push switch (Alps EC11E, Bourns PEC11R), vertical shaft, origin at the shaft.

    Pins as KiCad's RotaryEncoder_Alps_EC11E-Switch_Vertical_H20mm (A, C, B on 2.5 mm pitch; S1, S2 5 mm apart,
    14.5 mm from A). The two mounting lugs go into UNPLATED 2.8 x 1.5 mm slots: on the macropad the controller sits
    right under the knob, so the lugs are trimmed flush and must not carry exposed copper over the module's back.
    """
    f = Fp("RotaryEncoder_EC11_Switch_NPTH", "EC11-size rotary encoder with switch (Alps EC11E, Bourns PEC11R), "
           "vertical, origin at the shaft, unplated slots for the mounting lugs", "rotary encoder EC11 PEC11R")
    A = (-7.5, -2.5)
    f.tht("A", A, 2.0, 1.0, "rect").tht("C", (-7.5, 0), 2.0, 1.0).tht("B", (-7.5, 2.5), 2.0, 1.0)
    f.tht("S2", (7.0, -2.5), 2.0, 1.0).tht("S1", (7.0, 2.5), 2.0, 1.0)
    f.slot((0, -5.6), 2.8, 1.5).slot((0, 5.6), 2.8, 1.5)
    f.rect(-6, -5.8, 6, 5.8, "F.Fab", 0.12).circle((0, 0), 3, "F.Fab", 0.12)
    f.line((-6.1, -4.3), (-6.1, -5.9), "F.SilkS").line((-6.1, -5.9), (-2.0, -5.9), "F.SilkS")
    f.line((2.0, -5.9), (6.1, -5.9), "F.SilkS").line((6.1, -5.9), (6.1, -3.9), "F.SilkS")
    f.line((6.1, 3.9), (6.1, 5.9), "F.SilkS").line((6.1, 5.9), (2.0, 5.9), "F.SilkS")
    f.line((-2.0, 5.9), (-6.1, 5.9), "F.SilkS").line((-6.1, 5.9), (-6.1, 4.3), "F.SilkS")
    f.circle((0, 0), 3, "F.SilkS", 0.12)
    f.rect(-8.75, -6.9, 8.25, 6.9, "F.CrtYd", 0.05)
    f.write(lib, (0, -8), (0, 8))


# ---------------------------------------------------------------------------------------------------------------
def copy_stock(lib, src_lib, src_name, new_name=None, renumber=None, descr=None):
    """Copy a footprint with pcbnew, optionally renaming it and renumbering pads (list of new numbers in pad order)."""
    import pcbnew
    fp = pcbnew.FootprintLoad(src_lib, src_name)
    assert fp is not None, (src_lib, src_name)
    name = new_name or src_name
    fp.SetFPID(pcbnew.LIB_ID("", name))
    fp.Value().SetText(name)
    if descr:
        fp.SetDescription(descr)
    if renumber:
        pads = list(fp.Pads())
        assert len(pads) == len(renumber), (src_name, [p.GetNumber() for p in pads])
        for p, n in zip(pads, renumber):
            p.SetNumber(n)
    pcbnew.FootprintSave(lib, fp)
    return name


def build(lib):
    os.makedirs(lib, exist_ok=True)
    supermini(lib)
    kailh_mx_hotswap(lib)
    ec11_npth(lib)
    K = lambda l: f"{KICAD_FP}/{l}.pretty"
    copy_stock(lib, K("Diode_SMD"), "D_SOD-123")
    copy_stock(lib, K("Connector_JST"), "JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal")
    copy_stock(lib, K("Connector_PinHeader_2.54mm"), "PinHeader_1x08_P2.54mm_Vertical")
    copy_stock(lib, K("MountingHole"), "MountingHole_2.2mm_M2")
    # Unique pad numbers for EAGLE: the slide switch's two soldered frame tabs become MP1/MP2 (no net) ...
    copy_stock(lib, K("Button_Switch_THT"), "SW_Slide_SPDT_Angled_CK_OS102011MA1Q",
               renumber=None)
    import pcbnew
    fp = pcbnew.FootprintLoad(lib, "SW_Slide_SPDT_Angled_CK_OS102011MA1Q")
    k = 1
    for p in fp.Pads():
        if p.GetNumber() == "":
            p.SetNumber(f"MP{k}"); k += 1
    pcbnew.FootprintSave(lib, fp)
    # ... and the tact switch's 4 pads become 1-4 (1, 2 = one contact; 3, 4 = the other)
    copy_stock(lib, K("Button_Switch_SMD"), "SW_Push_1P1T_XKB_TS-1187A", renumber=["1", "2", "3", "4"],
               descr="XKB TS-1187A 5.1 x 5.1 mm SMD tactile switch, 4 gull-wing pads. Pads 1, 2 are one contact, 3, 4 the other")
    # Carrier footprints, unchanged
    for n in ("C_0805_2012Metric", "R_0805_2012Metric", "D_SMA", "SOT-23", "JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical",
              "PinHeader_1x02_P2.54mm_Vertical", "PinHeader_2x04_P2.00mm_Vertical", "PinHeader_2x05_P1.27mm_Vertical",
              "TestPoint_Pad_D1.5mm"):
        copy_stock(lib, f"{CARRIER}/Gameball.pretty", n)
    copy_stock(lib, f"{CARRIER}/src/Gameball.pretty", "XIAO_nRF52840_SMD")
