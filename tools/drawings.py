#!/usr/bin/env python3
"""Draw the comparison-page SVGs from build.py's output.

    python tools/drawings.py

Writes build/top_<c>.svg (plan view) and build/section_<c>_keys.svg / _mcu.svg
(cross-sections cut through the real meshes). All drawings of one kind share a
viewBox, so they compare at the same scale. Colours are CSS classes the page styles.
"""
import json
import math
import os

import trimesh

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get("MACROPAD_OUT", ROOT)
BUILD = os.path.join(OUT, "build")

SECTION_ORDER = ["bottom", "battery", "pcb", "sockets", "switches", "keycaps", "display", "clamp",
                 "encoder", "mcu", "power_switch", "knob", "top"]
BASE_Y = 144.0   # plan view: front edge of every concept sits on this line
PLAN_W = 104.0   # plan view: concepts are centred in this width


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def rrect(x, y, w, h, r, cls):
    return f'<rect class="{cls}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(r)}"/>'


def dim_h(x0, x1, y, text):
    t = 1.6
    return (f'<g class="dim"><line x1="{f(x0)}" y1="{f(y)}" x2="{f(x1)}" y2="{f(y)}"/>'
            f'<line x1="{f(x0)}" y1="{f(y - t)}" x2="{f(x0)}" y2="{f(y + t)}"/>'
            f'<line x1="{f(x1)}" y1="{f(y - t)}" x2="{f(x1)}" y2="{f(y + t)}"/>'
            f'<text x="{f((x0 + x1) / 2)}" y="{f(y - 1.4)}" text-anchor="middle">{text}</text></g>')


def dim_v(x, y0, y1, text, side=-1, rotate=False):
    t = 1.6
    tx = x + side * 1.6
    anchor = "end" if side < 0 else "start"
    ym = (y0 + y1) / 2
    label = (f'<text x="{f(x - 1.4)}" y="{f(ym)}" text-anchor="middle" transform="rotate(-90 {f(x - 1.4)} {f(ym)})">{text}</text>'
             if rotate else f'<text x="{f(tx)}" y="{f(ym + 1.2)}" text-anchor="{anchor}">{text}</text>')
    return (f'<g class="dim"><line x1="{f(x)}" y1="{f(y0)}" x2="{f(x)}" y2="{f(y1)}"/>'
            f'<line x1="{f(x - t)}" y1="{f(y0)}" x2="{f(x + t)}" y2="{f(y0)}"/>'
            f'<line x1="{f(x - t)}" y1="{f(y1)}" x2="{f(x + t)}" y2="{f(y1)}"/>' + label + '</g>')


