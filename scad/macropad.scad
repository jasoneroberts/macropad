// ============================================================
// Nordic macropad: parametric enclosure for concepts A, B and C
// OpenSCAD 2021.01 or newer. Units: mm.
//
// Pick a concept and a part below (or pass them on the command
// line: openscad -D 'concept="B"' -D 'part="top_print"' -o top.stl).
//
// Two coordinate frames are used:
//   plate frame: origin at the front-left corner of the top surface.
//                x = right, y = toward the back (up the slope),
//                z = out of the top surface. z = 0 is the plate top.
//                Almost everything is designed in this frame.
//   desk frame:  the plate frame tilted by `tilt` about x and lifted
//                so the front top edge is `front_h` above the desk.
//                z = 0 is the underside of the bottom plate (rubber
//                feet not included).
//
// Every number marked MEASURE comes from a datasheet or listing,
// not from a part on the bench. Check it with calipers before you
// print anything that depends on it.
// ============================================================

/* [Selection] */
concept = "A";      // [A, B, C]
// assembly = everything in place; *_print = oriented for the printer bed
part = "assembly";  // [assembly, top_print, bottom_print, knob_print, clamp_print, test_coupon, top, bottom, knob, clamp, pcb, sockets, switches, switch_bodies, keycaps, encoder, display, mcu, battery, power_switch, pcb_outline, report]

/* CONSTANTS */

// ---- Cherry MX switch and hot-swap stack ----
pitch        = 19.05;  // 1u key spacing
sw_hole      = 14.0;   // plate cutout. Printed holes shrink: try 14.0-14.2 on a test plate
sw_lip       = 1.5;    // plate thickness the MX clips are made for
sw_undercut  = 15.0;   // pocket under the lip so the clips can open
plate_to_pcb = 5.0;    // MX standard: plate top to PCB top
pcb_t        = 1.6;
socket_h     = 1.85;   // Kailh MX hot-swap socket below the PCB

// ---- case ----
skin         = 3.0;    // top surface thickness (1.5 mm lip + 1.5 mm stiffening ribs)
wall         = 2.4;    // 6 perimeters at 0.4 mm
bottom_t     = 2.4;    // bottom plate
front_h      = 12.5;   // plate top at the front edge, above the desk
corner_r     = 5;
edge_chamfer = 1.0;
lip_h        = 1.5;    // locating lip on the bottom plate
lip_w        = 1.2;
fit_gap      = 0.25;   // printed-part clearance

// ---- fasteners ----
boss_d       = 8;      // corner screw bosses
boss_inset   = 5.5;
insert_d     = 4.0;    // M3 heat-set insert, short type (M3 x 4 mm). MEASURE your inserts
insert_len   = 4.0;
screw_clear  = 3.3;
csk_d        = 6.4;    // M3 countersunk head
m2_pilot     = 1.7;    // M2 self-tapping pilot hole
pillar_d     = 4.4;    // PCB pillars between switches (fits a grid intersection)
dpillar_d    = 5.5;    // display clamp pillars
foot_d       = 10.6;   // 10 mm rubber bumpers
foot_depth   = 1.0;

// ---- EC11 rotary encoder ----
enc_hole     = 14.0;   // same as a switch hole, so a switch can go there instead
enc_body     = 12.0;
enc_body_h   = 6.5;    // PCB top to top of the metal body. MEASURE
enc_bushing_d= 7.0;
enc_bushing_h= 5.0;
enc_shaft_l  = 15.0;   // D shaft length above the body (15 mm type, or cut a 20 mm one)
knob_lift    = 0.8;    // gap between knob skirt and the top surface
knob_h       = 18.0;

// ---- display mounting ----
bezel_t      = 1.0;    // skin left over the glass edge
win_margin   = 0.4;    // window opening beyond the active area
glass_gap    = 0.25;
clamp_t      = 2.0;
clamp_rim    = 2.5;    // how far the clamp frame reaches under the module board

