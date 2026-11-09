#!/usr/bin/env python3
"""月ごとのカレンダー・テンプレート(content/sheets/cal-<月2桁>.html)を作る。
使い方: python3 tools/make_calendar.py 11 [既定の年]
日付の部分は、公開ページで年を選ぶと static/site.js が作り直す。ここで作るのは、JSなしでも見える既定の年の表。
月ごとの絵柄は THEME に足す。"""
import calendar, math, sys
from pathlib import Path

M = int(sys.argv[1]); Y = int(sys.argv[2]) if len(sys.argv) > 2 else 2026
S = 'stroke="#111" stroke-width=".35" stroke-linejoin="round" stroke-linecap="round" fill="#fff"'
N = 'stroke="#111" stroke-width=".25" stroke-linecap="round" fill="none"'

def momiji(x, y, R, rot=0):
    pts = []
    for k in range(5):
        base = -90 + 72 * k
        for da, rr in ((-36, .32), (-17, .68), (0, 1.0), (17, .68)):
            a = math.radians(base + da); pts.append((R * rr * math.cos(a), R * rr * math.sin(a)))
    d = "M" + " L".join("%.2f %.2f" % p for p in pts) + "Z"
    v = "".join("M0 0 L%.2f %.2f" % (R * .85 * math.cos(math.radians(-90 + 72 * k)), R * .85 * math.sin(math.radians(-90 + 72 * k))) for k in range(5))
    return '<g transform="translate(%s %s) rotate(%s)"><path d="%s" %s/><path d="%s" %s/><path d="M0 0 L0 %.2f" %s/></g>' % (x, y, rot, d, S, v, N, R * 1.3, N)

def ginkgo(x, y, R, rot=0):
    d = "M0 0 L%.2f %.2f Q%.2f %.2f %.2f %.2f Q%.2f %.2f 0 %.2f Q%.2f %.2f %.2f %.2f Q%.2f %.2f %.2f %.2f Z" % (
        -R, -R * .8, -R * 1.15, -R * 1.35, -R * .55, -R * 1.3, -R * .2, -R * 1.15, -R * .95, R * .2, -R * 1.15, R * .55, -R * 1.3, R * 1.15, -R * 1.35, R, -R * .8)
    v = "".join("M0 0 L%.2f %.2f" % (R * t, -R * 1.05) for t in (-.7, -.35, 0, .35, .7))
    return '<g transform="translate(%s %s) rotate(%s)"><path d="%s" %s/><path d="%s" %s/><path d="M0 0 L0 %.2f" %s/></g>' % (x, y, rot, d, S, v, N, R * .7, N)

def kaki(x, y, R):
    d = "M%s 0 C%s %.2f %.2f %.2f 0 %.2f C%.2f %.2f %s %.2f %s 0 C%s %.2f %.2f %s 0 %s C%.2f %s %s %.2f %s 0Z" % (
        -R, -R, -R * .9, -R * .5, -R, -R * .9, R * .5, -R, R, -R * .9, R, R, R * .9, R * .5, R, R, -R * .5, R, -R, R * .9, -R)
    cal = "M%.2f %.2f L%.2f %.2f L0 %.2f L%.2f %.2f L%.2f %.2f L%.2f %.2f L%.2f %.2f Z" % (
        -R * .55, -R * .85, -R * .2, -R * .55, -R * .95, R * .2, -R * .55, R * .55, -R * .85, R * .4, -R * .4, -R * .4, -R * .4)
    return '<g transform="translate(%s %s)"><path d="%s" %s/><path d="%s" %s/><path d="M0 %.2f L%.2f %.2f" %s/></g>' % (x, y, d, S, cal, S, -R * .95, R * .2, -R * 1.35, N)

# ---- 月ごとの絵柄(すべて自作。原点まわりの約±4.5の大きさで描き、THEMEで位置と大きさを決める) ----
def P(d, cls=S): return '<path d="%s" %s/>' % (d, cls)
def C(x, y, r, cls=S): return '<circle cx="%s" cy="%s" r="%s" %s/>' % (x, y, r, cls)
def E(x, y, rx, ry, cls=S, rot=0): return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" transform="rotate(%s %s %s)" %s/>' % (x, y, rx, ry, rot, x, y, cls)
def G(x, y, s, rot, body): return '<g transform="translate(%s %s) rotate(%s) scale(%s)">%s</g>' % (x, y, rot, s, body)
NOFILL = S.replace('fill="#fff"', 'fill="none"')