def plan(r):
    W, L = r["W"], r["L"]
    ox = (PLAN_W - W) / 2
    oy = BASE_Y - L
    X = lambda x: ox + x
    Y = lambda y: oy + (L - y)          # plate y (toward the back) points up the drawing
    s = [rrect(X(0), Y(L), W, L, r["corner_r"], "case")]
    s.append(rrect(X(1), Y(L - 1), W - 2, L - 2, r["corner_r"] - 1, "case-edge"))
    # screen
    ac = [r["disp_c"][0] + r["active_off"][0], r["disp_c"][1] + r["active_off"][1]]
    if r["disp_type"] == "round":
        rad = r["active"] / 2 + 0.4
        s.append(f'<circle class="bezel" cx="{f(X(ac[0]))}" cy="{f(Y(ac[1]))}" r="{f(rad + 1)}"/>')
        s.append(f'<circle class="screen" cx="{f(X(ac[0]))}" cy="{f(Y(ac[1]))}" r="{f(rad)}"/>')
        s.append(f'<circle class="screen-ui" cx="{f(X(ac[0]))}" cy="{f(Y(ac[1]))}" r="{f(rad - 3)}"/>')
    else:
        aw, ah = r["active"][0] + 0.8, r["active"][1] + 0.8
        s.append(rrect(X(ac[0] - aw / 2 - 1), Y(ac[1] + ah / 2 + 1), aw + 2, ah + 2, 1.6, "bezel"))
        s.append(rrect(X(ac[0] - aw / 2), Y(ac[1] + ah / 2), aw, ah, 0.6, "screen"))
        # tile grid that mirrors the keys (80 px tiles)
        px = r["px"]
        cols, rows = px[0] // 80, (px[1] - px[1] % 80) // 80
        tw, th = r["active"][0] / (px[0] / 80), r["active"][1] / (px[1] / 80)
        x0 = ac[0] - r["active"][0] / 2
        ytop = ac[1] + r["active"][1] / 2 - (px[1] % 80) / px[1] * r["active"][1]
        for i in range(cols):
            for j in range(rows):
                s.append(rrect(X(x0 + i * tw + 0.6), Y(ytop - j * th - 0.6), tw - 1.2, th - 1.2, 0.8, "tile"))
    # keys
    for kx, ky in r["keys_xy"]:
        s.append(rrect(X(kx - 9), Y(ky + 9), 18, 18, 2, "cap"))
        s.append(rrect(X(kx - 7.25), Y(ky + 7.25), 14.5, 14.5, 2.4, "cap-top"))
    # knob
    ex, ey = r["enc"]
    s.append(f'<circle class="knob" cx="{f(X(ex))}" cy="{f(Y(ey))}" r="{f(r["knob_d"] / 2)}"/>')
    s.append(f'<circle class="knob-top" cx="{f(X(ex))}" cy="{f(Y(ey))}" r="{f(r["knob_d"] / 2 - 1.5)}"/>')
    s.append(f'<circle class="knob-dot" cx="{f(X(ex))}" cy="{f(Y(ey + r["knob_d"] / 2 - 4))}" r="0.8"/>')
    # USB-C at the back edge
    mx = r["mcu_c"][0]
    s.append(rrect(X(mx - 4.5), Y(L) - 1.6, 9, 3.2, 1.4, "usb"))
    s.append(f'<text class="note" x="{f(X(mx))}" y="{f(Y(L) - 3)}" text-anchor="middle">USB-C</text>')
    # dimensions
    s.append(dim_h(X(0), X(W), BASE_Y + 7, f'{f(round(W, 1))}'))
    s.append(dim_v(X(0) - 5, Y(L), Y(0), f'{f(round(L, 1))}', rotate=True))
    return (f'<svg class="plan" viewBox="-14 -4 {f(PLAN_W + 28)} {f(BASE_Y + 16)}" role="img" '
            f'aria-label="Plan view of concept {r["concept"]}, {f(round(W, 1))} by {f(round(L, 1))} mm">'
            + "".join(s) + "</svg>")


def section(concept, r, x, label):
    view = os.path.join(OUT, "stl", concept, "view")
    s = ['<line class="desk" x1="-6" y1="0" x2="150" y2="0"/>']
    for part in SECTION_ORDER:
        mesh = trimesh.load(os.path.join(view, f"{part}.stl"), force="mesh")
        sec = mesh.section(plane_origin=[x, 0, 0], plane_normal=[1, 0, 0])
        if sec is None:
            continue
        d = ""
        for loop in sec.discrete:
            pts = [(p[1], -p[2]) for p in loop]
            d += "M" + " L".join(f"{f(a)},{f(b)}" for a, b in pts) + "Z"
        s.append(f'<path class="s-{part}" fill-rule="evenodd" d="{d}"/>')
    t = math.radians(r["tilt"])
    depth = r["L"] * math.cos(t)
    s.append(dim_v(-3, -r["front_h"], 0, f'{f(round(r["front_h"], 1))}'))
    s.append(dim_v(depth + 5, -r["rear_h"], 0, f'{f(round(r["rear_h"], 1))}', side=1))
    s.append(f'<text class="note" x="0" y="6.2">{label}</text>')
    return ('<svg class="section" viewBox="-16 -50 176 58" role="img" '
            f'aria-label="Cross-section of concept {concept} at {label}">' + "".join(s) + "</svg>")


def nearest_key_column(r):
    xs = sorted({k[0] for k in r["keys_xy"]})
    return min(xs, key=lambda c: (abs(c - r["disp_c"][0]), -c))


if __name__ == "__main__":
    for c in "ABC":
        r = json.load(open(os.path.join(BUILD, f"report_{c}.json")))
        open(os.path.join(BUILD, f"top_{c}.svg"), "w").write(plan(r))
        kx = nearest_key_column(r)
        open(os.path.join(BUILD, f"section_{c}_keys.svg"), "w").write(
            section(c, r, kx, f"x = {f(round(kx, 1))} · keys, screen, battery"))
        open(os.path.join(BUILD, f"section_{c}_mcu.svg"), "w").write(
            section(c, r, r["mcu_c"][0], f"x = {f(round(r['mcu_c'][0], 1))} · knob, controller, USB-C"))
        print(c, "drawings written")
