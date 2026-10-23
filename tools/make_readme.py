# README.md のツール表を index.html の groups・tools 配列から作り直す
#   python tools/make_readme.py          README.md を書き換える
#   python tools/make_readme.py --check  ずれていれば終了コード 1（書き換えない）
# 表は README.md の <!-- tools:start --> と <!-- tools:end --> の間に入る。手で直さないこと
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'
README = ROOT / 'README.md'
START, END = '<!-- tools:start -->', '<!-- tools:end -->'


def objects(text):
    """配列の中身から、いちばん外側の { … } を順に取り出す（文字列の中の括弧は数えない）"""
    out, depth, begin, quote, i = [], 0, None, None, 0
    while i < len(text):
        c = text[i]
        if quote:
            if c == '\\':
                i += 1
            elif c == quote:
                quote = None
        elif c in '"\'`':
            quote = c
        elif c == '{':
            if depth == 0:
                begin = i
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                out.append(text[begin:i + 1])
        i += 1
    return out


def field(obj, key):
    m = re.search(r'\b' + key + r'\s*:\s*"((?:[^"\\]|\\.)*)"', obj)
    return m.group(1) if m else None


def load():
    html = INDEX.read_text(encoding='utf-8')
    g = re.search(r'const groups\s*=\s*\{(.*?)\n\};', html, re.S)
    t = re.search(r'const tools\s*=\s*\[(.*?)\n\];', html, re.S)
    if not g or not t:
        sys.exit('index.html に groups または tools 配列が見つかりません')
    groups = dict(re.findall(r'(\w+)\s*:\s*\{\s*title\s*:\s*"([^"]*)"', g.group(1)))
    tools = []
    for obj in objects(t.group(1)):
        item = {k: field(obj, k) for k in ('section', 'name', 'open', 'repo')}
        missing = [k for k, v in item.items() if not v]
        if missing:
            sys.exit(f'tools 配列に {"・".join(missing)} が無い項目があります：{item.get("name") or obj[:60]}')
        if item['section'] not in groups:
            sys.exit(f'{item["name"]} の section「{item["section"]}」が groups にありません')
        tools.append(item)
    return groups, tools


def table(groups, tools):
    rows = ['| 区分 | ツール | 公開ページ | リポジトリ |', '|---|---|---|---|']
    # 区分は groups の並び順、区分の中は tools 配列の並び順
    for key, title in groups.items():
        for t in (t for t in tools if t['section'] == key):
            repo = t['repo'].rstrip('/').rsplit('/', 1)[-1]
            rows.append(f'| {title} | {t["name"]} | {t["open"]} | [{repo}]({t["repo"]}) |')
    return '\n'.join(rows)


def main():
    check = '--check' in sys.argv[1:]
    readme = README.read_text(encoding='utf-8')
    if readme.count(START) != 1 or readme.count(END) != 1:
        sys.exit(f'README.md に {START} と {END} を1つずつ置いてください')
    head, rest = readme.split(START)
    _, tail = rest.split(END)
    new = f'{head}{START}\n{table(*load())}\n{END}{tail}'
    if new == readme:
        print('README.md のツール表は最新です')
        return
    if check:
        sys.exit('README.md のツール表が index.html とずれています。python tools/make_readme.py を実行してください')
    README.write_text(new, encoding='utf-8', newline='\n')
    print('README.md のツール表を作り直しました')


if __name__ == '__main__':
    main()
