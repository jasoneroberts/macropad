"""Concept B main PCB: parts, nets and placement. The single source of truth for the board, the schematic and the
Altium hand-off (build_board.py, schematic.py, export_altium.py all read this file).

Coordinates are the case's plate frame (the same as pcb/generate.py and the DXF): mm, origin at the case's front-left
corner, x to the right, y toward the back (the screen end), seen from the top. Bottom-side parts are given where they
physically sit, seen through the board.

Every part is a JR library part (pcb/library/src/jr_parts.py), so the Altium components match JR.SchLib/JR.PcbLib.
"""
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPORT = json.load(open(os.path.join(ROOT, "build", "report_B.json")))

TITLE = "Macropad concept B main board"
REV = "A"
DATE = "2026-11-11"

# ---------------------------------------------------------------------------------------------------------------
# Controller pins: SuperMini nRF52840 (nice!nano v2 pinout). (pin, label on the module, nRF pin, net or None)
# Same map as firmware/boards/promicro_nrf52840_nrf52840_uf2.overlay and pcb/generate.py.
# The LCD signals sit on pins 5-10, which face the LCD wire pads (J2) once U1 is mounted face down, so the six
# LCD tracks run straight across; SPI clock and data stay on full-speed pins (P0.20, P0.17).
U1_PINS = [
    (1, "D1", "P0.06", "DBG_TX"), (2, "D0", "P0.08", None), (3, "GND", "", "GND"), (4, "GND", "", "GND"),
    (5, "D2", "P0.17", "LCD_MOSI"), (6, "D3", "P0.20", "LCD_SCK"), (7, "D4", "P0.22", "LCD_CS"),
    (8, "D5", "P0.24", "LCD_DC"), (9, "D6", "P1.00", "LCD_RST"), (10, "D7", "P0.11", "LCD_BL"),
    (11, "D8", "P1.04", "ROW2"), (12, "D9", "P1.06", "COL0"), (13, "D10", "P0.09", "ENC_A"),
    (14, "D16", "P0.10", "ENC_B"), (15, "D14", "P1.11", "COL1"), (16, "D15", "P1.13", "COL2"),
    (17, "D18", "P1.15", "ROW0"), (18, "D19", "P0.02", "ROW1"), (19, "D20", "P0.29", "COL3"),
    (20, "D21", "P0.31", "COL4"), (21, "VCC", "", "3V3_SW"), (22, "RST", "", "NRST"), (23, "GND", "", "GND"),
    (24, "B+", "", "VBAT_SW"),
]
# Waveshare LCD cable order (VCC, GND, DIN, CLK, CS, DC, RST, BL)
J2_PINS = [(1, "VCC", "3V3_SW"), (2, "GND", "GND"), (3, "DIN", "LCD_MOSI"), (4, "CLK", "LCD_SCK"), (5, "CS", "LCD_CS"),
           (6, "DC", "LCD_DC"), (7, "RST", "LCD_RST"), (8, "BL", "LCD_BL")]

ROWS, COLS = REPORT["rows"], REPORT["cols"]          # 3 x 4 keys; the knob push is column 4
PUSH_COL = COLS

# ---------------------------------------------------------------------------------------------------------------
# Parts: ref -> (JR part, note)
PARTS = {}
NETS = {}             # net -> [(ref, pad)]


def c(net, ref, pad):
    NETS.setdefault(net, []).append((ref, str(pad)))


PARTS["U1"] = ("SuperMini_nRF52840", "Bottom side, hanging under the board on 2.5 mm low-profile headers with its components facing "
               "down (its plain back toward the PCB). "
               "No headers on the 3 inner pins")
for pin, _, _, net in U1_PINS:
    if net:
        c(net, "U1", pin)

