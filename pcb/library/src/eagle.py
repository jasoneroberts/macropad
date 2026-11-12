"""EAGLE 7 XML writer shared by the JR library (.lbr) and the designs that use it (.sch / .brd).

Altium Designer 19 has no KiCad importer, but its Import Wizard reads EAGLE 6.4+ XML designs and libraries. EAGLE is
mm with y up; KiCad footprints are mm with y down, so every footprint y is negated.

What EAGLE cannot hold, and how it is carried:
  - SMD pads must be on the top layer of a package: parts whose pads belong on the bottom copper are drawn from the
    bottom (see the hot-swap socket) and placed mirrored ("MR" rotation).
  - Through-hole pads are round/square/octagon/long: an oval pad becomes a round pad of its narrow width.
  - Pad holes are round: an unplated slot becomes a round hole of the slot's width plus the slot outline on layer 46
    (Milling). After the Altium import, change those holes to slots (README step).
  - Pin and pad names must be unique: a repeated pin name gets "@<pin number>", which EAGLE and Altium display without
    the suffix.
"""
import math
from xml.sax.saxutils import escape, quoteattr

EAGLE_VERSION = "7.7.0"


def f(v):
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def a(**kw):
    return " ".join(f'{k.rstrip("_")}={quoteattr(str(v))}' for k, v in kw.items() if v is not None)


LAYERS = [(1, "Top", 4), (16, "Bottom", 1), (17, "Pads", 2), (18, "Vias", 2), (19, "Unrouted", 6), (20, "Dimension", 15),
          (21, "tPlace", 7), (22, "bPlace", 7), (23, "tOrigins", 15), (24, "bOrigins", 15), (25, "tNames", 7),
          (26, "bNames", 7), (27, "tValues", 7), (28, "bValues", 7), (29, "tStop", 7), (30, "bStop", 7),
          (31, "tCream", 7), (32, "bCream", 7), (35, "tGlue", 7), (36, "bGlue", 7), (39, "tKeepout", 4),
          (40, "bKeepout", 1), (41, "tRestrict", 4), (42, "bRestrict", 1), (43, "vRestrict", 2), (44, "Drills", 7),
          (45, "Holes", 7), (46, "Milling", 3), (47, "Measures", 7), (48, "Document", 7), (49, "Reference", 7),
          (51, "tDocu", 7), (52, "bDocu", 7), (91, "Nets", 2), (92, "Busses", 1), (93, "Pins", 2), (94, "Symbols", 4),
          (95, "Names", 7), (96, "Values", 7), (97, "Info", 7), (98, "Guide", 6)]


def layers_xml():
    return "<layers>\n" + "\n".join(f'<layer {a(number=n, name=nm, color=c, fill=1, visible="yes", active="yes")}/>'
                                    for n, nm, c in LAYERS) + "\n</layers>"


HEAD = (f'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE eagle SYSTEM "eagle.dtd">\n<eagle version="{EAGLE_VERSION}">\n'
        '<drawing>\n<settings>\n<setting alwaysvectorfont="no"/>\n<setting verticaltext="up"/>\n</settings>\n'
        '<grid distance="1.27" unitdist="mm" unit="mm" style="lines" multiple="1" display="no" altdistance="0.1" '
        'altunitdist="mm" altunit="mm"/>\n')
TAIL = "</drawing>\n</eagle>\n"


def arc_curve(s, m, e):
    """EAGLE 'curve' (degrees, + = counter-clockwise) for the arc s -> m -> e, all points y-up."""
    ax, ay = s; bx, by = m; cx, cy = e
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax*ax + ay*ay) * (by - cy) + (bx*bx + by*by) * (cy - ay) + (cx*cx + cy*cy) * (ay - by)) / d
    uy = ((ax*ax + ay*ay) * (cx - bx) + (bx*bx + by*by) * (ax - cx) + (cx*cx + cy*cy) * (bx - ax)) / d
    ang = lambda p: math.atan2(p[1] - uy, p[0] - ux)
    a0, a1, a2 = ang(s), ang(m), ang(e)
    ccw = lambda x, y: (y - x) % (2 * math.pi)
    sweep = ccw(a0, a2)
    return math.degrees(sweep) if ccw(a0, a1) <= sweep else -math.degrees(2 * math.pi - sweep)


