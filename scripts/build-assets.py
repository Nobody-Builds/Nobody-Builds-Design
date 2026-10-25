"""Builds every Nobody Builds logo, icon and mascot file from the two sources in brand/source/.

    python scripts/build-assets.py        (from the repository root; needs scripts/requirements.txt)

brand/source/avatar-460.png     the untouched GitHub avatar, the only copy of the artwork
brand/source/builder-cutout.png the builder cut out of its cream background (scripts/cutout.py)

The artwork is never redrawn: every file below is the same pixels, scaled, framed or bordered.
"""
import base64
import io
import shutil
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "brand" / "source"

NIGHT_SHIFT, BLUEPRINT, HARD_HAT = "#172033", "#2457A6", "#FDC521"
SKY, BUTTER, BRICK, PAPER = "#CFE0F7", "#FFE8A3", "#EA724A", "#F5F7FB"
SEVEN = [NIGHT_SHIFT, BLUEPRINT, HARD_HAT, SKY, BUTTER, BRICK, PAPER]

art = Image.open(SRC / "builder-cutout.png").convert("RGBA")


def font(name, size):
    """Pillow can't read WOFF/WOFF2, so decode the webfont to plain TrueType in memory."""
    tt = TTFont(ROOT / "fonts" / name)
    tt.flavor = None
    buf = io.BytesIO()
    tt.save(buf)
    buf.seek(0)
    return ImageFont.truetype(buf, size)


def rgb(hex_):
    return tuple(int(hex_[i:i + 2], 16) for i in (1, 3, 5))


def fit(img, h):
    return img.resize((round(img.width * h / img.height), h), Image.LANCZOS)


def pad(img, p):
    out = Image.new("RGBA", (img.width + 2 * p, img.height + 2 * p))
    out.alpha_composite(img, (p, p))
    return out


def sticker(img, r=7):
    """The approved dark-surface treatment: a thin Paper die-cut border, art untouched."""
    base = pad(img, r + 2)
    a = base.getchannel("A").point(lambda v: 255 if v > 40 else 0)
    a = a.filter(ImageFilter.MaxFilter(2 * r + 1)).filter(ImageFilter.GaussianBlur(0.8))
    out = Image.new("RGBA", base.size, rgb(PAPER) + (0,))
    out.putalpha(a)
    out.alpha_composite(base)
    return out


def text(lines, size, colour, leading=0.92):
    """Lowercase Gilroy Bold wordmark, one or more lines, tight leading like the space works masters."""
    f = font("Gilroy-Bold.woff", size)
    boxes = [f.getbbox(t, anchor="ls") for t in lines]  # relative to the baseline
    asc = -min(b[1] for b in boxes)
    step = round(size * leading)
    w = max(b[2] - b[0] for b in boxes)
    h = step * (len(lines) - 1) + max(b[3] for b in boxes) + asc
    im = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(im)
    for i, (t, b) in enumerate(zip(lines, boxes)):
        d.text((-b[0], asc + i * step), t, font=f, fill=rgb(colour), anchor="ls")
    return im.crop(im.getbbox())


