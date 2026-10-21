#!/usr/bin/env python3
"""Assemble the comparison page from page_template.html and the build outputs.

    python tools/make_page.py <out_dir>

Writes <out_dir>/index.html and <out_dir>/models/viewer_<c>.glb.
Run build.py and drawings.py first.
"""
import base64
import datetime
import json
import math
import os
import shutil
import struct
import sys

import trimesh

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.environ.get("MACROPAD_OUT", ROOT)
BUILD = os.path.join(OUT, "build")
sys.path.insert(0, HERE)
from build import VIEW_COLOURS  # noqa: E402

TEXT = {
    "A": dict(sub="3 × 3 keys · 1.69″ LCD · knob",
              screen="1.69″ 240 × 280 IPS, portrait: a header row and 3 × 3 tiles of 80 px, one per key",
              battery="603040 LiPo, about 700–800 mAh",
              good="the cheapest and quickest build, and the smallest case. A good first print to learn the fit.",
              watch="9 keys fill up fast, and the 26 mm knob is the smallest of the three."),
    "B": dict(sub="4 × 3 keys · 2.0″ LCD · knob",
              screen="2.0″ 320 × 240 IPS, landscape: exactly 4 × 3 tiles of 80 px, laid out like the keys",
              battery="603040 LiPo, about 700–800 mAh",
              good="a Stream Deck-style layout, where every key's label sits on the screen in the same spot as the key.",
              watch="the 2.0″ module's board is 58 mm long, so the knob moves right and the case is 101 mm wide."),
    "C": dict(sub="4 × 4 keys · 1.28″ round LCD · big knob",
              screen="1.28″ 240 × 240 round IPS: knob state (volume ring, mode, battery)",
              battery="803040 LiPo, about 1000 mAh (the deeper case has room)",
              good="the most keys and a 36 mm knob that's nice to turn. The longest battery life.",
              watch="the round screen is too small for 16 labels, so use relegendable keycaps. It's the longest and tallest case."),
}


def f1(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def sheet(c, r):
    t = TEXT[c]
    name = r["name"].split(" - ")[1]
    pick = c == "B"
    pb = r["print_bbox"]["top"]
    vols = sum(trimesh.load(os.path.join(OUT, "stl", c, "print", f"{p}.stl")).volume
               for p in ("top", "bottom", "knob", "clamp")) / 1000
    grams = round(vols * 1.24 / 5) * 5
    svg = lambda n: open(os.path.join(BUILD, n)).read()
    specs = [
        ("Keys", f"{r['keys']} MX hot-swap + knob Ø{r['knob_d']}"),
        ("On the desk", f"{f1(r['W'])} × {f1(r['depth_on_desk'])} mm"),
        ("Height", f"{f1(r['front_h'])} front · {f1(r['rear_h'])} rear (+2 with feet)"),
        ("Tilt", f"{r['tilt']}°"),
        ("Screen", t["screen"]),
        ("Battery", t["battery"]),
        ("Largest print", f"top shell {f1(pb[0])} × {f1(pb[1])} × {f1(pb[2])}"),
        ("Filament", f"under {grams} g even if printed solid"),
    ]
    dl = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in specs)
    return f"""    <article class="sheet{' pick' if pick else ''}" id="sheet-{c}">
      <div class="tb"><span class="letter">{c}</span><div class="nm"><b>{name}</b><span>{t['sub']}</span></div>{'<span class="badge">My pick</span>' if pick else '<span></span>'}</div>
      <div class="fig">{svg(f'top_{c}.svg')}<span class="figcap">PLAN · looking square onto the top surface</span></div>
      <div class="fig">{svg(f'section_{c}_keys.svg')}{svg(f'section_{c}_mcu.svg')}<span class="figcap">SECTIONS · front on the left</span></div>
      <dl class="specs">{dl}</dl>
      <div class="verdict"><p><b>Good for</b> {t['good']}</p><p><b>Watch:</b> {t['watch']}</p></div>
      <div class="act"><button class="btn" type="button" data-show="{c}">View {c} in 3D</button></div>
    </article>"""


