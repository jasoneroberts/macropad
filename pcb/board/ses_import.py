"""Reads a Freerouting/Specctra session (.ses) into a pcbnew board: wires and vias of every net.

pcbnew's own ImportSpecctraSES() only works inside the PCB editor, so this does the same from a script.
Session coordinates are in (resolution um N) units with y negated; KiCad's DSN export uses um with y up.
"""
import re

import pcbnew


def _sexpr(text):
    tok = re.findall(r'"(?:[^"\\]|\\.)*"|[()]|[^\s()"]+', text)
    stack, cur = [], []
    for t in tok:
        if t == "(":
            stack.append(cur); cur = []
        elif t == ")":
            done = cur; cur = stack.pop(); cur.append(done)
        else:
            cur.append(t.strip('"'))
    return cur[0]


def _kids(n, tag):
    return [k for k in n[1:] if isinstance(k, list) and k and k[0] == tag]


def import_ses(board, path, replace=True):
    s = _sexpr(open(path).read())
    routes = _kids(s, "routes")[0]
    res = _kids(routes, "resolution")[0]
    scale = {"um": 1e-3, "mil": 0.0254, "mm": 1.0}[res[1]] / float(res[2])     # session unit -> mm
    pt = lambda x, y: pcbnew.VECTOR2I(pcbnew.FromMM(float(x) * scale), pcbnew.FromMM(-float(y) * scale))
    vias = {}
    lib = _kids(routes, "library_out")
    for ps in (_kids(lib[0], "padstack") if lib else []):
        shapes = [k for k in _kids(ps, "shape")]
        d = float(shapes[0][1][2]) * scale
        vias[ps[1]] = d
    layers = {"F.Cu": pcbnew.F_Cu, "B.Cu": pcbnew.B_Cu}
    if replace:
        for t in list(board.GetTracks()):
            if not t.IsLocked():
                board.Remove(t)
    n_w = n_v = 0
    for net in _kids(_kids(routes, "network_out")[0], "net"):
        ni = board.FindNet(net[1])
        for w in _kids(net, "wire"):
            if any(t[1] == "protect" for t in _kids(w, "type")):
                continue                     # fixed (pre-routed, locked) wiring is already on the board
            p = _kids(w, "path")[0]
            layer, width = layers[p[1]], float(p[2]) * scale
            xy = p[3:]
            pts = [pt(xy[i], xy[i + 1]) for i in range(0, len(xy), 2)]
            for a, c in zip(pts, pts[1:]):
                t = pcbnew.PCB_TRACK(board)
                t.SetStart(a); t.SetEnd(c); t.SetWidth(pcbnew.FromMM(width)); t.SetLayer(layer); t.SetNet(ni)
                board.Add(t); n_w += 1
        for v in _kids(net, "via"):
            name, x, y = v[1], v[2], v[3]
            via = pcbnew.PCB_VIA(board)
            via.SetPosition(pt(x, y)); via.SetWidth(pcbnew.FromMM(vias.get(name, 0.6)))
            via.SetDrill(pcbnew.FromMM(0.3)); via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu); via.SetNet(ni)
            board.Add(via); n_v += 1
    return n_w, n_v
