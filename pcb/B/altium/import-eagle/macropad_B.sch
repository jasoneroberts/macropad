<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="7.7.0">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="1.27" unitdist="mm" unit="mm" style="lines" multiple="1" display="no" altdistance="0.1" altunitdist="mm" altunit="mm"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="yes" active="yes"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="yes" active="yes"/>
<layer number="17" name="Pads" color="2" fill="1" visible="yes" active="yes"/>
<layer number="18" name="Vias" color="2" fill="1" visible="yes" active="yes"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="yes" active="yes"/>
<layer number="20" name="Dimension" color="15" fill="1" visible="yes" active="yes"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="yes" active="yes"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="yes" active="yes"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="yes" active="yes"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="yes" active="yes"/>
<layer number="25" name="tNames" color="7" fill="1" visible="yes" active="yes"/>
<layer number="26" name="bNames" color="7" fill="1" visible="yes" active="yes"/>
<layer number="27" name="tValues" color="7" fill="1" visible="yes" active="yes"/>
<layer number="28" name="bValues" color="7" fill="1" visible="yes" active="yes"/>
<layer number="29" name="tStop" color="7" fill="1" visible="yes" active="yes"/>
<layer number="30" name="bStop" color="7" fill="1" visible="yes" active="yes"/>
<layer number="31" name="tCream" color="7" fill="1" visible="yes" active="yes"/>
<layer number="32" name="bCream" color="7" fill="1" visible="yes" active="yes"/>
<layer number="35" name="tGlue" color="7" fill="1" visible="yes" active="yes"/>
<layer number="36" name="bGlue" color="7" fill="1" visible="yes" active="yes"/>
<layer number="39" name="tKeepout" color="4" fill="1" visible="yes" active="yes"/>
<layer number="40" name="bKeepout" color="1" fill="1" visible="yes" active="yes"/>
<layer number="41" name="tRestrict" color="4" fill="1" visible="yes" active="yes"/>
<layer number="42" name="bRestrict" color="1" fill="1" visible="yes" active="yes"/>
<layer number="43" name="vRestrict" color="2" fill="1" visible="yes" active="yes"/>
<layer number="44" name="Drills" color="7" fill="1" visible="yes" active="yes"/>
<layer number="45" name="Holes" color="7" fill="1" visible="yes" active="yes"/>
<layer number="46" name="Milling" color="3" fill="1" visible="yes" active="yes"/>
<layer number="47" name="Measures" color="7" fill="1" visible="yes" active="yes"/>
<layer number="48" name="Document" color="7" fill="1" visible="yes" active="yes"/>
<layer number="49" name="Reference" color="7" fill="1" visible="yes" active="yes"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="yes" active="yes"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="yes" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="JR">
<description>JR library (subset used by this design)</description>
<packages>
<package name="C_0805_2012Metric">
<description>Capacitor SMD 0805 (2012 Metric), square (rectangular) end terminal, IPC_7351 nominal, (Body size source: IPC-SM-782 page 76, https://www.pcb-3d.com/wordpress/wp-content/uploads/ipc-sm-782a_amendment_1_and_2.pdf, https://docs.google.com/spreadsheets/d/1BsfQQcO9C6DZCsRaXUlFlo91Tg2WpOkGARC1WS5S8t0/edit?usp=sharing), generated with kicad-footprint-generator</description>
<smd name="1" x="-0.95" y="0" dx="1" dy="1.45" layer="1" roundness="50" rot="R0"/>
<smd name="2" x="0.95" y="0" dx="1" dy="1.45" layer="1" roundness="50" rot="R0"/>
<text x="0" y="0" size="0.5" layer="51" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<wire x1="-0.2613" y1="0.735" x2="0.2613" y2="0.735" width="0.12" layer="21"/>
<wire x1="-0.2613" y1="-0.735" x2="0.2613" y2="-0.735" width="0.12" layer="21"/>
<wire x1="-1" y1="0.625" x2="1" y2="0.625" width="0.1" layer="51"/>
<wire x1="-1" y1="-0.625" x2="-1" y2="0.625" width="0.1" layer="51"/>
<wire x1="1" y1="0.625" x2="1" y2="-0.625" width="0.1" layer="51"/>
<wire x1="1" y1="-0.625" x2="-1" y2="-0.625" width="0.1" layer="51"/>
<text x="0" y="1.68" size="1" layer="25" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<text x="0" y="-1.68" size="1" layer="27" font="vector" ratio="12" rot="R0" align="center">&gt;VALUE</text>
</package>
<package name="D_SOD-123">
<description>SOD-123</description>
<smd name="1" x="-1.65" y="0" dx="0.9" dy="1.2" layer="1" roundness="50" rot="R0"/>
<smd name="2" x="1.65" y="0" dx="0.9" dy="1.2" layer="1" roundness="50" rot="R0"/>
<text x="0" y="2" size="1" layer="51" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<wire x1="-2.36" y1="1" x2="-2.36" y2="-1" width="0.12" layer="21"/>
<wire x1="-2.36" y1="1" x2="1.65" y2="1" width="0.12" layer="21"/>
<wire x1="-2.36" y1="-1" x2="1.65" y2="-1" width="0.12" layer="21"/>
<wire x1="-1.4" y1="0.9" x2="1.4" y2="0.9" width="0.1" layer="51"/>
<wire x1="-1.4" y1="-0.9" x2="-1.4" y2="0.9" width="0.1" layer="51"/>
<wire x1="-0.75" y1="0" x2="-0.35" y2="0" width="0.1" layer="51"/>
<wire x1="-0.35" y1="0" x2="-0.35" y2="0.55" width="0.1" layer="51"/>
<wire x1="-0.35" y1="0" x2="-0.35" y2="-0.55" width="0.1" layer="51"/>
<wire x1="-0.35" y1="0" x2="0.25" y2="0.4" width="0.1" layer="51"/>
<wire x1="0.25" y1="0.4" x2="0.25" y2="-0.4" width="0.1" layer="51"/>
<wire x1="0.25" y1="0" x2="0.75" y2="0" width="0.1" layer="51"/>
<wire x1="0.25" y1="-0.4" x2="-0.35" y2="0" width="0.1" layer="51"/>
<wire x1="1.4" y1="0.9" x2="1.4" y2="-0.9" width="0.1" layer="51"/>
<wire x1="1.4" y1="-0.9" x2="-1.4" y2="-0.9" width="0.1" layer="51"/>
<text x="0" y="2" size="1" layer="25" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<text x="0" y="-2.1" size="1" layer="27" font="vector" ratio="12" rot="R0" align="center">&gt;VALUE</text>
</package>
<package name="JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal">
<description>JST PH series connector, S2B-PH-K (http://www.jst-mfg.com/product/pdf/eng/ePH.pdf), generated with kicad-footprint-generator</description>
<pad name="1" x="0" y="0" drill="0.75" diameter="1.2" shape="square" rot="R0"/>
<pad name="2" x="2" y="0" drill="0.75" diameter="1.2" shape="round" rot="R0"/>
<text x="1" y="-2.5" size="1" layer="51" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<wire x1="-2.06" y1="1.46" x2="-2.06" y2="-6.36" width="0.12" layer="21"/>
<wire x1="-2.06" y1="-0.14" x2="-1.14" y2="-0.14" width="0.12" layer="21"/>
<wire x1="-2.06" y1="-6.36" x2="4.06" y2="-6.36" width="0.12" layer="21"/>
<wire x1="-1.3" y1="-2.5" x2="-1.3" y2="-4.1" width="0.12" layer="21"/>
<wire x1="-1.3" y1="-4.1" x2="-0.3" y2="-4.1" width="0.12" layer="21"/>
<wire x1="-1.14" y1="1.46" x2="-2.06" y2="1.46" width="0.12" layer="21"/>
<wire x1="-1.14" y1="-0.14" x2="-1.14" y2="1.46" width="0.12" layer="21"/>
<wire x1="-0.86" y1="-0.14" x2="-1.14" y2="-0.14" width="0.12" layer="21"/>
<wire x1="-0.86" y1="-0.14" x2="-0.86" y2="1.075" width="0.12" layer="21"/>
<wire x1="-0.8" y1="-4.1" x2="-0.8" y2="-6.36" width="0.12" layer="21"/>
<wire x1="-0.3" y1="-2.5" x2="-1.3" y2="-2.5" width="0.12" layer="21"/>
<wire x1="-0.3" y1="-4.1" x2="-0.3" y2="-2.5" width="0.12" layer="21"/>
<wire x1="-0.3" y1="-4.1" x2="-0.3" y2="-6.36" width="0.12" layer="21"/>
<wire x1="0.5" y1="-2" x2="1.5" y2="-2" width="0.12" layer="21"/>
<wire x1="0.5" y1="-6.36" x2="0.5" y2="-2" width="0.12" layer="21"/>
<wire x1="1.5" y1="-2" x2="1.5" y2="-6.36" width="0.12" layer="21"/>
<wire x1="2.3" y1="-2.5" x2="3.3" y2="-2.5" width="0.12" layer="21"/>
<wire x1="2.3" y1="-4.1" x2="2.3" y2="-2.5" width="0.12" layer="21"/>
<wire x1="3.14" y1="1.46" x2="3.14" y2="-0.14" width="0.12" layer="21"/>
<wire x1="3.14" y1="-0.14" x2="2.86" y2="-0.14" width="0.12" layer="21"/>
<wire x1="3.3" y1="-2.5" x2="3.3" y2="-4.1" width="0.12" layer="21"/>
<wire x1="3.3" y1="-4.1" x2="2.3" y2="-4.1" width="0.12" layer="21"/>
<wire x1="4.06" y1="1.46" x2="3.14" y2="1.46" width="0.12" layer="21"/>
<wire x1="4.06" y1="-0.14" x2="3.14" y2="-0.14" width="0.12" layer="21"/>
<wire x1="4.06" y1="-6.36" x2="4.06" y2="1.46" width="0.12" layer="21"/>
<wire x1="-1.95" y1="1.35" x2="-1.95" y2="-6.25" width="0.1" layer="51"/>
<wire x1="-1.95" y1="-6.25" x2="3.95" y2="-6.25" width="0.1" layer="51"/>
<wire x1="-1.25" y1="1.35" x2="-1.95" y2="1.35" width="0.1" layer="51"/>
<wire x1="-1.25" y1="-0.25" x2="-1.25" y2="1.35" width="0.1" layer="51"/>
<wire x1="-0.5" y1="-1.375" x2="0.5" y2="-1.375" width="0.1" layer="51"/>
<wire x1="0" y1="-0.875" x2="-0.5" y2="-1.375" width="0.1" layer="51"/>
<wire x1="0.5" y1="-1.375" x2="0" y2="-0.875" width="0.1" layer="51"/>
<wire x1="3.25" y1="1.35" x2="3.25" y2="-0.25" width="0.1" layer="51"/>
<wire x1="3.25" y1="-0.25" x2="-1.25" y2="-0.25" width="0.1" layer="51"/>
<wire x1="3.95" y1="1.35" x2="3.25" y2="1.35" width="0.1" layer="51"/>
<wire x1="3.95" y1="-6.25" x2="3.95" y2="1.35" width="0.1" layer="51"/>
<text x="1" y="2.55" size="1" layer="25" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<text x="1" y="-7.45" size="1" layer="27" font="vector" ratio="12" rot="R0" align="center">&gt;VALUE</text>
</package>
<package name="MountingHole_2.2mm_M2">
<description>Mounting Hole 2.2mm, no annular, M2</description>
<hole x="0" y="0" drill="2.2"/>
<text x="0" y="0" size="1" layer="51" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<circle x="0" y="0" radius="2.2" width="0.15" layer="49"/>
<text x="0" y="3.2" size="1" layer="25" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<text x="0" y="-3.2" size="1" layer="27" font="vector" ratio="12" rot="R0" align="center">&gt;VALUE</text>
</package>
<package name="PinHeader_1x08_P2.54mm_Vertical">
<description>Through hole straight pin header, 1x08, 2.54mm pitch, single row</description>
<pad name="1" x="0" y="0" drill="1" diameter="1.7" shape="square" rot="R0"/>
<pad name="2" x="0" y="-2.54" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="3" x="0" y="-5.08" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="4" x="0" y="-7.62" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="5" x="0" y="-10.16" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="6" x="0" y="-12.7" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="7" x="0" y="-15.24" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="8" x="0" y="-17.78" drill="1" diameter="1.7" shape="round" rot="R0"/>
<text x="0" y="-8.89" size="1" layer="51" font="vector" ratio="12" rot="R90" align="center">&gt;NAME</text>
<wire x1="-1.33" y1="1.33" x2="0" y2="1.33" width="0.12" layer="21"/>
<wire x1="-1.33" y1="0" x2="-1.33" y2="1.33" width="0.12" layer="21"/>
<wire x1="-1.33" y1="-1.27" x2="-1.33" y2="-19.11" width="0.12" layer="21"/>
<wire x1="-1.33" y1="-1.27" x2="1.33" y2="-1.27" width="0.12" layer="21"/>
<wire x1="-1.33" y1="-19.11" x2="1.33" y2="-19.11" width="0.12" layer="21"/>
<wire x1="1.33" y1="-1.27" x2="1.33" y2="-19.11" width="0.12" layer="21"/>
<wire x1="-1.27" y1="0.635" x2="-0.635" y2="1.27" width="0.1" layer="51"/>
<wire x1="-1.27" y1="-19.05" x2="-1.27" y2="0.635" width="0.1" layer="51"/>
<wire x1="-0.635" y1="1.27" x2="1.27" y2="1.27" width="0.1" layer="51"/>
<wire x1="1.27" y1="1.27" x2="1.27" y2="-19.05" width="0.1" layer="51"/>
<wire x1="1.27" y1="-19.05" x2="-1.27" y2="-19.05" width="0.1" layer="51"/>
<text x="0" y="2.33" size="1" layer="25" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<text x="0" y="-20.11" size="1" layer="27" font="vector" ratio="12" rot="R0" align="center">&gt;VALUE</text>
</package>
<package name="RotaryEncoder_EC11_Switch_NPTH">
<description>EC11-size rotary encoder with switch (Alps EC11E, Bourns PEC11R), vertical, origin at the shaft, unplated slots for the mounting lugs</description>
<pad name="A" x="-7.5" y="2.5" drill="1" diameter="2" shape="square" rot="R0"/>
<pad name="C" x="-7.5" y="0" drill="1" diameter="2" shape="round" rot="R0"/>
<pad name="B" x="-7.5" y="-2.5" drill="1" diameter="2" shape="round" rot="R0"/>
<pad name="S2" x="7" y="2.5" drill="1" diameter="2" shape="round" rot="R0"/>
<pad name="S1" x="7" y="-2.5" drill="1" diameter="2" shape="round" rot="R0"/>
<hole x="0" y="5.6" drill="1.5"/>
<wire x1="-0.65" y1="6.35" x2="0.65" y2="6.35" width="0" layer="46"/>
<wire x1="0.65" y1="6.35" x2="0.65" y2="4.85" width="0" layer="46" curve="-180"/>
<wire x1="0.65" y1="4.85" x2="-0.65" y2="4.85" width="0" layer="46"/>
<wire x1="-0.65" y1="4.85" x2="-0.65" y2="6.35" width="0" layer="46" curve="-180"/>
<hole x="0" y="-5.6" drill="1.5"/>
<wire x1="-0.65" y1="-4.85" x2="0.65" y2="-4.85" width="0" layer="46"/>
<wire x1="0.65" y1="-4.85" x2="0.65" y2="-6.35" width="0" layer="46" curve="-180"/>
<wire x1="0.65" y1="-6.35" x2="-0.65" y2="-6.35" width="0" layer="46"/>
<wire x1="-0.65" y1="-6.35" x2="-0.65" y2="-4.85" width="0" layer="46" curve="-180"/>
<wire x1="-6" y1="5.8" x2="6" y2="5.8" width="0.12" layer="51"/>
<wire x1="6" y1="5.8" x2="6" y2="-5.8" width="0.12" layer="51"/>
<wire x1="6" y1="-5.8" x2="-6" y2="-5.8" width="0.12" layer="51"/>
<wire x1="-6" y1="-5.8" x2="-6" y2="5.8" width="0.12" layer="51"/>
<circle x="0" y="0" radius="3" width="0.12" layer="51"/>
<wire x1="-6.1" y1="4.3" x2="-6.1" y2="5.9" width="0.12" layer="21"/>
<wire x1="-6.1" y1="5.9" x2="-2" y2="5.9" width="0.12" layer="21"/>
<wire x1="2" y1="5.9" x2="6.1" y2="5.9" width="0.12" layer="21"/>
<wire x1="6.1" y1="5.9" x2="6.1" y2="3.9" width="0.12" layer="21"/>
<wire x1="6.1" y1="-3.9" x2="6.1" y2="-5.9" width="0.12" layer="21"/>
<wire x1="6.1" y1="-5.9" x2="2" y2="-5.9" width="0.12" layer="21"/>
<wire x1="-2" y1="-5.9" x2="-6.1" y2="-5.9" width="0.12" layer="21"/>
<wire x1="-6.1" y1="-5.9" x2="-6.1" y2="-4.3" width="0.12" layer="21"/>
<circle x="0" y="0" radius="3" width="0.12" layer="21"/>
<text x="0" y="8" size="1" layer="25" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<text x="0" y="-8" size="1" layer="27" font="vector" ratio="12" rot="R0" align="center">&gt;VALUE</text>
</package>
<package name="SW_Kailh_MX_Hotswap">
<description>Kailh MX hot-swap socket CPG151101S11, drawn from the socket side: place on the BOTTOM layer, switch centre at the origin, switch pins toward -y</description>
<hole x="0" y="0" drill="4"/>
<hole x="-5.08" y="0" drill="1.75"/>
<hole x="5.08" y="0" drill="1.75"/>
<hole x="3.81" y="2.54" drill="3.05"/>
<hole x="-2.54" y="5.08" drill="3.05"/>
<smd name="1" x="7.085" y="2.54" dx="2.55" dy="2.5" layer="1" roundness="20" rot="R0"/>
<smd name="2" x="-5.842" y="5.08" dx="2.55" dy="2.5" layer="1" roundness="20" rot="R0"/>
<wire x1="4" y1="6.8" x2="-4.8" y2="6.8" width="0.12" layer="51"/>
<wire x1="-4.8" y1="6.8" x2="-4.8" y2="2.8" width="0.12" layer="51"/>
<wire x1="-4.8" y1="2.8" x2="0.3" y2="2.8" width="0.12" layer="51"/>
<wire x1="0.3" y1="2.8" x2="2.3" y2="0.8" width="0.12" layer="51" curve="-89.9973"/>
<wire x1="2.3" y1="0.8" x2="6" y2="0.8" width="0.12" layer="51"/>
<wire x1="6" y1="0.8" x2="6" y2="4.8" width="0.12" layer="51"/>
<wire x1="4" y1="6.8" x2="6" y2="4.8" width="0.12" layer="51" curve="-89.9973"/>
<wire x1="4.1" y1="6.9" x2="-1" y2="6.9" width="0.12" layer="21"/>
<wire x1="0.2" y1="2.7" x2="-4.9" y2="2.7" width="0.12" layer="21"/>
<wire x1="6.1" y1="0.7" x2="6.1" y2="4.8" width="0.12" layer="21"/>
<wire x1="-7" y1="7" x2="7" y2="7" width="0.1" layer="52"/>
<wire x1="7" y1="7" x2="7" y2="-7" width="0.1" layer="52"/>
<wire x1="7" y1="-7" x2="-7" y2="-7" width="0.1" layer="52"/>
<wire x1="-7" y1="-7" x2="-7" y2="7" width="0.1" layer="52"/>
<text x="0" y="8.2" size="1" layer="25" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<text x="0" y="-8.2" size="1" layer="27" font="vector" ratio="12" rot="R0" align="center">&gt;VALUE</text>
</package>
<package name="SW_Push_1P1T_XKB_TS-1187A">
<description>XKB TS-1187A 5.1 x 5.1 mm SMD tactile switch, 4 gull-wing pads. Pads 1, 2 are one contact, 3, 4 the other</description>
<smd name="1" x="-3" y="1.875" dx="1" dy="0.75" layer="1" roundness="0" rot="R0"/>
<smd name="2" x="3" y="1.875" dx="1" dy="0.75" layer="1" roundness="0" rot="R0"/>
<smd name="3" x="-3" y="-1.875" dx="1" dy="0.75" layer="1" roundness="0" rot="R0"/>
<smd name="4" x="3" y="-1.875" dx="1" dy="0.75" layer="1" roundness="0" rot="R0"/>
<text x="0" y="3.75" size="1" layer="51" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<wire x1="-2.75" y1="1" x2="-2.75" y2="-1" width="0.12" layer="21"/>
<wire x1="-1.75" y1="2.3" x2="-1.3" y2="2.75" width="0.12" layer="21"/>
<wire x1="-1.75" y1="-2.3" x2="-1.3" y2="-2.75" width="0.12" layer="21"/>
<wire x1="-1.3" y1="2.75" x2="1.3" y2="2.75" width="0.12" layer="21"/>
<wire x1="-1.3" y1="-2.75" x2="1.3" y2="-2.75" width="0.12" layer="21"/>
<wire x1="1.75" y1="2.3" x2="1.3" y2="2.75" width="0.12" layer="21"/>
<wire x1="1.75" y1="-2.3" x2="1.3" y2="-2.75" width="0.12" layer="21"/>
<wire x1="2.75" y1="1" x2="2.75" y2="-1" width="0.12" layer="21"/>
<wire x1="-2.9" y1="2.1" x2="-2.9" y2="1.6" width="0.1" layer="51"/>
<wire x1="-2.9" y1="-2.1" x2="-2.9" y2="-1.6" width="0.1" layer="51"/>
<wire x1="-2.4" y1="1.4" x2="-1.4" y2="2.4" width="0.1" layer="51"/>
<wire x1="-2.4" y1="1.25" x2="-2.4" y2="1.4" width="0.1" layer="51"/>
<wire x1="-2.4" y1="-1.4" x2="-2.4" y2="-1.25" width="0.1" layer="51"/>
<wire x1="-1.4" y1="2.4" x2="-1.25" y2="2.4" width="0.1" layer="51"/>
<wire x1="-1.4" y1="-2.4" x2="-2.4" y2="-1.4" width="0.1" layer="51"/>
<wire x1="-1.25" y1="-2.4" x2="-1.4" y2="-2.4" width="0.1" layer="51"/>
<wire x1="1.25" y1="2.4" x2="1.4" y2="2.4" width="0.1" layer="51"/>
<wire x1="1.4" y1="2.4" x2="2.4" y2="1.4" width="0.1" layer="51"/>
<wire x1="1.4" y1="-2.4" x2="1.25" y2="-2.4" width="0.1" layer="51"/>
<wire x1="2.4" y1="1.4" x2="2.4" y2="1.25" width="0.1" layer="51"/>
<wire x1="2.4" y1="-1.25" x2="2.4" y2="-1.4" width="0.1" layer="51"/>
<wire x1="2.4" y1="-1.4" x2="1.4" y2="-2.4" width="0.1" layer="51"/>
<wire x1="2.9" y1="2.1" x2="2.9" y2="1.6" width="0.1" layer="51"/>
<wire x1="2.9" y1="-2.1" x2="2.9" y2="-1.6" width="0.1" layer="51"/>
<circle x="0" y="0" radius="1" width="0.1" layer="51"/>
<polygon width="0.1" layer="51"><vertex x="-1.7" y="2.1"/><vertex x="-2.2" y="1.6"/><vertex x="-3.25" y="1.6"/><vertex x="-3.25" y="2.1"/></polygon>
<polygon width="0.1" layer="51"><vertex x="-1.7" y="-2.1"/><vertex x="-2.2" y="-1.6"/><vertex x="-3.25" y="-1.6"/><vertex x="-3.25" y="-2.1"/></polygon>
<polygon width="0.1" layer="51"><vertex x="1.7" y="2.1"/><vertex x="2.2" y="1.6"/><vertex x="3.25" y="1.6"/><vertex x="3.25" y="2.1"/></polygon>
<polygon width="0.1" layer="51"><vertex x="1.7" y="-2.1"/><vertex x="2.2" y="-1.6"/><vertex x="3.25" y="-1.6"/><vertex x="3.25" y="-2.1"/></polygon>
<polygon width="0.1" layer="51"><vertex x="0.85" y="1.85"/><vertex x="1.85" y="0.85"/><vertex x="1.85" y="-0.85"/><vertex x="0.85" y="-1.85"/><vertex x="-0.85" y="-1.85"/><vertex x="-1.85" y="-0.85"/><vertex x="-1.85" y="0.85"/><vertex x="-0.85" y="1.85"/></polygon>
<polygon width="0.1" layer="51"><vertex x="-1.25" y="2.55"/><vertex x="1.25" y="2.55"/><vertex x="1.25" y="1.975"/><vertex x="1.575" y="1.975"/><vertex x="1.975" y="1.575"/><vertex x="1.975" y="1.25"/><vertex x="2.55" y="1.25"/><vertex x="2.55" y="-1.25"/><vertex x="1.975" y="-1.25"/><vertex x="1.975" y="-1.575"/><vertex x="1.575" y="-1.975"/><vertex x="1.25" y="-1.975"/><vertex x="1.25" y="-2.55"/><vertex x="-1.25" y="-2.55"/><vertex x="-1.25" y="-1.975"/><vertex x="-1.575" y="-1.975"/><vertex x="-1.975" y="-1.575"/><vertex x="-1.975" y="-1.25"/><vertex x="-2.55" y="-1.25"/><vertex x="-2.55" y="1.25"/><vertex x="-1.975" y="1.25"/><vertex x="-1.975" y="1.575"/><vertex x="-1.575" y="1.975"/><vertex x="-1.25" y="1.975"/></polygon>
<text x="0" y="3.75" size="1" layer="25" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<text x="0" y="-3.75" size="1" layer="27" font="vector" ratio="12" rot="R0" align="center">&gt;VALUE</text>
</package>
<package name="SW_Slide_SPDT_Angled_CK_OS102011MA1Q">
<description>CuK miniature slide switch, OS series, SPDT, right angle, http://www.ckswitches.com/media/1428/os.pdf</description>
<pad name="1" x="0" y="0" drill="0.9" diameter="1.5" shape="square" rot="R0"/>
<pad name="2" x="2" y="0" drill="0.9" diameter="1.5" shape="round" rot="R0"/>
<pad name="3" x="4" y="0" drill="0.9" diameter="1.5" shape="round" rot="R0"/>
<pad name="MP1" x="-2.1" y="0" drill="1.5" diameter="2.2" shape="round" rot="R0"/>
<pad name="MP2" x="6.1" y="0" drill="1.5" diameter="2.2" shape="round" rot="R0"/>
<text x="2.3" y="-1.7" size="0.5" layer="51" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<wire x1="-2.3" y1="2.3" x2="6.3" y2="2.3" width="0.12" layer="21"/>
<wire x1="-2.3" y1="-2.3" x2="-0.1" y2="-2.3" width="0.12" layer="21"/>
<wire x1="4" y1="-2.3" x2="6.3" y2="-2.3" width="0.12" layer="21"/>
<wire x1="-2.3" y1="2.2" x2="-2.3" y2="-2.2" width="0.1" layer="51"/>
<wire x1="-2.3" y1="2.2" x2="6.3" y2="2.2" width="0.1" layer="51"/>
<wire x1="-2.3" y1="-2.2" x2="6.3" y2="-2.2" width="0.1" layer="51"/>
<wire x1="0" y1="-6.2" x2="0" y2="-2.2" width="0.1" layer="51"/>
<wire x1="2" y1="-2.2" x2="2" y2="-6.2" width="0.1" layer="51"/>
<wire x1="2" y1="-6.2" x2="0" y2="-6.2" width="0.1" layer="51"/>
<wire x1="6.3" y1="-2.2" x2="6.3" y2="2.2" width="0.1" layer="51"/>
<text x="1.4" y="3.6" size="1" layer="25" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<text x="1.7" y="-7.7" size="1" layer="27" font="vector" ratio="12" rot="R0" align="center">&gt;VALUE</text>
</package>
<package name="SuperMini_nRF52840">
<description>SuperMini nRF52840 / nice!nano v2, Pro Micro 24-pin, 2.54 mm, rows 15.24 mm. Module outline 18 x 33 mm, USB-C at the top edge</description>
<pad name="1" x="-7.62" y="13.97" drill="1" diameter="1.7" shape="square" rot="R0"/>
<pad name="24" x="7.62" y="13.97" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="2" x="-7.62" y="11.43" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="23" x="7.62" y="11.43" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="3" x="-7.62" y="8.89" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="22" x="7.62" y="8.89" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="4" x="-7.62" y="6.35" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="21" x="7.62" y="6.35" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="5" x="-7.62" y="3.81" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="20" x="7.62" y="3.81" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="6" x="-7.62" y="1.27" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="19" x="7.62" y="1.27" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="7" x="-7.62" y="-1.27" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="18" x="7.62" y="-1.27" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="8" x="-7.62" y="-3.81" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="17" x="7.62" y="-3.81" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="9" x="-7.62" y="-6.35" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="16" x="7.62" y="-6.35" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="10" x="-7.62" y="-8.89" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="15" x="7.62" y="-8.89" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="11" x="-7.62" y="-11.43" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="14" x="7.62" y="-11.43" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="12" x="-7.62" y="-13.97" drill="1" diameter="1.7" shape="round" rot="R0"/>
<pad name="13" x="7.62" y="-13.97" drill="1" diameter="1.7" shape="round" rot="R0"/>
<wire x1="-9" y1="16.5" x2="9" y2="16.5" width="0.1" layer="51"/>
<wire x1="9" y1="16.5" x2="9" y2="-16.5" width="0.1" layer="51"/>
<wire x1="9" y1="-16.5" x2="-9" y2="-16.5" width="0.1" layer="51"/>
<wire x1="-9" y1="-16.5" x2="-9" y2="16.5" width="0.1" layer="51"/>
<wire x1="-4.47" y1="17.6" x2="4.47" y2="17.6" width="0.1" layer="51"/>
<wire x1="4.47" y1="17.6" x2="4.47" y2="11.25" width="0.1" layer="51"/>
<wire x1="4.47" y1="11.25" x2="-4.47" y2="11.25" width="0.1" layer="51"/>
<wire x1="-4.47" y1="11.25" x2="-4.47" y2="17.6" width="0.1" layer="51"/>
<text x="0" y="14.3" size="1" layer="51" font="vector" ratio="12" rot="R0" align="center">USB-C</text>
<wire x1="-9.12" y1="16.62" x2="9.12" y2="16.62" width="0.12" layer="21"/>
<wire x1="9.12" y1="16.62" x2="9.12" y2="-16.62" width="0.12" layer="21"/>
<wire x1="9.12" y1="-16.62" x2="-9.12" y2="-16.62" width="0.12" layer="21"/>
<wire x1="-9.12" y1="-16.62" x2="-9.12" y2="16.62" width="0.12" layer="21"/>
<wire x1="-9.12" y1="15.3" x2="-10.2" y2="14.7" width="0.12" layer="21"/>
<wire x1="-10.2" y1="14.7" x2="-10.2" y2="15.9" width="0.12" layer="21"/>
<wire x1="-10.2" y1="15.9" x2="-9.12" y2="15.3" width="0.12" layer="21"/>
<text x="0" y="19" size="1" layer="25" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<text x="0" y="-18.2" size="1" layer="27" font="vector" ratio="12" rot="R0" align="center">&gt;VALUE</text>
</package>
<package name="TestPoint_Pad_D1.5mm">
<description>SMD pad as test Point, diameter 1.5mm</description>
<smd name="1" x="0" y="0" dx="1.5" dy="1.5" layer="1" roundness="100" rot="R0" cream="no"/>
<text x="0" y="1.65" size="1" layer="51" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<circle x="0" y="0" radius="0.95" width="0.12" layer="21"/>
<text x="0" y="1.648" size="1" layer="25" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<text x="0" y="-1.75" size="1" layer="27" font="vector" ratio="12" rot="R0" align="center">&gt;VALUE</text>
</package>
</packages>
<symbols>
<symbol name="C">
<description>Capacitor</description>
<wire x1="0" y1="2.54" x2="0" y2="0.635" width="0.254" layer="94"/>
<wire x1="0" y1="-2.54" x2="0" y2="-0.635" width="0.254" layer="94"/>
<rectangle x1="-1.524" y1="0.508" x2="1.524" y2="0.762" layer="94"/>
<rectangle x1="-1.524" y1="-0.762" x2="1.524" y2="-0.508" layer="94"/>
<pin name="1" x="0" y="5.08" visible="off" length="short" direction="pas" rot="R270"/>
<pin name="2" x="0" y="-5.08" visible="off" length="short" direction="pas" rot="R90"/>
<text x="2.032" y="0.762" size="1.778" layer="95" font="vector" ratio="12" rot="R0" align="center-left">&gt;NAME</text>
<text x="2.032" y="-1.524" size="1.778" layer="96" font="vector" ratio="12" rot="R0" align="center-left">&gt;VALUE</text>
</symbol>
<symbol name="Conn_01x02">
<description>Connector or wire pads, 1 x 2</description>
<wire x1="-1.27" y1="-1.27" x2="1.27" y2="-1.27" width="0.254" layer="94"/>
<wire x1="1.27" y1="-1.27" x2="1.27" y2="3.81" width="0.254" layer="94"/>
<wire x1="1.27" y1="3.81" x2="-1.27" y2="3.81" width="0.254" layer="94"/>
<wire x1="-1.27" y1="3.81" x2="-1.27" y2="-1.27" width="0.254" layer="94"/>
<rectangle x1="-1.27" y1="2.413" x2="0" y2="2.667" layer="94"/>
<rectangle x1="-1.27" y1="-0.127" x2="0" y2="0.127" layer="94"/>
<pin name="1" x="-5.08" y="2.54" visible="pad" length="short" direction="pas" rot="R0"/>
<pin name="2" x="-5.08" y="0" visible="pad" length="short" direction="pas" rot="R0"/>
<text x="-1.27" y="4.572" size="1.778" layer="95" font="vector" ratio="12" rot="R0" align="center-left">&gt;NAME</text>
<text x="-1.27" y="-2.794" size="1.778" layer="96" font="vector" ratio="12" rot="R0" align="center-left">&gt;VALUE</text>
</symbol>
<symbol name="Conn_01x08">
<description>Connector or wire pads, 1 x 8</description>
<wire x1="-1.27" y1="-8.89" x2="1.27" y2="-8.89" width="0.254" layer="94"/>
<wire x1="1.27" y1="-8.89" x2="1.27" y2="11.43" width="0.254" layer="94"/>
<wire x1="1.27" y1="11.43" x2="-1.27" y2="11.43" width="0.254" layer="94"/>
<wire x1="-1.27" y1="11.43" x2="-1.27" y2="-8.89" width="0.254" layer="94"/>
<rectangle x1="-1.27" y1="10.033" x2="0" y2="10.287" layer="94"/>
<rectangle x1="-1.27" y1="7.493" x2="0" y2="7.747" layer="94"/>
<rectangle x1="-1.27" y1="4.953" x2="0" y2="5.207" layer="94"/>
<rectangle x1="-1.27" y1="2.413" x2="0" y2="2.667" layer="94"/>
<rectangle x1="-1.27" y1="-0.127" x2="0" y2="0.127" layer="94"/>
<rectangle x1="-1.27" y1="-2.667" x2="0" y2="-2.413" layer="94"/>
<rectangle x1="-1.27" y1="-5.207" x2="0" y2="-4.953" layer="94"/>
<rectangle x1="-1.27" y1="-7.747" x2="0" y2="-7.493" layer="94"/>
<pin name="1" x="-5.08" y="10.16" visible="pad" length="short" direction="pas" rot="R0"/>
<pin name="2" x="-5.08" y="7.62" visible="pad" length="short" direction="pas" rot="R0"/>
<pin name="3" x="-5.08" y="5.08" visible="pad" length="short" direction="pas" rot="R0"/>
<pin name="4" x="-5.08" y="2.54" visible="pad" length="short" direction="pas" rot="R0"/>
<pin name="5" x="-5.08" y="0" visible="pad" length="short" direction="pas" rot="R0"/>
<pin name="6" x="-5.08" y="-2.54" visible="pad" length="short" direction="pas" rot="R0"/>
<pin name="7" x="-5.08" y="-5.08" visible="pad" length="short" direction="pas" rot="R0"/>
<pin name="8" x="-5.08" y="-7.62" visible="pad" length="short" direction="pas" rot="R0"/>
<text x="-1.27" y="12.192" size="1.778" layer="95" font="vector" ratio="12" rot="R0" align="center-left">&gt;NAME</text>
<text x="-1.27" y="-10.414" size="1.778" layer="96" font="vector" ratio="12" rot="R0" align="center-left">&gt;VALUE</text>
</symbol>
<symbol name="D">
<description>Diode</description>
<wire x1="-2.54" y1="0" x2="2.54" y2="0" width="0.254" layer="94"/>
<polygon width="0.127" layer="94"><vertex x="-1.27" y="1.27"/><vertex x="-1.27" y="-1.27"/><vertex x="1.27" y="0"/></polygon>
<wire x1="1.27" y1="1.27" x2="1.27" y2="-1.27" width="0.254" layer="94"/>
<pin name="K" x="5.08" y="0" visible="off" length="short" direction="pas" rot="R180"/>
<pin name="A" x="-5.08" y="0" visible="off" length="short" direction="pas" rot="R0"/>
<text x="0" y="2.286" size="1.778" layer="95" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<text x="0" y="-2.794" size="1.778" layer="96" font="vector" ratio="12" rot="R0" align="center">&gt;VALUE</text>
</symbol>
<symbol name="MountingHole">
<description>Mounting hole, no connection</description>
<circle x="0" y="0" radius="1.27" width="0.254" layer="94"/>
<circle x="0" y="0" radius="2.032" width="0.254" layer="94"/>
<text x="3.048" y="0.508" size="1.778" layer="95" font="vector" ratio="12" rot="R0" align="center-left">&gt;NAME</text>
<text x="3.048" y="-1.27" size="1.778" layer="96" font="vector" ratio="12" rot="R0" align="center-left">&gt;VALUE</text>
</symbol>
<symbol name="RotaryEncoder_Switch">
<description>Rotary encoder with push switch: A, B, C = common; S1, S2 = switch</description>
<wire x1="-5.08" y1="-5.08" x2="5.08" y2="-5.08" width="0.254" layer="94"/>
<wire x1="5.08" y1="-5.08" x2="5.08" y2="5.08" width="0.254" layer="94"/>
<wire x1="5.08" y1="5.08" x2="-5.08" y2="5.08" width="0.254" layer="94"/>
<wire x1="-5.08" y1="5.08" x2="-5.08" y2="-5.08" width="0.254" layer="94"/>
<circle x="0" y="0" radius="1.778" width="0.254" layer="94"/>
<wire x1="-0.635" y1="1.778" x2="0.635" y2="2.286" width="0.254" layer="94"/>
<wire x1="-0.635" y1="-1.778" x2="0.635" y2="-2.286" width="0.254" layer="94"/>
<pin name="A" x="-10.16" y="2.54" visible="both" length="middle" direction="pas" rot="R0"/>
<pin name="C" x="-10.16" y="0" visible="both" length="middle" direction="pas" rot="R0"/>
<pin name="B" x="-10.16" y="-2.54" visible="both" length="middle" direction="pas" rot="R0"/>
<pin name="S1" x="10.16" y="2.54" visible="both" length="middle" direction="pas" rot="R180"/>
<pin name="S2" x="10.16" y="-2.54" visible="both" length="middle" direction="pas" rot="R180"/>
<text x="-5.08" y="6.096" size="1.778" layer="95" font="vector" ratio="12" rot="R0" align="center-left">&gt;NAME</text>
<text x="-5.08" y="-6.858" size="1.778" layer="96" font="vector" ratio="12" rot="R0" align="center-left">&gt;VALUE</text>
</symbol>
<symbol name="SW_Key">
<description>Key switch (MX socket)</description>
<wire x1="-2.54" y1="0" x2="-1.524" y2="0" width="0.254" layer="94"/>
<wire x1="2.54" y1="0" x2="1.524" y2="0" width="0.254" layer="94"/>
<circle x="-1.27" y="0" radius="0.254" width="0.254" layer="94"/>
<circle x="1.27" y="0" radius="0.254" width="0.254" layer="94"/>
<wire x1="-1.27" y1="0.508" x2="1.524" y2="1.524" width="0.254" layer="94"/>
<wire x1="0" y1="1.016" x2="0" y2="2.032" width="0.254" layer="94"/>
<wire x1="-0.762" y1="2.032" x2="0.762" y2="2.032" width="0.254" layer="94"/>
<pin name="1" x="-5.08" y="0" visible="off" length="short" direction="pas" rot="R0"/>
<pin name="2" x="5.08" y="0" visible="off" length="short" direction="pas" rot="R180"/>
<text x="0" y="3.048" size="1.778" layer="95" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<text x="0" y="-2.032" size="1.778" layer="96" font="vector" ratio="12" rot="R0" align="center">&gt;VALUE</text>
</symbol>
<symbol name="SW_Push_4pin">
<description>Tactile switch, 4 pads: 1 and 2 are one side, 3 and 4 the other</description>
<wire x1="-2.54" y1="2.54" x2="-2.54" y2="-2.54" width="0.254" layer="94"/>
<wire x1="2.54" y1="2.54" x2="2.54" y2="-2.54" width="0.254" layer="94"/>
<wire x1="-2.54" y1="0" x2="-1.524" y2="0" width="0.254" layer="94"/>
<wire x1="2.54" y1="0" x2="1.524" y2="0" width="0.254" layer="94"/>
<circle x="-1.27" y="0" radius="0.254" width="0.254" layer="94"/>
<circle x="1.27" y="0" radius="0.254" width="0.254" layer="94"/>
<wire x1="-1.524" y1="0.762" x2="1.524" y2="0.762" width="0.254" layer="94"/>
<wire x1="0" y1="0.762" x2="0" y2="1.778" width="0.254" layer="94"/>
<wire x1="-0.762" y1="1.778" x2="0.762" y2="1.778" width="0.254" layer="94"/>
<pin name="1" x="-5.08" y="2.54" visible="pad" length="short" direction="pas" rot="R0"/>
<pin name="2" x="-5.08" y="-2.54" visible="pad" length="short" direction="pas" rot="R0"/>
<pin name="3" x="5.08" y="2.54" visible="pad" length="short" direction="pas" rot="R180"/>
<pin name="4" x="5.08" y="-2.54" visible="pad" length="short" direction="pas" rot="R180"/>
<text x="0" y="3.302" size="1.778" layer="95" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<text x="0" y="-3.81" size="1.778" layer="96" font="vector" ratio="12" rot="R0" align="center">&gt;VALUE</text>
</symbol>
<symbol name="SW_SPDT">
<description>Slide switch, SPDT: pin 2 is common</description>
<wire x1="-2.54" y1="0" x2="-1.524" y2="0" width="0.254" layer="94"/>
<circle x="-1.27" y="0" radius="0.254" width="0.254" layer="94"/>
<wire x1="2.54" y1="2.54" x2="1.524" y2="2.54" width="0.254" layer="94"/>
<circle x="1.27" y="2.54" radius="0.254" width="0.254" layer="94"/>
<wire x1="2.54" y1="-2.54" x2="1.524" y2="-2.54" width="0.254" layer="94"/>
<circle x="1.27" y="-2.54" radius="0.254" width="0.254" layer="94"/>
<wire x1="-1.016" y1="0.254" x2="1.27" y2="2.032" width="0.254" layer="94"/>
<pin name="COM" x="-5.08" y="0" visible="pad" length="short" direction="pas" rot="R0"/>
<pin name="1" x="5.08" y="2.54" visible="pad" length="short" direction="pas" rot="R180"/>
<pin name="3" x="5.08" y="-2.54" visible="pad" length="short" direction="pas" rot="R180"/>
<text x="0" y="4.064" size="1.778" layer="95" font="vector" ratio="12" rot="R0" align="center">&gt;NAME</text>
<text x="0" y="-4.318" size="1.778" layer="96" font="vector" ratio="12" rot="R0" align="center">&gt;VALUE</text>
</symbol>
<symbol name="SuperMini_nRF52840">
<description>SuperMini nRF52840 (nice!nano v2 pinout), Pro Micro 24-pin</description>
<wire x1="-7.62" y1="-15.24" x2="7.62" y2="-15.24" width="0.254" layer="94"/>
<wire x1="7.62" y1="-15.24" x2="7.62" y2="17.78" width="0.254" layer="94"/>
<wire x1="7.62" y1="17.78" x2="-7.62" y2="17.78" width="0.254" layer="94"/>
<wire x1="-7.62" y1="17.78" x2="-7.62" y2="-15.24" width="0.254" layer="94"/>
<text x="0" y="16.51" size="1.27" layer="94" font="vector" ratio="12" rot="R0" align="center">USB-C</text>
<pin name="P0.06" x="-12.7" y="15.24" visible="both" length="middle" direction="pas" rot="R0"/>
<pin name="P0.08" x="-12.7" y="12.7" visible="both" length="middle" direction="pas" rot="R0"/>
<pin name="GND@3" x="-12.7" y="10.16" visible="both" length="middle" direction="pas" rot="R0"/>
<pin name="GND@4" x="-12.7" y="7.62" visible="both" length="middle" direction="pas" rot="R0"/>
<pin name="P0.17" x="-12.7" y="5.08" visible="both" length="middle" direction="pas" rot="R0"/>
<pin name="P0.20" x="-12.7" y="2.54" visible="both" length="middle" direction="pas" rot="R0"/>
<pin name="P0.22" x="-12.7" y="0" visible="both" length="middle" direction="pas" rot="R0"/>
<pin name="P0.24" x="-12.7" y="-2.54" visible="both" length="middle" direction="pas" rot="R0"/>
<pin name="P1.00" x="-12.7" y="-5.08" visible="both" length="middle" direction="pas" rot="R0"/>
<pin name="P0.11" x="-12.7" y="-7.62" visible="both" length="middle" direction="pas" rot="R0"/>
<pin name="P1.04" x="-12.7" y="-10.16" visible="both" length="middle" direction="pas" rot="R0"/>
<pin name="P1.06" x="-12.7" y="-12.7" visible="both" length="middle" direction="pas" rot="R0"/>
<pin name="BAT+" x="12.7" y="15.24" visible="both" length="middle" direction="pas" rot="R180"/>
<pin name="GND@23" x="12.7" y="12.7" visible="both" length="middle" direction="pas" rot="R180"/>
<pin name="RST" x="12.7" y="10.16" visible="both" length="middle" direction="pas" rot="R180"/>
<pin name="VCC" x="12.7" y="7.62" visible="both" length="middle" direction="pas" rot="R180"/>
<pin name="P0.31" x="12.7" y="5.08" visible="both" length="middle" direction="pas" rot="R180"/>
<pin name="P0.29" x="12.7" y="2.54" visible="both" length="middle" direction="pas" rot="R180"/>
<pin name="P0.02" x="12.7" y="0" visible="both" length="middle" direction="pas" rot="R180"/>
<pin name="P1.15" x="12.7" y="-2.54" visible="both" length="middle" direction="pas" rot="R180"/>
<pin name="P1.13" x="12.7" y="-5.08" visible="both" length="middle" direction="pas" rot="R180"/>
<pin name="P1.11" x="12.7" y="-7.62" visible="both" length="middle" direction="pas" rot="R180"/>
<pin name="P0.10" x="12.7" y="-10.16" visible="both" length="middle" direction="pas" rot="R180"/>
<pin name="P0.09" x="12.7" y="-12.7" visible="both" length="middle" direction="pas" rot="R180"/>
<text x="-7.62" y="18.796" size="1.778" layer="95" font="vector" ratio="12" rot="R0" align="center-left">&gt;NAME</text>
<text x="-7.62" y="-17.78" size="1.778" layer="96" font="vector" ratio="12" rot="R0" align="center-left">&gt;VALUE</text>
</symbol>
<symbol name="TestPoint">
<description>Test pad</description>
<circle x="0" y="3.302" radius="0.762" width="0.254" layer="94"/>
<pin name="1" x="0" y="0" visible="off" length="short" direction="pas" rot="R90"/>
<text x="1.524" y="3.81" size="1.778" layer="95" font="vector" ratio="12" rot="R0" align="center-left">&gt;NAME</text>
<text x="1.524" y="2.032" size="1.778" layer="96" font="vector" ratio="12" rot="R0" align="center-left">&gt;VALUE</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="C_10n_0805" prefix="C" uservalue="yes">
<description>Capacitor 10 nF 50 V X7R 0805</description>
<gates><gate name="G$1" symbol="C" x="0" y="0"/></gates>
<devices>
<device name="" package="C_0805_2012Metric">
<connects><connect gate="G$1" pin="1" pad="1"/><connect gate="G$1" pin="2" pad="2"/></connects>
<technologies><technology name=""><attribute name="MANUFACTURER" value="Samsung"/><attribute name="MPN" value="CL21B103KBANNNC"/><attribute name="LCSC" value="C1710"/><attribute name="DESCRIPTION" value="Capacitor 10 nF 50 V X7R 0805"/></technology></technologies>
</device>
</devices>
</deviceset>
<deviceset name="C_10u_0805" prefix="C" uservalue="yes">
<description>Capacitor 10 uF 25 V X5R 0805</description>
<gates><gate name="G$1" symbol="C" x="0" y="0"/></gates>
<devices>
<device name="" package="C_0805_2012Metric">
<connects><connect gate="G$1" pin="1" pad="1"/><connect gate="G$1" pin="2" pad="2"/></connects>
<technologies><technology name=""><attribute name="MANUFACTURER" value="Samsung"/><attribute name="MPN" value="CL21A106KAYNNNE"/><attribute name="LCSC" value="C15850"/><attribute name="DESCRIPTION" value="Capacitor 10 uF 25 V X5R 0805"/></technology></technologies>
</device>
</devices>
</deviceset>
<deviceset name="Conn_JST_PH_S2B_Horizontal" prefix="J" uservalue="yes">
<description>JST PH 2-pin header, side entry, through-hole (LiPo plug)</description>
<gates><gate name="G$1" symbol="Conn_01x02" x="0" y="0"/></gates>
<devices>
<device name="" package="JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal">
<connects><connect gate="G$1" pin="1" pad="1"/><connect gate="G$1" pin="2" pad="2"/></connects>
<technologies><technology name=""><attribute name="MANUFACTURER" value="JST"/><attribute name="MPN" value="S2B-PH-K-S(LF)(SN)"/><attribute name="LCSC" value="C173752"/><attribute name="DESCRIPTION" value="JST PH 2-pin header, side entry, through-hole (LiPo plug)"/></technology></technologies>
</device>
</devices>
</deviceset>
<deviceset name="Conn_Wire_Pads_1x08" prefix="J" uservalue="yes">
<description>8 plated holes, 2.54 mm, 1.0 mm drill: solder wires (or a 1x8 header)</description>
<gates><gate name="G$1" symbol="Conn_01x08" x="0" y="0"/></gates>
<devices>
<device name="" package="PinHeader_1x08_P2.54mm_Vertical">
<connects><connect gate="G$1" pin="1" pad="1"/><connect gate="G$1" pin="2" pad="2"/><connect gate="G$1" pin="3" pad="3"/><connect gate="G$1" pin="4" pad="4"/><connect gate="G$1" pin="5" pad="5"/><connect gate="G$1" pin="6" pad="6"/><connect gate="G$1" pin="7" pad="7"/><connect gate="G$1" pin="8" pad="8"/></connects>
<technologies><technology name=""><attribute name="DESCRIPTION" value="8 plated holes, 2.54 mm, 1.0 mm drill: solder wires (or a 1x8 header)"/></technology></technologies>
</device>
</devices>
</deviceset>
<deviceset name="D_1N4148W_SOD-123" prefix="D" uservalue="yes">
<description>Switching diode 100 V 150 mA, SOD-123</description>
<gates><gate name="G$1" symbol="D" x="0" y="0"/></gates>
<devices>
<device name="" package="D_SOD-123">
<connects><connect gate="G$1" pin="K" pad="1"/><connect gate="G$1" pin="A" pad="2"/></connects>
<technologies><technology name=""><attribute name="MANUFACTURER" value="ST(Semtech)"/><attribute name="MPN" value="1N4148W"/><attribute name="LCSC" value="C81598"/><attribute name="DESCRIPTION" value="Switching diode 100 V 150 mA, SOD-123"/></technology></technologies>
</device>
</devices>
</deviceset>
<deviceset name="Encoder_PEC11R-4220F-S0024" prefix="ENC" uservalue="yes">
<description>Rotary encoder, 24 detents / 24 pulses, push switch, 20 mm flatted shaft, EC11 size</description>
<gates><gate name="G$1" symbol="RotaryEncoder_Switch" x="0" y="0"/></gates>
<devices>
<device name="" package="RotaryEncoder_EC11_Switch_NPTH">
<connects><connect gate="G$1" pin="A" pad="A"/><connect gate="G$1" pin="C" pad="C"/><connect gate="G$1" pin="B" pad="B"/><connect gate="G$1" pin="S2" pad="S2"/><connect gate="G$1" pin="S1" pad="S1"/></connects>
<technologies><technology name=""><attribute name="MANUFACTURER" value="Bourns"/><attribute name="MPN" value="PEC11R-4220F-S0024"/><attribute name="LCSC" value="C143797"/><attribute name="DESCRIPTION" value="Rotary encoder, 24 detents / 24 pulses, push switch, 20 mm flatted shaft, EC11 size"/></technology></technologies>
</device>
</devices>
</deviceset>
<deviceset name="MountingHole_M2" prefix="H" uservalue="yes">
<description>Unplated 2.2 mm hole for an M2 screw</description>
<gates><gate name="G$1" symbol="MountingHole" x="0" y="0"/></gates>
<devices>
<device name="" package="MountingHole_2.2mm_M2">
<connects></connects>
<technologies><technology name=""><attribute name="DESCRIPTION" value="Unplated 2.2 mm hole for an M2 screw"/></technology></technologies>
</device>
</devices>
</deviceset>
<deviceset name="SW_Kailh_MX_Hotswap" prefix="SW" uservalue="yes">
<description>Kailh MX hot-swap socket for MX switches. Footprint goes on the bottom layer</description>
<gates><gate name="G$1" symbol="SW_Key" x="0" y="0"/></gates>
<devices>
<device name="" package="SW_Kailh_MX_Hotswap">
<connects><connect gate="G$1" pin="1" pad="1"/><connect gate="G$1" pin="2" pad="2"/></connects>
<technologies><technology name=""><attribute name="MANUFACTURER" value="Kailh"/><attribute name="MPN" value="CPG151101S11"/><attribute name="LCSC" value="C2803348"/><attribute name="DESCRIPTION" value="Kailh MX hot-swap socket for MX switches. Footprint goes on the bottom layer"/></technology></technologies>
</device>
</devices>
</deviceset>
<deviceset name="SW_Slide_OS102011MA1QN1" prefix="SW" uservalue="yes">
<description>Slide switch SPDT, right angle, through-hole, 4 mm actuator</description>
<gates><gate name="G$1" symbol="SW_SPDT" x="0" y="0"/></gates>
<devices>
<device name="" package="SW_Slide_SPDT_Angled_CK_OS102011MA1Q">
<connects><connect gate="G$1" pin="1" pad="1"/><connect gate="G$1" pin="COM" pad="2"/><connect gate="G$1" pin="3" pad="3"/></connects>
<technologies><technology name=""><attribute name="MANUFACTURER" value="C&amp;K"/><attribute name="MPN" value="OS102011MA1QN1"/><attribute name="LCSC" value="C226259"/><attribute name="DESCRIPTION" value="Slide switch SPDT, right angle, through-hole, 4 mm actuator"/></technology></technologies>
</device>
</devices>
</deviceset>
<deviceset name="SW_Tact_TS-1187A-B-A-B" prefix="SW" uservalue="yes">
<description>Tactile switch 5.1 x 5.1 x 1.5 mm, SMD gull-wing, 160 gf</description>
<gates><gate name="G$1" symbol="SW_Push_4pin" x="0" y="0"/></gates>
<devices>
<device name="" package="SW_Push_1P1T_XKB_TS-1187A">
<connects><connect gate="G$1" pin="1" pad="1"/><connect gate="G$1" pin="2" pad="2"/><connect gate="G$1" pin="3" pad="3"/><connect gate="G$1" pin="4" pad="4"/></connects>
<technologies><technology name=""><attribute name="MANUFACTURER" value="XKB Connection"/><attribute name="MPN" value="TS-1187A-B-A-B"/><attribute name="LCSC" value="C318884"/><attribute name="DESCRIPTION" value="Tactile switch 5.1 x 5.1 x 1.5 mm, SMD gull-wing, 160 gf"/></technology></technologies>
</device>
</devices>
</deviceset>
<deviceset name="SuperMini_nRF52840" prefix="U" uservalue="yes">
<description>nRF52840 module, nice!nano v2 pinout, LiPo charger, USB-C. Pro Micro 24-pin</description>
<gates><gate name="G$1" symbol="SuperMini_nRF52840" x="0" y="0"/></gates>
<devices>
<device name="" package="SuperMini_nRF52840">
<connects><connect gate="G$1" pin="P0.06" pad="1"/><connect gate="G$1" pin="BAT+" pad="24"/><connect gate="G$1" pin="P0.08" pad="2"/><connect gate="G$1" pin="GND@23" pad="23"/><connect gate="G$1" pin="GND@3" pad="3"/><connect gate="G$1" pin="RST" pad="22"/><connect gate="G$1" pin="GND@4" pad="4"/><connect gate="G$1" pin="VCC" pad="21"/><connect gate="G$1" pin="P0.17" pad="5"/><connect gate="G$1" pin="P0.31" pad="20"/><connect gate="G$1" pin="P0.20" pad="6"/><connect gate="G$1" pin="P0.29" pad="19"/><connect gate="G$1" pin="P0.22" pad="7"/><connect gate="G$1" pin="P0.02" pad="18"/><connect gate="G$1" pin="P0.24" pad="8"/><connect gate="G$1" pin="P1.15" pad="17"/><connect gate="G$1" pin="P1.00" pad="9"/><connect gate="G$1" pin="P1.13" pad="16"/><connect gate="G$1" pin="P0.11" pad="10"/><connect gate="G$1" pin="P1.11" pad="15"/><connect gate="G$1" pin="P1.04" pad="11"/><connect gate="G$1" pin="P0.10" pad="14"/><connect gate="G$1" pin="P1.06" pad="12"/><connect gate="G$1" pin="P0.09" pad="13"/></connects>
<technologies><technology name=""><attribute name="MANUFACTURER" value="generic (nice!nano v2 clone)"/><attribute name="MPN" value="SuperMini nRF52840"/><attribute name="DESCRIPTION" value="nRF52840 module, nice!nano v2 pinout, LiPo charger, USB-C. Pro Micro 24-pin"/></technology></technologies>
</device>
</devices>
</deviceset>
<deviceset name="TestPoint_Pad_1.5mm" prefix="TP" uservalue="yes">
<description>Test pad, 1.5 mm, no part fitted</description>
<gates><gate name="G$1" symbol="TestPoint" x="0" y="0"/></gates>
<devices>
<device name="" package="TestPoint_Pad_D1.5mm">
<connects><connect gate="G$1" pin="1" pad="1"/></connects>
<technologies><technology name=""><attribute name="DESCRIPTION" value="Test pad, 1.5 mm, no part fitted"/></technology></technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes/>
<variantdefs/>
<classes>
<class number="0" name="default" width="0.25" drill="0.3">
<clearance class="0" value="0.2"/>
</class>
<class number="1" name="power" width="0.4" drill="0.3">
<clearance class="1" value="0.2"/>
</class>
</classes>
<parts>
<part name="C1" library="JR" deviceset="C_10n_0805" device="" value="10nF"><attribute name="MANUFACTURER" value="Samsung"/><attribute name="MPN" value="CL21B103KBANNNC"/><attribute name="LCSC" value="C1710"/><attribute name="DESCRIPTION" value="Capacitor 10 nF 50 V X7R 0805"/></part>
<part name="C2" library="JR" deviceset="C_10n_0805" device="" value="10nF"><attribute name="MANUFACTURER" value="Samsung"/><attribute name="MPN" value="CL21B103KBANNNC"/><attribute name="LCSC" value="C1710"/><attribute name="DESCRIPTION" value="Capacitor 10 nF 50 V X7R 0805"/></part>
<part name="C3" library="JR" deviceset="C_10u_0805" device="" value="10uF"><attribute name="MANUFACTURER" value="Samsung"/><attribute name="MPN" value="CL21A106KAYNNNE"/><attribute name="LCSC" value="C15850"/><attribute name="DESCRIPTION" value="Capacitor 10 uF 25 V X5R 0805"/></part>
<part name="D1" library="JR" deviceset="D_1N4148W_SOD-123" device="" value="1N4148W"><attribute name="MANUFACTURER" value="ST(Semtech)"/><attribute name="MPN" value="1N4148W"/><attribute name="LCSC" value="C81598"/><attribute name="DESCRIPTION" value="Switching diode 100 V 150 mA, SOD-123"/></part>
<part name="D2" library="JR" deviceset="D_1N4148W_SOD-123" device="" value="1N4148W"><attribute name="MANUFACTURER" value="ST(Semtech)"/><attribute name="MPN" value="1N4148W"/><attribute name="LCSC" value="C81598"/><attribute name="DESCRIPTION" value="Switching diode 100 V 150 mA, SOD-123"/></part>
<part name="D3" library="JR" deviceset="D_1N4148W_SOD-123" device="" value="1N4148W"><attribute name="MANUFACTURER" value="ST(Semtech)"/><attribute name="MPN" value="1N4148W"/><attribute name="LCSC" value="C81598"/><attribute name="DESCRIPTION" value="Switching diode 100 V 150 mA, SOD-123"/></part>
<part name="D4" library="JR" deviceset="D_1N4148W_SOD-123" device="" value="1N4148W"><attribute name="MANUFACTURER" value="ST(Semtech)"/><attribute name="MPN" value="1N4148W"/><attribute name="LCSC" value="C81598"/><attribute name="DESCRIPTION" value="Switching diode 100 V 150 mA, SOD-123"/></part>
<part name="D5" library="JR" deviceset="D_1N4148W_SOD-123" device="" value="1N4148W"><attribute name="MANUFACTURER" value="ST(Semtech)"/><attribute name="MPN" value="1N4148W"/><attribute name="LCSC" value="C81598"/><attribute name="DESCRIPTION" value="Switching diode 100 V 150 mA, SOD-123"/></part>
<part name="D6" library="JR" deviceset="D_1N4148W_SOD-123" device="" value="1N4148W"><attribute name="MANUFACTURER" value="ST(Semtech)"/><attribute name="MPN" value="1N4148W"/><attribute name="LCSC" value="C81598"/><attribute name="DESCRIPTION" value="Switching diode 100 V 150 mA, SOD-123"/></part>
<part name="D7" library="JR" deviceset="D_1N4148W_SOD-123" device="" value="1N4148W"><attribute name="MANUFACTURER" value="ST(Semtech)"/><attribute name="MPN" value="1N4148W"/><attribute name="LCSC" value="C81598"/><attribute name="DESCRIPTION" value="Switching diode 100 V 150 mA, SOD-123"/></part>
<part name="D8" library="JR" deviceset="D_1N4148W_SOD-123" device="" value="1N4148W"><attribute name="MANUFACTURER" value="ST(Semtech)"/><attribute name="MPN" value="1N4148W"/><attribute name="LCSC" value="C81598"/><attribute name="DESCRIPTION" value="Switching diode 100 V 150 mA, SOD-123"/></part>
<part name="D9" library="JR" deviceset="D_1N4148W_SOD-123" device="" value="1N4148W"><attribute name="MANUFACTURER" value="ST(Semtech)"/><attribute name="MPN" value="1N4148W"/><attribute name="LCSC" value="C81598"/><attribute name="DESCRIPTION" value="Switching diode 100 V 150 mA, SOD-123"/></part>
<part name="D10" library="JR" deviceset="D_1N4148W_SOD-123" device="" value="1N4148W"><attribute name="MANUFACTURER" value="ST(Semtech)"/><attribute name="MPN" value="1N4148W"/><attribute name="LCSC" value="C81598"/><attribute name="DESCRIPTION" value="Switching diode 100 V 150 mA, SOD-123"/></part>
<part name="D11" library="JR" deviceset="D_1N4148W_SOD-123" device="" value="1N4148W"><attribute name="MANUFACTURER" value="ST(Semtech)"/><attribute name="MPN" value="1N4148W"/><attribute name="LCSC" value="C81598"/><attribute name="DESCRIPTION" value="Switching diode 100 V 150 mA, SOD-123"/></part>
<part name="D12" library="JR" deviceset="D_1N4148W_SOD-123" device="" value="1N4148W"><attribute name="MANUFACTURER" value="ST(Semtech)"/><attribute name="MPN" value="1N4148W"/><attribute name="LCSC" value="C81598"/><attribute name="DESCRIPTION" value="Switching diode 100 V 150 mA, SOD-123"/></part>
<part name="D13" library="JR" deviceset="D_1N4148W_SOD-123" device="" value="1N4148W"><attribute name="MANUFACTURER" value="ST(Semtech)"/><attribute name="MPN" value="1N4148W"/><attribute name="LCSC" value="C81598"/><attribute name="DESCRIPTION" value="Switching diode 100 V 150 mA, SOD-123"/></part>
<part name="ENC1" library="JR" deviceset="Encoder_PEC11R-4220F-S0024" device="" value="PEC11R-4220F-S0024"><attribute name="MANUFACTURER" value="Bourns"/><attribute name="MPN" value="PEC11R-4220F-S0024"/><attribute name="LCSC" value="C143797"/><attribute name="DESCRIPTION" value="Rotary encoder, 24 detents / 24 pulses, push switch, 20 mm flatted shaft, EC11 size"/></part>
<part name="H1" library="JR" deviceset="MountingHole_M2" device="" value="M2 hole"><attribute name="DESCRIPTION" value="Unplated 2.2 mm hole for an M2 screw"/></part>
<part name="H2" library="JR" deviceset="MountingHole_M2" device="" value="M2 hole"><attribute name="DESCRIPTION" value="Unplated 2.2 mm hole for an M2 screw"/></part>
<part name="H3" library="JR" deviceset="MountingHole_M2" device="" value="M2 hole"><attribute name="DESCRIPTION" value="Unplated 2.2 mm hole for an M2 screw"/></part>
<part name="H4" library="JR" deviceset="MountingHole_M2" device="" value="M2 hole"><attribute name="DESCRIPTION" value="Unplated 2.2 mm hole for an M2 screw"/></part>
<part name="J1" library="JR" deviceset="Conn_JST_PH_S2B_Horizontal" device="" value="S2B-PH-K-S"><attribute name="MANUFACTURER" value="JST"/><attribute name="MPN" value="S2B-PH-K-S(LF)(SN)"/><attribute name="LCSC" value="C173752"/><attribute name="DESCRIPTION" value="JST PH 2-pin header, side entry, through-hole (LiPo plug)"/></part>
<part name="J2" library="JR" deviceset="Conn_Wire_Pads_1x08" device="" value="Wire pads 1x8"><attribute name="DESCRIPTION" value="8 plated holes, 2.54 mm, 1.0 mm drill: solder wires (or a 1x8 header)"/></part>
<part name="SW1" library="JR" deviceset="SW_Kailh_MX_Hotswap" device="" value="MX hot-swap"><attribute name="MANUFACTURER" value="Kailh"/><attribute name="MPN" value="CPG151101S11"/><attribute name="LCSC" value="C2803348"/><attribute name="DESCRIPTION" value="Kailh MX hot-swap socket for MX switches. Footprint goes on the bottom layer"/></part>
<part name="SW2" library="JR" deviceset="SW_Kailh_MX_Hotswap" device="" value="MX hot-swap"><attribute name="MANUFACTURER" value="Kailh"/><attribute name="MPN" value="CPG151101S11"/><attribute name="LCSC" value="C2803348"/><attribute name="DESCRIPTION" value="Kailh MX hot-swap socket for MX switches. Footprint goes on the bottom layer"/></part>
<part name="SW3" library="JR" deviceset="SW_Kailh_MX_Hotswap" device="" value="MX hot-swap"><attribute name="MANUFACTURER" value="Kailh"/><attribute name="MPN" value="CPG151101S11"/><attribute name="LCSC" value="C2803348"/><attribute name="DESCRIPTION" value="Kailh MX hot-swap socket for MX switches. Footprint goes on the bottom layer"/></part>
<part name="SW4" library="JR" deviceset="SW_Kailh_MX_Hotswap" device="" value="MX hot-swap"><attribute name="MANUFACTURER" value="Kailh"/><attribute name="MPN" value="CPG151101S11"/><attribute name="LCSC" value="C2803348"/><attribute name="DESCRIPTION" value="Kailh MX hot-swap socket for MX switches. Footprint goes on the bottom layer"/></part>
<part name="SW5" library="JR" deviceset="SW_Kailh_MX_Hotswap" device="" value="MX hot-swap"><attribute name="MANUFACTURER" value="Kailh"/><attribute name="MPN" value="CPG151101S11"/><attribute name="LCSC" value="C2803348"/><attribute name="DESCRIPTION" value="Kailh MX hot-swap socket for MX switches. Footprint goes on the bottom layer"/></part>
<part name="SW6" library="JR" deviceset="SW_Kailh_MX_Hotswap" device="" value="MX hot-swap"><attribute name="MANUFACTURER" value="Kailh"/><attribute name="MPN" value="CPG151101S11"/><attribute name="LCSC" value="C2803348"/><attribute name="DESCRIPTION" value="Kailh MX hot-swap socket for MX switches. Footprint goes on the bottom layer"/></part>
<part name="SW7" library="JR" deviceset="SW_Kailh_MX_Hotswap" device="" value="MX hot-swap"><attribute name="MANUFACTURER" value="Kailh"/><attribute name="MPN" value="CPG151101S11"/><attribute name="LCSC" value="C2803348"/><attribute name="DESCRIPTION" value="Kailh MX hot-swap socket for MX switches. Footprint goes on the bottom layer"/></part>
<part name="SW8" library="JR" deviceset="SW_Kailh_MX_Hotswap" device="" value="MX hot-swap"><attribute name="MANUFACTURER" value="Kailh"/><attribute name="MPN" value="CPG151101S11"/><attribute name="LCSC" value="C2803348"/><attribute name="DESCRIPTION" value="Kailh MX hot-swap socket for MX switches. Footprint goes on the bottom layer"/></part>
<part name="SW9" library="JR" deviceset="SW_Kailh_MX_Hotswap" device="" value="MX hot-swap"><attribute name="MANUFACTURER" value="Kailh"/><attribute name="MPN" value="CPG151101S11"/><attribute name="LCSC" value="C2803348"/><attribute name="DESCRIPTION" value="Kailh MX hot-swap socket for MX switches. Footprint goes on the bottom layer"/></part>
<part name="SW10" library="JR" deviceset="SW_Kailh_MX_Hotswap" device="" value="MX hot-swap"><attribute name="MANUFACTURER" value="Kailh"/><attribute name="MPN" value="CPG151101S11"/><attribute name="LCSC" value="C2803348"/><attribute name="DESCRIPTION" value="Kailh MX hot-swap socket for MX switches. Footprint goes on the bottom layer"/></part>
<part name="SW11" library="JR" deviceset="SW_Kailh_MX_Hotswap" device="" value="MX hot-swap"><attribute name="MANUFACTURER" value="Kailh"/><attribute name="MPN" value="CPG151101S11"/><attribute name="LCSC" value="C2803348"/><attribute name="DESCRIPTION" value="Kailh MX hot-swap socket for MX switches. Footprint goes on the bottom layer"/></part>
<part name="SW12" library="JR" deviceset="SW_Kailh_MX_Hotswap" device="" value="MX hot-swap"><attribute name="MANUFACTURER" value="Kailh"/><attribute name="MPN" value="CPG151101S11"/><attribute name="LCSC" value="C2803348"/><attribute name="DESCRIPTION" value="Kailh MX hot-swap socket for MX switches. Footprint goes on the bottom layer"/></part>
<part name="SW_PWR" library="JR" deviceset="SW_Slide_OS102011MA1QN1" device="" value="OS102011MA1QN1"><attribute name="MANUFACTURER" value="C&amp;K"/><attribute name="MPN" value="OS102011MA1QN1"/><attribute name="LCSC" value="C226259"/><attribute name="DESCRIPTION" value="Slide switch SPDT, right angle, through-hole, 4 mm actuator"/></part>
<part name="SW_RST" library="JR" deviceset="SW_Tact_TS-1187A-B-A-B" device="" value="TS-1187A-B-A-B"><attribute name="MANUFACTURER" value="XKB Connection"/><attribute name="MPN" value="TS-1187A-B-A-B"/><attribute name="LCSC" value="C318884"/><attribute name="DESCRIPTION" value="Tactile switch 5.1 x 5.1 x 1.5 mm, SMD gull-wing, 160 gf"/></part>
<part name="TP1" library="JR" deviceset="TestPoint_Pad_1.5mm" device="" value="Test pad"><attribute name="DESCRIPTION" value="Test pad, 1.5 mm, no part fitted"/></part>
<part name="TP2" library="JR" deviceset="TestPoint_Pad_1.5mm" device="" value="Test pad"><attribute name="DESCRIPTION" value="Test pad, 1.5 mm, no part fitted"/></part>
<part name="U1" library="JR" deviceset="SuperMini_nRF52840" device="" value="SuperMini nRF52840"><attribute name="MANUFACTURER" value="generic (nice!nano v2 clone)"/><attribute name="MPN" value="SuperMini nRF52840"/><attribute name="DESCRIPTION" value="nRF52840 module, nice!nano v2 pinout, LiPo charger, USB-C. Pro Micro 24-pin"/></part>
</parts>
<sheets>
<sheet>
<plain>
<wire x1="5" y1="5" x2="415" y2="5" width="0.4" layer="97"/>
<wire x1="415" y1="5" x2="415" y2="292" width="0.4" layer="97"/>
<wire x1="415" y1="292" x2="5" y2="292" width="0.4" layer="97"/>
<wire x1="5" y1="292" x2="5" y2="5" width="0.4" layer="97"/>
<wire x1="15" y1="140" x2="145" y2="140" width="0.254" layer="97"/>
<wire x1="145" y1="140" x2="145" y2="285" width="0.254" layer="97"/>
<wire x1="145" y1="285" x2="15" y2="285" width="0.254" layer="97"/>
<wire x1="15" y1="285" x2="15" y2="140" width="0.254" layer="97"/>
<wire x1="155" y1="140" x2="330" y2="140" width="0.254" layer="97"/>
<wire x1="330" y1="140" x2="330" y2="285" width="0.254" layer="97"/>
<wire x1="330" y1="285" x2="155" y2="285" width="0.254" layer="97"/>
<wire x1="155" y1="285" x2="155" y2="140" width="0.254" layer="97"/>
<wire x1="155" y1="75" x2="330" y2="75" width="0.254" layer="97"/>
<wire x1="330" y1="75" x2="330" y2="135" width="0.254" layer="97"/>
<wire x1="330" y1="135" x2="155" y2="135" width="0.254" layer="97"/>
<wire x1="155" y1="135" x2="155" y2="75" width="0.254" layer="97"/>
<wire x1="15" y1="75" x2="145" y2="75" width="0.254" layer="97"/>
<wire x1="145" y1="75" x2="145" y2="135" width="0.254" layer="97"/>
<wire x1="145" y1="135" x2="15" y2="135" width="0.254" layer="97"/>
<wire x1="15" y1="135" x2="15" y2="75" width="0.254" layer="97"/>
<wire x1="340" y1="200" x2="415" y2="200" width="0.254" layer="97"/>
<wire x1="415" y1="200" x2="415" y2="285" width="0.254" layer="97"/>
<wire x1="415" y1="285" x2="340" y2="285" width="0.254" layer="97"/>
<wire x1="340" y1="285" x2="340" y2="200" width="0.254" layer="97"/>
<wire x1="340" y1="75" x2="415" y2="75" width="0.254" layer="97"/>
<wire x1="415" y1="75" x2="415" y2="195" width="0.254" layer="97"/>
<wire x1="415" y1="195" x2="340" y2="195" width="0.254" layer="97"/>
<wire x1="340" y1="195" x2="340" y2="75" width="0.254" layer="97"/>
<wire x1="300" y1="10" x2="415" y2="10" width="0.254" layer="97"/>
<wire x1="415" y1="10" x2="415" y2="40" width="0.254" layer="97"/>
<wire x1="415" y1="40" x2="300" y2="40" width="0.254" layer="97"/>
<wire x1="300" y1="40" x2="300" y2="10" width="0.254" layer="97"/>
<text x="17" y="280.8" size="2.5" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">Controller: SuperMini nRF52840 (U1, bottom side, face down)</text>
<text x="63.5" y="225.26" size="1.524" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">NC</text>
<text x="20" y="153" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">Pin map = firmware/boards/promicro_nrf52840_nrf52840_uf2.overlay</text>
<text x="20" y="149" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">LCD SPI on full-speed pins (P0.20 clock, P0.17 data). P0.09/P0.10 (NFC) carry the knob.</text>
<text x="20" y="145" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">VCC (pin 21) is switched by P0.13: the firmware turns the LCD supply on.</text>
<text x="157" y="280.8" size="2.5" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">Key matrix: rows = inputs with pull-ups, columns driven low</text>
<text x="167.64" y="258.08" size="1.524" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">key 0</text>
<text x="195.58" y="258.08" size="1.524" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">key 1</text>
<text x="223.52" y="258.08" size="1.524" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">key 2</text>
<text x="251.46" y="258.08" size="1.524" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">key 3</text>
<text x="167.64" y="230.14" size="1.524" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">key 4</text>
<text x="195.58" y="230.14" size="1.524" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">key 5</text>
<text x="223.52" y="230.14" size="1.524" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">key 6</text>
<text x="251.46" y="230.14" size="1.524" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">key 7</text>
<text x="167.64" y="202.2" size="1.524" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">key 8</text>
<text x="195.58" y="202.2" size="1.524" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">key 9</text>
<text x="223.52" y="202.2" size="1.524" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">key 10</text>
<text x="251.46" y="202.2" size="1.524" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">key 11</text>
<text x="274.32" y="269.24" size="1.524" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">knob push (key 16)</text>
<text x="157" y="130.8" size="2.5" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">Knob: EC11-size encoder with push (PEC11R-4220F-S0024)</text>
<text x="160" y="82" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">24 detents / 24 pulses: both contacts open at every detent</text>
<text x="160" y="78.5" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">(no current through the NFC pins at rest). 10 nF + internal pull-up = debounce.</text>
<text x="17" y="130.8" size="2.5" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">LCD: Waveshare 2.0in ST7789 module on 8 wires (J2)</text>
<text x="63.5" y="110.96" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">VCC</text>
<text x="63.5" y="108.42" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">GND</text>
<text x="63.5" y="105.88" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">DIN</text>
<text x="63.5" y="103.34" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">CLK</text>
<text x="63.5" y="100.8" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">CS</text>
<text x="63.5" y="98.26" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">DC</text>
<text x="63.5" y="95.72" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">RST</text>
<text x="63.5" y="93.18" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">BL</text>
<text x="20" y="82" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">Wires in the module's cable order: VCC GND DIN CLK CS DC RST BL</text>
<text x="20" y="78.5" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">C3 = bulk for the backlight switch-on, next to U1 pin 21</text>
<text x="342" y="280.8" size="2.5" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">Power</text>
<text x="365.76" y="265.9" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">LiPo +</text>
<text x="365.76" y="263.36" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">LiPo -</text>
<text x="387.08" y="230.34" size="1.524" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">NC</text>
<text x="345" y="215" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">Slide switch in the right wall:</text>
<text x="345" y="211.5" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">ON = battery to U1 B+ (charger</text>
<text x="345" y="208" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">output; USB charges through it)</text>
<text x="342" y="190.8" size="2.5" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">Reset, debug, mounting</text>
<text x="345" y="160" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">Double-press = UF2 bootloader</text>
<text x="345" y="133" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">UART log out, 115200 8N1</text>
<text x="345" y="93" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">M2 screws into the case pillars</text>
<text x="15" y="62" size="2" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">NOTES</text>
<text x="15" y="57" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">1. Every part is in the JR library (JR.SchLib / JR.PcbLib); parameters carry the LCSC numbers.</text>
<text x="15" y="52" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">2. U1 is soldered face down on 2.5 mm low-profile headers. Trim ENC1 pins flush first; Kapton on U1's back.</text>
<text x="15" y="47" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">3. Firmware key n = SW(n+1): row 0 is the back row (next to the screen), SW1 = back-left = top-left tile.</text>
<text x="15" y="42" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">4. Knob push sits in row 0, column 4 with its own diode (D13); firmware key 16 on every concept.</text>
<text x="15" y="37" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">5. Switch sockets, diodes, U1, J1, J2, power and reset are on the bottom; switches and the knob on top.</text>
<text x="303" y="31" size="2.5" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">Macropad concept B main board</text>
<text x="303" y="25" size="2" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">Rev A   2026-11-11   Sheet 1/1   A3</text>
<text x="303" y="19" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">Drawn by pcb/board/schematic.py from design_b.py</text>
<text x="303" y="14" size="1.778" layer="97" font="vector" ratio="12" rot="R0" align="bottom-left">github.com/jasoneroberts/macropad</text>
</plain>
<instances>
<instance part="C1" gate="G$1" x="264.16" y="106.68" rot="R0"></instance>
<instance part="C2" gate="G$1" x="294.64" y="106.68" rot="R0"></instance>
<instance part="C3" gate="G$1" x="111.76" y="101.6" rot="R0"></instance>
<instance part="D1" gate="G$1" x="180.34" y="256.54" rot="R270" smashed="yes"><attribute name="NAME" x="172.74" y="256.24" size="1.778" layer="95" rot="R0"/><attribute name="VALUE" x="171.24" y="254.24" size="1.27" layer="96" rot="R0"/></instance>
<instance part="D2" gate="G$1" x="208.28" y="256.54" rot="R270" smashed="yes"><attribute name="NAME" x="200.68" y="256.24" size="1.778" layer="95" rot="R0"/><attribute name="VALUE" x="199.18" y="254.24" size="1.27" layer="96" rot="R0"/></instance>
<instance part="D3" gate="G$1" x="236.22" y="256.54" rot="R270" smashed="yes"><attribute name="NAME" x="228.62" y="256.24" size="1.778" layer="95" rot="R0"/><attribute name="VALUE" x="227.12" y="254.24" size="1.27" layer="96" rot="R0"/></instance>
<instance part="D4" gate="G$1" x="264.16" y="256.54" rot="R270" smashed="yes"><attribute name="NAME" x="256.56" y="256.24" size="1.778" layer="95" rot="R0"/><attribute name="VALUE" x="255.06" y="254.24" size="1.27" layer="96" rot="R0"/></instance>
<instance part="D5" gate="G$1" x="180.34" y="228.6" rot="R270" smashed="yes"><attribute name="NAME" x="172.74" y="228.3" size="1.778" layer="95" rot="R0"/><attribute name="VALUE" x="171.24" y="226.3" size="1.27" layer="96" rot="R0"/></instance>
<instance part="D6" gate="G$1" x="208.28" y="228.6" rot="R270" smashed="yes"><attribute name="NAME" x="200.68" y="228.3" size="1.778" layer="95" rot="R0"/><attribute name="VALUE" x="199.18" y="226.3" size="1.27" layer="96" rot="R0"/></instance>
<instance part="D7" gate="G$1" x="236.22" y="228.6" rot="R270" smashed="yes"><attribute name="NAME" x="228.62" y="228.3" size="1.778" layer="95" rot="R0"/><attribute name="VALUE" x="227.12" y="226.3" size="1.27" layer="96" rot="R0"/></instance>
<instance part="D8" gate="G$1" x="264.16" y="228.6" rot="R270" smashed="yes"><attribute name="NAME" x="256.56" y="228.3" size="1.778" layer="95" rot="R0"/><attribute name="VALUE" x="255.06" y="226.3" size="1.27" layer="96" rot="R0"/></instance>
<instance part="D9" gate="G$1" x="180.34" y="200.66" rot="R270" smashed="yes"><attribute name="NAME" x="172.74" y="200.36" size="1.778" layer="95" rot="R0"/><attribute name="VALUE" x="171.24" y="198.36" size="1.27" layer="96" rot="R0"/></instance>
<instance part="D10" gate="G$1" x="208.28" y="200.66" rot="R270" smashed="yes"><attribute name="NAME" x="200.68" y="200.36" size="1.778" layer="95" rot="R0"/><attribute name="VALUE" x="199.18" y="198.36" size="1.27" layer="96" rot="R0"/></instance>
<instance part="D11" gate="G$1" x="236.22" y="200.66" rot="R270" smashed="yes"><attribute name="NAME" x="228.62" y="200.36" size="1.778" layer="95" rot="R0"/><attribute name="VALUE" x="227.12" y="198.36" size="1.27" layer="96" rot="R0"/></instance>
<instance part="D12" gate="G$1" x="264.16" y="200.66" rot="R270" smashed="yes"><attribute name="NAME" x="256.56" y="200.36" size="1.778" layer="95" rot="R0"/><attribute name="VALUE" x="255.06" y="198.36" size="1.27" layer="96" rot="R0"/></instance>
<instance part="D13" gate="G$1" x="292.1" y="256.54" rot="R270" smashed="yes"><attribute name="NAME" x="284.5" y="256.24" size="1.778" layer="95" rot="R0"/><attribute name="VALUE" x="283" y="254.24" size="1.27" layer="96" rot="R0"/></instance>
<instance part="ENC1" gate="G$1" x="203.2" y="106.68" rot="R0"></instance>
<instance part="H1" gate="G$1" x="350.52" y="101.6" rot="R0"></instance>
<instance part="H2" gate="G$1" x="368.3" y="101.6" rot="R0"></instance>
<instance part="H3" gate="G$1" x="386.08" y="101.6" rot="R0"></instance>
<instance part="H4" gate="G$1" x="403.86" y="101.6" rot="R0"></instance>
<instance part="J1" gate="G$1" x="360.68" y="264.16" rot="R0"></instance>
<instance part="J2" gate="G$1" x="60.96" y="101.6" rot="R0"></instance>
<instance part="SW1" gate="G$1" x="172.72" y="264.16" rot="R0"></instance>
<instance part="SW2" gate="G$1" x="200.66" y="264.16" rot="R0"></instance>
<instance part="SW3" gate="G$1" x="228.6" y="264.16" rot="R0"></instance>
<instance part="SW4" gate="G$1" x="256.54" y="264.16" rot="R0"></instance>
<instance part="SW5" gate="G$1" x="172.72" y="236.22" rot="R0"></instance>
<instance part="SW6" gate="G$1" x="200.66" y="236.22" rot="R0"></instance>
<instance part="SW7" gate="G$1" x="228.6" y="236.22" rot="R0"></instance>
<instance part="SW8" gate="G$1" x="256.54" y="236.22" rot="R0"></instance>
<instance part="SW9" gate="G$1" x="172.72" y="208.28" rot="R0"></instance>
<instance part="SW10" gate="G$1" x="200.66" y="208.28" rot="R0"></instance>
<instance part="SW11" gate="G$1" x="228.6" y="208.28" rot="R0"></instance>
<instance part="SW12" gate="G$1" x="256.54" y="208.28" rot="R0"></instance>
<instance part="SW_PWR" gate="G$1" x="381" y="233.68" rot="R0"></instance>
<instance part="SW_RST" gate="G$1" x="370.84" y="172.72" rot="R0"></instance>
<instance part="TP1" gate="G$1" x="355.6" y="142.24" rot="R0"></instance>
<instance part="TP2" gate="G$1" x="381" y="142.24" rot="R0"></instance>
<instance part="U1" gate="G$1" x="81.28" y="213.36" rot="R0"></instance>
</instances>
<busses/>
<nets>
<net name="3V3_SW" class="1">
<segment><pinref part="U1" gate="G$1" pin="VCC"/><wire x1="93.98" y1="220.98" x2="101.6" y2="220.98" width="0.1524" layer="91"/><label x="101.6" y="220.98" size="1.778" layer="95" rot="R0"/></segment>
<segment><pinref part="J2" gate="G$1" pin="1"/><wire x1="55.88" y1="111.76" x2="48.26" y2="111.76" width="0.1524" layer="91"/><label x="48.26" y="111.76" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="C3" gate="G$1" pin="1"/><wire x1="111.76" y1="106.68" x2="111.76" y2="111.76" width="0.1524" layer="91"/><label x="111.76" y="111.76" size="1.778" layer="95" rot="R90"/></segment>
</net>
<net name="COL0" class="0">
<segment><pinref part="U1" gate="G$1" pin="P1.06"/><wire x1="68.58" y1="200.66" x2="60.96" y2="200.66" width="0.1524" layer="91"/><label x="60.96" y="200.66" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="D1" gate="G$1" pin="K"/><pinref part="D5" gate="G$1" pin="K"/><pinref part="D9" gate="G$1" pin="K"/><wire x1="180.34" y1="251.46" x2="185.42" y2="251.46" width="0.1524" layer="91"/><wire x1="180.34" y1="223.52" x2="185.42" y2="223.52" width="0.1524" layer="91"/><wire x1="180.34" y1="195.58" x2="185.42" y2="195.58" width="0.1524" layer="91"/><wire x1="185.42" y1="251.46" x2="185.42" y2="223.52" width="0.1524" layer="91"/><wire x1="185.42" y1="223.52" x2="185.42" y2="195.58" width="0.1524" layer="91"/><wire x1="185.42" y1="195.58" x2="185.42" y2="187.96" width="0.1524" layer="91"/><junction x="185.42" y="223.52"/><junction x="185.42" y="195.58"/><junction x="185.42" y="195.58"/><label x="185.42" y="187.96" size="1.778" layer="95" rot="R270"/></segment>
</net>
<net name="COL1" class="0">
<segment><pinref part="U1" gate="G$1" pin="P1.11"/><wire x1="93.98" y1="205.74" x2="101.6" y2="205.74" width="0.1524" layer="91"/><label x="101.6" y="205.74" size="1.778" layer="95" rot="R0"/></segment>
<segment><pinref part="D2" gate="G$1" pin="K"/><pinref part="D6" gate="G$1" pin="K"/><pinref part="D10" gate="G$1" pin="K"/><wire x1="208.28" y1="251.46" x2="213.36" y2="251.46" width="0.1524" layer="91"/><wire x1="208.28" y1="223.52" x2="213.36" y2="223.52" width="0.1524" layer="91"/><wire x1="208.28" y1="195.58" x2="213.36" y2="195.58" width="0.1524" layer="91"/><wire x1="213.36" y1="251.46" x2="213.36" y2="223.52" width="0.1524" layer="91"/><wire x1="213.36" y1="223.52" x2="213.36" y2="195.58" width="0.1524" layer="91"/><wire x1="213.36" y1="195.58" x2="213.36" y2="187.96" width="0.1524" layer="91"/><junction x="213.36" y="223.52"/><junction x="213.36" y="195.58"/><junction x="213.36" y="195.58"/><label x="213.36" y="187.96" size="1.778" layer="95" rot="R270"/></segment>
</net>
<net name="COL2" class="0">
<segment><pinref part="U1" gate="G$1" pin="P1.13"/><wire x1="93.98" y1="208.28" x2="101.6" y2="208.28" width="0.1524" layer="91"/><label x="101.6" y="208.28" size="1.778" layer="95" rot="R0"/></segment>
<segment><pinref part="D3" gate="G$1" pin="K"/><pinref part="D7" gate="G$1" pin="K"/><pinref part="D11" gate="G$1" pin="K"/><wire x1="236.22" y1="251.46" x2="241.3" y2="251.46" width="0.1524" layer="91"/><wire x1="236.22" y1="223.52" x2="241.3" y2="223.52" width="0.1524" layer="91"/><wire x1="236.22" y1="195.58" x2="241.3" y2="195.58" width="0.1524" layer="91"/><wire x1="241.3" y1="251.46" x2="241.3" y2="223.52" width="0.1524" layer="91"/><wire x1="241.3" y1="223.52" x2="241.3" y2="195.58" width="0.1524" layer="91"/><wire x1="241.3" y1="195.58" x2="241.3" y2="187.96" width="0.1524" layer="91"/><junction x="241.3" y="223.52"/><junction x="241.3" y="195.58"/><junction x="241.3" y="195.58"/><label x="241.3" y="187.96" size="1.778" layer="95" rot="R270"/></segment>
</net>
<net name="COL3" class="0">
<segment><pinref part="U1" gate="G$1" pin="P0.29"/><wire x1="93.98" y1="215.9" x2="101.6" y2="215.9" width="0.1524" layer="91"/><label x="101.6" y="215.9" size="1.778" layer="95" rot="R0"/></segment>
<segment><pinref part="D4" gate="G$1" pin="K"/><pinref part="D8" gate="G$1" pin="K"/><pinref part="D12" gate="G$1" pin="K"/><wire x1="264.16" y1="251.46" x2="269.24" y2="251.46" width="0.1524" layer="91"/><wire x1="264.16" y1="223.52" x2="269.24" y2="223.52" width="0.1524" layer="91"/><wire x1="264.16" y1="195.58" x2="269.24" y2="195.58" width="0.1524" layer="91"/><wire x1="269.24" y1="251.46" x2="269.24" y2="223.52" width="0.1524" layer="91"/><wire x1="269.24" y1="223.52" x2="269.24" y2="195.58" width="0.1524" layer="91"/><wire x1="269.24" y1="195.58" x2="269.24" y2="187.96" width="0.1524" layer="91"/><junction x="269.24" y="223.52"/><junction x="269.24" y="195.58"/><junction x="269.24" y="195.58"/><label x="269.24" y="187.96" size="1.778" layer="95" rot="R270"/></segment>
</net>
<net name="COL4" class="0">
<segment><pinref part="U1" gate="G$1" pin="P0.31"/><wire x1="93.98" y1="218.44" x2="101.6" y2="218.44" width="0.1524" layer="91"/><label x="101.6" y="218.44" size="1.778" layer="95" rot="R0"/></segment>
<segment><pinref part="D13" gate="G$1" pin="K"/><wire x1="292.1" y1="251.46" x2="297.18" y2="251.46" width="0.1524" layer="91"/><wire x1="297.18" y1="251.46" x2="297.18" y2="243.84" width="0.1524" layer="91"/><label x="297.18" y="243.84" size="1.778" layer="95" rot="R270"/></segment>
</net>
<net name="DBG_TX" class="0">
<segment><pinref part="U1" gate="G$1" pin="P0.06"/><wire x1="68.58" y1="228.6" x2="60.96" y2="228.6" width="0.1524" layer="91"/><label x="60.96" y="228.6" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="TP1" gate="G$1" pin="1"/><wire x1="355.6" y1="142.24" x2="355.6" y2="137.16" width="0.1524" layer="91"/><label x="355.6" y="137.16" size="1.778" layer="95" rot="R270"/></segment>
</net>
<net name="ENC_A" class="0">
<segment><pinref part="U1" gate="G$1" pin="P0.09"/><wire x1="93.98" y1="200.66" x2="101.6" y2="200.66" width="0.1524" layer="91"/><label x="101.6" y="200.66" size="1.778" layer="95" rot="R0"/></segment>
<segment><pinref part="ENC1" gate="G$1" pin="A"/><wire x1="193.04" y1="109.22" x2="185.42" y2="109.22" width="0.1524" layer="91"/><label x="185.42" y="109.22" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="C1" gate="G$1" pin="1"/><wire x1="264.16" y1="111.76" x2="264.16" y2="116.84" width="0.1524" layer="91"/><label x="264.16" y="116.84" size="1.778" layer="95" rot="R90"/></segment>
</net>
<net name="ENC_B" class="0">
<segment><pinref part="U1" gate="G$1" pin="P0.10"/><wire x1="93.98" y1="203.2" x2="101.6" y2="203.2" width="0.1524" layer="91"/><label x="101.6" y="203.2" size="1.778" layer="95" rot="R0"/></segment>
<segment><pinref part="ENC1" gate="G$1" pin="B"/><wire x1="193.04" y1="104.14" x2="185.42" y2="104.14" width="0.1524" layer="91"/><label x="185.42" y="104.14" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="C2" gate="G$1" pin="1"/><wire x1="294.64" y1="111.76" x2="294.64" y2="116.84" width="0.1524" layer="91"/><label x="294.64" y="116.84" size="1.778" layer="95" rot="R90"/></segment>
</net>
<net name="GND" class="1">
<segment><pinref part="U1" gate="G$1" pin="GND@3"/><wire x1="68.58" y1="223.52" x2="60.96" y2="223.52" width="0.1524" layer="91"/><label x="60.96" y="223.52" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="U1" gate="G$1" pin="GND@4"/><wire x1="68.58" y1="220.98" x2="60.96" y2="220.98" width="0.1524" layer="91"/><label x="60.96" y="220.98" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="U1" gate="G$1" pin="GND@23"/><wire x1="93.98" y1="226.06" x2="101.6" y2="226.06" width="0.1524" layer="91"/><label x="101.6" y="226.06" size="1.778" layer="95" rot="R0"/></segment>
<segment><pinref part="ENC1" gate="G$1" pin="C"/><wire x1="193.04" y1="106.68" x2="185.42" y2="106.68" width="0.1524" layer="91"/><label x="185.42" y="106.68" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="C1" gate="G$1" pin="2"/><wire x1="264.16" y1="101.6" x2="264.16" y2="96.52" width="0.1524" layer="91"/><label x="264.16" y="96.52" size="1.778" layer="95" rot="R270"/></segment>
<segment><pinref part="C2" gate="G$1" pin="2"/><wire x1="294.64" y1="101.6" x2="294.64" y2="96.52" width="0.1524" layer="91"/><label x="294.64" y="96.52" size="1.778" layer="95" rot="R270"/></segment>
<segment><pinref part="J2" gate="G$1" pin="2"/><wire x1="55.88" y1="109.22" x2="48.26" y2="109.22" width="0.1524" layer="91"/><label x="48.26" y="109.22" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="C3" gate="G$1" pin="2"/><wire x1="111.76" y1="96.52" x2="111.76" y2="91.44" width="0.1524" layer="91"/><label x="111.76" y="91.44" size="1.778" layer="95" rot="R270"/></segment>
<segment><pinref part="J1" gate="G$1" pin="2"/><wire x1="355.6" y1="264.16" x2="350.52" y2="264.16" width="0.1524" layer="91"/><label x="350.52" y="264.16" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="SW_RST" gate="G$1" pin="3"/><pinref part="SW_RST" gate="G$1" pin="4"/><wire x1="375.92" y1="175.26" x2="378.46" y2="175.26" width="0.1524" layer="91"/><wire x1="378.46" y1="175.26" x2="378.46" y2="170.18" width="0.1524" layer="91"/><wire x1="378.46" y1="170.18" x2="375.92" y2="170.18" width="0.1524" layer="91"/><wire x1="378.46" y1="172.72" x2="386.08" y2="172.72" width="0.1524" layer="91"/><junction x="378.46" y="172.72"/><label x="386.08" y="172.72" size="1.778" layer="95" rot="R0"/></segment>
<segment><pinref part="TP2" gate="G$1" pin="1"/><wire x1="381" y1="142.24" x2="381" y2="137.16" width="0.1524" layer="91"/><label x="381" y="137.16" size="1.778" layer="95" rot="R270"/></segment>
</net>
<net name="K1" class="0">
<segment><pinref part="SW1" gate="G$1" pin="2"/><pinref part="D1" gate="G$1" pin="A"/><wire x1="177.8" y1="264.16" x2="180.34" y2="264.16" width="0.1524" layer="91"/><wire x1="180.34" y1="264.16" x2="180.34" y2="261.62" width="0.1524" layer="91"/></segment>
</net>
<net name="K10" class="0">
<segment><pinref part="SW10" gate="G$1" pin="2"/><pinref part="D10" gate="G$1" pin="A"/><wire x1="205.74" y1="208.28" x2="208.28" y2="208.28" width="0.1524" layer="91"/><wire x1="208.28" y1="208.28" x2="208.28" y2="205.74" width="0.1524" layer="91"/></segment>
</net>
<net name="K11" class="0">
<segment><pinref part="SW11" gate="G$1" pin="2"/><pinref part="D11" gate="G$1" pin="A"/><wire x1="233.68" y1="208.28" x2="236.22" y2="208.28" width="0.1524" layer="91"/><wire x1="236.22" y1="208.28" x2="236.22" y2="205.74" width="0.1524" layer="91"/></segment>
</net>
<net name="K12" class="0">
<segment><pinref part="SW12" gate="G$1" pin="2"/><pinref part="D12" gate="G$1" pin="A"/><wire x1="261.62" y1="208.28" x2="264.16" y2="208.28" width="0.1524" layer="91"/><wire x1="264.16" y1="208.28" x2="264.16" y2="205.74" width="0.1524" layer="91"/></segment>
</net>
<net name="K2" class="0">
<segment><pinref part="SW2" gate="G$1" pin="2"/><pinref part="D2" gate="G$1" pin="A"/><wire x1="205.74" y1="264.16" x2="208.28" y2="264.16" width="0.1524" layer="91"/><wire x1="208.28" y1="264.16" x2="208.28" y2="261.62" width="0.1524" layer="91"/></segment>
</net>
<net name="K3" class="0">
<segment><pinref part="SW3" gate="G$1" pin="2"/><pinref part="D3" gate="G$1" pin="A"/><wire x1="233.68" y1="264.16" x2="236.22" y2="264.16" width="0.1524" layer="91"/><wire x1="236.22" y1="264.16" x2="236.22" y2="261.62" width="0.1524" layer="91"/></segment>
</net>
<net name="K4" class="0">
<segment><pinref part="SW4" gate="G$1" pin="2"/><pinref part="D4" gate="G$1" pin="A"/><wire x1="261.62" y1="264.16" x2="264.16" y2="264.16" width="0.1524" layer="91"/><wire x1="264.16" y1="264.16" x2="264.16" y2="261.62" width="0.1524" layer="91"/></segment>
</net>
<net name="K5" class="0">
<segment><pinref part="SW5" gate="G$1" pin="2"/><pinref part="D5" gate="G$1" pin="A"/><wire x1="177.8" y1="236.22" x2="180.34" y2="236.22" width="0.1524" layer="91"/><wire x1="180.34" y1="236.22" x2="180.34" y2="233.68" width="0.1524" layer="91"/></segment>
</net>
<net name="K6" class="0">
<segment><pinref part="SW6" gate="G$1" pin="2"/><pinref part="D6" gate="G$1" pin="A"/><wire x1="205.74" y1="236.22" x2="208.28" y2="236.22" width="0.1524" layer="91"/><wire x1="208.28" y1="236.22" x2="208.28" y2="233.68" width="0.1524" layer="91"/></segment>
</net>
<net name="K7" class="0">
<segment><pinref part="SW7" gate="G$1" pin="2"/><pinref part="D7" gate="G$1" pin="A"/><wire x1="233.68" y1="236.22" x2="236.22" y2="236.22" width="0.1524" layer="91"/><wire x1="236.22" y1="236.22" x2="236.22" y2="233.68" width="0.1524" layer="91"/></segment>
</net>
<net name="K8" class="0">
<segment><pinref part="SW8" gate="G$1" pin="2"/><pinref part="D8" gate="G$1" pin="A"/><wire x1="261.62" y1="236.22" x2="264.16" y2="236.22" width="0.1524" layer="91"/><wire x1="264.16" y1="236.22" x2="264.16" y2="233.68" width="0.1524" layer="91"/></segment>
</net>
<net name="K9" class="0">
<segment><pinref part="SW9" gate="G$1" pin="2"/><pinref part="D9" gate="G$1" pin="A"/><wire x1="177.8" y1="208.28" x2="180.34" y2="208.28" width="0.1524" layer="91"/><wire x1="180.34" y1="208.28" x2="180.34" y2="205.74" width="0.1524" layer="91"/></segment>
</net>
<net name="K_PUSH" class="0">
<segment><pinref part="D13" gate="G$1" pin="A"/><wire x1="292.1" y1="261.62" x2="292.1" y2="264.16" width="0.1524" layer="91"/><wire x1="292.1" y1="264.16" x2="281.94" y2="264.16" width="0.1524" layer="91"/><label x="281.94" y="264.16" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="ENC1" gate="G$1" pin="S2"/><wire x1="213.36" y1="104.14" x2="220.98" y2="104.14" width="0.1524" layer="91"/><label x="220.98" y="104.14" size="1.778" layer="95" rot="R0"/></segment>
</net>
<net name="LCD_BL" class="0">
<segment><pinref part="U1" gate="G$1" pin="P0.11"/><wire x1="68.58" y1="205.74" x2="60.96" y2="205.74" width="0.1524" layer="91"/><label x="60.96" y="205.74" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="J2" gate="G$1" pin="8"/><wire x1="55.88" y1="93.98" x2="48.26" y2="93.98" width="0.1524" layer="91"/><label x="48.26" y="93.98" size="1.778" layer="95" rot="R180"/></segment>
</net>
<net name="LCD_CS" class="0">
<segment><pinref part="U1" gate="G$1" pin="P0.22"/><wire x1="68.58" y1="213.36" x2="60.96" y2="213.36" width="0.1524" layer="91"/><label x="60.96" y="213.36" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="J2" gate="G$1" pin="5"/><wire x1="55.88" y1="101.6" x2="48.26" y2="101.6" width="0.1524" layer="91"/><label x="48.26" y="101.6" size="1.778" layer="95" rot="R180"/></segment>
</net>
<net name="LCD_DC" class="0">
<segment><pinref part="U1" gate="G$1" pin="P0.24"/><wire x1="68.58" y1="210.82" x2="60.96" y2="210.82" width="0.1524" layer="91"/><label x="60.96" y="210.82" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="J2" gate="G$1" pin="6"/><wire x1="55.88" y1="99.06" x2="48.26" y2="99.06" width="0.1524" layer="91"/><label x="48.26" y="99.06" size="1.778" layer="95" rot="R180"/></segment>
</net>
<net name="LCD_MOSI" class="0">
<segment><pinref part="U1" gate="G$1" pin="P0.17"/><wire x1="68.58" y1="218.44" x2="60.96" y2="218.44" width="0.1524" layer="91"/><label x="60.96" y="218.44" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="J2" gate="G$1" pin="3"/><wire x1="55.88" y1="106.68" x2="48.26" y2="106.68" width="0.1524" layer="91"/><label x="48.26" y="106.68" size="1.778" layer="95" rot="R180"/></segment>
</net>
<net name="LCD_RST" class="0">
<segment><pinref part="U1" gate="G$1" pin="P1.00"/><wire x1="68.58" y1="208.28" x2="60.96" y2="208.28" width="0.1524" layer="91"/><label x="60.96" y="208.28" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="J2" gate="G$1" pin="7"/><wire x1="55.88" y1="96.52" x2="48.26" y2="96.52" width="0.1524" layer="91"/><label x="48.26" y="96.52" size="1.778" layer="95" rot="R180"/></segment>
</net>
<net name="LCD_SCK" class="0">
<segment><pinref part="U1" gate="G$1" pin="P0.20"/><wire x1="68.58" y1="215.9" x2="60.96" y2="215.9" width="0.1524" layer="91"/><label x="60.96" y="215.9" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="J2" gate="G$1" pin="4"/><wire x1="55.88" y1="104.14" x2="48.26" y2="104.14" width="0.1524" layer="91"/><label x="48.26" y="104.14" size="1.778" layer="95" rot="R180"/></segment>
</net>
<net name="NRST" class="0">
<segment><pinref part="U1" gate="G$1" pin="RST"/><wire x1="93.98" y1="223.52" x2="101.6" y2="223.52" width="0.1524" layer="91"/><label x="101.6" y="223.52" size="1.778" layer="95" rot="R0"/></segment>
<segment><pinref part="SW_RST" gate="G$1" pin="1"/><pinref part="SW_RST" gate="G$1" pin="2"/><wire x1="365.76" y1="175.26" x2="363.22" y2="175.26" width="0.1524" layer="91"/><wire x1="363.22" y1="175.26" x2="363.22" y2="170.18" width="0.1524" layer="91"/><wire x1="363.22" y1="170.18" x2="365.76" y2="170.18" width="0.1524" layer="91"/><wire x1="363.22" y1="172.72" x2="355.6" y2="172.72" width="0.1524" layer="91"/><junction x="363.22" y="172.72"/><label x="355.6" y="172.72" size="1.778" layer="95" rot="R180"/></segment>
</net>
<net name="ROW0" class="0">
<segment><pinref part="U1" gate="G$1" pin="P1.15"/><wire x1="93.98" y1="210.82" x2="101.6" y2="210.82" width="0.1524" layer="91"/><label x="101.6" y="210.82" size="1.778" layer="95" rot="R0"/></segment>
<segment><pinref part="SW1" gate="G$1" pin="1"/><pinref part="SW2" gate="G$1" pin="1"/><pinref part="SW3" gate="G$1" pin="1"/><pinref part="SW4" gate="G$1" pin="1"/><wire x1="167.64" y1="264.16" x2="167.64" y2="269.24" width="0.1524" layer="91"/><wire x1="195.58" y1="264.16" x2="195.58" y2="269.24" width="0.1524" layer="91"/><wire x1="223.52" y1="264.16" x2="223.52" y2="269.24" width="0.1524" layer="91"/><wire x1="251.46" y1="264.16" x2="251.46" y2="269.24" width="0.1524" layer="91"/><wire x1="160.02" y1="269.24" x2="167.64" y2="269.24" width="0.1524" layer="91"/><wire x1="167.64" y1="269.24" x2="195.58" y2="269.24" width="0.1524" layer="91"/><wire x1="195.58" y1="269.24" x2="223.52" y2="269.24" width="0.1524" layer="91"/><wire x1="223.52" y1="269.24" x2="251.46" y2="269.24" width="0.1524" layer="91"/><junction x="167.64" y="269.24"/><junction x="195.58" y="269.24"/><junction x="223.52" y="269.24"/><label x="160.02" y="269.24" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="ENC1" gate="G$1" pin="S1"/><wire x1="213.36" y1="109.22" x2="220.98" y2="109.22" width="0.1524" layer="91"/><label x="220.98" y="109.22" size="1.778" layer="95" rot="R0"/></segment>
</net>
<net name="ROW1" class="0">
<segment><pinref part="U1" gate="G$1" pin="P0.02"/><wire x1="93.98" y1="213.36" x2="101.6" y2="213.36" width="0.1524" layer="91"/><label x="101.6" y="213.36" size="1.778" layer="95" rot="R0"/></segment>
<segment><pinref part="SW5" gate="G$1" pin="1"/><pinref part="SW6" gate="G$1" pin="1"/><pinref part="SW7" gate="G$1" pin="1"/><pinref part="SW8" gate="G$1" pin="1"/><wire x1="167.64" y1="236.22" x2="167.64" y2="241.3" width="0.1524" layer="91"/><wire x1="195.58" y1="236.22" x2="195.58" y2="241.3" width="0.1524" layer="91"/><wire x1="223.52" y1="236.22" x2="223.52" y2="241.3" width="0.1524" layer="91"/><wire x1="251.46" y1="236.22" x2="251.46" y2="241.3" width="0.1524" layer="91"/><wire x1="160.02" y1="241.3" x2="167.64" y2="241.3" width="0.1524" layer="91"/><wire x1="167.64" y1="241.3" x2="195.58" y2="241.3" width="0.1524" layer="91"/><wire x1="195.58" y1="241.3" x2="223.52" y2="241.3" width="0.1524" layer="91"/><wire x1="223.52" y1="241.3" x2="251.46" y2="241.3" width="0.1524" layer="91"/><junction x="167.64" y="241.3"/><junction x="195.58" y="241.3"/><junction x="223.52" y="241.3"/><label x="160.02" y="241.3" size="1.778" layer="95" rot="R180"/></segment>
</net>
<net name="ROW2" class="0">
<segment><pinref part="U1" gate="G$1" pin="P1.04"/><wire x1="68.58" y1="203.2" x2="60.96" y2="203.2" width="0.1524" layer="91"/><label x="60.96" y="203.2" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="SW9" gate="G$1" pin="1"/><pinref part="SW10" gate="G$1" pin="1"/><pinref part="SW11" gate="G$1" pin="1"/><pinref part="SW12" gate="G$1" pin="1"/><wire x1="167.64" y1="208.28" x2="167.64" y2="213.36" width="0.1524" layer="91"/><wire x1="195.58" y1="208.28" x2="195.58" y2="213.36" width="0.1524" layer="91"/><wire x1="223.52" y1="208.28" x2="223.52" y2="213.36" width="0.1524" layer="91"/><wire x1="251.46" y1="208.28" x2="251.46" y2="213.36" width="0.1524" layer="91"/><wire x1="160.02" y1="213.36" x2="167.64" y2="213.36" width="0.1524" layer="91"/><wire x1="167.64" y1="213.36" x2="195.58" y2="213.36" width="0.1524" layer="91"/><wire x1="195.58" y1="213.36" x2="223.52" y2="213.36" width="0.1524" layer="91"/><wire x1="223.52" y1="213.36" x2="251.46" y2="213.36" width="0.1524" layer="91"/><junction x="167.64" y="213.36"/><junction x="195.58" y="213.36"/><junction x="223.52" y="213.36"/><label x="160.02" y="213.36" size="1.778" layer="95" rot="R180"/></segment>
</net>
<net name="VBAT" class="1">
<segment><pinref part="J1" gate="G$1" pin="1"/><wire x1="355.6" y1="266.7" x2="350.52" y2="266.7" width="0.1524" layer="91"/><label x="350.52" y="266.7" size="1.778" layer="95" rot="R180"/></segment>
<segment><pinref part="SW_PWR" gate="G$1" pin="1"/><wire x1="386.08" y1="236.22" x2="391.16" y2="236.22" width="0.1524" layer="91"/><label x="391.16" y="236.22" size="1.778" layer="95" rot="R0"/></segment>
</net>
<net name="VBAT_SW" class="1">
<segment><pinref part="U1" gate="G$1" pin="BAT+"/><wire x1="93.98" y1="228.6" x2="101.6" y2="228.6" width="0.1524" layer="91"/><label x="101.6" y="228.6" size="1.778" layer="95" rot="R0"/></segment>
<segment><pinref part="SW_PWR" gate="G$1" pin="COM"/><wire x1="375.92" y1="233.68" x2="370.84" y2="233.68" width="0.1524" layer="91"/><label x="370.84" y="233.68" size="1.778" layer="95" rot="R180"/></segment>
</net>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
</eagle>