def m_kagamimochi():
    return E(0, 2.4, 4.2, 1.8) + E(0, .3, 3.0, 1.5) + C(0, -1.9, 1.4) + P("M0 -3.3 Q1.8 -4.6 2.8 -3.6 Q1.6 -2.8 0 -3.3Z") + P("M-2.6 -.3 Q0 .5 2.6 -.3", N)
def m_pine():
    o = P("M-3.6 4.2 Q0 0 3.4 -4.4", NOFILL)
    for t in (0.0, .25, .5, .75):
        x = -3.6 + 7 * t * .98; y = 4.2 - 8.6 * t
        o += P("M%.2f %.2f l-2.2 -1.4 M%.2f %.2f l-2.4 .2 M%.2f %.2f l2.0 -1.8 M%.2f %.2f l2.2 -.2" % ((x, y) * 4), N)
    return o

def m_daruma():
    return E(0, 0, 3.6, 4.2) + E(0, -.6, 2.3, 1.9) + C(-.9, -.7, .35, 'fill="#111"') + C(.9, -.7, .35, 'fill="#111"') + P("M-1.8 -2.5 Q-1.2 -2.9 -.4 -2.5 M.4 -2.5 Q1.2 -2.9 1.8 -2.5", N) + P("M-1.4 2.0 Q0 3.2 1.4 2.0", N)

def m_oni():
    return (P("M-2.6 -2.4 L-3.2 -5 L-1.2 -3.4Z M2.6 -2.4 L3.2 -5 L1.2 -3.4Z") + C(0, 0, 3.8) + P("M-2.4 -.8 L-.8 -1.4 M2.4 -.8 L.8 -1.4", N) +
            C(-1.5, -.2, .4, 'fill="#111"') + C(1.5, -.2, .4, 'fill="#111"') + P("M-1.8 1.6 Q0 2.8 1.8 1.6", N) + P("M-1.0 1.9 L-.7 2.8 L-.3 2.1 M.3 2.1 L.7 2.8 L1.0 1.9", N))
def m_mame():
    return E(-2, 1.5, 1.3, .9, rot=-30) + E(1.5, -1.5, 1.3, .9, rot=20) + E(2.2, 2.4, 1.3, .9, rot=60) + E(-1.2, -2.6, 1.3, .9, rot=-10)
def flower5(R, notch=False):
    o = ""
    for k in range(5):
        if notch:
            o += '<path d="M0 0 C%.2f %.2f %.2f %.2f %.2f %.2f L0 %.2f L%.2f %.2f C%.2f %.2f %.2f %.2f 0 0Z" transform="rotate(%d)" %s/>' % (
                -R * .55, -R * .3, -R * .6, -R * 1.0, -R * .2, -R * 1.0, -R * .82, R * .2, -R * 1.0, R * .6, -R * 1.0, R * .55, -R * .3, 72 * k, S)
        else:
            o += E(0, -R * .58, R * .42, R * .45, rot=0).replace('rotate(0 0 %s)' % (-R * .58), 'rotate(%d 0 0)' % (72 * k))
    return o + C(0, 0, R * .2, 'fill="#111"')

def m_ume(): return flower5(4.2)
def m_momo(): return flower5(4.4, True)
def m_sakura(): return flower5(4.6, True)
def m_hishimochi():
    o = ""
    for y in (-2.9, 0, 2.9): o += P("M0 %.1f L3.2 %.1f L0 %.1f L-3.2 %.1f Z" % (y - 1.9, y, y + 1.9, y))
    return o
def m_tulip():
    return P("M0 4.5 L0 .8", NOFILL) + P("M0 3.8 Q3.2 3.4 3 .8 Q1.2 1.2 0 3.8Z") + P("M-2.6 -1 Q-2.6 2 0 2.4 Q2.6 2 2.6 -1 L1.3 .3 L0 -1.8 L-1.3 .3Z")
def m_butterfly():
    return E(-1.9, -1.4, 2.0, 1.6, rot=-25) + E(1.9, -1.4, 2.0, 1.6, rot=25) + E(-1.5, 1.6, 1.4, 1.2, rot=25) + E(1.5, 1.6, 1.4, 1.2, rot=-25) + E(0, 0, .5, 2.6, 'fill="#111" stroke="#111" stroke-width=".2"') + P("M-.2 -2.4 Q-1 -3.8 -1.8 -3.8 M.2 -2.4 Q1 -3.8 1.8 -3.8", N)
