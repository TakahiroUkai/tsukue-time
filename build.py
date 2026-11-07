#!/usr/bin/env python3
"""机タイム素材集 サイトのビルド。content/ と data/ から docs/ を生成する。

使い方:
  python3 build.py            # docs/ を生成(プレビュー画像 docs/img/ が無いシートは画像なしで出力)
  python3 build.py --thumbs   # 先にプレビュー画像(Playwright)を作ってから生成
  python3 build.py --next     # 次に作る題材(data/queue.json の先頭の未掲載)を表示
  python3 build.py --artifact-json <id>   # 自分用Artifactに足す1件のJSON(<は\\u003cに置き換え済み)を表示
"""
import html
import urllib.parse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
CFG = json.loads((ROOT / "config/site.json").read_text(encoding="utf8"))
SHEETS = json.loads((ROOT / "data/sheets.json").read_text(encoding="utf8"))["sheets"]
BOOKS = json.loads((ROOT / "data/books.json").read_text(encoding="utf8"))
RESEARCH = json.loads((ROOT / "data/research.json").read_text(encoding="utf8"))["entries"]
RES = CFG["research"]
SHEET_BY_ID = {s["id"]: s for s in SHEETS}
TABS = CFG["tabs"]
TAB = {t["id"]: t for t in TABS}
SITE = CFG["url"]
TODAY_FALLBACK = "2026-11-01"
# トップの「いまの季節のシート」に出すシートのid(季節が変わったら入れ替える)
SEASON_TITLE = "いまの季節のシート(クリスマス・お正月)"
SEASON_IDS = ["s-xmas", "s-christmas-wreath", "s-xmas-stocking", "seal-xmas", "d-tree",
              "s-newyear", "s-newyear-sheep", "t-mochi"]

esc = html.escape


def isbn13_to_10(isbn13):
    d = re.sub(r"[^0-9]", "", isbn13)
    if len(d) != 13 or not d.startswith("978"):
        raise ValueError("ISBN-13 (978始まり) ではありません: " + isbn13)
    if sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(d)) % 10 != 0:
        raise ValueError("ISBN-13 のチェックディジットが合いません: " + isbn13)
    body = d[3:12]
    s = sum(int(c) * (10 - i) for i, c in enumerate(body))
    chk = (11 - s % 11) % 11
    return body + ("X" if chk == 10 else str(chk))


def amazon_url(isbn13):
    return "https://www.amazon.co.jp/dp/%s?tag=%s" % (isbn13_to_10(isbn13), CFG["affiliate"]["amazon_tag"])


def head(title, desc, rel, path, img=None):
    full_title = title if title == CFG["name"] else "%s | %s" % (title, CFG["name"])
    url = SITE + path
    og = ""
    if img:
        og = '<meta property="og:image" content="%s"><meta name="twitter:card" content="summary_large_image">' % esc(SITE + img)
    ga = CFG["ga4"]
    return """<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta property="og:type" content="website"><meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s"><meta property="og:locale" content="ja_JP">
%s
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Klee+One:wght@400;600&family=Zen+Maru+Gothic:wght@400;500;700&family=Andika:wght@400;700&display=swap">
<link rel="stylesheet" href="%sassets/site.css"><link rel="stylesheet" href="%sassets/sheet.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','%s');</script>
</head><body>
""" % (esc(full_title), esc(desc), esc(url), esc(full_title), esc(desc), esc(url), og, rel, rel, ga, ga)


def header(rel, current):
    links = "".join(
        '<a href="%s%s/"%s>%s</a>' % (rel, t["id"], ' aria-current="page"' if t["id"] == current else "", esc(t["label"]))
        for t in TABS
    )
    links += '<a href="%sresearch/"%s class="rs-link">%s</a>' % (
        rel, ' aria-current="page"' if current == "research" else "", esc(RES["label"]))
    return ('<header class="top"><div class="wrap"><a class="brand" href="%s">%s</a>'
            '<nav class="tabs" aria-label="コンテンツの種類">%s</nav></div></header>\n' % (rel or "./", esc(CFG["name"]), links))