def glb_to_gltf_json(path):
    """Unpack a binary glTF (.glb) into glTF JSON with its binary chunk as a data URI."""
    data = open(path, "rb").read()
    magic, _version, _length = struct.unpack_from("<4sII", data, 0)
    assert magic == b"glTF"
    off, gltf, binary = 12, None, b""
    while off < len(data):
        size, kind = struct.unpack_from("<I4s", data, off)
        chunk = data[off + 8: off + 8 + size]
        if kind == b"JSON":
            gltf = json.loads(chunk)
        elif kind == b"BIN\x00":
            binary = chunk
        off += 8 + size
    gltf["buffers"][0]["uri"] = "data:application/octet-stream;base64," + base64.b64encode(binary).decode()
    return gltf


def stack_svg(rB):
    """Layer stack under a key (left) and under the screen (right), to scale, drawn flat."""
    t = math.radians(rB["tilt"])
    # clearance between the display clamp and the battery at the screen's front edge, concept B
    y_front = rB["disp_c"][1] - 17.5
    clamp_bot = rB["front_h"] + y_front * math.sin(t) - 6.6 * math.cos(t)
    bat_top = 2.4 + 0.05 + rB["lipo"][0]
    gap_screen = clamp_bot - bat_top
    s = []

    def box(x, z0, z1, w, cls, rx=0.3):
        s.append(f'<rect class="{cls}" x="{x - w / 2:.2f}" y="{-z1:.2f}" width="{w:.2f}" height="{z1 - z0:.2f}" rx="{rx}"/>')

    pending = []

    def dim(x, z0, z1, label, text_x):
        s.append(f'<path class="dimv" d="M{x},{-z0:.2f} V{-z1:.2f} M{x - 1},{-z0:.2f} H{x + 1} M{x - 1},{-z1:.2f} H{x + 1}"/>')
        pending.append((x, (z0 + z1) / 2, label, text_x))

    def place_labels(gap=3.6):
        """Spread labels so thin layers don't overprint, with leaders back to each layer."""
        items = sorted(pending, key=lambda p: -p[1])           # top to bottom
        ys = [-p[1] for p in items]
        for i in range(1, len(ys)):
            ys[i] = max(ys[i], ys[i - 1] + gap)
        shift = (sum(-p[1] for p in items) - sum(ys)) / len(ys)  # recentre the column on the layers
        ys = [y + shift for y in ys]
        for (x, zm, label, tx), y in zip(items, ys):
            s.append(f'<path class="dimv" d="M{x + 1},{-zm:.2f} H{x + 2.5} L{tx - 2},{y:.2f} H{tx - 0.8}" stroke-dasharray="0.6 0.5"/>')
            s.append(f'<text x="{tx}" y="{y + 0.9:.2f}">{label}</text>')
        pending.clear()

    # left column: one key at the front row (plate frame, z = 0 is the plate top)
    floor_top = -8.45 - 2.0
    box(0, floor_top - 2.4, floor_top, 40, "s-bottom", 0)
    box(0, -6.6, -5.0, 40, "s-pcb", 0)
    box(-1.0, -8.45, -6.6, 14.0, "s-sockets", 0.2)
    box(0, -5.0, 0, 13.9, "s-switches", 0.2)
    s.append('<path class="s-switches" d="M-7.8,0 L-5.5,-5.4 L5.5,-5.4 L7.8,0 Z"/>')
    box(0, 5.4, 11.6, 1.2, "s-switches", 0)
    s.append('<path class="s-keycaps" d="M-9,-7 L-7.25,-16 L7.25,-16 L9,-7 Z"/>')
    for sx in (-1, 1):   # skin: 1.5 mm lip to the 14 mm hole, ribs stop at the 15 mm pocket
        s.append(f'<path class="s-top" d="M{sx * 7.0},0 H{sx * 20} V3 H{sx * 7.5} V1.5 H{sx * 7.0} Z"/>')
    dim(24, -1.5, 0, "lip 1.5 · 14.0 hole", 30)
    dim(24, -3.0, -1.5, "rib 1.5 · 15.0 pocket", 30)
    dim(24, -5.0, -3.0, "gap 2.0", 30)
    dim(24, -6.6, -5.0, "PCB 1.6", 30)
    dim(24, -8.45, -6.6, "socket 1.85", 30)
    dim(24, floor_top, -8.45, "≥ 2.0 at the front row", 30)
    dim(24, floor_top - 2.4, floor_top, "bottom plate 2.4", 30)
    place_labels()
    s.append('<text class="lbl" x="-20" y="-20">UNDER A FRONT KEY</text>')
    s.append('<text class="lbl" x="-20" y="23.5">plate top to PCB top = 5.0 (MX standard)</text>')

    # right column: under the screen at its front edge, concept B
    ox = 92
    floor2 = -(6.6 + gap_screen + rB["lipo"][0] + 0.05)
    box(ox, floor2 - 2.4, floor2, 40, "s-bottom", 0)
    box(ox, floor2 + 0.05, floor2 + 0.05 + rB["lipo"][0], 34, "s-battery", 0.8)
    box(ox, -6.6, -4.6, 30, "s-clamp", 0)
    box(ox, -4.6, -3.0, 34, "s-pcb", 0)
    box(ox, -3.0, -1.0, 32, "s-display", 0)
    for sx in (-1, 1):   # bezel with a 45 degree chamfer, glass pocket below it
        s.append(f'<path class="s-top" d="M{ox + sx * 15.6},0 H{ox + sx * 20} V3 H{ox + sx * 16.25} V1 H{ox + sx * 14.6} Z"/>')
    dim(ox + 24, -1.0, 0, "bezel 1.0 (45° chamfer)", ox + 30)
    dim(ox + 24, -3.0, -1.0, "glass 2.0 in a pocket", ox + 30)
    dim(ox + 24, -4.6, -3.0, "module board 1.6", ox + 30)
    dim(ox + 24, -6.6, -4.6, "printed clamp 2.0", ox + 30)
    dim(ox + 24, floor2 + 0.05 + rB["lipo"][0], -6.6, f"air {gap_screen:.1f}", ox + 30)
    dim(ox + 24, floor2, floor2 + rB["lipo"][0] + 0.05, f"LiPo {rB['lipo'][0]:.0f}", ox + 30)
    dim(ox + 24, floor2 - 2.4, floor2, "bottom plate 2.4", ox + 30)
    place_labels()
    s.append(f'<text class="lbl" x="{ox - 20}" y="-20">UNDER THE SCREEN (B, FRONT EDGE)</text>')
    s.append(f'<text class="lbl" x="{ox - 20}" y="23.5">the tilt adds height toward the back</text>')
    top = 24
    bottom = 26
    return (f'<svg viewBox="-22 -{top} 200 {top + bottom:.1f}" aria-hidden="true">' + "".join(s) + "</svg>")


