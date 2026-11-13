"""Full-size, tiled cut pattern for the WAVE 3 window vent panel.

Prints on US Letter (landscape), double-sided, at 100% / Actual size. Each page
carries a 3/4" overlap strip on its right and bottom edges; the next page's
margin is trimmed on its TRIM line and that edge laid on the blue line. Every
pattern page has its own back (taping guide), and the title page's back is blank.
Writes window_vent_pattern.pdf next to this script.
"""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", FD + "DejaVuSans-Bold.ttf"))

IN = 72.0
PW, PH = 11.0, 8.5          # page, landscape, inches
M = 0.5                     # unprinted paper margin (safe for any printer)
PRW, PRH = PW - 2 * M, PH - 2 * M   # printed area per page, 10.5 x 8
OV = 0.75                   # overlap between neighboring pages
SX, SY = PRW - OV, PRH - OV         # step between pages, 9.5 x 7
COLS, ROWS = 4, 2
GW, GH = (COLS - 1) * SX + PRW, (ROWS - 1) * SY + PRH   # 39 x 15 layout

# Panel (inches) - Appendix J, 12 Nov 2026 measurements
PANEL_W, PANEL_H = 34 + 11 / 16, 9.75
X0, Y0 = (GW - PANEL_W) / 2, (GH - PANEL_H) / 2
HOLE_DOWN = 4 + 7 / 8
HOLE_IN = 9 + 11 / 32       # from each panel end (9" from the opening + 11/32" tuck)
TUCK = 11 / 32
EXH = dict(x=X0 + HOLE_IN, d=5 + 1 / 16, name="EXHAUST", size='5 1/16"')
INT = dict(x=X0 + PANEL_W - HOLE_IN, d=6 + 1 / 8, name="INTAKE", size='6 1/8"')
ROUGH = 1 / 8

RED = Color(0.75, 0.12, 0.08)
BLUE = Color(0.15, 0.40, 0.70)
GRAY = Color(0.55, 0.55, 0.55)
LIGHT = Color(0.80, 0.80, 0.80)
FAINT = Color(0.88, 0.88, 0.88)

OUT = Path(__file__).with_name("window_vent_pattern.pdf")


class Tile:
    """Maps layout inches (y down) onto the page for one tile."""
    def __init__(self, c, col, row):
        self.c, self.gx, self.gy = c, col * SX, row * SY

    def p(self, x, y):
        return (M + x - self.gx) * IN, (PH - M - (y - self.gy)) * IN

    def line(self, x1, y1, x2, y2):
        a, b = self.p(x1, y1), self.p(x2, y2)
        self.c.line(*a, *b)

    def circle(self, x, y, r):
        self.c.circle(*self.p(x, y), r * IN, stroke=1, fill=0)

    def text(self, x, y, s, size=10, font="DV", align="c", color=black, angle=0):
        c = self.c
        c.saveState()
        c.setFillColor(color)
        c.setFont(font, size)
        c.translate(*self.p(x, y))
        c.rotate(angle)
        {"c": c.drawCentredString, "l": c.drawString, "r": c.drawRightString}[align](0, 0, s)
        c.restoreState()


