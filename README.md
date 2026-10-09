# QC Workbench

品質管理の計算ツールと問題集の入口ページ。公開先は https://kotaooka.github.io/ 。

| ツール | 公開ページ | リポジトリ |
|---|---|---|
| 工程能力解析 | https://kotaooka.github.io/cpk-calc/ | [cpk-calc](https://github.com/kotaooka/cpk-calc) |
| 抜取検査計算機 | https://kotaooka.github.io/sampling-calc/ | [sampling-calc](https://github.com/kotaooka/sampling-calc) |
| 公差積み上げ計算 | https://kotaooka.github.io/stackup-calc/ | [stackup-calc](https://github.com/kotaooka/stackup-calc) |
| 色差累積ビューア | https://kotaooka.github.io/deltae-calc/ | [deltae-calc](https://github.com/kotaooka/deltae-calc) |
| QC2級ドリル | https://kotaooka.github.io/qc2-drill/ | [qc2-drill](https://github.com/kotaooka/qc2-drill) |
| 幾何公差ドリル | https://kotaooka.github.io/gdt-drill/ | [gdt-drill](https://github.com/kotaooka/gdt-drill) |

## ファイル

```
index.html                     入口ページ（ツール一覧は中の tools 配列）
og.png                         SNS 共有用の画像（1200×630）。tools/make_og.py で作り直せる
tools/make_og.py               og.png を作り直すスクリプト（ツール名の一覧はスクリプト内の TOOLS）
sitemap.xml                    検索エンジン向けのページ一覧（各ツールのページを含む）
robots.txt                     サイト全体のクロール設定と sitemap.xml の場所
googlede6a9549483e5636.html    Search Console の所有権確認ファイル（消さない）
```

## ツールを追加するとき

新しいツールを公開したら、次の4か所を更新する。

1. **このリポジトリの `index.html`**：`tools` 配列に1項目を足す（`section`・`fig`・`name`・`desc`・`std`・`open`・`repo`、Android 版があれば `android`）。`fig` は行の左に描く図の名前で、`figs` に同じ名前の関数（viewBox 132×88 の SVG を返す。色は `currentColor`）を足す。グループを増やすときは `groups` にも足す。
2. **このリポジトリの `sitemap.xml`**：`<url>` を1つ足し、`lastmod` を公開日にする。
3. **ツール側の OGP**：`<head>` に description、canonical、`og:*`（`og:site_name` は `QC Workbench`）、`twitter:card` を入れ、1200×630 の `og.png` をツールの公開フォルダに置く。`og:image` は絶対 URL で書く。
4. **ツール側の戻るリンク**：画面上部の見出しの前に `https://kotaooka.github.io/` へのリンク（表示は「QC Workbench ›」）を置く。

ツールの中身を大きく更新したときは、`sitemap.xml` の該当ページの `lastmod` も更新する。

## og.png の作り直し

`python tools/make_og.py [Noto Sans CJK のフォルダ]` で作り直す。ツールを追加したらスクリプト内の `TOOLS` と `SUBTITLE` も直す。

文字は画像に焼き込んでいるので、表示する側のフォントに左右されない。作り直すときは、日本語フォントに Noto Sans CJK **JP** を使う（`.ttc` は日本語・中国語・韓国語の字形を1ファイルに持つので、日本語版を明示して選ぶ。選ばないと「直」「骨」などが中国語の字形になる）。

SNS は一度読んだ画像をしばらく保持するので、差し替え直後に共有すると古い画像が出ることがある。
