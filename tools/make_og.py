# SNS 共有用の画像 og.png（1200×630）を作り直す
#
# 文字は画像に焼き込むので、日本語フォントは Noto Sans CJK JP を使う。
# .ttc は日本語・中国語・韓国語の字形を1ファイルに持つため、index=0（JP）を明示して選ぶ。
# 実行: python tools/make_og.py [Noto Sans CJK のフォルダ]
#   既定は /usr/share/fonts/opentype/noto（Windows なら NotoSansCJK-*.ttc を置いたフォルダを指定）
# ツールを増やしたら TOOLS（1 行に収まる数ずつ）と SUBTITLE を直す
import math, pathlib, sys
from PIL import Image, ImageDraw, ImageFont

REPO = pathlib.Path(__file__).resolve().parent.parent
FONT_DIR = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/usr/share/fonts/opentype/noto")

SUBTITLE = ["品質管理の計算ツールと、", "QC検定・幾何公差の問題集"]
TOOLS = [
    ["工程能力解析", "測定システム解析", "抜取検査計算機"],
    ["2値データの要因解析", "公差積み上げ計算"],
    ["色差累積ビューア", "QC2級ドリル", "幾何公差ドリル"],
]
TOP, BOTTOM = (28, 91, 121), (25, 82, 110)
K = 2  # 縮小前の倍率（アンチエイリアス用）


def font(weight, size):
    f = ImageFont.truetype(str(FONT_DIR / f"NotoSansCJK-{weight}.ttc"), size * K, index=0)
    assert f.getname()[0] == "Noto Sans CJK JP", f.getname()
    return f


def main():
    W, H = 1200 * K, 630 * K
    im = Image.new("RGB", (W, H))
    g = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        g.line([(0, y), (W, y)], fill=tuple(round(TOP[i] + (BOTTOM[i] - TOP[i]) * t) for i in range(3)))
    d = ImageDraw.Draw(im, "RGBA")
    soft = (222, 233, 240)

    d.text((72 * K, 104 * K), "kotaooka.github.io", font=font("Regular", 26), fill=soft)
    d.text((70 * K, 152 * K), "QC Workbench", font=font("Bold", 82), fill=(255, 255, 255))
    for i, line in enumerate(SUBTITLE):
        d.text((72 * K, (264 + i * 46) * K), line, font=font("Regular", 28), fill=soft)
        assert 72 * K + d.textlength(line, font=font("Regular", 28)) < 770 * K, f"副題の行が図に重なる: {line}"

    pf = font("Regular", 24)
    y = 402 * K
    for row in TOOLS:
        x = 72 * K
        for name in row:
            w = d.textlength(name, font=pf) + 46 * K
            d.rounded_rectangle([x, y, x + w, y + 50 * K], radius=25 * K, fill=(255, 255, 255, 28), outline=(255, 255, 255, 110), width=2 * K)
            d.text((x + 23 * K, y + 9 * K), name, font=pf, fill=(255, 255, 255))
            x += w + 14 * K
        assert x < 770 * K, f"ツール名の行が図に重なる: {row}"
        y += 66 * K

    # 右側の図：分布曲線と規格線
    x0, x1, base, m, s, amp = 770, 1185, 500, 985, 62, 250
    curve = [(xx * K, (base - amp * math.exp(-((xx - m) / s) ** 2 / 2)) * K) for xx in range(x0, x1 + 1, 2)]
    d.polygon(curve + [(x1 * K, base * K), (x0 * K, base * K)], fill=(255, 255, 255, 30))
    d.line(curve, fill=(225, 236, 242), width=4 * K, joint="curve")
    d.line([(x0 * K, base * K), (x1 * K, base * K)], fill=(255, 255, 255, 90), width=2 * K)
    lf = font("Regular", 20)
    for xx, lab in ((796, "LSL"), (1160, "USL")):
        for yy in range(186, base, 12):
            d.line([(xx * K, yy * K), (xx * K, min(yy + 6, base) * K)], fill=(255, 255, 255, 150), width=2 * K)
        d.text((xx * K, 162 * K), lab, font=lf, fill=soft, anchor="mm")

    im.resize((1200, 630), Image.LANCZOS).save(REPO / "og.png", optimize=True)
    print("og.png を書き出した")


if __name__ == "__main__":
    main()
