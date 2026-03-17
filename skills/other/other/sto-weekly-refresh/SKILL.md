---
name: sto-weekly-refresh
description: "週次の最適化更新（STO）を行い、結果を workspace に保存する"
metadata: {"openclaw":{"emoji":"🗓️","os":["linux"]}}
---

# sto-weekly-refresh

## 目的
STO（Schedule/Trigger/Observation）の週次リフレッシュ。UserStoModel 等を更新。投稿時間最適化の週次更新。

## 保存先（Anicca 内・フルパス）

| 種類 | フルパス |
|------|----------|
| 実行結果 | `/home/anicca/.openclaw/workspace/sto-weekly-refresh/run_YYYY-MM-DD.json` |

VPS 相対: `~/.openclaw/workspace/sto-weekly-refresh/run_YYYY-MM-DD.json`。

## 必須 env
| キー | 説明 |
|------|------|
| （実装が参照する DB 等があればその認証） |  |

## 必須 tools
- `web_fetch`（実装で API 利用する場合）

## 入力
- なし（cron 起動）。

## 実行手順
1. VPS 上で STO 週次リフレッシュを実行する。
2. 結果を `workspace/sto-weekly-refresh/run_YYYY-MM-DD.json` に書く。
3. UserStoModel 更新数を記録する。

## 出力 / 監査ログ
- 上記パスに結果を記録。

## Slack 報告
**【絶対】** 実行結果・要約は Slack #metrics（チャンネル ID: `C091G3PKHL2`）に投稿する。成功でも失敗でも必ず投稿する。投稿しないことは許されない。

## 失敗時処理
- 5xx: 次回 cron（翌週）で再実行。

## 禁止事項
- なし。

## Cron
`0 3 * * 0` (日曜 03:00 JST)