// ---- controller: Pro Micro size nRF52840 (nice!nano v2 / SuperMini clone) ----
mcu_size     = [18.0, 33.0, 1.0];   // x, y, board thickness
mcu_gap      = 2.5;    // header plastic between the main PCB and the controller
usb_size     = [8.94, 7.35, 3.26];  // USB-C receptacle w, depth, height
usb_slot     = [13.0, 7.5];         // wall opening, sized for the cable overmould

// ---- LiPo ----
// [thickness, width, length] as in the cell name, e.g. 603040 = 6.0 x 30 x 40
LIPO_603040  = [6.0, 30, 40];
LIPO_803040  = [8.0, 30, 40];

/* DISPLAY MODULES (as mounted; MEASURE) */
// glass: panel outline, active: visible pixels, board: module PCB.
// *_off: offset of that item from the glass centre.
LCD169 = [ ["type","rect"], ["label","1.69in ST7789V2 240x280 (portrait)"],
           ["glass",[30.1,37.4]], ["glass_t",2.0],
           ["active",[27.97,32.63]], ["active_off",[0,-1.2]],
           ["board",[31.5,39.0]], ["board_off",[0,0]], ["board_t",1.6],
           ["px",[240,280]] ];
LCD200 = [ ["type","rect"], ["label","2.0in ST7789 320x240 (landscape)"],
           ["glass",[47.0,34.6]], ["glass_t",2.0],
           ["active",[40.8,30.6]], ["active_off",[1.0,0]],
           ["board",[58.0,35.0]], ["board_off",[-5.5,0]], ["board_t",1.6],
           ["px",[320,240]] ];
GC9A01 = [ ["type","round"], ["label","1.28in GC9A01 240x240 round"],
           ["glass",35.6], ["glass_t",2.0],
           ["active",32.4], ["active_off",[0,0]],
           ["board",37.5], ["board_tab",[20,20.2]], ["board_off",[0,0]], ["board_t",1.6],
           ["px",[240,240]] ];

/* CONCEPTS */
// Positions are plate-frame centres. bat = [desk x, desk y, rotation].
CFG_A = [ ["name","A - Pocket"], ["cols",3], ["rows",3], ["tilt",6],
          ["W",76.0], ["m_front",8], ["band_gap",4], ["band_h",41], ["m_back",10],
          ["disp",LCD169], ["disp_c",[26.25,89.65]],
          ["enc_c",[57.05,89.65]], ["knob_d",26],
          ["mcu_x",56.5], ["sw_y",73], ["lipo",LIPO_603040], ["bat",[26,89,0]] ];
CFG_B = [ ["name","B - Studio"], ["cols",4], ["rows",3], ["tilt",6],
          ["W",101.0], ["m_front",8], ["band_gap",4], ["band_h",37], ["m_back",10],
          ["disp",LCD200], ["disp_c",[44.5,87.65]],
          ["enc_c",[83.0,87.65]], ["knob_d",28],
          ["mcu_x",82.0], ["sw_y",72], ["lipo",LIPO_603040], ["bat",[39,88,90]] ];
CFG_C = [ ["name","C - Deck"], ["cols",4], ["rows",4], ["tilt",7],
          ["W",92.2], ["m_front",8], ["band_gap",4], ["band_h",41.5], ["m_back",10],
          ["disp",GC9A01], ["disp_c",[27.05,108.95]],
          ["enc_c",[65.15,108.95]], ["knob_d",36],
          ["mcu_x",73.0], ["sw_y",94], ["lipo",LIPO_803040], ["bat",[27,110,0]] ];

/* FUNCTIONS */
function kv(t, k) = let(i = search([k], t)[0])
    assert(i != [], str("missing key: ", k)) t[i][1];
function cfg(k) = kv(concept == "A" ? CFG_A : concept == "B" ? CFG_B : CFG_C, k);
function dsp(k) = kv(cfg("disp"), k);

