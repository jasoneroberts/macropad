#!/usr/bin/env python3
"""Draws the board as a PNG/PDF for review: outline, pads, tracks (red = top, blue = bottom), vias, holes, refs.

    /usr/bin/python3 pcb/board/render.py <board.kicad_pcb> <out.png|out.pdf> [--pours] [--nets]
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Polygon  # noqa: E402
import pcbnew  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_board as BB  # noqa: E402


def render(path, out, pours=False, nets=False, title=None):
    b = pcbnew.LoadBoard(path)
    if pours:
        pcbnew.ZONE_FILLER(b).Fill(b.Zones())
    fig, ax = plt.subplots(figsize=(11, 12.5))
    ax.set_aspect("equal")
    P = BB.P
    mm = pcbnew.ToMM
    # outline
    for d in b.GetDrawings():
        if d.GetLayer() != pcbnew.Edge_Cuts:
            continue
        if d.GetShape() == pcbnew.SHAPE_T_SEGMENT:
            (x0, y0), (x1, y1) = P(d.GetStart()), P(d.GetEnd())
            ax.plot([x0, x1], [y0, y1], color="#2c6e49", lw=1.2)
        elif d.GetShape() == pcbnew.SHAPE_T_ARC:
            pts = [P(p) for p in d.GetCorners()] if False else None
            poly = d.GetPolyShape() if False else None
            s, m, e = P(d.GetStart()), P(d.GetArcMid()), P(d.GetEnd())
            import math
            ax_, ay = s; bx, by = m; cx, cy = e
            dd = 2 * (ax_ * (by - cy) + bx * (cy - ay) + cx * (ay - by))
            ux = ((ax_**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / dd
            uy = ((ax_**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax_ - cx) + (cx**2 + cy**2) * (bx - ax_)) / dd
            r = math.hypot(ax_ - ux, ay - uy)
            a0 = math.atan2(ay - uy, ax_ - ux); a1 = math.atan2(by - uy, bx - ux); a2 = math.atan2(cy - uy, cx - ux)
            sw = (a2 - a0) % (2 * math.pi)
            if (a1 - a0) % (2 * math.pi) > sw:
                sw -= 2 * math.pi
            xs = [ux + r * math.cos(a0 + sw * i / 30) for i in range(31)]
            ys = [uy + r * math.sin(a0 + sw * i / 30) for i in range(31)]
            ax.plot(xs, ys, color="#2c6e49", lw=1.2)
    if pours:
        for z in b.Zones():
            if z.GetIsRuleArea():
                continue
            for layer, col in ((pcbnew.B_Cu, "#9ec5ff"), (pcbnew.F_Cu, "#ffb3b3")):
                if not z.IsOnLayer(layer):
                    continue
                fp = z.GetFilledPolysList(layer)
                for i in range(fp.OutlineCount()):
                    o = fp.Outline(i)
                    pts = [P(o.CPoint(k)) for k in range(o.PointCount())]
                    ax.add_patch(Polygon(pts, closed=True, fc=col, ec="none", alpha=0.35, zorder=0))
    for t in b.GetTracks():
        if t.GetClass() == "PCB_VIA":
            x, y = P(t.GetPosition())
            ax.add_patch(Circle((x, y), mm(t.GetWidth()) / 2, fc="#555", ec="none", zorder=5))
            ax.add_patch(Circle((x, y), 0.15, fc="white", ec="none", zorder=6))
        else:
            (x0, y0), (x1, y1) = P(t.GetStart()), P(t.GetEnd())
            col = "#d62828" if t.GetLayer() == pcbnew.F_Cu else "#1d4ed8"
            ax.plot([x0, x1], [y0, y1], color=col, lw=mm(t.GetWidth()) * 4.2, solid_capstyle="round",
                    alpha=0.85, zorder=3 if t.GetLayer() == pcbnew.F_Cu else 2)
    for fp in b.GetFootprints():
        bottom = fp.IsFlipped()
        for p in fp.Pads():
            x, y = P(p.GetPosition())
            sx, sy = mm(p.GetBoundingBox().GetWidth()), mm(p.GetBoundingBox().GetHeight())
            if p.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH:
                ax.add_patch(Circle((x, y), mm(min(p.GetDrillSize().x, p.GetDrillSize().y)) / 2, fc="white",
                                    ec="#333", lw=0.6, zorder=7))
                continue
            col = "#c9a227" if p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH else ("#6c8ebf" if bottom else "#e07a5f")
            ax.add_patch(FancyBboxPatch((x - sx / 2, y - sy / 2), sx, sy, boxstyle="round,pad=0,rounding_size=0.2",
                                        fc=col, ec="none", zorder=4))
            if p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH:
                ax.add_patch(Circle((x, y), mm(p.GetDrillSize().x) / 2, fc="white", ec="none", zorder=4.5))
            if nets and p.GetNetname():
                ax.text(x, y, p.GetNetname(), fontsize=2.2, ha="center", va="center", zorder=8, color="#111")
        x, y = P(fp.GetPosition())
        ref = fp.GetReference()
        if not ref.startswith("H"):
            ax.text(x, y, ref, fontsize=4, ha="center", va="center", zorder=9,
                    color="#0b3d91" if bottom else "#7a1f1f", alpha=0.8)
    ax.set_xlim(-2, 103); ax.set_ylim(-2, 118)
    ax.set_title(title or "Concept B main board, top view (blue = bottom copper, red = top copper)", fontsize=10)
    ax.grid(True, lw=0.2, alpha=0.4)
    fig.tight_layout()
    fig.savefig(out, dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2], "--pours" in sys.argv, "--nets" in sys.argv)
