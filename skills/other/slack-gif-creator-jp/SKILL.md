---
name: slack-gif-creator-jp
description: Simplified Japanese Slack GIF creator skill covering animation GIF creation with Japanese text, traditional reaction GIFs, and recommended specifications for Slack. Triggers on requests for SlackGIF作成, GIFアニメ, リアクションGIF, Slack用画像.
---

# Slack用アニメーションGIF作成支援スキル

## 概要

Slack で使用するアニメーションGIFの作成を支援するスキルです。日本語テキストアニメーション、和風リアクションGIF、最適なサイズ・フレームレート設定をカバーします。

## ツール

| ツール | 用途 |
|--------|------|
| **gifski** | 高品質GIFエンコード（256色制限でも美しい出力） |
| **ffmpeg** | 動画からGIF変換、フレーム加工 |
| **ImageMagick** | テキスト合成、画像加工、GIF生成 |

## 日本語テキストGIF

### 日本語フォントの指定方法

```bash
# ImageMagick でフォントを指定
convert -font "Noto-Sans-JP-Bold" -pointsize 48 \
  -fill white -gravity center \
  -size 400x200 xc:transparent \
  -annotate +0+0 "お疲れさまです" output.png

# 利用可能なフォント一覧の確認
convert -list font | grep -i "jp\|japan\|gothic\|mincho"
```

### テキストアニメーション

#### 文字送り（1文字ずつ表示）

```bash
# 1文字ずつフレームを生成
TEXT="ありがとう！"
for i in $(seq 1 ${#TEXT}); do
  PARTIAL=$(echo "$TEXT" | cut -c1-$i)
  convert -size 300x100 xc:"#2C2F33" \
    -font "Noto-Sans-JP-Bold" -pointsize 36 \
    -fill white -gravity center \
    -annotate +0+0 "$PARTIAL" frame_${i}.png
done
gifski -o typing.gif --fps 4 frame_*.png
```

#### フェードイン

```bash
# 透明度を段階的に変化させてフェードイン
for i in $(seq 0 10); do
  OPACITY=$((i * 10))
  convert -size 300x100 xc:"#2C2F33" \
    -font "Noto-Sans-JP-Bold" -pointsize 36 \
    -fill "rgba(255,255,255,${OPACITY}%)" -gravity center \
    -annotate +0+0 "完了！" fade_${i}.png
done
gifski -o fadein.gif --fps 10 fade_*.png
```

### 絵文字との組み合わせ

- テキストと絵文字を別レイヤーで合成
- 絵文字部分はアニメーション（拡大・回転・バウンス）を追加
- 例: 「LGTM」+ 拍手絵文字のバウンスアニメーション

## 和風リアクションGIFアイデア

| リアクション | 表現 | 用途 |
|-------------|------|------|
| **お辞儀** | キャラクターが頭を下げるアニメ | 感謝・お願い |
| **拍手** | 手が叩かれるモーション | 称賛・お祝い |
| **花丸** | 大きな丸が描かれるアニメ | 承認・合格 |
| **了解** | 「了解」の文字が押印されるアニメ | 確認・承知 |
| **お疲れさま** | お茶のアイコンと湯気アニメ | 労いの言葉 |
| **確認中** | 虫眼鏡が動くアニメ | レビュー中 |
| **ありがとう** | 桜の花びらが舞うテキストアニメ | 感謝 |

## Slack推奨サイズ・フレームレート

| 項目 | 推奨値 |
|------|--------|
| **横幅** | 200〜400px（カスタム絵文字は128px） |
| **フレームレート** | 10〜15fps |
| **ファイルサイズ** | カスタム絵文字: 256KB以下、投稿用: 5MB以下 |
| **ループ** | 無限ループ推奨 |
| **色数** | 128〜256色 |
| **長さ** | 1〜3秒がベスト |

### カスタム絵文字用の最適化

```bash
# 128x128px、256KB以下に収めるコマンド例
gifski -o emoji.gif --fps 10 --width 128 --height 128 \
  --quality 80 frames/*.png

# ファイルサイズの確認
ls -lh emoji.gif
```

## 基本的なコマンド例

### 動画からGIF変換

```bash
# ffmpeg で動画をGIFに変換（日本語テロップ付き）
ffmpeg -i input.mp4 -vf \
  "fps=12,scale=320:-1,drawtext=fontfile=NotoSansJP-Bold.otf:\
  text='お疲れさまでした':fontsize=24:fontcolor=white:\
  x=(w-text_w)/2:y=h-40" \
  -t 3 output.gif
```

### フレーム連番からGIF生成

```bash
# ImageMagick でフレーム画像をGIFに結合
convert -delay 8 -loop 0 frame_*.png animation.gif

# gifski で高品質GIF生成
gifski -o output.gif --fps 12 --quality 90 frame_*.png
```

### GIFの最適化（ファイルサイズ削減）

```bash
# gifsicle で最適化
gifsicle -O3 --colors 128 --lossy=30 input.gif -o optimized.gif
```