tilt   = cfg("tilt");
cols   = cfg("cols");
rows   = cfg("rows");
W      = cfg("W");
L      = cfg("m_front") + rows * pitch + cfg("band_gap") + cfg("band_h") + cfg("m_back");
grid_x0 = (W - cols * pitch) / 2;
grid_y0 = cfg("m_front");
disp_c = cfg("disp_c");
enc_c  = cfg("enc_c");
round_disp = dsp("type") == "round";
win_round  = round_disp ? dsp("active") + 2 * win_margin : 0;
win_rect   = round_disp ? [0, 0] : dsp("active") + [2, 2] * win_margin;

function key_c(c, r) = [grid_x0 + (c + 0.5) * pitch, grid_y0 + (r + 0.5) * pitch];
KEYS = [ for (r = [0:rows-1]) for (c = [0:cols-1]) key_c(c, r) ];

// PCB pillars at the four outermost inner grid intersections
PILLARS = [ for (i = [1, cols-1]) for (j = [1, rows-1])
            [grid_x0 + i * pitch, grid_y0 + j * pitch] ];

// display stack, plate z
z_glass_bot = -(bezel_t + dsp("glass_t"));
z_board_bot = z_glass_bot - dsp("board_t");
z_clamp_bot = z_board_bot - clamp_t;

// board outline extents (from the glass centre) and clamp pillar positions
board_c  = disp_c + dsp("board_off");
board_y0 = round_disp ? board_c[1] - dsp("board")/2 : board_c[1] - dsp("board")[1]/2;
board_y1 = round_disp ? board_c[1] + dsp("board_tab")[1] : board_c[1] + dsp("board")[1]/2;
DPILLARS = [ [board_c[0], board_y0 - 3.5], [board_c[0], board_y1 + 3.5] ];

// controller and USB, plate frame
z_pcb_top  = -plate_to_pcb;
z_pcb_bot  = z_pcb_top - pcb_t;
z_mcu_top  = z_pcb_bot - mcu_gap;              // controller back face (pads only)
z_mcu_bot  = z_mcu_top - mcu_size[2];          // component side faces down
z_usb      = z_mcu_bot - usb_size[2] / 2;
usb_face_y = L - wall - 0.2;
mcu_c      = [cfg("mcu_x"), usb_face_y - 0.8 - mcu_size[1] / 2];

// power switch on the PCB underside at the right edge
psw_size = [3.5, 8.6, 3.5];
z_psw    = z_pcb_bot - psw_size[2] / 2;

// corner bosses: plate xy where they meet the skin underside
BOSSES = [ [boss_inset, boss_inset], [W - boss_inset, boss_inset],
           [boss_inset, L - boss_inset], [W - boss_inset, L - boss_inset] ];

// plate frame -> desk frame
function desk_pt(p) = [p[0],
                       p[1] * cos(tilt) - p[2] * sin(tilt),
                       front_h + p[1] * sin(tilt) + p[2] * cos(tilt)];
// plate z of the floor (bottom plate top) below plate point y
function floor_z(y) = (bottom_t - front_h - y * sin(tilt)) / cos(tilt);

/* MODULES: 2D */
module rrect(size, r) {
    translate([r, r]) offset(r = r) square([size[0] - 2 * r, size[1] - 2 * r]);
}
module crect(size, r = 0) {
    if (r > 0) translate(-size / 2) rrect(size, r);
    else square(size, center = true);
}
module outline() { rrect([W, L], corner_r); }

module board_2d(grow = 0) {
    translate(board_c)
    if (round_disp) {
        circle(d = dsp("board") + 2 * grow, $fn = 96);
        translate([-dsp("board_tab")[0] / 2 - grow, 0])
            square([dsp("board_tab")[0] + 2 * grow, dsp("board_tab")[1] + grow]);
    } else crect(dsp("board") + [2, 2] * grow);
}

