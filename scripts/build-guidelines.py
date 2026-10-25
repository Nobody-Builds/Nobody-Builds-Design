"""Builds the Nobody Builds brand guidelines: 17 pages at 1440 × 1000 and one PDF, modelled on the Space Works
brand guidelines v1. Run after scripts/build-assets.py (it reads logo/, mascot/ and icons/).

    python scripts/build-guidelines.py

brand/guidelines/png/01.png … 17.png
brand/nobody-builds-brand-guidelines-v1.pdf
"""
import io
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "brand" / "guidelines" / "png"
W, H, M = 1440, 1000, 64

NIGHT, BLUEPRINT, HARD_HAT = "#172033", "#2457A6", "#FDC521"
SKY, BUTTER, BRICK, PAPER = "#CFE0F7", "#FFE8A3", "#EA724A", "#F5F7FB"
GREEN, MUTED, LINE, WHITE = "#A6D98F", "#4F5A70", "#D3DAE6", "#FFFFFF"
SEVEN = [("Night Shift", NIGHT, "Text · structure · depth"), ("Blueprint", BLUEPRINT, "Primary brand · actions"),
         ("Hard Hat", HARD_HAT, "Energy · one bold moment"), ("Sky", SKY, "Fresh fields · information"),
         ("Butter", BUTTER, "Small highlights · ink text"), ("Brick", BRICK, "Warm accent · warnings"),
         ("Paper", PAPER, "Canvas · breathing room")]

_fonts = {}


def font(name, size, weight=None):
    """Pillow can't read WOFF/WOFF2, so decode the webfont to TrueType in memory (cached per file)."""
    if name not in _fonts:
        tt = TTFont(ROOT / "fonts" / name)
        tt.flavor = None
        buf = io.BytesIO()
        tt.save(buf)
        _fonts[name] = buf.getvalue()
    f = ImageFont.truetype(io.BytesIO(_fonts[name]), size)
    if weight:
        f.set_variation_by_axes([weight])
    return f


def reg(s): return font("Gilroy-Regular.woff", s)
def med(s): return font("Gilroy-Medium.woff", s)
def semi(s): return font("Gilroy-SemiBold.woff", s)
def bold(s): return font("Gilroy-Bold.woff", s)
def accent(s): return font("Unbounded-Variable.woff2", s, 600)


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def load(rel):
    return Image.open(ROOT / rel).convert("RGBA")


def fit(img, h=None, w=None):
    s = h / img.height if h else w / img.width
    return img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)