def wire(p, q, w, layer, curve=None):
    cv = None if curve is None or abs(curve) < 1e-6 else f(curve)
    return f'<wire {a(x1=f(p[0]), y1=f(p[1]), x2=f(q[0]), y2=f(q[1]), width=f(w), layer=layer, curve=cv)}/>'


def text_xml(t, x, y, size, layer, rot=0, mirror=False, align="center"):
    r = ("M" if mirror else "") + f"R{int(round(rot)) % 360}"
    return f'<text {a(x=f(x), y=f(y), size=f(size), layer=layer, font="vector", ratio=12, rot=r, align=align)}>{escape(t)}</text>'


# ---------------------------------------------------------------------------------------------------------------
# Packages from KiCad footprints (pcbnew objects)
def _pcbnew():
    import pcbnew
    return pcbnew


def kicad_layer_map():
    pcbnew = _pcbnew()
    return {pcbnew.F_SilkS: 21, pcbnew.B_SilkS: 22, pcbnew.F_Fab: 51, pcbnew.B_Fab: 52, pcbnew.Edge_Cuts: 20,
            pcbnew.Dwgs_User: 48, pcbnew.Cmts_User: 49}


def shape_xml(g, T, layer):
    """One KiCad graphic as EAGLE primitives. T maps a KiCad point (mm, y down) to EAGLE coordinates."""
    pcbnew = _pcbnew()
    mm = pcbnew.ToMM
    st = g.GetShape(); w = mm(g.GetWidth())
    P = lambda v: T(mm(v.x), mm(v.y))
    if st == pcbnew.SHAPE_T_SEGMENT:
        return [wire(P(g.GetStart()), P(g.GetEnd()), w, layer)]
    if st == pcbnew.SHAPE_T_ARC:
        s, m, e = P(g.GetStart()), P(g.GetArcMid()), P(g.GetEnd())
        return [wire(s, e, w, layer, arc_curve(s, m, e))]
    if st == pcbnew.SHAPE_T_CIRCLE:
        c = P(g.GetCenter()); r = mm(g.GetRadius())
        return [f'<circle {a(x=f(c[0]), y=f(c[1]), radius=f(r), width=f(w), layer=layer)}/>']
    if st == pcbnew.SHAPE_T_RECT:
        s, e = g.GetStart(), g.GetEnd()
        pts = [T(mm(s.x), mm(s.y)), T(mm(e.x), mm(s.y)), T(mm(e.x), mm(e.y)), T(mm(s.x), mm(e.y))]
        return [wire(pts[i], pts[(i + 1) % 4], w, layer) for i in range(4)]
    if st == pcbnew.SHAPE_T_POLY:
        out = []
        ps = g.GetPolyShape()
        for i in range(ps.OutlineCount()):
            o = ps.Outline(i)
            vs = "".join(f'<vertex {a(x=f(T(mm(o.CPoint(k).x), mm(o.CPoint(k).y))[0]), y=f(T(mm(o.CPoint(k).x), mm(o.CPoint(k).y))[1]))}/>'
                         for k in range(o.PointCount()))
            out.append(f'<polygon {a(width=f(max(w, 0.0)), layer=layer)}>{vs}</polygon>')
        return out
    raise SystemExit(f"unhandled shape {g.GetShapeStr()}")


def slot_outline(cx, cy, sx, sy, rot_deg, w=0.0):
    """Milling outline (EAGLE layer 46) of an oval slot sx x sy centred on (cx, cy), y up."""
    L, W = max(sx, sy), min(sx, sy)
    r = W / 2
    ang = math.radians(rot_deg) + (0 if sx >= sy else math.pi / 2)
    ux, uy = math.cos(ang), math.sin(ang)
    vx, vy = -uy, ux
    h = L / 2 - r
    p = lambda s, t: (cx + ux * s + vx * t, cy + uy * s + vy * t)
    a1, a2, b1, b2 = p(-h, r), p(h, r), p(h, -r), p(-h, -r)
    return [wire(a1, a2, w, 46), wire(a2, b1, w, 46, -180), wire(b1, b2, w, 46), wire(b2, a1, w, 46, -180)]