module clamp_2d() {
    difference() {
        union() {
            board_2d();
            for (p = DPILLARS) {
                translate(p) circle(d = dpillar_d + 1, $fn = 32);
                translate([p[0] - 3.5, min(p[1], board_c[1])]) square([7, abs(p[1] - board_c[1])]);
            }
        }
        board_2d(-clamp_rim);
        for (p = DPILLARS) translate(p) circle(d = 2.3, $fn = 24);
    }
}

module pcb_2d() {
    difference() {
        offset(r = -(wall + 0.5)) outline();
        offset(delta = 1) hull() { board_2d(); for (p = DPILLARS) translate(p) circle(d = dpillar_d + 1); }
        for (b = BOSSES) translate(b) circle(d = boss_d + 2, $fn = 32);
        for (k = KEYS) translate(k) circle(d = 4.0, $fn = 24);          // MX centre pin hole
        for (p = PILLARS) translate(p) circle(d = 2.2, $fn = 16);       // M2 clearance
    }
}

/* MODULES: placement */
module to_desk() translate([0, 0, front_h]) rotate([tilt, 0, 0]) children();
module above_floor() translate([-50, -50, bottom_t]) cube([W + 100, L + 100, 100]);
DEEP = 80;

/* MODULES: top shell */
module outer_plate() {
    hull() {
        translate([0, 0, -edge_chamfer]) linear_extrude(edge_chamfer) offset(r = -edge_chamfer) outline();
        translate([0, 0, -DEEP]) linear_extrude(DEEP - edge_chamfer) outline();
    }
}

module shell_body_plate() {
    difference() {
        outer_plate();
        translate([0, 0, -DEEP - 1]) linear_extrude(DEEP + 1 - skin) offset(r = -wall) outline();
    }
    // PCB pillars
    for (p = PILLARS) translate([p[0], p[1], z_pcb_top]) cylinder(d = pillar_d, h = plate_to_pcb - skin + 0.01, $fn = 24);
    // display clamp pillars
    for (p = DPILLARS) translate([p[0], p[1], z_board_bot]) cylinder(d = dpillar_d, h = -z_board_bot - skin + 0.01, $fn = 24);
}

module shell_cuts_plate() {
    // switch holes with the clip undercut
    for (k = KEYS) translate(k) {
        translate([0, 0, -skin - 1]) linear_extrude(skin + 2) square(sw_hole, center = true);
        translate([0, 0, -skin - 1]) linear_extrude(skin + 1 - sw_lip) square(sw_undercut, center = true);
    }
    // encoder
    translate(enc_c) translate([0, 0, -skin - 1]) linear_extrude(skin + 2) square(enc_hole, center = true);
    // display window (45 degree chamfer through the bezel) and glass pocket
    translate(disp_c + dsp("active_off")) {
        if (round_disp) {
            translate([0, 0, -bezel_t - 0.01]) cylinder(d1 = win_round, d2 = win_round + 2 * bezel_t + 0.02, h = bezel_t + 0.02, $fn = 128);
            translate([0, 0, -0.01]) cylinder(d = win_round + 2 * bezel_t + 0.02, h = 2, $fn = 128);
        } else {
            hull() {
                translate([0, 0, -bezel_t - 0.01]) linear_extrude(0.01) crect(win_rect, 0.6);
                linear_extrude(0.01) crect(win_rect + [2, 2] * bezel_t, 0.6 + bezel_t);
            }
            translate([0, 0, -0.01]) linear_extrude(2) crect(win_rect + [2, 2] * bezel_t, 0.6 + bezel_t);
        }
    }
    translate(disp_c) translate([0, 0, -skin - 1]) linear_extrude(skin + 1 - bezel_t)
        if (round_disp) circle(d = dsp("glass") + 2 * glass_gap, $fn = 128);
        else crect(dsp("glass") + [2, 2] * glass_gap);
    // pilot holes (stop 1 mm under the top surface)
    for (p = PILLARS) translate([p[0], p[1], z_pcb_top - 1]) cylinder(d = m2_pilot, h = plate_to_pcb, $fn = 16);
    for (p = DPILLARS) translate([p[0], p[1], z_board_bot - 1]) cylinder(d = m2_pilot, h = -z_board_bot, $fn = 16);
    // USB-C opening in the back wall
    translate([mcu_c[0], L - wall - 1, z_usb]) rotate([-90, 0, 0])
        linear_extrude(wall + 2) crect(usb_slot, 3.5);
    // power switch slot in the right wall
    translate([W - wall - 1, cfg("sw_y"), z_psw]) rotate([0, 90, 0])
        linear_extrude(wall + 2) crect([3.0, 6.0], 1.0);
}

