---
name: kaizen-site
description: 机タイム素材集の「改善の1周」で、このサイトだけに当てはまる部分(読者像、判断の観点、確かめ方)。共通の手順は TakahiroUkai/site-ops の kaizen-loop スキルにある。
---

# 改善の1周(机タイム素材集だけの部分)

共通の手順(`TakahiroUkai/site-ops` の `.claude/skills/kaizen-loop/SKILL.md`)と一緒に使う。

## 基本

- 項目の接頭辞: `TT`(司令塔の `site` は `tsukue-time`)
- 既定ブランチ: `main`。公開URL: https://takahiroukai.github.io/tsukue-time/
- 改善の曜日: 水曜
- 研究ノートの取得で分かったことは `LESSONS.md` に書く決まりがある。改善の回で研究ノートに触れたときも、それに従う。

## ユーザー役の読者像

`style.md` の「想定読者」の2つの場面を演じる。(1)スマホで、今すぐ印刷できるシートを数分で探す。(2)研究のページを、不安をあおられずに読みたい。トップページ → タブ → シートのページ → 印刷、研究の一覧 → 研究ノート、の順に使う。

## 事業推進役の観点(共通の観点に加えて)

- 欲しいシートに少ない操作でたどり着き、すぐ印刷できるか。
- 続けて来たくなるか(新しいシート、季節のテーマの見つけやすさ)。
- 集中タイマー(tsukue-timer)との行き来が自然か。

## 直してよい範囲

- `build.py` のページの組み立て、`static/` の CSS・JS、一覧の見せ方、既存のシートの題名・説明。
- 直さない: `config/site.json` の affiliate・ads・ga4、`data/queue.json` の順番、`data/books.json`、`RULES.md` と `style.md`(変えたほうがよいときは「要確認」の項目にする)。公開ページに年齢の数字を書かない。

## 確かめ方

1. `python3 build.py`(シートの絵を変えたときは `python3 build.py --thumbs`)
2. `python3 check.py --visual` で ERROR が 0 件。A4 で1ページに収まり、印刷時に余計な要素が出ないこと。
3. 変えたページを、スマホ幅(iPhone 13 相当)のスクリーンショットで見て、崩れがないこと。
