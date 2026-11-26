#!/usr/bin/env python3
"""Generate three 1024x1024 variants summarising world news of
Thursday 26 November 2026. Deterministic: no network, no clock,
no randomness. Run: python3 gen.py [vA|vB|vC|all] [outdir]"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
DATE = "Thursday 26 November 2026"

DJ_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
DJ_SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
DJ_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DJ_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, color, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# ---------------------------------------------------------------- stories
LEAD_HEAD = "US ANNOUNCES SWEEPING NEW TARIFFS"
LEAD_SUM = ("Washington unveils new tariffs on a host of trading partners, "
            "including China, the EU, Japan and India, in a Section 301 "
            "overcapacity probe. Rates reach up to 15% on Taiwan and 25% "
            "on Indian goods, and are due to take effect in January.")

STORIES = [
    ("TARIFFS SHAKE WORLD TRADE",
     "US unveils new levies on China, the EU, Japan and India."),
    ("HOUTHIS CLAIM SAUDI REFINERY HIT",
     "Houthis say they struck Ras Tanura; Brent crude tops $94."),
    ("WALL STREET TUMBLES ON AI FEARS",
     "Nasdaq -3.1%, S&P 500 -2.2% on AI fears; US markets shut for Thanksgiving."),
    ("CAIRO TANKER FIRE KILLS AT LEAST 30",
     "A fuel tanker crash on a Cairo highway ignites a huge fire; at least 30 dead."),
    ("COLOMBIA POLICE FREE 76 HOSTAGES",
     "Police storm a supermarket and free 76 people held hostage for 17 hours."),
    ("JUDGES URGE DROPPING NETANYAHU CHARGES",
     "Israeli judges urge dropping the most serious charges."),
    ("PAKISTAN'S FIRST ASTRONAUT IN ORBIT",
     "Shenzhou-24 carries Muhammad Zeeshan Ali to the Tiangong station."),
    ("COLOMBIA MARKS 10 YEARS OF PEACE ACCORD",
     "UN chief praises progress, warns of unfinished commitments."),
    ("VENEZUELA REVEALS $237.5BN DEBT",
     "Caracas discloses a debt load far above earlier estimates."),
    ("FIRST CLOSE-UPS OF ASTEROID CRATER",
     "ESA's Hera releases close-up images of Dimorphos, hit by NASA's DART."),
    ("CHESS TITLE: GAME 3 IN GENEVA",
     "Gukesh and Sindarov, both 20, play Game 3 level after two draws."),
    ("DURAN DURAN GUITARIST ANDY TAYLOR DIES, 65",
     "Andy Taylor, guitarist of the new-wave icons, dies aged 65."),
    ("MACY'S POSTPONES 100TH THANKSGIVING PARADE",
     "New York's parade is delayed by weather, the first such postponement in over half a century."),
    ("ROCKET LAB ELECTRON FLIGHT 101",
     "Electron is set to launch a Synspective radar satellite from New Zealand on Thursday."),
]


# ---------------------------------------------------------------- variant A
def variant_a(path):
    img = Image.new("RGB", (W, H), (250, 248, 240))
    d = ImageDraw.Draw(img)
    ink = (18, 18, 18)
    red = (178, 34, 34)
    grey = (90, 88, 82)

    # masthead
    d.text((512, 18), "THE WORLD", font=font(DJ_SERIF, 96), fill=ink,
           anchor="ma")
    rule(d, 40, 138, 984, ink, 4)
    d.text((40, 150), DATE, font=font(DJ_SANS_B, 30), fill=red)
    d.text((984, 150), "No. 330  |  $100 PRIZE EDITION",
           font=font(DJ_SANS_B, 22), fill=grey, anchor="ra")
    rule(d, 40, 196, 984, ink, 2)

    # lead story
    y = 214
    d.text((40, y), "LEAD STORY", font=font(DJ_SANS_B, 22), fill=red)
    y += 34
    lead_lines = wrap(d, LEAD_HEAD, font(DJ_SERIF, 46), 944)
    for ln in lead_lines:
        d.text((40, y), ln, font=font(DJ_SERIF, 46), fill=ink)
        y += 58
    y = draw_lines(d, 40, y, wrap(d, LEAD_SUM, font(DJ_SANS, 26), 944),
                   font(DJ_SANS, 26), ink, 34)
    rule(d, 40, y + 14, 984, ink, 2)

    # story grid: 3 columns x 4 rows (12 stories)
    top = y + 30
    col_w = 300
    gap = 22
    row_h = 104
    head_f = font(DJ_SANS_B, 20)
    body_f = font(DJ_SANS, 16)
    for i, (head, summ) in enumerate(STORIES[:12]):
        col = i % 3
        row = i // 3
        x = 40 + col * (col_w + gap)
        yy = top + row * row_h
        head_lines = wrap(d, head, head_f, col_w)
        draw_lines(d, x, yy, head_lines[:3], head_f, ink, 24)
        body_y = yy + 24 * len(head_lines[:3]) + 4
        lines = wrap(d, summ, body_f, col_w)
        draw_lines(d, x, body_y, lines[:2], body_f, grey, 19)
        if col < 2:
            d.line([(x + col_w + 10, yy), (x + col_w + 10, yy + row_h - 18)],
                   fill=(200, 196, 186), width=1)
    # footer: the two stories not in the grid
    fy = top + 4 * row_h + 12
    footer = ("ALSO:  Macy's postpones 100th Thanksgiving parade  |  "
              "Rocket Lab Electron flight 101 lifts off from New Zealand")
    draw_lines(d, 40, fy, wrap(d, footer, font(DJ_SANS_B, 19), 944),
               font(DJ_SANS_B, 19), red, 24)
    img.save(path)
    return path


# ---------------------------------------------------------------- variant B
def variant_b(path):
    navy = (13, 27, 62)
    img = Image.new("RGB", (W, H), navy)
    d = ImageDraw.Draw(img)
    white = (245, 245, 240)
    gold = (255, 193, 60)
    sky = (120, 180, 255)
    red = (255, 99, 71)
    teal = (64, 224, 180)
    purple = (196, 141, 255)
    orange = (255, 150, 60)

    # date banner
    d.rectangle([0, 0, W, 190], fill=(9, 18, 44))
    d.text((512, 22), "THE WORLD IN ONE DAY", font=font(DJ_SANS_B, 44),
           fill=gold, anchor="ma")
    d.text((512, 84), DATE, font=font(DJ_SERIF, 56), fill=white, anchor="ma")
    d.text((512, 152), "14 STORIES  |  ONE IMAGE", font=font(DJ_SANS_B, 24),
           fill=sky, anchor="ma")

    panels = [
        ("TRADE", "US announces sweeping tariffs", "Levies on China, the EU,\nJapan and India; up to 25%\non Indian goods.", gold),
        ("OIL", "Houthis claim Saudi refinery attack", "Ras Tanura, the kingdom's\nlargest refinery, hit;\nBrent crude tops $94.", red),
        ("MARKETS", "Wall Street tumbles on AI fears", "Nasdaq -3.1%, S&P 500\n-2.2%; US markets shut\nfor Thanksgiving.", sky),
        ("SPACE", "First Pakistani astronaut in orbit", "Shenzhou-24 carries\nMuhammad Zeeshan Ali to\nChina's space station.", teal),
        ("TRAGEDY", "Cairo tanker fire kills at least 30", "Fuel tanker crash on a\nCairo highway ignites a\nmassive blaze.", orange),
        ("PEACE", "Colombia marks 10 years of peace accord", "UN chief praises progress\nand warns of unfinished\ncommitments.", purple),
    ]
    pw, ph = 300, 252
    gx, gy = 40, 216
    gapx, gapy = 22, 22
    for i, (tag, head, body, col) in enumerate(panels):
        col_i = i % 3
        row = i // 3
        x = gx + col_i * (pw + gapx)
        y = gy + row * (ph + gapy)
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=18,
                            fill=(24, 42, 84), outline=col, width=4)
        d.rectangle([x + 18, y + 18, x + 66, y + 66], fill=col)
        d.text((x + 42, y + 42), tag[0], font=font(DJ_SANS_B, 30),
               fill=navy, anchor="mm")
        d.text((x + 82, y + 20), tag, font=font(DJ_SANS_B, 22), fill=col)
        yy = y + 78
        head_lines = wrap(d, head, font(DJ_SANS_B, 26), pw - 36)
        for ln in head_lines[:3]:
            d.text((x + 18, yy), ln, font=font(DJ_SANS_B, 26), fill=white)
            yy += 32
        yy += 4
        for ln in body.split("\n"):
            d.text((x + 18, yy), ln, font=font(DJ_SANS, 19),
                   fill=(205, 212, 228))
            yy += 24

    # bottom strip: remaining headlines
    y = gy + 2 * (ph + gapy) + 8
    d.text((40, y), "ALSO TODAY", font=font(DJ_SANS_B, 22), fill=gold)
    y += 34
    extra = [
        "Colombia police free 76 hostages after 17 hours",
        "Judges urge dropping gravest Netanyahu charges",
        "Venezuela reveals $237.5bn public debt",
        "First close-ups of asteroid crater Dimorphos",
        "Chess title: Game 3 in Geneva  |  Andy Taylor dies, 65",
        "Macy's postpones 100th Thanksgiving parade",
    ]
    for e in extra:
        d.text((56, y), "\u2022  " + e, font=font(DJ_SANS, 20), fill=white)
        y += 28
    img.save(path)
    return path


# ---------------------------------------------------------------- variant C
def variant_c(path):
    img = Image.new("RGB", (W, H), (16, 24, 40))
    d = ImageDraw.Draw(img)
    white = (245, 245, 240)
    gold = (255, 193, 60)
    sky = (120, 180, 255)
    red = (255, 99, 71)

    # illustrated globe scene: big globe with continents + tariff arrows
    cx, cy, r = 512, 330, 210
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(28, 90, 160),
              outline=(140, 200, 255), width=5)
    # stylised continents (deterministic blobs)
    d.ellipse([cx - 150, cy - 120, cx - 30, cy - 10], fill=(74, 160, 90))
    d.ellipse([cx - 90, cy - 40, cx + 10, cy + 60], fill=(74, 160, 90))
    d.ellipse([cx + 40, cy - 90, cx + 150, cy + 10], fill=(96, 190, 110))
    d.ellipse([cx + 20, cy + 60, cx + 120, cy + 140], fill=(74, 160, 90))
    d.ellipse([cx - 170, cy + 40, cx - 90, cy + 120], fill=(96, 190, 110))
    # tariff arrows pointing at the globe
    for (ax, ay, bx, by) in [(140, 130, 330, 220), (884, 130, 694, 220),
                             (120, 480, 320, 400), (904, 480, 704, 400)]:
        d.line([(ax, ay), (bx, by)], fill=red, width=7)
        d.polygon([(bx, by), (bx - 22, by - 4), (bx - 6, by + 20)],
                  fill=red)
    # orbiting satellite + stars
    d.ellipse([cx + 235, cy - 235, cx + 285, cy - 185], fill=gold)
    d.rectangle([cx + 245, cy - 225, cx + 275, cy - 195], fill=white)
    for (sx, sy) in [(90, 90), (930, 80), (60, 300), (960, 300),
                     (200, 560), (830, 560), (512, 60)]:
        d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=white)

    # headline banner
    d.rectangle([0, 560, W, 700], fill=(9, 18, 44))
    d.text((512, 574), "TARIFFS SHAKE THE WORLD", font=font(DJ_SANS_B, 52),
           fill=gold, anchor="ma")
    d.text((512, 640), DATE, font=font(DJ_SERIF, 34), fill=white,
           anchor="ma")

    # lead summary (short version so the ticker strip fits)
    vc_sum = ("Washington unveils new tariffs on China, the EU, Japan and "
              "India, up to 25% on Indian goods, due to take effect in "
              "January.")
    y = 716
    y = draw_lines(d, 40, y, wrap(d, vc_sum, font(DJ_SANS, 24), 944),
                   font(DJ_SANS, 24), white, 32)

    # ticker strip
    y = 806
    rule(d, 40, y, 984, gold, 3)
    y += 12
    tickers = [
        "Houthis claim Saudi refinery hit; Brent tops $94",
        "Wall Street tumbles on AI fears; Nasdaq -3.1%",
        "Cairo tanker fire kills at least 30",
        "Colombia police free 76 hostages",
        "Pakistan's first astronaut reaches Tiangong",
        "Chess title: Game 3 in Geneva",
        "Macy's postpones 100th Thanksgiving parade",
        "Andy Taylor of Duran Duran dies, 65",
    ]
    for t in tickers:
        d.text((56, y), "\u25b6  " + t, font=font(DJ_SANS, 21), fill=white)
        y += 25
    img.save(path)
    return path


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    outdir = sys.argv[2] if len(sys.argv) > 2 else "."
    os.makedirs(outdir, exist_ok=True)
    jobs = {"vA": variant_a, "vB": variant_b, "vC": variant_c}
    if which == "all":
        for name, fn in jobs.items():
            d2 = os.path.join(outdir, name)
            os.makedirs(d2, exist_ok=True)
            fn(os.path.join(d2, "entry.png"))
            print("wrote", os.path.join(d2, "entry.png"))
    else:
        fn = jobs[which]
        fn(os.path.join(outdir, "entry.png"))
        print("wrote", os.path.join(outdir, "entry.png"))


if __name__ == "__main__":
    main()