def m_koinobori():
    return (P("M-4.6 -4.2 L-4.6 4.6", NOFILL) + P("M-3.6 0 C-3.6 -2.3 1.4 -2.7 3 0 C1.4 2.7 -3.6 2.3 -3.6 0Z") + P("M3 0 L5 -1.7 L5 1.7Z") + C(-2, -.5, .45, 'fill="#111"') +
            P("M-.4 -1.6 Q.6 0 -.4 1.6 M1.2 -1.4 Q2 0 1.2 1.4", N) + P("M-4.6 -4.2 L-3 -3.8 L-4.6 -3.2", N))
def m_ayame():
    return P("M0 4.5 Q-.5 0 .4 -3 M.8 4.5 Q1.8 1 2.6 -2", NOFILL) + P("M-2.4 -1.4 Q-.6 -3.6 .4 -1.2 Q-1 -.2 -2.4 -1.4Z") + P("M3.2 -.6 Q1.6 -3.4 .4 -1.2 Q1.8 .2 3.2 -.6Z") + P("M-.6 -1 Q.4 -4.4 1.4 -1 Q.4 .4 -.6 -1Z")
def m_ajisai():
    o = ""
    for x, y in ((0, 0), (-2.6, -1.3), (2.6, -1.3), (-2.6, 1.9), (2.6, 1.9), (0, -3.0), (0, 3.2)):
        o += "".join(C(x + dx, y + dy, .72) for dx, dy in ((0, -.55), (.55, 0), (0, .55), (-.55, 0)))
    return o

def m_katatsumuri():
    return P("M-4.3 3.6 Q-3 3.0 -1 3.4 L3.4 3.4 Q4.4 3.4 4.4 2.4 L4.4 1.6 Q5.6 .6 5 -.8 M4.4 1.6 Q3.6 -.2 4 -1.8", NOFILL) + C(0, .4, 3.0) + P("M0 .4 m0 0 q1 -.8 1.4 0 q.2 1.4 -1.6 1.6 q-2.0 -.2 -1.8 -2.2 q.8 -2 2.8 -1.4", N)
def m_teruteru():
    return C(0, -2.3, 1.8) + P("M-1.4 -.8 Q-3.6 3.8 -2.2 4.4 Q-1 3.6 0 4.4 Q1 3.6 2.2 4.4 Q3.6 3.8 1.4 -.8Z") + P("M-1.2 -.5 Q0 .5 1.2 -.5", N) + C(-.7, -2.5, .25, 'fill="#111"') + C(.7, -2.5, .25, 'fill="#111"')
def m_kasa():
    return P("M-4.4 0 Q-4 -4.2 0 -4.4 Q4 -4.2 4.4 0 Q3 -1 1.5 0 Q0 -1 -1.5 0 Q-3 -1 -4.4 0Z") + P("M0 -4.4 L0 3 Q0 4.4 -1.4 4.4", NOFILL) + P("M-1.5 0 Q-1 -2 0 -4.4 M1.5 0 Q1 -2 0 -4.4", N)
def star5(R, r=None):
    r = r or R * .45
    pts = []
    for k in range(10):
        a = math.radians(-90 + 36 * k); rr = R if k % 2 == 0 else r
        pts.append("%.2f %.2f" % (rr * math.cos(a), rr * math.sin(a)))
    return P("M" + " L".join(pts) + "Z")
def m_star(): return star5(4.2)
def m_sasa():
    leaves = "".join(P("M0 0 Q%.1f %.1f %.1f %.1f Q%.1f %.1f 0 0Z" % (dx * .5, dy * .1 - 1.2, dx, dy, dx * .5, dy * .1 + 1.2), S) for dx, dy in ((3.6, -1.6), (-3.6, -1.0)))
    return P("M-.5 4.6 Q0 0 .8 -4.6", NOFILL) + G(0, 1.4, 1, 0, leaves) + G(.2, -1.8, 1, 0, leaves) + P("M2.8 -1 L2.8 -.6", N)
def m_tanzaku():
    return P("M-1.2 -4.4 L-1.2 -3.4", N) + '<rect x="-1.6" y="-3.4" width="3.2" height="7.6" %s/>' % S + P("M0 -2.2 L0 -.8 M0 .2 L0 1.6", N)
def m_himawari():
    o = "".join(E(0, -3.0, 1.0, 1.6, rot=0).replace('rotate(0 0 -3.0)', 'rotate(%d 0 0)' % (30 * k)) for k in range(12))
    return o + C(0, 0, 2.1) + "".join(C(.9 * math.cos(a), .9 * math.sin(a), .22, 'fill="#111"') for a in (0, 2.1, 4.2)) + C(0, 0, .22, 'fill="#111"')
