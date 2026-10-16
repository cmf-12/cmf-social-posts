"""Set B: 15 elegant layouts (cream background, serif titles, product + room photos).

Each function takes p and returns (css, body). p has:
  ph(i, cls, style, pos)  -> html for photo slot i (cycles through the post's photos)
  title                    -> escaped category title, e.g. "Cotton Fabrics"
  words                    -> title split into words (for stacked titles)
  foot(light)              -> footer html (optional product line + site)
  fit(px_width, base, k)   -> font size that fits the title in px_width
"""
import math


def b_diagonal(p):
    s = p["fit"](980, 100, .46)
    css = f""".t{{left:40px;right:40px;top:44px;text-align:center;font-size:{s}px;font-weight:600}}
.d1{{left:40px;top:190px;width:1000px;height:1050px;clip-path:polygon(0 0,66% 0,30% 100%,0 100%)}}
.d2{{left:40px;top:190px;width:1000px;height:1050px;clip-path:polygon(69% 0,100% 0,100% 100%,33% 100%)}}"""
    body = (f'<div class="title serif t">{p["title"]}</div>' + p["ph"](0, "d1") + p["ph"](1, "d2")
            + p["foot"]())
    return css, body


def b_grid_pill(p):
    s = p["fit"](700, 46, .52)
    cell = "display:flex;align-items:center;justify-content:center;text-align:center;background:var(--paper);padding:24px;font-family:'Cormorant Garamond',serif;font-style:italic;font-size:30px;line-height:1.25;color:var(--muted)"
    css = f""".pill{{left:50%;transform:translateX(-50%);top:48px;padding:16px 46px;border:2px solid var(--line);border-radius:60px;background:var(--paper);
  font-family:'Montserrat',sans-serif;font-weight:500;font-size:{s}px;white-space:nowrap;z-index:6}}
.c{{position:absolute;{cell}}}"""
    L, C, R = 48, 360, 772
    body = (f'<div class="abs pill">{p["title"]}</div>'
            + p["ph"](1, "", f"left:{L}px;top:170px;width:300px;height:430px")
            + f'<div class="c" style="left:{L}px;top:612px;width:300px;height:200px">{p["product"]}</div>'
            + p["ph"](2, "", f"left:{L}px;top:824px;width:300px;height:426px")
            + f'<div class="c" style="left:{C}px;top:170px;width:360px;height:190px">{p["headline"]}</div>'
            + p["ph"](0, "", f"left:{C}px;top:372px;width:360px;height:680px")
            + f'<div class="c" style="left:{C}px;top:1064px;width:360px;height:186px">{p["price"]}</div>'
            + p["ph"](3, "", f"left:{R}px;top:170px;width:260px;height:520px")
            + f'<div class="c" style="left:{R}px;top:702px;width:260px;height:200px">Free shipping<br>over $75</div>'
            + p["ph"](4, "", f"left:{R}px;top:914px;width:260px;height:336px")
            + p["foot"](site_only=True))
    return css, body


def b_full_serif(p):
    s = p["fit"](980, 150, .44)
    css = f""".bgp{{inset:0}}
.shade{{position:absolute;inset:0;z-index:4;background:linear-gradient(180deg,rgba(0,0,0,.42) 0,rgba(0,0,0,0) 34%,rgba(0,0,0,0) 72%,rgba(0,0,0,.5) 100%)}}
.t{{left:40px;right:40px;top:70px;text-align:center;font-size:{s}px;font-weight:600;color:#fff;text-shadow:0 4px 22px rgba(0,0,0,.45)}}"""
    body = p["ph"](0, "bgp") + '<div class="shade"></div>' + f'<div class="title serif t">{p["title"]}</div>' + p["foot"](light=True)
    return css, body


