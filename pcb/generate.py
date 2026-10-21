#!/usr/bin/env python3
"""Altium inputs for the macropad's main PCB, one set per concept.

    python pcb/generate.py            # A, B and C
    python pcb/generate.py B

Reads build/report_<c>.json and dxf/pcb_outline_<c>.dxf (from tools/build.py) and
writes pcb/<c>/:
    BOM.csv            parts with UK price estimates
    connections.csv    net, designator, pin, pin name (easy to read / diff)
    macropad_<c>.NET   Protel netlist, imports into Altium (Design > Import Netlist)
    placement.csv      where every part goes, plate-frame mm, origin = case front-left
    placement.svg      the same as a drawing, top view
    pcb_outline.dxf    copy of the board outline (mm, same origin)

Same layout as pcb/altium-import/generate.py for the trackball. The pin map matches
firmware/boards/promicro_nrf52840_nrf52840_uf2.overlay; change both together.
Needs: pip install shapely
"""
import csv
import json
import os
import re
import shutil
import sys
from collections import defaultdict

from shapely.geometry import LineString, Point, box
from shapely.ops import polygonize, unary_union

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_ROOT = os.environ.get("MACROPAD_OUT", ROOT)

# ---------------------------------------------------------------------------
# Controller: Pro Micro footprint, nice!nano v2 / SuperMini nRF52840 pin names.
# Pins 1-12 run down the left side and 13-24 up the right, seen from the module's
# component side with USB-C at the top (the usual Pro Micro numbering).
# (pin, label, nRF pin, net). None = not connected on this concept.
# ---------------------------------------------------------------------------
def u1_pins(rows, cols_total):
    return [
        (1, "D1", "P0.06", "DBG_TX"),
        (2, "D0", "P0.08", "ROW3" if rows > 3 else None),
        (3, "GND", "GND", "GND"),
        (4, "GND", "GND", "GND"),
        (5, "D2", "P0.17", "LCD_SCK"),
        (6, "D3", "P0.20", "LCD_MOSI"),
        (7, "D4", "P0.22", "LCD_CS"),
        (8, "D5", "P0.24", "LCD_DC"),
        (9, "D6", "P1.00", "ROW0"),
        (10, "D7", "P0.11", "ROW1"),
        (11, "D8", "P1.04", "ROW2"),
        (12, "D9", "P1.06", "COL0"),
        (13, "D10", "P0.09", "ENC_A"),
        (14, "D16", "P0.10", "ENC_B"),
        (15, "D14", "P1.11", "COL1"),
        (16, "D15", "P1.13", "COL2"),
        (17, "D18", "P1.15", "LCD_RST"),
        (18, "D19", "P0.02", "LCD_BL"),
        (19, "D20", "P0.29", "COL3"),
        (20, "D21", "P0.31", "COL4" if cols_total > 4 else None),
        (21, "VCC", "3V3 out (P0.13 switched)", "3V3_SW"),
        (22, "RST", "nRESET", "NRST"),
        (23, "GND", "GND", "GND"),
        (24, "B+", "Battery +", "VBAT_SW"),
    ]


# LCD module cable, Waveshare order (same on the 1.28", 1.69" and 2.0" modules)
LCD_PINS = [(1, "VCC", "3V3_SW"), (2, "GND", "GND"), (3, "DIN", "LCD_MOSI"), (4, "CLK", "LCD_SCK"),
            (5, "CS", "LCD_CS"), (6, "DC", "LCD_DC"), (7, "RST", "LCD_RST"), (8, "BL", "LCD_BL")]

DISPLAY = {
    "A": ("Waveshare 1.69inch LCD Module (ST7789V2 240x280)", 9.00),
    "B": ("Waveshare 2inch LCD Module (ST7789V 240x320)", 11.00),
    "C": ("Waveshare 1.28inch Round LCD Module (GC9A01 240x240)", 11.00),
}
LIPO = {"A": ("603040 LiPo 3.7 V ~800 mAh, JST-PH lead", 6.00),
        "B": ("603040 LiPo 3.7 V ~800 mAh, JST-PH lead", 6.00),
        "C": ("803040 LiPo 3.7 V ~1000 mAh, JST-PH lead", 7.00)}

