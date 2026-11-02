#!/usr/bin/env python3
"""公開前の検査。ERROR が1件でもあると終了コード1。--visual で A4 印刷(1枚に収まるか)も確かめる。"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
errors, warns = [], []
cfg = json.loads((ROOT / "config/site.json").read_text(encoding="utf8"))
sheets = json.loads((ROOT / "data/sheets.json").read_text(encoding="utf8"))["sheets"]
books = json.loads((ROOT / "data/books.json").read_text(encoding="utf8"))
tabs = {t["id"] for t in cfg["tabs"]}
DENY = ["窪田", "稼ぎのトリセツ", "hiragana-town", "ut.0608", "2歳と4歳", "2〜4歳", "2歳向け", "4歳向け"]  # 運営者の他の活動・個人情報・お子さんの年齢は公開しない

def err(m): errors.append(m)
def warn(m): warns.append(m)

ids = [s["id"] for s in sheets]
if len(ids) != len(set(ids)): err("シートのidが重複しています")
for s in sheets:
    f = ROOT / "content/sheets" / (s["id"] + ".html")
    if s["tab"] not in tabs: err("未知のタブ: %s" % s["id"])
    for k in ("title", "desc", "added"):
        if not s.get(k): err("%s: %s が空です" % (s["id"], k))
    if not f.exists():
        err("断片がありません: " + s["id"]); continue
    h = f.read_text(encoding="utf8")
    if re.search(r"<script|<iframe|onclick=|javascript:", h, re.I): err("%s: script等が含まれています" % s["id"])
    if re.search(r"<img|https?://", h, re.I): err("%s: 外部画像・URLが含まれています(自作SVGのみ可)" % s["id"])
    if not (DOCS / "img" / (s["id"] + ".png")).exists(): err("プレビュー画像がありません: %s (python3 build.py --thumbs)" % s["id"])
for f in (ROOT / "content/sheets").glob("*.html"):
    if f.stem not in ids: warn("manifestに無い断片: " + f.name)

# 子育て研究
research = json.loads((ROOT / "data/research.json").read_text(encoding="utf8"))["entries"]
sheet_ids = set(ids)
rids = [r["id"] for r in research]
if len(rids) != len(set(rids)): err("研究のidが重複しています")
ABS = re.compile(r"必ず|絶対|確実に|間違いなく|すれば.{0,6}(伸びる|身につく|治る)|効果がある")
for r in research:
    for k in ("id", "date", "title", "lead", "tags", "design", "about", "findings", "athome", "limits", "source"):
        if not r.get(k): err("研究 %s: %s が空です" % (r.get("id"), k))
    s = r.get("source", {})
    for k in ("authors", "title", "journal", "year", "doi", "url"):
        if not s.get(k): err("研究 %s: source.%s が空です" % (r.get("id"), k))
    if s.get("url") and not s["url"].startswith("https://"): err("研究 %s: 出典URLがhttpsではありません" % r["id"])
    for a in r.get("athome", []):
        if not (a.get("title") and a.get("text")): err("研究 %s: athome に空の項目があります" % r["id"])
    for i in r.get("related", []):
        if i not in sheet_ids: err("研究 %s: related の未知のシート %s" % (r["id"], i))
    body = json.dumps([r.get("lead"), r.get("about"), r.get("findings"), r.get("athome"), r.get("limits")], ensure_ascii=False)
    for m in ABS.findall(body):
        warn("研究 %s: 断定的な表現がないか確認してください(%s)" % (r["id"], m if isinstance(m, str) else "".join(m)))
    if len(r.get("limits", [])) < 2: warn("研究 %s: 『読むときの注意』が少ないです" % r["id"])

# 紹介本: ISBN13 のチェックディジット
sys.path.insert(0, str(ROOT))
import importlib.util
spec = importlib.util.spec_from_file_location("build", ROOT / "build.py"); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
for tab, items in books.items():
    if tab not in tabs: err("books: 未知のタブ " + tab)
    if len(items) > 3: warn("books[%s]: 3冊を超えています" % tab)
    for it in items:
        try: b.isbn13_to_10(it["isbn"])
        except Exception as e: err("books[%s] %s: %s" % (tab, it.get("title"), e))
        for k in ("title", "author", "publisher", "isbn"):
            if not it.get(k): err("books[%s]: %s が空です" % (tab, k))

# 生成物
pages = list(DOCS.rglob("*.html"))
if not pages: err("docs/ が空です。python3 build.py を実行してください")
for p in pages:
    t = p.read_text(encoding="utf8")
    rel = p.relative_to(DOCS)
    for w in DENY:
        if w in t: err("%s: 公開しない語 '%s' が含まれています" % (rel, w))
    if not re.search(r"<title>.+</title>", t): err("%s: titleがありません" % rel)
    if 'name="description"' not in t: err("%s: descriptionがありません" % rel)
    if cfg["ga4"] not in t: err("%s: GA4タグがありません" % rel)
    if re.search(r"共有|拡散|SNS|評価", t): warn("%s: 共有・評価に触れた語があります(公開ページには書かない)" % rel)
    if cfg["ads"].get("placeholder") is False and re.search(r"広告スペース|準備中", t): err("%s: 広告枠の仮表示が残っています" % rel)
    for m in re.findall(r'(?:href|src)="([^"#:]+?)"', t):
        if m.startswith(("http", "mailto")): continue
        tgt = (p.parent / m).resolve()
        if m.endswith("/"): tgt = tgt / "index.html"
        if not tgt.exists(): err("%s: リンク切れ %s" % (rel, m))
    if "amazon.co.jp" in t and "適格販売" not in t: err("%s: アソシエイトの表示がありません" % rel)

if "--visual" in sys.argv:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch()
        ctx = br.new_context(viewport={"width": 390, "height": 800})
        ctx.route("**/*", lambda r: r.abort() if r.request.url.startswith("http") else r.continue_())
        pg = ctx.new_page()
        for s in sheets:
            pg.emulate_media(media="screen")
            pg.goto("file://%s/%s/%s.html" % (DOCS, s["tab"], s["id"]))
            over = pg.evaluate("""()=>{const sh=document.querySelector('.sheet');const r=sh.getBoundingClientRect();
              return Array.from(sh.querySelectorAll('*')).filter(e=>{if(e.closest('svg'))return false;const q=e.getBoundingClientRect();return q.width>0&&(q.right>r.right+2||q.bottom>r.bottom+2)}).length}""")
            if over: warn("%s: シートからはみ出す要素が %d 個あります" % (s["id"], over))
            pg.emulate_media(media="print")
            pdf = pg.pdf(prefer_css_page_size=True, print_background=True)
            n = len(re.findall(rb"/Type\s*/Page[^s]", pdf))
            if n != 1: err("%s: 印刷が %d ページになります(1ページにする)" % (s["id"], n))
            vis = pg.evaluate("()=>Array.from(document.querySelectorAll('.books,footer.site,.top,.actions')).filter(e=>getComputedStyle(e).display!=='none').length")
            if vis: err("%s: 印刷時に非表示にすべき要素が表示されます" % s["id"])
        br.close()

for w in warns: print("WARN ", w)
for e in errors: print("ERROR", e)
print("ERROR %d件 / WARN %d件" % (len(errors), len(warns)))
sys.exit(1 if errors else 0)
