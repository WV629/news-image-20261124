#!/usr/bin/env python3
"""One-page broadsheet: Tuesday 24 November 2026 world news, drawn with Pillow.

The news itself lives in the JSON block below (verified Tuesday morning
against Reuters, AP, CNN, Guardian, Bloomberg, Yonhap, Nikkei, SCMP,
Japan Times and the White House). The renderer is table-driven: it turns
the data into draw operations and runs them, so no story is laid out by
hand. Deterministic: no network, no clock, no randomness — two runs give
byte-identical PNGs. Run it: python3 generate.py (writes entry.png).
"""
import json
import os
from PIL import Image as Pic, ImageDraw as Pen, ImageFont as Typ

_HERE = os.path.dirname(os.path.abspath(__file__))
OUT = _HERE + "/entry.png"
S = 1024

DATA = """{
  "mast": ["THE WORLD IN ONE IMAGE", "TUESDAY 24 NOVEMBER 2026  \\u00b7  27 STORIES  \\u00b7  5 REGIONS  \\u00b7  ONE DAY"],
  "strip": [["+31.5%", "Nvidia's Monday surge"], ["+7.5%", "KOSPI's Tuesday leap"], ["470,000", "Russian war dead"], ["3", "Missiles hit Poland"], ["5 min", "Ulleung alert lifted after"], ["2", "States sue Musk's firms"]],
  "leads": [
    {"n": "01", "pl": "TOKYO \\u00b7 SEOUL", "cat": "MARKETS", "h": "Asia rides the Huang rally", "d": "Nikkei +4.5%, KOSPI +7.5%, Taiwan +9.1% after Wall Street's best day since April 2025. Nvidia +31.5%.", "src": "Reuters \\u00b7 Nikkei", "art": "asia"},
    {"n": "02", "pl": "ULLEUNG, S. KOREA", "cat": "SECURITY", "h": "Russian jets trigger island alert", "d": "Seoul tells Ulleung residents to shelter as Russian jets enter the air-defence zone; alert lifted in minutes.", "src": "Reuters \\u00b7 Yonhap", "art": "alert"},
    {"n": "03", "pl": "MOSCOW", "cat": "WAR", "h": "Russia's war dead near 500,000", "d": "Hacked Rosstat records put war-linked deaths at 460,000-470,000; Meduza counts 700,000+ with the missing.", "src": "Guardian \\u00b7 Bloomberg", "art": "records"}
  ],
  "seconds": [
    ["04", "WARSAW", "DEFENCE", "NATO sends AWACS to Poland", "After 3 missiles land, NATO sends an early-warning jet to its eastern flank.", "Reuters"],
    ["05", "WASHINGTON", "JUSTICE", "Trump orders federal executions sped up", "Memo seeks death penalty for child murder, rape and trafficking killings.", "White House \\u00b7 AP"],
    ["06", "LOS ANGELES", "POLITICS", "Congressman Gomez quits over ethics report", "House panel finds 'substantial evidence' of sexual misconduct; out Dec 1.", "CNN \\u00b7 WSJ"],
    ["07", "RICHMOND", "TECH", "Two states sue Musk's firms over Grok", "Virginia and Oregon say 'spicy mode' made non-consensual sexual images.", "Reuters \\u00b7 AP"],
    ["08", "CANBERRA", "CLIMATE", "COP31 fallout: blame game begins", "Australia faces backlash; Pacific nations despair after the talks collapse.", "Reuters"],
    ["09", "TEHRAN", "CONFLICT", "Iran vows to fight US naval blockade", "Tehran vows to use 'all its tools' against the blockade.", "Reuters"],
    ["10", "CIKANDE", "DISASTER", "More bodies found in factory fire", "Search goes on at the Indonesian candy plant; 24 dead Monday, ~30 missing.", "Manila Times \\u00b7 Reuters"],
    ["11", "TALLINN", "SECURITY", "Moscow warns Estonia over 'open war'", "Russia accuses Tallinn of hostile acts on the verge of triggering open war.", "Japan Times"],
    ["12", "NEW DELHI", "TRADE", "India-EU trade pact set for Dec 16", "Landmark deal to be signed in Brussels on Dec 16 during Modi's visit.", "Sunday Guardian"],
    ["13", "MANILA", "DEFENCE", "Trump offers Manila $2.4bn \\u2014 with a catch", "US self-defence aid for the Philippines comes with conditions.", "SCMP"]
  ],
  "shorts": [
    ["London", "GTA VI hacker Arion Kurtaj, 21, gets 7 years; free on time served."],
    ["Manchester", "Thousands evacuated from a Don Toliver show after a substance release."],
    ["New York", "UN chief calls for an AI risk-management framework within a year."],
    ["Beijing", "China sentences an official to death for spying and leaking secrets."],
    ["Pyongyang", "North Korea threatens to close its Swiss diplomatic office."],
    ["Jakarta", "Prabowo taps a loyalist and a tycoon's cousin as VP picks."],
    ["Washington", "Vance tapped as Trump's emissary to the Nvidia board."],
    ["Iowa", "Trump orders a pause on the Army's lead-azide detonation."],
    ["Washington", "Trump claims on Truth Social he made the Huang deal: 'I made the deal.'"],
    ["California", "Flood watch in the Bay Area as storms threaten Thanksgiving travel."],
    ["Kathmandu", "Nepal's PM in India for economic and energy talks."],
    ["Bangkok", "Thai court upholds the verdict against an opposition lawmaker."],
    ["Ottawa", "Canada's PM brings a Trump impersonator on stage at a press gala."],
    ["Ibaraki", "City holds its first briefing on a nuclear-waste survey."]
  ],
  "datecheck": "NOT TUESDAY \\u2014 before today: Huang reinstated (Mon) \\u00b7 COP31 collapses (Sun) \\u00b7 Democrats' 258 seats (Mon) \\u00b7 Kyiv: 14 killed (Mon) \\u00b7 Delta glitch (Sun)",
  "footer": "Sources: Reuters \\u00b7 AP \\u00b7 CNN \\u00b7 Guardian \\u00b7 Bloomberg \\u00b7 Yonhap \\u00b7 Nikkei \\u00b7 SCMP \\u00b7 Japan Times \\u00b7 White House.",
  "chips": ["NORTH AMERICA 3", "EUROPE 3", "MIDDLE EAST 1", "ASIA 5", "OCEANIA 1"],
  "pins": [["1", 139.7, 35.7, 6, -14], ["2", 130.9, 37.5, -16, -14], ["3", 37.6, 55.7, 8, -14], ["4", 21.0, 52.2, -4, -16], ["5", -77.0, 38.9, -14, -16], ["6", -118.2, 34.0, -16, 8], ["7", -74.5, 36.0, 6, 8], ["8", 149.1, -35.3, 8, -6], ["9", 51.4, 35.7, 8, -6], ["10", 106.1, -6.2, 8, -6], ["11", 24.7, 59.4, 8, -14], ["12", 77.2, 28.6, 8, -6], ["13", 121.0, 14.6, 8, -6]],
  "land": [
    "-168,66 -140,70 -125,72 -110,68 -95,80 -85,70 -75,62 -60,55 -55,47 -70,42 -80,32 -90,21 -97,16 -105,20 -115,28 -125,40 -125,49 -140,60 -165,60",
    "-80,10 -60,5 -50,0 -35,-8 -40,-20 -48,-28 -58,-35 -65,-45 -70,-55 -73,-40 -72,-20 -77,-12",
    "-10,36 -2,37 5,38 12,42 18,40 23,36 28,41 30,46 20,50 12,55 8,58 5,60 -5,58 -10,50 -10,43",
    "-17,15 -10,30 0,35 10,37 20,32 30,31 35,28 43,12 51,11 48,0 40,-10 35,-18 28,-28 20,-35 15,-30 12,-18 9,-1 9,4 -8,4 -13,8 -17,12",
    "30,70 50,70 70,72 90,75 110,76 130,72 150,70 170,66 178,65 170,60 160,55 150,45 140,40 130,35 122,30 115,22 108,12 103,8 100,8 95,15 90,22 85,20 80,13 75,8 70,20 65,25 60,25 55,26 50,29 48,30 45,35 40,38 35,36 30,36 28,42 30,45 30,50 35,55 40,60 35,65",
    "113,-22 114,-30 120,-34 130,-32 140,-38 150,-37 153,-27 146,-19 142,-11 135,-12 130,-13 122,-14 114,-22"
  ]
}"""