# Bottom-side footprint sizes (x, y) in mm, including pads, for the overlap check
SOCKET_BOX = (-7.6, 1.3, 6.4, 7.0)      # Kailh MX socket relative to the switch centre
DIODE = (5.0, 2.0)                      # SOD-123 incl. pads
CAP = (3.0, 1.8)                        # 0805 incl. pads
JST2 = (6.0, 4.6)                       # JST PH 2-pin vertical THT
TACT = (6.6, 4.0)                       # 6 x 3.5 mm tact switch incl. legs
PADS8 = (20.8, 2.6)                     # 8 wire pads, 2.54 mm pitch
TP = (1.6, 1.6)
SLIDE = (4.0, 9.0)                      # right-angle slide switch, as in macropad.scad
U1_BOX = (18.0, 33.0)
ENC_BOX = (13.0, 16.0)


def read_dxf_lines(path):
    """OpenSCAD writes the outline as plain LINE entities: group codes 10/20 and 11/21."""
    lines, cur = [], {}
    tokens = [t.strip() for t in open(path).read().split("\n")]
    for code, value in zip(tokens[0::2], tokens[1::2]):
        if code == "0":
            if {"10", "20", "11", "21"} <= cur.keys():
                lines.append(LineString([(cur["10"], cur["20"]), (cur["11"], cur["21"])]))
            cur = {}
        elif code in ("10", "20", "11", "21"):
            cur[code] = float(value)
    return lines


def pcb_polygon(path):
    """Outer outline minus every hole (display cut-out, key centre holes, pillar holes)."""
    loops = sorted(polygonize(unary_union(read_dxf_lines(path))), key=lambda p: -p.area)
    outer, holes = loops[0], loops[1:]
    board = outer
    for h in holes:
        board = board.difference(h)
    return outer, holes, board


def rect(cx, cy, w, h):
    return box(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)


class Layout:
    """Bottom-side parts and keep-outs, so each new part can find a free spot."""

    def __init__(self, outer, cutout):
        self.outer = outer.buffer(-0.6)          # 0.6 mm from the board edge
        self.cutout = cutout.buffer(0.6)
        self.taken = []                          # (designator, shape)

    def free(self, shape, ignore=()):
        if not self.outer.contains(shape) or shape.intersects(self.cutout):
            return False
        return all(not shape.intersects(s.buffer(0.4)) for d, s in self.taken if d not in ignore)

    def add(self, ref, shape):
        self.taken.append((ref, shape))

    def place(self, ref, want, size, rot=0, step=0.5, reach=40):
        """Nearest free spot to `want` on a 0.5 mm grid, spiralling outwards."""
        w, h = (size[1], size[0]) if rot in (90, 270) else size
        best = None
        n = int(reach / step)
        for i in range(-n, n + 1):
            for j in range(-n, n + 1):
                x, y = want[0] + i * step, want[1] + j * step
                d = (x - want[0]) ** 2 + (y - want[1]) ** 2
                if best is not None and d >= best[0]:
                    continue
                if self.free(rect(x, y, w, h)):
                    best = (d, x, y)
        if best is None:
            raise SystemExit(f"{ref}: no room near {want}")
        _, x, y = best
        self.add(ref, rect(x, y, w, h))
        return round(x, 2), round(y, 2)


