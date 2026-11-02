# 机タイム素材集

印刷して使える、幼児向けの無料シートと、子育て研究の紹介ノートのサイトです。GitHub Pages(`main` ブランチの `/docs`)で公開します。

公開URL: https://takahiroukai.github.io/tsukue-time/

## 構成

| 場所 | 内容 |
|---|---|
| `config/site.json` | サイト名、URL、GA4の測定ID、アフィリエイトID、広告設定、タブ(種類)の説明と使い方 |
| `data/sheets.json` | シートの一覧(id、tab、title、desc、added)。表示順はこの並び順 |
| `content/sheets/<id>.html` | シート本体(A4の中身。自作のSVGとHTMLだけ) |
| `data/research.json` | 子育て研究の紹介(新しいものを配列の先頭ではなく、日付で並べて表示)。`research/<id>.html` が生成される |
| `data/queue.json` | 次に作るシートの題材。`python3 build.py --next` で先頭の未掲載が出る |
| `data/books.json` | タブごとの紹介本(最大3冊)。`{tab: [{title, author, publisher, isbn}]}` |
| `static/` | CSS・JS(`docs/assets/` にコピーされる) |
| `docs/` | 生成物。直接編集しない |

## コマンド

- `python3 build.py --thumbs` : プレビュー画像(`docs/img/`)を作ってから `docs/` を生成(Playwright が必要)
- `python3 build.py` : `docs/` だけを生成(プレビュー画像は残る)
- `python3 check.py --visual` : 検査。A4で1ページに収まるか、印刷時に余計な要素が出ないかも確かめる
- `python3 build.py --next` : 次に作る題材を表示

## シートを1枚追加する手順

1. `python3 build.py --next` で題材を決める。なければ `data/queue.json` に題材を足す。
2. `content/sheets/<id>.html` に、シートの中身を書く。形は既存の断片(例: `a-car.html`)に合わせる。
   - 外側は `<div class="sh">…</div>`。見出し `<h2>タイトル<small>ひとこと</small></h2>`、本体、必要なら名前欄 `<div class="foot"><span>なまえ</span><i></i></div>`。
   - 大きさの単位は `cqw`(シート幅基準)。ぬりえの絵は `<svg class="art-svg">` で自作する。
3. `data/sheets.json` の、同じタブの最後に1件足す(`added` は今日の日付、日本時間)。
4. `python3 build.py --thumbs` のあと `python3 check.py --visual` を実行し、ERRORを0にする。
5. `main` にコミットして push する。

## 子育て研究を1件追加する手順

1. WebSearch で、幼児(おおむね1〜6歳)の子育てに関わる、最新または確かな研究を探す。論文本体(または出版社・公的機関のページ)を WebFetch で開き、題名・著者・雑誌・年・DOI・対象・人数・結果の数字を、本文で確かめる。確かめられない数字は書かない。
2. `data/research.json` の `entries` に1件足す。項目: `id`(日付-英数字)、`date`、`title`、`lead`(要点を先頭に1〜2文)、`tags`、`design`(研究の種類)、`about`(どんな研究か)、`findings`(わかったこと)、`athome`(ふだんの子育てへの活かし方。title と text)、`limits`(読むときの注意。2つ以上)、`related`(あわせて使えるシートのid。任意)、`source`(authors, title, journal, year, doi, url)。
3. `python3 build.py` のあと `python3 check.py` を実行し、ERRORを0にする。WARN(断定的な表現)は、文を読んで直す。
4. `main` にコミットして push する。

## 守ること

- 研究の紹介は、出典の論文を自分の言葉で言い換える。長い引用はしない。「効果がある」「必ず」と断定せず、「〜の傾向」「〜と報告されています」にとどめる。研究の限界(対象、人数、測定方法、ばらつき)を必ず書く。医療・診断・治療の助言にしない。
- お子さんの年齢・人数・名前を、公開ページに書かない(サイトは「幼児向け」とだけ書く)。研究の対象の年齢は、研究の説明として書いてよい。

- 絵はすべて自作。既存のキャラクター・ブランドのロゴ・他サイトの画像や文章は使わない。
- 公開ページに、お子さんの名前・年齢などの個人情報、運営者の他のサイトや活動、拡散・評価の話は書かない(各ページの「共有」ボタンは、外部スクリプトを使わない共有リンクとして設置済み)。入力欄は `localStorage` だけに保存し、外部に送らない。
- 「効果がある」「必ず身につく」のような断定はしない。「〜の練習に使えます」にとどめる。
- 紹介本は、国立国会図書館や書店の書誌情報で、題名・著者・出版社・ISBN(13桁)を確かめたものだけ。1タブ3冊を目安に、確かめられなければ載せない。商品画像は載せない。
- アフィリエイトID(`config/site.json` の `affiliate.amazon_tag`)と広告設定(`ads`)は変えない。AdSenseは、独自ドメインを取得してから申し込む。それまで広告枠は置かない。
- 印刷時は、シート以外(ヘッダー、紹介本、フッター)が出ない。広告や紹介欄を足すときも、印刷では非表示にする。
- 更新頻度(毎日など)は公開ページに書かない。

## 文体

記事・シートを書く前に、`RULES.md`(書き方の規則)と `style.md`(想定読者と文体ガイド)を読む。この README の決まりが優先する。
