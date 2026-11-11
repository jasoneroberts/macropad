#!/usr/bin/env python3
"""Writes the Altium 19 hand-off for concept B: EAGLE schematic + board (the Import Wizard reads both), plus the
reference outputs made by KiCad from the same board.

    /usr/bin/python3 pcb/board/export_altium.py <kicad dir> <out dir>

<out>/
    macropad_B.sch, macropad_B.brd     EAGLE 7 XML: import with File > Import Wizard > EAGLE projects
    JR.lbr                             the JR library (same packages and devicesets as in the two files)
    macropad_B-schematic.pdf           the schematic, A3
    macropad_B-board.pdf               copper, both sides, top view
    BOM.csv, order-list.csv            parts with LCSC numbers
    gerbers-reference/                 KiCad's Gerbers + drill of the same board (compare with Altium's)

Board coordinates are the case's plate frame (mm, origin = case front-left corner, y toward the screen end), so the
EAGLE/Altium board lines up with dxf/pcb_outline_B.dxf and pcb/B/placement.csv.
"""
import csv
import math
import os
import shutil
import subprocess
import sys
from collections import defaultdict
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
LIBSRC = os.path.join(os.path.dirname(HERE), "library", "src")
sys.path.insert(0, LIBSRC)
import pcbnew  # noqa: E402

import build_board as BB  # noqa: E402
import design_b as D  # noqa: E402
import eagle as E  # noqa: E402
import schematic as S  # noqa: E402
from eagle import a, f  # noqa: E402
from jr_parts import part  # noqa: E402
from jr_symbols import all_symbols  # noqa: E402

KDIR, OUT = sys.argv[1], sys.argv[2]
NAME = "macropad_B"
LIB = "JR"
LIBDIR = os.path.join(os.path.dirname(HERE), "library")
SYMS = all_symbols()
P = BB.P
mm = pcbnew.ToMM

board = pcbnew.LoadBoard(os.path.join(KDIR, NAME + ".kicad_pcb"))
fps = {fp.GetReference(): fp for fp in board.GetFootprints()}
lib_fps = {}


def lib_fp(name):
    if name not in lib_fps:
        lib_fps[name] = pcbnew.FootprintLoad(os.path.join(LIBDIR, "JR.pretty"), name)
    return lib_fps[name]


used = sorted({part(p)["name"] for p, _ in D.PARTS.values()})
used_fp = sorted({part(n)["footprint"] for n in used})
used_sym = sorted({part(n)["symbol"] for n in used})
packages = [E.package_xml(lib_fp(n), n) for n in used_fp]
symbols = [E.symbol_xml(SYMS[n]) for n in used_sym]
devsets = [E.deviceset_xml(part(n), SYMS[part(n)["symbol"]], E.pad_names(lib_fp(part(n)["footprint"]))) for n in used]
library = E.library_xml(LIB, packages, symbols, devsets, "JR library (subset used by this design)")
POWER = sorted(D.POWER_NETS)
CLASSES = ('<classes>\n<class number="0" name="default" width="0.25" drill="0.3">\n<clearance class="0" value="0.2"/>\n</class>\n'
           '<class number="1" name="power" width="0.4" drill="0.3">\n<clearance class="1" value="0.2"/>\n</class>\n</classes>')
cls = lambda n: 1 if n in POWER else 0


def keyf(r):
    import re
    m = re.match(r"([A-Z_]+?)(\d*)$", r)
    return (m.group(1), int(m.group(2) or 0))


# ---------------------------------------------------------------------------------------------------------------
# Board
def eagle_xform(mirror, ang, x, y):
    """Package point -> board offset for an element at rot="[M]R<ang>": EAGLE rotates first, then mirrors about
    the y axis (KiCad's EAGLE importer reads it the same way: orientation ang + 180, then a top/bottom flip)."""
    r = math.radians(ang)
    x, y = x * math.cos(r) - y * math.sin(r), x * math.sin(r) + y * math.cos(r)
    return (-x, y) if mirror else (x, y)


