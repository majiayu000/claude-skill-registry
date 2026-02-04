---
name: storyboard-generator
description: AI UGC用の16コマ絵コンテを生成し、キャラクター一貫性を保ちながらKlingで動画生成まで対応。「絵コンテを作って」「ストーリーボード生成」で発動。
---

# Storyboard Generator (UGC絵コンテ生成)

AI UGC動画制作のための絵コンテ作成ツール。キャラクター参照画像＋詳細プロンプトで一貫性を保ちながら、16コマの絵コンテを1枚の画像として生成します。

## 機能

### 1. キャラクター設計
- キャラクター詳細プロンプトから基準画像を生成
- 既存のキャラクター画像を参照画像として使用可能
- 全フレームで同一キャラクターの一貫性を維持

### 2. 絵コンテ生成
- シナリオから16コマのシーン説明を自動生成（Gemini Flash）
- キャラクター参照画像を使って各コマを生成（Gemini Image）
- レイアウト自動調整:
  - **縦型（9:16）**: 2x8グリッド または 4x4
  - **横型（16:9）**: 8x2グリッド または 4x4

### 3. 動画生成連携
- 絵コンテから任意のStartFrame/EndFrameを選択
- Kling 2.6 Pro（Image-to-Video）で一貫した動画を生成
- カメラワーク指定対応

## Usage

```bash
# 絵コンテ生成のみ
python .claude/skills/storyboard-generator/scripts/generate_storyboard.py \
    --scenario "アプリの使い方を説明するUGC動画" \
    --character "20代の日本人女性、カジュアルな服装、明るい表情" \
    --aspect-ratio 9:16 \
    --session "app_promo"

# 既存キャラクター画像を使用
python .claude/skills/storyboard-generator/scripts/generate_storyboard.py \
    --scenario "商品レビュー動画" \
    --character-image "path/to/character.png" \
    --aspect-ratio 16:9 \
    --session "product_review"

# 動画生成まで実行（フレーム1→8の動き）
python .claude/skills/storyboard-generator/scripts/generate_storyboard.py \
    --scenario "..." \
    --character "..." \
    --aspect-ratio 9:16 \
    --start-frame 1 \
    --end-frame 8 \
    --video-duration 10 \
    --camera-motion "zoom_in"
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --scenario | Yes | - | 動画のシナリオ・トピック |
| --character | No* | - | キャラクター詳細プロンプト |
| --character-image | No* | - | 既存キャラクター参照画像パス |
| --aspect-ratio | No | 9:16 | アスペクト比（9:16, 16:9, 1:1, 4:3, 3:4） |
| --num-frames | No | 16 | フレーム数（4, 8, 16） |
| --layout | No | auto | グリッドレイアウト（auto, 4x4, 2x8, 8x2） |
| --session | No | - | セッション名（出力フォルダ名） |
| --start-frame | No | - | 動画生成時の開始フレーム番号 |
| --end-frame | No | - | 動画生成時の終了フレーム番号 |
| --video-duration | No | 5 | 動画の長さ（秒）: 5 or 10 |
| --camera-motion | No | - | カメラワーク（zoom_in, zoom_out, pan_left, pan_right, tilt_up, tilt_down） |
| --style | No | modern_clean | ビジュアルスタイル（modern_clean, animal_crossing, vibrant_ugc, anime） |

*--character または --character-image のどちらか必須

## Output Structure

```
output/storyboard/
└── YYYYMMDD_HHMMSS_session/
    ├── character_reference.png    # キャラクター参照画像
    ├── frames/
    │   ├── frame_01.png          # 各フレーム画像
    │   ├── frame_02.png
    │   └── ...
    ├── storyboard_grid.png       # 16コマグリッド画像
    ├── scenes.json               # シーン説明データ
    └── video/                    # 動画生成時
        ├── start_frame.png
        ├── end_frame.png
        └── output.mp4
```

## Examples

### 縦型TikTok用絵コンテ
```bash
python .claude/skills/storyboard-generator/scripts/generate_storyboard.py \
    --scenario "スマホアプリの便利な機能を紹介するTikTok動画。フックで問題提起、解決策を見せて、CTAで締める" \
    --character "20代前半の日本人女性、ショートヘア、カジュアルな白Tシャツ、親しみやすい笑顔" \
    --aspect-ratio 9:16 \
    --style vibrant_ugc \
    --session "app_tiktok"
```

### 横型YouTube用絵コンテ
```bash
python .claude/skills/storyboard-generator/scripts/generate_storyboard.py \
    --scenario "新製品のレビュー動画。開封から使用感、おすすめポイントまで" \
    --character "30代の日本人男性、メガネ、ビジネスカジュアル、信頼感のある表情" \
    --aspect-ratio 16:9 \
    --style modern_clean \
    --session "product_review"
```

### 絵コンテから動画生成
```bash
# 既存の絵コンテから動画を生成
python .claude/skills/storyboard-generator/scripts/generate_storyboard.py \
    --storyboard-dir "output/storyboard/20260127_123456_app_tiktok" \
    --start-frame 1 \
    --end-frame 5 \
    --video-duration 10 \
    --camera-motion zoom_in
```

## Requirements

- `GEMINI_API_KEY`: Gemini Flash/Image Generation用
- `FAL_KEY`: Kling動画生成用（動画生成時のみ）
- Python packages: google-genai, Pillow, python-dotenv

## Trigger Phrases

- 「絵コンテを作って」「絵コンテ生成」
- 「ストーリーボードを作成」
- 「UGC動画の絵コンテ」
- 「16コマで動画の流れを作って」
- 「縦型/横型の絵コンテ」
