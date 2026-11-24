#!/usr/bin/env python3
"""Render 'The World in One Image' for Tuesday 24 November 2026 — v1.

Early build (~02:30 UTC Tuesday): overnight stories plus the first hours
of Tuesday — Asia's markets riding Wall Street's Huang rally, the Ulleung
air-defence alert, the hacked Rosstat war-dead analysis, NATO's AWACS
decision, Trump's executions memo, the Gomez resignation and the Grok
lawsuits. Every fact below was checked against live reporting on Tuesday
morning (Reuters, AP, CNN, Guardian, Bloomberg, Yonhap, Nikkei, SCMP,
Japan Times, White House). Market figures are Tuesday-morning reports of
Monday's close and Tuesday's Asia open (Nvidia +31.5%, S&P 500 +4.7%,
Nasdaq +6.5%, Nikkei +4.5%, KOSPI +7.5%, Taiwan +9.1%).

Deterministic Pillow pipeline: no network, no timestamps, no randomness.
Running it twice must produce byte-identical PNG output.
Writes entry.png (1024x1024, PNG) next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---- palette ---------------------------------------------------------------
PAPER = (247, 243, 234)   # warm off-white page
INK = (18, 30, 54)        # deep navy ink
INK_SOFT = (52, 68, 96)
RED = (178, 34, 34)       # headline accent
TEAL = (14, 92, 96)
GOLD = (184, 134, 11)
GREY_LINE = (203, 196, 182)
CARD = (255, 255, 255)
DARK_PANEL = (24, 38, 64)
MUTED = (110, 116, 128)

# ---- fonts -----------------------------------------------------------------
def font(name, size):
    paths = {
        "sans": "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "sans_b": "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        "serif_b": "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
        "serif": "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
    }
    try:
        return ImageFont.truetype(paths[name], size)
    except OSError:
        return ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if name.endswith("_b") else
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)

F_TITLE = font("serif_b", 46)
F_STRAP = font("sans_b", 15)
F_KICK = font("sans_b", 12)
F_HEAD = font("sans_b", 21)
F_DECK = font("sans", 14)
F_SMALL_HEAD = font("sans_b", 15)
F_SMALL_DECK = font("sans", 11)
F_STAT_N = font("sans_b", 30)
F_STAT_L = font("sans_b", 11)
F_BRIEF = font("sans", 12)
F_BRIEF_B = font("sans_b", 12)
F_FOOT = font("sans", 11)
F_MAP_LBL = font("sans_b", 11)
F_NUM = font("sans_b", 16)
F_BIG_NUM = font("serif_b", 40)

# ---- verified news content: Tuesday 24 November 2026 (early build) --------
# Every fact below was checked against live reporting on Tuesday morning
# (Reuters, AP, CNN, Guardian, Bloomberg, Yonhap, Nikkei, SCMP,
# Japan Times, White House). Market figures are Tuesday-morning reports:
# Nvidia +31.5% Monday (Reuters: biggest daily gain in 23 years, ~$1tn
# restored), S&P 500 +4.7%, Nasdaq +6.5%, Dow +3%; Tuesday Asia open:
# Nikkei +4.5%, KOSPI +7.5%, Taiwan +9.1%, MSCI Asia ex-Japan +4.6%.
MASTHEAD_STRAP = "TUESDAY 24 NOVEMBER 2026  ·  27 STORIES  ·  5 REGIONS  ·  ONE DAY"

STATS = [
    ("+31.5%", "Nvidia's Monday surge"),
    ("+7.5%", "KOSPI's Tuesday leap"),
    ("470,000", "Russian war dead"),
    ("3", "Missiles hit Poland"),
    ("5 min", "Ulleung alert lifted after"),
    ("2", "States sue Musk's firms"),
]

FEATURES = [
    {
        "num": "01", "place": "TOKYO · SEOUL", "cat": "MARKETS",
        "head": "Asia rides the Huang rally",
        "deck": ("Nikkei +4.5%, KOSPI +7.5%, Taiwan +9.1% after Wall "
                 "Street's best day since April 2025. Nvidia +31.5%."),
        "src": "Reuters · Nikkei",
        "art": "asia",
    },
    {
        "num": "02", "place": "ULLEUNG, S. KOREA", "cat": "SECURITY",
        "head": "Russian jets trigger island alert",
        "deck": ("Seoul tells Ulleung residents to shelter as Russian "
                 "jets enter the air-defence zone; alert lifted in minutes."),
        "src": "Reuters · Yonhap",
        "art": "alert",
    },
    {
        "num": "03", "place": "MOSCOW", "cat": "WAR",
        "head": "Russia's war dead near 500,000",
        "deck": ("Hacked Rosstat records put war-linked deaths at "
                 "460,000-470,000; Meduza counts 700,000+ with the missing."),
        "src": "Guardian · Bloomberg",
        "art": "records",
    },
]

SMALLS = [
    ("04", "WARSAW", "DEFENCE",
     "NATO sends AWACS to Poland",
     "After 3 missiles land, NATO sends an early-warning jet to its eastern flank.",
     "Reuters"),
    ("05", "WASHINGTON", "JUSTICE",
     "Trump orders federal executions sped up",
     "Memo seeks death penalty for child murder, rape and trafficking killings.",
     "White House · AP"),
    ("06", "LOS ANGELES", "POLITICS",
     "Congressman Gomez quits over ethics report",
     "House panel finds 'substantial evidence' of sexual misconduct; out Dec 1.",
     "CNN · WSJ"),
    ("07", "RICHMOND", "TECH",
     "Two states sue Musk's firms over Grok",
     "Virginia and Oregon say 'spicy mode' made non-consensual sexual images.",
     "Reuters · AP"),
    ("08", "CANBERRA", "CLIMATE",
     "COP31 fallout: blame game begins",
     "Australia faces backlash; Pacific nations despair after the talks collapse.",
     "Reuters"),
    ("09", "TEHRAN", "CONFLICT",
     "Iran vows to fight US naval blockade",
     "Tehran vows to use 'all its tools' against the blockade.",
     "Reuters"),
    ("10", "CIKANDE", "DISASTER",
     "More bodies found in factory fire",
     "Search goes on at the Indonesian candy plant; 24 dead Monday, ~30 missing.",
     "Manila Times · Reuters"),
    ("11", "TALLINN", "SECURITY",
     "Moscow warns Estonia over 'open war'",
     "Russia accuses Tallinn of hostile acts on the verge of triggering open war.",
     "Japan Times"),
    ("12", "NEW DELHI", "TRADE",
     "India-EU trade pact set for Dec 16",
     "Landmark deal to be signed in Brussels on Dec 16 during Modi's visit.",
     "Sunday Guardian"),
    ("13", "MANILA", "DEFENCE",
     "Trump offers Manila $2.4bn — with a catch",
     "US self-defence aid for the Philippines comes with conditions.",
     "SCMP"),
]

BRIEFS = [
    ("London", "GTA VI hacker Arion Kurtaj, 21, gets 7 years; free on time served."),
    ("Manchester", "Thousands evacuated from a Don Toliver show after a substance release."),
    ("New York", "UN chief calls for an AI risk-management framework within a year."),
    ("Beijing", "China sentences an official to death for spying and leaking secrets."),
    ("Pyongyang", "North Korea threatens to close its Swiss diplomatic office."),
    ("Jakarta", "Prabowo taps a loyalist and a tycoon's cousin as VP picks."),
    ("Washington", "Vance tapped as Trump's emissary to the Nvidia board."),
    ("Iowa", "Trump orders a pause on the Army's lead-azide detonation."),
    ("Washington", "Trump claims on Truth Social he made the Huang deal: 'I made the deal.'"),
    ("California", "Flood watch in the Bay Area as storms threaten Thanksgiving travel."),
    ("Kathmandu", "Nepal's PM in India for economic and energy talks."),
    ("Bangkok", "Thai court upholds the verdict against an opposition lawmaker."),
    ("Ottawa", "Canada's PM brings a Trump impersonator on stage at a press gala."),
    ("Ibaraki", "City holds its first briefing on a nuclear-waste survey."),
]

DATE_CHECK = ("NOT TUESDAY — before today: Huang reinstated (Mon) · "
              "COP31 collapses (Sun) · Democrats' 258 seats (Mon) · "
              "Kyiv: 14 killed (Mon) · Delta glitch (Sun)")

FOOTER = "Sources: Reuters · AP · CNN · Guardian · Bloomberg · Yonhap · Nikkei · SCMP · Japan Times · White House."

REGION_CHIPS = ["NORTH AMERICA 3", "EUROPE 3", "MIDDLE EAST 1", "ASIA 5", "OCEANIA 1"]

# ---- text helpers ------------------------------------------------------------
def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` px."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)

# ---- banner art (simple flat shapes, drawn, not photos) ----------------------
def banner_asia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 58, 40))
    # rising market line with arrowhead
    pts = [(x + 14, y + 92), (x + 70, y + 78), (x + 118, y + 84),
           (x + 170, y + 56), (x + 222, y + 40), (x + 268, y + 22)]
    d.line(pts, fill=(118, 185, 0), width=5)
    d.polygon([(x + 268, y + 22), (x + 246, y + 24), (x + 262, y + 42)],
              fill=(118, 185, 0))
    # rising bars: Nikkei, KOSPI, Taiwan
    d.rectangle([x + 18, y + 66, x + 46, y + 104], fill=(24, 38, 64),
                outline=(118, 185, 0), width=2)
    d.rectangle([x + 56, y + 52, x + 84, y + 104], fill=(24, 38, 64),
                outline=(118, 185, 0), width=2)
    d.rectangle([x + 94, y + 38, x + 122, y + 104], fill=(24, 38, 64),
                outline=(118, 185, 0), width=2)
    d.text((x + w - 118, y + h - 46), "+7.5%", font=F_BIG_NUM,
           fill=(255, 255, 255))

def banner_alert(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(74, 20, 20))
    # radar rings
    cx, cy = x + 78, y + 58
    for r in (48, 34, 20):
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  outline=(232, 122, 42), width=2)
    d.line([cx, cy, cx + 40, cy - 26], fill=(232, 122, 42), width=3)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(232, 122, 42))
    # alert triangle
    d.polygon([(x + w - 66, y + 16), (x + w - 26, y + 88), (x + w - 106, y + 88)],
              fill=(232, 196, 90))
    d.text((x + w - 70, y + 48), "!", font=F_BIG_NUM, fill=(74, 20, 20))
    d.text((x + 12, y + h - 30), "07:52", font=F_NUM, fill=(255, 255, 255))

def banner_records(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 38, 64))
    # stack of documents
    for i in range(3):
        dx, dy = i * 8, i * -8
        d.rectangle([x + 20 + dx, y + 26 + dy, x + 120 + dx, y + 92 + dy],
                    fill=(247, 243, 234), outline=GREY_LINE, width=1)
        for j in range(3):
            d.line([x + 30 + dx, y + 40 + j * 14 + dy,
                    x + 110 + dx, y + 40 + j * 14 + dy],
                   fill=INK_SOFT, width=2)
    d.text((x + w - 178, y + h - 46), "470,000", font=F_BIG_NUM,
           fill=(255, 255, 255))

BANNERS = {"asia": banner_asia, "alert": banner_alert, "records": banner_records}

# ---- stylised world map ------------------------------------------------------
# Rough continent outlines as (lon, lat) polygons; equirectangular projection.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80), (-85, 70),
     (-75, 62), (-60, 55), (-55, 47), (-70, 42), (-80, 32), (-90, 21),
     (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60),
     (-165, 60)],
    [(-80, 10), (-60, 5), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
     (-58, -35), (-65, -45), (-70, -55), (-73, -40), (-72, -20), (-77, -12)],
    [(-10, 36), (-2, 37), (5, 38), (12, 42), (18, 40), (23, 36), (28, 41),
     (30, 46), (20, 50), (12, 55), (8, 58), (5, 60), (-5, 58), (-10, 50),
     (-10, 43)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -18), (28, -28), (20, -35),
     (15, -30), (12, -18), (9, -1), (9, 4), (-8, 4), (-13, 8), (-17, 12)],
    [(30, 70), (50, 70), (70, 72), (90, 75), (110, 76), (130, 72), (150, 70),
     (170, 66), (178, 65), (170, 60), (160, 55), (150, 45), (140, 40),
     (130, 35), (122, 30), (115, 22), (108, 12), (103, 8), (100, 8), (95, 15),
     (90, 22), (85, 20), (80, 13), (75, 8), (70, 20), (65, 25), (60, 25),
     (55, 26), (50, 29), (48, 30), (45, 35), (40, 38), (35, 36), (30, 36),
     (28, 42), (30, 45), (30, 50), (35, 55), (40, 60), (35, 65)],
    [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (150, -37),
     (153, -27), (146, -19), (142, -11), (135, -12), (130, -13), (122, -14),
     (114, -22)],
]
# numbered pins: (lon, lat, label, label dx, label dy) — one pin per story
# 01–13. Dots are nudged a few degrees where the map scale would merge
# them; the map is stylised, not a survey chart. Richmond is nudged east
# so its dot does not sit on Washington's.
PINS = [
    (139.7, 35.7, "1", 6, -14), (130.9, 37.5, "2", -16, -14),
    (37.6, 55.7, "3", 8, -14), (21.0, 52.2, "4", -4, -16),
    (-77.0, 38.9, "5", -14, -16), (-118.2, 34.0, "6", -16, 8),
    (-74.5, 36.0, "7", 6, 8), (149.1, -35.3, "8", 8, -6),
    (51.4, 35.7, "9", 8, -6), (106.1, -6.2, "10", 8, -6),
    (24.7, 59.4, "11", 8, -14), (77.2, 28.6, "12", 8, -6),
    (121.0, 14.6, "13", 8, -6),
]

def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 242))
    d.rectangle([x, y, x + w, y + h], outline=GREY_LINE, width=1)
    def proj(lon, lat):
        px = x + (lon + 180.0) / 360.0 * w
        py = y + (90.0 - lat) / 180.0 * h
        return (px, py)
    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=(148, 168, 178))
    for lon, lat, lbl, dx, dy in PINS:
        px, py = proj(lon, lat)
        r = 5
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((px + dx, py + dy), lbl, font=F_MAP_LBL, fill=RED)

# ---- page assembly -----------------------------------------------------------
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 92], fill=INK)
    d.text((24, 12), "THE WORLD IN ONE IMAGE", font=F_TITLE, fill=(255, 255, 255))
    d.text((24, 66), MASTHEAD_STRAP, font=F_STRAP, fill=(232, 196, 90))
    d.rectangle([0, 92, W, 96], fill=RED)

    # stat strip
    y0 = 96
    cw = W // 6
    for i, (num, lbl) in enumerate(STATS):
        cx = i * cw + cw // 2
        d.text((cx, y0 + 8), num, font=F_STAT_N, fill=RED, anchor="ma")
        d.text((cx, y0 + 46), lbl, font=F_STAT_L, fill=INK_SOFT, anchor="ma")
        if i:
            d.line([i * cw, y0 + 10, i * cw, y0 + 62], fill=GREY_LINE, width=1)
    d.line([0, 168, W, 168], fill=GREY_LINE, width=1)

    # features: three columns
    fx, fy, fw, fh = 24, 180, 312, 284
    gap = 16
    for i, f in enumerate(FEATURES):
        x = fx + i * (fw + gap)
        d.rectangle([x, fy, x + fw, fy + fh], fill=CARD, outline=GREY_LINE, width=1)
        BANNERS[f["art"]](d, x + 1, fy + 1, fw - 2, 118)
        ty = fy + 130
        d.text((x + 12, ty), f["num"] + "  " + f["place"] + " — " + f["cat"],
               font=F_KICK, fill=RED)
        ty += 20
        for ln in wrap(d, f["head"], F_HEAD, fw - 24):
            d.text((x + 12, ty), ln, font=F_HEAD, fill=INK)
            ty += 24
        ty += 4
        for ln in wrap(d, f["deck"], F_DECK, fw - 24):
            d.text((x + 12, ty), ln, font=F_DECK, fill=INK_SOFT)
            ty += 18
        d.text((x + 12, fy + fh - 20), f["src"], font=F_FOOT, fill=MUTED)

    # smalls: two columns x five rows
    sy = 476
    col_w = (W - 48 - 16) // 2
    row_h = 48
    for i, (num, place, cat, head, deck, src) in enumerate(SMALLS):
        col, row = i % 2, i // 2
        x = 24 + col * (col_w + 16)
        y = sy + row * row_h
        d.text((x, y), num, font=F_NUM, fill=RED)
        d.text((x + 34, y), place + " — " + cat, font=F_KICK, fill=INK_SOFT)
        d.text((x + 34, y + 14), head, font=F_SMALL_HEAD, fill=INK)
        for j, ln in enumerate(wrap(d, deck, F_SMALL_DECK, col_w - 34)):
            if j >= 1:
                break
            d.text((x + 34, y + 31), ln, font=F_SMALL_DECK, fill=MUTED)
        if row < 4:
            d.line([x, y + row_h - 1, x + col_w, y + row_h - 1],
                   fill=GREY_LINE, width=1)
    d.line([0, 720, W, 720], fill=GREY_LINE, width=1)

    # map + region chips
    my = 728
    draw_map(d, 24, my, 660, 110)
    d.text((24, my + 114), "WHERE IT HAPPENED — pins 01–13 match the stories above",
           font=F_KICK, fill=INK_SOFT)
    chip_x, chip_y = 708, my + 2
    d.text((chip_x, chip_y), "STORIES BY REGION", font=F_KICK, fill=RED)
    chip_y += 22
    for chip in REGION_CHIPS:
        tw = d.textlength(chip, font=F_STAT_L) + 18
        d.rounded_rectangle([chip_x, chip_y, chip_x + tw, chip_y + 22],
                            radius=11, fill=INK)
        d.text((chip_x + 9, chip_y + 4), chip, font=F_STAT_L,
               fill=(255, 255, 255))
        chip_y += 24

    # briefs: two columns
    by = 856
    d.text((24, by), "ALSO TODAY", font=F_KICK, fill=RED)
    by += 18
    bcol_w = (W - 48 - 16) // 2
    for i, (place, txt) in enumerate(BRIEFS):
        col, row = i % 2, i // 2
        x = 24 + col * (bcol_w + 16)
        y = by + row * 15
        line = place + ": " + txt
        d.text((x, y), "•  ", font=F_BRIEF, fill=RED)
        d.text((x + 12, y), line, font=F_BRIEF, fill=INK_SOFT)

    # date check + footer
    d.rectangle([0, 984, W, 1006], fill=(253, 238, 214))
    d.text((24, 988), "DATE CHECK", font=F_KICK, fill=RED)
    d.text((118, 988), DATE_CHECK, font=F_FOOT, fill=INK_SOFT)
    d.text((24, 1010), FOOTER, font=F_FOOT, fill=MUTED)
    return img

def main():
    img = render()
    img.save(OUT, format="PNG", optimize=True)

if __name__ == "__main__":
    main()
