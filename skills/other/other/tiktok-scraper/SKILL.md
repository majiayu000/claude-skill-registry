---
name: tiktok-scraper
description: "Apify の clockworks~tiktok-scraper を使って TikTok トレンドを検索する"
metadata: {"openclaw":{"emoji":"📱","os":["linux"]}}
---

# tiktok-scraper

trend-hunter が TikTok トレンドを収集するために使うスキル。Apify Actor `clockworks~tiktok-scraper` を API 経由で実行する。

## 必須 env

| キー | 説明 |
|------|------|
| `APIFY_API_TOKEN` | Apify API トークン（`~/.openclaw/.env` に設定） |

## 使い方

### 1. Actor を実行（POST）

```bash
curl -s -X POST \
  "https://api.apify.com/v2/acts/clockworks~tiktok-scraper/runs?token=${APIFY_API_TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{
    "searchQueries": ["meditation", "習慣", "mindfulness"],
    "resultsPerPage": 20,
    "shouldDownloadVideos": false,
    "shouldDownloadCovers": false
  }'
```

レスポンスから `data.id`（run ID）を取得。

### 2. 結果を取得（GET）

実行完了を待ってから（数十秒〜数分）:

```bash
curl -s "https://api.apify.com/v2/actor-runs/${RUN_ID}/dataset/items?token=${APIFY_API_TOKEN}"
```

### 3. 実行ステータス確認

```bash
curl -s "https://api.apify.com/v2/actor-runs/${RUN_ID}?token=${APIFY_API_TOKEN}"
```

`data.status` が `SUCCEEDED` になるまでポーリング（10秒間隔、最大 5 分）。

## 代替: 同期実行（小規模検索向け）

少量の検索なら同期で結果を直接取得:

```bash
curl -s -X POST \
  "https://api.apify.com/v2/acts/clockworks~tiktok-scraper/run-sync-get-dataset-items?token=${APIFY_API_TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{
    "searchQueries": ["meditation anxiety"],
    "resultsPerPage": 10,
    "shouldDownloadVideos": false,
    "shouldDownloadCovers": false
  }'
```

## レスポンスから使うフィールド

| フィールド | 説明 |
|------------|------|
| `text` | 動画のキャプション |
| `diggCount` | いいね数 |
| `shareCount` | シェア数 |
| `playCount` | 再生数 |
| `commentCount` | コメント数 |
| `createTimeISO` | 投稿日時 |
| `webVideoUrl` | 動画 URL |
| `authorMeta.name` | 投稿者名 |
| `hashtags` | ハッシュタグ配列 |

## trend-hunter での使い方

trend-hunter は上記 API を呼び、`playCount` や `diggCount` が高い動画のキャプション・ハッシュタグをトレンド候補として `trends/YYYY-MM-DD.json` に書く。

## Slack 報告
**【絶対】** 実行結果・要約は Slack #metrics（チャンネル ID: `C091G3PKHL2`）に投稿する。成功でも失敗でも必ず投稿する。投稿しないことは許されない。

## 禁止事項

- 動画のダウンロードはしない（`shouldDownloadVideos: false`）
- Apify クレジットの無駄遣いを避けるため、`resultsPerPage` は 20 以下にする
