#!/usr/bin/env python3
"""Build every macropad concept: STLs, PCB outline DXF, report JSON and a fit check.

Needs OpenSCAD 2021.01+ on PATH, plus `pip install trimesh manifold3d numpy`.

    python tools/build.py            # all concepts
    python tools/build.py A C        # just A and C

Outputs (next to this folder):
    stl/<concept>/print/   top.stl bottom.stl knob.stl clamp.stl, oriented for the bed
    stl/<concept>/view/    every part and dummy component in the assembled position
    dxf/pcb_outline_<concept>.dxf
    build/report_<concept>.json   dimensions and positions used by the comparison page
    stl/test_coupon.stl           print this first to tune switch and insert holes
    build/fitcheck.txt            overlaps between parts (should say OK)
    build/viewer_<concept>.glb    coloured assembly for the 3D viewer (also opens in Windows 3D Viewer)
"""
import concurrent.futures as cf
import json
import os
import re
import subprocess
import sys

import manifold3d as m3d
import numpy as np
import trimesh

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAD = os.path.join(ROOT, "scad", "macropad.scad")
OUT = os.environ.get("MACROPAD_OUT", ROOT)

VIEW_PARTS = ["top", "bottom", "knob", "clamp", "pcb", "sockets", "switches", "switch_bodies",
              "keycaps", "encoder", "display", "mcu", "battery", "power_switch"]
PRINT_PARTS = {"top": "top_print", "bottom": "bottom_print", "knob": "knob_print", "clamp": "clamp_print"}

VIEW_COLOURS = {"top": "#e4e1da", "bottom": "#5b636d", "knob": "#0b6e74", "clamp": "#4a525b",
                "pcb": "#1f6f43", "sockets": "#2b2b2b", "switches": "#3a3f45", "keycaps": "#f4f3ef",
                "encoder": "#a8adb3", "display": "#101418", "mcu": "#24477a", "battery": "#b9c3cc",
                "power_switch": "#d0d0d0"}

# Pairs that must not overlap. Parts that touch by design are modelled with small gaps.
CHECKS = [
    ("top", ["pcb", "sockets", "switch_bodies", "encoder", "display", "clamp", "mcu", "battery",
             "power_switch", "knob", "keycaps"]),
    ("bottom", ["pcb", "sockets", "encoder", "display", "clamp", "mcu", "battery", "power_switch"]),
    ("battery", ["pcb", "sockets", "mcu", "clamp", "display", "power_switch"]),
    ("mcu", ["clamp", "display", "sockets", "power_switch", "pcb"]),
    ("clamp", ["pcb", "sockets", "encoder"]),
    ("pcb", ["display", "encoder", "switch_bodies", "sockets", "power_switch"]),
    ("knob", ["keycaps"]),
]


def scad(concept, part, out):
    cmd = ["openscad", "-D", f'concept="{concept}"', "-D", f'part="{part}"', "-o", out, SCAD]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or "ERROR" in r.stderr:
        raise RuntimeError(f"{concept}/{part}: {r.stderr[-2000:]}")
    return r.stderr


def to_manifold(path):
    mesh = trimesh.load(path, force="mesh")
    mesh.merge_vertices()
    return m3d.Manifold(m3d.Mesh(vert_properties=np.asarray(mesh.vertices, dtype=np.float32),
                                 tri_verts=np.asarray(mesh.faces, dtype=np.uint32)))


def build(concept):
    view = os.path.join(OUT, "stl", concept, "view")
    prn = os.path.join(OUT, "stl", concept, "print")
    for d in (view, prn, os.path.join(OUT, "dxf"), os.path.join(OUT, "build")):
        os.makedirs(d, exist_ok=True)

    jobs = [(p, os.path.join(view, f"{p}.stl")) for p in VIEW_PARTS]
    jobs += [(pp, os.path.join(prn, f"{p}.stl")) for p, pp in PRINT_PARTS.items()]
    jobs += [("pcb_outline", os.path.join(OUT, "dxf", f"pcb_outline_{concept}.dxf"))]
    with cf.ThreadPoolExecutor(max_workers=os.cpu_count() or 2) as ex:
        list(ex.map(lambda j: scad(concept, *j), jobs))

    echo = os.path.join(OUT, "build", f"report_{concept}.echo")
    scad(concept, "report", echo)
    text = open(echo).read()
    os.remove(echo)
    report = json.loads(re.search(r'REPORT (\{.*\})"', text).group(1).replace('\\"', '"'))

    # fit check
    solids = {p: to_manifold(os.path.join(view, f"{p}.stl")) for p in VIEW_PARTS}
    clashes = []
    for a, others in CHECKS:
        for b in others:
            v = (solids[a] ^ solids[b]).volume()
            if v > 0.01:
                clashes.append(f"{a} x {b}: {v:.2f} mm3")
    report["fitcheck"] = clashes

    # quick numbers for the page
    top = trimesh.load(os.path.join(prn, "top.stl"))
    report["print_bbox"] = {p: [round(float(x), 1) for x in trimesh.load(os.path.join(prn, f"{p}.stl")).extents]
                            for p in PRINT_PARTS}
    report["top_volume_cm3"] = round(float(top.volume) / 1000, 1)
    report["bottom_volume_cm3"] = round(float(trimesh.load(os.path.join(prn, "bottom.stl")).volume) / 1000, 1)
    with open(os.path.join(OUT, "build", f"report_{concept}.json"), "w") as f:
        json.dump(report, f, indent=1)

    # one coloured GLB per concept, a node per part
    scene = trimesh.Scene()
    for p, colour in VIEW_COLOURS.items():
        mesh = trimesh.load(os.path.join(view, f"{p}.stl"), force="mesh")
        rgba = [int(colour[i:i + 2], 16) / 255 for i in (1, 3, 5)] + [1.0]
        mesh.visual = trimesh.visual.TextureVisuals(
            material=trimesh.visual.material.PBRMaterial(name=p, baseColorFactor=rgba,
                                                         metallicFactor=0.0, roughnessFactor=0.7))
        scene.add_geometry(mesh, node_name=p, geom_name=p)
    scene.export(os.path.join(OUT, "build", f"viewer_{concept}.glb"))
    return concept, clashes


if __name__ == "__main__":
    concepts = sys.argv[1:] or ["A", "B", "C"]
    os.makedirs(os.path.join(OUT, "stl"), exist_ok=True)
    scad("A", "test_coupon", os.path.join(OUT, "stl", "test_coupon.stl"))
    lines = []
    for c, clashes in map(build, concepts):
        lines.append(f"{c}: " + ("OK" if not clashes else "; ".join(clashes)))
        print(lines[-1])
    with open(os.path.join(OUT, "build", "fitcheck.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
