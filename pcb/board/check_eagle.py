#!/usr/bin/env python3
"""Checks the EAGLE hand-off files on their own, the way Altium will read them.

    python3 pcb/board/check_eagle.py <dir with macropad_B.sch and macropad_B.brd>

Schematic: every <pinref> must sit on an end of a wire in its own segment (Altium joins by geometry, not by the
pinref list), no wire end may touch a pin of another net; pins in no net are listed so they can be checked by eye.
Board vs schematic: the nets built from <connect> (gate pin -> package pad) must equal the board's contactrefs,
which is what Altium's "Update PCB" compares after the import.
"""
import math
import os
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

D = sys.argv[1]
sch = ET.parse(os.path.join(D, "macropad_B.sch")).getroot()
brd = ET.parse(os.path.join(D, "macropad_B.brd")).getroot()
R = lambda v: round(float(v), 3)


def rot(rs):
    m = rs.startswith("M")
    return m, float(rs.lstrip("MSR") or 0)


def xform(x, y, rs):
    m, ang = rot(rs or "R0")
    a = math.radians(ang)
    x, y = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
    return (-x, y) if m else (x, y)


lib = sch.find("drawing/schematic/libraries/library")
symbols = {s.get("name"): {p.get("name"): (float(p.get("x")), float(p.get("y"))) for p in s.findall("pin")}
           for s in lib.findall("symbols/symbol")}
devsets = {}
for ds in lib.findall("devicesets/deviceset"):
    g = ds.find("gates/gate")
    dev = ds.find("devices/device")
    devsets[ds.get("name")] = (g.get("symbol"), {c.get("pin"): c.get("pad") for c in dev.findall("connects/connect")})
parts = {p.get("name"): p.get("deviceset") for p in sch.findall("drawing/schematic/parts/part")}
sheet = sch.find("drawing/schematic/sheets/sheet")
pinpos = {}
for inst in sheet.findall("instances/instance"):
    ref = inst.get("part")
    sym, _ = devsets[parts[ref]]
    for pin, (px, py) in symbols[sym].items():
        dx, dy = xform(px, py, inst.get("rot"))
        pinpos[(ref, pin)] = (R(float(inst.get("x")) + dx), R(float(inst.get("y")) + dy))

errors = []
sch_nets = {}
all_ends = defaultdict(set)          # point -> nets with a wire end there
seg_ends = []
for net in sheet.findall("nets/net"):
    name = net.get("name")
    members = set()
    for seg in net.findall("segment"):
        ends = set()
        for w in seg.findall("wire"):
            for k in ("1", "2"):
                pt = (R(w.get("x" + k)), R(w.get("y" + k)))
                ends.add(pt); all_ends[pt].add(name)
        for pr in seg.findall("pinref"):
            key = (pr.get("part"), pr.get("pin"))
            if pinpos[key] not in ends:
                errors.append(f"{name}: pin {key} at {pinpos[key]} is not on a wire end of its segment")
            pad = devsets[parts[key[0]]][1][key[1]]
            for p in pad.split():
                members.add((key[0], p))
        seg_ends.append((name, ends))
    sch_nets[name] = members
for key, pt in pinpos.items():
    other = all_ends.get(pt, set())
    mine = {n for n, m in sch_nets.items() if (key[0], devsets[parts[key[0]]][1][key[1]].split()[0]) in m}
    if other - mine:
        errors.append(f"pin {key} at {pt} touches a wire of {sorted(other - mine)}")

brd_nets = defaultdict(set)
for s in brd.findall("drawing/board/signals/signal"):
    for c in s.findall("contactref"):
        brd_nets[s.get("name")].add((c.get("element"), c.get("pad")))
for n in sorted(set(sch_nets) | set(brd_nets)):
    if sch_nets.get(n, set()) != brd_nets.get(n, set()):
        errors.append(f"net {n}: schematic-only {sorted(sch_nets.get(n, set()) - brd_nets.get(n, set()))}, "
                      f"board-only {sorted(brd_nets.get(n, set()) - sch_nets.get(n, set()))}")
brd_parts = {e.get("name") for e in brd.findall("drawing/board/elements/element")}
if brd_parts != set(parts):
    errors.append(f"parts differ: sch-only {sorted(set(parts) - brd_parts)}, brd-only {sorted(brd_parts - set(parts))}")
in_net = {(r, p) for m in sch_nets.values() for r, p in m}
loose = sorted(k for k in pinpos if (k[0], devsets[parts[k[0]]][1][k[1]].split()[0]) not in in_net)
print("pins in no net:", ", ".join(f"{r}.{p}" for r, p in loose) or "none")
for e in errors:
    print("ERROR", e)
print(f"{len(parts)} parts, {len(sch_nets)} nets, {len(pinpos)} pins: " + ("OK" if not errors else f"{len(errors)} errors"))
sys.exit(1 if errors else 0)
