"""The 15 rotating post layouts, picked from JD's sample boards.

Each function gets a dict `p` with: img (the <img> tag), head, cap, word, hs (headline px size)
and returns (css, body_html). Colors come from CSS vars set by the palette.
"""


def bold_repeat(p):
    """1. Big repeated block word behind a large offset photo (sample: 'BOLD')."""
    rows = "".join(
        f'<div class="word {"outline" if i % 2 else ""}" style="font-size:190px;color:var(--a)">'
        f'{p["word"]} {p["word"]} {p["word"]}</div>' for i in range(8))
    css = """
      .rep{position:absolute;left:-40px;top:-20px;width:1300px;z-index:1}
      .shadow{left:150px;top:130px;width:840px;height:980px;background:var(--b);z-index:2}
      .ph{left:110px;top:90px;width:840px;height:980px;z-index:3;border:14px solid var(--frame)}
      .pill{left:0;right:0;top:1110px;z-index:6;text-align:center}
      .pill span{display:inline-block;background:var(--ink);color:var(--frame);font-family:Shrikhand,serif;font-size:58px;padding:10px 40px;border-radius:60px}
      .cap{bottom:44px}"""
    body = f"""<div class="rep">{rows}</div>
      <div class="abs shadow"></div><div class="clip ph">{p['img']}</div>
      <div class="abs pill"><span>{p['head']}</span></div><div class="cap">{p['cap']}</div>"""
    return css, body


def vertical_strip(p):
    """2. Vertical repeated word strip on the left + tall photo + thin squiggle (sample: 'BE YOU')."""
    strip = " · ".join([p["word"]] * 6)
    css = """
      .strip{left:0;top:0;width:150px;height:1350px;background:var(--a);z-index:2}
      .strip div{position:absolute;left:75px;top:675px;transform:translate(-50%,-50%) rotate(-90deg);
        font-family:Bungee,sans-serif;font-size:58px;color:var(--frame);white-space:nowrap;letter-spacing:4px}
      .ph{left:200px;top:200px;width:830px;height:960px;z-index:3;border-radius:6px}
      .head{left:190px;right:30px;top:52px;font-size:var(--hs);text-align:left}
      .cap{left:200px;right:40px;text-align:left}"""
    squiggle = """<svg class="full" style="z-index:4;pointer-events:none" viewBox="0 0 1080 1350">
      <path d="M130 1240 C300 1150 260 1300 470 1230 S720 1120 760 1250 S980 1210 1060 1120" stroke="var(--frame)" stroke-width="7" fill="none" stroke-linecap="round"/>
      <path d="M1010 170 c30 -40 70 10 40 40 s-60 40 -20 70" stroke="var(--b)" stroke-width="9" fill="none" stroke-linecap="round"/></svg>"""
    body = f"""<div class="abs strip"><div>{strip}</div></div>
      <div class="head" style="--hs:{min(p['hs'],64)}px">{p['head']}</div>
      <div class="clip ph">{p['img']}</div>{squiggle}<div class="cap">{p['cap']}</div>"""
    return css, body


def psy_waves(p):
    """3. Groovy wavy-stripe background + photo in a thick white mat (sample: yellow wave pattern)."""
    waves = "".join(
        f'<path d="M-50 {y} C130 {y-60} 260 {y+60} 440 {y} S800 {y-60} 1130 {y}" stroke="var(--soft)" stroke-width="22" fill="none"/>'
        for y in range(-20, 1400, 62))
    css = """
      .mat{left:90px;top:210px;width:900px;height:960px;background:var(--frame);z-index:3;padding:26px;box-shadow:12px 14px 0 var(--a)}
      .mat .clip{position:relative;width:100%;height:100%}
      .head{left:60px;right:60px;top:40px;z-index:6}
      .head span{display:inline-block;background:var(--frame);padding:12px 44px;border-radius:80px;font-size:var(--hs)}
      .cap span{display:inline-block;background:var(--frame);padding:8px 26px;border-radius:30px;line-height:1.35}"""
    body = f"""<svg class="full" viewBox="0 0 1080 1350">{waves}</svg>
      <div class="head" style="--hs:{min(p['hs'],80)}px"><span>{p['head']}</span></div>
      <div class="abs mat"><div class="clip">{p['img']}</div></div>
      <div class="cap"><span>{p['cap']}</span></div>"""
    return css, body


