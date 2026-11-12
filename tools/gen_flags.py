#!/usr/bin/env python3
"""国旗のぬりえ(a-flag-*)と なぞりがき(t-flag-*)の断片を作る。 python3 tools/gen_flags.py"""
import math, json, os
X0, Y0, W, H = 9.0, 0.0, 87.0, 58.0
f = lambda v: ('%.2f' % v).rstrip('0').rstrip('.')

class K:
    def __init__(s, mode, sid): s.mode, s.sid, s.out = mode, sid, []
    def add(s, tag, attrs, thin=False, nofill=False, solid=False, raw=''):
        if s.mode == 'art':
            c = ' '.join(x for x in ['th' if thin else '', 'nf' if nofill else ''] if x)
            extra = f' class="{c}"' if c else ''
        else:
            st = 'fill:none' if nofill else 'fill:#fff'
            if solid: st += ';stroke-width:.5;stroke-dasharray:none'
            elif thin: st += ';stroke-width:.9;stroke-dasharray:1.5 1.3'
            extra = f' style="{st}"'
        s.out.append(f'<{tag} {attrs}{extra}>{raw}</{tag}>')
    def poly(s, pts, **k): s.add('path', 'd="M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts) + ' Z"', **k)
    def line(s, pts, **k): s.add('path', 'd="M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts) + '"', nofill=True, **k)
    def rect(s, x, y, w, h, **k): s.add('rect', f'x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"', **k)
    def circle(s, cx, cy, r, **k): s.add('circle', f'cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}"', **k)
    def star(s, cx, cy, R, n=5, ratio=0.382, rot=-90.0, **k):
        pts = []
        for i in range(2 * n):
            a = math.radians(rot + i * 180.0 / n); r = R if i % 2 == 0 else R * ratio
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        s.poly(pts, **k)

def frame(k): k.rect(X0, Y0, W, H, nofill=True)

def union_jack(k, x, y, w, h, thin=True):
    u = h / 30.0; cx, cy = x + w / 2, y + h / 2; L = math.hypot(w, h); far = L
    cid = 'uj-' + k.sid
    k.out.append(f'<clipPath id="{cid}"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"></rect></clipPath><g clip-path="url(#{cid})">')
    d1 = (w / L, h / L); n1 = (-h / L, w / L)      # 左上→右下。n1 は左下むき
    d2 = (w / L, -h / L); m2 = (-h / L, -w / L)    # 左下→右上。m2 は左上むき
    for d, n in ((d1, n1), (d2, m2)):               # 白い斜め帯
        k.poly([(cx - d[0]*far + n[0]*3*u, cy - d[1]*far + n[1]*3*u), (cx + d[0]*far + n[0]*3*u, cy + d[1]*far + n[1]*3*u),
                (cx + d[0]*far - n[0]*3*u, cy + d[1]*far - n[1]*3*u), (cx - d[0]*far - n[0]*3*u, cy - d[1]*far - n[1]*3*u)], thin=thin)
    arms = [((-d1[0], -d1[1]), n1), (d1, (-n1[0], -n1[1])), (d2, m2), ((-d2[0], -d2[1]), (-m2[0], -m2[1]))]
    for a, sgn in arms:                             # 赤い斜め帯(風車の形)
        k.poly([(cx, cy), (cx + a[0]*far, cy + a[1]*far), (cx + a[0]*far + sgn[0]*2*u, cy + a[1]*far + sgn[1]*2*u), (cx + sgn[0]*2*u, cy + sgn[1]*2*u)], thin=thin)
    for hw in (5 * u, 3 * u):                       # 白い十字、赤い十字
        k.poly([(cx - hw, y - 1), (cx + hw, y - 1), (cx + hw, cy - hw), (x + w + 1, cy - hw), (x + w + 1, cy + hw), (cx + hw, cy + hw),
                (cx + hw, y + h + 1), (cx - hw, y + h + 1), (cx - hw, cy + hw), (x - 1, cy + hw), (x - 1, cy - hw), (cx - hw, cy - hw)], thin=thin)
    k.out.append('</g>')

def us(k):
    cw, ch, sh = 0.4 * W, H * 7 / 13, H / 13
    for i in range(1, 13):
        k.line([(X0 + (cw if i < 7 else 0), Y0 + i * sh), (X0 + W, Y0 + i * sh)], thin=True)
    k.rect(X0, Y0, cw, ch)
    for j in range(1, 10):
        for i in range(1, 12):
            if (i + j) % 2 == 0: k.star(X0 + cw * i / 12, Y0 + ch * j / 10, 0.4 * sh * 1.15, thin=True, solid=True)
    frame(k)
def cn(k):
    u = W / 30; bc = (X0 + 5 * u, Y0 + 5 * u); k.star(*bc, 3 * u)
    for gx, gy in ((10, 2), (12, 4), (12, 7), (10, 9)):
        c = (X0 + gx * u, Y0 + gy * u); rot = math.degrees(math.atan2(bc[1] - c[1], bc[0] - c[0]))
        k.star(*c, u, rot=rot, thin=True)
    frame(k)
def kr(k):
    cx, cy, r = X0 + W / 2, Y0 + H / 2, H / 4; th = math.atan2(2, 3)
    d = (math.cos(th), math.sin(th)); n = (-d[1], d[0])
    k.circle(cx, cy, r)
    pts = []
    for sg, c in ((1, (cx - d[0]*r/2, cy - d[1]*r/2)), (-1, (cx + d[0]*r/2, cy + d[1]*r/2))):
        for i in range(0, 25):
            p = math.pi * i / 24
            pts.append((c[0] + r/2 * (-math.cos(p)*d[0] + sg*math.sin(p)*n[0]), c[1] + r/2 * (-math.cos(p)*d[1] + sg*math.sin(p)*n[1])))
    k.line(pts)
    D = 2 * r; bw, gap, bl = D / 12, D / 24, D / 2; dist = r + D / 4 + (3 * bw + 2 * gap) / 2
    # 左上 ☰、右上 ☵、左下 ☲、右下 ☷(外がわから順に。0=つながった棒 1=切れた棒)
    for (sx, sy), bars in (((-1, -1), (0, 0, 0)), ((1, -1), (1, 0, 1)), ((-1, 1), (0, 1, 0)), ((1, 1), (1, 1, 1))):
        a = (sx * d[0], sy * d[1]); p = (-a[1], a[0])
        for bi, broken in enumerate(bars):
            off = dist + (1 - bi) * (bw + gap)
            c = (cx + a[0] * off, cy + a[1] * off)
            segs = [(-bl/2, -gap/2), (gap/2, bl/2)] if broken else [(-bl/2, bl/2)]
            for s0, s1 in segs:
                if k.mode == 'art':
                    k.poly([(c[0] + p[0]*s0 + a[0]*bw/2, c[1] + p[1]*s0 + a[1]*bw/2), (c[0] + p[0]*s1 + a[0]*bw/2, c[1] + p[1]*s1 + a[1]*bw/2),
                            (c[0] + p[0]*s1 - a[0]*bw/2, c[1] + p[1]*s1 - a[1]*bw/2), (c[0] + p[0]*s0 - a[0]*bw/2, c[1] + p[1]*s0 - a[1]*bw/2)], thin=True)
                else:
                    k.line([(c[0] + p[0]*s0, c[1] + p[1]*s0), (c[0] + p[0]*s1, c[1] + p[1]*s1)])
    frame(k)
def au(k):
    union_jack(k, X0, Y0, W / 2, H / 2); k.rect(X0, Y0, W / 2, H / 2, nofill=True)
    k.star(X0 + W / 4, Y0 + H * 0.75, 0.15 * H, n=7, ratio=4/9)
    fx, fy, q = X0 + W * 0.75, Y0 + H / 2, 0.75
    for dx, dy, dia, n in ((0, 0.5 - 1/6, 1/7, 7), (-0.25, -1/16, 1/7, 7), (0, -(0.5 - 1/6), 1/7, 7), (2/9, -31/240, 1/7, 7), (0.1, 1/24, 1/12, 5)):
        k.star(fx + dx * H * q, fy + dy * H, dia * H / 2, n=n, ratio=4/9 if n == 7 else 0.382, thin=True)
    frame(k)
def th_(k):
    for i in (1, 2, 4, 5): k.line([(X0, Y0 + H * i / 6), (X0 + W, Y0 + H * i / 6)])
    frame(k)
def vn(k): k.star(X0 + W / 2, Y0 + H / 2, 0.3 * H); frame(k)
def id_(k): k.line([(X0, Y0 + H / 2), (X0 + W, Y0 + H / 2)]); frame(k)
def de(k):
    for i in (1, 2): k.line([(X0, Y0 + H * i / 3), (X0 + W, Y0 + H * i / 3)])
    frame(k)
def fr(k):
    for i in (1, 2): k.line([(X0 + W * i / 3, Y0), (X0 + W * i / 3, Y0 + H)])
    frame(k)
def gb(k): union_jack(k, X0, Y0, W, H, thin=False); frame(k)

FLAGS = [
 ('us', 'アメリカ', us, 'あか・しろ・あお', 'しまは あかと しろ。ほしの まわりは あお'),
 ('cn', 'ちゅうごく', cn, 'あか・きいろ', 'ほしは きいろ。まわりは あか'),
 ('kr', 'かんこく', kr, 'しろ・あか・あお・くろ', 'まるの うえは あか、したは あお。ぼうは くろ'),
 ('au', 'オーストラリア', au, 'あお・しろ・あか', 'ほしは しろ。まわりは あお'),
 ('th', 'タイ', th_, 'あか・しろ・あお', 'うえから あか・しろ・あお・しろ・あか'),
 ('vn', 'ベトナム', vn, 'あか・きいろ', 'ほしは きいろ。まわりは あか'),
 ('id', 'インドネシア', id_, 'あか・しろ', 'うえは あか、したは しろ'),
 ('de', 'ドイツ', de, 'くろ・あか・きいろ', 'うえから くろ・あか・きいろ'),
 ('fr', 'フランス', fr, 'あお・しろ・あか', 'ひだりから あお・しろ・あか'),
 ('gb', 'イギリス', gb, 'あお・しろ・あか', 'じゅうじと ななめの ほそい おびは あか。|さんかくは あお'),
]

def build(mode, code, name, fn, guide):
    sid = ('a' if mode == 'art' else 't') + '-flag-' + code
    k = K(mode, sid)
    k.rect(4.5, -3, 4.5, 109); k.circle(6.75, -5.5, 3.2)      # ポール
    k.line([(0, 106), (100, 106)])
    fn(k)
    fs = 13 if len(name) <= 5 else 10.5
    if mode == 'art':
        k.out.append(f'<text x="54" y="82" text-anchor="middle" font-size="{fs}" font-weight="700" style="stroke-width:.6">{name}</text>')
        for gi, gl in enumerate(guide.split('|')):
            k.out.append(f'<text x="54" y="{94 + gi * 6}" text-anchor="middle" font-size="3.9" style="fill:#333;stroke:none">{gl}</text>')
        title, small, cls = f'ぬりえ こっき({name})', 'いろを ぬろう', 'art-svg'
    else:
        k.out.append(f'<text x="54" y="84" text-anchor="middle" font-size="{fs}" font-weight="700" style="stroke-width:.6;stroke-dasharray:1.3 1">{name}</text>')
        k.out.append(f'<circle class="st" cx="{f(X0)}" cy="{f(Y0)}" r="2"></circle>')
        title, small, cls = f'なぞりがき こっき({name})', 'なぞろう', 'trace-svg'
    html = (f'<div class="sh"><h2>{title}<small>{small}</small></h2><div class="art"><svg class="{cls}" viewBox="0 -10 100 120" role="img" '
            f'aria-label="{title}">{"".join(k.out)}</svg></div><div class="foot"><span>なまえ</span><i></i></div></div>\n')
    return sid, title, html

if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(root, 'data', 'sheets.json'); data = json.load(open(p, encoding='utf-8')); have = {x['id'] for x in data['sheets']}
    for mode, tab in (('art', 'art'), ('trace', 'trace')):
        for code, name, fn, colors, guide in FLAGS:
            sid, title, html = build(mode, code, name, fn, guide)
            open(os.path.join(root, 'content', 'sheets', sid + '.html'), 'w', encoding='utf-8').write(html)
            if sid not in have:
                idx = max(i for i, x in enumerate(data['sheets']) if x['tab'] == tab)
                desc = f'国旗・{colors}' if mode == 'art' else 'てんせんをなぞる・国旗'
                data['sheets'].insert(idx + 1, {'id': sid, 'tab': tab, 'title': title, 'desc': desc, 'added': os.environ.get('ADDED', '2026-11-12')})
    json.dump(data, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
