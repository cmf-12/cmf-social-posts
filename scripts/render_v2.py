"""Render CMF posts with the 10 rotating layouts in layouts.py.

posts/YYYY-MM-DD.json:
{
  "photo": "https://cdn.shopify.com/...jpg",
  "headline": "Love at first touch",          # catchy phrase, different every day
  "product": "Burgundy floral damask velvet",  # product name
  "price": "$26.99/yd",
  "caption": optional full override of the bottom line,
  "word": "VELVET",         # big repeated word (layouts 1, 2)   default: FABRIC
  "badge": "NEW",           # badge / outlined word (layouts 4, 9) default: NEW
  "layout": optional override, else rotates by date (Feb 1 2027 = layout 1)
  "palette": optional override, else rotates by date (6 themes)
  "fit": "cover" | "contain"
}
Usage: python scripts/render_v2.py [files...]   (no args = all posts/*.json)
Env LOCAL_FONTS=/path/to/node_modules/@fontsource embeds fonts for offline previews.
"""
import datetime
import html
import json
import os
import pathlib
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from layouts import LAYOUTS, ORDER  # noqa: E402
from layouts_b import LAYOUTS_B, ORDER_B  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "templates" / "base.html").read_text()
BASE_B = (ROOT / "templates" / "base_b.html").read_text()

TERRA, MUSTARD, BLUSH, PEACH, MINT, CREAM, INK = (
    "#D9663F", "#E8A93A", "#F4BDB8", "#F7CBA6", "#A9D8C4", "#FBF3E6", "#3B2A20")

# bg, a (main accent), b (second accent), c, ink, frame (mat/border), soft (pattern tint)
PALETTES = {
    "blush":   (BLUSH, TERRA, MUSTARD, MINT, INK, CREAM, "#F8D3CF"),
    "mint":    (MINT, TERRA, MUSTARD, BLUSH, INK, CREAM, "#C4E6D7"),
    "mustard": (MUSTARD, TERRA, CREAM, MINT, INK, CREAM, "#F2C56C"),
    "peach":   (PEACH, TERRA, MINT, MUSTARD, INK, CREAM, "#FADCC2"),
    "cream":   (CREAM, TERRA, MUSTARD, MINT, INK, "#FFFFFF", "#F2E2C8"),
    "sky":     ("#BFE0E6", TERRA, MUSTARD, BLUSH, INK, CREAM, "#D6ECEF"),
}
PALETTE_ORDER = ["blush", "mint", "mustard", "peach", "cream", "sky", "mint"]  # 7-day cycle
EPOCH = datetime.date(2027, 2, 1)
BRAND = "Classic Modern Fabrics"
# Brand reminder: 3 of every 5 posts get a bold tag line ("B" = brand name, "P" = product name).
TAG_CYCLE = ["B", None, "P", None, "B", "P", None, "B", None, "P"]


def local_fonts():
    base = os.environ.get("LOCAL_FONTS")
    if not base:
        return ""
    faces = [("Shrikhand", "shrikhand/files/shrikhand-latin-400-normal.woff2", 400),
             ("Pacifico", "pacifico/files/pacifico-latin-400-normal.woff2", 400),
             ("Bungee", "bungee/files/bungee-latin-400-normal.woff2", 400),
             ("Poppins", "poppins/files/poppins-latin-500-normal.woff2", 500),
             ("Poppins", "poppins/files/poppins-latin-700-normal.woff2", 700),
             ("Poppins", "poppins/files/poppins-latin-800-normal.woff2", 800)]
    for w in (400, 500, 600, 700):
        faces.append(("Cormorant Garamond", f"cormorant-garamond/files/cormorant-garamond-latin-{w}-normal.woff2", w))
    for w in (300, 400, 500, 600):
        faces.append(("Montserrat", f"montserrat/files/montserrat-latin-{w}-normal.woff2", w))
    faces += [("Playfair Display", "playfair-display/files/playfair-display-latin-500-normal.woff2", 500),
              ("Bebas Neue", "bebas-neue/files/bebas-neue-latin-400-normal.woff2", 400),
              ("Josefin Sans", "josefin-sans/files/josefin-sans-latin-300-normal.woff2", 300)]
    css = "".join(f"@font-face{{font-family:'{n}';font-weight:{w};src:url('file://{base}/{f}')}}" for n, f, w in faces)
    css += (f"@font-face{{font-family:'Playfair Display';font-style:italic;font-weight:500;src:url('file://{base}/playfair-display/files/playfair-display-latin-500-italic.woff2')}}"
            f"@font-face{{font-family:'Cormorant Garamond';font-style:italic;font-weight:500;src:url('file://{base}/cormorant-garamond/files/cormorant-garamond-latin-500-italic.woff2')}}")
    return f"<style>{css}</style>"


def day_index(date_str):
    try:
        return (datetime.date.fromisoformat(date_str) - EPOCH).days
    except ValueError:
        return 0


def pick(date_str, post):
    n = day_index(date_str)
    layout = post.get("layout") or ORDER[n % len(ORDER)]
    palette = post.get("palette") or PALETTE_ORDER[n % len(PALETTE_ORDER)]
    return layout, palette


