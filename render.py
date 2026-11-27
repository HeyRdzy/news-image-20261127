#!/usr/bin/env python3
"""Render the news-image-20261127 front page: one image summing up the world
news of Friday 27 November 2026. Dense classic-newspaper layout, drawn with
PIL only. Every fact was verified against primary sources (Reuters, AP, BBC,
PHIVOLCS, Global Fund, PowerOutage.us) on 27 Nov 2026; events from Thursday
26 Nov are named in DATE CHECK and kept off the page.

Run:  python3 render.py   -> writes entry.png (1024x1024, < 1 MiB)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---- palette -------------------------------------------------------------
PAPER = (248, 242, 223)   # warm cream
INK = (26, 26, 26)
RED = (160, 30, 30)
GREY = (110, 108, 100)
SEA = (220, 232, 239)
LAND = (185, 196, 168)
LAND_LINE = (122, 138, 122)
DARK = (31, 42, 68)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_MAST = font(SERIF, 42)
F_SUB = font(SANS_B, 14)
F_TOP = font(SANS_B, 12)
F_HDR = font(SANS_B, 13)
F_LEAD = font(SERIF, 21)
F_LEAD2 = font(SERIF, 16)
F_BODY = font(SANS, 13)
F_BODY2 = font(SANS, 12)
F_SEC_H = font(SANS_B, 13)
F_SEC = font(SANS, 11)
F_NUM = font(SERIF, 22)
F_NUML = font(SANS, 9)
F_BRIEF = font(SANS, 11)
F_FOOT = font(SANS, 10)
F_TAG = font(SANS_B, 9)
F_PIN = font(SANS_B, 8)
F_LEG = font(SANS, 11)


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, xy, text, fnt, max_w, max_lines, fill=INK, leading=1.3):
    """Draw text wrapped to max_w, at most max_lines; truncate with ellipsis."""
    x, y = xy
    lines = wrap(text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and fnt.getlength(lines[-1] + "...") > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1] + "..."
    lh = int(fnt.size * leading)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def tag_chip(d, x, y, label, bg):
    """Small coloured source tag; returns width used."""
    w = int(F_TAG.getlength(label)) + 12
    h = 15
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    d.text((x + 6, y + 2), label, font=F_TAG, fill=(255, 255, 255))
    return w


TAG_COLORS = {
    "CONFIRMED": (34, 110, 60),
    "OFFICIALS": (38, 70, 110),
    "REPORTED": (176, 120, 20),
    "CLAIM": (120, 60, 120),
}


def section_header(d, x, y, w, title):
    d.rectangle([x, y, x + w, y + 18], fill=INK)
    d.rectangle([x, y, x + 5, y + 18], fill=RED)
    d.text((x + 11, y + 2), title, font=F_HDR, fill=(255, 255, 255))
    return y + 18


# ---- content (all verified 27 Nov 2026) ----------------------------------
UTC_SLOTS = [
    ("00:30", "Storm: 961,000 without power (PowerOutage.us)"),
    ("01:37", "Zelensky's BBC interview published"),
    ("02:04", "Key economies hesitate at proposed US duties"),
    ("11:00", "Poland signs Palantir AI deal (noon CET)"),
    ("15:00", "Davis Cup semi: Italy v Czechia (16:00 CET)"),
    ("18:00", "Wall Street closes early for Black Friday"),
]

NUMBERS = [
    ("961,000", "WITHOUT POWER, 00:30 UTC"),
    ("70 mph", "STRONGEST STORM GUSTS"),
    ("+2.9%", "TOKYO CORE CPI, NOV Y/Y"),
    ("57,499", "NIKKEI 225, +0.9% FRI"),
    ("8,770", "ASX 200, +0.1% FRI"),
    ("1.5-1.5", "GUKESH-SINDAROV 1.5-1.5"),
]

LEAD1 = {
    "tag": "CONFIRMED", "src": "PowerOutage.us / Reuters",
    "head": "Black Friday dawns dark: storm cuts power to 961,000",
    "body": ("A Thanksgiving storm rolled into Friday: 961,000 without power at "
             "00:30 UTC - Pennsylvania 235,000, New Jersey 180,000, Maryland "
             "156,000, Virginia 132,000. Gusts to 70 mph, flooding, flight "
             "delays; Macy's 100th parade, moved to Saturday, leaves Fifth "
             "Avenue quiet."),
}

LEAD2 = {
    "tag": "CONFIRMED", "src": "BBC",
    "head": "Zelensky: Trump-Putin friendship 'strange'",
    "body": ("Zelensky told the BBC it was 'very strange' Trump calls Putin "
             "'my friend': 'He's an aggressor, and a killer.' US Patriot "
             "delays cost Ukrainian lives."),
}

LEAD3 = {
    "tag": "OFFICIALS", "src": "Reuters",
    "head": "Poland signs Palantir AI deal at noon",
    "body": ("Poland signs with Palantir today for AI to aid military "
             "decisions - noon, Army Museum, Warsaw Citadel. No value "
             "disclosed; privacy protests, ombudsman complaint."),
}

SECONDARIES = [
    ("Tokyo prices cool: core CPI +2.9%",
     "Core CPI +2.9% y/y vs +3.0% forecast; ex food/energy +2.5%.",
     "OFFICIALS"),
    ("Key economies balk at US duties",
     "Major economies hesitate at proposed US duties.",
     "REPORTED"),
    ("Davis Cup semi: Italy v Czech Republic",
     "Three-time champions Italy in Bologna, 16:00 CET.",
     "OFFICIALS"),
    ("Chess: a rest day in Geneva",
     "Level 1.5-1.5 after 60-move Game 3 draw; Game 4 Sat.",
     "OFFICIALS"),
    ("Mayon stays at Alert Level 3",
     "8 quakes, 2,361 t SO2/day; 6-km danger zone closed.",
     "OFFICIALS"),
    ("Uganda next for $40-a-year HIV jab",
     "Generic jab reached Zambia Wed; Uganda next; 3m by 2028.",
     "OFFICIALS"),
    ("Nikkei +0.9% to 57,499; ASX +0.1%",
     "Tokyo rebounds early Friday; Sydney edges to 8,770.",
     "CONFIRMED"),
    ("N. Korea halts help for Russia's war",
     "Pyongyang stopped military support for Russia.",
     "CLAIM"),
    ("Iran vows to advance nuclear programme",
     "Tehran pledges to press on as West seeks inspections.",
     "REPORTED"),
    ("EU leaders to try again on 17-18 Dec",
     "No deal after the 'frugal' seven walk out.",
     "REPORTED"),
]

BRIEFS = [
    "Key economies hesitate at US duties - REPORTED",
    "Dollar at 159.26 yen in Friday trade - Market data",
    "Wall Street reopens for a short Black Friday - NYSE",
    "Iraq blocks 2 border crossings in Kurdistan - REPORTED",
    "China threatens retaliation over Trump tariffs - REPORTED",
    "Taiwan candidate hit by AI-generated graphic - REPORTED",
    "EPA: zero airborne lead after Iowa blast - REPORTED",
    "Canada student curbs challenge Carney - REPORTED",
    "Pashinyan aims to replace Russian guards - REPORTED",
    "Baghdad sceptical of federalism, says Barzani - REPORTED",
    "US tech defences hinder China's next AI - REPORTED",
    "German boat dealer 'supplied Channel gangs' - BBC",
    "France mainstream risks presidential debacle - BBC",
    "Pakistani TV show screenings cancelled in India - BBC",
    "Sandpapergate probe widens to 2017-18 Ashes - BBC",
    "'Met ruined my life,' says wrongly jailed Kenyan - BBC",
    "Pregnant US inmate escapes in prison vehicle - BBC",
    "Man and dog escape king tide in Oregon - BBC",
    "Flooding, flight delays as storm crosses East - BBC",
    "Zelensky defends sinking Russian warship off Libya - BBC",
    "Starlink still restricted in occupied Ukraine - BBC",
    "Ukraine downs ~70% of Russia's fastest drones - BBC",
    "Abu Dhabi talks stall; resume in December - BBC",
    "Britain face Spain in Saturday's semi - Davis Cup",
    "Zelensky: US 'too focused on Middle East' - BBC",
    "Zelensky: 'without a capital, no country' - BBC",
    "Asia mixed: Hang Seng +1.2%, Vietnam -3.4% - Markets",
    "Cairo tanker probe: DNA tests to name 31 dead - REPORTED",
    "Hamas consults factions; no measures named - REPORTED",
    "Nikkei futures +0.7% at 57,810 on SGX - Market data",
]

DATE_CHECK = (
    "DATE CHECK - NOT ON THIS PAGE (Thu 26 Nov): Kuwait drone attack; Aramco Jazan fire; "
    "Argentina votes; Ukraine strikes on Russian refineries; Kim's nuclear tour; BOK hike; "
    "UK migration 77,000; Bangkok blast; EU budget collapse; Hamas weighs response; Egypt "
    "arrests tanker driver; 50 Houthi targets hit. "
    "NOT YET: Davis Cup result; Japan housing starts; Black Friday sales."
)

SOURCES = ("Sources: Reuters, AP, BBC, Euronews, Davis Cup, FIDE, PHIVOLCS, Global Fund, "
           "PowerOutage.us. All events happened or were first reported on 27 November 2026.")

# world map: rough continent polygons in (lon, lat)
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-75, 62), (-65, 60),
     (-55, 52), (-60, 45), (-70, 42), (-75, 35), (-80, 26), (-85, 30), (-90, 21),
     (-95, 18), (-105, 20), (-110, 23), (-120, 34), (-125, 40), (-125, 49),
     (-135, 58), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-70, 0), (-60, -5), (-50, -5), (-40, -10), (-35, -15),
     (-40, -25), (-50, -30), (-60, -35), (-65, -40), (-70, -50), (-75, -45),
     (-75, -30), (-80, -20), (-80, -10)],
    [(-10, 36), (-5, 44), (0, 50), (5, 55), (10, 58), (15, 55), (20, 55), (25, 60),
     (30, 65), (35, 68), (40, 65), (35, 55), (30, 50), (25, 45), (20, 40),
     (15, 38), (10, 38), (5, 40), (0, 36)],
    [(-15, 15), (-10, 25), (0, 32), (10, 35), (20, 32), (30, 30), (35, 25), (40, 15),
     (45, 10), (50, 5), (45, -5), (40, -15), (35, -25), (30, -30), (25, -35),
     (20, -35), (15, -25), (10, -15), (5, -5), (0, 0), (-5, 5), (-10, 10)],
    [(40, 65), (50, 70), (60, 70), (70, 72), (80, 72), (90, 75), (100, 75), (110, 70),
     (120, 72), (130, 70), (140, 60), (140, 50), (135, 40), (130, 35), (125, 30),
     (120, 25), (115, 20), (110, 10), (105, 5), (100, 10), (95, 15), (90, 20),
     (85, 20), (80, 10), (75, 8), (70, 15), (65, 20), (60, 25), (55, 25),
     (50, 30), (45, 30), (40, 35), (40, 45), (40, 55)],
    [(113, -22), (120, -20), (130, -15), (135, -12), (140, -15), (145, -20),
     (150, -25), (150, -35), (145, -38), (140, -38), (135, -35), (130, -32),
     (125, -32), (120, -30), (115, -32), (113, -25)],
]

# pins: (number, lon, lat, legend label, optional label offset dx, dy in px)
PINS = [
    (1, -75, 40, "US East Coast - storm", None),
    (2, 30.5, 50.5, "Kyiv - Zelensky", (16, 8)),
    (3, 21, 52.2, "Warsaw - Palantir", (14, -14)),
    (4, 139.7, 35.7, "Tokyo - CPI", None),
    (5, 4.4, 50.8, "Brussels - EU budget", (-16, -14)),
    (6, 11.3, 44.5, "Bologna - Davis Cup", (16, -10)),
    (7, 6.1, 46.2, "Geneva - chess", (14, 12)),
    (8, 123.7, 13.2, "Albay - Mayon", None),
    (9, 28.3, -15.4, "Lusaka - HIV jab", None),
    (10, 151.2, -33.9, "Sydney - ASX", None),
]


# ---- lead art (simple drawn scenes) --------------------------------------
def art_storm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=DARK)
    for i in range(40):
        rx = x + (i * 37) % w
        ry = y + (i * 53) % h
        d.line([rx, ry, rx - 6, ry + 12], fill=(157, 184, 214), width=1)
    d.rectangle([x + 18, y + h - 52, x + 88, y + h - 14], fill=(16, 20, 32))
    d.rectangle([x + 30, y + h - 44, x + 40, y + h - 34], fill=(16, 20, 32))
    d.rectangle([x + 60, y + h - 44, x + 70, y + h - 34], fill=(240, 200, 90))
    d.rectangle([x + 108, y + h - 60, x + 178, y + h - 14], fill=(16, 20, 32))
    d.rectangle([x + 122, y + h - 50, x + 132, y + h - 40], fill=(240, 200, 90))
    d.rectangle([x + 152, y + h - 50, x + 162, y + h - 40], fill=(16, 20, 32))
    d.line([x + 215, y + 14, x + 228, y + h - 14], fill=(90, 70, 50), width=5)
    d.line([x + 205, y + 24, x + 238, y + 20], fill=(90, 70, 50), width=3)
    d.line([x + 205, y + 24, x + 150, y + 52, x + 108, y + 36], fill=(200, 200, 200), width=1)
    d.line([x + 238, y + 20, x + 280, y + 50, x + 300, y + 32], fill=(200, 200, 200), width=1)
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(46, 95, 138))
    for i in range(6):
        wx = x + 12 + i * 48
        d.arc([wx, y + h - 10, wx + 26, y + h - 2], 200, 340, fill=(220, 235, 245), width=1)


def art_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(43, 58, 85))
    d.rectangle([x + 8, y + h - 40, x + 34, y + h], fill=(20, 26, 40))
    d.rectangle([x + 40, y + h - 54, x + 66, y + h], fill=(20, 26, 40))
    d.ellipse([x + 44, y + h - 68, x + 62, y + h - 52], fill=(212, 175, 55))
    d.line([x + 53, y + h - 72, x + 53, y + h - 66], fill=(212, 175, 55), width=2)
    d.rectangle([x + 72, y + h - 34, x + 102, y + h], fill=(20, 26, 40))
    d.ellipse([x + 76, y + h - 46, x + 88, y + h - 34], fill=(212, 175, 55))
    for wx in (14, 46, 78, 92):
        d.rectangle([x + wx, y + h - 26, x + wx + 6, y + h - 18], fill=(240, 200, 90))


def art_contract(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 220, 200))
    d.rectangle([x + 14, y + 10, x + w - 26, y + h - 12], fill=(255, 255, 255),
                outline=(120, 120, 120))
    for i in range(5):
        ly = y + 26 + i * 11
        d.line([x + 22, ly, x + w - 34, ly], fill=(150, 150, 150), width=1)
    d.rectangle([x + 22, y + 16, x + w - 60, y + 20], fill=RED)
    d.ellipse([x + w - 52, y + h - 44, x + w - 28, y + h - 20], fill=RED)
    d.ellipse([x + w - 46, y + h - 38, x + w - 34, y + h - 26], fill=(190, 60, 60))
    d.rectangle([x + 16, y + h - 40, x + 52, y + h - 10], fill=(30, 30, 30))
    d.rectangle([x + 24, y + h - 32, x + 44, y + h - 18], fill=(212, 175, 55))
    for px in (20, 30, 40):
        d.line([x + px, y + h - 44, x + px, y + h - 40], fill=(212, 175, 55), width=2)
        d.line([x + px, y + h - 10, x + px, y + h - 6], fill=(212, 175, 55), width=2)


# ---- page ----------------------------------------------------------------
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 24
    CW = W - 2 * MX

    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=1)

    y = 20
    d.text((MX, y), "FRIDAY EDITION  |  No. 331", font=F_TOP, fill=INK)
    r = "PRICE: ONE DAY'S NEWS"
    d.text((W - MX - F_TOP.getlength(r), y), r, font=F_TOP, fill=INK)
    y += 16
    d.line([MX, y, W - MX, y], fill=INK, width=1)
    y += 6

    title = "FRIDAY 27 NOVEMBER 2026"
    d.text(((W - F_MAST.getlength(title)) / 2, y), title, font=F_MAST, fill=INK)
    y += 50
    sub = "43 STORIES  ·  9 REGIONS  ·  12 FIELDS  —  THE WORLD IN ONE IMAGE"
    d.text(((W - F_SUB.getlength(sub)) / 2, y), sub, font=F_SUB, fill=RED)
    y += 20
    d.line([MX, y, W - MX, y], fill=INK, width=3)
    d.line([MX, y + 4, W - MX, y + 4], fill=INK, width=1)
    y += 8

    # THE DAY IN UTC
    y = section_header(d, MX, y, CW, "THE DAY IN UTC") + 3
    col_w = CW // 2
    for i, (t, txt) in enumerate(UTC_SLOTS):
        cx = MX + (i % 2) * col_w
        cy = y + (i // 2) * 21
        d.text((cx, cy), t, font=F_SEC_H, fill=RED)
        d.text((cx + 52, cy), txt, font=F_BODY2, fill=INK)
    y += 3 * 21 + 4

    # THE DAY IN NUMBERS (single-line labels)
    y = section_header(d, MX, y, CW, "THE DAY IN NUMBERS") + 4
    cell = CW // 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx = MX + i * cell
        d.text((cx + 4, y), num, font=F_NUM, fill=RED)
        d.text((cx + 4, y + 26), lab, font=F_NUML, fill=GREY)
        if i:
            d.line([cx, y, cx, y + 38], fill=(200, 194, 175), width=1)
    y += 42

    # LEAD 1 (full width, art left)
    d.line([MX, y, W - MX, y], fill=INK, width=1)
    y += 5
    art_w, art_h = 300, 122
    art_storm(d, MX, y, art_w, art_h)
    tx = MX + art_w + 14
    tw = W - MX - tx
    ty = y
    tw_tag = tag_chip(d, tx, ty, LEAD1["tag"], TAG_COLORS[LEAD1["tag"]])
    d.text((tx + tw_tag + 6, ty + 1), LEAD1["src"], font=F_FOOT, fill=GREY)
    ty += 19
    ty = draw_wrapped(d, (tx, ty), LEAD1["head"], F_LEAD, tw, 2, leading=1.15)
    ty += 2
    draw_wrapped(d, (tx, ty), LEAD1["body"], F_BODY, tw, 3, leading=1.3)
    y += art_h + 8

    # LEADS 2 + 3 (two columns, small art left)
    col2 = CW // 2
    for i, lead in enumerate((LEAD2, LEAD3)):
        cx = MX + i * col2
        cw = col2 - (12 if i == 0 else 0)
        aw, ah = 108, 103
        (art_kyiv if i == 0 else art_contract)(d, cx, y, aw, ah)
        tx2 = cx + aw + 10
        tw2 = (cx + cw) - tx2
        ty2 = y
        tw_tag = tag_chip(d, tx2, ty2, lead["tag"], TAG_COLORS[lead["tag"]])
        d.text((tx2 + tw_tag + 6, ty2 + 1), lead["src"], font=F_FOOT, fill=GREY)
        ty2 += 18
        ty2 = draw_wrapped(d, (tx2, ty2), lead["head"], F_LEAD2, tw2, 2, leading=1.15)
        draw_wrapped(d, (tx2, ty2 + 2), lead["body"], F_SEC, tw2, 3, leading=1.3)
        if i == 0:
            d.line([cx + col2 - 6, y, cx + col2 - 6, y + ah], fill=(200, 194, 175), width=1)
    y += 103 + 8

    # SECONDARIES (2 cols x 5 rows, one-line bodies)
    y = section_header(d, MX, y, CW, "ALSO TODAY") + 3
    for i, (head, body, tag) in enumerate(SECONDARIES):
        cx = MX + (i % 2) * col_w
        cy = y + (i // 2) * 27
        tw_tag = tag_chip(d, cx, cy + 1, tag, TAG_COLORS[tag])
        hx = cx + tw_tag + 6
        d.text((hx, cy), head, font=F_SEC_H, fill=INK)
        d.text((hx, cy + 14), body, font=F_SEC, fill=INK)
        if i % 2 == 0:
            d.line([cx + col_w - 6, cy, cx + col_w - 6, cy + 24], fill=(200, 194, 175), width=1)
    y += 5 * 27 + 4

    # MAP (Europe cluster uses offset number labels with leader lines)
    y = section_header(d, MX, y, CW, "WHERE IT HAPPENED") + 3
    map_x, map_y, map_w, map_h = MX, y, 620, 110
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=SEA,
                outline=(170, 180, 190))
    def proj(lon, lat):
        return (map_x + (lon + 180) / 360 * map_w,
                map_y + (75 - lat) / 130 * map_h)
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    for n, lon, lat, _lab, off in PINS:
        px, py = proj(lon, lat)
        t = str(n)
        if off is None:
            d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255))
            d.text((px - F_PIN.getlength(t) / 2, py - 5), t, font=F_PIN, fill=(255, 255, 255))
        else:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED, outline=(255, 255, 255))
            lx, ly = px + off[0], py + off[1]
            d.line([px, py, lx, ly], fill=RED, width=1)
            d.ellipse([lx - 7, ly - 7, lx + 7, ly + 7], fill=RED, outline=(255, 255, 255))
            d.text((lx - F_PIN.getlength(t) / 2, ly - 5), t, font=F_PIN, fill=(255, 255, 255))
    lx = map_x + map_w + 14
    lw = W - MX - lx
    for i, (_n, _lon, _lat, lab, _off) in enumerate(PINS):
        ly = map_y + (i // 2) * 22
        lxx = lx + (i % 2) * (lw // 2)
        d.text((lxx, ly), f"{i + 1}. {lab}", font=F_LEG, fill=INK)
    y += map_h + 6

    # BRIEFS (3 cols x 10 rows)
    y = section_header(d, MX, y, CW, "ALSO ON FRIDAY 27 NOVEMBER") + 3
    bcol = CW // 3
    rows = 10
    for i, b in enumerate(BRIEFS):
        cx = MX + (i // rows) * bcol
        cy = y + (i % rows) * 12
        d.text((cx, cy), f"{i + 1:2d}. {b}", font=F_BRIEF, fill=INK)
    y += rows * 12 + 4

    # FOOTER: date check + sources
    d.line([MX, y, W - MX, y], fill=INK, width=1)
    y += 4
    y = draw_wrapped(d, (MX, y), DATE_CHECK, F_FOOT, CW, 2, fill=INK, leading=1.3)
    y += 2
    draw_wrapped(d, (MX, y), SOURCES, F_FOOT, CW, 1, fill=GREY, leading=1.3)

    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}, {size} bytes, final y={y}")
    assert img.size == (1024, 1024), "must be 1024x1024"
    assert size <= 1048576, "must be <= 1 MiB"
    assert y <= 1008, f"content overflows the page (final y={y})"


if __name__ == "__main__":
    main()
