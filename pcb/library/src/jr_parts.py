"""The JR component library: one entry per real, orderable part ("atomic" parts).

Each entry becomes one Altium library component (SchLib symbol + PcbLib footprint + parameters), one EAGLE deviceset
(the import route into Altium 19) and one KiCad symbol. Keep the names stable: designs find their parts by name,
and Altium's Tools > Update From Libraries relinks by them.

Parameters on every part (Altium names): Value, Description, Manufacturer, Manufacturer Part Number, LCSC.
Comment = Value. Empty strings are fine (wire pads, test pads).

LCSC numbers were looked up on lcsc.com on 2026-11-11 (macropad parts) or come from the carrier's order list.
"""

#  name: (symbol, footprint, value, description, manufacturer, MPN, LCSC, used on)
PARTS = {
    # ---- controllers --------------------------------------------------------------------------------------------
    "SuperMini_nRF52840": ("SuperMini_nRF52840", "SuperMini_nRF52840", "SuperMini nRF52840",
        "nRF52840 module, nice!nano v2 pinout, LiPo charger, USB-C. Pro Micro 24-pin", "generic (nice!nano v2 clone)",
        "SuperMini nRF52840", "", "macropad"),
    "XIAO_nRF52840": ("XIAO_nRF52840", "XIAO_nRF52840_SMD", "XIAO nRF52840",
        "nRF52840 module with LiPo charger, 3V3 regulator, USB-C; castellated edge, SWD and battery pads",
        "Seeed Studio", "102010448", "", "carrier"),
    # ---- switches, encoder --------------------------------------------------------------------------------------
    "SW_Kailh_MX_Hotswap": ("SW_Key", "SW_Kailh_MX_Hotswap", "MX hot-swap",
        "Kailh MX hot-swap socket for MX switches. Footprint goes on the bottom layer", "Kailh", "CPG151101S11",
        "C2803348", "macropad"),
    "Encoder_PEC11R-4220F-S0024": ("RotaryEncoder_Switch", "RotaryEncoder_EC11_Switch_NPTH", "PEC11R-4220F-S0024",
        "Rotary encoder, 24 detents / 24 pulses, push switch, 20 mm flatted shaft, EC11 size", "Bourns",
        "PEC11R-4220F-S0024", "C143797", "macropad"),
    "SW_Slide_OS102011MA1QN1": ("SW_SPDT", "SW_Slide_SPDT_Angled_CK_OS102011MA1Q", "OS102011MA1QN1",
        "Slide switch SPDT, right angle, through-hole, 4 mm actuator", "C&K", "OS102011MA1QN1", "C226259", "macropad"),
    "SW_Tact_TS-1187A-B-A-B": ("SW_Push_4pin", "SW_Push_1P1T_XKB_TS-1187A", "TS-1187A-B-A-B",
        "Tactile switch 5.1 x 5.1 x 1.5 mm, SMD gull-wing, 160 gf", "XKB Connection", "TS-1187A-B-A-B", "C318884",
        "macropad"),
    # ---- diodes, transistors ------------------------------------------------------------------------------------
    "D_1N4148W_SOD-123": ("D", "D_SOD-123", "1N4148W", "Switching diode 100 V 150 mA, SOD-123", "ST(Semtech)",
        "1N4148W", "C81598", "macropad"),
    "D_SS14_SMA": ("D_Schottky", "D_SMA", "SS14", "Schottky diode 40 V 1 A, SMA", "MDD", "SS14", "C2480", "carrier"),
    "Q_DMG2305UX_SOT-23": ("Q_PMOS_GSD", "SOT-23", "DMG2305UX", "P-MOSFET -20 V -4.2 A, SOT-23", "Diodes Inc",
        "DMG2305UX-7", "C150470", "carrier"),
    # ---- passives -----------------------------------------------------------------------------------------------
    "R_2k2_0805": ("R", "R_0805_2012Metric", "2k2", "Resistor 2.2 kOhm 1% 0805", "YAGEO", "RC0805FR-072K2L",
        "C114561", "carrier"),
    "R_100k_0805": ("R", "R_0805_2012Metric", "100k", "Resistor 100 kOhm 1% 0805", "UNI-ROYAL", "0805W8F1003T5E",
        "C149504", "carrier"),
    "C_10n_0805": ("C", "C_0805_2012Metric", "10nF", "Capacitor 10 nF 50 V X7R 0805", "Samsung", "CL21B103KBANNNC",
        "C1710", "macropad"),
    "C_1u_0805": ("C", "C_0805_2012Metric", "1uF", "Capacitor 1 uF 50 V X7R 0805", "Samsung", "CL21B105KBFNNNE",
        "C28323", "carrier"),
    "C_10u_0805": ("C", "C_0805_2012Metric", "10uF", "Capacitor 10 uF 25 V X5R 0805", "Samsung", "CL21A106KAYNNNE",
        "C15850", "macropad, carrier"),
    # ---- connectors ---------------------------------------------------------------------------------------------
    "Conn_JST_PH_S2B_Horizontal": ("Conn_01x02", "JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal", "S2B-PH-K-S",
        "JST PH 2-pin header, side entry, through-hole (LiPo plug)", "JST", "S2B-PH-K-S(LF)(SN)", "C173752", "macropad"),
    "Conn_JST_PH_B2B_Vertical": ("Conn_01x02", "JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", "B2B-PH-K-S",
        "JST PH 2-pin header, top entry, through-hole (LiPo plug)", "JST", "B2B-PH-K-S(LF)(SN)", "C131337", "carrier"),
    "Conn_Wire_Pads_1x08": ("Conn_01x08", "PinHeader_1x08_P2.54mm_Vertical", "Wire pads 1x8",
        "8 plated holes, 2.54 mm, 1.0 mm drill: solder wires (or a 1x8 header)", "", "", "", "macropad"),
    "Conn_Wire_Pads_1x02": ("Conn_01x02", "PinHeader_1x02_P2.54mm_Vertical", "Wire pads 1x2",
        "2 plated holes, 2.54 mm, 1.0 mm drill: solder wires (or a 1x2 header)", "", "", "", "carrier"),
    "Conn_2x05_1.27mm_Shrouded": ("Conn_02x05_Odd_Even", "PinHeader_2x05_P1.27mm_Vertical", "2x5 1.27 mm",
        "2 x 5 header, 1.27 mm pitch, shrouded, through-hole", "", "1.27 mm 2x5 box header THT", "", "carrier"),
    "Conn_2x04_2.00mm_Socket": ("Conn_02x04_Odd_Even", "PinHeader_2x04_P2.00mm_Vertical", "2x4 2.00 mm",
        "2 x 4 socket (female), 2.00 mm pitch, through-hole", "", "2.0 mm 2x4 female header THT", "", "carrier"),
    # ---- mechanical ---------------------------------------------------------------------------------------------
    "TestPoint_Pad_1.5mm": ("TestPoint", "TestPoint_Pad_D1.5mm", "Test pad", "Test pad, 1.5 mm, no part fitted",
        "", "", "", "macropad, carrier"),
    "MountingHole_M2": ("MountingHole", "MountingHole_2.2mm_M2", "M2 hole", "Unplated 2.2 mm hole for an M2 screw",
        "", "", "", "macropad"),
}

FIELDS = ("symbol", "footprint", "value", "description", "manufacturer", "mpn", "lcsc", "used")


def part(name):
    return dict(zip(FIELDS, PARTS[name]), name=name)
