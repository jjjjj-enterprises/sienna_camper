// ============================================================
// Fridge installation detail — zoomed top-down view of Panel C
// ============================================================
// The whole-vehicle top_view.scad is too small-scale to label the
// fridge's 2 fans, temperature sensor, cabinet door, and floor
// anchors clearly (they're packed into Panel C's 46in x 36in
// footprint). This file draws JUST Panel C, at a scale where every
// component gets its own numbered marker — pairs with rear_view.scad
// (elevation), fridge_slide_detail.scad (the slide mechanism, side
// profile), and fridge_wiring.scad (the electrical side).
//
// Numbered markers + a side list (not inline labels scattered across
// the drawing) — an early draft tried inline labels and every one of
// them collided with something else in this tight a footprint.
//
// AIRFLOW (owner question, July 2026): the intake fan on Panel C's
// FRONT wall blows cabin air IN, it crosses the fridge's compressor
// end, and the exhaust fan on the fridge bay's RIGHT (kitchen-
// facing) side blows it INTO the utility cabinet — the door isn't
// airtight, so it leaks back out around the edges. Arrows drawn.
// The control panel lives in the OPEN utility bay between the
// fridge and kitchen (no door — the old hinged, louvered door was
// cut as pointless), on a backer board hung from the deck underside
// (the 3/4" sheet's offcut) — reach it by hand. Also here: the
// NO-DRILL ANCHOR BOARD for both the fridge's slide and the kitchen
// unit (Oct 2026 redesign) — three separate one-piece 3/4in ply strips
// on 1/8in neoprene, tied by two 2 x 3/16in steel rungs set into their
// undersides, strapped forward and down to the 3rd-row seats' latch
// hoops H1-H4 in the headrest trough — see "Securing heavy components"
// (Section 8) for why the factory cargo hooks aren't used for
// either, and why nothing bolts to the van (owner: no holes).
//
// COORDINATE SYSTEM (also used in the build-plan coordinate table):
// origin (0,0) is Panel C's TAILGATE-FACING, LEFT corner, at floor
// level (as you'd stand at the open tailgate facing forward into the
// van). X increases to the RIGHT, 0 to 46in (panel_width). Y
// increases FORWARD (toward the Panel B seam), 0 to 36in
// (panel_c_length). This is the reverse of top_view.scad's own
// internal Y convention (increases toward the FRONT of the whole
// vehicle) and platform.scad's true 3D model convention (increases
// toward the TAILGATE) — both exist for other reasons already
// explained in their own files. This one reads most naturally for
// "how far in from the tailgate, how far over from the left" — the
// two questions you actually ask while installing something back
// here.
//
// Render with: openscad -o renders/fridge-install-detail.svg fridge_install_detail.scad
// ============================================================
// LEGIBILITY (Aug 2026): 6 prose line(s) moved out of this
// sheet into the document, and every text size scaled x2.4. Those
// sentences were setting the sheet's width, and a figure's printed
// text height is size x (page_width / sheet_width) — so they were
// holding every other label on the sheet down to 3-6pt on paper.
// Keep prose in the markdown; this sheet carries geometry and short
// labels only.

include <params.scad>
include <colors.scad>

stroke = 0.25;

module rect_outline(w, l, s = stroke) {
    color("black")
    difference() {
        square([w, l]);
        translate([s, s]) square([w - 2*s, l - 2*s]);
    }
}

module label(txt, x, y, size = 3.36) {
    color("black")
    translate([x, y]) text(txt, size = size, halign = "center", valign = "center");
}

module label_left(txt, x, y, size = 2.88) {
    color("black")
    translate([x, y]) text(txt, size = size, halign = "left", valign = "center");
}

