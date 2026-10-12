# SNS 共有用の画像 og.png（1200×630）を作り直す
#
# 文字は画像に焼き込む。字体はサイトと同じ BIZ UDPゴシック（DESIGN.md 2）。
# 実行: python tools/make_og.py [フォントのフォルダ]
#   Google Fonts 版（BIZUDPGothic-Regular.ttf / -Bold.ttf）と、Windows 付属版（BIZ-UDGothicR.ttc / B.ttc。
#   1つのファイルに BIZ UDゴシックと BIZ UDPゴシックが入っている）のどちらでも読める。
#   フォルダを省略すると C:\Windows\Fonts と ~/.fonts を順に探す
# TOOLS は代表的なツールだけ載せる（全部は載せない。ツールを増やしても直さなくてよい）
# 余白は左右を MARGIN にそろえ、上下は中身を画像の上下中央に置いてそろえる
import math, pathlib, sys
from PIL import Image, ImageDraw, ImageFont

REPO = pathlib.Path(__file__).resolve().parent.parent
FONT_DIRS = [pathlib.Path(sys.argv[1])] if len(sys.argv) > 1 else [pathlib.Path("C:/Windows/Fonts"), pathlib.Path.home() / ".fonts"]
FONT_FILES = {"Regular": ["BIZUDPGothic-Regular.ttf", "BIZ-UDGothicR.ttc"], "Bold": ["BIZUDPGothic-Bold.ttf", "BIZ-UDGothicB.ttc"]}

SUBTITLE = ["品質管理の計算ツールと、", "QC検定・幾何公差の問題集"]
TOOLS = [
    ["工程能力解析", "測定システム解析", "実験計画法"],
    ["抜取検査計算機", "公差積み上げ計算"],
    ["QC2級ドリル", "幾何公差ドリル"],
]
TOP, BOTTOM = (29, 92, 150), (26, 83, 136)  # 計算ツールのアクセント #1d5c96 から少し暗く
K = 2  # 縮小前の倍率（アンチエイリアス用）
MARGIN = 72  # 左右の余白（px）
GAP = 48  # 左の文字と右の図の間の最小の間隔（px）
FIG_W = 360  # 右の図の幅（px）


def font(weight, size):
    # 見つかったファイルの中から、名前が BIZ UDPGothic の字体を選ぶ（.ttc は BIZ UDGothic と同居している）
    for d in FONT_DIRS:
        for name in FONT_FILES[weight]:
            path = d / name
            if not path.exists():
                continue
            for index in range(4):
                try:
                    f = ImageFont.truetype(str(path), size * K, index=index)
                except OSError:
                    break
                if f.getname()[0] == "BIZ UDPGothic":
                    return f
    sys.exit(f"BIZ UDPGothic（{weight}）が見つからない。フォントのフォルダを引数で指定する")


def main():
    W, H = 1200 * K, 630 * K
    im = Image.new("RGB", (W, H))
    g = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        g.line([(0, y), (W, y)], fill=tuple(round(TOP[i] + (BOTTOM[i] - TOP[i]) * t) for i in range(3)))
    # 左（文字とチップ）と右（図）をそれぞれ透明の層に描き、実際に色の付いた範囲で位置を決める
    left = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(left)
    soft = (222, 232, 244)
    d.text((0, 0), "kotaooka.github.io", font=font("Regular", 26), fill=soft)
    # BIZ UDPゴシックは欧文の幅が広いので、図との間隔（GAP）を保てる 74px にする
    d.text((-2 * K, 50 * K), "QC Workbench", font=font("Bold", 74), fill=(255, 255, 255))
    for i, line in enumerate(SUBTITLE):
        d.text((0, (154 + i * 46) * K), line, font=font("Regular", 28), fill=soft)
    pf = font("Regular", 24)
    y = 272 * K
    for row in TOOLS:
        x = 0
        for name in row:
            w = d.textlength(name, font=pf) + 46 * K
            d.rounded_rectangle([x, y, x + w, y + 50 * K], radius=25 * K, fill=(255, 255, 255, 28), outline=(255, 255, 255, 110), width=2 * K)
            d.text((x + 23 * K, y + 9 * K), name, font=pf, fill=(255, 255, 255))
            x += w + 14 * K
        y += 60 * K

    # 右の図：分布曲線と規格線（図の左端を 0 として描く）
    right = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(right)
    x0, x1, base, amp = 0, FIG_W, 360, 250
    m, s = FIG_W / 2, FIG_W * 0.15
    curve = [(xx * K, (base - amp * math.exp(-((xx - m) / s) ** 2 / 2)) * K) for xx in range(x0, x1 + 1, 2)]
    d.polygon(curve + [(x1 * K, base * K), (x0 * K, base * K)], fill=(255, 255, 255, 30))
    d.line(curve, fill=(225, 235, 246), width=4 * K, joint="curve")
    d.line([(x0 * K, base * K), (x1 * K, base * K)], fill=(255, 255, 255, 90), width=2 * K)
    lf = font("Regular", 20)
    for xx, lab in ((26, "LSL"), (FIG_W - 26, "USL")):
        for yy in range(46, base, 12):
            d.line([(xx * K, yy * K), (xx * K, min(yy + 6, base) * K)], fill=(255, 255, 255, 150), width=2 * K)
        d.text((xx * K, 22 * K), lab, font=lf, fill=soft, anchor="mm")

    lb, rb = left.getbbox(), right.getbbox()
    M = MARGIN * K
    # 左：左端を MARGIN に、上下中央に。右：右端を W − MARGIN に、上下中央に
    lx, ly = M - lb[0], (H - (lb[3] - lb[1])) // 2 - lb[1]
    rx, ry = W - M - rb[2], (H - (rb[3] - rb[1])) // 2 - rb[1]
    assert lb[2] + lx + GAP * K <= rb[0] + rx, "左の文字と右の図が近すぎる"
    assert ly + lb[1] >= M, "上下の余白が左右より狭い"
    im.paste(left, (lx, ly), left)
    im.paste(right, (rx, ry), right)

    im.resize((1200, 630), Image.LANCZOS).save(REPO / "og.png", optimize=True)
    print("og.png を書き出した")


if __name__ == "__main__":
    main()
