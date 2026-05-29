---
name: video-agent
description: 動画自動生成パイプライン（Video Agent OS）の統合スキル。ダウンロード、文字起こし、制作、品質管理、CI/CD、通知まで一貫して対応。
version: "2.0.0"
author: TAISUN
---

# Video Agent - 統合動画自動化スキル

動画制作から品質管理、自動化パイプラインまでを一元管理するスキル。

---

## 機能一覧

### 1. コンテンツ取得・変換

#### 動画ダウンロード
```bash
# YouTube等から動画をダウンロード
yt-dlp -f "best[height<=1080]" <URL> -o "output/%(title)s.%(ext)s"

# 音声のみ抽出
yt-dlp -x --audio-format mp3 <URL>
```

#### 文字起こし（Whisper）
```bash
# ローカルWhisper（無料・低速）
whisper video.mp4 --model medium --language ja --output_format srt

# OpenAI API（高速・有料）
curl https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file=@audio.mp3 \
  -F model="whisper-1" \
  -F language="ja"
```

---

### 2. 動画制作

#### 制作フロー
1. **台本作成** - Claude/GPTでスクリプト生成
2. **ナレーション** - GPT-SoVITS / OpenAI TTS
3. **映像素材** - NanoBanana Pro / Pexels API
4. **編集** - Remotion / FFmpeg
5. **出力** - MP4 (1080p/4K)

#### Remotion動画生成
```bash
cd remotion-project
npm run build
npx remotion render src/index.tsx VideoComposition out/video.mp4
```

#### FFmpeg基本操作
```bash
# 動画結合
ffmpeg -f concat -i list.txt -c copy output.mp4

# 音声追加
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac output.mp4

# リサイズ（縦動画）
ffmpeg -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" output.mp4
```

---

### 3. 品質管理（Phase 4）

#### ポリシーチェック
```bash
make phase4-policy
```
- `.env` がgit追跡されていないか確認
- Secrets漏れ防止

#### 回帰評価
```bash
make phase4-eval
```
- 評価データセット10件以上必要
- 品質スコアの回帰検出

---

### 4. メトリクス・監視（Phase 5）

#### メトリクス収集
```bash
make phase5-metrics
# → metrics/YYYYMMDD.jsonl に記録
```

#### 異常検知
```bash
make phase5-anomaly
# 直近N件のメトリクスを分析し異常を検出
```

#### 通知
```bash
make phase5-notify
# Slack/Discord/メールに異常通知
```

---

### 5. 実行制御（Phase 6）

#### 実行フロー
```
validate → guard → dispatch → 実行
```

#### コマンド
```bash
# 入力検証
make phase6-validate PHASE=<phase> MODE=<mode> REASON='<reason>'

# 安全確認
make phase6-guard PHASE=<phase> MODE=<mode> REASON='<reason>'

# 実行
make phase6-run PHASE=<phase> MODE=<mode> REASON='<reason>'
```

---

### 6. CI/CD スケジューリング

#### GitHub Actions
- Phase2: 毎日 01:00 UTC
- Phase3: 毎日 01:30 UTC

#### ファイル
- `.github/workflows/phase2-scheduled.yml`
- `.github/workflows/phase3-scheduled.yml`

---

## ディレクトリ構造

```
video-agent/
├── scripts/
│   ├── phase4-policy.sh
│   ├── phase4-eval.sh
│   ├── phase5-metrics.sh
│   ├── phase5-anomaly.sh
│   ├── phase5-notify.sh
│   ├── phase6-validate.sh
│   ├── phase6-guard.sh
│   └── phase6-dispatch.sh
├── metrics/
│   └── YYYYMMDD.jsonl
├── config/
│   └── policy.yaml
└── Makefile
```

---

## 使用例

### ショート動画の自動生成
```
1. /video-agent download <YouTube URL>
2. /video-agent transcribe video.mp4
3. /video-agent produce --type short --style vertical
4. /video-agent validate
5. /video-agent deploy
```

### バッチ処理
```bash
# 複数動画の一括処理
for url in $(cat urls.txt); do
  make phase6-run PHASE=download MODE=batch REASON="Batch download"
done
```

---

## 関連スキル

- `nanobanana-pro` - 画像生成（サムネイル、素材）
- `gpt-sovits-tts` - 音声合成
- `テロップ` - テロップ追加
- `youtube-thumbnail` - サムネイル最適化
