#!/usr/bin/env python3
"""
hero_text_zone.py — ヒーロー画像の中で、文字(コピー)を乗せるのに適したエリアを検出する。

画像をグリッドに分割し、セルごとに
  - busyness（情報密度。エッジの強さの平均。低いほど"抜けている"＝フラットなエリア）
  - brightness（輝度の平均。文字色を白にするか黒にするかの判断材料）
  - contrast_std（そのセル内の明暗のばらつき。低いほど単色に近く、文字を乗せても背景が暴れない）
を計算し、文字を置くのに適した順にランキングする。

縦組テキストを想定して、デフォルトでは「縦長のセル」（列を細かく、行を粗く分割）でグリッドを組む
（--orientation horizontal で横組用の横長セルに変更可）。

Usage:
    python3 hero_text_zone.py <image_path> [--cols N] [--rows N] [--orientation vertical|horizontal] [--top K]

Requires: Pillow, numpy (pip install pillow numpy)
"""
import argparse
import sys

import numpy as np
from PIL import Image


def analyze(image_path: str, cols: int, rows: int):
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    arr = np.asarray(img, dtype=np.float32)

    # 輝度 (perceptual luminance)
    luminance = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]

    # エッジ強度: 輝度のx方向・y方向の勾配の大きさ
    gy, gx = np.gradient(luminance)
    edge_mag = np.sqrt(gx**2 + gy**2)

    cell_w = w / cols
    cell_h = h / rows

    cells = []
    for r in range(rows):
        for c in range(cols):
            x0, x1 = int(c * cell_w), int((c + 1) * cell_w)
            y0, y1 = int(r * cell_h), int((r + 1) * cell_h)
            lum_cell = luminance[y0:y1, x0:x1]
            edge_cell = edge_mag[y0:y1, x0:x1]
            busyness = float(edge_cell.mean())
            brightness = float(lum_cell.mean())
            contrast_std = float(lum_cell.std())
            cells.append(
                {
                    "row": r,
                    "col": c,
                    "x_pct": round(100 * x0 / w, 1),
                    "y_pct": round(100 * y0 / h, 1),
                    "w_pct": round(100 * (x1 - x0) / w, 1),
                    "h_pct": round(100 * (y1 - y0) / h, 1),
                    "busyness": round(busyness, 2),
                    "brightness": round(brightness, 1),
                    "contrast_std": round(contrast_std, 2),
                    "suggested_text_color": "white" if brightness < 128 else "dark",
                }
            )

    # スコア: busynessとcontrast_stdが低いほど良い（フラットで文字を乗せやすい）
    b_vals = np.array([c["busyness"] for c in cells])
    s_vals = np.array([c["contrast_std"] for c in cells])
    b_norm = (b_vals - b_vals.min()) / (np.ptp(b_vals) + 1e-6)
    s_norm = (s_vals - s_vals.min()) / (np.ptp(s_vals) + 1e-6)
    for cell, bn, sn in zip(cells, b_norm, s_norm):
        cell["flatness_score"] = round(1 - (0.6 * bn + 0.4 * sn), 3)  # 1に近いほど文字を置くのに適する

    cells.sort(key=lambda c: -c["flatness_score"])
    return cells, (w, h)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image_path")
    ap.add_argument("--cols", type=int, default=None)
    ap.add_argument("--rows", type=int, default=None)
    ap.add_argument("--orientation", choices=["vertical", "horizontal"], default="vertical")
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()

    if args.cols is None or args.rows is None:
        if args.orientation == "vertical":
            cols, rows = 8, 3  # 縦組コピー用: 列を細かく
        else:
            cols, rows = 4, 5  # 横組コピー用: 行を細かく
    else:
        cols, rows = args.cols, args.rows

    cells, (w, h) = analyze(args.image_path, cols, rows)

    print(f"image: {args.image_path} ({w}x{h}px), grid: {cols}x{rows} ({args.orientation})")
    print(f"top {args.top} candidate zones for placing copy (1.0 = most suitable):")
    for cell in cells[: args.top]:
        print(
            f"  score={cell['flatness_score']:.3f}  "
            f"pos=({cell['x_pct']}%, {cell['y_pct']}%) size=({cell['w_pct']}% x {cell['h_pct']}%)  "
            f"busyness={cell['busyness']}  brightness={cell['brightness']}  "
            f"text_color={cell['suggested_text_color']}"
        )


if __name__ == "__main__":
    sys.exit(main())