def m_suika():
    return (P("M-4.4 -1.8 A4.4 4.4 0 0 0 4.4 -1.8 Z") + P("M-3.4 -1.8 A3.4 3.4 0 0 0 3.4 -1.8 Z", N) + E(-1.5, .2, .4, .7, 'fill="#111"') + E(0, 1.3, .4, .7, 'fill="#111"') + E(1.5, .2, .4, .7, 'fill="#111"'))
def m_asagao():
    V = [(3.0 * math.cos(math.radians(-90 + 36 + 72 * k)), 3.0 * math.sin(math.radians(-90 + 36 + 72 * k))) for k in range(5)]
    d = "M%.2f %.2f " % V[0] + "".join("A2.7 2.7 0 0 1 %.2f %.2f " % V[(k + 1) % 5] for k in range(5)) + "Z"
    return P(d) + "".join(P("M0 0 L%.2f %.2f" % v, N) for v in V) + C(0, 0, 1.1) + C(0, 0, .3, 'fill="#111"')

def m_tsuki():
    return P("M1.6 -4.4 A4.6 4.6 0 1 0 1.6 4.4 A3.6 3.6 0 1 1 1.6 -4.4Z")
def m_dango():
    o = '<rect x="-4" y="3.6" width="8" height="1.2" %s/>' % S
    for x in (-2.2, 0, 2.2): o += C(x, 2.2, 1.1)
    for x in (-1.1, 1.1): o += C(x, .1, 1.1)
    return o + C(0, -2.0, 1.1)
def m_susuki():
    o = P("M-1.2 4.6 Q3 2 4.4 -.8", NOFILL)
    o += P("M-1 4.6 Q0 0 2 -3.2", NOFILL) + P("M-2 4.6 Q-2.5 1 -3.6 -1.4", NOFILL)
    o += E(2.6, -3.6, .8, 2.0, rot=35) + E(-3.9, -2.6, .7, 1.7, rot=-15)
    o += P("M2.2 -5 L3.2 -2.4 M2.9 -5.2 L3.4 -3.4 M-4.2 -4 L-3.8 -1.6", N)
    return o

def m_donguri():
    return (P("M0 4.6 Q-2.8 2.8 -3 -.4 L3 -.4 Q2.8 2.8 0 4.6Z") + P("M-3.6 -.2 Q-3.6 -3.4 0 -3.6 Q3.6 -3.4 3.6 -.2Z") + P("M-2.6 -2.4 L-1.2 -.2 M0 -3.4 L0 -.2 M2.6 -2.4 L1.2 -.2", N) + P("M0 -3.6 L.4 -4.6", N))
def m_pumpkin():
    return (E(0, .6, 4.4, 3.5) + P("M0 -2.8 L.5 -4.4 L1.4 -4.5", S) + P("M-2.6 -2.6 Q-3.9 .6 -2.6 3.6 M2.6 -2.6 Q3.9 .6 2.6 3.6", N) +
            P("M-2.4 -.2 L-1.2 -1.4 L-.2 -.2Z M.2 -.2 L1.2 -1.4 L2.4 -.2Z", 'fill="#111" stroke="#111" stroke-width=".2"') + P("M-2.0 1.4 L-1.0 2.4 L0 1.4 L1.0 2.4 L2.0 1.4", N))

def m_kuri():
    return P("M0 -3.6 Q3.8 -1 3.6 2 Q3 4.4 0 4.4 Q-3 4.4 -3.6 2 Q-3.8 -1 0 -3.6Z") + P("M-3.2 2.6 Q0 1 3.2 2.6", N) + P("M-.6 -3 L0 -4.4 L.6 -3", S) + P("M-1.4 3.4 L-1.4 4 M0 3 L0 4 M1.4 3.4 L1.4 4", N)
def m_tree():
    return P("M0 -4.6 L2.2 -1.4 L1 -1.4 L3.2 1.6 L1.6 1.6 L4 4 L-4 4 L-1.6 1.6 L-3.2 1.6 L-1 -1.4 L-2.2 -1.4Z") + '<rect x="-.8" y="4" width="1.6" height="1" %s/>' % S + C(-1.4, 2.4, .35, 'fill="#111"') + C(1.2, .2, .35, 'fill="#111"') + C(-.3, -2.2, .3, 'fill="#111"')