def outline_offset(p):
    """4. Photo with a thin offset outline frame + spinning circle text badge (sample: 'NEW' badge)."""
    css = """
      .line{left:150px;top:170px;width:850px;height:960px;border:5px solid var(--a);z-index:2}
      .ph{left:90px;top:220px;width:850px;height:960px;z-index:3}
      .head{left:60px;right:60px;top:52px;font-size:var(--hs)}
      .badge{left:20px;top:1010px;width:250px;height:250px;z-index:5}"""
    badge = f"""<svg class="abs badge" viewBox="0 0 250 250"><circle cx="125" cy="125" r="118" fill="var(--b)"/>
      <defs><path id="cir" d="M125 125 m-88 0 a88 88 0 1 1 176 0 a88 88 0 1 1 -176 0"/></defs>
      <text font-family="Poppins" font-weight="800" font-size="25" letter-spacing="5" fill="var(--ink)">
      <textPath href="#cir">{p['badge']} • {p['badge']} • {p['badge']} •</textPath></text>
      <path transform="translate(125 125) scale(1.4)" d="M0-22 L6-6 L22 0 L6 6 L0 22 L-6 6 L-22 0 L-6-6Z" fill="var(--a)"/></svg>"""
    body = f"""<div class="head" style="--hs:{p['hs']}px">{p['head']}</div>
      <div class="abs line"></div><div class="clip ph">{p['img']}</div>{badge}<div class="cap">{p['cap']}</div>"""
    return css, body


def circle_curved(p):
    """5. Photo fills the whole post; cream arch band at top with the headline curved over a big ring outline (sample: 'meet the owner')."""
    css = """
      .ph{left:0;top:0;width:1080px;height:1350px;z-index:1}
      .cap{bottom:34px;z-index:7}
      .cap span{display:inline-block;background:var(--frame);padding:10px 30px;border-radius:40px;line-height:1.35}"""
    arc = f"""<svg class="full" style="z-index:5" viewBox="0 0 1080 1350">
      <path d="M0 0 H1080 V230 C840 120 240 120 0 230Z" fill="var(--frame)"/>
      <circle cx="540" cy="760" r="470" fill="none" stroke="var(--frame)" stroke-width="10"/>
      <circle cx="540" cy="760" r="495" fill="none" stroke="var(--a)" stroke-width="8" stroke-dasharray="4 22" stroke-linecap="round"/>
      <defs><path id="arc" d="M150 250 A520 300 0 0 1 930 250"/></defs>
      <text font-family="Shrikhand" font-size="{min(p['hs'],86)}" fill="var(--ink)" text-anchor="middle"><textPath href="#arc" startOffset="50%">{p['head']}</textPath></text></svg>"""
    body = f"""<div class="clip ph">{p['img']}</div>{arc}<div class="cap"><span>{p['cap']}</span></div>"""
    return css, body


def abstract_frame(p):
    """6. Bold black-and-white abstract pattern border around the photo (sample: zebra 'SALE')."""
    css = """
      .pat{left:70px;top:190px;width:940px;height:1010px;z-index:2;
        background:radial-gradient(circle at 20% 30%,var(--ink) 0 40px,transparent 41px),
          radial-gradient(circle at 70% 80%,var(--ink) 0 55px,transparent 56px),
          repeating-linear-gradient(55deg,var(--ink) 0 26px,var(--frame) 26px 60px)}
      .ph{left:120px;top:240px;width:840px;height:910px;z-index:3;border:10px solid var(--frame)}
      .head{left:60px;right:60px;top:46px;font-size:var(--hs)}"""
    body = f"""<div class="head" style="--hs:{p['hs']}px">{p['head']}</div>
      <div class="abs pat"></div><div class="clip ph">{p['img']}</div><div class="cap">{p['cap']}</div>"""
    return css, body