def package_xml(fp, name=None):
    """EAGLE <package> for a pcbnew footprint (in its library orientation)."""
    pcbnew = _pcbnew()
    mm = pcbnew.ToMM
    KL = kicad_layer_map()
    name = name or str(fp.GetFPID().GetLibItemName())
    T = lambda x, y: (x, -y)
    out, names = [], set()
    for p in fp.Pads():
        n = p.GetNumber()
        x, y = T(mm(p.GetPosition().x), mm(p.GetPosition().y))
        sx, sy = mm(p.GetSize().x), mm(p.GetSize().y)
        ang = p.GetOrientationDegrees()
        rot = f"R{int(round(ang)) % 360}"
        shp = p.GetShape()
        att = p.GetAttribute()
        if att in (pcbnew.PAD_ATTRIB_SMD, pcbnew.PAD_ATTRIB_PTH):
            assert n and n not in names, f"{name}: pad number {n!r} empty or repeated"
            names.add(n)
        if att == pcbnew.PAD_ATTRIB_SMD:
            assert p.GetLayerSet().Contains(pcbnew.F_Cu), f"{name}: SMD pad {n} not on the front copper"
            if shp == pcbnew.PAD_SHAPE_RECT: rnd = 0
            elif shp == pcbnew.PAD_SHAPE_ROUNDRECT: rnd = min(100, round(200 * p.GetRoundRectRadiusRatio()))
            elif shp in (pcbnew.PAD_SHAPE_CIRCLE, pcbnew.PAD_SHAPE_OVAL): rnd = 100
            else: raise SystemExit(f"{name}: pad shape {shp}")
            paste = p.GetLayerSet().Contains(pcbnew.F_Paste)
            out.append(f'<smd {a(name=n, x=f(x), y=f(y), dx=f(sx), dy=f(sy), layer=1, roundness=rnd, rot=rot, cream=None if paste else "no")}/>')
        elif att == pcbnew.PAD_ATTRIB_PTH:
            drill = mm(min(p.GetDrillSize().x, p.GetDrillSize().y))
            dia = min(sx, sy)
            square = shp in (pcbnew.PAD_SHAPE_RECT, pcbnew.PAD_SHAPE_ROUNDRECT)
            out.append(f'<pad {a(name=n, x=f(x), y=f(y), drill=f(drill), diameter=f(dia), shape="square" if square else "round", rot=rot)}/>')
        else:   # unplated
            dx, dy = mm(p.GetDrillSize().x), mm(p.GetDrillSize().y)
            out.append(f'<hole {a(x=f(x), y=f(y), drill=f(min(dx, dy)))}/>')
            if abs(dx - dy) > 1e-3:
                out += slot_outline(x, y, dx, dy, ang)
    for g in fp.GraphicalItems():
        L = KL.get(g.GetLayer())
        if L is None:
            continue
        if isinstance(g, pcbnew.FP_TEXT):
            t = g.GetText().replace("${REFERENCE}", ">NAME").replace("${VALUE}", ">VALUE").replace("%R", ">NAME")
            x, y = T(mm(g.GetPosition().x), mm(g.GetPosition().y))
            out.append(text_xml(t, x, y, mm(g.GetTextHeight()), L, g.GetTextAngleDegrees(), mirror=L in (22, 52)))
        else:
            out += shape_xml(g, T, L)
    for t, field, L in ((">NAME", fp.Reference(), 25), (">VALUE", fp.Value(), 27)):
        x, y = T(mm(field.GetPosition().x), mm(field.GetPosition().y))
        out.append(text_xml(t, x, y, mm(field.GetTextHeight()), L, field.GetTextAngleDegrees()))
    desc = fp.GetDescription() or name
    return f'<package {a(name=name)}>\n<description>{escape(desc)}</description>\n' + "\n".join(out) + "\n</package>"


def pad_names(fp):
    pcbnew = _pcbnew()
    return [p.GetNumber() for p in fp.Pads() if p.GetAttribute() != pcbnew.PAD_ATTRIB_NPTH]


