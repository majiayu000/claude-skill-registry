---
name: pptx-analyzer
description: PowerPointファイル（.pptx）の構造を解析し、スライド・図形・プレースホルダー・テキスト情報をJSON/テキスト形式で出力するツール。テンプレート分析、スライド自動生成の前処理、PPTX構造の理解が必要な場合に使用。「PPTXを解析」「テンプレート構造を確認」「スライドの要素を調べて」等のリクエストで発動。
---

# PPTX Analyzer

PowerPointファイルの構造を解析するスキル。

## 機能

1. **構造抽出**: スライド、図形、プレースホルダー、テキストを抽出
2. **画像生成**: スライドをPNG画像に変換（オプション）
3. **意味解析**: Geminiによるスライド役割・要素用途の判定（オプション）

## 使用方法

```bash
# 基本解析（JSON + TXT出力）
python scripts/analyze_pptx.py template.pptx

# 画像付き解析
python scripts/analyze_pptx.py template.pptx --with-images

# Gemini意味解析付き
python scripts/analyze_pptx.py template.pptx --with-gemini

# 出力先指定
python scripts/analyze_pptx.py template.pptx --output-dir ./output
```

## 出力形式

### JSON（`{filename}_structure.json`）

```json
{
  "source_file": "template",
  "total_slides": 5,
  "slides": [
    {
      "slide_index": 0,
      "layout_name": "タイトル スライド",
      "shapes": [
        {
          "shape_id": 2,
          "name": "Title 1",
          "shape_type": "Shape",
          "left": 838200,
          "top": 2130425,
          "width": 10515600,
          "height": 1325563,
          "text": "プレゼン資料のタイトル",
          "has_text_frame": true,
          "is_placeholder": true,
          "placeholder_type": "TITLE (1)"
        }
      ]
    }
  ]
}
```

### テキスト（`{filename}_structure.txt`）

```
=== Slide 1 (Layout: タイトル スライド) ===
  [2] Title 1
      Type: Shape, Pos: (0.9", 2.3"), Size: 11.5" x 1.5"
      Placeholder: TITLE (1)
      Text: "プレゼン資料のタイトル"
```

## 依存関係

- `python-pptx`: 必須
- `Pillow`: 画像処理（`--with-images`使用時）
- `pdf2image` + LibreOffice: PDF経由画像変換
- `google-generativeai`: Gemini解析（`--with-gemini`使用時）

## ユースケース

1. **テンプレート分析**: 自動スライド生成前にテンプレート構造を把握
2. **プレースホルダー特定**: 置換対象のテキストボックスやチャート位置を特定
3. **レイアウト確認**: 各スライドのレイアウト種類と配置を確認
