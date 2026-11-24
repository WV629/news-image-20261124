#!/usr/bin/env python3
"""Render the Tuesday 24 November 2026 news poster, 1024x1024.

Layout follows the champion pattern of the news-image-20261122 winners:
giant date masthead, red headline strip, three hero stories up top, a
numbers panel, region pills, twelve small cards, a map plus two-column
briefs, a DATE CHECK box and a HOW SURE legend. Everything is drawn in
code with Pillow; no network, no fonts outside the system tree, and the
same input always writes the same PNG bytes.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (193, 18, 31)
NAVY = (20, 33, 61)
TEAL = (15, 118, 110)
GOLD = (180, 83, 9)
GREY = (110, 105, 95)
LINE = (210, 203, 188)

NOTO = "/usr/share/fonts/truetype/noto/"
DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf"


def pick(name, size):
    """Load a Noto face, falling back to DejaVu if the file is absent."""
    for path in (NOTO + name, DEJAVU % ("-Bold" if "Bold" in name else "")):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def serif_b(size):
    return pick("NotoSerif-Bold.ttf", size)


def serif_i(size):
    return pick("NotoSerif-Italic.ttf", size)


def sans_b(size):
    return pick("NotoSans-Bold.ttf", size)


def sans(size):
    return pick("NotoSans-Regular.ttf", size)


# ---------------------------------------------------------------- data

HEROES = [
    dict(n=1, place="TOKYO \u00b7 SEOUL", cat="MARKETS", region="EAST ASIA",
         status="CONFIRMED", src="Reuters \u00b7 Nikkei", lat=35.7, lon=139.7,
         art="chart", banner="ASIA RIDES THE HUANG RALLY",
         head="Asia rides the Huang rally",
         deck="Nikkei +4.5%, KOSPI +7.5% and Taiwan +9.1% as Nvidia's Monday "
              "surge of +31.5% \u2014 its biggest in 23 years \u2014 lifts the "
              "region and restores nearly $1tn of value."),
    dict(n=2, place="ULLEUNG, S. KOREA", cat="SECURITY", region="EAST ASIA",
         status="CONFIRMED", src="Reuters \u00b7 Yonhap", lat=37.5, lon=130.9,
         art="radar", banner="RUSSIAN JETS TRIGGER ISLAND ALERT",
         head="Russian jets trigger island alert",
         deck="An alert sounds on Ulleung at 07:52 as Russian jets enter "
              "the air-defence zone; lifted three minutes later. Seoul "
              "scrambles F-15Ks; no airspace was violated."),
    dict(n=3, place="MOSCOW", cat="WAR", region="EUROPE",
         status="CONFIRMED", src="Guardian \u00b7 Mediazona", lat=55.8, lon=37.6,
         art="files", banner="RUSSIA'S WAR DEAD NEAR 500,000",
         head="Russia's war dead near 500,000",
         deck="Hacked Rosstat records put war-linked deaths at 460,000\u2013"
              "470,000; Mediazona counts about 490,000 registered dead, and "
              "700,000 with the missing."),
]

SMALLS = [
    dict(n=4, place="WARSAW", cat="WAR", region="EUROPE", status="CONFIRMED",
         src="Reuters", lat=52.2, lon=21.0, art="awacs",
         head="NATO sends AWACS to Poland",
         deck="Three Kh-101 missiles hit Poland; NATO sends a warning jet."),
    dict(n=5, place="WASHINGTON", cat="JUSTICE", region="AMERICAS",
         status="OFFICIAL", src="White House", lat=38.9, lon=-77.0, art="gavel",
         head="Trump orders federal executions sped up",
         deck="A new memo pushes federal death sentences to move faster."),
    dict(n=6, place="RICHMOND", cat="TECH", region="AMERICAS",
         status="CONFIRMED", src="Reuters \u00b7 SCMP", lat=37.5, lon=-77.4,
         art="chip",
         head="Two states sue Musk's firms over Grok",
         deck="First state suits over Grok's sexualised images of children."),
    dict(n=7, place="BRUSSELS", cat="SANCTIONS", region="EUROPE",
         status="REPORTED", src="Al Jazeera", lat=50.8, lon=4.4, art="sanctions",
         head="EU plans sweeping new Russia sanctions",
         deck="Banks, crypto and sport are in the frame for the next package."),
    dict(n=8, place="WASHINGTON", cat="TRADE", region="AMERICAS",
         status="CONFIRMED", src="BBC \u00b7 DW", lat=38.9, lon=-77.0, art="ban",
         head="US puts Megaspeed on blacklist",
         deck="Nvidia chip scandal firm joins the export blacklist."),
    dict(n=9, place="TEHRAN", cat="CONFLICT", region="MIDDLE EAST",
         status="OFFICIAL", src="Reuters", lat=35.7, lon=51.4, art="ship",
         head="Iran vows to fight US naval blockade",
         deck="Tehran says it will resist any US blockade in the Gulf."),
    dict(n=10, place="CIKANDE", cat="DISASTER", region="SE ASIA",
         status="CONFIRMED", src="Antara \u00b7 Reuters", lat=-6.2, lon=106.3,
         art="fire",
         head="More bodies found in factory fire",
         deck="Death toll reaches 24, with about 30 still missing."),
    dict(n=11, place="TALLINN", cat="SECURITY", region="EUROPE",
         status="CLAIM", src="Japan Times", lat=59.4, lon=24.7, art="warning",
         head="Moscow warns Estonia over 'open war'",
         deck="Russia accuses Tallinn of preparing for war; Estonia denies."),
    dict(n=12, place="MANILA", cat="DEFENCE", region="SE ASIA",
         status="REPORTED", src="SCMP", lat=14.6, lon=121.0, art="money",
         head="Trump offers Manila $2.4bn \u2014 with a catch",
         deck="The aid comes with conditions on Manila's China ties."),
    dict(n=13, place="CANBERRA", cat="CLIMATE", region="OCEANIA",
         status="REPORTED", src="Reuters", lat=-35.3, lon=149.1, art="climate",
         head="COP31 fallout: blame game begins",
         deck="Nations trade blame after the summit collapses without a deal."),
    dict(n=14, place="KYIV", cat="WAR", region="EUROPE", status="REPORTED",
         src="Ukrainian Air Force", lat=50.5, lon=30.5, art="drones",
         head="Moscow strikes Ukraine with 153 drones",
         deck="Sixty of the drones were jet-powered in the overnight attack."),
    dict(n=15, place="PERM", cat="ENERGY", region="EUROPE", status="REPORTED",
         src="Reports", lat=58.0, lon=56.3, art="refinery",
         head="Fire at Lukoil refinery in Perm",
         deck="A blaze breaks out at the refinery after a drone strike."),
]

BRIEFS = [
    ("London", "Met seize 893kg cocaine in oranges", "Guardian", "EUROPE"),
    ("Tehran", "Iran flogs singer over hijab show", "Guardian", "MIDDLE EAST"),
    ("Dhaka", "Garment workers reject pay offer", "Reuters", "SOUTH ASIA"),
    ("Mexico City", "'El Chapo Isidro' faces trial", "AP", "AMERICAS"),
    ("Rome", "Warship downs target in Aster 30 test", "Reports", "EUROPE"),
    ("Riga", "Latvian PM refuses to restore Russia ties", "Reports", "EUROPE"),
    ("The Hague", "14 nations back ICJ Rohingya ruling", "France 24", "WORLD"),
    ("Brussels", "Rutte warns of rising NATO incursions", "NPR", "EUROPE"),
    ("Washington", "US sanctions Iran 'shadow banks'", "Al Jazeera", "MIDDLE EAST"),
    ("Washington", "Trump warns of action on Iran", "Reports", "MIDDLE EAST"),
    ("Gaza", "Israeli fire kills one, child dies of lead", "Reports", "MIDDLE EAST"),
    ("New York", "UN seeks AI safety framework", "UN News", "WORLD"),
    ("Seoul", "Minister quits over AI exam-cheating", "Reports", "EAST ASIA"),
    ("Beijing", "China sentences spy official to death", "Reports", "EAST ASIA"),
    ("Washington", "Vance is Nvidia board envoy", "Reports", "AMERICAS"),
    ("Kathmandu", "Nepal's PM in India for energy talks", "Reports", "SOUTH ASIA"),
    ("Ottawa", "PM brings Trump impersonator on stage", "Reports", "AMERICAS"),
    ("Khartoum", "Aid group accuses RSF of looting", "Yeni Safak", "AFRICA"),
    ("Sydney", "Australia to fine tech firms up to 5%", "Reuters", "OCEANIA"),
    ("PNG", "Ratifies Bougainville independence", "The Conversation", "OCEANIA"),
]

NUMBERS = [
    ("+31.5%", "Nvidia's Monday surge"),
    ("+7.5%", "KOSPI's Tuesday leap"),
    ("470,000", "war dead in hacked records"),
    ("3 MIN", "Ulleung alert, issued to lifted"),
    ("153", "drones fired at Ukraine"),
    ("893 KG", "cocaine seized in London"),
]

PILLS = [("EUROPE", 10), ("EAST ASIA", 4), ("SE ASIA", 2), ("SOUTH ASIA", 2),
         ("AMERICAS", 6), ("MIDDLE EAST", 5), ("AFRICA", 1), ("OCEANIA", 3),
         ("WORLD", 2)]

TIMELINE = ("00:00 Asia opens higher (Nikkei +4.5%, KOSPI +7.5%)  \u00b7  "
            "01:30 Lukoil refinery fire, Perm  \u00b7  02:40 US blacklists "
            "Megaspeed  \u00b7  07:52 KST Ulleung alert sounds \u2014 lifted 07:55")

DATECHECK = ("DATE CHECK \u2014 Every story here happened, or was first "
             "reported, on Tuesday 24 November 2026 (UTC). Left out as other "
             "days' news: Huang reinstated (Mon) \u00b7 COP31 collapses (Sun) "
             "\u00b7 Democrats' 258 seats (Mon) \u00b7 Kyiv: 14 killed (Mon) "
             "\u00b7 CrowdStrike buys Zscaler $44bn (Mon) \u00b7 US weighs "
             "Korea digital probe (Sun) \u00b7 India\u2013EU pact (Sun) "
             "\u00b7 Zelensky confirms Libya ship sinking (Mon)")

LEGEND = ("HOW SURE:  CONFIRMED = two or more outlets  \u00b7  OFFICIAL = on "
          "the record  \u00b7  REPORTED = one outlet  \u00b7  CLAIM = one "
          "side's account.  Claims are attributed, not stated as fact.  "
          "Illustrations and map drawn in code.")

# ------------------------------------------------------- text helpers

def wrap_to(d, text, font, width):
    """Greedy wrap: pack as many whole words per line as fit in `width`."""
    out = []
    for para in text.split("\n"):
        line = ""
        for word in para.split():
            trial = (line + " " + word).strip()
            if d.textlength(trial, font=font) <= width or not line:
                line = trial
            else:
                out.append(line)
                line = word
        if line:
            out.append(line)
    return out


def fit_lines(d, text, font, width, max_lines):
    """Wrap and, if too long, trim the last line with an ellipsis."""
    lines = wrap_to(d, text, font, width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while d.textlength(lines[-1] + "\u2026", font=font) > width and len(lines[-1]) > 1:
            lines[-1] = lines[-1][:-1]
        lines[-1] += "\u2026"
    return lines


def text(d, xy, s, font, fill=INK, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


# ------------------------------------------------------- flat scenes

def scene(d, kind, box, bg):
    """One flat vector-style illustration inside `box` (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=bg)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    w, h = x1 - x0, y1 - y0
    if kind == "chart":
        d.rectangle([x0 + 18, y1 - 34, x0 + 42, y1 - 14], fill=TEAL)
        d.rectangle([x0 + 50, y1 - 52, x0 + 74, y1 - 14], fill=TEAL)
        d.rectangle([x0 + 82, y1 - 70, x0 + 106, y1 - 14], fill=GOLD)
        d.line([(x0 + 14, y1 - 30), (x0 + 62, y1 - 62), (x0 + 110, y1 - 88),
                (x0 + 158, y1 - 96)], fill=RED, width=5)
        d.polygon([(x0 + 158, y1 - 96), (x0 + 148, y1 - 92), (x0 + 158, y1 - 84)],
                  fill=RED)
        d.ellipse([x1 - 52, y0 + 12, x1 - 16, y0 + 48], fill=(255, 255, 255))
        d.text((x1 - 34, y0 + 30), "$", font=sans_b(22), fill=TEAL, anchor="mm")
    elif kind == "radar":
        for r in (52, 38, 24):
            d.ellipse([cx - r, cy - r + 6, cx + r, cy + r + 6], outline=(255, 255, 255), width=2)
        d.line([(cx, cy + 6), (cx + 40, cy - 26)], fill=(255, 255, 255), width=3)
        d.ellipse([cx + 34, cy - 32, cx + 46, cy - 20], fill=RED)
        d.polygon([(x0 + 20, y1 - 26), (x0 + 44, y1 - 34), (x0 + 44, y1 - 18)],
                  fill=(255, 255, 255))
        d.polygon([(x0 + 44, y1 - 30), (x0 + 96, y1 - 44), (x0 + 96, y1 - 20)],
                  fill=(255, 255, 255))
        d.ellipse([x0 + 96, y1 - 48, x0 + 104, y1 - 40], fill=RED)
    elif kind == "files":
        for i, off in enumerate((0, 8, 16)):
            d.rectangle([x0 + 26 + off, y0 + 22 + off, x0 + 96 + off, y1 - 18 + off],
                        fill=(255, 255, 255), outline=INK)
            for j, yy in enumerate((y0 + 34 + off, y0 + 48 + off, y0 + 62 + off)):
                d.rectangle([x0 + 34 + off, yy, x0 + 88 + off, yy + 5],
                            fill=RED if j == 1 else (200, 195, 180))
        d.ellipse([x1 - 46, y0 + 14, x1 - 14, y0 + 46], fill=RED)
        d.text((x1 - 30, y0 + 30), "?", font=sans_b(20), fill=(255, 255, 255), anchor="mm")
    elif kind == "awacs":
        d.ellipse([cx - 46, cy - 8, cx + 46, cy + 8], fill=(255, 255, 255))
        d.polygon([(cx + 46, cy), (cx + 78, cy - 10), (cx + 78, cy + 10)], fill=(255, 255, 255))
        d.polygon([(cx - 30, cy - 6), (cx - 52, cy - 22), (cx - 18, cy - 6)], fill=(255, 255, 255))
        d.line([(cx, cy - 8), (cx, cy - 30)], fill=(255, 255, 255), width=3)
        d.ellipse([cx - 16, cy - 40, cx + 16, cy - 24], fill=GOLD)
    elif kind == "gavel":
        d.rectangle([cx - 34, cy - 26, cx + 34, cy - 12], fill=(120, 72, 20))
        d.rectangle([cx - 6, cy - 12, cx + 6, cy + 30], fill=(120, 72, 20))
        d.rectangle([cx - 26, cy + 30, cx + 26, cy + 38], fill=(120, 72, 20))
        d.ellipse([x1 - 44, y0 + 12, x1 - 18, y0 + 38], fill=RED)
        d.text((x1 - 31, y0 + 25), "!", font=sans_b(18), fill=(255, 255, 255), anchor="mm")
    elif kind == "chip":
        d.rectangle([cx - 30, cy - 30, cx + 30, cy + 30], fill=(255, 255, 255))
        d.rectangle([cx - 16, cy - 16, cx + 16, cy + 16], fill=NAVY)
        for i in range(4):
            yy = cy - 24 + i * 16
            d.line([(cx - 42, yy), (cx - 30, yy)], fill=(255, 255, 255), width=3)
            d.line([(cx + 30, yy), (cx + 42, yy)], fill=(255, 255, 255), width=3)
        d.ellipse([x1 - 46, y0 + 12, x1 - 14, y0 + 44], fill=RED)
        d.line([(x1 - 38, y0 + 20), (x1 - 22, y0 + 36)], fill=(255, 255, 255), width=4)
        d.line([(x1 - 22, y0 + 20), (x1 - 38, y0 + 36)], fill=(255, 255, 255), width=4)
    elif kind == "sanctions":
        for i in range(8):
            import math
            a = math.pi * i / 4
            px, py = cx + int(34 * math.cos(a)), cy + int(30 * math.sin(a))
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GOLD)
        d.rectangle([cx - 20, cy - 12, cx + 20, cy + 14], fill=(255, 255, 255))
        d.line([(cx - 26, cy + 18), (cx + 26, cy - 16)], fill=RED, width=5)
    elif kind == "ban":
        d.rectangle([cx - 28, cy - 28, cx + 28, cy + 28], fill=(255, 255, 255))
        d.rectangle([cx - 14, cy - 14, cx + 14, cy + 14], fill=INK)
        d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], outline=RED, width=6)
        d.line([(cx - 24, cy + 24), (cx + 24, cy - 24)], fill=RED, width=6)
    elif kind == "ship":
        d.polygon([(x0 + 22, y1 - 34), (x0 + 118, y1 - 34), (x0 + 106, y1 - 14),
                   (x0 + 34, y1 - 14)], fill=(255, 255, 255))
        d.rectangle([x0 + 52, y1 - 56, x0 + 88, y1 - 34], fill=(255, 255, 255))
        d.line([(x0 + 16, y1 - 40), (x0 + 124, y1 - 40)], fill=RED, width=4)
        d.line([(x0 + 16, y1 - 40), (x0 + 40, y1 - 52)], fill=RED, width=4)
        d.line([(x0 + 16, y1 - 40), (x0 + 40, y1 - 28)], fill=RED, width=4)
        for xx in range(x0 + 14, x1 - 10, 18):
            d.arc([xx, y0 + 14, xx + 14, y0 + 30], 0, 180, fill=(255, 255, 255), width=3)
    elif kind == "fire":
        d.polygon([(cx - 34, y1 - 16), (cx - 20, y1 - 52), (cx - 8, y1 - 30),
                   (cx + 4, y1 - 58), (cx + 16, y1 - 30), (cx + 30, y1 - 50),
                   (cx + 36, y1 - 16)], fill=(255, 120, 0))
        d.polygon([(cx - 16, y1 - 16), (cx - 6, y1 - 40), (cx + 6, y1 - 24),
                   (cx + 16, y1 - 16)], fill=(255, 200, 0))
        d.rectangle([x0 + 18, y1 - 12, x1 - 18, y1 - 8], fill=(255, 255, 255))
    elif kind == "warning":
        d.rectangle([x0 + 24, y0 + 18, x1 - 24, y0 + 52], fill=(255, 255, 255))
        d.polygon([(x0 + 40, y0 + 52), (x0 + 40, y0 + 66), (x0 + 56, y0 + 52)],
                  fill=(255, 255, 255))
        d.text((cx, y0 + 35), "!", font=sans_b(24), fill=RED, anchor="mm")
        d.rectangle([x0 + 24, y1 - 26, x1 - 24, y1 - 14], fill=RED)
    elif kind == "money":
        d.rectangle([x0 + 16, cy - 20, x1 - 16, cy + 20], fill=(255, 255, 255))
        d.ellipse([cx - 16, cy - 14, cx + 16, cy + 14], outline=TEAL, width=3)
        d.text((cx, cy), "$", font=sans_b(18), fill=TEAL, anchor="mm")
        d.rectangle([x0 + 16, cy - 20, x1 - 16, cy - 12], fill=TEAL)
    elif kind == "climate":
        d.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], fill=(120, 190, 220))
        d.arc([cx - 32, cy - 32, cx + 32, cy + 32], 200, 340, fill=(40, 140, 60), width=8)
        d.arc([cx - 32, cy - 32, cx + 32, cy + 32], 20, 120, fill=(40, 140, 60), width=8)
        for xx, yy in ((cx + 34, cy - 30), (cx - 40, cy - 26), (cx + 40, cy + 28)):
            d.line([(xx - 8, yy), (xx + 8, yy)], fill=GOLD, width=3)
            d.line([(xx, yy - 8), (xx, yy + 8)], fill=GOLD, width=3)
    elif kind == "drones":
        for i, (dx, dy) in enumerate(((-44, -18), (-14, -30), (16, -14), (44, -26),
                                      (-28, 6), (6, 16), (38, 8))):
            d.ellipse([cx + dx - 5, cy + dy - 5, cx + dx + 5, cy + dy + 5], fill=INK)
            d.line([(cx + dx - 10, cy + dy), (cx + dx + 10, cy + dy)],
                   fill=(255, 255, 255), width=2)
        d.ellipse([x1 - 46, y0 + 10, x1 - 16, y0 + 40], fill=RED)
        d.text((x1 - 31, y0 + 25), "153", font=sans_b(12), fill=(255, 255, 255), anchor="mm")
    elif kind == "refinery":
        for bx in (x0 + 26, x0 + 56, x0 + 86):
            d.rectangle([bx, y1 - 52, bx + 20, y1 - 14], fill=(255, 255, 255))
            d.polygon([(bx, y1 - 52), (bx + 10, y1 - 66), (bx + 20, y1 - 52)],
                      fill=(255, 255, 255))
        d.polygon([(cx - 8, y1 - 66), (cx, y1 - 86), (cx + 8, y1 - 66)], fill=(255, 120, 0))
        d.polygon([(cx - 4, y1 - 66), (cx, y1 - 78), (cx + 4, y1 - 66)], fill=(255, 200, 0))
    else:
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(255, 255, 255))


