---
name: ops-heartbeat
description: "閉ループ ops のハートビート。proposals/steps を評価し次の step を生成する"
metadata: {"openclaw":{"emoji":"🫀","os":["linux"]}}
---

# ops-heartbeat

## 目的
閉ループ制御プレーン。trigger/reaction/recovery を進め、次の Proposal/Mission/Step を **Anicca 内** に生成・保存する。Railway の heartbeat API は使わない。

## 保存先（Anicca 内・フルパス）

| データ | フルパス |
|--------|----------|
| heartbeat 状態 | `/home/anicca/.openclaw/workspace/ops/heartbeat_state.json` |
| 提案一覧（proposals） | `/home/anicca/.openclaw/workspace/ops/proposals.json`（または日付別 `proposals/YYYY-MM-DD.json`） |

VPS 上の相対パス: `~/.openclaw/workspace/ops/heartbeat_state.json` および `~/.openclaw/workspace/ops/proposals.json`。

## 必須 env
| キー | 説明 |
|------|------|
| （他 API 呼び出しが必要な場合のみ、その API 用の env を置く） |  |

## 必須 tools
- `web_fetch` または同等（API 呼び出し用）
- ファイル読み書き（上記 ops パスへの読み書き）

## 入力
なし（cron 起動）。

## 実行手順
1. **Anicca 内の状態を読む:** `heartbeat_state.json` と必要に応じて `proposals.json` を読む。
2. trigger/reaction/recovery のロジックを実行し、次の Proposal/Mission/Step を決定する。
3. **Anicca 内に書く:** 結果を `heartbeat_state.json` に書き、新規提案があれば `proposals.json`（または日付別ファイル）に追記する。`steps.json` に実行すべき step を追加する（mission-worker がここを読む）。
4. 監査用に `triggers`, `reactions`, `insights`, `stale` をログまたは同一 ops 配下の監査ファイルに記録する。**Railway の `POST .../api/ops/heartbeat` は呼ばない。**

## 出力 / 監査ログ
- `{ ok: true, elapsed, triggers, reactions, insights, stale }`
- 失敗時は `{ ok: false, error }`

## Slack 報告
**【絶対】** 実行結果・要約は Slack #metrics（チャンネル ID: `C091G3PKHL2`）に投稿する。成功でも失敗でも必ず投稿する。投稿しないことは許されない。

## 失敗時処理
- 5xx: リトライは heartbeat 側で次回 cron に任せる（冪等）。
- ネットワークエラー: 次回 cron で再実行。

## 禁止事項
- なし（読み取り・制御のみ、送信しない）。

## Cron
`*/5 * * * *` (5分ごと)