module bosses_desk() {
    for (b = BOSSES) let(d = desk_pt([b[0], b[1], -skin]))
        translate([d[0], d[1], bottom_t - 0.01]) cylinder(d = boss_d, h = 60, $fn = 40);
}
module boss_holes_desk() {
    for (b = BOSSES) let(d = desk_pt([b[0], b[1], -skin])) translate([d[0], d[1], bottom_t - 1]) {
        cylinder(d = insert_d, h = insert_len + 1.0 + 1, $fn = 32);
        cylinder(d = 3.2, h = insert_len + 1.0 + 2.5 + 1, $fn = 24);
    }
}

module top_shell() {
    intersection() {
        difference() {
            union() {
                to_desk() shell_body_plate();
                intersection() { bosses_desk(); to_desk() outer_plate(); }
            }
            to_desk() shell_cuts_plate();
            boss_holes_desk();
        }
        above_floor();
    }
}

/* MODULES: bottom plate */
module bottom_outline() {
    projection(cut = true) translate([0, 0, -bottom_t]) to_desk() outer_plate();
}
module inner_outline_desk(z = bottom_t + 0.01) {
    projection(cut = true) translate([0, 0, -z])
        to_desk() translate([0, 0, -DEEP - 1]) linear_extrude(DEEP + 1 - skin) offset(r = -wall) outline();
}
// the walls lean with the tilt, so take the inside at both ends of the lip
module lip_outline() intersection() { inner_outline_desk(); inner_outline_desk(bottom_t + lip_h); }
function boss_desk_xy(b) = let(d = desk_pt([b[0], b[1], -skin])) [d[0], d[1]];

module bottom_plate() {
    bat  = cfg("bat");
    lipo = cfg("lipo");
    difference() {
        union() {
            linear_extrude(bottom_t) bottom_outline();
            // locating lip just inside the walls
            translate([0, 0, bottom_t - 0.01]) linear_extrude(lip_h) difference() {
                offset(delta = -fit_gap) lip_outline();
                offset(delta = -fit_gap - lip_w) lip_outline();
                for (b = BOSSES) translate(boss_desk_xy(b)) circle(d = boss_d + 1, $fn = 32);
            }
            // battery cradle
            translate([bat[0], bat[1], bottom_t - 0.01]) rotate(bat[2]) linear_extrude(2.0) difference() {
                crect([lipo[1], lipo[2]] + [1, 1] + [2.4, 2.4], 1.5);
                crect([lipo[1], lipo[2]] + [1, 1], 1);
                square([lipo[1] + 10, 12], center = true);   // finger gaps to lift the cell out
            }
        }
        // countersunk M3 holes
        for (b = BOSSES) translate(boss_desk_xy(b)) {
            translate([0, 0, -1]) cylinder(d = screw_clear, h = bottom_t + 2, $fn = 24);
            translate([0, 0, -0.01]) cylinder(d1 = csk_d, d2 = screw_clear, h = (csk_d - screw_clear) / 2, $fn = 32);
        }
        // rubber feet
        for (p = [[14, 12], [W - 14, 12], [14, L * cos(tilt) - 10], [W - 14, L * cos(tilt) - 10]])
            translate([p[0], p[1], -0.01]) cylinder(d = foot_d, h = foot_depth + 0.01, $fn = 48);
    }
}