// Numbered marker: a filled circle with a white number, used in the
// drawing; the matching number in the side list gives the real
// coordinates, description, and fastener spec.
// nx: which side the numeral sits on (+ right, - left). OpenSCAD merges
// TOUCHING 2D shapes into one polygon set and paints them a single colour, so
// a white numeral inside a filled circle disappears — every marker on this
// sheet rendered as an unreadable coloured blob. The numeral goes beside the
// icon instead, on whichever side is clear.
module marker(n, x, y, col, nx = 2.1) {
    // numbered AND hue-coded (marker_col, colors.scad) — number
    // pairs to the table row, color separates markers at a glance
    translate([x, y]) {
        color(marker_col(n)) circle(r = 1.3);
        color(marker_col(n)) translate([nx, 0])
            text(str(n), size = 3.0, halign = nx > 0 ? "left" : "right",
                 valign = "center");
    }
}

// anchor-board strip (neoprene + 3/4in ply) — drawn as an outline with
// diagonal section-hatching so it stays LINE ART (filled shapes
// union into solid blobs in OpenSCAD's monochrome SVG export) —
// the no-drill securing chassis, Section 8
module board_strip(x0, y0, w, l) {
    board_poly([[x0, y0], [x0 + w, y0], [x0 + w, y0 + l], [x0, y0 + l]]);
}

// one strip's hatched outline
module board_poly(pts) {
    xs = [for (p = pts) p[0]];  ys = [for (p = pts) p[1]];
    x0 = min(xs); y0 = min(ys); w = max(xs) - x0; l = max(ys) - y0;
    color("Peru") difference() {
        polygon(pts);
        offset(delta = -0.15) polygon(pts);
    }
    color("Tan") intersection() {
        offset(delta = -0.3) polygon(pts);
        union() {
            for (d = [2 : 4 : w + l])
                translate([x0, y0 + d]) rotate(-45) square([(w + l) * 1.5, 0.1]);
        }
    }
}

// steel rung UNDER the strips: a dashed outline (hidden line)
module rung_dashed(x0, y0, w, l) {
    color("SlateGray") {
        for (dx = [0 : 1.6 : w - 0.8]) {
            translate([x0 + dx, y0]) square([0.8, 0.15]);
            translate([x0 + dx, y0 + l - 0.15]) square([0.8, 0.15]);
        }
        translate([x0, y0]) square([0.15, l]);
        translate([x0 + w - 0.15, y0]) square([0.15, l]);
    }
}

// a strap drawn as a line between two plan points (dashed = optional)
module strap_line(a, b, dashed = false) {
    v = b - a; n = norm(v);
    color("Firebrick")
        if (!dashed)
            hull() { translate(a) circle(r = 0.2, $fn = 12); translate(b) circle(r = 0.2, $fn = 12); }
        else
            for (t = [0 : 1.6 / n : 1 - 0.8 / n])
                hull() { translate(a + v * t) circle(r = 0.2, $fn = 12); translate(a + v * min(1, t + 0.8 / n)) circle(r = 0.2, $fn = 12); }
}

// 3rd-row seat-latch hoop (3in wide), seen from above
module hoop_icon(x, y, name) {
    color("Black") translate([x - aboard_hoop_w/2, y - 0.4]) difference() {
        square([aboard_hoop_w, 0.8]);
        translate([0.2, 0.2]) square([aboard_hoop_w - 0.4, 0.4]);
    }
    label(name, x, y + 1.5, 1.0);
}

// shackle in a riser's front end
module shackle_icon(x, y) {
    color("Goldenrod") translate([x, y]) difference() { circle(r = 0.5, $fn = 24); circle(r = 0.28, $fn = 20); }
}

// stainless footman loop, lengthwise on a strip
module footman_icon(x, y0, y1) {
    color("ForestGreen") translate([x - 0.35, y0]) difference() {
        square([0.7, y1 - y0]);
        translate([0.15, 0.15]) square([0.4, y1 - y0 - 0.3]);
    }
}

module drawing() {
    z_deck = leg_height + frame_rail_sz;
    kitchen_x0 = x_kitchen - kitchen_box_width/2 + panel_width/2; // 24.375 — against the passenger rear corner leg (1.5in in from the edge)
    fridge_x0  = x_fridge_module - fridge_ext_length/2 + panel_width/2;