_PAL = {
    "paper": (247, 243, 234), "ink": (18, 30, 54), "soft": (52, 68, 96),
    "red": (178, 34, 34), "teal": (14, 92, 96), "gold": (184, 134, 11),
    "line": (203, 196, 182), "card": (255, 255, 255), "panel": (24, 38, 64),
    "muted": (110, 116, 128), "sea": (232, 238, 242), "land": (148, 168, 178),
    "cream": (253, 238, 214), "green": (118, 185, 0), "amber": (232, 196, 90),
    "flame": (232, 122, 42), "pine": (12, 58, 40), "wine": (74, 20, 20),
}
_FONT_PATHS = {
    "r": "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "rb": "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "sb": "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
    "s": "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
}
_FALLBACK = "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf"


def _typeface(kind, size):
    try:
        return Typ.truetype(_FONT_PATHS[kind], size)
    except OSError:
        return Typ.truetype(_FALLBACK % ("-Bold" if kind.endswith("b") else ""), size)


_SPEC = (
    ("title", "sb", 46), ("strap", "rb", 15), ("kick", "rb", 12),
    ("head", "rb", 21), ("deck", "r", 14), ("smhead", "rb", 15),
    ("smdeck", "r", 11), ("statn", "rb", 30), ("statl", "rb", 11),
    ("brief", "r", 12), ("foot", "r", 11), ("maplbl", "rb", 11),
    ("num", "rb", 16), ("bignum", "sb", 40),
)
F = {name: _typeface(kind, size) for name, kind, size in _SPEC}