def lum(h):
    c = [x / 255 for x in rgb(h)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


builder = load("mascot/builder.png")
builder_dark = load("mascot/dark/builder.png")
symbol = load("logo/symbol.png")
stacked, stacked_rev = load("logo/lockup-stacked.png"), load("logo/lockup-stacked-reversed.png")
horizontal, horizontal_rev = load("logo/lockup-horizontal.png"), load("logo/lockup-horizontal-reversed.png")
app_icon = load("logo/app-icon.png")
og = load("icons/og-1200x630.png")


class Page:
    """One guidelines page: header, title, subtitle and footer, like the Space Works sheets."""

    def __init__(self, n, section, title, sub, bg=PAPER):
        self.n, self.bg = n, bg
        self.im = Image.new("RGBA", (W, H), rgb(bg))
        self.d = ImageDraw.Draw(self.im)
        dark = bg in (NIGHT, BLUEPRINT)
        self.ink = PAPER if dark else NIGHT
        self.soft = "#C3C8D2" if dark else MUTED
        self.label_ink = HARD_HAT if dark else BLUEPRINT
        self.text((M, 44), "nobody builds  /  brand guidelines", med(15), self.soft)
        self.text((W - M, 44), f"{n:02d}  /  {section.upper()}", med(15), self.soft, anchor="rs")
        if title:
            self.text((M, 128), title, semi(46), self.ink)
        if sub:
            self.text((M, 170), sub, reg(20), self.soft)
        self.text((M, H - 36), "Brand guidelines · 1.0", med(15), self.soft)
        self.text((W - M, H - 36), f"{n:02d}", med(15), self.soft, anchor="rs")

    def text(self, xy, s, f, fill, anchor="ls", spacing=1.18):
        x, y = xy
        for i, line in enumerate(s.split("\n")):
            self.d.text((x, y + round(i * f.size * spacing)), line, font=f, fill=rgb(fill), anchor=anchor)

    def label(self, xy, s, fill=None):
        self.text(xy, s.upper(), med(14), fill or self.label_ink)

    def card(self, box, fill, radius=20, outline=None):
        self.d.rounded_rectangle(box, radius, fill=rgb(fill), outline=rgb(outline) if outline else None, width=2)

    def put(self, img, x, y):
        self.im.alpha_composite(img, (round(x), round(y)))

    def centre(self, img, box):
        x0, y0, x1, y1 = box
        self.put(img, x0 + (x1 - x0 - img.width) / 2, y0 + (y1 - y0 - img.height) / 2)

    def save(self):
        OUT.mkdir(parents=True, exist_ok=True)
        rgb_im = self.im.convert("RGB")
        rgb_im.save(OUT / f"{self.n:02d}.png", optimize=True)
        return rgb_im


def rounded(img, r):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.width - 1, img.height - 1], r, fill=255)
    out = img.copy()
    out.putalpha(ImageChops.multiply(out.getchannel("A"), mask))
    return out


pages = []

# 01 · Cover
p = Page(1, "Identity system", None, None, NIGHT)
p.put(fit(horizontal_rev, h=96), M - 20, 104)
p.text((M, 470), "Nobody builds.\nExcept us.", bold(84), PAPER, spacing=1.1)
p.text((M, 860), "Brand guidelines\nVersion 1.0", med(18), "#C3C8D2")
p.centre(fit(app_icon, h=440), (820, 220, 1376, 780))
pages.append(p.save())

# 02 · Brand
p = Page(2, "Brand", "Nobody builds. Except us.", "A builder, asleep on the job, on a wall that's already half built.", SKY)
p.text((M, 360), "Lay a brick.\nTake a nap.\nBuild anyway.", semi(74), NIGHT, spacing=1.12)
p.label((900, 360), "Our purpose")
p.text((900, 396), "To fill in: what Nobody Builds\nmakes, and who it's for.", reg(22), NIGHT)
p.label((900, 560), "Our personality")
p.text((900, 596), "Honest. Hands-on.\nFriendly. Unbothered.", reg(22), NIGHT)
pages.append(p.save())

# 03 · Brand
p = Page(3, "Brand", "Asleep on the job.", "The symbol is the builder: hard hat on, head down, zzz up.")
p.centre(fit(builder, h=560), (M, 240, 760, 900))
for i, (head, body) in enumerate([("Honest", "We laugh at ourselves first."), ("Hands-on", "Real bricks, real work."),
                                  ("Friendly", "Round shapes, warm colours.")]):
    y = 380 + i * 150
    p.text((900, y), head, semi(26), NIGHT)
    p.text((900, y + 36), body, reg(19), MUTED)
pages.append(p.save())

# 04 · Logo
p = Page(4, "Logo", "One builder. A flexible family.", "Use the supplied masters. Keep the spelling and the lowercase wordmark intact.")
tiles = [((M, 230, 708, 530), WHITE, stacked, "Primary · builder + two-line wordmark", MUTED),
         ((732, 230, 1376, 530), SKY, symbol, "Symbol · recognition at a glance", NIGHT),
         ((M, 554, 708, 854), BUTTER, horizontal, "Horizontal · narrow headers", NIGHT),
         ((732, 554, 1376, 854), NIGHT, stacked_rev, "Reversed · dark surfaces", "#C3C8D2")]