def generate(concept):
    r = json.load(open(os.path.join(OUT_ROOT, "build", f"report_{concept}.json")))
    out = os.path.join(OUT_ROOT, "pcb", concept)
    os.makedirs(out, exist_ok=True)
    dxf = os.path.join(OUT_ROOT, "dxf", f"pcb_outline_{concept}.dxf")
    outer, holes, board = pcb_polygon(dxf)
    # The display opening is the biggest gap: a hole on A and B, a notch in the back
    # edge on C (the round screen's tab runs into the edge)
    notches = outer.convex_hull.difference(outer)
    notches = list(getattr(notches, "geoms", [notches]))
    cutout = max(holes + notches, key=lambda p: p.area)

    rows, cols = r["rows"], r["cols"]
    push_col = cols                               # the knob push gets its own column
    keys = r["keys_xy"]
    ex, ey = r["enc"]
    mx, my = r["mcu_c"]
    W, L, wall = r["W"], r["L"], r["wall"]

    parts = {}
    place = []          # (ref, layer, x, y, rot, footprint, note)
    nets = defaultdict(list)

    def c(net, ref, pin, name=""):
        nets[net].append((ref, str(pin), name or str(pin)))

    lay = Layout(outer, cutout)

    # --- controller, face down under the PCB, USB-C toward the back wall ---
    parts["U1"] = ("SuperMini nRF52840", "nice!nano v2 compatible", "generic (or nice!nano v2)",
                   "Pro Micro 24-pin DIP, 2.54 mm, rows 15.24 mm apart",
                   "nRF52840 module with LiPo charger and USB-C. Bottom side, components facing down, "
                   "on 2.5 mm low-profile headers; no headers on the 3 inner pins (P1.01, P1.02, P1.07)", 4.50)
    lay.add("U1", rect(mx, my, *U1_BOX))
    place.append(("U1", "Bottom", mx, my, 0, "PRO_MICRO_24",
                  "Mirrored by Altium on the bottom layer. USB-C end toward +y (back wall)"))
    for pin, label, port, net in u1_pins(rows, push_col + 1):
        if net:
            c(net, "U1", pin, f"{label} ({port})" if port.startswith("P") else label)

    # --- keys: hot-swap socket + diode each ---
    # The model lists keys front row first; the firmware's row 0 is the back row (next
    # to the screen, top row of tiles). SWn / Dn follow the firmware: key n - 1.
    fw_keys = {}
    for k, xy in enumerate(keys):
        row, col = rows - 1 - k // cols, k % cols
        fw_keys[row * cols + col] = (row, col, xy)
    keys = [fw_keys[i][2] for i in range(len(fw_keys))]
    n = len(keys)
    for k, (kx, ky) in enumerate(keys):
        row, col, _ = fw_keys[k]
        sw, d = f"SW{k + 1}", f"D{k + 1}"
        parts[sw] = ("MX hot-swap socket", "CPG151101S11", "Kailh", "MX hot-swap socket (pads on bottom)",
                     "Key socket, switch plugs in from the top", 0.12)
        parts[d] = ("1N4148W", "1N4148W-7-F", "Diodes Inc", "SOD-123", "Matrix diode", 0.03)
        lay.add(sw, box(kx + SOCKET_BOX[0], ky + SOCKET_BOX[1], kx + SOCKET_BOX[2], ky + SOCKET_BOX[3]))
        place.append((sw, "Top", kx, ky, 0, "MX_HOTSWAP",
                      f"row {row} col {col}; switch pins toward +y (back), socket on the bottom"))
        c(f"ROW{row}", sw, 1)
        c(f"K{k + 1}", sw, 2)
        c(f"K{k + 1}", d, 1, "A")
        c(f"COL{col}", d, 2, "K")
    for k, (kx, ky) in enumerate(keys):
        x, y = lay.place(f"D{k + 1}", (kx, ky - 5.5), DIODE)
        place.append((f"D{k + 1}", "Bottom", x, y, 0, "SOD-123", "cathode (bar) toward +x"))

    # --- knob: EC11 with push switch; push is wired into row 0, its own column ---
    dp = f"D{n + 1}"
    parts["ENC1"] = ("EC11 encoder with switch", "EC11E15244G1", "Alps Alpine (or generic EC11)",
                     "EC11, THT, 15-20 mm D-shaft", "Knob: volume, push = mute", 1.80)
    parts[dp] = ("1N4148W", "1N4148W-7-F", "Diodes Inc", "SOD-123", "Matrix diode", 0.03)
    place.append(("ENC1", "Top", ex, ey, 0, "EC11_SW",
                  "A/C/B pins toward the front (-y), switch pins toward the back. Trim all pins flush "
                  "underneath" + (" (U1 sits under it)" if lay.taken[0][1].intersects(rect(ex, ey, *ENC_BOX)) else "")))
    c("ENC_A", "ENC1", "A"); c("GND", "ENC1", "C"); c("ENC_B", "ENC1", "B")
    c("ROW0", "ENC1", "S1"); c("K_PUSH", "ENC1", "S2")
    c("K_PUSH", dp, 1, "A"); c(f"COL{push_col}", dp, 2, "K")
    lay.add("ENC1", rect(ex, ey, *ENC_BOX))
    x, y = lay.place(dp, (ex - 4, ey + 10), DIODE)
    place.append((dp, "Bottom", x, y, 0, "SOD-123", "knob push diode, cathode toward +x"))
    for ref, net, want in (("C1", "ENC_A", (ex - 4, ey - 11)), ("C2", "ENC_B", (ex + 4, ey - 11))):
        parts[ref] = ("10nF", "", "", "0805", "Encoder debounce (with the internal pull-up)", 0.02)
        c(net, ref, 1); c("GND", ref, 2)
        x, y = lay.place(ref, want, CAP)
        place.append((ref, "Bottom", x, y, 0, "0805", f"{net} to GND, close to ENC1"))

    # --- LCD module: 8 wire pads in front of the display opening ---
    cx0, cy0, cx1, cy1 = cutout.bounds
    parts["J2"] = ("LCD wires", "", "", "8 x 1.0 mm plated holes, 2.54 mm pitch",
                   "Solder the module's cable here (Waveshare order)", 0)
    # Left of the opening, where the Waveshare modules have their connector
    x, y = lay.place("J2", (cx0 - 2.5, (cy0 + cy1) / 2), PADS8, rot=90)
    place.append(("J2", "Bottom", x, y, 90, "PADS_1x8_2.54", "pin 1 (VCC) at the -y end"))
    for pin, name, net in LCD_PINS:
        c(net, "J2", pin, name)
    parts["C3"] = ("10uF", "", "", "0805", "LCD supply bulk (backlight switch-on)", 0.05)
    c("3V3_SW", "C3", 1); c("GND", "C3", 2)
    x, y = lay.place("C3", (x, y - 13), CAP, rot=90)
    place.append(("C3", "Bottom", x, y, 90, "0805", "next to J2 pin 1"))

    # --- power: LiPo plug, slide switch in the right wall, reset button ---
    parts["J1"] = ("Battery", "B2B-PH-K-S(LF)(SN)", "JST", "JST PH 2-pin, THT, vertical",
                   "LiPo plug. Check the cell's lead polarity before plugging in", 0.20)
    c("VBAT", "J1", 1, "BAT+"); c("GND", "J1", 2, "BAT-")
    bx, by = r["bat"][0], r["bat"][1]
    x, y = lay.place("J1", (cx1 + 4, cy0 - 3), JST2)
    place.append(("J1", "Bottom", x, y, 0, "JST_PH_2_V", "pin 1 = BAT+"))
    parts["SW_PWR"] = ("Power switch", "SK12D07VG4", "generic", "SPDT slide, right-angle THT, 2.54 mm",
                       "Battery on/off. Actuator pokes out of the right wall slot. MEASURE vs case slot", 0.30)
    c("VBAT", "SW_PWR", 1); c("VBAT_SW", "SW_PWR", 2, "COM")
    sx = W - wall - 0.3 - SLIDE[0] / 2
    lay.add("SW_PWR", rect(sx, r["sw_y"], *SLIDE))
    place.append(("SW_PWR", "Bottom", round(sx, 2), r["sw_y"], 90, "SLIDE_RA",
                  "actuator toward +x through the right wall, matches power_switch() in macropad.scad"))
    parts["SW_RST"] = ("Reset", "PTS636 SM25 SMTR LFS", "C&K", "6 x 3.5 mm tact, gull-wing",
                       "Double-press = UF2 bootloader (case open)", 0.25)
    c("NRST", "SW_RST", 1); c("GND", "SW_RST", 2)
    x, y = lay.place("SW_RST", (mx - 14, my + 10), TACT)
    place.append(("SW_RST", "Bottom", x, y, 0, "TACT_6x3.5", "only needed to recover a bricked board"))

    # --- test pads, mounting holes ---
    for ref, net, want in (("TP1", "DBG_TX", (mx - 4, my - 19)), ("TP2", "GND", (mx + 4, my - 19))):
        parts[ref] = (net, "", "", "1.5 mm test pad", "UART log out (115200), optional", 0)
        c(net, ref, 1)
        x, y = lay.place(ref, want, TP)
        place.append((ref, "Bottom", x, y, 0, "TP_1.5", net))
    for i, (px, py) in enumerate(r["pillars"], 1):
        ref = f"H{i}"
        parts[ref] = ("M2 hole", "", "", "2.2 mm NPTH", "M2 self-tapping screw into the case pillar", 0)
        place.append((ref, "Both", px, py, 0, "HOLE_2.2", "already in the DXF outline"))

    # --- off-board parts that belong in the BOM ---
    extras = [
        ("LCD", DISPLAY[concept][0], "", "Waveshare", "module", "Screen, sits in the case window", DISPLAY[concept][1]),
        ("BT1", LIPO[concept][0], "", "", "pouch cell", "Under the display band, on the bottom plate", LIPO[concept][1]),
    ]

    used = {ref for v in nets.values() for ref, _, _ in v}
    missing = set(parts) - used - {p[0] for p in place if p[0].startswith("H")}
    assert not missing, missing
    singles = [n_ for n_, v in nets.items() if len(v) < 2]
    # DBG_TX goes to a test pad only, which is the point
    assert set(singles) <= {"DBG_TX"}, singles

    # overlaps between bottom-side parts (U1 over ENC1 pins is expected, see the note)
    clashes = []
    for i, (a, sa) in enumerate(lay.taken):
        for b, sb in lay.taken[i + 1:]:
            if {a, b} == {"U1", "ENC1"}:
                continue
            if sa.intersection(sb).area > 0.01:
                clashes.append((a, b))
    assert not clashes, clashes

    # ---- files ----
    def keyf(ref):
        m = re.match(r"([A-Z_]+?)(\d*)$", ref)
        return (m.group(1), int(m.group(2) or 0))

    with open(os.path.join(out, "connections.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Net", "Designator", "Pin", "Pin name"])
        for net_ in sorted(nets):
            for ref, pin, name in sorted(nets[net_], key=lambda t: (keyf(t[0]), t[1])):
                w.writerow([net_, ref, pin, name])

    with open(os.path.join(out, f"macropad_{concept}.NET"), "w", newline="\r\n") as f:
        for ref, v in sorted(parts.items(), key=lambda kv: keyf(kv[0])):
            f.write(f"[\n{ref}\n{v[3]}\n{v[0]}\n\n\n\n]\n")
        for net_ in sorted(nets):
            f.write(f"(\n{net_}\n" + "".join(f"{ref}-{pin}\n" for ref, pin, _ in sorted(nets[net_])) + ")\n")

    groups, descs = defaultdict(list), defaultdict(list)
    for ref, (val, pn, mfr, pkg, desc, gbp) in parts.items():
        k = (val, pn, mfr, pkg, gbp)
        groups[k].append(ref)
        descs[k].append(desc)
    total = 0.0
    with open(os.path.join(out, "BOM.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Designators", "Qty", "Value", "Manufacturer", "Manufacturer part number",
                    "Package", "Est. unit GBP", "Description"])
        for k, refs in sorted(groups.items(), key=lambda kv: keyf(sorted(kv[1], key=keyf)[0])):
            refs = sorted(refs, key=keyf)
            val, pn, mfr, pkg, gbp = k
            total += gbp * len(refs)
            w.writerow([", ".join(refs), len(refs), val, mfr, pn, pkg, gbp or "",
                        "; ".join(dict.fromkeys(descs[k]))])
        for ref, val, pn, mfr, pkg, desc, gbp in extras:
            total += gbp
            w.writerow([ref, 1, val, mfr, pn, pkg, gbp, desc])

    with open(os.path.join(out, "placement.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Designator", "Layer", "X mm", "Y mm", "Rotation", "Footprint", "Note"])
        for row_ in sorted(place, key=lambda p: keyf(p[0])):
            w.writerow([row_[0], row_[1], f"{row_[2]:.2f}", f"{row_[3]:.2f}", row_[4], row_[5], row_[6]])

    shutil.copyfile(dxf, os.path.join(out, "pcb_outline.dxf"))
    write_svg(os.path.join(out, "placement.svg"), concept, r, outer, holes, lay, place)
    print(f"{concept}: {len(parts)} parts, {len(nets)} nets, est. board parts + LCD + LiPo GBP {total:.2f}")
    return total


