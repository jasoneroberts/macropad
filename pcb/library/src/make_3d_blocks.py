#!/usr/bin/env python3
"""Plain block STEP models for the two module footprints that have no maker model (SuperMini, XIAO).

Frame: footprint origin = STEP origin, z = 0 at the board surface, +z = away from the board, STEP y = -(KiCad y)
(the KiCad .kicad_mod is y-down, Altium and STEP are y-up). Sizes come from the F.Fab outline of each footprint.
Needs: pip install cadquery.  Usage: python3 make_3d_blocks.py [out_dir]
"""
import sys, os
import cadquery as cq

def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def supermini():
    # F.Fab x -9.05..9.05, KiCad y -17.65..16.55  ->  STEP y -16.55..17.65 (USB-C at the +y end)
    x0, x1, y0, y1 = -9.05, 9.05, -16.55, 17.65
    s = box(x0, x1, y0, y1, 2.5, 3.5)                          # module PCB on 2.5 mm headers
    for hx in (-7.62, 7.62):                                   # header strips under the PCB, on the pad rows
        s = s.union(box(hx - 1.27, hx + 1.27, -13.97 - 1.27, 13.97 + 1.27, 0, 2.5))
    s = s.union(box(-4.5, 4.5, y1 - 5.5, y1 + 0.0, 3.5, 6.8))  # USB-C shell, flush with the edge, 3.3 mm tall
    return s

def xiao():
    # F.Fab x -8.94..8.94, KiCad y -11.85..10.55  ->  STEP y -10.55..11.85; about 3.5 mm over the pads
    return box(-8.94, 8.94, -10.55, 11.85, 0, 3.5)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "3d")
    os.makedirs(out, exist_ok=True)
    for name, fn in (("SuperMini_nRF52840", supermini), ("XIAO_nRF52840_SMD", xiao)):
        cq.exporters.export(fn(), os.path.join(out, name + ".step"))
        print("wrote", name + ".step")