def lockup(mark, lines, colour, h, text_h):
    m = fit(mark, h)
    t = text(lines, 400, colour)
    t = fit(t, text_h)
    gap = round(h / 6)  # gap between symbol and wordmark: H / 6
    im = Image.new("RGBA", (m.width + gap + t.width, h))
    im.alpha_composite(m, (0, 0))
    im.alpha_composite(t, (m.width + gap, (h - t.height) // 2))
    return im


def tile(size, scale=0.62, radius=0.0):
    t = Image.new("RGBA", (size, size))
    ImageDraw.Draw(t).rounded_rectangle([0, 0, size - 1, size - 1], round(size * radius), fill=rgb(PAPER))
    a = fit(art, round(size * scale))
    t.alpha_composite(a, ((size - a.width) // 2, (size - a.height) // 2))
    return t


def save(img, rel, svg=False, title="Nobody Builds"):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, optimize=True)
    if svg:  # SVG wrapper around the PNG: the artwork only exists as pixels
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        w, h = img.size
        path.with_suffix(".svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-labelledby="t"><title id="t">{title}</title>'
            f'<image width="{w}" height="{h}" href="data:image/png;base64,{data}"/></svg>\n',
            encoding="utf-8")


dark_art = sticker(art)
H = art.height  # 280 px: the artwork's native height, never upscaled in the masters

# logo/
save(pad(art, 24), "logo/symbol.png", svg=True, title="Nobody Builds symbol")
save(pad(dark_art, 16), "logo/symbol-dark.png", svg=True, title="Nobody Builds symbol for dark surfaces")
save(tile(512, radius=0.22), "logo/app-icon.png", svg=True, title="Nobody Builds app icon")
for name, mark, colour in (("", art, NIGHT_SHIFT), ("-reversed", dark_art, PAPER)):
    save(pad(lockup(mark, ["nobody", "builds"], colour, H, round(H * 0.8)), 24),
         f"logo/lockup-stacked{name}.png", svg=True, title="Nobody Builds logo")
    save(pad(lockup(mark, ["nobody builds"], colour, H, round(H * 0.42)), 24),
         f"logo/lockup-horizontal{name}.png", svg=True, title="Nobody Builds logo")

# icons/
square = tile(1024, scale=0.66)
for s in (16, 32, 180, 192, 512):
    save(square.resize((s, s), Image.LANCZOS), f"icons/icon-{s}.png")
save(square.resize((64, 64), Image.LANCZOS), "icons/favicon.png", svg=True, title="Nobody Builds")
(ROOT / "icons" / "favicon.png").unlink()

og = Image.new("RGBA", (1200, 630), rgb(PAPER))
ImageDraw.Draw(og).rounded_rectangle([40, 40, 1160, 590], 32, fill=rgb(SKY))
lk = lockup(art, ["nobody", "builds"], NIGHT_SHIFT, 330, 264)
og.alpha_composite(lk, ((1200 - lk.width) // 2, 120))
sub = font("Gilroy-Medium.woff", 40)
d = ImageDraw.Draw(og)
d.text((600, 535), "Design system", font=sub, fill=rgb(BLUEPRINT), anchor="mm")
save(og.convert("RGB"), "icons/og-1200x630.png")

# mascot/
save(pad(art, 24), "mascot/builder.png")
save(pad(dark_art, 16), "mascot/dark/builder.png")
shutil.copyfile(SRC / "avatar-460.png", ROOT / "mascot/original/builder.png")  # byte-for-byte

# brand/logo-masters.png: the one-page overview, like the space works logo library
sheet = Image.new("RGBA", (1440, 1150), rgb(PAPER))
d = ImageDraw.Draw(sheet)
d.text((64, 100), "Logo masters", font=font("Gilroy-Bold.woff", 56), fill=rgb(NIGHT_SHIFT), anchor="ls")
d.text((64, 150), "The builder, as supplied. Keep the master proportions.", font=font("Gilroy-Regular.woff", 26),
       fill=rgb(NIGHT_SHIFT), anchor="ls")
small = font("Gilroy-Medium.woff", 20)
d.text((64, 215), "Full colour", font=small, fill=rgb(BLUEPRINT), anchor="ls")
d.rounded_rectangle([720, 190, 1376, 760], 24, fill=rgb(NIGHT_SHIFT))
d.text((752, 230), "Reversed", font=small, fill=rgb(HARD_HAT), anchor="ls")
for x, mark, colour, cap in ((64, art, NIGHT_SHIFT, NIGHT_SHIFT), (752, dark_art, PAPER, PAPER)):
    st = lockup(mark, ["nobody", "builds"], colour, 200, 160)
    sheet.alpha_composite(st, (x, 250))
    d.text((x, 485), "Primary", font=small, fill=rgb(cap), anchor="ls")
    hz = lockup(mark, ["nobody builds"], colour, 110, 46)
    sheet.alpha_composite(hz, (x, 520))
    d.text((x, 660), "Horizontal", font=small, fill=rgb(cap), anchor="ls")
d.line([64, 800, 1376, 800], fill=rgb("#D3DAE6"), width=2)
d.rounded_rectangle([40, 820, 330, 1080], 12, fill=(255, 255, 255))
sheet.alpha_composite(tile(240, radius=0.22), (65, 830))
d.text((64, 1110), "App tile", font=small, fill=rgb(NIGHT_SHIFT), anchor="ls")
d.text((400, 880), "Seven colour styles", font=font("Gilroy-SemiBold.woff", 28), fill=rgb(NIGHT_SHIFT), anchor="ls")
for i, c in enumerate(SEVEN):
    x = 400 + i * 136
    d.rounded_rectangle([x, 905, x + 116, 1005], 10, fill=rgb(c), outline=rgb(NIGHT_SHIFT) if c == PAPER else None)
    d.text((x, 1035), c, font=font("Gilroy-Regular.woff", 18), fill=rgb(NIGHT_SHIFT), anchor="ls")
d.text((400, 1100), "Gilroy / primary", font=font("Gilroy-SemiBold.woff", 28), fill=rgb(NIGHT_SHIFT), anchor="ls")
d.text((860, 1100), "Unbounded / accent", font=font("Unbounded-Variable.woff2", 28), fill=rgb(NIGHT_SHIFT), anchor="ls")
save(sheet.convert("RGB"), "brand/logo-masters.png")
print("build-assets: logo/, icons/, mascot/ and brand/logo-masters.png written")