def caption_html(post, date_str):
    """Bottom line. On tag days it starts with a bold BRAND or PRODUCT line."""
    if post.get("caption"):
        return html.escape(post["caption"])
    tag = post.get("tag", TAG_CYCLE[day_index(date_str) % len(TAG_CYCLE)])
    product, price, site = post.get("product", ""), post.get("price", ""), "classicmodernfabrics.com"
    if tag == "B":
        top = f'<b class="tg">{html.escape(BRAND)}</b><br>'
        rest = " · ".join(x for x in (product, price, site) if x)
    elif tag == "P":
        top = f'<b class="tg">{html.escape(product)}</b><br>'
        rest = " · ".join(x for x in (price, site) if x)
    else:
        top, rest = "", " · ".join(x for x in (product, price, site) if x)
    return top + html.escape(rest)


def design_set(post, date_str):
    """Which layout set a post uses: the post's own "set", else sets.json (latest "from" date wins), else A."""
    if post.get("set"):
        return post["set"].upper()
    cfg = ROOT / "sets.json"
    chosen = "A"
    if cfg.exists():
        for row in sorted(json.loads(cfg.read_text()), key=lambda r: r["from"]):
            if row["from"] <= date_str:
                chosen = row["set"].upper()
    return chosen


POS = ["50% 50%", "25% 35%", "75% 65%", "35% 80%", "70% 25%"]


def build_html_b(post, date_str=""):
    n = day_index(date_str)
    layout = post.get("layout") if post.get("layout") in LAYOUTS_B else ORDER_B[n % len(ORDER_B)]
    photos = post.get("photos") or [post["photo"]]
    title = post.get("category") or post["headline"]
    tag = post.get("tag", TAG_CYCLE[n % len(TAG_CYCLE)])
    alt = html.escape(post.get("product", title))

    def ph(i, cls="", style="", pos=None):
        src = photos[i % len(photos)]
        if pos is None and i >= len(photos):
            pos = POS[i % len(POS)]
        st = f' style="object-position:{pos}"' if pos else ""
        return f'<div class="ph {cls}" style="{style}"><img src="{html.escape(src)}" alt="{alt}"{st}></div>'

    def foot(light=False, site_only=False):
        pn = ""
        if tag in ("B", "P") and not site_only:
            bits = " · ".join(x for x in (post.get("product", ""), post.get("price", "")) if x)
            pn = f'<span class="pn">{html.escape(bits)}</span>'
        return f'<div class="foot{" light" if light else ""}">{pn}classicmodernfabrics.com</div>'

    def fit(width, base, k):
        return min(base, int(width / (max(len(title), 4) * k)))

    p = {"ph": ph, "foot": foot, "fit": fit, "title": html.escape(title), "words": html.escape(title).split(),
         "product": html.escape(post.get("product", "")), "price": html.escape(post.get("price", "")),
         "headline": html.escape(post.get("headline", ""))}
    css, body = LAYOUTS_B[layout](p)
    out = BASE_B.replace("{{layout_css}}", css).replace("{{body}}", body).replace("{{local_fonts}}", local_fonts())
    return out, "B:" + layout


def build_html(post, date_str=""):
    if design_set(post, date_str) == "B":
        return build_html_b(post, date_str)
    layout, palette = pick(date_str, post)
    bg, a, b, c, ink, frame, soft = PALETTES[palette]
    head = post["headline"]
    hs = 92 if len(head) <= 16 else 72 if len(head) <= 22 else 58 if len(head) <= 30 else 50
    p = {
        "img": f'<img class="photo" src="{html.escape(post["photo"])}" alt="{html.escape(post.get("alt", head))}">',
        "head": html.escape(head), "cap": caption_html(post, date_str),
        "word": html.escape(post.get("word", "FABRIC")), "badge": html.escape(post.get("badge", "NEW")),
        "hs": post.get("headline_size", hs),
    }
    css, body = LAYOUTS[layout](p)
    vals = {"bg": bg, "a": a, "b": b, "c": c, "ink": ink, "frame": frame, "soft": soft,
            "fit": post.get("fit", "cover"), "layout_css": css, "body": body, "local_fonts": local_fonts()}
    out = BASE
    for k, v in vals.items():
        out = out.replace("{{" + k + "}}", str(v))
    return out, layout


def render(paths):
    (ROOT / "out").mkdir(exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350})
        for path in paths:
            post = json.loads(path.read_text())
            doc, layout = build_html(post, path.stem)
            tmp = ROOT / "out" / f".{path.stem}.html"
            tmp.write_text(doc)
            page.goto(tmp.resolve().as_uri(), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            dest = ROOT / "out" / f"{path.stem}.jpg"
            page.screenshot(path=str(dest), type="jpeg", quality=92)
            tmp.unlink()
            print("rendered", dest.relative_to(ROOT), "layout:", layout)
        browser.close()


if __name__ == "__main__":
    args = [pathlib.Path(a) for a in sys.argv[1:]] or sorted((ROOT / "posts").glob("*.json"))
    render([a if a.is_absolute() else ROOT / a for a in args])