def draw_pattern(t):
    c = t.c
    # light 1" grid to help keep the pages square
    c.setStrokeColor(FAINT); c.setLineWidth(0.4); c.setDash()
    for i in range(int(GW) + 1):
        t.line(i, 0, i, GH)
    for j in range(int(GH) + 1):
        t.line(0, j, GW, j)

    # channel / glass zones (do not cut)
    c.setStrokeColor(BLUE); c.setLineWidth(0.8); c.setDash(6, 4)
    t.line(X0, Y0 + 3 / 8, X0 + PANEL_W, Y0 + 3 / 8)
    t.line(X0, Y0 + PANEL_H - 3 / 8, X0 + PANEL_W, Y0 + PANEL_H - 3 / 8)
    t.line(X0 + TUCK, Y0, X0 + TUCK, Y0 + PANEL_H)
    t.line(X0 + PANEL_W - TUCK, Y0, X0 + PANEL_W - TUCK, Y0 + PANEL_H)
    for x in (X0 + 6, X0 + 17, X0 + 28.5):
        t.text(x, Y0 + 0.62, 'top 3/8" goes into the top channel (not a cut line)', 7.5, color=BLUE)
        t.text(x, Y0 + PANEL_H - 0.5, 'glass pinches the bottom 3/8" (not a cut line)', 7.5, color=BLUE)
    for x, a in ((X0 + TUCK + 0.14, 90), (X0 + PANEL_W - TUCK - 0.14, -90)):
        t.text(x, Y0 + PANEL_H / 2 + (0.0), 'about 11/32" sits in the side channel', 7, color=BLUE, angle=a)

    # center line
    c.setStrokeColor(GRAY); c.setLineWidth(0.6); c.setDash([10, 3, 2, 3])
    t.line(X0 - 0.4, Y0 + HOLE_DOWN, X0 + PANEL_W + 0.4, Y0 + HOLE_DOWN)

    # outer cut line
    c.setDash(); c.setStrokeColor(black); c.setLineWidth(2.2)
    c.rect(*t.p(X0, Y0 + PANEL_H), PANEL_W * IN, PANEL_H * IN, stroke=1, fill=0)

    # holes
    yc = Y0 + HOLE_DOWN
    for h in (EXH, INT):
        r = h["d"] / 2
        c.setDash(); c.setStrokeColor(black); c.setLineWidth(2.0)
        t.circle(h["x"], yc, r)
        c.setStrokeColor(RED); c.setLineWidth(1.0); c.setDash(5, 3)
        t.circle(h["x"], yc, r - ROUGH)
        c.setDash(); c.setStrokeColor(black); c.setLineWidth(0.6)
        t.line(h["x"] - 0.3, yc, h["x"] + 0.3, yc)
        t.line(h["x"], yc - 0.3, h["x"], yc + 0.3)
        t.text(h["x"], yc - 1.25, h["name"], 13, "DVB")
        t.text(h["x"], yc - 0.98, "hole " + h["size"], 10)
        t.text(h["x"], yc + 0.75, "rough-cut the red dashed circle first,", 7.5, color=RED)
        t.text(h["x"], yc + 0.95, "then open up to the black line to fit the collar", 7.5, color=RED)
        t.text(h["x"], yc + 0.5, "center", 7, color=GRAY)
        for k in range(8):   # CUT ticks around the hole, outside it
            import math
            a = k * math.pi / 4 + math.pi / 8
            rr = r + 0.28
            t.text(h["x"] + rr * math.cos(a), yc + rr * math.sin(a) + 0.04, "CUT", 6.5, "DVB")

    # labels on the outer cut line
    for x in [X0 + 1.5 + 3.5 * i for i in range(10)]:
        t.text(x, Y0 - 0.12, "✂ CUT", 9, "DVB")
        t.text(x, Y0 + PANEL_H + 0.3, "✂ CUT", 9, "DVB")
    for y in (Y0 + 2.5, Y0 + 7.25):
        t.text(X0 - 0.15, y, "✂ CUT", 9, "DVB", angle=90)
        t.text(X0 + PANEL_W + 0.15, y, "✂ CUT", 9, "DVB", angle=-90)

    # match targets in each overlap (printed on both pages)
    c.setDash(); c.setStrokeColor(black); c.setLineWidth(0.6)
    targets = [(k * SX + OV / 2, y) for k in range(1, COLS) for y in (1.2, 4.2, 10.4, 13.6)]
    targets += [(k * SX + 4.0, SY + OV / 2) for k in range(COLS)]
    for x, y in targets:
        t.circle(x, y, 0.12)
        t.line(x - 0.25, y, x + 0.25, y)
        t.line(x, y - 0.25, x, y + 0.25)

    t.text(X0 + PANEL_W / 2, Y0 + 8.1, "INSIDE FACE", 26, "DVB", color=LIGHT)
    t.text(X0 + 0.65, Y0 + 1.25, "REAR end", 11, "DVB", "l")
    t.text(X0 + PANEL_W - 0.65, Y0 + 1.25, "FRONT end →", 11, "DVB", "r")
    t.text(X0 + PANEL_W - 0.65, Y0 + 1.5, "(your right, from inside the van)", 7.5, align="r", color=GRAY)

    # check dimensions
    c.setStrokeColor(GRAY); c.setLineWidth(0.6); c.setDash()
    t.line(EXH["x"], Y0 + HOLE_DOWN + 1.6, INT["x"], Y0 + HOLE_DOWN + 1.6)
    t.text((EXH["x"] + INT["x"]) / 2, Y0 + HOLE_DOWN + 1.5, 'centers 16" apart (check with a tape)', 8, color=GRAY)
    t.line(X0, Y0 - 0.9, X0 + PANEL_W, Y0 - 0.9)
    t.text(X0 + PANEL_W / 2, Y0 - 1.0, 'panel 34 11/16" x 9 3/4"   ·   holes 4 7/8" down, 9 11/32" in from each end', 9, color=GRAY)