for box, fill, art, cap, capc in tiles:
    p.card(box, fill, outline=LINE if fill == WHITE else None)
    p.centre(fit(art, h=190 if art is not horizontal else 120), (box[0], box[1], box[2], box[3] - 40))
    p.text((box[0] + 24, box[3] - 22), cap.upper(), med(13), capc)
pages.append(p.save())

# 05 · Logo
p = Page(5, "Logo", "Room to breathe.", "Keep the lockup together. Measure the visible artwork.")
art = fit(stacked, h=280)
x, y = 140, 390
pad = 280 // 4
for x0, y0, x1, y1 in [(x - pad, y - pad, x + art.width + pad, y + art.height + pad)]:
    for i in range(x0, x1, 18):
        p.d.line([i, y0, min(i + 9, x1), y0], fill=rgb(BLUEPRINT), width=2)
        p.d.line([i, y1, min(i + 9, x1), y1], fill=rgb(BLUEPRINT), width=2)
    for j in range(y0, y1, 18):
        p.d.line([x0, j, x0, min(j + 9, y1)], fill=rgb(BLUEPRINT), width=2)
        p.d.line([x1, j, x1, min(j + 9, y1)], fill=rgb(BLUEPRINT), width=2)
p.put(art, x, y)
p.text((x - pad, y + art.height + pad + 44), "H = builder height. Scale the supplied master as one object.", reg(17), MUTED)
for i, (big, small) in enumerate([("1.25×", "Builder / stacked wordmark height"), ("H ÷ 6", "Gap between builder and wordmark"),
                                  ("H ÷ 4", "Clear space on every side")]):
    yy = 330 + i * 170
    p.text((1040, yy), big, semi(52), NIGHT)
    p.text((1040, yy + 40), small, reg(18), MUTED)
pages.append(p.save())

# 06 · Logo
p = Page(6, "Logo", "Keep it legible.", "Recommended starting sizes. Always check the final output.")
p.put(fit(symbol, h=48), M, 330)
p.text((M, 440), "48 px", semi(30), NIGHT)
p.text((M, 470), "Builder height", reg(17), MUTED)
p.put(fit(horizontal, w=180), 330, 350)
p.text((330, 440), "180 px", semi(30), NIGHT)
p.text((330, 470), "Primary lockup width", reg(17), MUTED)
p.label((M, 600), "In print")
p.text((M, 640), "12 mm builder  /  40 mm lockup", semi(26), NIGHT)
p.text((M, 674), "Proof at actual size before production.", reg(17), MUTED)
p.text((M, 760), "Largest: 280 px builder height on screen, the artwork's native size.", reg(17), MUTED)
p.card((900, 250, 1300, 650), WHITE, 28, LINE)
p.centre(fit(app_icon, h=320), (900, 250, 1300, 650))
p.text((900, 700), "App icon", semi(26), NIGHT)
p.text((900, 734), "Builder ≈ 62% of the tile height.\nUse a Paper field.", reg(17), MUTED)
p.text((900, 830), "Below 48 px, use the tuned favicons in icons/.", reg(15), MUTED)
pages.append(p.save())

# 07 · Logo
p = Page(7, "Logo", "Choose the right background.", "Keep the builder, its outline and the wordmark's proportions intact.")
tiles = [((M, 230, 708, 530), PAPER, stacked, "01  Full colour / Paper", MUTED, LINE),
         ((732, 230, 1376, 530), WHITE, stacked, "02  Full colour / White", MUTED, LINE),
         ((M, 554, 708, 854), NIGHT, stacked_rev, "03  Reversed / Night Shift", "#C3C8D2", None),
         ((732, 554, 1376, 854), BLUEPRINT, stacked_rev, "04  Reversed / Blueprint", "#E3ECF8", None)]
for box, fill, art, cap, capc, outline in tiles:
    p.card(box, fill, outline=outline)
    p.centre(fit(art, h=190), (box[0], box[1], box[2], box[3] - 40))
    p.text((box[0] + 24, box[3] - 22), cap, med(15), capc)
