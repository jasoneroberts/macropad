#!/usr/bin/env python3
"""Routes the placed concept B board with Freerouting, then pours ground and runs KiCad's DRC.

    /usr/bin/python3 pcb/board/route.py <kicad dir> <freerouting.jar> [passes]

1. Pre-routes the six LCD signals (straight across from U1 pins 5-10 to J2 pins 3-8) and locks them.
2. Exports Specctra DSN without the ground pours (so Freerouting draws real ground tracks too), with two classes:
   signals 0.25 mm and power (GND, VBAT, VBAT_SW, 3V3_SW) 0.4 mm, 0.2 mm clearance, 0.6/0.3 mm vias.
3. Runs Freerouting headless, imports the session, puts the pours back, fills them, writes the DRC report.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pcbnew  # noqa: E402

import build_board as BB  # noqa: E402
import design_b as D  # noqa: E402
from ses_import import import_ses  # noqa: E402

KDIR, JAR = sys.argv[1], sys.argv[2]
PASSES = sys.argv[3] if len(sys.argv) > 3 else "100"
PCB = os.path.join(KDIR, BB.NAME + ".kicad_pcb")
DSN = os.path.join(KDIR, BB.NAME + ".dsn")
SES = os.path.join(KDIR, BB.NAME + ".ses")

b = pcbnew.LoadBoard(PCB)
fps = {fp.GetReference(): fp for fp in b.GetFootprints()}
nets = {n: b.FindNet(n) for n in D.NETS}


def track(a, c, net, layer=pcbnew.B_Cu, w=0.25, locked=True):
    t = pcbnew.PCB_TRACK(b)
    t.SetStart(BB.K(*a)); t.SetEnd(BB.K(*c)); t.SetWidth(BB.mm(w)); t.SetLayer(layer); t.SetNet(nets[net])
    t.SetLocked(locked)
    b.Add(t)


# 1. LCD signals, bottom layer, U1 pin k (x 89.62) -> J2 pin k-2 (x 93.8), same y
u = BB.pad_xy(fps["U1"]); j = BB.pad_xy(fps["J2"])
for upin, jpin in zip(range(5, 11), range(3, 9)):
    net = next(n for p, _, _, n in D.U1_PINS if p == upin)
    assert abs(u[str(upin)][1] - j[str(jpin)][1]) < 1e-3, (upin, jpin)
    track(u[str(upin)], j[str(jpin)], net)

# 2. DSN without pours (rule areas stay: they become keep-outs)
# pours, and rule areas that only forbid pours (KiCad's DSN export would turn them into full keep-outs)
pours = [z for z in b.Zones() if not z.GetIsRuleArea() or not z.GetDoNotAllowTracks()]
for z in pours:
    b.Remove(z)
pcbnew.ExportSpecctraDSN(b, DSN)
txt = open(DSN).read()
txt = txt.replace("(width 200)", "(width 250)").replace("(clearance 200.1)", "(clearance 200)")
m = re.search(r'\(class kicad_default "" (.*?)\n\s*\(circuit', txt, re.S)
members = m.group(1).split()
sig = [n for n in members if n not in D.POWER_NETS]
pwr = [n for n in members if n in D.POWER_NETS]
cls = ('(class kicad_default "" ' + " ".join(sig) + '\n      (circuit (use_via Via[0-1]_600:300_um))\n'
       '      (rule (width 250) (clearance 200))\n    )\n'
       '    (class power ' + " ".join(pwr) + '\n      (circuit (use_via Via[0-1]_600:300_um))\n'
       '      (rule (width 400) (clearance 200))\n    )')
start = txt.index('(class kicad_default')
depth, i = 0, start
while True:
    if txt[i] == "(": depth += 1
    elif txt[i] == ")":
        depth -= 1
        if depth == 0: break
    i += 1
txt = txt[:start] + cls + txt[i + 1:]
open(DSN, "w").write(txt)

# 3. Freerouting
if os.path.exists(SES):
    os.remove(SES)
cmd = ["xvfb-run", "-a", "java", "-Djava.awt.headless=false", "-jar", JAR, "-de", DSN, "-do", SES, "-mp", PASSES]
print(" ".join(cmd), flush=True)
r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
print(r.stdout[-3000:], r.stderr[-2000:])
assert os.path.exists(SES), "Freerouting wrote no session file"
print("imported session: %d track segments, %d vias" % import_ses(b, SES))
for z in pours:
    b.Add(z)
filler = pcbnew.ZONE_FILLER(b)
filler.Fill(b.Zones())
pcbnew.SaveBoard(PCB, b)
print("tracks", sum(1 for t in b.GetTracks() if t.GetClass() == "PCB_TRACK"),
      "vias", sum(1 for t in b.GetTracks() if t.GetClass() == "PCB_VIA"))
