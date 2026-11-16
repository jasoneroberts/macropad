#!/usr/bin/env python3
"""Builds the placed concept B board (KiCad) from design_b.py and the JR library.

    /usr/bin/python3 pcb/board/build_board.py <out dir>      -> <out>/macropad_B.kicad_pcb (placed, zones, no tracks)

The KiCad board is the working copy here: Freerouting routes it (route.py), KiCad checks it (DRC) and makes
reference Gerbers, and export_altium.py turns it into the EAGLE files that Altium 19 imports.
KiCad coordinates: x = 20 + plate x, y = 140 - plate y (KiCad's y points down).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "library", "src"))
import pcbnew  # noqa: E402

import design_b as D  # noqa: E402
from jr_parts import part  # noqa: E402

LIB = os.path.join(os.path.dirname(HERE), "library", "JR.pretty")
XO, YO = 20.0, 140.0
NAME = "macropad_B"


def K(x, y):
    return pcbnew.VECTOR2I(pcbnew.FromMM(XO + x), pcbnew.FromMM(YO - y))


def P(v):
    return (pcbnew.ToMM(v.x) - XO, YO - pcbnew.ToMM(v.y))


def mm(v):
    return pcbnew.FromMM(v)


def pad_xy(fp):
    return {p.GetNumber(): P(p.GetPosition()) for p in fp.Pads()}


def fab_box(fp):
    xs, ys = [], []
    for g in fp.GraphicalItems():
        if g.GetLayer() in (pcbnew.F_Fab, pcbnew.B_Fab, pcbnew.F_CrtYd, pcbnew.B_CrtYd) and not isinstance(g, pcbnew.FP_TEXT):
            bb = g.GetBoundingBox()
            for v in (bb.GetOrigin(), bb.GetEnd()):
                x, y = P(v); xs.append(x); ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)


def place(fp, side, want, check=None):
    """Put fp on side 'T'/'B' at the rotation that lands every pad in `want` where asked."""
    fp.SetPosition(K(0, 0))
    if side == "B":
        fp.Flip(K(0, 0), True)
    for ang in (0, 90, 180, 270):
        fp.SetOrientationDegrees(ang)
        fp.SetPosition(K(0, 0))
        q = pad_xy(fp)
        k0 = next(iter(want))
        dx, dy = want[k0][0] - q[k0][0], want[k0][1] - q[k0][1]
        if all(abs(q[k][0] + dx - x) < 1e-3 and abs(q[k][1] + dy - y) < 1e-3 for k, (x, y) in want.items()):
            fp.SetPosition(K(dx, dy))
            if check is None or check(fp):
                return ang
    raise SystemExit(f"{fp.GetReference()}: no rotation puts the pads at {want}")


CHECKS = {
    # the slide switch's actuator must point out through the right wall, the battery plug must open to the left
    "SW_PWR": lambda fp: fab_box(fp)[2] > D.X1 + 2.0,
    "J1": lambda fp: (fab_box(fp)[0] + fab_box(fp)[2]) / 2 < 86.0,
    "SW_RST": lambda fp: min(x for x, _ in pad_xy(fp).values()) > 70.0,
}


def add_shape(b, kind, layer, pts, w=0.1):
    s = pcbnew.PCB_SHAPE(b)
    s.SetLayer(layer)
    s.SetWidth(mm(w))
    if kind == "line":
        s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetStart(K(*pts[0])); s.SetEnd(K(*pts[1]))
    elif kind == "arc":
        s.SetShape(pcbnew.SHAPE_T_ARC); s.SetArcGeometry(K(*pts[0]), K(*pts[1]), K(*pts[2]))
    elif kind == "circle":
        s.SetShape(pcbnew.SHAPE_T_CIRCLE); s.SetCenter(K(*pts[0])); s.SetEnd(K(pts[0][0] + pts[1], pts[0][1]))
    b.Add(s)
    return s


def add_text(b, t, x, y, layer=pcbnew.B_SilkS, size=1.0, rot=0, just=None):
    s = pcbnew.PCB_TEXT(b)
    s.SetText(t); s.SetPosition(K(x, y)); s.SetLayer(layer)
    s.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size))); s.SetTextThickness(mm(max(0.15, size * 0.15)))
    s.SetTextAngleDegrees(rot)
    if layer in (pcbnew.B_SilkS, pcbnew.B_Fab, pcbnew.B_Cu):
        s.SetMirrored(True)
    if just == "left":
        s.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_LEFT if not s.IsMirrored() else pcbnew.GR_TEXT_H_ALIGN_RIGHT)
    b.Add(s)
    return s


def add_zone(b, pts, layers, net=None, rule=None, name=""):
    z = pcbnew.ZONE(b)
    ls = pcbnew.LSET()
    for l in layers:
        ls.AddLayer(l)
    z.SetLayerSet(ls)
    o = z.Outline(); o.NewOutline()
    for x, y in pts:
        o.Append(K(x, y))
    if rule:
        z.SetIsRuleArea(True)
        z.SetDoNotAllowCopperPour("pour" in rule); z.SetDoNotAllowVias("vias" in rule)
        z.SetDoNotAllowTracks("tracks" in rule); z.SetDoNotAllowPads(False); z.SetDoNotAllowFootprints(False)
    else:
        z.SetNet(net)
        z.SetLocalClearance(mm(0.3))
        z.SetMinThickness(mm(0.25))
        z.SetThermalReliefGap(mm(0.4))
        z.SetThermalReliefSpokeWidth(mm(0.4))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
        z.SetAssignedPriority(0)
    if name:
        z.SetZoneName(name)
    b.Add(z)
    return z


def circle_pts(cx, cy, r, n=24):
    import math
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def build(out):
    b = pcbnew.BOARD()
    ds = b.GetDesignSettings()
    ds.SetBoardThickness(mm(1.6))
    ds.SetCopperLayerCount(2)
    ds.m_TrackMinWidth = mm(0.2)
    ds.m_ViasMinSize = mm(0.6)
    ds.m_MinThroughDrill = mm(0.3)
    ds.m_MinClearance = mm(0.2)
    ds.m_CopperEdgeClearance = mm(0.3)
    ds.m_HoleClearance = mm(0.25)
    ds.m_HoleToHoleMin = mm(0.25)
    ds.SetAuxOrigin(K(0, 0))        # drill/place origin = the case's plate origin, so outputs use plate mm
    tb = b.GetTitleBlock()
    tb.SetTitle(D.TITLE); tb.SetRevision(D.REV); tb.SetDate(D.DATE); tb.SetCompany("Jase")
    tb.SetComment(0, "SuperMini nRF52840, 12 MX hot-swap keys, EC11 knob, 2.0in ST7789 LCD on wires")

    # outline
    for s in D.outline():
        add_shape(b, s[0], pcbnew.Edge_Cuts, s[1:], 0.1)

    # nets
    nets = {}
    for name in sorted(D.NETS):
        n = pcbnew.NETINFO_ITEM(b, name); b.Add(n); nets[name] = n
    padnet = {(r, p): n for n, lst in D.NETS.items() for r, p in lst}

    # footprints
    fps = {}
    for ref, (pname, note) in D.PARTS.items():
        p = part(pname)
        fp = pcbnew.FootprintLoad(LIB, p["footprint"])
        assert fp is not None, p["footprint"]
        fp.SetFPID(pcbnew.LIB_ID("JR", p["footprint"]))
        fp.SetReference(ref); fp.SetValue(p["value"])
        fp.Models().clear()
        b.Add(fp)
        side, want = D.PLACE[ref]
        place(fp, side, want, CHECKS.get(ref))
        for pad in fp.Pads():
            n = padnet.get((ref, pad.GetNumber()))
            if n:
                pad.SetNet(nets[n])
        fps[ref] = fp
    unplaced = set(D.PARTS) - set(D.PLACE)
    assert not unplaced, unplaced

    # Small parts' designators: keep them readable, 0.8 mm, and the sockets' on the fab layer only (silk is under
    # the socket bodies anyway); keys get a clear label on the bottom silk instead.
    for ref, fp in fps.items():
        t = fp.Reference()
        t.SetTextSize(pcbnew.VECTOR2I(mm(0.8), mm(0.8))); t.SetTextThickness(mm(0.15))
    for n, r, col, kx, ky in D.KEYS:
        fps[f"SW{n + 1}"].Reference().SetVisible(False)
        add_text(b, f"SW{n + 1}", kx - 3.0, ky - 2.6, size=0.9)
        fps[f"D{n + 1}"].Reference().SetPosition(K(kx, ky - 7.1))
        fps[f"D{n + 1}"].Reference().SetTextAngleDegrees(0)

    # ground pours on both layers
    poly = D.outline_polygon(4)
    add_zone(b, poly, [pcbnew.F_Cu], nets["GND"], name="GND top")
    add_zone(b, poly, [pcbnew.B_Cu], nets["GND"], name="GND bottom")
    # keep-outs: no pour over the controller (antenna end unknown), nothing near the case pillars' screws
    x0, y0, x1, y1 = D.U1_BOX
    add_zone(b, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], [pcbnew.F_Cu, pcbnew.B_Cu], rule="pour",
             name="U1: no pour (antenna)")
    for i, (px, py) in enumerate(D.REPORT["pillars"], 1):
        add_zone(b, circle_pts(px, py, D.PILLAR_KEEPOUT_R), [pcbnew.F_Cu, pcbnew.B_Cu], rule="pour vias tracks",
                 name=f"H{i} screw keep-out")

    # unplated slots (knob lugs): keep tracks 0.35 mm off the whole slot, not just the round hole the router sees
    for fp in fps.values():
        for p in fp.Pads():
            if p.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH and p.GetDrillSize().x != p.GetDrillSize().y:
                bb = p.GetBoundingBox()
                (xa, ya), (xb, yb) = P(bb.GetOrigin()), P(bb.GetEnd())
                m = 0.35
                xa, xb, ya, yb = min(xa, xb) - m, max(xa, xb) + m, min(ya, yb) - m, max(ya, yb) + m
                add_zone(b, [(xa, ya), (xb, ya), (xb, yb), (xa, yb)], [pcbnew.F_Cu, pcbnew.B_Cu],
                         rule="pour vias tracks", name=f"{fp.GetReference()} lug slot keep-out")

    # silkscreen
    add_text(b, "MACROPAD B  rev A  2026-11-11", 50.5, 8.0, size=1.2)
    add_text(b, "U1: SuperMini nRF52840, parts facing the board", 82.0, 114.6 - 3.0, pcbnew.B_Fab, 0.8)
    q = pad_xy(fps["J2"])
    J2X_LABEL = q["1"][0]
    for pin, label, _ in D.J2_PINS:
        x, y = q[str(pin)]
        add_text(b, label, x + 1.4, y, size=0.8, just="left")
    q = pad_xy(fps["J1"])
    add_text(b, "+", q["1"][0] + 2.9, q["1"][1], size=1.0)
    add_text(b, "-", q["2"][0] + 2.9, q["2"][1], size=1.0)
    add_text(b, "BATT", q["1"][0] + 4.4, (q["1"][1] + q["2"][1]) / 2, size=0.9, rot=90)
    q = pad_xy(fps["SW_PWR"])
    add_text(b, "ON", q["1"][0] - 2.4, q["1"][1], size=0.9, rot=90)
    add_text(b, "RESET", 74.5, 69.9, size=0.8)
    q = pad_xy(fps["TP1"]); add_text(b, "TX", q["1"][0], q["1"][1] + 1.6, size=0.8)
    q = pad_xy(fps["TP2"]); add_text(b, "GND", q["1"][0], q["1"][1] - 1.6, size=0.8)
    # designators of the parts around the knob and controller, where the defaults collide
    refpos = {"C1": (75.6, 77.35, 90), "C2": (88.4, 77.35, 90), "D13": (82.0, 78.4, 0), "C3": (71.0, 100.0, 0),
              "SW_RST": (74.5, 61.9 + 4.1, 0), "J1": (83.0, 72.0, 0), "TP1": (72.6, 112.2, 0), "TP2": (72.6, 106.6, 0),
              "J2": (91.7, 106.4, 0), "ENC1": (82.0, 96.6, 0), "U1": (82.0, 81.0, 0)}
    for ref, (x, y, rot) in refpos.items():
        t = fps[ref].Reference(); t.SetPosition(K(x, y)); t.SetTextAngleDegrees(rot)
    fps["TP1"].Reference().SetVisible(False); fps["TP2"].Reference().SetVisible(False)
    add_text(b, "USB-C", 82.0, 110.5, pcbnew.B_SilkS, 0.9)
    # top side: key numbers next to each switch (the firmware's key index), knob, and which side is which
    for n, r, col, kx, ky in D.KEYS:
        add_text(b, f"K{n}", kx - 7.6, ky + 7.6, pcbnew.F_SilkS, 0.9)
    add_text(b, "TOP: switches + knob.  BOTTOM: everything else", 50.5, 4.6, pcbnew.F_SilkS, 0.9)
    # mechanical notes on User.Drawings
    add_text(b, "Display opening: module sits here", 39.0, 90.0, pcbnew.Dwgs_User, 1.5)

    pcbnew.SaveBoard(os.path.join(out, NAME + ".kicad_pcb"), b)
    return b, fps


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "B", "kicad")
    os.makedirs(out, exist_ok=True)
    b, fps = build(out)
    for ref in ("U1", "ENC1", "J2", "SW_PWR", "J1", "SW_RST", "SW1", "D1"):
        fp = fps[ref]
        print(ref, "side", "B" if fp.IsFlipped() else "T", "rot", fp.GetOrientationDegrees(),
              {k: tuple(round(v, 2) for v in xy) for k, xy in list(pad_xy(fp).items())[:5]},
              "box", tuple(round(v, 2) for v in fab_box(fp)))
