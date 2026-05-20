---
name: tiktok-poster
description: "workspace/hooks の slot(9am/9pm) を読んで TikTok に投稿する"
metadata: {"openclaw":{"emoji":"🎵","os":["linux"]}}
---

# tiktok-poster

## 目的
TikTok 投稿の Proposal を作成。steps: `draft_content -> verify_content -> post_tiktok`。TikTok は**投稿のみ**。朝は **slot 9am**、夜は **slot 9pm** の 1 本だけを使う。

## 保存先（Anicca 内・読むだけ）

| データ | フルパス |
|--------|----------|
| キャプション・画像 URL（読む） | **morning:** `~/.openclaw/workspace/hooks/9am/YYYY-MM-DD.json`。**evening:** `~/.openclaw/workspace/hooks/9pm/YYYY-MM-DD.json`。各ファイルの `entries` のうち `platform: "tiktok"` の `caption`、`imageUrl`、`imagePrompt` を参照。 |
| 書き戻し（投稿後） | 投稿完了後、同じ hook ファイルの当該エントリに **imageUrl**（FAL 生成した場合はその URL）と **publicUrl**（Blotato から取得）を上書き保存する。 |

YYYY-MM-DD は今日の日付（Asia/Tokyo）。**imageUrl が空または無い場合:** 同じエントリの **imagePrompt** を FAL API に渡して画像を生成し、得た URL を imageUrl として **backend.blotato.com** 経由で TikTok に投稿する。呼び出す API は **`https://backend.blotato.com/v2/...`**（api.blotato.com は使わない）。投稿後、Blotato の **publicUrl** が取得できるまでポーリングし、取得したら hook の当該エントリに書き戻す。

## 必須 env
| キー | 説明 |
|------|------|
| `BLOTATO_API_KEY` | Blotato API キー（TikTok 投稿に必須） |
| `BLOTATO_TIKTOK_ACCOUNT_ID` | Blotato 上の TikTok アカウント ID（無い場合は `BLOTATO_ACCOUNT_ID_EN`） |
| `FAL_API_KEY` または `FAL_KEY` | Fal.ai API キー（imageUrl が空のとき imagePrompt で画像生成するために必須）。VPS の `~/.openclaw/.env` に `FAL_KEY` を設定すること。 |

## 必須 tools
- `web_fetch`（API）
- TikTok 投稿は **Blotato API のみ**（post_tiktok step で `BLOTATO_*` 使用）。

## 入力
- cron slot 起動時: trigger で proposal 作成。
- `skillName: "tiktok-poster"`, `steps: [draft_content, verify_content, post_tiktok]`。

## 実行手順
1. **読むパス:** cron が morning なら `~/.openclaw/workspace/hooks/9am/YYYY-MM-DD.json`、evening なら `~/.openclaw/workspace/hooks/9pm/YYYY-MM-DD.json`（今日の日付）。
2. **imageUrl が空の場合:** 同じエントリの **imagePrompt** を FAL に渡して画像を生成 → 得た URL を imageUrl として使ってから投稿する。**画像 verify ループ:** 生成後、内容を確認し基準を満たさない場合は imagePrompt を調整して再生成。基準を満たすまで繰り返してから投稿。
3. TikTok 投稿は **Blotato API（backend.blotato.com）** のみ。mission-worker が draft_content -> verify_content -> post_tiktok を順実行。投稿後、publicUrl をポーリングで取得し、当該 hook ファイルのエントリに imageUrl（生成した場合はその値）と publicUrl を書き戻す。
4. 文字数上限 2000、429/5xx のみリトライ、DLQ に非リトライを退避。

## Slack 報告
**【絶対】** 実行結果を Slack #metrics（チャンネル ID: `C091G3PKHL2`）に投稿する。要約禁止。**以下をそのままこの形式で投稿する。**

```
【Slack #metrics に必ず以下の形式で投稿する。要約禁止。】

1. スキル名と結果
   tiktok-poster ({slot}) — :white_check_mark: 投稿成功 / :x: 失敗

2. 日時
   日付と投稿実行時刻（例: 2026-02-15 21:00 JST）

3. 内容（省略禁止）
   - キャプション: 投稿した caption の全文をそのまま貼る。
   - imagePrompt: 使用した画像生成プロンプトの全文をそのまま貼る。

4. TikTok の投稿リンク
   Blotato の **publicUrl** のみ（取得できるまでポーリングする）。他 URL は貼らない。

5. 備考（あれば）
   スキップ理由・imageUrl 空で FAL 生成した等
```

## 出力 / 監査ログ
- `post_tiktok` 完了時: 投稿 ID に加え **publicUrl** を output に含める。
- 失敗時: DLQ + ops event。

## 失敗時処理
- 429/5xx: リトライ（最大3回）。
- その他: DLQ + ops event。

## 禁止事項
- 返信禁止。投稿のみ。
- 文字数 2000 超禁止。

## Cron
- `tiktok-poster-morning`: `0 9 * * *`
- `tiktok-poster-evening`: `0 21 * * *`
