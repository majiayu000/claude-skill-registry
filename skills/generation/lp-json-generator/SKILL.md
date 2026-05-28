---
name: lp-json-generator
description: |
  参考画像のデザインスタイルを維持しながら、テキストのみを変更したLP画像を生成。
  Use when: (1) user says「この画像で文字だけ変えて」「デザインで別の内容を」,
  (2) user wants to regenerate LP images with different text,
  (3) user mentions「参考画像と同じスタイル」「テキスト差し替え」.
  Do NOT use for: ゼロからの画像生成（nanobanana-proを使用）、
  LP設計（lp-designを使用）。
---

# LP JSON Generator

参考画像のデザインスタイルを維持しながら、テキストのみを変更したLP画像を生成するスキル。

## When to Use This Skill

以下の場合に使用：
- 「この画像で文字だけ変えて」
- 「このLPのデザインで別の内容を作りたい」
- 「参考画像と同じスタイルで画像を作って」
- 「LPヘッダーのテキストを差し替えたい」

## Prerequisites

- **NanoBanana Pro**: `.claude/skills/nanobanana-pro` にインストール済み
- **Google認証**: `python3 scripts/run.py auth_manager.py setup` で認証済み

## Quick Start

### 1. 参考画像を分析してJSON化

```bash
# Claudeに依頼
「この参考画像をJSON形式でデザイン仕様書に変換して」
```

### 2. JSONのテキストを変更

JSONファイル内の `text` プロパティのみを変更。

### 3. 画像を生成

```bash
cd .claude/skills/nanobanana-pro

python3 scripts/run.py image_generator.py \
  --prompt 'Generate a Japanese marketing LP header image exactly according to this JSON specification: [JSON内容]' \
  --output output/generated.png \
  --timeout 180
```

## JSON Structure Template

```json
{
  "canvas": {
    "width": 900,
    "height": 800,
    "backgroundColor": "#FFFFFF"
  },
  "topBar": {
    "backgroundColor": "#C92A2A",
    "text": "【変更可能】上部バーのテキスト",
    "textColor": "#FFFFFF"
  },
  "textElements": [
    {
      "text": "【変更可能】",
      "fontSize": "22px",
      "fontStyle": "italic handwritten",
      "color": "#333333",
      "position": "top-left"
    },
    {
      "text": "【変更可能】メインテキスト",
      "fontSize": "72px",
      "fontFamily": "brush calligraphy",
      "color": "#111111",
      "decoration": "golden beige oval brush stroke circle around it"
    }
  ],
  "personPhoto": {
    "position": "right 50%",
    "width": "50%",
    "description": "人物の説明"
  },
  "ctaButton": {
    "backgroundColor": "green gradient",
    "text": "【変更可能】CTAテキスト",
    "playIcon": "yellow circle with play triangle"
  },
  "bottomBar": {
    "backgroundColor": "#C92A2A",
    "text1": "【変更可能】小さいテキスト",
    "text2": "【変更可能】大きいテキスト"
  }
}
```

## Examples

### Example 1: 寿司LP → 7年間の沈黙LP

**変更前（参考画像のテキスト）:**
```
えっ！最短2ヶ月で高級店レベルの寿司職人に！
```

**変更後:**
```
えっ！7年間の『沈黙』で気づいた残酷な真実を発見！
```

**生成コマンド:**
```bash
python3 scripts/run.py image_generator.py \
  --prompt 'Generate a Japanese marketing LP header image exactly according to this JSON specification:
{
  "canvas": {"width": 900, "height": 800, "backgroundColor": "#FFFFFF"},
  "topBar": {"backgroundColor": "#C92A2A", "text": "7年間の徹底調査に基づく「成功の方程式」公開", "textColor": "#FFFFFF"},
  "textElements": [
    {"text": "えっ！", "fontSize": "22px", "fontStyle": "italic handwritten", "color": "#333333"},
    {"text": "7年間の『沈黙』で", "fontSize": "28px", "fontFamily": "serif", "color": "#111111"},
    {"text": "気づいた", "fontSize": "28px", "fontFamily": "serif", "color": "#111111"},
    {"text": "残酷な真実", "fontSize": "72px", "fontFamily": "brush calligraphy", "color": "#111111", "decoration": "golden beige oval brush stroke circle around it"},
    {"text": "を発見！", "fontSize": "36px", "color": "#C92A2A"},
    {"text": "影響力がゼロでも", "fontSize": "22px", "color": "#1A4D80"},
    {"text": "成功できる秘密を", "fontSize": "22px", "color": "#1A4D80", "highlight": "秘密 in red with underline"},
    {"text": "特別公開中！", "fontSize": "46px", "color": "#C92A2A"}
  ],
  "personPhoto": {"position": "right 50%", "width": "50%", "description": "smiling Japanese man with curly hair"},
  "ctaButton": {"backgroundColor": "green gradient", "text": "無料オンライン動画を今すぐ視聴する！", "playIcon": "yellow circle"},
  "bottomBar": {"backgroundColor": "#C92A2A", "text1": "影響力に依存しない成功法則を提供する", "text2": "メイン講師の紹介"}
}
Create this exact layout with all Japanese text rendered clearly.' \
  --output output/lp_header.png \
  --timeout 180
```

## Workflow Steps

```
[Step 1] 参考画像の分析
    │
    ▼
[Step 2] JSON仕様書の作成
    │
    ▼
[Step 3] テキスト部分のみ変更
    │
    ▼
[Step 4] NanoBanana Proで画像生成
    │
    ▼
[Step 5] 結果確認・必要に応じて再生成
```

## Tips

1. **JSONは具体的に**: 色はHEXコード、サイズは数値で指定
2. **装飾を明示**: 「golden beige oval brush stroke」のように詳細に記述
3. **複数回試行**: 結果が微妙なら同じプロンプトで再生成
4. **日本語テキスト**: 完璧ではないが、JSONで構造を指定すると精度向上

## Limitations

- 日本語テキストの完全な再現は困難（AIの制限）
- 毎回完全に同じ結果にはならない
- 特定の人物写真の再現は不可能

## Related Skills

- `nanobanana-pro` - 画像生成基盤
- `gemini-image-generator` - 同じ基盤（別名）

## Troubleshooting

| 問題 | 解決方法 |
|------|----------|
| 認証エラー | `auth_manager.py setup` で再認証 |
| タイムアウト | `--timeout 300` で延長 |
| テキストが崩れる | JSONを簡略化して再試行 |
| 生成拒否 | プロンプトを修正 |