def tile_name(col, row):
    return "ABCD"[col] + str(row + 1)


def draw_frame(t, col, row):
    c = t.c
    tint = Color(0.15, 0.40, 0.70, alpha=0.10)
    top = PH - M            # paper y (points/IN) of the printed area's top
    name = tile_name(col, row)
    # overlap strips: the next page lies on these
    if col < COLS - 1:
        ex = M + SX          # where the next page's trimmed edge lands (paper inches)
        c.setFillColor(tint); c.rect(ex * IN, M * IN, (PW - M - ex) * IN, PRH * IN, stroke=0, fill=1)
        c.setStrokeColor(BLUE); c.setLineWidth(1.6); c.setDash()
        c.line(ex * IN, M * IN, ex * IN, top * IN)
        c.setFillColor(BLUE); c.setFont("DVB", 9)
        for yy in (2.2, 6.3):
            c.saveState(); c.translate((ex + 0.22) * IN, yy * IN); c.rotate(-90)
            c.drawCentredString(0, 0, "OVERLAP: page " + tile_name(col + 1, row) + " goes on top")
            c.restoreState()
            c.saveState(); c.translate((ex + 0.42) * IN, yy * IN); c.rotate(-90)
            c.setFont("DV", 7.5)
            c.drawCentredString(0, 0, "its trimmed edge on the blue line, targets matched")
            c.setFont("DVB", 9); c.restoreState()
    if row < ROWS - 1:
        ey = PH - M - SY     # paper y where the page below's trimmed edge lands
        c.setFillColor(tint); c.rect(M * IN, M * IN, PRW * IN, (ey - M) * IN, stroke=0, fill=1)
        c.setStrokeColor(BLUE); c.setLineWidth(1.6); c.setDash()
        c.line(M * IN, ey * IN, (PW - M) * IN, ey * IN)
        c.setFillColor(BLUE); c.setFont("DVB", 9)
        c.drawCentredString(PW / 2 * IN, (ey - 0.2) * IN, "OVERLAP: page " + tile_name(col, row + 1) + " goes on top, its trimmed top edge on the blue line")
        c.setFont("DV", 7.5)
        c.drawCentredString(PW / 2 * IN, (ey - 0.36) * IN, "match the targets (hold to a window or lamp to see through), then tape on the back along its edge")
    # edges that lie on top of a neighbor: trim the margin off on these
    c.setStrokeColor(black); c.setLineWidth(1.0); c.setDash(4, 3)
    c.setFillColor(black)
    if col > 0:
        c.line(M * IN, 0, M * IN, PH * IN)
        for yy in (1.6, PH / 2, PH - 1.6):
            c.saveState(); c.translate((M - 0.12) * IN, yy * IN); c.rotate(90)
            c.setFont("DVB", 8); c.drawCentredString(0, 0, "\u2702 TRIM on the dashed line")
            c.restoreState()
        c.saveState(); c.translate((M + 0.14) * IN, (PH / 2) * IN); c.rotate(90)
        c.setFont("DV", 7.5); c.setFillColor(BLUE)
        c.drawCentredString(0, 0, "then lay this edge on the blue line of page " + tile_name(col - 1, row))
        c.restoreState(); c.setFillColor(black)
    if row > 0:
        c.line(0, top * IN, PW * IN, top * IN)
        c.setFont("DVB", 8)
        for xx in (2.2, PW - 2.2):
            c.drawCentredString(xx * IN, (top + 0.1) * IN, "\u2702 TRIM on the dashed line")
        c.setFont("DV", 7.5); c.setFillColor(BLUE)
        c.drawCentredString(PW / 2 * IN, (top - 0.14) * IN, "then lay this edge on the blue line of page " + tile_name(col, row - 1))
    c.setDash()
    # page name, mini map, 2" check: top-left on row 1, bottom-left on row 2
    ly = (top - 0.45) if row == 0 else (M + 0.2)
    lx = M + (0.35 if col > 0 else 0.1)
    c.setFillColor(black); c.setFont("DVB", 15)
    c.drawString(lx * IN, ly * IN, "Page " + name)
    mx, cw, ch = (lx + 1.05) * IN, 0.22 * IN, 0.13 * IN
    c.setStrokeColor(black); c.setLineWidth(0.5); c.setDash()
    for i in range(COLS):
        for j in range(ROWS):
            c.setFillColor(black if (i, j) == (col, row) else Color(1, 1, 1))
            c.rect(mx + i * cw, ly * IN + ch - j * ch, cw, ch, stroke=1, fill=1)
    sx, sy = (lx + 2.2) * IN, (ly + 0.08) * IN
    c.setStrokeColor(black); c.setLineWidth(1)
    c.line(sx, sy, sx + 2 * IN, sy)
    for k in range(3):
        c.line(sx + k * IN, sy - 4, sx + k * IN, sy + 4)
    c.setFillColor(black); c.setFont("DV", 7)
    c.drawString(sx + 2 * IN + 6, sy - 2, 'must measure exactly 2"; if not, reprint at 100% / Actual size')