def b_thumbs(p):
    s = p["fit"](980, 108, .44)
    css = f""".t{{left:40px;right:40px;top:44px;text-align:center;font-size:{s}px;font-weight:600}}"""
    body = (f'<div class="title serif t">{p["title"]}</div>'
            + p["ph"](0, "", "left:60px;top:180px;width:600px;height:770px")
            + p["ph"](1, "", "left:676px;top:180px;width:344px;height:377px")
            + p["ph"](2, "", "left:676px;top:573px;width:344px;height:377px")
            + p["ph"](3, "", "left:60px;top:966px;width:309px;height:284px")
            + p["ph"](4, "", "left:385px;top:966px;width:310px;height:284px")
            + p["ph"](1, "", "left:711px;top:966px;width:309px;height:284px", "30% 70%")
            + p["foot"]())
    return css, body


def b_fan(p):
    cx, cy, R = 540, 1110, 1000
    bounds = [180, 148, 112, 68, 32, 0]
    order = [2, 0, 1, 3, 4]
    wedges, lines = "", ""
    for k in range(5):
        a1, a2 = math.radians(bounds[k]), math.radians(bounds[k + 1])
        pts = [(cx, cy)]
        steps = 6
        for j in range(steps + 1):
            a = a1 + (a2 - a1) * j / steps
            pts.append((cx + 1800 * math.cos(a), cy - 1800 * math.sin(a)))
        poly = ",".join(f"{x:.0f}px {y:.0f}px" for x, y in pts)
        wedges += p["ph"](order[k], "", f"inset:0;clip-path:polygon({poly})")
    for b in bounds[1:-1]:
        a = math.radians(b)
        lines += f'<line x1="{cx}" y1="{cy}" x2="{cx + 1800 * math.cos(a):.0f}" y2="{cy - 1800 * math.sin(a):.0f}" stroke="#F5F0E8" stroke-width="12"/>'
    rays = ""
    for b in range(100, 171, 10):
        a = math.radians(b)
        rays += f'<line x1="{cx}" y1="{cy}" x2="{cx + 1400 * math.cos(a):.0f}" y2="{cy - 1400 * math.sin(a):.0f}" stroke="#B8975F" stroke-width="1.6"/>'
        a = math.radians(180 - b)
        rays += f'<line x1="{cx}" y1="{cy}" x2="{cx + 1400 * math.cos(a):.0f}" y2="{cy - 1400 * math.sin(a):.0f}" stroke="#B8975F" stroke-width="1.6"/>'
    s = p["fit"](940, 84, .42)
    css = f""".fan{{position:absolute;inset:0;clip-path:circle({R}px at {cx}px {cy}px);z-index:2}}
.rays{{position:absolute;inset:0;width:1080px;height:1350px;z-index:1}}
.band{{position:absolute;left:0;right:0;top:{cy}px;bottom:0;background:var(--bg);z-index:4}}
.t{{left:40px;right:40px;top:{cy + 34}px;text-align:center;font-size:{s}px;font-style:italic;font-weight:500}}
.rule{{position:absolute;left:150px;right:150px;top:{cy + 54 + s}px;height:2px;background:var(--line);z-index:6}}"""
    body = (f'<svg class="rays" viewBox="0 0 1080 1350">{rays}<circle cx="{cx}" cy="{cy}" r="{R + 18}" fill="none" stroke="#B8975F" stroke-width="2"/></svg>'
            + f'<div class="fan">{wedges}<svg class="full" viewBox="0 0 1080 1350">{lines}</svg></div>'
            + '<div class="band"></div>' + f'<div class="title play t">{p["title"]}</div><div class="rule"></div>' + p["foot"](site_only=True))
    return css, body


