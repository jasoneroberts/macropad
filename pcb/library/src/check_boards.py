#!/usr/bin/env /usr/bin/python3
"""Checks that every footprint on a board is geometrically identical to its JR library footprint.

    /usr/bin/python3 pcb/library/src/check_boards.py [board.kicad_pcb ...]

With no arguments it checks the macropad (pcb/B/kicad) and, if present, the Gameball carrier
(/mnt/project-files/pcb/kicad). "Identical" means the same pad numbers, positions, sizes, shapes, drills and layer
sets, measured in the footprint's own frame (orientation and side taken out), so a part that is rotated or on the
bottom layer on the board still compares equal. Run it after editing a footprint here, and before relinking an
Altium design to the JR library, to see which boards would change.
"""
import os
import sys

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(os.path.dirname(HERE), "JR.pretty")
DEFAULT_BOARDS = [os.path.join(HERE, "..", "..", "B", "kicad", "macropad_B.kicad_pcb"),
                  "/mnt/project-files/pcb/kicad/gameball-carrier.kicad_pcb"]
MM = pcbnew.FromMM(1)
TOL = 0.005   # mm


FLIP_LEFT_RIGHT = True   # see pads_of


def pads_of(fp):
    """Pads in the footprint's own frame: KiCad undoes the side flip and the orientation itself."""
    d = fp.Duplicate()
    if d.IsFlipped():
        d.Flip(d.GetPosition(), FLIP_LEFT_RIGHT)
    d.SetOrientationDegrees(0)
    pos = d.GetPosition()
    out = []
    for p in d.Pads():
        sz = p.GetSize()
        dr = p.GetDrillSize()
        out.append((p.GetNumber(), round((p.GetPosition().x - pos.x) / MM, 3), round((p.GetPosition().y - pos.y) / MM, 3),
                    round(sz.x / MM, 3), round(sz.y / MM, 3), round(dr.x / MM, 3), round(dr.y / MM, 3),
                    p.GetShape(), int(p.GetAttribute())))
    return sorted(out, key=lambda r: (r[0], r[1], r[2]))


def libfp(name, cache={}):
    if name not in cache:
        cache[name] = pcbnew.FootprintLoad(LIB, name)
    return cache[name]


def same(a, b):
    if len(a) != len(b):
        return False, f"{len(a)} pads on the board, {len(b)} in JR"
    bad = []
    for ra, rb in zip(a, b):
        if ra[0] != rb[0] or any(abs(ra[i] - rb[i]) > TOL for i in range(1, 7)) or ra[7:] != rb[7:]:
            bad.append(f"pad {ra[0]}: board {ra[1:7]} vs JR {rb[1:7]}")
    return not bad, "; ".join(bad[:4])


def check(path):
    b = pcbnew.LoadBoard(path)
    seen = {}
    print(f"\n{os.path.basename(path)}: {len(b.GetFootprints())} footprints")
    problems = 0
    for fp in sorted(b.GetFootprints(), key=lambda f: f.GetReference()):
        name = str(fp.GetFPID().GetLibItemName())
        ref = fp.GetReference()
        if name.startswith("MountingHole") and not os.path.exists(os.path.join(LIB, name + ".kicad_mod")):
            name = "MountingHole_2.2mm_M2"
        if not os.path.exists(os.path.join(LIB, name + ".kicad_mod")):
            print(f"  {ref:8s} {name}: NOT IN JR")
            problems += 1
            continue
        ok, why = same(pads_of(fp), pads_of(libfp(name)))
        seen.setdefault(name, []).append((ref, ok, why))
    for name, lst in sorted(seen.items()):
        bad = [(r, w) for r, ok, w in lst if not ok]
        refs = ",".join(r for r, _, _ in lst)
        if bad:
            problems += len(bad)
            print(f"  DIFFERS  {name}  ({refs})")
            for r, w in bad[:2]:
                print(f"           {r}: {w}")
        else:
            print(f"  same     {name}  ({refs})")
    return problems


if __name__ == "__main__":
    boards = sys.argv[1:] or [p for p in DEFAULT_BOARDS if os.path.exists(p)]
    total = sum(check(p) for p in boards)
    print("\nall footprints match JR" if not total else f"\n{total} footprint(s) differ from JR")
    sys.exit(1 if total else 0)