def _wrap(cv, s, fnt, w):
    """Split s into pixel-width lines for font fnt (greedy, word by word)."""
    words, lines = s.split(), []
    while words:
        line, used = "", 0
        while used < len(words):
            trial = (line + " " + words[used]).strip()
            if cv.textlength(trial, font=fnt) > w:
                break
            line, used = trial, used + 1
        lines.append(line)
        words = words[used:]
    return lines


def _show(cv, items):
    """Draw (x, y, text, font-key, colour-key, anchor) rows in one pass."""
    for x, y, s, fk, ck, a in items:
        cv.text((x, y), s, font=F[fk], fill=_PAL[ck], anchor=a)


def _art_asia(cv, ox, oy, ow, oh):
    cv.rectangle([ox, oy, ox + ow, oy + oh], fill=_PAL["pine"])
    pts = [(ox + dx, oy + dy) for dx, dy in
           ((14, 92), (70, 78), (118, 84), (170, 56), (222, 40), (268, 22))]
    cv.line(pts, fill=_PAL["green"], width=5)
    cv.polygon([(ox + 268, oy + 22), (ox + 246, oy + 24), (ox + 262, oy + 42)],
               fill=_PAL["green"])
    for bx, bh in ((18, 38), (56, 52), (94, 66)):
        cv.rectangle(
            [ox + bx, oy + 104 - bh, ox + bx + 28, oy + 104],
            fill=_PAL["panel"], outline=_PAL["green"], width=2)
    cv.text((ox + ow - 118, oy + oh - 46), "+7.5%", font=F["bignum"],
            fill=_PAL["card"])


def _art_alert(cv, ox, oy, ow, oh):
    cv.rectangle([ox, oy, ox + ow, oy + oh], fill=_PAL["wine"])
    cx, cy = ox + 78, oy + 58
    for r in (48, 34, 20):
        cv.ellipse([cx - r, cy - r, cx + r, cy + r], outline=_PAL["flame"],
                   width=2)
    cv.line([cx, cy, cx + 40, cy - 26], fill=_PAL["flame"], width=3)
    cv.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=_PAL["flame"])
    cv.polygon([(ox + 244, oy + 16), (ox + 284, oy + 88), (ox + 204, oy + 88)],
               fill=_PAL["amber"])
    cv.text((ox + 240, oy + 48), "!", font=F["bignum"], fill=_PAL["wine"])
    cv.text((ox + 12, oy + oh - 30), "07:52", font=F["num"],
            fill=_PAL["card"])


def _art_records(cv, ox, oy, ow, oh):
    cv.rectangle([ox, oy, ox + ow, oy + oh], fill=_PAL["panel"])
    for i in range(3):
        dx, dy = i * 8, i * -8
        cv.rectangle([ox + 20 + dx, oy + 26 + dy, ox + 120 + dx, oy + 92 + dy],
                     fill=_PAL["paper"], outline=_PAL["line"], width=1)
        for j in range(3):
            cv.line([ox + 30 + dx, oy + 40 + j * 14 + dy,
                     ox + 110 + dx, oy + 40 + j * 14 + dy],
                    fill=_PAL["soft"], width=2)
    cv.text((ox + ow - 178, oy + oh - 46), "470,000", font=F["bignum"],
            fill=_PAL["card"])


_ART = {"asia": _art_asia, "alert": _art_alert, "records": _art_records}


def _atlas(cv, data, x, y, w, h):
    cv.rectangle([x, y, x + w, y + h], fill=_PAL["sea"])
    cv.rectangle([x, y, x + w, y + h], outline=_PAL["line"], width=1)

    def proj(lon, lat):
        return (x + (lon + 180.0) / 360.0 * w, y + (90.0 - lat) / 180.0 * h)

    for s in data["land"]:
        pts = [proj(float(a), float(b)) for a, b in
               (p.split(",") for p in s.split())]
        cv.polygon(pts, fill=_PAL["land"])
    for lbl, lon, lat, dx, dy in data["pins"]:
        px, py = proj(lon, lat)
        cv.ellipse([px - 5, py - 5, px + 5, py + 5], fill=_PAL["red"],
                   outline=_PAL["card"], width=2)
        cv.text((px + dx, py + dy), lbl, font=F["maplbl"], fill=_PAL["red"])

