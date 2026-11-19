#!/usr/bin/env python3
"""Build-time renderer for THE WORLD, 18 November 2026.

Draws a 1024x1024 newspaper front page with Pillow and real fonts, then
writes entry.png next to this file. Build-time only: the submitted program
(main.ts) just copies entry.png, so the entry runs offline with no keys
and no network. Rendering is deterministic: same fonts, same text, same
bytes every run (Pillow writes no timestamps into the PNG).

Layout (1024 x 1024, margin 36):
  masthead -> dateline -> lead story (APEC, with drawn tarmac scene)
  -> 2x2 grid (Gulf, Cyclone Akvan, Gaza, Manila) -> markets strip
  -> "ALSO TODAY" footer strip -> credit line.
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
INK = (20, 20, 20)
PAPER = (246, 241, 229)
PANEL = (251, 248, 239)
RED = (164, 31, 31)
BLUE = (31, 78, 121)
GREY = (90, 86, 76)
RULE = (60, 58, 50)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap by measured pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, width, fill=INK, leading=None):
    """Draw wrapped text; returns y just below the last line."""
    leading = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, text, x, y, size=17):
    fnt = font(SANS_B, size)
    draw.text((x, y), text, font=fnt, fill=RED)
    return y + size + 6


# ---------------------------------------------------------------- icons
def icon_plane(draw, x, y, s, ink=INK):
    """Flat side view of a jet on a runway, drawn at (x, y), size s."""
    # tail fin (short, swept back)
    draw.polygon([(x + 0.12 * s, y + 0.34 * s), (x + 0.07 * s, y + 0.16 * s),
                  (x + 0.22 * s, y + 0.34 * s)], fill=ink)
    # fuselage: long rounded body
    draw.rounded_rectangle([x, y + 0.30 * s, x + 0.92 * s, y + 0.52 * s],
                           radius=int(s * 0.11), fill=ink)
    # nose cone
    draw.polygon([(x + 0.86 * s, y + 0.30 * s), (x + s, y + 0.41 * s),
                  (x + 0.86 * s, y + 0.52 * s)], fill=ink)
    # wing sweeping down, shallow
    draw.polygon([(x + 0.42 * s, y + 0.50 * s), (x + 0.50 * s, y + 0.62 * s),
                  (x + 0.62 * s, y + 0.50 * s)], fill=ink)
    # windows
    for i in range(4):
        wx = x + (0.30 + 0.12 * i) * s
        draw.ellipse([wx, y + 0.36 * s, wx + 0.05 * s, y + 0.44 * s],
                     fill=PAPER)
    # runway
    draw.line([(x, y + 0.72 * s), (x + s, y + 0.72 * s)], fill=ink, width=3)


def icon_spiral(draw, x, y, s, ink=BLUE):
    """Cyclone spiral: concentric arcs shrinking inward."""
    cx, cy = x + s / 2, y + s / 2
    for i, r in enumerate(range(int(s * 0.48), 4, -int(s * 0.07))):
        start = 20 + i * 55
        draw.arc([cx - r, cy - r, cx + r, cy + r], start, start + 240,
                 fill=ink, width=max(2, int(s * 0.045)))
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)


def icon_drone(draw, x, y, s, ink=INK):
    """Quad-rotor drone seen from above."""
    cx, cy = x + s / 2, y + s / 2
    arm = s * 0.30
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        px, py = cx + dx * arm, cy + dy * arm
        draw.line([(cx, cy), (px, py)], fill=ink, width=max(2, int(s * 0.05)))
        draw.ellipse([px - s * 0.13, py - s * 0.05, px + s * 0.13,
                      py + s * 0.05], fill=ink)
    draw.ellipse([cx - s * 0.16, cy - s * 0.12, cx + s * 0.16,
                  cy + s * 0.12], fill=RED)


def icon_flags(draw, x, y, s, ink=INK):
    """Four small flags on poles (Quad leaders)."""
    for i in range(4):
        px = x + (0.08 + 0.24 * i) * s
        draw.line([(px, y + 0.10 * s), (px, y + 0.92 * s)], fill=ink,
                  width=max(2, int(s * 0.04)))
        col = [RED, BLUE, INK, (180, 120, 20)][i]
        draw.polygon([(px, y + 0.10 * s), (px + 0.20 * s, y + 0.22 * s),
                      (px, y + 0.34 * s)], fill=col)


def icon_operation(draw, x, y, s, ink=INK):
    """Three blocks west of a line: the Yellow Line in central Gaza."""
    draw.line([(x + 0.55 * s, y + 0.05 * s), (x + 0.55 * s, y + 0.95 * s)],
              fill=(200, 160, 20), width=max(3, int(s * 0.07)))
    for i, (bx, by) in enumerate(((0.05, 0.15), (0.10, 0.50), (0.02, 0.72))):
        draw.rectangle([x + bx * s, y + by * s, x + (bx + 0.30) * s,
                        y + (by + 0.16) * s], fill=RED if i == 1 else ink)
    draw.polygon([(x + 0.70 * s, y + 0.40 * s), (x + 0.95 * s, y + 0.50 * s),
                  (x + 0.70 * s, y + 0.60 * s)], fill=ink)


def icon_bars(draw, x, y, s, ink=INK):
    """Rising bars with an arrow: markets up."""
    heights = (0.30, 0.45, 0.42, 0.62, 0.80)
    bw = s / 7
    for i, hfrac in enumerate(heights):
        bx = x + i * (bw + s * 0.03)
        bh = s * hfrac
        draw.rectangle([bx, y + s - bh, bx + bw, y + s],
                       fill=RED if i == len(heights) - 1 else ink)
    draw.line([(x, y + 0.05 * s), (x + s, y + 0.10 * s)], fill=BLUE, width=3)
    draw.polygon([(x + s, y + 0.10 * s), (x + 0.88 * s, y + 0.02 * s),
                  (x + 0.90 * s, y + 0.22 * s)], fill=BLUE)


# ---------------------------------------------------------------- page
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN

    # top furniture
    f_small = font(SANS_B, 15)
    d.text((x0, 22), "VOL. I — No. 322", font=f_small, fill=GREY)
    right = "ONE DAY, ONE PAGE"
    d.text((x1 - d.textlength(right, font=f_small), 22), right,
           font=f_small, fill=GREY)
    hrule(d, x0, x1, 46, width=3)

    # masthead
    f_mast = font(SERIF_B, 118)
    title = "THE WORLD"
    d.text(((W - d.textlength(title, font=f_mast)) / 2, 52), title,
           font=f_mast, fill=INK)
    hrule(d, x0, x1, 178, width=2, fill=RED)

    # dateline
    f_date = font(SERIF_B, 36)
    date = "WEDNESDAY  18  NOVEMBER  2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 188), date,
           font=f_date, fill=RED)
    f_sub = font(SANS, 16)
    sub = "SHENZHEN  ·  MANILA  ·  THE GULF  ·  GAZA  ·  NEW DELHI"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 232), sub,
           font=f_sub, fill=GREY)
    hrule(d, x0, x1, 258, width=2)

    # ---- lead story: APEC
    ly = 272
    kicker(d, "APEC  ·  SHENZHEN", x0, ly)
    f_head = font(SERIF_B, 46)
    y = draw_wrapped(d, "XI GREETS TRUMP ON THE TARMAC",
                     f_head, x0, ly + 26, 560, leading=52)
    f_deck = font(SERIF, 21)
    y = draw_wrapped(
        d,
        "First-ever Trump–Xi–Putin trilateral set for Thursday as "
        "APEC leaders meet in Shenzhen — after a hug, a red carpet "
        "and a fighter-jet flypast.",
        f_deck, x0, y + 8, 560, leading=28)
    # lead illustration, right of the text
    ix, iy, isz = 640, 272, 330
    d.rectangle([ix, iy, ix + isz, iy + 210], outline=RULE, width=2)
    d.rectangle([ix, iy, ix + isz, iy + 210], fill=(233, 226, 205))
    d.ellipse([ix + 268, iy + 8, ix + 304, iy + 44], fill=(232, 190, 60))
    icon_plane(d, ix + 50, iy + 14, 210)
    d.text((ix + 22, iy + 186), "Air Force One lands in Shenzhen",
           font=font(SERIF_I, 17), fill=GREY)
    hrule(d, x0, x1, 500, width=2)

    # ---- 2x2 grid of supporting stories
    panels = [
        ("THE GULF", "US JETS HIT IRAN'S QESHM ISLAND",
         "Iran's drones strike a US base in Kuwait; Bahrain "
         "intercepts more attacks as the war widens.",
         icon_drone),
        ("CYCLONE AKVAN", "AKVAN BEARS DOWN ON ANDHRA",
         "Severe storm in the Bay of Bengal; landfall due "
         "Friday, winds 100–110 km/h, coasts on alert.",
         icon_spiral),
        ("GAZA", "ISRAEL OPENS NEW GAZA OPERATION",
         "\u201cConcentrated operation\u201d in three areas of central "
         "Gaza — first broad ground push since the 2025 ceasefire.",
         icon_operation),
        ("MANILA", "QUAD MEETS; TRADE DEAL HAILED",
         "Trump calls the US–Philippines pact \u201cthe biggest\u201d; "
         "Manila says nothing has been signed yet.",
         icon_flags),
    ]
    gw, gh = (x1 - x0 - 24) // 2, 148
    gy = 516
    for i, (kick, head, body, icon) in enumerate(panels):
        px = x0 + (i % 2) * (gw + 24)
        py = gy + (i // 2) * (gh + 14)
        d.rectangle([px, py, px + gw, py + gh], fill=PANEL,
                    outline=RULE, width=1)
        ix = px + gw - 92
        icon(d, ix, py + 18, 72)
        kicker(d, kick, px + 14, py + 10, size=15)
        f_ph = font(SERIF_B, 25)
        draw_wrapped(d, head, f_ph, px + 14, py + 36, gw - 118, leading=29)
        f_pb = font(SANS, 16)
        draw_wrapped(d, body, f_pb, px + 14, py + 96, gw - 28, leading=20)

    # ---- markets strip
    my = gy + 2 * gh + 14 + 12
    d.rectangle([x0, my, x1, my + 64], fill=PANEL, outline=RULE, width=1)
    icon_bars(d, x0 + 14, my + 10, 44)
    f_mk = font(SERIF_B, 22)
    d.text((x0 + 72, my + 9), "MARKETS", font=f_mk, fill=RED)
    f_mb = font(SANS, 18)
    draw_wrapped(
        d,
        "Nvidia Q3 revenue $115.8bn, up 103% on AI demand; "
        "shares rise after hours.",
        f_mb, x0 + 72, my + 36, x1 - x0 - 90, leading=22)

    # ---- footer strip
    fy = my + 64 + 14
    hrule(d, x0, x1, fy, width=2)
    f_fh = font(SANS_B, 16)
    d.text((x0, fy + 10), "ALSO TODAY", font=f_fh, fill=RED)
    f_fb = font(SANS, 16)
    draw_wrapped(
        d,
        "Modi back in Delhi after ASEAN Manila  ·  "
        "Magnitude 6 quake hits Papua New Guinea  ·  "
        "Gold below $3,800, first since Sept 2025",
        f_fb, x0, fy + 34, x1 - x0, leading=21)
    hrule(d, x0, x1, H - 40, width=2)
    f_cr = font(SANS, 13)
    credit = ("Stories verified against two or more outlets  ·  "
              "All art drawn for this page  ·  18 November 2026")
    d.text(((W - d.textlength(credit, font=f_cr)) / 2, H - 33), credit,
           font=f_cr, fill=GREY)

    return img


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    page = render()
    page.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")