def script_repeat(p):
    """7. Headline repeated in script, stacked, over a blob + big circle photo (sample: 'sale sale sale')."""
    lines = "".join(f'<div>{p["head"]}</div>' for _ in range(3))
    css = """
      .blob{left:-80px;top:60px;width:760px;height:620px;background:var(--soft);border-radius:60% 40% 55% 45%/55% 45% 55% 45%;z-index:1}
      .scr{left:50px;top:70px;z-index:6;font-family:Pacifico,cursive;font-size:var(--hs);line-height:1.15;color:var(--a);text-align:left}
      .scr div:nth-child(2){color:var(--ink)}
      .ring{left:130px;top:300px;width:900px;height:900px;border-radius:50%;background:var(--b);z-index:2}
      .ph{left:155px;top:325px;width:850px;height:850px;border-radius:50%;z-index:3;border:12px solid var(--frame)}
      .cap{bottom:40px}"""
    body = f"""<div class="abs blob"></div><div class="abs scr" style="--hs:{min(p['hs'],72)}px">{lines}</div>
      <div class="abs ring"></div><div class="clip ph">{p['img']}</div><div class="cap">{p['cap']}</div>"""
    return css, body


def squiggle_bg(p):
    """8. Photo fills the whole post with hand-drawn squiggle doodles around the edges + headline on a color pill (sample: mustard squiggles)."""
    css = """
      .ph{left:0;top:0;width:1080px;height:1350px;z-index:1}
      .head{left:0;right:0;top:46px;z-index:6}
      .head span{display:inline-block;background:var(--a);color:var(--frame);padding:12px 46px;border-radius:70px;font-size:var(--hs);transform:rotate(-2deg)}
      .cap{bottom:34px;z-index:6}
      .cap span{display:inline-block;background:var(--frame);padding:10px 30px;border-radius:40px;line-height:1.35}"""
    doodles = """<svg class="full" style="z-index:4" viewBox="0 0 1080 1350" fill="none" stroke-linecap="round">
      <path d="M30 260 c40 -60 90 40 130 -10 s70 -70 120 0" stroke="var(--frame)" stroke-width="12"/>
      <path d="M840 300 c30 -50 80 30 110 -10 s60 -60 100 0" stroke="var(--b)" stroke-width="12"/>
      <path d="M40 1120 c50 -40 60 50 110 20 s40 -70 100 -30" stroke="var(--b)" stroke-width="12"/>
      <path d="M850 1150 c40 -60 90 40 130 -10 s50 -60 90 -10" stroke="var(--frame)" stroke-width="12"/>
      <path d="M990 560 c-40 40 30 80 -10 120 s-50 60 0 100" stroke="var(--frame)" stroke-width="10"/>
      <path d="M70 620 c40 40 -30 80 10 120 s50 60 0 100" stroke="var(--a)" stroke-width="10"/>
      <path d="M1000 420 l18 -40 l18 40 l40 18 l-40 18 l-18 40 l-18 -40 l-40 -18z" fill="var(--b)" stroke="none"/>
      <path d="M60 470 l14 -30 l14 30 l30 14 l-30 14 l-14 30 l-14 -30 l-30 -14z" fill="var(--frame)" stroke="none"/></svg>"""
    body = f"""<div class="clip ph">{p['img']}</div>{doodles}
      <div class="head" style="--hs:{min(p['hs'],80)}px"><span>{p['head']}</span></div><div class="cap"><span>{p['cap']}</span></div>"""
    return css, body


def polaroid_new(p):
    """9. Polaroid card with bold caption bar + giant outlined repeated word on the right (sample: 'NEW / Converse')."""
    rows = "".join(f'<div class="word outline" style="font-size:230px">{p["badge"]}</div>' for _ in range(7))
    css = """
      .rep{right:-60px;top:-30px;z-index:1;text-align:right}
      .rep .outline{-webkit-text-stroke:4px var(--a)}
      .card{left:70px;top:110px;width:880px;height:1110px;background:#fffdf8;z-index:3;padding:32px 32px 170px;box-shadow:16px 18px 0 var(--b);transform:rotate(-1.5deg)}
      .card .clip{position:relative;width:100%;height:100%}
      .bar{position:absolute;left:32px;right:32px;bottom:42px;text-align:center;font-family:Shrikhand,serif;font-size:var(--hs);color:#3B2A20}
      .cap{bottom:38px}"""
    body = f"""<div class="abs rep">{rows}</div>
      <div class="abs card"><div class="clip">{p['img']}</div><div class="bar" style="--hs:{min(p['hs'],76)}px">{p['head']}</div></div>
      <div class="cap">{p['cap']}</div>"""
    return css, body