def mini_scene(d, kind, box, bg):
    """Small flat motif for a 163x38 card banner; all sizes scale off the
    banner height so nothing can spill past the box edges."""
    import math
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=bg)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    u = (y1 - y0) / 2.0
    if kind == "awacs":
        d.ellipse([cx - 0.9 * u, cy - 0.28 * u, cx + 0.9 * u, cy + 0.28 * u],
                  fill=(255, 255, 255))
        d.ellipse([cx - 0.32 * u, cy - 0.72 * u, cx + 0.32 * u, cy - 0.3 * u],
                  fill=GOLD)
        d.polygon([(cx + 0.9 * u, cy), (cx + 1.25 * u, cy - 0.3 * u),
                   (cx + 1.25 * u, cy + 0.3 * u)], fill=(255, 255, 255))
    elif kind == "gavel":
        d.rectangle([cx - 0.7 * u, cy - 0.6 * u, cx + 0.7 * u, cy - 0.2 * u],
                    fill=(120, 72, 20))
        d.rectangle([cx - 0.08 * u, cy - 0.2 * u, cx + 0.08 * u, cy + 0.55 * u],
                    fill=(120, 72, 20))
        d.rectangle([cx - 0.5 * u, cy + 0.55 * u, cx + 0.5 * u, cy + 0.72 * u],
                    fill=(120, 72, 20))
    elif kind == "chip":
        d.rectangle([cx - 0.55 * u, cy - 0.55 * u, cx + 0.55 * u, cy + 0.55 * u],
                    fill=(255, 255, 255))
        d.rectangle([cx - 0.28 * u, cy - 0.28 * u, cx + 0.28 * u, cy + 0.28 * u],
                    fill=NAVY)
        for i in range(3):
            yy = cy - 0.35 * u + i * 0.35 * u
            d.line([(cx - 0.8 * u, yy), (cx - 0.55 * u, yy)], fill=(255, 255, 255), width=2)
            d.line([(cx + 0.55 * u, yy), (cx + 0.8 * u, yy)], fill=(255, 255, 255), width=2)
        d.line([(cx - 0.55 * u, cy + 0.55 * u), (cx + 0.55 * u, cy - 0.55 * u)],
               fill=RED, width=3)
    elif kind == "sanctions":
        for i in range(6):
            a = math.pi * i / 3
            px, py = cx + 0.55 * u * math.cos(a), cy + 0.55 * u * math.sin(a)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=GOLD)
        d.rectangle([cx - 0.3 * u, cy - 0.2 * u, cx + 0.3 * u, cy + 0.2 * u],
                    fill=(255, 255, 255))
        d.line([(cx - 0.7 * u, cy + 0.55 * u), (cx + 0.7 * u, cy - 0.55 * u)],
               fill=RED, width=3)
    elif kind == "ban":
        d.rectangle([cx - 0.5 * u, cy - 0.5 * u, cx + 0.5 * u, cy + 0.5 * u],
                    fill=(255, 255, 255))
        d.ellipse([cx - 0.62 * u, cy - 0.62 * u, cx + 0.62 * u, cy + 0.62 * u],
                  outline=RED, width=3)
        d.line([(cx - 0.44 * u, cy + 0.44 * u), (cx + 0.44 * u, cy - 0.44 * u)],
               fill=RED, width=3)
    elif kind == "ship":
        d.polygon([(cx - 0.95 * u, cy + 0.05 * u), (cx + 0.95 * u, cy + 0.05 * u),
                   (cx + 0.7 * u, cy + 0.6 * u), (cx - 0.7 * u, cy + 0.6 * u)],
                  fill=(255, 255, 255))
        d.rectangle([cx - 0.3 * u, cy - 0.4 * u, cx + 0.3 * u, cy + 0.05 * u],
                    fill=(255, 255, 255))
        d.line([(cx, cy - 0.4 * u), (cx, cy - 0.75 * u)], fill=(255, 255, 255), width=2)
        d.polygon([(cx, cy - 0.75 * u), (cx + 0.35 * u, cy - 0.6 * u), (cx, cy - 0.45 * u)],
                  fill=RED)
    elif kind == "fire":
        d.polygon([(cx - 0.6 * u, cy + 0.6 * u), (cx - 0.35 * u, cy - 0.35 * u),
                   (cx - 0.1 * u, cy + 0.1 * u), (cx + 0.1 * u, cy - 0.6 * u),
                   (cx + 0.3 * u, cy + 0.05 * u), (cx + 0.55 * u, cy - 0.25 * u),
                   (cx + 0.6 * u, cy + 0.6 * u)], fill=(255, 120, 0))
        d.polygon([(cx - 0.28 * u, cy + 0.6 * u), (cx - 0.1 * u, cy - 0.1 * u),
                   (cx + 0.12 * u, cy + 0.2 * u), (cx + 0.28 * u, cy + 0.6 * u)],
                  fill=(255, 200, 0))
    elif kind == "warning":
        d.rectangle([cx - 0.75 * u, cy - 0.6 * u, cx + 0.75 * u, cy + 0.3 * u],
                    fill=(255, 255, 255))
        d.polygon([(cx - 0.4 * u, cy + 0.3 * u), (cx - 0.4 * u, cy + 0.65 * u),
                   (cx - 0.1 * u, cy + 0.3 * u)], fill=(255, 255, 255))
        d.text((cx, cy - 0.12 * u), "!", font=sans_b(18), fill=RED, anchor="mm")
    elif kind == "money":
        d.rectangle([cx - 0.95 * u, cy - 0.42 * u, cx + 0.95 * u, cy + 0.42 * u],
                    fill=(255, 255, 255))
        d.ellipse([cx - 0.3 * u, cy - 0.3 * u, cx + 0.3 * u, cy + 0.3 * u],
                  outline=TEAL, width=2)
        d.text((cx, cy), "$", font=sans_b(13), fill=TEAL, anchor="mm")
    elif kind == "climate":
        d.ellipse([cx - 0.55 * u, cy - 0.55 * u, cx + 0.55 * u, cy + 0.55 * u],
                  fill=(120, 190, 220))
        d.arc([cx - 0.55 * u, cy - 0.55 * u, cx + 0.55 * u, cy + 0.55 * u],
              200, 340, fill=(40, 140, 60), width=5)
        d.arc([cx - 0.55 * u, cy - 0.55 * u, cx + 0.55 * u, cy + 0.55 * u],
              20, 120, fill=(40, 140, 60), width=5)
    elif kind == "drones":
        for dx, dy in ((-0.6, -0.25), (0, 0.25), (0.6, -0.25)):
            d.ellipse([cx + dx * u - 3, cy + dy * u - 3, cx + dx * u + 3, cy + dy * u + 3],
                      fill=INK)
            d.line([(cx + dx * u - 7, cy + dy * u), (cx + dx * u + 7, cy + dy * u)],
                   fill=(255, 255, 255), width=2)
    elif kind == "refinery":
        for bx in (cx - 0.75 * u, cx - 0.15 * u):
            d.rectangle([bx, cy - 0.1 * u, bx + 0.45 * u, cy + 0.6 * u],
                        fill=(255, 255, 255))
            d.polygon([(bx, cy - 0.1 * u), (bx + 0.22 * u, cy - 0.45 * u),
                       (bx + 0.45 * u, cy - 0.1 * u)], fill=(255, 255, 255))
        d.polygon([(cx + 0.55 * u, cy + 0.1 * u), (cx + 0.72 * u, cy - 0.45 * u),
                   (cx + 0.9 * u, cy + 0.1 * u)], fill=(255, 120, 0))
    else:
        d.ellipse([cx - 0.4 * u, cy - 0.4 * u, cx + 0.4 * u, cy + 0.4 * u],
                  fill=(255, 255, 255))