/* MODULES: knob and display clamp */
module knob() {
    d = cfg("knob_d");
    shaft_top = enc_body_h - plate_to_pcb + enc_shaft_l - knob_lift;   // shaft tip in knob coordinates
    n = round(PI * d / 3.2);                                           // grip flutes
    difference() {
        union() {
            cylinder(d = d - 2, h = knob_h, $fn = 96);
            translate([0, 0, 0]) cylinder(d = d, h = knob_h - 1.5, $fn = 96);
            translate([0, 0, knob_h - 1.5]) cylinder(d1 = d, d2 = d - 3, h = 1.5, $fn = 96);
        }
        // grip flutes
        for (i = [0:n-1]) rotate(i * 360 / n) translate([d / 2 + 0.35, 0, 1.5]) cylinder(d = 1.6, h = knob_h, $fn = 12);
        // recess over the encoder body and bushing
        translate([0, 0, -0.01]) cylinder(d = 18.0, h = 1.6, $fn = 64);
        translate([0, 0, -0.01]) cylinder(d = enc_bushing_d + 2.0, h = enc_body_h - plate_to_pcb + enc_bushing_h - knob_lift + 0.8, $fn = 48);
        // D bore (6 mm shaft, flat leaves 4.5 mm)
        intersection() {
            translate([0, 0, -0.01]) cylinder(d = 6.15, h = shaft_top + 0.5, $fn = 48);
            translate([-3.2, 3.075 - 4.65, -0.02]) cube([6.4, 6.4, shaft_top + 1]);
        }
        // indicator dimple
        translate([0, d / 2 - 4, knob_h - 0.6]) cylinder(d = 1.6, h = 1, $fn = 16);
    }
}

module clamp() {
    translate([0, 0, z_clamp_bot]) linear_extrude(clamp_t) clamp_2d();
}

/* MODULES: test coupon (print this first) */
// Four switch holes (13.9 / 14.0 / 14.1 / 14.2, marked with 1-4 dots), two heat-set
// insert holes (insert_d - 0.2 and insert_d) and one M2 pilot. Printed the same way
// as the top shell: top surface down. Use the hole that clicks a switch in firmly.
module test_coupon() {
    sizes = [13.9, 14.0, 14.1, 14.2];
    n = len(sizes);
    len_x = n * pitch + 4;
    difference() {
        union() {
            linear_extrude(skin) rrect([len_x + 22, pitch + 4], 2);
            for (i = [0, 1]) translate([len_x + 6 + i * 10, (pitch + 4) / 2, 0]) cylinder(d = boss_d, h = 10, $fn = 40);
        }
        for (i = [0:n-1]) translate([2 + (i + 0.5) * pitch, 2 + pitch / 2, 0]) {
            translate([0, 0, -1]) linear_extrude(skin + 2) square(sizes[i], center = true);
            translate([0, 0, sw_lip]) linear_extrude(skin) square(sizes[i] + (sw_undercut - sw_hole), center = true);
            for (j = [0:i]) translate([-3.3 + j * 2.2, sizes[i] / 2 + 1.6, -0.01]) cylinder(d = 1.2, h = 0.5, $fn = 12);
        }
        for (i = [0, 1]) translate([len_x + 6 + i * 10, (pitch + 4) / 2, 10 - insert_len - 1])
            cylinder(d = insert_d - 0.2 + i * 0.2, h = insert_len + 2, $fn = 32);
        translate([len_x + 11, 4, -1]) cylinder(d = m2_pilot, h = skin + 2, $fn = 16);
    }
}

