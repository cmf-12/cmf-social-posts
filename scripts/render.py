"""Render Classic Modern Fabrics social posts from posts/*.json into out/*.jpg.

Each post file (posts/YYYY-MM-DD.json) looks like:
{
  "photo": "https://cdn.shopify.com/...jpg",   # real product photo (URL or local path)
  "headline": "Pom pom party",
  "caption": "Melio pompom fringe · 4 yds $48.99 · classicmodernfabrics.com",
  "layout": optional; default rotates through 10 layouts by date (see LAYOUT_ORDER),
  "palette": optional; default rotates by date (6 themes),
  "decor": optional; default rotates by date (7 sets),
  "sticker": "optional short text",
  "fit": "cover" | "contain"                     # contain = whole product, no crop
}
Usage: python scripts/render.py [posts/2027-02-01.json ...]   (no args = render all that changed)
"""
import datetime
import html
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = (ROOT / "templates" / "post.html").read_text()

TERRA, MUSTARD, BLUSH, PEACH, MINT, CREAM, INK = (
    "#C8643B", "#E3A72F", "#F2B8B5", "#F6C6A0", "#A8D5BA", "#F6EEDF", "#3B2A20")

# bg, accent a (frame backing), accent b, accent c, ink, frame border
PALETTES = {
    "mint":       (MINT,    TERRA,   MUSTARD, BLUSH,  INK, CREAM),
    "blush":      (BLUSH,   TERRA,   MUSTARD, CREAM,  INK, CREAM),
    "mustard":    (MUSTARD, TERRA,   MINT,    BLUSH,  INK, CREAM),
    "peach":      (PEACH,   MINT,    MUSTARD, TERRA,  INK, CREAM),
    "cream":      (CREAM,   TERRA,   MUSTARD, MINT,   INK, "#FFFFFF"),
    "terracotta": (TERRA,   MUSTARD, CREAM,   PEACH,  CREAM, CREAM),
}

DECOR = {
    "waves": """
      <path d="M-20 1120 C120 1060 240 1180 380 1120 S640 1060 780 1120 S1000 1180 1120 1120" stroke="var(--b)" stroke-width="26" fill="none" stroke-linecap="round"/>
      <path d="M-20 1180 C120 1120 240 1240 380 1180 S640 1120 780 1180 S1000 1240 1120 1180" stroke="var(--c)" stroke-width="22" fill="none" stroke-linecap="round"/>
      <path d="M-20 230 C140 170 260 290 420 230 S700 170 860 230 S1040 290 1120 240" stroke="var(--a)" stroke-width="18" fill="none" stroke-linecap="round" opacity=".7"/>""",
    "blobs": """
      <path d="M-60 120 C40 20 220 60 230 180 C240 300 90 330 10 300 C-70 270 -120 200 -60 120Z" fill="var(--a)"/>
      <path d="M900 1060 C1000 980 1150 1040 1130 1160 C1110 1280 980 1300 910 1250 C840 1200 820 1120 900 1060Z" fill="var(--b)"/>
      <path d="M940 140 C1000 100 1080 130 1070 200 C1060 260 990 270 950 240 C910 210 900 170 940 140Z" fill="var(--c)"/>""",
    "stars": """
      <g fill="var(--b)">
        <path transform="translate(90 220) scale(1.3)" d="M0-40 L10-10 L40 0 L10 10 L0 40 L-10 10 L-40 0 L-10-10Z"/>
        <path transform="translate(980 260) scale(1)" d="M0-40 L10-10 L40 0 L10 10 L0 40 L-10 10 L-40 0 L-10-10Z"/>
        <path transform="translate(1000 1110) scale(1.5)" d="M0-40 L10-10 L40 0 L10 10 L0 40 L-10 10 L-40 0 L-10-10Z"/>
        <path transform="translate(80 1150) scale(.9)" d="M0-40 L10-10 L40 0 L10 10 L0 40 L-10 10 L-40 0 L-10-10Z"/>
      </g>
      <g fill="var(--c)"><circle cx="160" cy="300" r="10"/><circle cx="920" cy="190" r="12"/><circle cx="930" cy="1210" r="9"/></g>""",
    "hearts": """
      <g fill="var(--c)">
        <path transform="translate(95 230) scale(1.6)" d="M0 12 C-20 -4 -12 -18 0 -8 C12 -18 20 -4 0 12Z"/>
        <path transform="translate(990 300) scale(1.2)" d="M0 12 C-20 -4 -12 -18 0 -8 C12 -18 20 -4 0 12Z"/>
        <path transform="translate(985 1130) scale(1.8)" d="M0 12 C-20 -4 -12 -18 0 -8 C12 -18 20 -4 0 12Z"/>
        <path transform="translate(90 1120) scale(1.1)" d="M0 12 C-20 -4 -12 -18 0 -8 C12 -18 20 -4 0 12Z"/>
      </g>
      <text x="70" y="1230" font-family="Shrikhand,serif" font-size="46" fill="var(--a)">xo</text>
      <text x="930" y="420" font-family="Shrikhand,serif" font-size="46" fill="var(--a)">xo</text>""",
    "zebra": """
      <rect x="-120" y="300" width="260" height="260" rx="130" fill="url(#zebra)" opacity=".85"/>
      <rect x="840" y="1060" width="320" height="320" rx="160" fill="url(#zebra)" opacity=".85"/>""",
    "leopard": """
      <circle cx="80" cy="1180" r="150" fill="url(#leopard)"/>
      <circle cx="1010" cy="250" r="110" fill="url(#leopard)"/>""",
    "dots": """
      <rect x="0" y="0" width="1080" height="260" fill="url(#dots)" opacity=".55"/>
      <rect x="0" y="1110" width="1080" height="240" fill="url(#dots)" opacity=".55"/>""",
}

