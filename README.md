# 机タイム素材集

印刷して使える、2〜4歳向けの無料シートのサイトです。GitHub Pages(`main` ブランチの `/docs`)で公開します。

公開URL: https://takahiroukai.github.io/tsukue-time/

## 構成

| 場所 | 内容 |
|---|---|
| `config/site.json` | サイト名、URL、GA4の測定ID、アフィリエイトID、広告設定、タブ(種類)の説明と使い方 |
| `data/sheets.json` | シートの一覧(id、tab、title、desc、added)。表示順はこの並び順 |
| `content/sheets/<id>.html` | シート本体(A4の中身。自作のSVGとHTMLだけ) |
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

## 守ること

- 絵はすべて自作。既存のキャラクター・ブランドのロゴ・他サイトの画像や文章は使わない。
- 公開ページに、お子さんの名前・年齢の個人情報、運営者の他のサイトや活動、共有・拡散・評価の話は書かない。入力欄は `localStorage` だけに保存し、外部に送らない。
- 「効果がある」「必ず身につく」のような断定はしない。「〜の練習に使えます」にとどめる。
- 紹介本は、国立国会図書館や書店の書誌情報で、題名・著者・出版社・ISBN(13桁)を確かめたものだけ。1タブ3冊を目安に、確かめられなければ載せない。商品画像は載せない。
- アフィリエイトID(`config/site.json` の `affiliate.amazon_tag`)と広告設定(`ads`)は変えない。AdSenseは、独自ドメインを取得してから申し込む。それまで広告枠は置かない。
- 印刷時は、シート以外(ヘッダー、紹介本、フッター)が出ない。広告や紹介欄を足すときも、印刷では非表示にする。
- 更新頻度(毎日など)は公開ページに書かない。