pages.append(p.save())

# 08 · Logo
p = Page(8, "Logo", "Keep the system intact.", "The builder is a fixed piece of artwork. Treat it as one recognizable unit.")
sym = fit(symbol, h=190)
r, g, b, a = sym.split()
blur = Image.new("RGBA", (sym.width + 60, sym.height + 60))
blur.paste(Image.new("RGBA", sym.size, rgb(NIGHT) + (110,)), (36, 40), a)
blur = blur.filter(ImageFilter.GaussianBlur(12))
blur.alpha_composite(sym, (30, 30))
type_change = Image.new("RGBA", (420, 230))
type_change.alpha_composite(fit(symbol, h=150), (135, 0))
ImageDraw.Draw(type_change).text((210, 205), "NOBODY BUILDS", font=accent(30), fill=rgb(NIGHT), anchor="ms")
misuse = [(sym.resize((round(sym.width * 1.6), sym.height)), WHITE, "01  Don't stretch"),
          (sym.rotate(24, expand=True, resample=Image.BICUBIC), WHITE, "02  Don't rotate"),
          (Image.merge("RGBA", (b, r, g, a)), WHITE, "03  Don't recolour"),
          (sym, NIGHT, "04  Don't lose the outline on dark"),
          (blur, WHITE, "05  Don't add effects"),
          (type_change, WHITE, "06  Don't change the type")]
