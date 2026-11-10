#!/usr/bin/env python3
"""アルファベットのシート(つなごう・ぬけたもじ・めいろ・ビンゴ)を作る。乱数は固定(毎回同じ結果)。
名前入りなぞりがき(abc-name)は、固定の枠だけここで作り、中身は static/site.js が入力に合わせて作る。"""
import random, string
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "content/sheets"
U = string.ascii_uppercase; L = string.ascii_lowercase
HEAD = '<div class="sh abc"><h2>%s<small>%s</small></h2>%s%s</div>'
NM = '<div class="nmline"><span>なまえ</span><i></i></div>'

def write(sid, title, sub, body, nm=True):
    (OUT / (sid + ".html")).write_text(HEAD % (title, sub, NM if nm else "", body), encoding="utf8")

# 0. 名前入りなぞりがき(枠だけ)
write("abc-name", "なまえ アルファベット", "うすい もじを なぞろう", '<p class="empty">お名前をローマ字で入力すると、ここになぞり書きの練習が作られます。</p>')

# 1. 大文字と小文字 つなごう A〜M
perm = [6, 2, 10, 0, 8, 4, 12, 1, 9, 5, 11, 3, 7]   # 右の列に並べる小文字(0=a)
n = 13; dy = 7.4; y0 = 5.5
s = ['<svg class="mt" viewBox="0 0 86 100" role="img" aria-label="大文字と小文字をつなぐシート" style="flex:1;min-height:0;width:100%;font-family:var(--f-abc)">']
ay = lambda i: y0 + dy * i
for i in range(n):
    s.append('<text x="12" y="%.1f" font-size="6" font-weight="700" text-anchor="middle" dominant-baseline="central">%s</text>' % (ay(i), U[i]))
    s.append('<circle cx="23" cy="%.1f" r="1.3" fill="#fff" stroke="#111" stroke-width=".35"/>' % ay(i))
    s.append('<text x="74" y="%.1f" font-size="6" font-weight="700" text-anchor="middle" dominant-baseline="central">%s</text>' % (ay(i), L[perm[i]]))
    s.append('<circle cx="63" cy="%.1f" r="1.3" fill="#fff" stroke="#111" stroke-width=".35"/>' % ay(i))
ex = perm.index(0)  # a は右の何番目か
s.append('<line x1="23" y1="%.1f" x2="63" y2="%.1f" stroke="#999" stroke-width=".6" stroke-linecap="round"/>' % (ay(0), ay(ex)))
s.append('<text x="43" y="%.1f" font-size="2.6" fill="#777" text-anchor="middle">れい</text>' % (ay(0) + (ay(ex) - ay(0)) / 2 - 1.8 + 0.0))
s.append('</svg>')
write("abc-match", "おおもじと こもじ", "おなじ もじを せんで つなごう(A〜M)", "".join(s))

# 2. ぬけた もじ
blank_u = {2, 5, 8, 11, 13, 16, 19, 22, 24}; blank_l = {1, 4, 7, 10, 14, 17, 20, 23, 25}
def grid(chars, blanks):
    return '<div class="ms">%s</div>' % "".join('<div class="mc%s">%s</div>' % (" q" if i in blanks else "", "" if i in blanks else c) for i, c in enumerate(chars))
body = '<p class="lab">おおもじ</p>%s<p class="lab">こもじ</p>%s' % (grid(U, blank_u), grid(L, blank_l))
write("abc-missing", "ぬけた もじ", "ならびを みて、あいた マスに かこう", body)

# 3. めいろ(A→Zの順に進む)
rng = random.Random(7)
COLS, ROWS = 6, 7
def walk():
    while True:
        cur = (rng.randrange(COLS), 0); path = [cur]
        while len(path) < 26:
            x, y = path[-1]
            nb = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < COLS and 0 <= y + dy < ROWS and (x + dx, y + dy) not in path]
            if not nb: break
            path.append(rng.choice(nb))
        if len(path) == 26 and path[-1][1] >= ROWS - 2:
            return path
while True:
    path = walk(); cell = {p: U[i] for i, p in enumerate(path)}
    for y in range(ROWS):
        for x in range(COLS):
            if (x, y) in cell: continue
            ban = set()
            for i, (px, py) in enumerate(path):
                if abs(px - x) + abs(py - y) == 1 and i + 1 < 26: ban.add(U[i + 1])
            cell[(x, y)] = rng.choice([c for c in U if c not in ban])
    # 迷わないか確かめる: 各マスから見て、となりに「つぎの文字」が1つだけ
    ok = all(sum(1 for q in ((px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)) if cell.get(q) == U[i + 1]) == 1 for i, (px, py) in enumerate(path[:-1]))
    if ok: break
cells = ""
for y in range(ROWS):
    for x in range(COLS):
        c = cell[(x, y)]
        extra = ""
        if (x, y) == path[0]: extra = '<small>スタート</small>'
        if (x, y) == path[-1]: extra = '<small>ゴール</small>'
        cells += '<div class="mc%s"><b>%s</b>%s</div>' % (" go" if extra else "", c, extra)
write("abc-maze", "アルファベット めいろ", "A から Z へ すすもう", '<div class="mz">%s</div>' % cells)

# 4. ビンゴ
def card(k):
    letters = rng.sample(U, 9)
    return ('<div class="bc"><div class="nmline"><span>ビンゴ %d</span><span>なまえ</span><i></i></div><div class="bg">%s</div></div>'
            % (k, "".join('<div class="mc">%s</div>' % c for c in letters)))
strip = '<div class="cs">%s</div>' % "".join('<div>%s</div>' % c for c in U)
note = '<p class="lab">よびだしカード(きりとって ふくろに いれ、1まい ずつ ひこう)</p>'
write("abc-bingo", "アルファベット ビンゴ", "よばれた もじに ○ を つけよう", card(1) + card(2) + note + strip, nm=False)
print("ok", len(path))