    // ---- NO-DRILL ANCHOR BOARD (Section 8, Oct 2026) — drawn FIRST so
    // every component sits on top of it. Three separate one-piece strips
    // (neoprene + 3/4in ply), 3"-26" from the hatch, tied by two steel
    // rungs set into their undersides (dashed: hidden under the strips,
    // the fridge tray and the kitchen unit). No crossbar, no tongues. ----
    for (st = aboard_strips)
        board_strip(st[0], aboard_y0, st[1] - st[0], aboard_strip_len);
    for (ry = aboard_rungs_y)
        rung_dashed(0, ry, aboard_rung_len, aboard_rung_w);
    // the 3rd-row seat-latch hoops H1-H4, in the headrest trough
    for (i = [0 : 3])
        hoop_icon(aboard_hoops_x[i], aboard_hoop_y, str("H", i + 1));
    // board straps: a shackle in each riser's front end -> H1 (driver
    // riser) and H2 (kitchen riser), forward and down
    shackle_y = fridge_riser_y0 + fridge_riser_len - 0.5;
    for (i = [0, 1]) {
        st = aboard_strips[i];
        sx = (st[0] + st[1]) / 2;
        strap_line([sx, shackle_y], [aboard_hoops_x[i], aboard_hoop_y]);
        shackle_icon(sx, shackle_y);
    }
    // kitchen tie-down: front strap (front notches) down to H2 and H4,
    // rear strap (rear notches) down to the two footman loops
    k_front_y = kitchen_hatch_inset + kitchen_box_length - 2;
    k_rear_y  = kitchen_hatch_inset + 2.3;
    loop_y    = (aboard_loop_y[0] + aboard_loop_y[1]) / 2;
    loop_xs   = [aboard_strips[1][1] - 0.375, (aboard_strips[2][0] + aboard_strips[2][1]) / 2];
    for (lx = loop_xs) footman_icon(lx, aboard_loop_y[0], aboard_loop_y[1]);
    strap_line([kitchen_x0, k_front_y], [kitchen_x0 + kitchen_box_width, k_front_y]);
    strap_line([kitchen_x0, k_front_y], [aboard_hoops_x[1], aboard_hoop_y]);
    strap_line([kitchen_x0 + kitchen_box_width, k_front_y], [aboard_hoops_x[3], aboard_hoop_y]);
    strap_line([kitchen_x0, k_rear_y], [kitchen_x0 + kitchen_box_width, k_rear_y]);
    strap_line([kitchen_x0, k_rear_y], [loop_xs[0], loop_y]);
    strap_line([kitchen_x0 + kitchen_box_width, k_rear_y], [loop_xs[1], loop_y]);
    // optional backup straps (dashed) forward from the front rung to the
    // 3rd-row striker loops, under Panel C's front edge (off the top of
    // the drawing) — through the relief-notch bands, if cut
    for (bx = [14.25, 31.75]) {
        strap_line([bx, aboard_rungs_y[1] + aboard_rung_w / 2], [bx, panel_c_length + 4], true);
        color("Firebrick") translate([bx, panel_c_length + 4]) polygon([[0, 1.6], [-0.9, 0], [0.9, 0]]);
    }
    marker(9, aboard_strips[0][1] + 1.6, aboard_hoop_y - 1.6, "Firebrick", 2.1);
    marker(10, 31.75 - 1.7, panel_c_length + 4.5, "Firebrick", -2.1);

    // Panel C outline (the full 46in x 36in deck footprint)
    rect_outline(panel_width, panel_c_length);
    label(str("PANEL C — ", panel_width, "\" wide x ", panel_c_length, "\" deep, looking down from above"),
          panel_width/2, panel_c_length + 17, 1.6);
    label("TAILGATE (open) — Y = 0 here", panel_width/2, -2, 1.4);
    label("DRIVER side (X=0)", 8, -5.4, 1.1);
    label("PASSENGER side", panel_width - 8, -5.4, 1.1);
    label_left("Y, in.", -6, panel_c_length/2, 1.2);
    label_left("(toward Panel B)", -9, panel_c_length/2 - 1.8, 0.9);
    label("X, in. (left to right) ->", panel_width/2, -3.8, 1.1);