def b_deco_panels(p):
    longest = max(len(w) for w in p["words"])
    s = min(70, int(300 / (longest * .64)))
    css = f""".box{{left:48px;top:48px;width:380px;height:380px;background:var(--paper);border:2px solid var(--line);outline:1.5px solid var(--line);outline-offset:-14px;
  display:flex;flex-direction:column;justify-content:center;padding:0 38px;z-index:6}}
.box div{{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:{s}px;line-height:1.05;letter-spacing:2px;text-transform:uppercase}}
.ring{{position:absolute;border:2px solid var(--gold);z-index:5}}"""
    words = "".join(f"<div>{w}</div>" for w in p["words"])
    body = (f'<div class="abs box">{words}</div>'
            + p["ph"](0, "", "left:448px;top:48px;width:584px;height:380px;border-radius:0 0 0 300px")
            + p["ph"](2, "", "left:48px;top:448px;width:380px;height:800px;border-radius:0 300px 0 0")
            + p["ph"](1, "", "left:448px;top:448px;width:584px;height:800px;border-radius:300px 0 0 0")
            + '<div class="ring" style="left:462px;top:462px;width:556px;height:772px;border-radius:286px 0 0 0;border-right:0;border-bottom:0"></div>'
            + '<div class="ring" style="left:62px;top:462px;width:352px;height:772px;border-radius:0 286px 0 0;border-left:0;border-bottom:0"></div>'
            + '<div class="ring" style="left:462px;top:62px;width:556px;height:352px;border-radius:0 0 0 286px;border-top:0;border-right:0"></div>'
            + p["foot"](site_only=True))
    return css, body


def b_full_corner(p):
    longest = max(len(w) for w in p["words"])
    stack = len(p["title"]) > 11
    s = min(160, int(700 / (longest * .42))) if stack else min(170, int(800 / (max(len(p["title"]), 4) * .42)))
    css = f""".bgp{{inset:0}}
.shade{{position:absolute;inset:0;z-index:4;background:linear-gradient(200deg,rgba(0,0,0,.45) 0,rgba(0,0,0,0) 38%),linear-gradient(0deg,rgba(0,0,0,.45) 0,rgba(0,0,0,0) 20%)}}
.t{{right:56px;top:56px;max-width:900px;text-align:right;font-family:'Bebas Neue',sans-serif;font-size:{s}px;line-height:.92;letter-spacing:3px;color:#FBF3E6;text-shadow:0 4px 18px rgba(0,0,0,.45)}}"""
    t = "<br>".join(p["words"]) if stack else p["title"]
    body = p["ph"](0, "bgp") + '<div class="shade"></div>' + f'<div class="title t">{t}</div>' + p["foot"](light=True)
    return css, body


def b_full_light(p):
    longest = max(len(w) for w in p["words"])
    s = min(110, int(560 / (longest * .62)))
    css = f""".bgp{{inset:0}}
.veil{{position:absolute;right:-120px;top:-160px;width:820px;height:620px;z-index:4;background:radial-gradient(closest-side,rgba(251,248,242,.9),rgba(251,248,242,.55) 60%,rgba(251,248,242,0))}}
.shade{{position:absolute;inset:0;z-index:4;background:linear-gradient(0deg,rgba(0,0,0,.45) 0,rgba(0,0,0,0) 20%)}}
.t{{right:64px;top:70px;text-align:right;font-family:'Josefin Sans',sans-serif;font-weight:300;font-size:{s}px;line-height:1.02;letter-spacing:3px;text-transform:uppercase;color:#3D6566}}"""
    words = "<br>".join(p["words"])
    body = p["ph"](0, "bgp") + '<div class="veil"></div><div class="shade"></div>' + f'<div class="title t">{words}</div>' + p["foot"](light=True)
    return css, body