/* MODULES: dummy parts for fit checks and renders */
module pcb3d() translate([0, 0, z_pcb_bot]) linear_extrude(pcb_t) pcb_2d();
// Kailh MX socket incl. pads, north-facing switches (socket sits behind the switch centre)
module sockets() for (k = KEYS) translate([k[0] - 7.6, k[1] + 1.3, z_pcb_bot - socket_h + 0.02]) cube([14.0, 5.7, socket_h - 0.04]);
module switch_bodies() for (k = KEYS) translate([k[0], k[1], z_pcb_top + 0.05]) linear_extrude(plate_to_pcb - 0.1) square(13.9, center = true);
module switches() for (k = KEYS) translate(k) {
    translate([0, 0, z_pcb_top]) linear_extrude(plate_to_pcb) square(13.9, center = true);
    hull() { linear_extrude(0.01) crect([15.6, 15.6], 1); translate([0, 0, 5.4]) linear_extrude(0.01) crect([11, 11], 1); }
    translate([0, 0, 5.4]) linear_extrude(6.2) union() { square([4.1, 1.2], center = true); square([1.2, 4.1], center = true); }
}
module keycaps() for (k = KEYS) translate([k[0], k[1], 7.0]) hull() {
    linear_extrude(0.01) crect([18.0, 18.0], 2);
    translate([0, 0, 9.0]) linear_extrude(0.01) crect([14.5, 14.5], 2.5);
}
module encoder() translate(enc_c) {
    translate([0, 0, z_pcb_top + 0.05]) linear_extrude(enc_body_h - 0.05) square(11.9, center = true);
    translate([0, 0, z_pcb_top + enc_body_h]) cylinder(d = enc_bushing_d, h = enc_bushing_h, $fn = 32);
    translate([0, 0, z_pcb_top + enc_body_h]) cylinder(d = 6, h = enc_shaft_l, $fn = 32);
}
module display() {
    translate(disp_c) translate([0, 0, z_glass_bot + 0.02])
        linear_extrude(dsp("glass_t") - 0.04)
        if (round_disp) circle(d = dsp("glass"), $fn = 96); else crect(dsp("glass"));
    translate([0, 0, z_board_bot + 0.02]) linear_extrude(dsp("board_t") - 0.04) board_2d();
}
module mcu() {
    translate([mcu_c[0], mcu_c[1], z_mcu_bot]) linear_extrude(mcu_size[2]) square([mcu_size[0], mcu_size[1]], center = true);
    // USB-C receptacle on the downward-facing component side, at the back edge
    translate([mcu_c[0] - usb_size[0] / 2, usb_face_y - usb_size[1], z_mcu_bot - usb_size[2]]) cube(usb_size);
    // two 12-pin header strips between the PCB and the controller
    for (s = [-1, 1]) translate([mcu_c[0] + s * 7.62 - 1.27, mcu_c[1] - 15.24, z_mcu_top + 0.02]) cube([2.54, 30.48, mcu_gap - 0.04]);
}
module battery() {
    bat = cfg("bat"); lipo = cfg("lipo");
    translate([bat[0], bat[1], bottom_t + 0.05]) rotate(bat[2]) linear_extrude(lipo[0]) crect([lipo[1], lipo[2]], 1);
}
module power_switch() translate([W - wall - 0.3 - psw_size[0], cfg("sw_y") - psw_size[1] / 2, z_psw - psw_size[2] / 2]) {
    cube(psw_size - [0, 0, 0.02]);
    translate([psw_size[0], psw_size[1] / 2 - 0.75, psw_size[2] / 2 - 0.75]) cube([3.0, 1.5, 1.5]);
}