    // Kitchen unit footprint + floor anchors
    translate([kitchen_x0, kitchen_hatch_inset]) {
        color("Gainsboro") rect_outline(kitchen_box_width, kitchen_box_length);
        label("Kitchen unit", kitchen_box_width/2, kitchen_box_length - 3, 1.3);
        label("(JAGAHAHA)", kitchen_box_width/2, kitchen_box_length - 5, 1.1);
        label(str(kitchen_box_width, "\" x ", kitchen_box_length, "\""), kitchen_box_width/2, kitchen_box_length - 7, 1.1);
        label("slides out tailgate (-Y)", kitchen_box_width/2, 2.5, 1.0);
    }
    marker(6, kitchen_x0 + kitchen_box_width - 3, 6.5, "DimGray", -2.1); // kitchen tie-down: 2 straps, to H2/H4 and to the footman loops

    // Fridge footprint — name/description text kept in the UPPER
    // third of the box (Y=15-22), well clear of the intake fan
    // marker at the very top (Y=22.68) and leaving the lower 2/3 of
    // the box free for markers.
    translate([fridge_x0, 0]) {
        color("DimGray") rect_outline(fridge_ext_length, fridge_ext_width);
        label("Fridge", fridge_ext_length/2, 19, 1.2);
        label("(BougeRV)", fridge_ext_length/2, 17, 1.0);
        label("out tailgate (-Y)", fridge_ext_length/2, 15, 0.9);

        // exhaust fan + NTC sensor: on the RIGHT (kitchen-facing,
        // high-X) side of the fridge bay — blows INTO the utility
        // cabinet (the door isn't airtight; air leaks back out)
        marker(2, fridge_ext_length, fridge_ext_width/2, "Silver", -2.1);
        marker(3, fridge_ext_length - 1.5, fridge_ext_width/2 - 2.2, "GreenYellow", -2.1);
    }
    // intake fan: on Panel C's FRONT wall (the panel's one wall),
    // over its pre-cut fan hole — Panel C Front Wall render
    marker(1, fridge_x0 + fridge_ext_length/2, panel_c_length + 0.8, "DarkGray");

    // ---- airflow arrows: in through the front wall, across the
    // fridge, out into the cabinet ----
    module flow_arrow(x0, y0, x1, y1) {
        color("SteelBlue") {
            hull() { translate([x0, y0]) circle(r = 0.25, $fn = 12); translate([x1, y1]) circle(r = 0.25, $fn = 12); }
            dx = x1 - x0; dy = y1 - y0; n = norm([dx, dy]);
            translate([x1, y1]) rotate(atan2(dy, dx))
                polygon([[0, 0], [-1.6, 0.9], [-1.6, -0.9]]);
        }
    }
    flow_arrow(fridge_x0 + fridge_ext_length/2, panel_c_length + 1.5, fridge_x0 + fridge_ext_length/2, panel_c_length - 3.5);
    flow_arrow(fridge_x0 + 3, 10, fridge_x0 + fridge_ext_length - 2, 10);
    flow_arrow(fridge_x0 + fridge_ext_length - 2, fridge_ext_width/2, fridge_x0 + fridge_ext_length + 3.5, fridge_ext_width/2);
    // MOVED TO THE DOCUMENT: color("SteelBlue") translate([fridge_x0 + 2, 7.2]) text("airflow: cool air in at the front wall (fan + a low passive louver), across the fridge, OUT through the OPEN utility bay toward the tailgate (no door)", size = 2.28);
    // the 2 slide rails stand VERTICALLY flanking the tray (side-mount
    // — see fridge-slide-detail): drawn as the 2 narrow bands beside
    // the fridge, set back ~2.5in from the tailgate face so the
    // driver-side one clears the rear corner leg. Each rail's steel
    // riser bolts to the anchor-board strip drawn under these rail
    // lines (T-nuts from below — no floor holes), never under the tray.
    rail_xs = [fridge_x0 - fridge_slide_margin - fridge_rail_t,
               fridge_x0 + fridge_ext_length + fridge_slide_margin];
    for (rx = rail_xs)
        color("DimGray") translate([rx, fridge_riser_y0]) rect_outline(fridge_rail_t, fridge_riser_len, 0.12);
    marker(5, rail_xs[1] + fridge_rail_t/2, 27.5, "DimGray", -2.1);