def _mast(cv, data):
    cv.rectangle([0, 0, S, 92], fill=_PAL["ink"])
    _show(cv, [
        (24, 12, data["mast"][0], "title", "card", "la"),
        (24, 66, data["mast"][1], "strap", "amber", "la"),
    ])
    cv.rectangle([0, 92, S, 96], fill=_PAL["red"])


def _strip(cv, data):
    cw = S // 6
    items = []
    for i, (num, lbl) in enumerate(data["strip"]):
        cx = i * cw + cw // 2
        items.append((cx, 104, num, "statn", "red", "ma"))
        items.append((cx, 142, lbl, "statl", "soft", "ma"))
        if i:
            cv.line([i * cw, 106, i * cw, 158], fill=_PAL["line"], width=1)
    _show(cv, items)
    cv.line([0, 168, S, 168], fill=_PAL["line"], width=1)


def _leads(cv, data):
    for i, lead in enumerate(data["leads"]):
        x = 24 + i * (312 + 16)
        cv.rectangle([x, 180, x + 312, 180 + 284], fill=_PAL["card"],
                     outline=_PAL["line"], width=1)
        _ART[lead["art"]](cv, x + 1, 181, 310, 118)
        items = [(x + 12, 310,
                  lead["n"] + "  " + lead["pl"] + " — " + lead["cat"],
                  "kick", "red", "la")]
        ty = 330
        for ln in _wrap(cv, lead["h"], F["head"], 288):
            items.append((x + 12, ty, ln, "head", "ink", "la"))
            ty += 24
        ty += 4
        for ln in _wrap(cv, lead["d"], F["deck"], 288):
            items.append((x + 12, ty, ln, "deck", "soft", "la"))
            ty += 18
        items.append((x + 12, 444, lead["src"], "foot", "muted", "la"))
        _show(cv, items)


def _seconds(cv, data):
    col_w = (S - 48 - 16) // 2
    for i, (num, place, cat, head, deck, src) in enumerate(data["seconds"]):
        col, row = i % 2, i // 2
        x = 24 + col * (col_w + 16)
        y = 476 + row * 48
        first = _wrap(cv, deck, F["smdeck"], col_w - 34)[:1]
        _show(cv, [
            (x, y, num, "num", "red", "la"),
            (x + 34, y, place + " — " + cat, "kick", "soft", "la"),
            (x + 34, y + 14, head, "smhead", "ink", "la"),
            (x + 34, y + 31, first[0] if first else "", "smdeck", "muted", "la"),
        ])
        if row < 4:
            cv.line([x, y + 47, x + col_w, y + 47], fill=_PAL["line"],
                    width=1)
    cv.line([0, 720, S, 720], fill=_PAL["line"], width=1)


def _chips(cv, data):
    _show(cv, [(708, 730, "STORIES BY REGION", "kick", "red", "la")])
    cy = 752
    for chip in data["chips"]:
        tw = cv.textlength(chip, font=F["statl"]) + 18
        cv.rounded_rectangle([708, cy, 708 + tw, cy + 22], radius=11,
                             fill=_PAL["ink"])
        cv.text((717, cy + 4), chip, font=F["statl"], fill=_PAL["card"])
        cy += 24


def _shorts(cv, data):
    _show(cv, [(24, 856, "ALSO TODAY", "kick", "red", "la")])
    bcol_w = (S - 48 - 16) // 2
    items = []
    for i, (place, txt) in enumerate(data["shorts"]):
        col, row = i % 2, i // 2
        x = 24 + col * (bcol_w + 16)
        y = 874 + row * 15
        items.append((x, y, "•  ", "brief", "red", "la"))
        items.append((x + 12, y, place + ": " + txt, "brief", "soft", "la"))
    _show(cv, items)


def _tail(cv, data):
    cv.rectangle([0, 984, S, 1006], fill=_PAL["cream"])
    _show(cv, [
        (24, 988, "DATE CHECK", "kick", "red", "la"),
        (118, 988, data["datecheck"], "foot", "soft", "la"),
        (24, 1010, data["footer"], "foot", "muted", "la"),
    ])


def _render():
    data = json.loads(DATA)
    img = Pic.new("RGB", (S, S), _PAL["paper"])
    cv = Pen.Draw(img)
    _mast(cv, data)
    _strip(cv, data)
    _leads(cv, data)
    _seconds(cv, data)
    _atlas(cv, data, 24, 728, 660, 110)
    _show(cv, [(24, 842, "WHERE IT HAPPENED — pins 01–13 match the stories above",
                "kick", "soft", "la")])
    _chips(cv, data)
    _shorts(cv, data)
    _tail(cv, data)
    return img


def _run():
    _render().save(OUT, format="PNG", optimize=True)


_run()