/* REPORT: numbers for the comparison page (printed with echo) */
module report() {
    rear_h = front_h + L * sin(tilt);
    bat = cfg("bat"); lipo = cfg("lipo");
    // lowest point of anything hanging under the plate above the battery footprint
    echo(str("REPORT {",
        "\"concept\":\"", concept, "\",\"name\":\"", cfg("name"), "\",",
        "\"cols\":", cols, ",\"rows\":", rows, ",\"keys\":", cols * rows, ",",
        "\"tilt\":", tilt, ",\"W\":", W, ",\"L\":", L, ",",
        "\"depth_on_desk\":", L * cos(tilt) + (front_h + L * sin(tilt) - bottom_t) * tan(tilt), ",",
        "\"front_h\":", front_h, ",\"rear_h\":", rear_h, ",",
        "\"grid_x0\":", grid_x0, ",\"grid_y0\":", grid_y0, ",\"pitch\":", pitch, ",",
        "\"keys_xy\":", KEYS, ",",
        "\"enc\":", enc_c, ",\"knob_d\":", cfg("knob_d"), ",\"knob_lift\":", knob_lift, ",\"knob_h\":", knob_h, ",",
        "\"disp_type\":\"", dsp("type"), "\",\"disp_label\":\"", dsp("label"), "\",",
        "\"disp_c\":", disp_c, ",\"active\":", dsp("active"), ",\"active_off\":", dsp("active_off"), ",",
        "\"glass\":", dsp("glass"), ",\"px\":", dsp("px"), ",\"bezel_t\":", bezel_t, ",",
        "\"mcu_c\":", mcu_c, ",\"mcu_size\":", mcu_size, ",",
        "\"lipo\":", lipo, ",\"bat\":", bat, ",",
        "\"bosses\":", BOSSES, ",\"pillars\":", PILLARS, ",\"dpillars\":", DPILLARS, ",",
        "\"usb_z\":", z_usb, ",\"skin\":", skin, ",\"corner_r\":", corner_r, ",",
        "\"sw_y\":", cfg("sw_y"), ",\"wall\":", wall, ",\"board_c\":", board_c, ",",
        "\"board_y\":", [board_y0, board_y1],
        "}"));
    // sanity checks
    for (b = BOSSES) let(top = desk_pt([b[0], b[1], -skin])[2] - boss_d / 2 * tan(tilt))
        assert(top - bottom_t >= insert_len + 1.0 + 2.5 + 0.1, str("boss too short at ", b, ": ", top - bottom_t));
}

/* TOP LEVEL */
if (part == "assembly") {
    color("#d9d4c7") top_shell();
    color("#7a7a7a") bottom_plate();
    to_desk() {
        color("#2e7d32") pcb3d();
        color("#333") sockets();
        color("#444") switches();
        color("#f2efe6") keycaps();
        color("#999") encoder();
        color("#c0392b") translate([enc_c[0], enc_c[1], knob_lift]) knob();
        color("#111") display();
        color("#555") clamp();
        color("#1565c0") mcu();
        color("#e0e0e0") power_switch();
    }
    color("#b0bec5") battery();
}
else if (part == "top")          top_shell();
else if (part == "bottom")       bottom_plate();
else if (part == "knob")         to_desk() translate([enc_c[0], enc_c[1], knob_lift]) knob();
else if (part == "clamp")        to_desk() clamp();
else if (part == "pcb")          to_desk() pcb3d();
else if (part == "sockets")      to_desk() sockets();
else if (part == "switches")     to_desk() switches();
else if (part == "switch_bodies") to_desk() switch_bodies();
else if (part == "keycaps")      to_desk() keycaps();
else if (part == "encoder")      to_desk() encoder();
else if (part == "display")      to_desk() display();
else if (part == "mcu")          to_desk() mcu();
else if (part == "battery")      battery();
else if (part == "power_switch") to_desk() power_switch();
else if (part == "top_print")    rotate([180, 0, 0]) rotate([-tilt, 0, 0]) translate([0, 0, -front_h]) top_shell();
else if (part == "bottom_print") bottom_plate();
else if (part == "knob_print")   translate([0, 0, knob_h]) rotate([180, 0, 0]) knob();
else if (part == "clamp_print")  translate([0, 0, -z_clamp_bot]) clamp();
else if (part == "test_coupon")  test_coupon();
else if (part == "pcb_outline")  pcb_2d();
else if (part == "report")       report();