# ---------------------------------------------------------------------------------------------------------------
# Symbols from jr_symbols.Sym
def eagle_pin_names(sym):
    counts = {}
    for num, name, *_ in sym.pins:
        counts[name] = counts.get(name, 0) + 1
    return {num: (name if counts[name] == 1 else f"{name}@{num}").replace(" ", "_") for num, name, *_ in sym.pins}


def symbol_xml(sym):
    vis = {(False, False): "both", (True, False): "pad", (False, True): "pin", (True, True): "off"}[
        (sym.hide_pin_names, sym.hide_pin_numbers)]
    out = []
    W = 0.254
    for it in sym.items:
        k = it[0]
        if k == "rect":
            _, x0, y0, x1, y1, filled = it
            if filled:
                out.append(f'<rectangle {a(x1=f(min(x0, x1)), y1=f(min(y0, y1)), x2=f(max(x0, x1)), y2=f(max(y0, y1)), layer=94)}/>')
            else:
                c = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
                out += [wire(c[i], c[(i + 1) % 4], W, 94) for i in range(4)]
        elif k == "poly":
            _, pts, filled = it
            if filled:
                out.append(f'<polygon {a(width=f(W / 2), layer=94)}>' + "".join(f'<vertex {a(x=f(x), y=f(y))}/>' for x, y in pts) + "</polygon>")
            else:
                out += [wire(pts[i], pts[i + 1], W, 94) for i in range(len(pts) - 1)]
        elif k == "circle":
            _, x, y, r, filled = it
            out.append(f'<circle {a(x=f(x), y=f(y), radius=f(r), width=f(0 if filled else W), layer=94)}/>')
        elif k == "arc":
            _, s, m, e = it
            out.append(wire(s, e, W, 94, arc_curve(s, m, e)))
        elif k == "text":
            _, s, x, y, size = it
            out.append(text_xml(s, x, y, size, 94))
    names = eagle_pin_names(sym)
    LEN = {2.54: "short", 5.08: "middle"}
    for num, name, x, y, d, length in sym.pins:
        out.append(f'<pin {a(name=names[num], x=f(x), y=f(y), visible=vis, length=LEN[length], direction="pas", rot=f"R{d}")}/>')
    for t, (x, y, just), L in ((">NAME", sym.ref_at, 95), (">VALUE", sym.val_at, 96)):
        al = {"left": "center-left", "right": "center-right", "center": "center"}[just]
        out.append(text_xml(t, x, y, 1.778, L, align=al))
    return f'<symbol {a(name=sym.name)}>\n<description>{escape(sym.desc)}</description>\n' + "\n".join(out) + "\n</symbol>"


def attributes(p, **kw):
    """EAGLE attributes for a JR part (EAGLE stores attribute names in upper case, without spaces)."""
    vals = (("MANUFACTURER", p["manufacturer"]), ("MPN", p["mpn"]), ("LCSC", p["lcsc"]),
            ("DESCRIPTION", p["description"]))
    return "".join(f'<attribute {a(name=k, value=v, **kw)}/>' for k, v in vals if v)


def deviceset_xml(p, sym, fp_pads):
    names = eagle_pin_names(sym)
    pins = {num for num, *_ in sym.pins}
    assert pins <= set(fp_pads), (p["name"], pins - set(fp_pads))
    con = "".join(f'<connect {a(gate="G$1", pin=names[n], pad=n)}/>' for n in fp_pads if n in pins)
    tech = f'<technology name="">{attributes(p)}</technology>'
    return (f'<deviceset {a(name=p["name"], prefix=sym.prefix, uservalue="yes")}>\n'
            f'<description>{escape(p["description"])}</description>\n'
            f'<gates><gate {a(name="G$1", symbol=sym.name, x=0, y=0)}/></gates>\n<devices>\n'
            f'<device {a(name="", package=p["footprint"])}>\n<connects>{con}</connects>\n'
            f'<technologies>{tech}</technologies>\n</device>\n</devices>\n</deviceset>')


def library_xml(libname, packages, symbols, devicesets, description=""):
    return (f'<library {a(name=libname)}>\n<description>{escape(description)}</description>\n<packages>\n'
            + "\n".join(packages) + "\n</packages>\n<symbols>\n" + "\n".join(symbols) + "\n</symbols>\n<devicesets>\n"
            + "\n".join(devicesets) + "\n</devicesets>\n</library>")