# ------------------------------------------------------- world map

# Rough continent outlines in (lon, lat), drawn as a dotted-grid sea with
# flat land shapes. Coordinates are approximate on purpose: the map is a
# locator, not a survey.
LAND = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-82, 66),
     (-76, 62), (-65, 60), (-55, 52), (-60, 47), (-70, 44), (-75, 35),
     (-80, 32), (-84, 30), (-90, 21), (-97, 26), (-105, 23), (-115, 29),
     (-125, 40), (-124, 49), (-135, 58), (-155, 58), (-165, 60)],
    [(-80, 9), (-72, 12), (-62, 9), (-52, 5), (-44, -3), (-35, -8),
     (-40, -20), (-48, -28), (-58, -35), (-65, -41), (-70, -52), (-74, -54),
     (-73, -44), (-72, -30), (-77, -12), (-81, -6), (-80, 2)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (8, 57), (12, 56), (18, 56),
     (21, 55), (24, 59), (30, 60), (28, 70), (40, 68), (32, 60), (28, 55),
     (24, 45), (19, 42), (12, 44), (3, 43), (-2, 37)],
    [(-6, 35), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12), (48, 11),
     (51, 12), (44, -1), (40, -10), (36, -18), (33, -26), (28, -33), (19, -35),
     (16, -29), (13, -18), (12, -6), (9, 4), (-8, 5), (-15, 12), (-17, 15)],
    [(60, 70), (70, 72), (90, 75), (110, 74), (130, 72), (150, 70), (170, 67),
     (178, 65), (162, 60), (158, 53), (142, 45), (140, 39), (130, 33),
     (122, 31), (120, 23), (109, 18), (105, 9), (100, 7), (97, 16), (92, 21),
     (88, 22), (80, 13), (77, 8), (72, 20), (66, 25), (60, 25), (57, 26),
     (52, 28), (48, 30), (44, 29), (40, 36), (36, 36), (30, 36), (27, 41),
     (23, 40), (22, 45), (19, 46), (15, 45), (12, 46), (8, 44), (5, 43)],
    [(113, -22), (114, -32), (124, -33), (134, -32), (140, -38), (147, -39),
     (150, -37), (153, -27), (153, -17), (146, -19), (142, -11), (137, -12),
     (132, -12), (126, -14), (122, -17), (114, -22)],
]