def back(c, col, row):
    """Back of a pattern page: where the tape goes. Seen from the back, the
    page's right edge is on the left (short-edge flip)."""
    name = tile_name(col, row)
    tint = Color(0.80, 0.55, 0.10, alpha=0.18)
    ink = Color(0.55, 0.33, 0.02)
    c.setFillColor(LIGHT); c.setFont("DVB", 40)
    c.drawCentredString(PW / 2 * IN, PH / 2 * IN, "back of page " + name)
    c.setFont("DV", 10); c.setFillColor(GRAY)
    c.drawCentredString(PW / 2 * IN, (PH / 2 - 0.4) * IN, "the pattern is on the other side \u00b7 tape the seams on this side")
    c.setFillColor(ink)
    if col < COLS - 1:      # this page's right edge, seen from the back: left
        c.setFillColor(tint); c.rect(M * IN, M * IN, 0.9 * IN, (PH - 2 * M) * IN, stroke=0, fill=1)
        c.setFillColor(ink); c.setFont("DVB", 10)
        for yy in (2.0, PH - 2.0):
            c.saveState(); c.translate((M + 0.35) * IN, yy * IN); c.rotate(90)
            c.drawCentredString(0, 0, "\u25c4 TAPE over this edge onto page " + tile_name(col + 1, row))
            c.restoreState()
    if row < ROWS - 1:      # this page's bottom edge
        c.setFillColor(tint); c.rect(M * IN, M * IN, (PW - 2 * M) * IN, 0.9 * IN, stroke=0, fill=1)
        c.setFillColor(ink); c.setFont("DVB", 10)
        c.drawCentredString(PW / 2 * IN, (M + 0.35) * IN, "\u25bc TAPE over this edge onto page " + tile_name(col, row + 1))
    if col == COLS - 1 and row == ROWS - 1:
        c.setFont("DV", 10)
        c.drawCentredString(PW / 2 * IN, (PH / 2 - 0.8) * IN, "nothing to tape from this page: tape from C2 and D1 lands here")
    c.setFillColor(GRAY); c.setFont("DV", 7.5)
    c.drawCentredString(PW / 2 * IN, (PH - 0.4) * IN,
        "If the tape strip isn't along the edge that meets the next page, your printer flipped the other way: tape along that edge anyway.")


