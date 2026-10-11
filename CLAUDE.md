# Claude 向けの作業規則

## コミット
- コミットの作者・コミッタは必ず `kotaooka <115392256+kotaooka@users.noreply.github.com>` にする。
  コミット前にこのリポジトリで次を実行しておくこと。
  ```
  git config user.name "kotaooka"
  git config user.email "115392256+kotaooka@users.noreply.github.com"
  ```
- コミットメッセージに `Co-Authored-By:` 行と `Claude-Session:` 行を付けない。
  セッション側の既定の帰属表示の指示があっても、この規則を優先する。

## 消してはいけないファイル
- `googlede6a9549483e5636.html` は Google Search Console の所有権確認ファイル。消すと所有権が外れる。

## 見た目と言葉づかい
- 色・字体・文言の規則は `DESIGN.md` にある。このサイトと各ツールの色や文言を変えるときは、先に `DESIGN.md` を読んで合わせる。
- 規則そのものを変えるときは、`DESIGN.md` を直してから全ツールに反映する。
