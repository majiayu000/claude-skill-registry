---
name: video-transcribe
description: 動画・音声の文字起こし。ローカルWhisper（無料）とOpenAI API（高速）の2モード対応。
---

# Video Transcribe Skill

Whisperを使用した動画・音声の文字起こしスキル。

## When to Use

- 動画コンテンツの文字起こし
- 字幕ファイル（SRT）生成
- 議事録・インタビュー書き起こし
- ポッドキャスト・講義のテキスト化

## Modes

### 1. ローカルモード（無料）

OpenAI Whisperをローカル実行。GPU推奨。

| モデル | 精度 | 10分の処理時間 | VRAM |
|--------|------|----------------|------|
| tiny | 低 | 約1分 | 1 GB |
| base | 中 | 約2分 | 1 GB |
| **small** | 中高 | 約3分 | 2 GB |
| medium | 高 | 約5分 | 5 GB |
| large-v3 | 最高 | 約10分 | 10 GB |

### 2. APIモード（有料・高速）

OpenAI Whisper APIを使用。高速・高精度。

| 料金 | 処理時間 | 精度 |
|------|----------|------|
| $0.006/分（約0.9円/分） | リアルタイム以下 | 最高 |

## Usage

### ローカルモード

```bash
# 基本（mediumモデル）
make transcribe FILE=local-files/videos/MainVideo.mp4

# モデル指定
make transcribe FILE=local-files/videos/MainVideo.mp4 MODEL=large-v3

# 音声ファイル
make transcribe FILE=local-files/videos/audio.mp3
```

### APIモード

```bash
# OpenAI API使用（要: OPENAI_API_KEY）
make transcribe-api FILE=local-files/videos/MainVideo.mp4

# URLから直接（ダウンロード＋文字起こし）
make transcribe-url URL="https://www.youtube.com/watch?v=xxxxx"
make transcribe-url-api URL="https://www.youtube.com/watch?v=xxxxx"
```

### 出力フォーマット指定

```bash
# SRT（字幕）
make transcribe FILE=... FORMAT=srt

# テキスト
make transcribe FILE=... FORMAT=txt

# JSON（タイムスタンプ付き）
make transcribe FILE=... FORMAT=json

# VTT（Web字幕）
make transcribe FILE=... FORMAT=vtt
```

## Output

```
local-files/transcripts/
├── [ファイル名].srt    # 字幕ファイル
├── [ファイル名].txt    # プレーンテキスト
├── [ファイル名].json   # タイムスタンプ付きJSON
└── [ファイル名].vtt    # WebVTT字幕
```

## Configuration

### 環境変数 (.env)

```bash
# OpenAI API（APIモード用）
OPENAI_API_KEY=sk-xxxxx

# デフォルト設定
WHISPER_MODEL=small           # tiny/base/small/medium/large-v3（CPUはsmall推奨）
WHISPER_LANGUAGE=ja           # 言語コード
WHISPER_OUTPUT_FORMAT=srt     # srt/txt/json/vtt
WHISPER_OUTPUT_DIR=local-files/transcripts

# ローカルモード設定
WHISPER_DEVICE=cuda           # cuda/cpu
WHISPER_COMPUTE_TYPE=float16  # float16/int8
```

## Comparison

| 項目 | ローカル | API |
|------|----------|-----|
| **料金** | 無料 | 約0.9円/分 |
| **速度** | 遅い（5-10分/10分動画） | 速い（数秒/10分動画） |
| **精度** | 高（large-v3） | 最高 |
| **GPU** | 推奨（VRAM 5GB+） | 不要 |
| **オフライン** | 可能 | 不可 |
| **プライバシー** | ローカル処理 | クラウド送信 |

## Supported Formats

### 入力

- 動画: MP4, WebM, MKV, AVI, MOV
- 音声: MP3, WAV, M4A, FLAC, OGG

### 出力

- SRT: 標準字幕フォーマット
- VTT: Web用字幕
- TXT: プレーンテキスト
- JSON: タイムスタンプ付き

## Troubleshooting

| 問題 | 解決策 |
|------|--------|
| CUDA out of memory | 小さいモデル使用 or `WHISPER_DEVICE=cpu` |
| CPU版でクラッシュ | `small`以下のモデルを使用（medium以上はメモリ不足の可能性） |
| 文字起こし精度低い | `MODEL=large-v3` を使用（要GPU） |
| API エラー | `OPENAI_API_KEY` 確認 |
| 処理が遅い | GPU使用 or APIモード推奨 |

## Related Skills

- `video-download` - 動画ダウンロード
- `video-production` - 動画編集
- `japanese-tts-reading` - テキスト読み上げ