# Keys: firmware key n = row * 4 + col; row 0 is the back row (next to the screen). SW(n+1), D(n+1).
KX = sorted({round(k[0], 3) for k in REPORT["keys_xy"]})
KY = sorted({round(k[1], 3) for k in REPORT["keys_xy"]}, reverse=True)     # row 0 = largest y
KEYS = []
for n in range(ROWS * COLS):
    r, col = divmod(n, COLS)
    KEYS.append((n, r, col, KX[col], KY[r]))
    sw, d = f"SW{n + 1}", f"D{n + 1}"
    PARTS[sw] = ("SW_Kailh_MX_Hotswap", f"key {n}: row {r}, column {col}")
    PARTS[d] = ("D_1N4148W_SOD-123", f"key {n} diode")
    c(f"ROW{r}", sw, 1); c(f"K{n + 1}", sw, 2)
    c(f"K{n + 1}", d, 2); c(f"COL{col}", d, 1)              # diode pad 2 = anode (switch side), pad 1 = cathode

NK = ROWS * COLS
DP = f"D{NK + 1}"
PARTS["ENC1"] = ("Encoder_PEC11R-4220F-S0024", "knob: A/B to the controller, push switch into row 0, column 4")
PARTS[DP] = ("D_1N4148W_SOD-123", "knob push diode")
c("ENC_A", "ENC1", "A"); c("GND", "ENC1", "C"); c("ENC_B", "ENC1", "B")
c("ROW0", "ENC1", "S1"); c("K_PUSH", "ENC1", "S2")
c("K_PUSH", DP, 2); c(f"COL{PUSH_COL}", DP, 1)
PARTS["C1"] = ("C_10n_0805", "ENC_A debounce, with the internal pull-up"); c("ENC_A", "C1", 1); c("GND", "C1", 2)
PARTS["C2"] = ("C_10n_0805", "ENC_B debounce, with the internal pull-up"); c("ENC_B", "C2", 1); c("GND", "C2", 2)

PARTS["J2"] = ("Conn_Wire_Pads_1x08", "LCD cable wires (Waveshare order)")
for pin, _, net in J2_PINS:
    c(net, "J2", pin)
PARTS["C3"] = ("C_10u_0805", "LCD supply bulk"); c("3V3_SW", "C3", 1); c("GND", "C3", 2)

PARTS["J1"] = ("Conn_JST_PH_S2B_Horizontal", "LiPo plug, pin 1 = +"); c("VBAT", "J1", 1); c("GND", "J1", 2)
PARTS["SW_PWR"] = ("SW_Slide_OS102011MA1QN1", "battery on/off, actuator through the right wall")
c("VBAT", "SW_PWR", 1); c("VBAT_SW", "SW_PWR", 2)
PARTS["SW_RST"] = ("SW_Tact_TS-1187A-B-A-B", "reset; double-press = UF2 bootloader")
c("NRST", "SW_RST", 1); c("NRST", "SW_RST", 2); c("GND", "SW_RST", 3); c("GND", "SW_RST", 4)
PARTS["TP1"] = ("TestPoint_Pad_1.5mm", "UART log out, 115200"); c("DBG_TX", "TP1", 1)
PARTS["TP2"] = ("TestPoint_Pad_1.5mm", "GND for the UART log"); c("GND", "TP2", 1)
for i, _ in enumerate(REPORT["pillars"], 1):
    PARTS[f"H{i}"] = ("MountingHole_M2", "M2 screw into the case pillar")

POWER_NETS = {"GND", "VBAT", "VBAT_SW", "3V3_SW"}
NO_CONNECT = {"U1": [2], "SW_PWR": [3]}

# ---------------------------------------------------------------------------------------------------------------
# Placement. Each entry: side, and where two or more pads must land (plate frame). build_board.py finds the
# rotation that puts them there, so the intent (e.g. "anode toward the socket") is written down, not a rotation.
UX, UY = REPORT["mcu_c"]                        # 82, 96.25
EX, EY = 82.0, REPORT["enc"][1]                 # knob moved 1 mm left so its lugs clear U1's pins
PITCH = 2.54
J2X = 93.6
SWX, SWY = 95.7, REPORT["sw_y"]                 # slide switch pin row, 2.2 mm in from the body's outer face