def b_wave_split(p):
    s = p["fit"](600, 76, .5) if len(p["words"]) < 2 else min(76, int(600 / (max(len(w) for w in p["words"]) * .55)))
    wave = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 960 610' preserveAspectRatio='none'%3E"
            "%3Cpath d='M0 110 C130 0 350 0 480 110 S830 220 960 110 V610 H0Z'/%3E%3C/svg%3E")
    css = f""".frame{{position:absolute;inset:24px;border:1.5px solid var(--line);z-index:1}}
.t{{right:64px;top:54px;text-align:right;font-size:{s}px;font-weight:500;letter-spacing:3px;text-transform:uppercase;line-height:1.05}}
.w2{{-webkit-mask:url("{wave}") center/100% 100% no-repeat;mask:url("{wave}") center/100% 100% no-repeat}}"""
    words = "<br>".join(p["words"])
    body = ('<div class="frame"></div>' + f'<div class="title serif t">{words}</div>'
            + p["ph"](0, "", "left:60px;top:250px;width:960px;height:620px")
            + p["ph"](1, "w2", "left:60px;top:640px;width:960px;height:610px")
            + '<svg class="full" viewBox="0 0 1080 1350"><path d="M60 750 C190 640 410 640 540 750 S890 860 1020 750" fill="none" stroke="#FBF8F2" stroke-width="16"/>'
              '<path d="M60 742 C190 632 410 632 540 742 S890 852 1020 742" fill="none" stroke="#B8975F" stroke-width="4"/></svg>'
            + p["foot"]())
    return css, body


def b_swatch_overlay(p):
    longest = max(len(w) for w in p["words"])
    s = min(84, int(440 / (longest * .66)))
    css = f""".bgp{{inset:0}}
.sw{{left:0;top:0;width:580px;height:560px;z-index:3;box-shadow:0 18px 40px rgba(0,0,0,.28)}}
.sw::after{{content:"";position:absolute;inset:0;background:rgba(30,24,18,.5)}}
.shade{{position:absolute;inset:0;z-index:2;background:linear-gradient(0deg,rgba(0,0,0,.5) 0,rgba(0,0,0,0) 22%)}}
.t{{left:0;top:0;width:580px;height:560px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
  font-size:{s}px;font-weight:700;letter-spacing:3px;text-transform:uppercase;line-height:1.05;color:#E9CF94;text-shadow:0 3px 14px rgba(0,0,0,.6)}}
.foot{{text-align:right;color:#E9CF94}}"""
    words = "<br>".join(p["words"])
    body = (p["ph"](1, "bgp") + '<div class="shade"></div>' + p["ph"](0, "sw")
            + f'<div class="title serif t">{words}</div>' + p["foot"](light=True))
    return css, body


def b_two_up(p):
    s = p["fit"](980, 104, .44)
    css = f""".t{{left:40px;right:40px;top:46px;text-align:center;font-size:{s}px;font-weight:500}}
.l{{box-shadow:0 10px 30px rgba(0,0,0,.08)}}"""
    leaf = ('<svg class="full" viewBox="0 0 1080 1350"><path d="M540 1196 c-14 -16 -14 -34 0 -50 c14 16 14 34 0 50z M540 1196 c-22 -4 -34 -18 -36 -36 c20 2 34 16 36 36z'
            ' M540 1196 c22 -4 34 -18 36 -36 c-20 2 -34 16 -36 36z" fill="none" stroke="#B8975F" stroke-width="2.5"/></svg>')
    body = (f'<div class="title serif t">{p["title"]}</div>'
            + p["ph"](0, "contain l", "left:60px;top:190px;width:470px;height:930px")
            + p["ph"](1, "", "left:550px;top:190px;width:470px;height:930px")
            + leaf + p["foot"]())
    return css, body


def b_grid4(p):
    s = p["fit"](960, 80, .6)
    css = f""".t{{left:40px;right:40px;top:56px;text-align:center;font-size:{s}px;font-weight:600;letter-spacing:4px;text-transform:uppercase}}"""
    body = (f'<div class="title serif t">{p["title"]}</div>'
            + p["ph"](0, "", "left:64px;top:170px;width:420px;height:520px")
            + p["ph"](1, "", "left:496px;top:170px;width:520px;height:520px")
            + p["ph"](2, "", "left:64px;top:702px;width:560px;height:548px")
            + p["ph"](3, "", "left:636px;top:702px;width:380px;height:548px")
            + p["foot"]())
    return css, body


