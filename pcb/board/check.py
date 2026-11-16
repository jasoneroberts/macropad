#!/usr/bin/env python3
"""KiCad checks on the routed board: unrouted connections and the DRC report.

    /usr/bin/python3 pcb/board/check.py <board.kicad_pcb> [report.txt]
"""
import sys

import pcbnew

b = pcbnew.LoadBoard(sys.argv[1])
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
b.BuildConnectivity()
un = b.GetConnectivity().GetUnconnectedCount(False)
rep = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1].replace(".kicad_pcb", "-drc.txt")
pcbnew.WriteDRCReport(b, rep, pcbnew.EDA_UNITS_MILLIMETRES, True)
txt = open(rep).read()
print("unconnected:", un)
for line in txt.splitlines():
    if line.startswith("**") or line.startswith("["):
        print(line)
