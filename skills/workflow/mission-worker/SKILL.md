---
name: mission-worker
description: "workspace/ops/steps.json を処理して step を実行し、completed に記録するワーカー"
metadata: {"openclaw":{"emoji":"⚙️","os":["linux"]}}
---

# mission-worker

## 目的
閉ループ実行エンジン。**Anicca 内の step キュー**から「次にやる step」を取得し、step_kind に応じた executor を実行し、結果を **Anicca 内の完了記録** に書く。Railway の step API は使わない。

## 保存先（Anicca 内・フルパス）

| データ | フルパス |
|--------|----------|
| 未実行 step キュー（読む） | `/home/anicca/.openclaw/workspace/ops/steps.json` |
| 完了した step（書く） | `/home/anicca/.openclaw/workspace/ops/completed/YYYY-MM-DD.json`（日付別に追記） |

VPS 上の相対パス: `~/.openclaw/workspace/ops/steps.json` および `~/.openclaw/workspace/ops/completed/`。

## 必須 env
| キー | 説明 |
|------|------|
| （step 実行に必要な Blotato / X 等の env は各 executor の SKILL に従う） |  |

## 必須 tools
- `web_fetch`（API 呼び出し）
- step_kind ごとの executor が要求する tools（例: web_search, twitter, tiktok 等）

## 入力
なし（cron 起動）。

## 実行手順（実装）
1. **steps.json** を読む（`/home/anicca/.openclaw/workspace/ops/steps.json`）。先頭 1 件を「次にやる step」として claim する（取り出しまたは inProgress マーク）。
2. キューが空なら `{ ok: true, reason: "queue_empty" }` として終了。
3. `step.stepKind` ごとの executor を実行（最低限: `noop` でも可）。失敗時は `status=failed`。
4. 完了したら **Anicca 内に記録する:** 当日の `workspace/ops/completed/YYYY-MM-DD.json` に `{ id, stepKind, status, output, error, events, completedAt }` を追記し、**steps.json からその step を削除**（または consumed としてマーク）。Railway の `PATCH .../step/{id}/complete` は呼ばない。

## 出力 / 監査ログ
- step 取得・実行・完了を **Anicca 内** の `workspace/ops/completed/YYYY-MM-DD.json` に記録。
- events は同一ファイルの `events` 配列に含める（または ops 配下の監査ログに出力）。

## Slack 報告
**【絶対】** 実行結果・要約は Slack #metrics（チャンネル ID: `C091G3PKHL2`）に投稿する。成功でも失敗でも必ず投稿する。投稿しないことは許されない。

## 失敗時処理
- executor 失敗: `status: failed`, `error` を付けて complete。
- ネットワークエラー: 次回 cron で再 claim 可能（running のまま stale になる場合は staleRecovery で処理）。

## 禁止事項
- X 返信禁止（post_x は投稿のみ）。
- TikTok 返信禁止。

## Cron
`* * * * *` (毎分)
