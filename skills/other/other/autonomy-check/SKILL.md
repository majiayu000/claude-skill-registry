---
name: autonomy-check
description: "運用監査。失敗率やDLQなどをチェックし、結果を workspace に保存する"
metadata: {"openclaw":{"emoji":"🧯","os":["linux"]}}
---

# autonomy-check

## 目的
規約違反（X 返信ゼロ等）、DLQ 滞留、失敗率等を合否判定し通知。長期運用で劣化しないよう自己点検。

## 保存先（Anicca 内・フルパス）

| 種類 | フルパス |
|------|----------|
| 監査ログ | `/home/anicca/.openclaw/workspace/autonomy-check/audit_YYYY-MM-DD.json` |

VPS 相対: `~/.openclaw/workspace/autonomy-check/audit_YYYY-MM-DD.json`。cron で直接起動し、結果を上記に書く。

## 必須 env
| キー | 説明 |
|------|------|
| （必要に応じて Slack 等の通知用） |  |

## 必須 tools
- `web_fetch`（通知・外部 API 用）

## 入力
- なし（cron 起動）。

## 実行手順
1. VPS 上で規約違反・DLQ 滞留・失敗率をチェックする。
2. 違反検出時は Slack 通知する。
3. 結果を `workspace/autonomy-check/audit_YYYY-MM-DD.json` に書く。

## 出力 / 監査ログ
- 合否判定結果を上記パスに記録。

## Slack 報告
**【絶対】** 実行結果・要約は Slack #metrics（チャンネル ID: `C091G3PKHL2`）に投稿する。成功でも失敗でも必ず投稿する。投稿しないことは許されない。

## 失敗時処理
- 5xx（外部 API 利用時）: 次回 cron で再実行。
- 違反検出: Slack 通知後も次回実行は継続。

## 禁止事項
- なし。

## Cron
`0 3 * * *` (03:00 JST 毎日)