PLACE = {
    # U1 face down: pin 1 (P0.06) at the back right in the top view, pins 1-12 down the right column
    "U1": ("B", {"1": (UX + 7.62, UY + 13.97), "12": (UX + 7.62, UY - 13.97), "13": (UX - 7.62, UY - 13.97)}),
    # Knob: A/C/B to the front, switch pins to the back, lugs left and right (between U1's pin rows)
    "ENC1": ("T", {"A": (EX - 2.5, EY - 7.5), "B": (EX + 2.5, EY - 7.5), "S1": (EX + 2.5, EY + 7.0)}),
    "J2": ("B", {"1": (J2X, UY + 8.89), "8": (J2X, UY - 8.89)}),
    "C3": ("B", {"1": (71.0, 103.55), "2": (71.0, 101.65)}),        # next to U1 pin 21 (VCC out)
    "SW_PWR": ("B", {"1": (SWX, SWY + 2.0), "3": (SWX, SWY - 2.0)}),
    "J1": ("B", {"1": (86.0, 71.0), "2": (86.0, 73.0)}),
    "SW_RST": ("B", {"1": (71.5, 64.25), "3": (71.5, 68.0)}),
    "C1": ("B", {"1": (77.4, 78.3), "2": (77.4, 76.4)}),
    "C2": ("B", {"1": (86.6, 78.3), "2": (86.6, 76.4)}),
    DP: ("B", {"2": (83.65, 77.0), "1": (80.35, 77.0)}),
    "TP1": ("B", {"1": (70.9, 110.9)}),
    "TP2": ("B", {"1": (70.9, 107.9)}),
}
for n, r, col, kx, ky in KEYS:
    # Socket under the switch: pad 1 (row) left, pad 2 (diode) right, switch pins toward the back
    PLACE[f"SW{n + 1}"] = ("B", {"1": (kx - 7.085, ky + 2.54), "2": (kx + 5.842, ky + 5.08)})
    # Diode in front of the switch centre, anode (pad 2) toward the socket's pad 2 side
    PLACE[f"D{n + 1}"] = ("B", {"2": (kx + 1.65, ky - 5.5), "1": (kx - 1.65, ky - 5.5)})
for i, (px, py) in enumerate(REPORT["pillars"], 1):
    PLACE[f"H{i}"] = ("T", {"": (px, py)})

# ---------------------------------------------------------------------------------------------------------------
# Board outline (plate frame), from scad/macropad.scad pcb_2d(): the case outline inset by wall + 0.5 mm, minus the
# corner bosses, minus the display opening, which is open to the back edge (no thin strip left of or above it).
W, L, WALL = REPORT["W"], REPORT["L"], REPORT["wall"]
INSET = WALL + 0.5
X0, Y0, X1, Y1 = INSET, INSET, W - INSET, L - INSET
BOSS_R = 4.4                                   # boss d8 + 0.4 mm clearance
BOSSES = REPORT["bosses"]
DISP_X0, DISP_X1 = 9.0, 69.0                   # display module board 58 x 35 at (39, 87.65), + 1 mm
DISP_Y0 = REPORT["board_y"][0] - 1.0           # 69.15
DPILLAR = REPORT["dpillars"][0]                # (39, 66.65), the front display clamp pillar
DPILLAR_R = 5.5 / 2 + 0.5


def _tangent(p, c, r, side):
    """Tangent point on circle (c, r) from external point p; side=+1/-1 picks the left/right one (seen from p)."""
    dx, dy = c[0] - p[0], c[1] - p[1]
    d = math.hypot(dx, dy)
    a = math.atan2(dy, dx) + side * math.asin(r / d)
    t = math.sqrt(d * d - r * r)
    return (p[0] + t * math.cos(a), p[1] + t * math.sin(a))