def project(lon, lat, box):
    """Equirectangular projection of lon/lat into `box` (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    x = x0 + (lon + 170.0) / 360.0 * (x1 - x0)
    y = y0 + (78.0 - lat) / 140.0 * (y1 - y0)
    return x, y


def draw_world(d, box, pins):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(214, 228, 235))
    for poly in LAND:
        pts = [project(lon, lat, box) for lon, lat in poly]
        d.polygon(pts, fill=(232, 222, 200), outline=(180, 168, 145))
    for lon in range(-150, 181, 30):
        gx, _ = project(lon, 0, box)
        d.line([(gx, y0), (gx, y1)], fill=(200, 214, 222))
    for lat in (-40, 0, 40):
        _, gy = project(0, lat, box)
        d.line([(x0, gy), (x1, gy)], fill=(200, 214, 222))
    placed = []
    for n, lat, lon in pins:
        px, py = project(lon, lat, box)
        while any((px - qx) ** 2 + (py - qy) ** 2 < 15 ** 2 for qx, qy in placed):
            px += 14
            py -= 12
        placed.append((px, py))
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255))
        d.text((px, py + 1), str(n), font=sans_b(8), fill=(255, 255, 255), anchor="mm")


# ------------------------------------------------------- cards

STATUS_FILL = {"CONFIRMED": TEAL, "OFFICIAL": NAVY, "REPORTED": GOLD, "CLAIM": RED}


def status_tag(d, x, y, status):
    """Small filled tag with the confidence status; returns its width."""
    f = sans_b(8)
    w = d.textlength(status, font=f) + 10
    d.rectangle([x, y, x + w, y + 12], fill=STATUS_FILL[status])
    d.text((x + 5, y + 6), status, font=f, fill=(255, 255, 255), anchor="lm")
    return w


def hero_card(d, s, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=LINE)
    art_h = 118
    art_bg = {1: NAVY, 2: (90, 40, 40), 3: (60, 60, 60)}[s["n"]]
    scene(d, s["art"], (x, y, x + w, y + art_h), art_bg)
    d.rectangle([x, y + art_h - 26, x + w, y + art_h], fill=RED)
    d.text((x + 10, y + art_h - 13), s["banner"], font=sans_b(13),
           fill=(255, 255, 255), anchor="lm")
    by = y + art_h + 8
    d.text((x + 10, by), "%d  %s" % (s["n"], s["place"]), font=sans_b(11), fill=INK)
    status_tag(d, x + w - 78, by - 1, s["status"])
    hy = by + 20
    head_lines = fit_lines(d, s["head"], serif_b(19), w - 20, 2)
    for i, line in enumerate(head_lines):
        d.text((x + 10, hy + i * 23), line, font=serif_b(19), fill=INK)
    dy = hy + len(head_lines) * 23
    for i, line in enumerate(fit_lines(d, s["deck"], sans(11), w - 20, 3)):
        d.text((x + 10, dy + i * 15), line, font=sans(11), fill=(60, 58, 52))
    d.text((x + 10, y + h - 12), "Source: " + s["src"], font=sans(9), fill=GREY)


def mini_card(d, s, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=LINE)
    art_h = 38
    art_bg = [NAVY, (90, 40, 40), (40, 70, 60), (60, 60, 60), TEAL, GOLD][s["n"] % 6]
    mini_scene(d, s["art"], (x, y, x + w, y + art_h), art_bg)
    d.rectangle([x, y + art_h - 13, x + 64, y + art_h], fill=RED)
    d.text((x + 4, y + art_h - 7), s["cat"], font=sans_b(8),
           fill=(255, 255, 255), anchor="lm")
    ly = y + art_h + 4
    d.text((x + 6, ly), "%d %s" % (s["n"], s["place"]), font=sans_b(9), fill=INK)
    status_tag(d, x + w - 62, ly - 1, s["status"])
    hy = ly + 13
    head_lines = fit_lines(d, s["head"], sans_b(11), w - 12, 2)
    for i, line in enumerate(head_lines):
        d.text((x + 6, hy + i * 13), line, font=sans_b(11), fill=INK)
    dy = hy + len(head_lines) * 13 + 1
    for i, line in enumerate(fit_lines(d, s["deck"], sans(9), w - 12, 2)):
        d.text((x + 6, dy + i * 11), line, font=sans(9), fill=(60, 58, 52))
    d.text((x + 6, y + h - 9), s["src"], font=sans(8), fill=GREY)


# ------------------------------------------------------- page

def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Top bar
    d.rectangle([0, 0, W, 22], fill=NAVY)
    d.text((10, 11), "THE WORLD IN ONE DAY", font=sans_b(12),
           fill=(255, 255, 255), anchor="lm")
    d.text((W - 10, 11), "35 STORIES \u00b7 9 REGIONS \u00b7 EVERY ONE DATED "
           "TUESDAY 24 NOVEMBER 2026 (UTC)", font=sans(10),
           fill=(230, 200, 120), anchor="rm")

    # Masthead
    d.text((W // 2, 58), "Tuesday 24 November 2026", font=serif_b(58),
           fill=INK, anchor="mm")
    d.line([(10, 88), (W - 10, 88)], fill=INK, width=2)

    # Red headline strip
    d.text((W // 2, 104), "Asia rides the Huang rally  \u00b7  Russian jets "
           "trigger island alert  \u00b7  Russia's war dead near 500,000",
           font=serif_i(18), fill=RED, anchor="mm")
    d.line([(10, 118), (W - 10, 118)], fill=INK, width=1)

    # UTC timeline
    d.rectangle([0, 122, W, 142], fill=NAVY)
    d.text((10, 132), "THE DAY IN UTC", font=sans_b(10), fill=(230, 200, 120), anchor="lm")
    d.text((150, 132), TIMELINE, font=sans(10), fill=(255, 255, 255), anchor="lm")

    # Numbers panel
    d.text((10, 150), "THE DAY IN NUMBERS", font=sans_b(11), fill=INK)
    cell_w = (W - 20) // 6
    for i, (big, cap) in enumerate(NUMBERS):
        cx0 = 10 + i * cell_w
        if i:
            d.line([(cx0 - 4, 166), (cx0 - 4, 196)], fill=LINE)
        d.text((cx0 + cell_w // 2, 162), big, font=serif_b(24),
               fill=RED if i % 2 == 0 else TEAL, anchor="ma")
        d.text((cx0 + cell_w // 2, 190), cap, font=sans(9), fill=GREY, anchor="ma")
    d.line([(10, 202), (W - 10, 202)], fill=INK, width=1)

    # Region pills
    px = 10
    for name, count in PILLS:
        label = "%s %d" % (name, count)
        w = d.textlength(label, font=sans_b(10)) + 16
        d.rounded_rectangle([px, 208, px + w, 228], radius=10, fill=NAVY)
        d.text((px + 8, 218), label, font=sans_b(10), fill=(255, 255, 255), anchor="lm")
        px += w + 6

    # Hero row
    hero_y, hero_h, hero_w = 236, 252, 330
    for i, s in enumerate(HEROES):
        hero_card(d, s, 8 + i * (hero_w + 9), hero_y, hero_w, hero_h)

    # Small cards, 2 rows x 6
    gap, cols = 6, 6
    cw = (W - 16 - gap * (cols - 1)) // cols
    ch = 112
    for i, s in enumerate(SMALLS):
        r, c = divmod(i, cols)
        mini_card(d, s, 8 + c * (cw + gap), 496 + r * (ch + 8), cw, ch)

    # Bottom band: map + briefs
    by = 736
    d.text((10, by + 2), "WHERE IT HAPPENED", font=sans_b(11), fill=INK)
    draw_world(d, (8, by + 20, 324, by + 196),
               [(s["n"], s["lat"], s["lon"]) for s in HEROES + SMALLS])
    d.text((8, by + 202), "Pins 1\u201315: the hero and small-card stories.",
           font=sans(9), fill=GREY)

    bx = 340
    d.text((bx, by + 2), "ALSO ON TUESDAY 24 NOVEMBER \u2014 20 MORE STORIES",
           font=sans_b(11), fill=INK)
    col_w = (W - bx - 8 - 10) // 2
    for i, (place, txt, src, _reg) in enumerate(BRIEFS):
        col, row = divmod(i, 10)
        x = bx + col * (col_w + 10)
        yy = by + 22 + row * 19
        src_txt = "(%s)" % src
        sw = d.textlength(src_txt, font=sans(9))
        body = "%s \u2014 %s" % (place, txt)
        limit = col_w - 22 - sw - 8
        if d.textlength(body, font=sans(11)) > limit:
            words = body.split(" ")
            body = ""
            for wd in words:
                trial = (body + " " + wd).strip()
                if d.textlength(trial + " \u2026", font=sans(11)) <= limit:
                    body = trial
                else:
                    break
            body += " \u2026"
        d.text((x, yy), "%d" % (16 + i), font=sans_b(11), fill=RED)
        d.text((x + 22, yy), body, font=sans(11), fill=INK)
        d.text((x + col_w - sw, yy + 1), src_txt, font=sans(9), fill=GREY)

    # DATE CHECK
    dy = 946
    d.rectangle([8, dy, W - 8, dy + 38], outline=RED, width=2)
    check_lines = wrap_to(d, DATECHECK, sans_b(9), W - 40)
    for i, line in enumerate(check_lines[:3]):
        d.text((16, dy + 9 + i * 11), line, font=sans_b(9), fill=RED)

    # Legend + footer
    d.text((10, 994), "HOW SURE:  CONFIRMED = two or more outlets  \u00b7  OFFICIAL = on "
           "the record  \u00b7  REPORTED = one outlet  \u00b7  CLAIM = one side's account.",
           font=sans(9), fill=GREY, anchor="lm")
    d.text((W - 10, 994), "Compiled Tue 24 Nov 2026 (UTC)", font=sans(9),
           fill=GREY, anchor="rm")
    d.text((10, 1010), "Claims are attributed, not stated as fact.  Illustrations "
           "and map drawn in code.", font=sans(9), fill=GREY, anchor="lm")
    return img


if __name__ == "__main__":
    render().save("entry.png", optimize=True)
    print("wrote entry.png")
