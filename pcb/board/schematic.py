#!/usr/bin/env python3
"""Concept B schematic: one A3 sheet, drawn in code from design_b.py.

The key matrix is drawn as a real matrix (row wires across, a diode down from every switch to its column wire);
everything else connects by net labels on short pin stubs, grouped by function. The same drawing is written to the
EAGLE .sch (Altium 19 imports it) and to a PDF for reading, and check() proves that the drawing's connections, read
the way Altium reads them (wire ends on pins, ends on wires, labels on wires, same-named labels), are exactly
design_b.NETS.

Units mm, y up, origin at the sheet's bottom-left corner; everything on the 2.54 mm grid.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "library", "src"))
import design_b as D  # noqa: E402
from jr_parts import part  # noqa: E402
from jr_symbols import all_symbols  # noqa: E402

G = 2.54
SYMS = all_symbols()
SHEET_W, SHEET_H = 420.0, 297.0          # A3 landscape
ROT = {0: lambda x, y: (x, y), 90: lambda x, y: (-y, x), 180: lambda x, y: (-x, -y), 270: lambda x, y: (y, -x)}


def g(n):
    return round(n * G, 4)


def snap(v):
    return round(round(v / G) * G, 4)


class Sheet:
    def __init__(self):
        self.inst = {}        # ref -> (x, y, rot)
        self.wires = []       # (net, (x1, y1), (x2, y2))
        self.labels = []      # (net, x, y, rot)
        self.junctions = []   # (net, x, y)
        self.texts = []       # (text, x, y, size, rot, align)
        self.lines = []       # frame / boxes: ((x1, y1), (x2, y2), width)

    # ---- parts and pins
    def part(self, ref, x, y, rot=0):
        assert ref in D.PARTS, ref
        self.inst[ref] = (snap(x), snap(y), rot)

    def sym(self, ref):
        return SYMS[part(D.PARTS[ref][0])["symbol"]]

    def pin(self, ref, num):
        x, y, rot = self.inst[ref]
        for n, name, px, py, d, length in self.sym(ref).pins:
            if n == str(num):
                dx, dy = ROT[rot](px, py)
                return (round(x + dx, 4), round(y + dy, 4)), (d + rot) % 360
        raise KeyError((ref, num))

    # ---- drawing
    def wire(self, net, *pts):
        for a, b in zip(pts, pts[1:]):
            self.wires.append((net, (round(a[0], 4), round(a[1], 4)), (round(b[0], 4), round(b[1], 4))))

    def junction(self, net, x, y):
        self.junctions.append((net, round(x, 4), round(y, 4)))

    def label(self, net, x, y, rot=0):
        self.labels.append((net, round(x, 4), round(y, 4), rot))

    def stub(self, ref, num, net, length=g(2)):
        """Short wire out of a pin with a net label at its end, text reading away from the part."""
        (x, y), d = self.pin(ref, num)
        out = {0: (-1, 0), 90: (0, -1), 180: (1, 0), 270: (0, 1)}[d]       # away from the body
        e = (x + out[0] * length, y + out[1] * length)
        self.wire(net, (x, y), e)
        self.label(net, e[0], e[1], {(1, 0): 0, (-1, 0): 180, (0, 1): 90, (0, -1): 270}[out])

    def text(self, t, x, y, size=1.778, rot=0, align="bottom-left"):
        self.texts.append((t, x, y, size, rot, align))

    def box(self, x0, y0, x1, y1, title=None, w=0.254):
        for a, b in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
            self.lines.append((a, b, w))
        if title:
            self.text(title, x0 + 2.0, y1 - 4.2, 2.5)


def build():
    s = Sheet()
    s.box(5, 5, SHEET_W - 5, SHEET_H - 5, w=0.4)
    net_of = {(r, p): n for n, lst in D.NETS.items() for r, p in lst}

    # ---- controller -------------------------------------------------------------------------------------------
    s.box(15, 140, 145, 285, "Controller: SuperMini nRF52840 (U1, bottom side, face down)")
    s.part("U1", g(32), g(84))
    for pin, label, port, net in D.U1_PINS:
        if net:
            s.stub("U1", pin, net, g(3))
        else:
            (x, y), _ = s.pin("U1", pin)
            s.text("NC", x - g(2), y - 0.8, 1.524)
    s.text("Pin map = firmware/boards/promicro_nrf52840_nrf52840_uf2.overlay", 20, 153, 1.778)
    s.text("LCD SPI on full-speed pins (P0.20 clock, P0.17 data). P0.09/P0.10 (NFC) carry the knob.", 20, 149, 1.778)
    s.text("VCC (pin 21) is switched by P0.13: the firmware turns the LCD supply on.", 20, 145, 1.778)

    # ---- key matrix -------------------------------------------------------------------------------------------
    s.box(155, 140, 330, 285, "Key matrix: rows = inputs with pull-ups, columns driven low")
    X0, Y0, DX, DY = g(68), g(104), g(11), g(11)
    nrow, ncol = D.ROWS, D.COLS + 1                       # + knob push column
    cells = {}
    for n, r, c, kx, ky in D.KEYS:
        cells[(r, c)] = (f"SW{n + 1}", f"D{n + 1}", f"K{n + 1}")
    cells[(0, D.PUSH_COL)] = (None, D.DP, "K_PUSH")
    for (r, c), (sw, d, knet) in cells.items():
        xc, yc = X0 + c * DX, Y0 - r * DY
        s.part(d, xc + g(3), yc - g(3), 270)                # anode up, cathode down
        if sw:
            s.part(sw, xc, yc)
            s.wire(knet, s.pin(sw, 2)[0], (xc + g(3), yc), s.pin(d, 2)[0])
            s.text(f"key {int(sw[2:]) - 1}", xc - g(2), yc - g(2) - 1.0, 1.524)
        else:
            a = s.pin(d, 2)[0]
            s.wire(knet, a, (a[0], yc), (xc - g(1), yc))
            s.label(knet, xc - g(1), yc, 180)
            s.text("knob push (key 16)", xc - g(4), yc + g(2), 1.524)
        k = s.pin(d, 1)[0]
        s.wire(f"COL{c}", k, (xc + g(5), k[1]))
    for c in range(ncol):
        xl = X0 + c * DX + g(5)
        rows_here = sorted(r for (r, cc) in cells if cc == c)
        ys = [Y0 - r * DY - g(5) for r in rows_here]
        bottom = ys[-1] - g(3)
        pts = [(xl, y) for y in ys] + [(xl, bottom)]
        s.wire(f"COL{c}", *pts)
        for y in ys[1:]:
            s.junction(f"COL{c}", xl, y)
        if len(ys) > 0:
            s.junction(f"COL{c}", xl, ys[-1]) if len(ys) > 1 or True else None
        s.label(f"COL{c}", xl, bottom, 270)
    # rows: a wire above the switches, each switch's pin 1 rises to it
    for r in range(nrow):
        yr = Y0 - r * DY + g(2)
        sws = [cells[(r, c)][0] for c in range(ncol) if (r, c) in cells and cells[(r, c)][0]]
        xs = []
        for sw in sws:
            p = s.pin(sw, 1)[0]
            s.wire(f"ROW{r}", p, (p[0], yr))
            xs.append(p[0])
        xstart = X0 - g(5)
        pts = [(xstart, yr)] + [(x, yr) for x in xs]
        s.wire(f"ROW{r}", *pts)
        for x in xs[:-1]:
            s.junction(f"ROW{r}", x, yr)
        s.label(f"ROW{r}", xstart, yr, 180)
    # the bottom junction of each column line is a T (column continues down to its label); the top is a corner
    s.junctions = [j for j in s.junctions if not (j[0].startswith("COL") and
                   abs(j[2] - (Y0 - g(5))) < 1e-6)]

    # ---- knob --------------------------------------------------------------------------------------------------
    s.box(155, 75, 330, 135, "Knob: EC11-size encoder with push (PEC11R-4220F-S0024)")
    s.part("ENC1", g(80), g(42))
    for pin in ("A", "C", "B", "S1", "S2"):
        s.stub("ENC1", pin, net_of[("ENC1", pin)], g(3))
    s.part("C1", g(104), g(42)); s.stub("C1", 1, "ENC_A"); s.stub("C1", 2, "GND")
    s.part("C2", g(116), g(42)); s.stub("C2", 1, "ENC_B"); s.stub("C2", 2, "GND")
    s.text("24 detents / 24 pulses: both contacts open at every detent", 160, 82, 1.778)
    s.text("(no current through the NFC pins at rest). 10 nF + internal pull-up = debounce.", 160, 78.5, 1.778)

    # ---- LCD -------------------------------------------------------------------------------------------------
    s.box(15, 75, 145, 135, "LCD: Waveshare 2.0in ST7789 module on 8 wires (J2)")
    s.part("J2", g(24), g(40))
    for pin, name, net in D.J2_PINS:
        s.stub("J2", pin, net, g(3))
        (x, y), _ = s.pin("J2", pin)
        s.text(name, x + g(3), y - 0.8, 1.778)
    s.part("C3", g(44), g(40)); s.stub("C3", 1, "3V3_SW"); s.stub("C3", 2, "GND")
    s.text("Wires in the module's cable order: VCC GND DIN CLK CS DC RST BL", 20, 82, 1.778)
    s.text("C3 = bulk for the backlight switch-on, next to U1 pin 21", 20, 78.5, 1.778)

    # ---- power -----------------------------------------------------------------------------------------------
    s.box(340, 200, 415, 285, "Power")
    s.part("J1", g(142), g(104))
    s.stub("J1", 1, "VBAT"); s.stub("J1", 2, "GND")
    s.text("LiPo +", g(142) + g(2), g(105) - 0.8, 1.778); s.text("LiPo -", g(142) + g(2), g(104) - 0.8, 1.778)
    s.part("SW_PWR", g(150), g(92))
    s.stub("SW_PWR", 1, "VBAT"); s.stub("SW_PWR", 2, "VBAT_SW")
    (x, y), _ = s.pin("SW_PWR", 3); s.text("NC", x + 1.0, y - 0.8, 1.524)
    s.text("Slide switch in the right wall:", 345, 215, 1.778)
    s.text("ON = battery to U1 B+ (charger", 345, 211.5, 1.778)
    s.text("output; USB charges through it)", 345, 208, 1.778)

    # ---- reset, debug, holes ------------------------------------------------------------------------------------
    s.box(340, 75, 415, 195, "Reset, debug, mounting")
    s.part("SW_RST", g(146), g(68))
    (p1, _), (p2, _) = s.pin("SW_RST", 1), s.pin("SW_RST", 2)
    xa = p1[0] - g(1)
    s.wire("NRST", p1, (xa, p1[1]), (xa, p2[1]), p2)
    s.wire("NRST", (xa, (p1[1] + p2[1]) / 2), (xa - g(3), (p1[1] + p2[1]) / 2))
    s.junction("NRST", xa, (p1[1] + p2[1]) / 2)
    s.label("NRST", xa - g(3), (p1[1] + p2[1]) / 2, 180)
    (p3, _), (p4, _) = s.pin("SW_RST", 3), s.pin("SW_RST", 4)
    xb = p3[0] + g(1)
    s.wire("GND", p3, (xb, p3[1]), (xb, p4[1]), p4)
    s.wire("GND", (xb, (p3[1] + p4[1]) / 2), (xb + g(3), (p3[1] + p4[1]) / 2))
    s.junction("GND", xb, (p3[1] + p4[1]) / 2)
    s.label("GND", xb + g(3), (p3[1] + p4[1]) / 2, 0)
    s.text("Double-press = UF2 bootloader", 345, 160, 1.778)
    s.part("TP1", g(140), g(56)); s.stub("TP1", 1, "DBG_TX")
    s.part("TP2", g(150), g(56)); s.stub("TP2", 1, "GND")
    s.text("UART log out, 115200 8N1", 345, 133, 1.778)
    for i in range(1, 5):
        s.part(f"H{i}", g(138 + (i - 1) * 7), g(40))
    s.text("M2 screws into the case pillars", 345, 93, 1.778)

    # ---- notes and title block -----------------------------------------------------------------------------------
    notes = [
        "NOTES",
        "1. Every part is in the JR library (JR.SchLib / JR.PcbLib); parameters carry the LCSC numbers.",
        "2. U1 is soldered face down on 2.5 mm low-profile headers. Trim ENC1 pins flush first; Kapton on U1's back.",
        "3. Firmware key n = SW(n+1): row 0 is the back row (next to the screen), SW1 = back-left = top-left tile.",
        "4. Knob push sits in row 0, column 4 with its own diode (D13); firmware key 16 on every concept.",
        "5. Switch sockets, diodes, U1, J1, J2, power and reset are on the bottom; switches and the knob on top.",
    ]
    for i, t in enumerate(notes):
        s.text(t, 15, 62 - i * 5.0, 2.0 if i == 0 else 1.778)
    s.box(300, 10, 415, 40)
    s.text(D.TITLE, 303, 31, 2.5)
    s.text(f"Rev {D.REV}   {D.DATE}   Sheet 1/1   A3", 303, 25, 2.0)
    s.text("Drawn by pcb/board/schematic.py from design_b.py", 303, 19, 1.778)
    s.text("github.com/jasoneroberts/macropad", 303, 14, 1.778)
    return s


# ---------------------------------------------------------------------------------------------------------------
def _on_segment(p, a, b, eps=1e-4):
    (px, py), (ax, ay), (bx, by) = p, a, b
    if abs((bx - ax) * (py - ay) - (by - ay) * (px - ax)) > eps:
        return False
    return min(ax, bx) - eps <= px <= max(ax, bx) + eps and min(ay, by) - eps <= py <= max(ay, by) + eps


def check(s):
    """Connectivity as Altium sees it (geometry and label names only), compared with design_b.NETS."""
    parent = {}

    def find(k):
        parent.setdefault(k, k)
        while parent[k] != k:
            parent[k] = parent[parent[k]]; k = parent[k]
        return k

    def union(a, b):
        parent[find(a)] = find(b)

    pins = {}
    for ref in s.inst:
        for n, *_ in s.sym(ref).pins:
            pins[(ref, n)] = s.pin(ref, n)[0]
    pts = lambda: [("w", i) for i in range(len(s.wires))]
    for i, (_, a, b) in enumerate(s.wires):
        find(("w", i))
    for i, (_, a, b) in enumerate(s.wires):
        for j, (_, c, d) in enumerate(s.wires):
            if j <= i:
                continue
            # wires connect where an end of one lies on the other (end-to-end or T); crossings do not
            if any(_on_segment(e, c, d) for e in (a, b)) or any(_on_segment(e, a, b) for e in (c, d)):
                union(("w", i), ("w", j))
    for key, p in pins.items():
        find(("p",) + key)
        for i, (_, a, b) in enumerate(s.wires):
            if p in (a, b):
                union(("p",) + key, ("w", i))
            elif _on_segment(p, a, b):
                raise SystemExit(f"pin {key} sits in the middle of a wire")
    for k, (name, x, y, _) in enumerate(s.labels):
        hit = [i for i, (_, a, b) in enumerate(s.wires) if _on_segment((x, y), a, b)]
        assert hit, f"label {name} at {(x, y)} is not on a wire"
        union(("l", name), ("w", hit[0]))
    # pins touching each other directly would also connect
    vals = list(pins.items())
    for i, (k1, p1) in enumerate(vals):
        for k2, p2 in vals[i + 1:]:
            if p1 == p2:
                union(("p",) + k1, ("p",) + k2)
    groups = {}
    for key in pins:
        groups.setdefault(find(("p",) + key), set()).add(key)
    names = {}
    for name, *_ in s.labels:
        names.setdefault(find(("l", name)), set()).add(name)
    got = {}
    for root, members in groups.items():
        nm = names.get(root, set())
        assert len(nm) <= 1, f"labels {nm} are shorted together"
        if len(members) > 1 or nm:
            got[next(iter(nm)) if nm else "?" + str(sorted(members))] = members
    want = {n: set(v) for n, v in D.NETS.items()}
    # unnamed groups must match a design net by membership
    for k in [k for k in got if k.startswith("?")]:
        m = got.pop(k)
        hit = [n for n, v in want.items() if v == m]
        assert hit, f"unnamed connection {sorted(m)} matches no net"
        got[hit[0]] = m
    bad = {n for n in set(want) | set(got) if want.get(n) != got.get(n)}
    for n in sorted(bad):
        print("MISMATCH", n, "want", sorted(want.get(n, [])), "got", sorted(got.get(n, [])))
    assert not bad, "schematic connections differ from design_b.NETS"
    assert set(s.inst) == set(D.PARTS), set(D.PARTS) ^ set(s.inst)
    # every drawn wire carries the net its connections say it does
    return len(got)




# ---------------------------------------------------------------------------------------------------------------
def rotated_label_at(ref, x, y):
    """Bottom-left anchors of the designator and value of a part turned 90/270 (the symbol's own field spots would
    land on its body). Diodes sit just right of a matrix column wire, so theirs go on the left; others on the right.
    The EAGLE export writes the same spots as smashed NAME / VALUE attributes."""
    if ref.startswith("D"):
        return (x - 7.6, y - 0.3), (x - 9.1, y - 2.3)
    return (x + 2.2, y + 0.6), (x + 2.2, y - 1.6)




def render(s, out):
    """PDF/PNG of the sheet (matplotlib), drawn from the same objects as the EAGLE file."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, Polygon, Rectangle
    fig = plt.figure(figsize=(SHEET_W / 25.4, SHEET_H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, SHEET_W); ax.set_ylim(0, SHEET_H); ax.set_aspect("equal"); ax.axis("off")
    SYM, PIN, WIRE, LAB = "#8b1a1a", "#8b1a1a", "#0b6623", "#1f3a93"
    pt_size = lambda mm_: mm_ * 72 / 25.4 * 0.85
    for a, b, w in s.lines:
        ax.plot([a[0], b[0]], [a[1], b[1]], color="#555", lw=w * 2)
    for ref, (x, y, rot) in s.inst.items():
        sym = s.sym(ref)
        T = lambda px, py: (x + ROT[rot](px, py)[0], y + ROT[rot](px, py)[1])
        for it in sym.items:
            k = it[0]
            if k == "rect":
                _, x0, y0, x1, y1, filled = it
                c = [T(x0, y0), T(x1, y0), T(x1, y1), T(x0, y1)]
                ax.add_patch(Polygon(c, closed=True, fc=SYM if filled else ("#fffbe6" if (x1 - x0) * (y1 - y0) > 20 else "none"),
                                     ec=SYM, lw=0.6))
            elif k == "poly":
                _, ps, filled = it
                ps = [T(*p) for p in ps]
                if filled:
                    ax.add_patch(Polygon(ps, closed=True, fc=SYM, ec=SYM, lw=0.4))
                else:
                    ax.plot([p[0] for p in ps], [p[1] for p in ps], color=SYM, lw=0.6)
            elif k == "circle":
                _, cx, cy, r, filled = it
                ax.add_patch(Circle(T(cx, cy), r, fc=SYM if filled else "none", ec=SYM, lw=0.6))
            elif k == "text":
                _, t, tx, ty, size = it
                ax.text(*T(tx, ty), t, fontsize=pt_size(size), color=SYM, ha="center", va="center")
        for n, name, px, py, d, length in sym.pins:
            (cx, cy), dd = s.pin(ref, n)
            ux, uy = {0: (1, 0), 90: (0, 1), 180: (-1, 0), 270: (0, -1)}[dd]
            ax.plot([cx, cx + ux * length], [cy, cy + uy * length], color=PIN, lw=0.6)
            if not sym.hide_pin_numbers:
                ax.text(cx + ux * length / 2, cy + uy * length / 2 + (0.6 if ux else 0), n, fontsize=pt_size(1.1),
                        color=PIN, ha="center", va="bottom" if ux else "center", rotation=0 if ux else 90)
            if not sym.hide_pin_names:
                ex, ey = cx + ux * (length + 0.8), cy + uy * (length + 0.8)
                ax.text(ex, ey, name, fontsize=pt_size(1.3), color="#333",
                        ha={1: "left", -1: "right", 0: "center"}[ux], va="center", rotation=0 if ux else 90)
        p = part(D.PARTS[ref][0])
        for i, (t, (fx, fy, just)) in enumerate(((ref, sym.ref_at), (p["value"], sym.val_at))):
            tx, ty = T(fx, fy)
            ha = {"left": "left", "right": "right", "center": "center"}[just]
            va = "center"
            if rot in (90, 270):        # same place as the smashed NAME / VALUE in the EAGLE file
                (tx, ty), ha, va = rotated_label_at(ref, x, y)[i], "left", "baseline"
            ax.text(tx, ty, t, fontsize=pt_size(1.6), color="#222" if t == ref else "#555", ha=ha, va=va,
                    rotation=0)
    for net, a, b in s.wires:
        ax.plot([a[0], b[0]], [a[1], b[1]], color=WIRE, lw=0.7)
    for net, x, y in s.junctions:
        ax.add_patch(Circle((x, y), 0.55, fc=WIRE, ec="none"))
    for net, x, y, rot in s.labels:
        ha, va, r = {0: ("left", "bottom", 0), 180: ("right", "bottom", 0), 90: ("left", "center", 90),
                     270: ("right", "center", 90)}[rot]
        ax.text(x + (0.4 if rot == 0 else -0.4 if rot == 180 else 0), y + (0.3 if rot in (0, 180) else 0.6 if rot == 90 else -0.6),
                net, fontsize=pt_size(1.6), color=LAB, ha=ha, va=va, rotation=r)
    for t, x, y, size, rot, align in s.texts:
        ax.text(x, y, t, fontsize=pt_size(size), color="#222", ha="left", va="bottom", rotation=rot)
    fig.savefig(out, dpi=200 if out.endswith(".png") else None)
    plt.close(fig)


if __name__ == "__main__":
    sh = build()
    print("schematic nets ok:", check(sh))
    if len(sys.argv) > 1:
        render(sh, sys.argv[1])