def write_svg(path, concept, r, outer, holes, lay, place):
    W, L = r["W"], r["L"]
    pad = 8
    Y = lambda y: L - y            # plate y points up the drawing

    def poly(p, cls):
        pts = " ".join(f"{x:.2f},{Y(y):.2f}" for x, y in p.exterior.coords)
        return f'<polygon class="{cls}" points="{pts}"/>'

    s = [poly(outer, "board")]
    s += [poly(h, "hole") for h in holes]
    colours = {"U1": "u1", "ENC1": "enc", "SW_PWR": "pwr"}
    for ref, shape in lay.taken:
        cls = colours.get(ref, "sock" if ref.startswith("SW") else "part")
        s.append(poly(shape, cls))
    for ref, layer, x, y, rot, fp, note in place:
        if ref.startswith("SW") and ref[2:].isdigit():
            s.append(f'<text x="{x:.2f}" y="{Y(y) + 1.2:.2f}" class="lbl">{ref}</text>')
        elif ref.startswith("H"):
            s.append(f'<circle cx="{x:.2f}" cy="{Y(y):.2f}" r="1.1" class="hole"/>')
        elif not ref.startswith("D") or ref == "D" + str(len(r["keys_xy"]) + 1):
            s.append(f'<text x="{x:.2f}" y="{Y(y) + 0.9:.2f}" class="lbl">{ref}</text>')
    css = ("svg{background:#fff}.board{fill:#e8f1ea;stroke:#1f6f43;stroke-width:.4}"
           ".hole{fill:#fff;stroke:#1f6f43;stroke-width:.3}.sock{fill:#cfd5db;stroke:#5b636d;stroke-width:.2}"
           ".part{fill:#f3d9a4;stroke:#a06a00;stroke-width:.2}.u1{fill:#bcd0ee;fill-opacity:.7;stroke:#24477a;stroke-width:.3}"
           ".enc{fill:none;stroke:#0b6e74;stroke-width:.4;stroke-dasharray:1 .6}.pwr{fill:#e0b0b0;stroke:#8a2b2b;stroke-width:.2}"
           ".lbl{font:2.2px sans-serif;text-anchor:middle;fill:#222}.t{font:3px sans-serif;fill:#222}")
    title = (f'<text class="t" x="0" y="-7">Concept {concept} main PCB, top view, mm. Bottom-side parts drawn '
             f'as seen through the board.</text><text class="t" x="0" y="-3">Blue = controller (ENC1 dashed above it), '
             f'orange = small parts, grey = key sockets, red = power switch.</text>')
    open(path, "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad - 6} {W + 2 * pad + 40} {L + 2 * pad + 6}" '
        f'width="{(W + 2 * pad + 40) * 5:.0f}" height="{(L + 2 * pad + 6) * 5:.0f}"><style>{css}</style>'
        + title + "".join(s) + "</svg>")


if __name__ == "__main__":
    for c_ in (sys.argv[1:] or ["A", "B", "C"]):
        generate(c_)