def review_card(p):
    """10. Rounded speech-bubble card with a five-star header (sample: 'Reviews' card)."""
    css = """
      .card{left:60px;top:60px;width:960px;height:1150px;background:var(--a);border-radius:44px;z-index:2}
      .tail{left:110px;top:1190px;width:0;height:0;border-left:40px solid transparent;border-right:40px solid transparent;border-top:70px solid var(--a);z-index:2}
      .stars{left:60px;width:960px;top:92px;text-align:center;font-size:44px;letter-spacing:10px;color:var(--b);z-index:4}
      .head{left:80px;right:80px;top:150px;font-family:Pacifico,cursive;font-size:var(--hs);color:var(--frame)}
      .ph{left:100px;top:290px;width:880px;height:880px;border-radius:30px;z-index:3;border:10px solid var(--frame)}
      .cap{bottom:36px;font-size:27px}"""
    body = f"""<div class="abs card"></div><div class="abs tail"></div><div class="abs stars">★★★★★</div>
      <div class="head" style="--hs:{min(p['hs'],70)}px">{p['head']}</div>
      <div class="clip ph">{p['img']}</div><div class="cap">{p['cap']}</div>"""
    return css, body


def circle_bubble(p):
    """11. Big circle 'bubble' with the headline overlapping the photo corner + dashed lines (sample: '1K GIVEAWAY')."""
    dashes = "".join(f'<line x1="{x}" y1="30" x2="{x}" y2="300" stroke="var(--ink)" stroke-width="12" stroke-dasharray="40 26" stroke-linecap="round"/>'
                     for x in (40, 90, 140))
    css = """
      .ph{left:190px;top:250px;width:840px;height:920px;z-index:3;border-radius:16px}
      .bub{left:40px;top:60px;width:430px;height:430px;border-radius:50%;background:var(--soft);z-index:5;
        display:flex;align-items:center;justify-content:center;text-align:center;padding:40px;box-shadow:10px 12px 0 var(--a)}
      .bub span{font-family:Shrikhand,serif;font-size:var(--hs);line-height:1.02;color:var(--ink)}
      .swoosh{left:640px;top:40px;width:520px;height:330px;background:var(--b);border-radius:60% 40% 50% 50%;z-index:1}
      .cap{left:220px;right:40px;text-align:left;bottom:44px}"""
    body = f"""<svg class="full" style="z-index:2" viewBox="0 0 1080 1350">{dashes}</svg><div class="abs swoosh"></div>
      <div class="clip ph">{p['img']}</div>
      <div class="abs bub" style="--hs:{min(p['hs'],64)}px"><span>{p['head']}</span></div><div class="cap">{p['cap']}</div>"""
    return css, body


def xoxo_tilt(p):
    """12. Photo slightly tilted with a solid color block + big hand-drawn XOXO (sample: 'STARBOY xoxo')."""
    css = """
      .blk{left:140px;top:120px;width:860px;height:1000px;background:var(--a);transform:rotate(3deg);z-index:2}
      .ph{left:100px;top:150px;width:860px;height:1000px;z-index:3;transform:rotate(-2deg);border:12px solid var(--frame)}
      .xo{left:520px;top:1060px;z-index:6;font-family:Bungee,sans-serif;font-size:130px;color:var(--frame);
        -webkit-text-stroke:5px var(--ink);transform:rotate(-8deg);letter-spacing:-6px}
      .head{left:60px;right:60px;top:40px;font-size:var(--hs)}
      .cap{left:50px;right:520px;text-align:left;bottom:40px;font-size:26px}"""
    body = f"""<div class="head" style="--hs:{min(p['hs'],80)}px">{p['head']}</div>
      <div class="abs blk"></div><div class="clip ph">{p['img']}</div><div class="abs xo">XOXO</div>
      <div class="cap">{p['cap']}</div>"""
    return css, body