def b_frame_lines(p):
    s = p["fit"](880, 76, .66)
    css = f""".fr{{position:absolute;border:2px solid var(--line);z-index:1}}
.t{{left:40px;right:40px;top:1040px;text-align:center;font-family:'Montserrat',sans-serif;font-size:{s}px;font-weight:600;letter-spacing:2px;text-transform:uppercase}}
.dk{{background:#14213A}}"""
    body = ('<div class="fr" style="left:56px;top:110px;width:968px;height:1110px"></div>'
            '<div class="fr" style="left:76px;top:130px;width:928px;height:1070px;border-color:#E2D4B8"></div>'
            + p["ph"](0, "dk", "left:110px;top:170px;width:430px;height:600px")
            + p["ph"](1, "", "left:560px;top:70px;width:420px;height:910px")
            + f'<div class="title t">{p["title"]}</div>'
            + '<svg class="full" viewBox="0 0 1080 1350"><path d="M120 1010 H470 M610 1010 H960" stroke="#B8975F" stroke-width="2"/>'
              '<path d="M540 1022 c-10 -12 -10 -26 0 -38 c10 12 10 26 0 38z M540 1022 c-16 -3 -25 -13 -27 -27 c15 1 25 12 27 27z M540 1022 c16 -3 25 -13 27 -27 c-15 1 -25 12 -27 27z" fill="none" stroke="#B8975F" stroke-width="2"/></svg>'
            + p["foot"]())
    return css, body


def b_arch_band(p):
    """Title band, then two photos side by side, exactly 50% each (e.g. two colors of one product)."""
    s = p["fit"](960, 78, .62)
    css = f""".t{{left:40px;right:40px;top:50px;text-align:center;font-size:{s}px;font-weight:500;letter-spacing:4px;text-transform:uppercase}}
.rule{{position:absolute;left:300px;right:300px;top:{60 + s + 14}px;height:2px;background:var(--line)}}
.ao{{position:absolute;left:44px;top:174px;width:992px;height:1092px;border:2px solid var(--gold);border-bottom:0;border-radius:496px 496px 0 0;z-index:5}}
.mid{{position:absolute;left:537px;top:190px;width:6px;height:1060px;background:var(--bg);z-index:4}}"""
    body = (f'<div class="title serif t">{p["title"]}</div><div class="rule"></div>'
            + p["ph"](0, "", "left:60px;top:190px;width:480px;height:1060px;border-radius:480px 0 0 0")
            + p["ph"](1, "", "left:540px;top:190px;width:480px;height:1060px;border-radius:0 480px 0 0")
            + '<div class="mid"></div><div class="ao"></div>' + p["foot"]())
    return css, body


def b_full_bold(p):
    """Whole post is the photo, with a large italic title stacked bottom-left."""
    longest = max(len(w) for w in p["words"])
    s = min(190, int(900 / (longest * .5)))
    css = f""".bgp{{inset:0}}
.shade{{position:absolute;inset:0;z-index:4;background:linear-gradient(0deg,rgba(0,0,0,.62) 0,rgba(0,0,0,.25) 38%,rgba(0,0,0,0) 60%)}}
.t{{left:64px;right:64px;bottom:150px;font-family:'Playfair Display',Georgia,serif;font-style:italic;font-weight:500;font-size:{s}px;line-height:.98;color:#fff;text-shadow:0 4px 24px rgba(0,0,0,.4)}}
.rule{{position:absolute;left:68px;width:220px;bottom:122px;height:3px;background:#E2C88E;z-index:6}}
.foot{{text-align:left;left:68px}}"""
    words = "<br>".join(p["words"])
    body = (p["ph"](0, "bgp") + '<div class="shade"></div>' + f'<div class="title t">{words}</div><div class="rule"></div>'
            + p["foot"](light=True))
    return css, body


LAYOUTS_B = {f.__name__: f for f in (
    b_diagonal, b_grid_pill, b_full_serif, b_thumbs, b_fan, b_deco_panels, b_full_corner, b_full_light,
    b_wave_split, b_swatch_overlay, b_two_up, b_grid4, b_frame_lines, b_arch_band, b_full_bold)}
ORDER_B = list(LAYOUTS_B)
