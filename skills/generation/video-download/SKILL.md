---
name: video-download
description: YouTube等から動画をダウンロード。オフライン視聴、教育コンテンツ保存、クリエイティブ素材収集に使用。
---

# Video Download Skill

yt-dlpを使用した動画ダウンロードスキル。

## When to Use

- オフライン視聴用の動画保存
- 教育コンテンツのアーカイブ
- クリエイティブプロジェクト素材の収集
- ウェビナー・講義の録画保存

## Capabilities

### 対応プラットフォーム

| プラットフォーム | 対応状況 |
|------------------|----------|
| YouTube | ✅ |
| Vimeo | ✅ |
| Twitter/X | ✅ |
| TikTok | ✅ |
| その他1000+サイト | ✅ |

### 品質オプション

| 品質 | 説明 |
|------|------|
| `480p` | SD画質 (容量節約) |
| `720p` | HD画質 (推奨) |
| `1080p` | Full HD |
| `4K` | 最高画質 |
| `best` | 利用可能な最高品質 |

### 出力フォーマット

| フォーマット | 用途 |
|--------------|------|
| `mp4` | 汎用動画 (推奨) |
| `webm` | Web最適化 |
| `mp3` | 音声のみ |
| `m4a` | 高品質音声 |

## Usage

### 単一動画ダウンロード

```bash
# 基本ダウンロード (最高品質)
make video-download URL="https://www.youtube.com/watch?v=xxxxx"

# 品質指定
make video-download URL="https://www.youtube.com/watch?v=xxxxx" QUALITY=720p

# フォーマット指定
make video-download URL="https://www.youtube.com/watch?v=xxxxx" FORMAT=mp4

# 音声のみ
make video-download-audio URL="https://www.youtube.com/watch?v=xxxxx"
```

### プレイリストダウンロード

```bash
# プレイリスト全体
make video-download-playlist URL="https://www.youtube.com/playlist?list=xxxxx"

# 範囲指定
make video-download-playlist URL="..." START=1 END=10
```

### バッチダウンロード

```bash
# URLリストファイルから
make video-download-batch FILE=urls.txt
```

## Output

ダウンロードされたファイルは `local-files/videos/` に保存されます。

```
local-files/videos/
├── [タイトル].mp4           # 動画ファイル
├── [タイトル].jpg           # サムネイル
├── [タイトル].info.json     # メタデータ
└── [タイトル].description   # 説明文
```

## Configuration

### 環境変数 (.env)

```bash
# 出力ディレクトリ
VIDEO_DOWNLOAD_DIR=local-files/videos

# デフォルト品質
VIDEO_DOWNLOAD_QUALITY=best

# デフォルトフォーマット
VIDEO_DOWNLOAD_FORMAT=mp4

# サムネイル保存
VIDEO_DOWNLOAD_THUMBNAIL=true

# メタデータ保存
VIDEO_DOWNLOAD_METADATA=true

# レート制限 (リクエスト/分)
VIDEO_DOWNLOAD_RATE_LIMIT=10
```

## Legal Notice

- 著作権保護されたコンテンツは権利者の許可が必要
- プラットフォームの利用規約を遵守
- 個人使用・教育目的に限定
- 商用利用は適切なライセンス確認が必要

## Troubleshooting

### よくある問題

| 問題 | 解決策 |
|------|--------|
| ダウンロード失敗 | `make video-download-update` でyt-dlp更新 |
| 403エラー | Cookieファイル設定が必要な場合あり |
| 低品質のみ | プラットフォームの制限による |

### 診断コマンド

```bash
# yt-dlpバージョン確認
make video-download-version

# 利用可能フォーマット確認
make video-download-formats URL="..."

# 診断実行
make video-download-doctor
```

## Related Skills

- `video-production` - 動画編集・制作
- `youtube-content` - YouTube動画企画
- `omnihuman1-video` - AIアバター動画