def footer(rel):
    return ('<footer class="site"><div class="wrap">'
            '<p>このサイトのシートは、すべて自作のオリジナルです。家庭・保育園・教室での印刷にご利用いただけます。再配布や販売はご遠慮ください。</p>'
            '<p>机に向かう時間に:<a href="https://takahiroukai.github.io/tsukue-timer/">丸が小さくなる集中タイマー</a>(作業と休憩の時間を、目で見て分かります)</p>'
            '<p>Amazonのアソシエイトとして、適格販売により収入を得ています。</p>'
            '<p><a href="%sabout.html">このサイトについて</a> / <a href="%sprivacy.html">プライバシーポリシー</a></p>'
            '</div></footer>\n<script src="%sassets/site.js" defer></script>\n</body></html>\n' % (rel, rel, rel))


def share_html(path, title):
    """共有ボタン。外部スクリプトは使わず、各サービスの共有URLへのリンクだけ。"""
    url = SITE + path
    q = urllib.parse.quote
    links = [
        ("X", "https://twitter.com/intent/tweet?url=%s&text=%s" % (q(url, safe=""), q(title, safe=""))),
        ("LINE", "https://social-plugins.line.me/lineit/share?url=%s" % q(url, safe="")),
        ("Facebook", "https://www.facebook.com/sharer/sharer.php?u=%s" % q(url, safe="")),
    ]
    a = "".join('<a class="sh-btn" href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (esc(h), n) for n, h in links)
    return ('<div class="share noprint" data-share data-url="%s" data-title="%s"><span class="share-t">このページを共有</span>'
            '<button type="button" class="sh-btn" data-share-native hidden>共有する</button>%s'
            '<button type="button" class="sh-btn" data-share-copy>リンクをコピー</button>'
            '<span class="share-ok" role="status" aria-live="polite"></span></div>' % (esc(url), esc(title), a))


def thumb_exists(sid):
    return (DOCS / "img" / (sid + ".png")).exists()


def card(s, rel):
    img = ('<img src="%simg/%s.png" alt="%sの見本" width="210" height="297" loading="lazy">' % (rel, esc(s["id"]), esc(s["title"]))
           if thumb_exists(s["id"]) else "")
    return ('<li class="card"><a href="%s%s/%s.html">%s<div class="b"><div class="t">%s</div><div class="d">%s</div></div></a></li>'
            % (rel, s["tab"], s["id"], img, esc(s["title"]), esc(s["desc"])))


def books_html(tab):
    items = BOOKS.get(tab, [])
    if not items:
        return ""
    lis = []
    for b in items:
        lis.append('<li><div class="bt"><a href="%s" rel="sponsored nofollow noopener" target="_blank">%s</a></div>'
                   '<div class="bm">%s(%s)</div></li>' % (esc(amazon_url(b["isbn"])), esc(b["title"]), esc(b["author"]), esc(b["publisher"])))
    return ('<h2>あわせて使える本</h2><p class="hint">紹介リンクを含みます(Amazonアソシエイト)。書名・著者・出版社・ISBNは書店や国立国会図書館の書誌情報で確認したものです。</p>'
            '<ul class="books">%s</ul>' % "".join(lis))


def write(path, text):
    p = DOCS / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf8")


def research_sorted():
    return sorted(RESEARCH, key=lambda r: (r["date"], r["id"]), reverse=True)


def research_card(r, rel):
    chips = "".join('<li class="chip">%s</li>' % esc(x) for x in r["tags"])
    return ('<li class="rcard"><a href="%sresearch/%s.html"><div class="rcd">%s</div><div class="rct">%s</div>'
            '<div class="rcl">%s</div><ul class="chips">%s</ul></a></li>'
            % (rel, esc(r["id"]), esc(r["date"]), esc(r["title"]), esc(r["lead"]), chips))


def research_block(rel, n):
    items = research_sorted()[:n]
    if not items:
        return ""
    return ('<h2>子育て研究ノート</h2><p class="lead">%s</p><ul class="rlist">%s</ul>'
            '<p><a href="%sresearch/">子育て研究の一覧を見る &rarr;</a></p>'
            % (esc(RES["intro"]), "".join(research_card(r, rel) for r in items), rel))


def build_research_index():
    rel = "../"
    desc = "幼児の子育てに関わる研究を、出典つきで1つずつ紹介します。研究の内容と、ふだんの暮らしでの活かし方をまとめています。"
    out = head(RES["label"], desc, rel, "research/")
    out += header(rel, "research")
    out += ('<main><div class="wrap"><p class="crumb"><a href="../">ホーム</a> &gt; %s</p><h1>%s</h1><p class="lead">%s</p>'
            % (esc(RES["label"]), esc(RES["label"]), esc(RES["intro"])))
    out += '<ul class="rlist">%s</ul>' % "".join(research_card(r, rel) for r in research_sorted())
    out += '<div class="box warn"><p>%s</p></div>' % esc(RES["notice"])
    out += "</div></main>" + footer(rel)
    write("research/index.html", out)


def build_research(r):
    rel = "../"
    s = r["source"]
    path = "research/%s.html" % r["id"]
    out = head(r["title"], r["lead"], rel, path)
    out += header(rel, "research")
    chips = "".join('<li class="chip">%s</li>' % esc(x) for x in r["tags"])
    out += ('<main><div class="wrap"><article class="article">'
            '<p class="crumb"><a href="../">ホーム</a> &gt; <a href="./">%s</a> &gt; この研究</p>'
            '<h1>%s</h1><p class="lead">%s</p><ul class="chips">%s</ul>'
            '<p class="hint">掲載日 %s / 研究の種類:%s</p>'
            % (esc(RES["label"]), esc(r["title"]), esc(r["lead"]), chips, esc(r["date"]), esc(r["design"])))
    out += share_html(path, r["title"] + " | " + CFG["name"])
    out += '<h2>どんな研究?</h2>' + "".join("<p>%s</p>" % esc(x) for x in r["about"])
    out += '<h2>わかったこと</h2><ul>%s</ul>' % "".join("<li>%s</li>" % esc(x) for x in r["findings"])
    out += '<h2>ふだんの子育てへの活かし方</h2><div class="box ok"><ol class="tips">%s</ol></div>' % "".join(
        "<li><b>%s</b><br>%s</li>" % (esc(a["title"]), esc(a["text"])) for a in r["athome"])
    out += '<h2>読むときの注意</h2><ul>%s</ul>' % "".join("<li>%s</li>" % esc(x) for x in r["limits"])
    rel_sheets = [SHEET_BY_ID[i] for i in r.get("related", []) if i in SHEET_BY_ID]
    if rel_sheets:
        out += '<h2>あわせて使えるシート</h2><ul class="grid">%s</ul>' % "".join(card(x, rel) for x in rel_sheets)
    out += ('<h2>出典</h2><p class="cite">%s(%d). %s. <i>%s</i>. DOI: %s<br><a href="%s" rel="noopener" target="_blank">論文のページを開く</a></p>'
            % (esc(s["authors"]), s["year"], esc(s["title"]), esc(s["journal"]), esc(s["doi"]), esc(s["url"])))
    out += '<div class="box warn"><p>%s</p></div>' % esc(RES["notice"])
    out += share_html(path, r["title"] + " | " + CFG["name"])
    items = research_sorted()
    idx = items.index(r)
    nav = ""
    nav += ('<a href="%s.html">&larr; %s</a>' % (items[idx + 1]["id"], esc(items[idx + 1]["title"]))) if idx + 1 < len(items) else "<span></span>"
    nav += ('<a href="%s.html">%s &rarr;</a>' % (items[idx - 1]["id"], esc(items[idx - 1]["title"]))) if idx > 0 else ""
    out += '<div class="pn">%s</div>' % nav
    out += '<p><a href="./">&larr; %s の一覧にもどる</a></p>' % esc(RES["label"])
    out += "</article></div></main>" + footer(rel)
    write(path, out)


def build_index():
    rel = ""
    counts = {t["id"]: sum(1 for s in SHEETS if s["tab"] == t["id"]) for t in TABS}
    tabcards = "".join(
        '<li class="card"><a href="%s/"><div class="b"><div class="t">%s(%d枚)</div><div class="d">%s</div></div></a></li>'
        % (t["id"], esc(t["label"]), counts[t["id"]], esc(t["intro"]))
        for t in TABS
    )
    newest = sorted(SHEETS, key=lambda s: s["added"], reverse=True)
    latest_date = newest[0]["added"]
    latest = [s for s in SHEETS if s["added"] == latest_date]
    if len(latest) == len(SHEETS):
        latest = SHEETS[:8]
        latest_title = "人気のシート"
    else:
        latest = latest[:8]
        latest_title = "新しいシート"
    desc = "A4で印刷できる、幼児向けの無料シート集です。ぬりえ、なぞり書き、ひらがな表、点つなぎなど%d種類。子育ての研究を紹介するコーナーもあります。" % len(SHEETS)
    out = head(CFG["name"], desc, rel, "", "img/%s.png" % latest[0]["id"] if thumb_exists(latest[0]["id"]) else None)
    out += header(rel, None)
    out += ('<section class="hero"><div class="wrap"><h1>%s</h1><p class="lead">%s。ぬりえ、なぞり書き、ひらがな表、点つなぎなど、全%d種類。印刷ボタンを押すだけでA4で1枚ずつ印刷できます。</p></div></section>'
            % (esc(CFG["name"]), esc(CFG["subtitle"]), len(SHEETS)))
    out += '<main><div class="wrap">'
    out += '<h2>シートの種類</h2><ul class="grid tabcards">%s</ul>' % tabcards
    out += '<h2>%s</h2><ul class="grid">%s</ul>' % (latest_title, "".join(card(s, rel) for s in latest))
    shown = {s["id"] for s in latest}
    season = [SHEET_BY_ID[i] for i in SEASON_IDS if i in SHEET_BY_ID and i not in shown][:6]
    if season:
        out += '<h2>%s</h2><ul class="grid">%s</ul>' % (SEASON_TITLE, "".join(card(s, rel) for s in season))
    out += research_block(rel, 3)
    out += ('<h2>印刷のコツ</h2><div class="box"><ul><li>用紙はA4。印刷の設定で、倍率は「100%」または「実際のサイズ」にします。</li>'
            '<li>余白は「なし」か「標準」。プリンターによって端が少し切れることがありますが、シートは周りに余白をとってあります。</li>'
            '<li>色はモノクロで十分です。ぬりえはコピー用紙でも使えます。</li></ul></div></div></main>')
    out += footer(rel)
    write("index.html", out)


def build_tab(t):
    rel = "../"
    items = [s for s in SHEETS if s["tab"] == t["id"]]
    desc = "%s(%d枚)。%s" % (t["label"], len(items), t["intro"])
    out = head(t["label"], desc, rel, t["id"] + "/", ("img/%s.png" % items[0]["id"]) if thumb_exists(items[0]["id"]) else None)
    out += header(rel, t["id"])
    out += '<main><div class="wrap"><p class="crumb"><a href="../">ホーム</a> &gt; %s</p><h1>%s</h1><p class="lead">%s</p>' % (esc(t["label"]), esc(t["label"]), esc(t["intro"]))
    out += '<ul class="grid">%s</ul>' % "".join(card(s, rel) for s in items)
    out += '<h2>使い方</h2><div class="box"><ol>%s</ol></div>' % "".join("<li>%s</li>" % esc(h) for h in t["howto"])
    out += books_html(t["id"])
    out += "</div></main>" + footer(rel)
    write(t["id"] + "/index.html", out)


def build_sheet(s, i):
    rel = "../"
    t = TAB[s["tab"]]
    frag = (ROOT / "content/sheets" / (s["id"] + ".html")).read_text(encoding="utf8")
    same = [x for x in SHEETS if x["tab"] == s["tab"]]
    idx = same.index(s)
    prev_s = same[idx - 1] if idx > 0 else None
    next_s = same[idx + 1] if idx + 1 < len(same) else None
    desc = "%s(%s)。A4で無料印刷できる、幼児向けのシートです。" % (s["title"], s["desc"])
    path = "%s/%s.html" % (s["tab"], s["id"])
    out = head(s["title"], desc, rel, path, ("img/%s.png" % s["id"]) if thumb_exists(s["id"]) else None)
    out += header(rel, s["tab"])
    out += ('<main><div class="wrap"><p class="crumb"><a href="../">ホーム</a> &gt; <a href="./">%s</a> &gt; %s</p>'
            '<h1>%s</h1><p class="lead">%s</p>' % (esc(t["label"]), esc(s["title"]), esc(s["title"]), esc(s["desc"])))
    out += '<div class="actions"><button type="button" class="btn" data-print>このシートを印刷する(A4)</button><span class="hint">印刷画面で、倍率は100%にします。</span></div>'
    out += share_html(path, s["title"] + " | " + CFG["name"])
    if s["id"] == "name":
        out += ('<div class="box noprint"><label for="nameIn"><b>お子さんの名前(ひらがな)</b></label><br>'
                '<input id="nameIn" type="text" maxlength="12" placeholder="ひらがなで入力" autocomplete="off" style="font:inherit;font-size:18px;padding:6px 12px;border:1px solid var(--line);border-radius:8px;max-width:100%">'
                '<p class="hint">入力した名前は、この端末のブラウザの中だけで使われ、サイトには送られません。6文字まで。</p></div>')
    elif "<input" in frag:
        out += '<p class="hint noprint">シートの中の入力欄に書き込めます。入力した内容は、この端末のブラウザの中にだけ保存されます。</p>'
    out += '<div class="sheet-wrap"><div class="sheet" data-sheet="%s">%s</div></div>' % (esc(s["id"]), frag.rstrip())
    out += '<h2>使い方</h2><div class="box"><ol>%s</ol></div>' % "".join("<li>%s</li>" % esc(h) for h in t["howto"])
    out += books_html(s["tab"])
    nav = ""
    if prev_s:
        nav += '<a href="%s.html">&larr; %s</a>' % (prev_s["id"], esc(prev_s["title"]))
    else:
        nav += "<span></span>"
    if next_s:
        nav += '<a href="%s.html">%s &rarr;</a>' % (next_s["id"], esc(next_s["title"]))
    out += '<div class="pn">%s</div>' % nav
    others = [x for x in same if x is not s]
    # 近い順(同じタブの前後)に最大4枚
    others.sort(key=lambda x: abs(same.index(x) - idx))
    others = others[:4]
    if others:
        out += '<h2 class="noprint">同じ種類のほかのシート</h2><ul class="grid noprint">%s</ul>' % "".join(card(x, rel) for x in others)
    out += '<p><a href="./">&larr; %s の一覧にもどる</a></p>' % esc(t["label"])
    out += "</div></main>" + footer(rel)
    write(path, out)


def build_static_pages():
    rel = ""
    about = head("このサイトについて", "机タイム素材集は、印刷して使える幼児向けの無料シートと、子育ての研究紹介を公開しているサイトです。", rel, "about.html")
    about += header(rel, None)
    about += ('<main><div class="wrap"><h1>このサイトについて</h1>'
              '<p>机タイム素材集は、小さな子どもが机に向かう時間のために、A4で印刷できるシートを公開するサイトです。ぬりえ、なぞり書き、ひらがな表、点つなぎなどを、印刷ボタンひとつで使えるようにしています。</p>'
              '<h2>子育て研究について</h2><p>幼児の子育てに関わる研究を、論文などの出典つきで紹介しています。研究の内容に加えて、ふだんの暮らしでの活かし方もまとめています。研究結果は、すべての子どもに当てはまるとは限りません。一般的な情報として読み、気になることは、かかりつけ医・保健師・園の先生などにご相談ください。</p>'
              '<h2>素材について</h2><p>シートの絵は、すべて自作のオリジナルです。既存のキャラクターは描いていません。家庭・保育園・教室での印刷にご利用いただけます。再配布や販売はご遠慮ください。</p>'
              '<h2>広告・紹介リンクについて</h2><p>一部のページに、書籍の紹介リンクを載せています。Amazonのアソシエイトとして、適格販売により収入を得ています。紹介する本は、書誌情報を確認したものにしています。</p>'
              '</div></main>')
    about += footer(rel)
    write("about.html", about)
    pv = head("プライバシーポリシー", "机タイム素材集のプライバシーポリシー(アクセス解析、入力内容の扱い、紹介リンクについて)です。", rel, "privacy.html")
    pv += header(rel, None)
    pv += ('<main><div class="wrap"><h1>プライバシーポリシー</h1>'
           '<h2>アクセス解析</h2><p>このサイトは、利用状況を把握するために、Googleアナリティクス(GA4)を使っています。GA4は、Cookieなどを使ってアクセス情報を集めますが、個人を特定する情報は含まれません。ブラウザの設定でCookieを無効にすると、収集を避けられます。詳しくはGoogleのプライバシーポリシーをご確認ください。</p>'
           '<h2>入力内容の扱い</h2><p>名前や曜日のテーマなど、シートの入力欄に書いた内容は、お使いの端末のブラウザの中(localStorage)にだけ保存されます。サイトの運営者には送られません。</p>'
           '<h2>紹介リンク</h2><p>Amazonアソシエイト・プログラムの参加者として、紹介リンクから購入があった場合に、運営者が紹介料を受け取ることがあります。</p>'
           '<h2>広告</h2><p>現在、このサイトに広告は掲載していません。将来、広告配信サービスを導入する場合は、このページに内容を追記します。</p>'
           '</div></main>')
    pv += footer(rel)
    write("privacy.html", pv)


def build_assets():
    (DOCS / "assets").mkdir(parents=True, exist_ok=True)
    for f in ("site.css", "sheet.css", "site.js"):
        shutil.copyfile(ROOT / "static" / f, DOCS / "assets" / f)
    (DOCS / ".nojekyll").write_text("", encoding="utf8")
    (DOCS / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: %ssitemap.xml\n" % SITE, encoding="utf8")
    urls = [SITE, SITE + "about.html", SITE + "privacy.html"] + [SITE + t["id"] + "/" for t in TABS] + [SITE + "research/"] + \
           ["%sresearch/%s.html" % (SITE, r["id"]) for r in RESEARCH] + \
           ["%s%s/%s.html" % (SITE, s["tab"], s["id"]) for s in SHEETS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % "".join(
        "<url><loc>%s</loc></url>\n" % esc(u) for u in urls)
    (DOCS / "sitemap.xml").write_text(sm, encoding="utf8")


def make_thumbs():
    from playwright.sync_api import sync_playwright
    try:
        from PIL import Image
    except ImportError:
        Image = None
    (DOCS / "img").mkdir(parents=True, exist_ok=True)
    css = (ROOT / "static/sheet.css").read_text(encoding="utf8")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 420, "height": 600}, device_scale_factor=1)
        for s in SHEETS:
            frag = (ROOT / "content/sheets" / (s["id"] + ".html")).read_text(encoding="utf8")
            pg.set_content('<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#fff}%s .sheet{box-shadow:none}</style>'
                           '<div class="sheet" style="width:420px">%s</div>' % (css, frag))
            out = DOCS / "img" / (s["id"] + ".png")
            pg.locator(".sheet").screenshot(path=str(out))
            if Image:
                im = Image.open(out).convert("RGB").quantize(colors=48)
                im.save(out, optimize=True)
        b.close()
    print("プレビュー画像を作りました:", len(SHEETS), "枚")


def next_topic():
    q = json.loads((ROOT / "data/queue.json").read_text(encoding="utf8"))
    done = {s["id"] for s in SHEETS}
    for item in q["queue"]:
        if item["id"] not in done:
            print(json.dumps(item, ensure_ascii=False))
            return
    print("")


def artifact_json(sid):
    s = next(x for x in SHEETS if x["id"] == sid)
    frag = (ROOT / "content/sheets" / (sid + ".html")).read_text(encoding="utf8").rstrip()
    item = {"id": s["id"], "tab": s["tab"], "title": s["title"], "desc": s["desc"], "added": s["added"], "html": frag}
    print(json.dumps(item, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c"))


def main():
    if "--artifact-json" in sys.argv:
        artifact_json(sys.argv[sys.argv.index("--artifact-json") + 1])
        return
    if "--next" in sys.argv:
        next_topic()
        return
    ids = [s["id"] for s in SHEETS]
    assert len(ids) == len(set(ids)), "シートのidが重複しています"
    rids = [r["id"] for r in RESEARCH]
    assert len(rids) == len(set(rids)), "研究のidが重複しています"
    for s in SHEETS:
        assert s["tab"] in TAB, "未知のタブ: " + s["tab"]
        assert (ROOT / "content/sheets" / (s["id"] + ".html")).exists(), "断片がありません: " + s["id"]
    if "--thumbs" in sys.argv:
        make_thumbs()
    if DOCS.exists():
        for child in DOCS.iterdir():
            if child.name == "img":
                continue
            shutil.rmtree(child) if child.is_dir() else child.unlink()
    build_assets()
    build_index()
    for t in TABS:
        build_tab(t)
    for i, s in enumerate(SHEETS):
        build_sheet(s, i)
    build_research_index()
    for r in RESEARCH:
        build_research(r)
    build_static_pages()
    print("docs/ を生成しました: シート%d枚・研究%d件" % (len(SHEETS), len(RESEARCH)))


if __name__ == "__main__":
    main()