def outline():
    """Closed outline as ("line", a, b) / ("arc", start, mid, end), counter-clockwise."""
    segs = []
    bx = lambda b, y: (b[0] + math.copysign(math.sqrt(BOSS_R ** 2 - (y - b[1]) ** 2), 0.0), y)
    dxb = math.sqrt(BOSS_R ** 2 - (BOSSES[0][0] - X0) ** 2)     # boss circle meets the edge this far from its centre
    b00, b10, b11 = BOSSES[0], BOSSES[1], BOSSES[3]
    mid = lambda b, a: (b[0] + BOSS_R * math.cos(math.radians(a)), b[1] + BOSS_R * math.sin(math.radians(a)))
    # bottom edge, right boss, right edge, back-right boss, back edge to the display opening
    segs.append(("line", (b00[0] + dxb, Y0), (b10[0] - dxb, Y0)))
    segs.append(("arc", (b10[0] - dxb, Y0), mid(b10, 135), (X1, b10[1] + dxb)))
    segs.append(("line", (X1, b10[1] + dxb), (X1, b11[1] - dxb)))
    segs.append(("arc", (X1, b11[1] - dxb), mid(b11, 225), (b11[0] - dxb, Y1)))
    segs.append(("line", (b11[0] - dxb, Y1), (DISP_X1, Y1)))
    # display opening: down its right side, under the clamp pillar, back up to the left edge
    t1 = _tangent((DISP_X1, DISP_Y0), DPILLAR, DPILLAR_R, +1)
    t2 = _tangent((DISP_X0, DISP_Y0), DPILLAR, DPILLAR_R, -1)
    segs.append(("line", (DISP_X1, Y1), (DISP_X1, DISP_Y0)))
    segs.append(("line", (DISP_X1, DISP_Y0), t1))
    segs.append(("arc", t1, (DPILLAR[0], DPILLAR[1] - DPILLAR_R), t2))
    segs.append(("line", t2, (DISP_X0, DISP_Y0)))
    segs.append(("line", (DISP_X0, DISP_Y0), (X0, DISP_Y0)))
    # left edge, front-left boss
    segs.append(("line", (X0, DISP_Y0), (X0, b00[1] + dxb)))
    segs.append(("arc", (X0, b00[1] + dxb), mid(b00, 45), (b00[0] + dxb, Y0)))
    return segs


def outline_polygon(step_deg=5):
    """The outline as a point list (arcs subdivided), for checks."""
    pts = []
    for s in outline():
        if s[0] == "line":
            pts.append(s[1])
        else:
            a, m, e = s[1:]
            ax, ay = a; bx_, by = m; cx, cy = e
            d = 2 * (ax * (by - cy) + bx_ * (cy - ay) + cx * (ay - by))
            ux = ((ax*ax + ay*ay) * (by - cy) + (bx_*bx_ + by*by) * (cy - ay) + (cx*cx + cy*cy) * (ay - by)) / d
            uy = ((ax*ax + ay*ay) * (cx - bx_) + (bx_*bx_ + by*by) * (ax - cx) + (cx*cx + cy*cy) * (bx_ - ax)) / d
            r = math.hypot(ax - ux, ay - uy)
            a0 = math.atan2(ay - uy, ax - ux); a1 = math.atan2(by - uy, bx_ - ux); a2 = math.atan2(cy - uy, cx - ux)
            sweep = (a2 - a0) % (2 * math.pi)
            if (a1 - a0) % (2 * math.pi) > sweep:
                sweep -= 2 * math.pi
            n = max(2, int(abs(math.degrees(sweep)) / step_deg))
            pts += [(ux + r * math.cos(a0 + sweep * i / n), uy + r * math.sin(a0 + sweep * i / n)) for i in range(n)]
    return pts


# Copper keep-outs (plate frame circles / polygons)
PILLAR_KEEPOUT_R = 2.6          # M2 pan head (d3.8) under the board, case pillar (d4.4) on top
U1_BOX = (UX - 9.5, UY - 16.5, UX + 9.5, UY + 17.6)    # module + USB overhang: no copper pour (antenna end unknown)
