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

# 月ごとの絵柄: (関数, x, y, 大きさ, 回転)。幅30×高さ10の枠に収める
THEME = {
    11: [(ginkgo, 5, 6.6, 4.6, -8), (momiji, 15.5, 5.6, 4.4, 8), (kaki, 25.5, 6.2, 3.3, None)],
}

def art(month):
    out = []
    for fn, x, y, r, rot in THEME[month]:
        out.append(fn(x, y, r) if rot is None else fn(x, y, r, rot))
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