    // Fridge hold-down strap D-rings (x2, tray side apron — separate
    // from the anchor board's straps above: these secure the FRIDGE to
    // its TRAY, not the tray to the van floor) — side profile + strap
    // geometry is in fridge-slide-detail.svg
    color("Firebrick") translate([fridge_x0 + fridge_ext_length/2 - 0.3, 1.3]) circle(r = 0.3, $fn = 20);
    marker(8, fridge_x0 + fridge_ext_length/2, 3.2, "Firebrick");

    // OPEN utility bay — the gap between the fridge module (left/
    // driver) and the kitchen unit (right/passenger). NO door: the
    // old hinged, louvered door was cut as pointless — the open bay
    // vents the exhaust air straight out the tailgate face and the
    // switches are reached by hand.
    bay_x0 = fridge_x0 + fridge_ext_length + fridge_slide_margin + fridge_rail_stack; // past the passenger-side rail + riser
    bay_w  = kitchen_x0 - bay_x0;
    color("black") translate([bay_x0 + 0.6, 16]) rotate(90) text("OPEN BAY", size = 1.8, halign = "left", valign = "center");
    flow_arrow(bay_x0 + bay_w/2 + 0.6, 6.2, bay_x0 + bay_w/2 + 0.6, -0.9); // exhaust air exits the open bay toward the tailgate

    // WAVE 3 hose/cord storage hook — in the open bay's void (under
    // the deck, same depth as the fridge/kitchen bays), screwed up
    // into the deck underside at the bay's kitchen side
    marker(7, bay_x0 + bay_w/2, 10, "Silver");

    // Control panel — at the tailgate end of the OPEN utility bay,
    // on a backer board hung from the deck underside (Z in the
    // side list; a top-down view only shows its footprint).
    // MOVED Aug 2026: the cluster is on the FRONT WALL's Panel-B face now, not
    // in the bay — the bay came out 1.28in wide. In this top-down the front
    // wall is the far edge (Y = panel_c_length), so the cluster's footprint is
    // a thin band just BEYOND it, standing off into Panel B.
    ctrl_x0 = cluster_x;
    color("Black") translate([ctrl_x0, panel_c_length])
        rect_outline(cluster_w, cluster_proj);
    marker(4, ctrl_x0 + cluster_w/2, panel_c_length + cluster_proj + 2.4, "Black");
    // MOVED TO THE DOCUMENT: label("(4 sits in the OPEN utility bay — Z in the list.", panel_width/2, -7.6, 1.05);
    // MOVED TO THE DOCUMENT: label("CO monitor + fire extinguisher: owner-placed, not located here)", panel_width/2, -9.3, 1.05);

    // ---- the numbered markers above are the whole legend ----
    // A 10-row x 3-line side list used to be printed here. Its longest line
    // was 180 characters, which made this sheet ~160 units wide against a
    // 46in-wide plan — and printed text height is size x (page_width /
    // sheet_width), so every label on the sheet, including the coordinates
    // themselves, came out near 3pt. The full table (component, coordinates,
    // fastener) is in the document directly under this figure, where it is
    // legible and searchable. Markers 1-10 index into it.
    label("Markers 1-10: see the component table under this figure",
          panel_width/2, -8.6, 1.6);
}

// NOTE: no outer color("black") wrapper here — every helper above
// (rect_outline, label, label_left, marker, anchor_icon) already
// self-colors, and OpenSCAD's camera-preview PNG render does not let
// a nested color() override an OUTER color() wrapping it (the
// outermost color in scope always wins). See top_view.scad/
// rear_view.scad for the same fix applied after this exact bug was
// found mid-project.
drawing();