def leopard_blob(p):
    """13. Leopard-spot blob peeking behind a rounded photo + mint XO doodles (sample: 'Thank you 1K followers')."""
    import random
    rnd = random.Random(3)
    spots = "".join(
        f'<ellipse cx="{rnd.randint(20,560)}" cy="{rnd.randint(20,560)}" rx="{rnd.randint(12,22)}" ry="{rnd.randint(9,16)}" fill="var(--ink)" transform="rotate({rnd.randint(0,180)})" transform-origin="center"/>'
        for _ in range(70))
    css = """
      .leo{left:-60px;top:110px;width:600px;height:600px;z-index:1}
      .ph{left:150px;top:230px;width:860px;height:930px;z-index:3;border-radius:48px;border:12px solid var(--frame)}
      .head{left:60px;right:60px;top:44px;font-size:var(--hs)}
      .xo{left:40px;top:1110px;z-index:6;font-family:Shrikhand,serif;font-size:120px;color:var(--c);transform:rotate(-10deg)}"""
    body = f"""<svg class="abs leo" viewBox="0 0 600 600"><clipPath id="lb"><path d="M300 20 C470 10 590 150 570 320 C550 490 400 590 250 570 C90 550 0 420 20 260 C40 110 150 30 300 20Z"/></clipPath>
      <g clip-path="url(#lb)"><rect width="600" height="600" fill="var(--b)"/>{spots}</g></svg>
      <div class="head" style="--hs:{p['hs']}px">{p['head']}</div>
      <div class="clip ph">{p['img']}</div><div class="abs xo">xo</div><div class="cap" style="left:260px">{p['cap']}</div>"""
    return css, body


def plus_dots(p):
    """14. Big plus marks + halftone dot grid + headline on a brush blob (sample: 'BE BOLD')."""
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="var(--frame)"/>' for x in range(620, 1080, 40) for y in range(40, 260, 40))
    css = """
      .ph{left:70px;top:270px;width:940px;height:930px;z-index:3;border-radius:22px;border:12px solid var(--frame)}
      .brush{left:60px;top:70px;width:760px;height:170px;background:var(--c);border-radius:50% 40% 55% 45%/60% 50% 50% 40%;z-index:4;transform:rotate(-2deg)}
      .head{left:60px;width:760px;top:100px;font-size:var(--hs);z-index:6;color:var(--ink)}"""
    plus = """<path d="M820 -40 h90 v160 h160 v90 h-160 v160 h-90 v-160 h-160 v-90 h160z" fill="var(--a)" opacity=".85"/>
      <path d="M-30 1150 h70 v120 h120 v70 h-120 v120 h-70 v-120 h-120 v-70 h120z" fill="var(--a)" opacity=".85"/>"""
    body = f"""<svg class="full" viewBox="0 0 1080 1350">{dots}{plus}</svg>
      <div class="abs brush"></div><div class="head" style="--hs:{min(p['hs'],74)}px">{p['head']}</div>
      <div class="clip ph">{p['img']}</div><div class="cap">{p['cap']}</div>"""
    return css, body


def pink_waves(p):
    """15. Soft wavy bands background + photo with a thin gold frame (sample: pink waves portrait)."""
    bands = "".join(
        f'<path d="M-60 {y} C120 {y-90} 300 {y+90} 540 {y} S900 {y-90} 1140 {y}" stroke="var(--soft)" stroke-width="48" fill="none"/>'
        for y in range(60, 1400, 170))
    css = """
      .gold{left:100px;top:200px;width:880px;height:990px;border:6px solid var(--b);z-index:3;padding:18px;background:var(--frame)}
      .gold .clip{position:relative;width:100%;height:100%}
      .head{left:60px;right:60px;top:46px;font-size:var(--hs)}"""
    body = f"""<svg class="full" viewBox="0 0 1080 1350">{bands}</svg>
      <div class="head" style="--hs:{p['hs']}px">{p['head']}</div>
      <div class="abs gold"><div class="clip">{p['img']}</div></div><div class="cap">{p['cap']}</div>"""
    return css, body


LAYOUTS = {
    "bold_repeat": bold_repeat, "vertical_strip": vertical_strip, "psy_waves": psy_waves,
    "outline_offset": outline_offset, "circle_curved": circle_curved, "abstract_frame": abstract_frame,
    "script_repeat": script_repeat, "squiggle_bg": squiggle_bg, "polaroid_new": polaroid_new,
    "review_card": review_card, "circle_bubble": circle_bubble, "xoxo_tilt": xoxo_tilt,
    "leopard_blob": leopard_blob, "plus_dots": plus_dots, "pink_waves": pink_waves,
}
ORDER = list(LAYOUTS)