def cover(c):
    M = 0.75
    c.setFillColor(black)
    c.setFont("DVB", 22); c.drawString(M * IN, (PH - 1.0) * IN, "WAVE 3 Window Vent Panel — full-size cut pattern")
    c.setFont("DV", 10)
    lines = [
        "Driver-side sliding door, Appendix J (Option B). Panel 34 11/16\" x 9 3/4\"; intake 6 1/8\", exhaust 5 1/16\", centers 4 7/8\" down,",
        "9 11/32\" in from each end, 16\" apart.",
        "",
        "1.  Print double-sided (flip on SHORT edge), Letter, landscape, at 100% / Actual size, NOT Fit. Check the 1\" square below.",
        "2.  On pages B-D and row 2, cut off the margin on the dashed TRIM line (left edge, and top edge on row 2).",
        "3.  Row 1: lay B1's trimmed edge on A1's blue line, match the targets and lines (hold to a window), then C1, D1.",
        "    Tape each seam on the back where the backs show the tape strip. Row 2 the same, then onto row 1's bottom strip.",
        "4.  Lay the pattern on the poster board with the INSIDE FACE up, square to a factory corner if you can.",
        "    Tape it down all round. Hold the overlap's board edge flat where it crosses the intake hole.",
        "5.  Cut the outer black line through pattern and board with a box cutter and straightedge.",
        "6.  Cut the holes on the red dashed circles first (1/8\" small). Open them up to the black line as you fit the collars.",
        "7.  Blue dashed lines are where the channels and glass grip the panel. They are not cut lines.",
        "8.  Peel the pattern off, or leave it on and write the fit results on it. Then test-fit in the window (Template sheet).",
    ]
    y = PH - 1.45
    for s in lines:
        c.drawString(M * IN, y * IN, s); y -= 0.24
    # map
    mx, my, cw = M * IN, 0.75 * IN, 1.4 * IN
    s = cw / SX
    ch = SY * s
    c.setFont("DVB", 11); c.drawString(mx, my + 2 * ch + 10, "Assembly map (inside face up, front of the van on the right)")
    c.setLineWidth(0.8)
    for i in range(COLS):
        for j in range(ROWS):
            c.setStrokeColor(GRAY); c.rect(mx + i * cw, my + 2 * ch - j * ch - PRH * s, PRW * s, PRH * s, stroke=1, fill=0)
            c.setFont("DVB", 14); c.setFillColor(LIGHT)
            c.drawCentredString(mx + (i + .5) * cw, my + (1 - j) * ch + ch / 2 - 5, tile_name(i, j))
    def mp(x, y):
        return mx + x * s, my + 2 * ch - y * s
    c.setStrokeColor(black); c.setLineWidth(1.5)
    c.rect(*mp(X0, Y0 + PANEL_H), PANEL_W * s, PANEL_H * s, stroke=1, fill=0)
    for h in (EXH, INT):
        c.circle(*mp(h["x"], Y0 + HOLE_DOWN), h["d"] / 2 * s, stroke=1, fill=0)
    # legend
    lx, ly = (M + 6.6) * IN, 2.75 * IN
    c.setFillColor(black); c.setFont("DVB", 11); c.drawString(lx, ly, "Lines")
    items = [(black, 2.2, None, "cut (final line)"), (RED, 1.0, (5, 3), "rough-cut the holes here first"),
             (BLUE, 0.8, (6, 4), "channel / glass grip, do not cut"), (GRAY, 0.6, (10, 3, 2, 3), "hole center line")]
    for k, (col, w, d, txt) in enumerate(items):
        yy = ly - 0.3 * IN * (k + 1)
        c.setStrokeColor(col); c.setLineWidth(w); c.setDash(list(d)) if d else c.setDash()
        c.line(lx, yy + 3, lx + 0.6 * IN, yy + 3)
        c.setDash(); c.setFont("DV", 9); c.drawString(lx + 0.75 * IN, yy, txt)
    # 1" test square
    c.setStrokeColor(black); c.setLineWidth(0.8)
    c.rect(lx, 0.5 * IN, IN, IN, stroke=1, fill=0)
    c.setFont("DV", 8); c.drawString(lx + IN + 8, 1.2 * IN, '1" square:'); c.drawString(lx + IN + 8, 1.05 * IN, 'check with a ruler'); c.drawString(lx + IN + 8, 0.9 * IN, 'before printing the rest')


def main():
    c = canvas.Canvas(str(OUT), pagesize=(PW * IN, PH * IN))
    c.setTitle("WAVE 3 window vent panel - full-size cut pattern")
    cover(c); c.showPage()
    c.setFillColor(GRAY); c.setFont("DV", 9)
    c.drawCentredString(PW / 2 * IN, PH / 2 * IN, "(back of the title page, left blank)")
    c.showPage()
    for row in range(ROWS):
        for col in range(COLS):
            t = Tile(c, col, row)
            c.saveState()
            path = c.beginPath()
            path.rect(M * IN, M * IN, PRW * IN, PRH * IN)
            c.clipPath(path, stroke=0, fill=0)
            draw_pattern(t)
            c.restoreState()
            draw_frame(t, col, row)
            c.showPage()
            back(c, col, row)
            c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