def element_rot(ref, fp):
    """The EAGLE rotation (R / MR) that puts the package's pads where KiCad has them; checked pad by pad."""
    pk = lib_fp(str(fp.GetFPID().GetLibItemName()))
    local = [(p.GetNumber(), mm(p.GetPosition().x), -mm(p.GetPosition().y)) for p in pk.Pads()]
    world = [(p.GetNumber(),) + P(p.GetPosition()) for p in fp.Pads()]
    cx, cy = P(fp.GetPosition())
    mirror = fp.IsFlipped()
    for ang in (0, 90, 180, 270):
        def hit(n, lx, ly):
            ex, ey = eagle_xform(mirror, ang, lx, ly)
            return any(wn == n and abs(cx + ex - wx) < 2e-3 and abs(cy + ey - wy) < 2e-3 for wn, wx, wy in world)
        if len(local) == len(world) and all(hit(*q) for q in local):
            return ("MR" if mirror else "R") + str(ang)
    raise SystemExit(f"{ref}: no EAGLE rotation matches KiCad's pads")


plain = []
KL = E.kicad_layer_map()
for d in board.GetDrawings():
    L = KL.get(d.GetLayer())
    if L is None:
        continue
    if isinstance(d, pcbnew.PCB_TEXT):
        x, y = P(d.GetPosition())
        plain.append(E.text_xml(d.GetText(), x, y, mm(d.GetTextHeight()), L, d.GetTextAngleDegrees(), mirror=d.IsMirrored()))
    else:
        plain += E.shape_xml(d, lambda x, y: (x - BB.XO, BB.YO - y), L)
# Keep-outs for the case pillars' screws (no copper on either layer)
for i, (px, py) in enumerate(D.REPORT["pillars"], 1):
    for L in (41, 42):
        plain.append(f'<circle {a(x=f(px), y=f(py), radius=f(D.PILLAR_KEEPOUT_R / 2 + 0.6), width=f(D.PILLAR_KEEPOUT_R - 1.2), layer=L)}/>')

elements = []
for ref in sorted(fps, key=keyf):
    fp = fps[ref]
    p = part(D.PARTS[ref][0])
    x, y = P(fp.GetPosition())
    rot = element_rot(ref, fp)
    attrs = E.attributes(p, x=f(x), y=f(y), size="1.27", layer=27, display="off")
    names = []
    for t, field, L in (("NAME", fp.Reference(), 25 if not fp.IsFlipped() else 26),
                        ("VALUE", fp.Value(), 27 if not fp.IsFlipped() else 28)):
        tx, ty = P(field.GetPosition())
        disp = "value" if (t == "VALUE" or field.IsVisible()) else "off"
        if t == "VALUE":
            disp = "off"
        names.append(f'<attribute {a(name=t, x=f(tx), y=f(ty), size=f(mm(field.GetTextHeight())), layer=L, ratio=12, rot=("M" if fp.IsFlipped() else "") + "R" + str(int(field.GetTextAngleDegrees()) % 360), display=disp)}/>')
    elements.append(f'<element {a(name=ref, library=LIB, package=p["footprint"], value=p["value"], x=f(x), y=f(y), rot=rot, smashed="yes")}>'
                    + attrs + "".join(names) + "</element>")

# signals: pads, tracks, vias, ground pours
from shapely.geometry import Polygon as SPoly, box as sbox  # noqa: E402
pour = SPoly(D.outline_polygon(3)).buffer(-0.3, join_style=2)
x0, y0, x1, y1 = D.U1_BOX
pour = pour.difference(sbox(x0 - 0.3, y0 - 0.3, x1 + 0.3, y1 + 5))
pour = max(getattr(pour, "geoms", [pour]), key=lambda g: g.area)
pour = pour.simplify(0.02)
assert not list(pour.interiors), "pour outline must be a single loop"
pour_xy = list(pour.exterior.coords)[:-1]

sig = defaultdict(list)
for ref, fp in fps.items():
    for p in fp.Pads():
        if p.GetNetname():
            sig[p.GetNetname()].append(f'<contactref {a(element=ref, pad=p.GetNumber())}/>')
for t in board.GetTracks():
    n = t.GetNetname()
    if t.GetClass() == "PCB_VIA":
        x, y = P(t.GetPosition())
        sig[n].append(f'<via {a(x=f(x), y=f(y), extent="1-16", drill=f(mm(t.GetDrillValue())), diameter=f(mm(t.GetWidth())))}/>')
    else:
        L = 1 if t.GetLayer() == pcbnew.F_Cu else 16
        sig[n].append(E.wire(P(t.GetStart()), P(t.GetEnd()), mm(t.GetWidth()), L))
for L, rank in ((1, 1), (16, 1)):
    vs = "".join(f'<vertex {a(x=f(x), y=f(y))}/>' for x, y in pour_xy)
    sig["GND"].append(f'<polygon {a(width="0.254", layer=L, isolate="0.3", thermals="yes", orphans="no", rank=rank)}>{vs}</polygon>')