if __name__ == "__main__":
    dest = sys.argv[1]
    os.makedirs(os.path.join(dest, "models"), exist_ok=True)
    reports = {c: json.load(open(os.path.join(BUILD, f"report_{c}.json"))) for c in "ABC"}
    for c in "ABC":   # artifacts don't serve .glb, so ship each model as glTF JSON with the buffer inlined
        with open(os.path.join(dest, "models", f"viewer_{c}.json"), "w") as fh:
            json.dump(glb_to_gltf_json(os.path.join(BUILD, f"viewer_{c}.glb")), fh, separators=(",", ":"))
    pcb_svg = os.path.join(os.path.dirname(BUILD), "pcb", "B", "placement.svg")   # from pcb/generate.py
    if os.path.exists(pcb_svg):
        shutil.copyfile(pcb_svg, os.path.join(dest, "models", "pcb_B.svg"))
    keep = ["concept", "name", "cols", "rows", "tilt", "W", "L", "depth_on_desk", "front_h", "rear_h", "disp_type",
            "disp_c", "active", "active_off", "px", "bezel_t"]
    data = {"colours": VIEW_COLOURS, "reports": {c: {k: r[k] for k in keep} for c, r in reports.items()}}
    pbC = reports["C"]["print_bbox"]["top"]
    page = open(os.path.join(HERE, "page_template.html")).read()
    page = (page.replace("{{SHEETS}}", "\n".join(sheet(c, reports[c]) for c in "ABC"))
                .replace("{{STACK}}", stack_svg(reports["B"]))
                .replace("{{DATA}}", json.dumps(data))
                .replace("{{LARGEST}}", f"{f1(pbC[0])} × {f1(pbC[1])} mm")
                .replace("{{DATE}}", datetime.date.today().isoformat()))
    open(os.path.join(dest, "index.html"), "w").write(page)
    print("page written:", os.path.join(dest, "index.html"))