for i, (art, fill, cap) in enumerate(misuse):
    x0 = M + (i % 3) * 440
    y0 = 230 + (i // 3) * 324
    box = (x0, y0, x0 + 416, y0 + 300)
    p.card(box, fill, outline=LINE if fill == WHITE else None)
    art = fit(art, h=min(art.height, 200)) if art.width <= 380 else fit(art, w=380)
    p.centre(art, (box[0], box[1], box[2], box[3] - 44))
    p.text((box[0] + 22, box[3] - 22), cap, med(15), "#C3C8D2" if fill == NIGHT else MUTED)
pages.append(p.save())

# 09 · Colour
p = Page(9, "Colour", "Seven colours. One clear system.", "Exact sRGB values. Three core colours, three accents and a daylight canvas.")
def swatch(box, name, hex_, role):
    p.card(box, hex_, 18, outline=LINE if hex_ in (PAPER,) else None)
    ink = PAPER if hex_ in (NIGHT, BLUEPRINT) else NIGHT
    x, y = box[0] + 26, box[1] + 46
    p.text((x, y), name, semi(24), ink)
    p.text((x, y + 44), hex_, med(22), ink)
    p.text((x, y + 76), "RGB " + ", ".join(str(v) for v in rgb(hex_)), reg(16), ink)
    p.text((x, box[3] - 24), role, reg(16), ink)
for i, c in enumerate(SEVEN[:3]):
    x0 = M + i * 444
    swatch((x0, 230, x0 + 424, 530), *c)
for i, c in enumerate(SEVEN[3:]):
    x0 = M + i * 333
    swatch((x0, 554, x0 + 313, 854), *c)
pages.append(p.save())

# 10 · Colour
p = Page(10, "Colour", "Readable by design.", "Use tested text pairings. Add a word or an icon to every status.")
pairs = [("Paper on Blueprint", PAPER, BLUEPRINT), ("Night Shift on Paper", NIGHT, PAPER),
         ("Night Shift on Hard Hat", NIGHT, HARD_HAT), ("Night Shift on Sky", NIGHT, SKY)]
for i, (cap, fg, bg) in enumerate(pairs):
    x0 = M + (i % 2) * 668
    y0 = 230 + (i // 2) * 270
    box = (x0, y0, x0 + 644, y0 + 246)
    p.card(box, bg, 18, outline=LINE if bg == PAPER else None)
    p.text((x0 + 30, y0 + 110), "Aa", semi(84), fg)
    p.text((box[2] - 30, y0 + 70), f"{ratio(fg, bg):.2f}:1", med(30), fg, anchor="rs")
    p.text((x0 + 30, box[3] - 28), cap, med(18), fg)
p.text((M, 820), f"Normal text ≥ 4.5:1 · Large text ≥ 3:1 · Night Shift on Butter {ratio(NIGHT, BUTTER):.2f}:1 · "
                 f"Night Shift on Brick {ratio(NIGHT, BRICK):.2f}:1", reg(18), NIGHT)
p.text((M, 856), f"Avoid yellow or Brick text on Paper ({ratio(HARD_HAT, PAPER):.2f}:1 and {ratio(BRICK, PAPER):.2f}:1). "
                 "Large = 24 px regular or 18.7 px bold.", reg(18), MUTED)
pages.append(p.save())

# 11 · Typography
p = Page(11, "Typography", "Two fonts. Clear roles.", "Gilroy leads. Unbounded brings the bold geometric accent.", SKY)
p.label((M, 280), "Primary")
p.text((M, 360), "Gilroy", semi(64), NIGHT)
p.text((M, 500), "Ready to\nbuild.", semi(86), NIGHT, spacing=1.05)
p.text((M, 760), "Wordmark, headings, body and labels.", reg(19), NIGHT)
p.text((M, 792), "Regular · Medium · Semibold · Bold", reg(17), MUTED)
p.d.line([720, 260, 720, 860], fill=rgb("#A9C3E8"), width=2)
p.label((780, 280), "Secondary / accent")
p.text((780, 360), "Unbounded", accent(46), NIGHT)
p.text((780, 500), "Wake\nup.", accent(86), BLUEPRINT, spacing=1.12)
p.text((780, 760), "Short headlines and campaign accents.", reg(19), NIGHT)
p.text((780, 792), "Medium · Semibold · one accent per layout", reg(17), MUTED)
pages.append(p.save())

# 12 · Typography
p = Page(12, "Typography", "A lean type scale.", "Gilroy does the everyday work. Unbounded adds a single moment of emphasis.")
rows = [("Display", "72 / 76", "Ready to build.", semi(52)), ("Heading", "48 / 52", "Lay the first brick.", semi(38)),
        ("Subheading", "32 / 38", "Pick up where you left off.", semi(28)),
        ("Body", "16 / 24", "Plans, parts and progress, all in one place.", reg(19)),
        ("Label", "14 / 20", "Start building", semi(17)), ("Accent", "48 / 56", "Wake up.", accent(38))]
for i, (role, size, sample, f) in enumerate(rows):
    y = 300 + i * 98
    p.d.line([M, y + 30, W - M, y + 30], fill=rgb(LINE), width=1)
    p.text((M, y), role, med(17), MUTED)
    p.text((300, y), size, med(17), MUTED)
    p.text((520, y), sample, f, NIGHT)
p.text((M, 920), "Keep long copy and interface text in Gilroy. Use Unbounded for short phrases only.", reg(17), MUTED)
pages.append(p.save())

# 13 · Graphic system
p = Page(13, "Graphic system", "Built from bricks.", "Use brick shapes and the zzz as quiet accents. Keep the builder itself intact.")
p.card((M, 230, 860, 760), BLUEPRINT, 22)
p.text((M + 48, 360), "Wake\nup.", accent(92), PAPER, spacing=1.12)
for (x0, y0, w) in [(560, 600, 200), (480, 668, 200), (690, 668, 140)]:
    p.d.rounded_rectangle([x0, y0, x0 + w, y0 + 56], 10, fill=rgb(HARD_HAT))
for i, rule in enumerate(["Use one bold moment.", "Align to a simple grid.", "Let empty space do its job."]):
    y = 330 + i * 110
    p.text((940, y), f"{i + 1:02d}", med(17), BLUEPRINT)
    p.text((1000, y), rule, reg(22), NIGHT)
p.label((M, 830), "Colour balance / neutral first, accent second")
x = M
for hex_, share in [(PAPER, 40), (BLUEPRINT, 18), (NIGHT, 14), (SKY, 14), (HARD_HAT, 6), (BUTTER, 4), (BRICK, 4)]:
    w = round((W - 2 * M) * share / 100)
    p.d.rectangle([x, 856, x + w, 884], fill=rgb(hex_), outline=rgb(LINE) if hex_ == PAPER else None)
    x += w
pages.append(p.save())

# 14 · Graphic system
p = Page(14, "Graphic system", "Useful details.", "Simple icons. Real builds. Details people recognize.")


def icon(kind):
    s = 4
    im = Image.new("RGBA", (64 * s, 64 * s))
    d = ImageDraw.Draw(im)
    ink, wdt = rgb(NIGHT), 5 * s

    def line(*pts):
        pts = [(x * s, y * s) for x, y in pts]
        d.line(pts, fill=ink, width=wdt, joint="curve")
        for x, y in (pts[0], pts[-1]):
            d.ellipse([x - wdt / 2, y - wdt / 2, x + wdt / 2, y + wdt / 2], fill=ink)
    if kind == "search":
        d.ellipse([12 * s, 10 * s, 46 * s, 44 * s], outline=ink, width=wdt)
        line((42, 40), (54, 52))
    elif kind == "bricks":
        d.rounded_rectangle([8 * s, 16 * s, 56 * s, 48 * s], 6 * s, outline=ink, width=wdt)
        line((8, 32), (56, 32))
        line((32, 16), (32, 32))
        line((20, 32), (20, 48))
        line((44, 32), (44, 48))
    elif kind == "build":
        d.arc([12 * s, 12 * s, 52 * s, 52 * s], 180, 360, fill=ink, width=wdt)
        line((6, 38), (58, 38))
        line((32, 12), (32, 24))
    elif kind == "sleep":
        line((16, 16), (46, 16), (16, 48), (46, 48))
    return im.resize((64, 64), Image.LANCZOS)


p.label((M, 280), "Icons")
for i, (kind, name) in enumerate([("search", "Search"), ("bricks", "Bricks"), ("build", "Build"), ("sleep", "Sleep")]):
    x = M + i * 140
    p.put(icon(kind), x, 320)
    p.text((x, 420), name, reg(17), MUTED)
p.text((M, 560), "24 px grid · 2 px stroke", semi(22), NIGHT)
p.text((M, 598), "Rounded ends · consistent weight", reg(19), MUTED)
p.text((M, 650), "Always pair unfamiliar icons with labels.", reg(19), MUTED)
p.label((820, 280), "Imagery")
p.text((820, 370), "Show real\nbuilds.", semi(56), NIGHT, spacing=1.08)
p.text((820, 540), "Hands, tools and half-finished projects.\nSoft daylight. Honest mess.\nKeep the work in focus.", reg(20), NIGHT)
p.text((820, 700), "Avoid staged stock photos and perfect desks.", reg(17), MUTED)
pages.append(p.save())

# 15 · Voice
p = Page(15, "Voice", "Sound like a builder who's in on the joke.", "Clear, warm and specific. Make the next step easy.", SKY)
p.label((M, 280), "Say")
p.label((820, 280), "Skip")
for i, (say, skip) in enumerate([("Nothing built yet. Lay the first brick.", "No records found in the database."),
                                 ("Saved. Back to work.", "Your changes have been successfully persisted!"),
                                 ("Couldn't save. Try again.", "Oops! Somebody fell asleep on the job.")]):
    y = 380 + i * 140
    p.d.line([M, y - 60, W - M, y - 60], fill=rgb("#A9C3E8"), width=1)
    p.text((M, y), say, semi(28), NIGHT)
    p.text((820, y), skip, reg(21), MUTED)
p.text((M, 860), "Brand name in copy: Nobody Builds. Wordmark: nobody builds. Joke when it's going well, never in an error.",
       reg(17), NIGHT)
pages.append(p.save())

# 16 · Applications
p = Page(16, "Applications", "Calm where it counts.", "In the product, let the work take the lead.", NIGHT)
win = (M, 230, W - M, 880)
p.card(win, WHITE, 20)
p.d.rounded_rectangle([win[0], win[1], win[0] + 250, win[3]], 20, fill=rgb("#ECF0F7"))
p.d.rectangle([win[0] + 230, win[1], win[0] + 250, win[3]], fill=rgb("#ECF0F7"))
p.put(fit(horizontal, h=52), win[0] + 16, win[1] + 24)
for i, item in enumerate(["Projects", "Builds", "Activity"]):
    y = win[1] + 130 + i * 52
    if i == 0:
        p.d.rounded_rectangle([win[0] + 18, y - 28, win[0] + 228, y + 12], 20, fill=rgb(BLUEPRINT))
    p.text((win[0] + 36, y), item, med(18), PAPER if i == 0 else NIGHT)
mx = win[0] + 290
p.text((mx, win[1] + 70), "Projects", semi(32), NIGHT)
p.d.rounded_rectangle([win[2] - 230, win[1] + 36, win[2] - 36, win[1] + 82], 10, fill=rgb(BLUEPRINT))
p.text((win[2] - 133, win[1] + 66), "+ New project", semi(18), PAPER, anchor="ms")
p.d.rounded_rectangle([mx, win[1] + 110, win[2] - 36, win[1] + 156], 10, outline=rgb(LINE), width=2)
p.text((mx + 20, win[1] + 140), "Search projects, builds or people", reg(17), MUTED)
cols = [mx, mx + 360, mx + 540, mx + 760]
for c, h in zip(cols, ["Name", "ID", "Owner", "Status"]):
    p.text((c, win[1] + 210), h, med(15), MUTED)
for i, (name, pid, owner, status, fill) in enumerate([("Garden shed", "NB-001", "Asha", "On track", GREEN),
                                                      ("Arcade cabinet", "NB-002", "Ravi", "Napping", HARD_HAT),
                                                      ("Bike rack", "NB-003", "Meera", "Blocked", BRICK)]):
    y = win[1] + 280 + i * 76
    p.d.line([mx, y - 44, win[2] - 36, y - 44], fill=rgb(LINE), width=1)
    p.text((cols[0], y), name, med(20), NIGHT)
    p.text((cols[1], y), pid, reg(18), MUTED)
    p.text((cols[2], y), owner, reg(18), NIGHT)
    w = med(15).getlength(status) + 32
    p.d.rounded_rectangle([cols[3], y - 24, cols[3] + w, y + 8], 16, fill=rgb(fill))
    p.text((cols[3] + 16, y - 2), status, med(15), NIGHT)
p.text((M, 930), "Clear hierarchy. Quiet surfaces. Colour only where it helps.", reg(17), "#C3C8D2")
pages.append(p.save())

# 17 · Applications
p = Page(17, "Applications", "From the repo to the laptop lid.", "Carry the same identity from the screen to the sticker.")
card = rounded(fit(og, w=780), 22)
p.put(card, M, 250)
p.text((M, 250 + card.height + 40), "Social card · 1200 × 630", semi(20), NIGHT)
p.text((M, 250 + card.height + 70), "The repo preview, link shares and the site's og:image.", reg(17), MUTED)
lid = (920, 250, 1376, 660)
p.card(lid, NIGHT, 28)
p.centre(fit(builder_dark, h=250), lid)
p.text((920, 710), "Laptop sticker", semi(20), NIGHT)
p.text((920, 740), "Die-cut, with the Paper sticker border.\nUse the dark/ file on dark surfaces.", reg(17), MUTED)
pages.append(p.save())

pdf = ROOT / "brand" / "nobody-builds-brand-guidelines-v1.pdf"
pages[0].save(pdf, save_all=True, append_images=pages[1:], resolution=144)
print(f"build-guidelines: {len(pages)} pages in brand/guidelines/png/ and {pdf.name}")