signals = [f'<signal {a(name=n, **{"class": cls(n)})}>' + "".join(v) + "</signal>" for n, v in sorted(sig.items())]
RULES = [("mdWireWire", "0.2mm"), ("mdWirePad", "0.2mm"), ("mdWireVia", "0.2mm"), ("mdPadPad", "0.2mm"),
         ("mdPadVia", "0.2mm"), ("mdViaVia", "0.2mm"), ("mdCopperDimension", "0.3mm"), ("mdDrill", "0.25mm"),
         ("msWidth", "0.2mm"), ("msDrill", "0.3mm"), ("rlMinViaOuter", "0.15mm"), ("layerSetup", "(1*16)")]
brd = (E.HEAD + E.layers_xml() + "\n<board>\n<plain>\n" + "\n".join(plain) + "\n</plain>\n<libraries>\n" + library
       + "\n</libraries>\n<attributes/>\n<variantdefs/>\n" + CLASSES + "\n"
       '<designrules name="macropad">\n' + "\n".join(f'<param {a(name=k, value=v)}/>' for k, v in RULES) + "\n</designrules>\n"
       "<autorouter/>\n<elements>\n" + "\n".join(elements) + "\n</elements>\n<signals>\n" + "\n".join(signals)
       + "\n</signals>\n</board>\n" + E.TAIL)

# ---------------------------------------------------------------------------------------------------------------
# Schematic
sh = S.build()
S.check(sh)
names_of = {}
for ref in sh.inst:
    names_of[ref] = E.eagle_pin_names(sh.sym(ref))
parts_xml = []
for ref in sorted(D.PARTS, key=keyf):
    p = part(D.PARTS[ref][0])
    parts_xml.append(f'<part {a(name=ref, library=LIB, deviceset=p["name"], device="", value=p["value"])}>'
                     + E.attributes(p) + "</part>")
inst_xml = []
for ref, (x, y, rot) in sorted(sh.inst.items(), key=lambda kv: keyf(kv[0])):
    extra = ""
    if rot in (90, 270):            # keep designator and value readable next to rotated parts
        (nx, ny), (vx, vy) = S.rotated_label_at(ref, x, y)
        extra = (f'<attribute {a(name="NAME", x=f(nx), y=f(ny), size="1.778", layer=95, rot="R0")}/>'
                 f'<attribute {a(name="VALUE", x=f(vx), y=f(vy), size="1.27", layer=96, rot="R0")}/>')
    inst_xml.append(f'<instance {a(part=ref, gate="G$1", x=f(x), y=f(y), rot=f"R{rot}", smashed="yes" if extra else None)}>'
                    + extra + "</instance>")