def m_snow():
    arm = "M0 0 L0 -4.4 M0 -2.6 L-1.2 -3.6 M0 -2.6 L1.2 -3.6 M0 -1.2 L-.9 -2.0 M0 -1.2 L.9 -2.0"
    return "".join(P(arm, NOFILL).replace('d="', 'transform="rotate(%d)" d="' % (60 * k), 1) for k in range(6))
def m_gift():
    return ('<rect x="-3.4" y="-1.4" width="6.8" height="5.2" %s/>' % S + '<rect x="-3.8" y="-2.8" width="7.6" height="1.6" %s/>' % S + P("M0 -2.8 L0 3.8 M-3.4 .6 L3.4 .6", N) +
            P("M0 -2.8 Q-3 -5 -3.4 -3.4 Q-3 -2.6 0 -2.8 Q3 -5 3.4 -3.4 Q3 -2.6 0 -2.8Z"))
def m_ginkgo(): return ginkgo(0, 1.6, 4.6, -8)
def m_momiji(): return momiji(0, 0, 4.4, 8)
def m_kaki(): return kaki(0, .4, 3.6)

# (関数, x, y, 大きさ(1=原寸), 回転)。30×10の枠に3つ並べる
def T(*fns, ys=(5, 5, 5), ss=(1, 1, 1)):
    return [(f, 5 + 10 * i, ys[i], ss[i], 0) for i, f in enumerate(fns)]
THEME = {
    1: T(m_pine, m_kagamimochi, m_daruma, ss=(.68, .95, .95)),
    2: T(m_oni, m_mame, m_ume, ss=(.95, .95, .95)),
    3: T(m_hishimochi, m_momo, m_tulip, ss=(.95, .95, .9)),
    4: T(m_sakura, m_butterfly, m_tulip, ss=(.95, .95, .9)),
    5: T(m_koinobori, m_ayame, m_koinobori, ss=(.95, .95, .8)),
    6: T(m_ajisai, m_katatsumuri, m_kasa, ss=(.95, .9, .9)),
    7: T(m_sasa, m_tanzaku, m_star, ss=(.95, .95, .9)),
    8: T(m_himawari, m_suika, m_asagao, ss=(.95, .95, 1.15)),
    9: T(m_tsuki, m_dango, m_susuki, ss=(.95, .95, .78)),
    10: T(m_donguri, m_pumpkin, m_kuri, ss=(.95, .9, .95)),
    11: T(m_ginkgo, m_momiji, m_kaki, ys=(5.3, 5, 5), ss=(.85, .82, .95)),
    12: T(m_tree, m_snow, m_gift, ss=(.95, .95, .95)),
}

def art(month):
    out = []
    for fn, x, y, sc, rot in THEME[month]:
        out.append(G(x, y, sc, rot, fn()))
    return '<svg viewBox="0 0 30 10" aria-hidden="true">%s</svg>' % "".join(out)

# 日付の表は static/site.js と同じ決まりで作る(日曜はじまり)
WD = ["にち", "げつ", "か", "すい", "もく", "きん", "ど"]
AVAIL = 42.0  # 1つの表の、曜日の行をのぞいた高さの目安(cqw)。マスの一辺 = min(12.28, AVAIL / 行数)

def grid(y, m):
    weeks = calendar.Calendar(firstweekday=6).monthdayscalendar(y, m)
    c = min(86 / 7, AVAIL / len(weeks))
    cells = "".join('<div class="cw">%s</div>' % w for w in WD)
    for wk in weeks:
        cells += "".join('<div class="cd"><b>%d</b></div>' % d if d else '<div class="cd"></div>' for d in wk)
    return c, cells

c, cells = grid(Y, M)
def block(k):
    return ('<div class="cb"><div class="cbw"><div class="ch"><input class="in nm" type="text" maxlength="8" data-k="calname%d" placeholder="なまえ" aria-label="なまえ(%d人目)" autocomplete="off">%s</div>'
            '<div class="cg">%s</div></div></div>') % (k, k, art(M), cells)
html = ('<div class="sh"><h2><span data-cal-title>%d年 %d月</span></h2>'
        '<div class="cal" data-cal-month="%d" data-cal-year="%d" style="--c:%.3f">%s%s</div></div>') % (Y, M, M, Y, c, block(1), block(2))
Path(__file__).resolve().parent.parent.joinpath("content/sheets/cal-%02d.html" % M).write_text(html, encoding="utf8")
print("rows", len(calendar.Calendar(6).monthdayscalendar(Y, M)), "c=%.2f" % c)