# The 10 layouts rotate one per day, in this order. Palettes and decor rotate on
# their own cycles (6 and 7 days), so the same combination only repeats every 210 days.
LAYOUT_ORDER = ["circle", "split", "arch", "polaroid", "tilt", "wave", "stamp", "blob", "tv", "offset"]
PALETTE_ORDER = ["blush", "mint", "mustard", "peach", "cream", "terracotta"]
DECOR_ORDER = ["hearts", "waves", "stars", "blobs", "zebra", "dots", "leopard"]
EPOCH = datetime.date(2027, 2, 1)  # Feb 1 2027 = layout #1


def defaults_for(date_str):
    try:
        n = (datetime.date.fromisoformat(date_str) - EPOCH).days
    except ValueError:
        n = 0
    return (LAYOUT_ORDER[n % len(LAYOUT_ORDER)], PALETTE_ORDER[n % len(PALETTE_ORDER)],
            DECOR_ORDER[n % len(DECOR_ORDER)])


def frame_html(layout, photo, alt):
    img = f'<img class="photo" src="{html.escape(photo)}" alt="{html.escape(alt)}">'
    clip = f'<div class="clip">{img}</div>'
    return {
        "circle":   f'<div class="ring">{clip}</div>',
        "arch":     f'<div class="shadow"></div>{clip}',
        "tilt":     f'<div class="back"></div><div class="card">{clip}</div>',
        "offset":   f'<div class="block"></div>{clip}',
        "split":    clip,
        "stamp":    f'<div class="perfshadow"></div><div class="perf"></div>{clip}',
        "blob":     f'<div class="under"></div>{clip}',
        "polaroid": f'<div class="p1"></div><div class="p2"></div><div class="card">{clip}</div>',
        "wave":     clip,
        "tv":       f'<div class="body">{clip}<div class="grill"></div><div class="knob k1"></div><div class="knob k2"></div></div>',
    }[layout]


def extra_html(layout, post):
    if layout == "split":
        return '<div class="band"></div>'
    if layout == "polaroid" and post.get("scribble"):
        return f'<div class="scribble">{html.escape(post["scribble"])}</div>'
    return ""


def build_html(post, date_str=""):
    d_layout, d_palette, d_decor = defaults_for(date_str)
    layout = post.get("layout") or d_layout
    bg, a, b, c, ink, frame = PALETTES[post.get("palette") or d_palette]
    headline = post["headline"]
    size = 92 if len(headline) <= 18 else 76 if len(headline) <= 26 else 62
    sticker = post.get("sticker")
    vals = {
        "bg": bg, "a": a, "b": b, "c": c, "ink": ink, "frame": frame,
        "headline": html.escape(headline),
        "headline_font": post.get("headline_font", "'Shrikhand', 'DM Serif Display', Georgia, serif"),
        "headline_size": str(post.get("headline_size", size)),
        "headline_size_split": str(min(118, int(1150 / max(len(headline), 8) * 1.7))),
        "caption": html.escape(post["caption"]),
        "layout": layout,
        "fit": post.get("fit", "cover"),
        "decor": DECOR[post.get("decor") or d_decor],
        "frame_html": frame_html(layout, post["photo"], post.get("alt", headline)),
        "extra_html": extra_html(layout, post),
        "sticker_html": f'<div class="sticker">{html.escape(sticker)}</div>' if sticker else "",
    }
    out = TEMPLATE
    for k, v in vals.items():
        out = out.replace("{{" + k + "}}", v)
    return out


def render(paths):
    (ROOT / "out").mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350})
        for path in paths:
            post = json.loads(path.read_text())
            tmp = ROOT / "out" / f".{path.stem}.html"
            tmp.write_text(build_html(post, path.stem))
            page.goto(tmp.resolve().as_uri(), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            dest = ROOT / "out" / f"{path.stem}.jpg"
            page.screenshot(path=str(dest), type="jpeg", quality=92, full_page=False)
            tmp.unlink()
            print("rendered", dest.relative_to(ROOT))
        browser.close()


if __name__ == "__main__":
    args = [pathlib.Path(a) for a in sys.argv[1:]]
    if not args:
        args = sorted((ROOT / "posts").glob("*.json"))
    render([a if a.is_absolute() else ROOT / a for a in args])