# group each net's wires into connected segments (EAGLE wants one <segment> per connected piece)
nets_xml = []
for net in sorted(D.NETS):
    ws = [(p, q) for n, p, q in sh.wires if n == net]
    parent = list(range(len(ws)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for i, (p1, q1) in enumerate(ws):
        for j, (p2, q2) in enumerate(ws):
            if j > i and (any(S._on_segment(e, p2, q2) for e in (p1, q1)) or any(S._on_segment(e, p1, q1) for e in (p2, q2))):
                parent[find(i)] = find(j)
    segs = defaultdict(list)
    for i in range(len(ws)):
        segs[find(i)].append(ws[i])
    out = []
    for group in segs.values():
        ends = {e for w in group for e in w}
        prs = []
        for ref, pin in D.NETS[net]:
            (px, py), _ = sh.pin(ref, pin)
            if (px, py) in ends:
                prs.append(f'<pinref {a(part=ref, gate="G$1", pin=names_of[ref][pin])}/>')
        wx = "".join(E.wire(p, q, 0.1524, 91) for p, q in group)
        jx = "".join(f'<junction {a(x=f(x), y=f(y))}/>' for n, x, y in sh.junctions
                     if n == net and any(S._on_segment((x, y), p, q) for p, q in group))
        lx = "".join(f'<label {a(x=f(x), y=f(y), size="1.778", layer=95, rot=f"R{r}")}/>' for n, x, y, r in sh.labels
                     if n == net and any(S._on_segment((x, y), p, q) for p, q in group))
        out.append("<segment>" + "".join(prs) + wx + jx + lx + "</segment>")
    nets_xml.append(f'<net {a(name=net, **{"class": cls(net)})}>\n' + "\n".join(out) + "\n</net>")
splain = []
for (p, q, w) in sh.lines:
    splain.append(E.wire(p, q, w, 97))
for t, x, y, size, rot, align in sh.texts:
    splain.append(E.text_xml(t, x, y, size, 97, rot, align="bottom-left"))
sch = (E.HEAD + E.layers_xml() + '\n<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">\n<libraries>\n' + library
       + "\n</libraries>\n<attributes/>\n<variantdefs/>\n" + CLASSES + "\n<parts>\n" + "\n".join(parts_xml)
       + "\n</parts>\n<sheets>\n<sheet>\n<plain>\n" + "\n".join(splain) + "\n</plain>\n<instances>\n" + "\n".join(inst_xml)
       + "\n</instances>\n<busses/>\n<nets>\n" + "\n".join(nets_xml) + "\n</nets>\n</sheet>\n</sheets>\n</schematic>\n" + E.TAIL)

IMP, REF, LIBO = (os.path.join(OUT, d) for d in ("import-eagle", "reference", "library"))
for d in (IMP, REF, LIBO):
    os.makedirs(d, exist_ok=True)
open(os.path.join(IMP, NAME + ".brd"), "w").write(brd)
open(os.path.join(IMP, NAME + ".sch"), "w").write(sch)
for fn in ("JR.lbr", "JR_parts.csv"):
    shutil.copyfile(os.path.join(LIBDIR, fn), os.path.join(LIBO, fn))
S.render(sh, os.path.join(REF, NAME + "-schematic.pdf"))
with open(os.path.join(REF, "connections.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["Net", "Designator", "Pin", "Pin name"])
    for net in sorted(D.NETS):
        for ref, pin in sorted(D.NETS[net], key=lambda rp: (keyf(rp[0]), rp[1])):
            sym = SYMS[part(D.PARTS[ref][0])["symbol"]]
            names = {str(q[0]): q[1] for q in sym.pins}
            w.writerow([net, ref, pin, names.get(pin, "")])

# ---------------------------------------------------------------------------------------------------------------
# BOM and order list
groups = defaultdict(list)
for ref, (pname, note) in D.PARTS.items():
    groups[pname].append(ref)
GBP = {"SuperMini_nRF52840": 4.50, "SW_Kailh_MX_Hotswap": 0.12, "Encoder_PEC11R-4220F-S0024": 1.60,
       "SW_Slide_OS102011MA1QN1": 0.45, "SW_Tact_TS-1187A-B-A-B": 0.03, "D_1N4148W_SOD-123": 0.02,
       "C_10n_0805": 0.01, "C_10u_0805": 0.03, "Conn_JST_PH_S2B_Horizontal": 0.10}
with open(os.path.join(REF, "BOM.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["Designators", "Qty", "JR part", "Value", "Description", "Manufacturer", "Manufacturer Part Number",
                "LCSC", "Footprint", "Side", "Est. unit GBP"])
    for pname, refs in sorted(groups.items(), key=lambda kv: keyf(sorted(kv[1], key=keyf)[0])):
        refs = sorted(refs, key=keyf)
        p = part(pname)
        side = sorted({"Bottom" if fps[r].IsFlipped() else "Top" for r in refs})
        w.writerow([", ".join(refs), len(refs), pname, p["value"], p["description"], p["manufacturer"], p["mpn"],
                    p["lcsc"], p["footprint"], "/".join(side), GBP.get(pname, "")])
# What to buy: the board's parts with LCSC numbers (spares included; LCSC rounds tiny parts up to its minimum), then
# everything else the build needs. Prices are rough GBP estimates, not quotes.
ORDER = [
    # item, buy, used, LCSC, where, est. GBP each, notes
    ("Kailh MX hot-swap socket CPG151101S11", 15, "SW1-SW12", "C2803348", "LCSC", 0.12, "3 spare"),
    ("Bourns PEC11R-4220F-S0024 encoder, 24 detents, push, 20 mm D shaft", 2, "ENC1", "C143797", "LCSC", 1.60,
     "1 spare / for the breadboard"),
    ("C&K OS102011MA1QN1 slide switch, right angle", 3, "SW_PWR", "C226259", "LCSC", 0.45, "2 spare"),
    ("XKB TS-1187A-B-A-B tact switch 5.1 x 5.1 mm", 5, "SW_RST", "C318884", "LCSC", 0.03, "LCSC minimum"),
    ("1N4148W diode, SOD-123", 50, "D1-D13", "C81598", "LCSC", 0.01, "LCSC minimum"),
    ("10 nF 50 V X7R 0805", 50, "C1, C2", "C1710", "LCSC", 0.005, "LCSC minimum"),
    ("10 uF 25 V X5R 0805", 20, "C3", "C15850", "LCSC", 0.02, "LCSC minimum"),
    ("JST PH 2-pin side-entry header S2B-PH-K-S", 3, "J1", "C173752", "LCSC", 0.10, "2 spare"),
    ("Main PCB, 2 layers, 1.6 mm, 95.3 x 110.5 mm, HASL", 5, "", "", "JLCPCB", 3.00, "Gerbers from Altium (Step 6)"),
    ("SuperMini nRF52840 (nice!nano v2 clone)", 3, "U1", "", "AliExpress", 4.50, "2 spare; UF2 bootloader"),
    ("Low-profile 2.5 mm header pins + sockets (Mill-Max style) for U1", 1, "U1", "", "Mechboards / AliExpress", 5.00,
     "sets the 2.5 mm gap the case is designed for; 2 x 12 pins"),
    ("Waveshare 2inch LCD Module (ST7789V, 240 x 320) with 8-wire PH2.0 cable", 1, "J2", "", "The Pi Hut", 12.00,
     "cut the cable and solder it into J2"),
    ("LiPo 603040 3.7 V ~800 mAh, protection board, JST PH lead", 1, "J1", "", "The Pi Hut / Amazon UK", 7.00,
     "check + is on J1 pin 1 before plugging in"),
    ("MX-style switches", 14, "", "", "Mechboards", 0.60, "2 spare"),
    ("1u MX keycaps", 12, "", "", "Mechboards / AliExpress", 0.80, ""),
    ("M2 x 5 self-tapping pan-head screws", 6, "H1-H4 + display clamp", "", "Accu / Amazon UK", 0.20, ""),
    ("M3 heat-set inserts (M3 x 4, ~4 mm OD) + M3 x 8 countersunk screws", 4, "case", "", "Amazon UK", 0.50, ""),
]
with open(os.path.join(REF, "order-list.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["Item", "Buy", "Used for", "LCSC", "Where", "Est. GBP each", "Est. GBP total", "Notes"])
    for item, qty, used_for, lcsc, where, each, note in ORDER:
        w.writerow([item, qty, used_for, lcsc, where, f"{each:.2f}", f"{qty * each:.2f}", note])
with open(os.path.join(REF, "placement.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["Designator", "JR part", "Side", "X mm", "Y mm", "EAGLE/Altium rotation", "Pin 1 X", "Pin 1 Y"])
    for ref in sorted(fps, key=keyf):
        fp = fps[ref]
        x, y = P(fp.GetPosition())
        pads = {p.GetNumber(): P(p.GetPosition()) for p in fp.Pads()}
        p1 = pads.get("1") or pads.get("A") or next(iter(pads.values()))
        w.writerow([ref, D.PARTS[ref][0], "Bottom" if fp.IsFlipped() else "Top", f"{x:.3f}", f"{y:.3f}",
                    element_rot(ref, fp), f"{p1[0]:.3f}", f"{p1[1]:.3f}"])
# ---------------------------------------------------------------------------------------------------------------
# Reference outputs from KiCad: the same board as Gerbers + drill (compare Altium's against these, layer by layer,
# in JLC's Gerber viewer) and a PDF of the copper
pcb_path = os.path.join(KDIR, NAME + ".kicad_pcb")
gdir = os.path.join(REF, "gerbers-reference")
shutil.rmtree(gdir, ignore_errors=True)
os.makedirs(gdir)
layers = "F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts"
subprocess.run(["kicad-cli", "pcb", "export", "gerbers", "-o", gdir + "/", "-l", layers, "--subtract-soldermask",
                "--erd", "--use-drill-file-origin", pcb_path], check=True, capture_output=True)
subprocess.run(["kicad-cli", "pcb", "export", "drill", "-o", gdir + "/", "--excellon-separate-th", "--generate-map",
                "--drill-origin", "plot",
                "--map-format", "pdf", pcb_path], check=True, capture_output=True)
import render  # noqa: E402
render.render(pcb_path, os.path.join(REF, NAME + "-board.pdf"), pours=True,
              title="Macropad concept B main board, seen from the top (red = top copper, blue = bottom copper)")
print(f"EAGLE files in {OUT}: {len(D.PARTS)} parts, {len(D.NETS)} nets, {len(packages)} packages; "
      f"{len(os.listdir(gdir))} reference Gerber/drill files")
