---
name: app-nudge-sender
description: "ユーザーへ送る app nudge を決め、workspace/nudges に保存して配信をトリガーする"
metadata: {"openclaw":{"emoji":"📣","os":["linux"]}}
---

# app-nudge-sender

## 目的
この slot で誰にどの nudge を送るかを決め、結果を `workspace/nudges/decisions_YYYY-MM-DD.json` に書き、そのリストを Railway API に渡してアプリ nudge を配信する。

## 保存先（Anicca 内・フルパス）

| 種類 | フルパス |
|------|----------|
| 判断結果 | `/home/anicca/.openclaw/workspace/nudges/decisions_YYYY-MM-DD.json` |

VPS 相対: `~/.openclaw/workspace/nudges/decisions_YYYY-MM-DD.json`。ユーザー一覧は Railway API から取得。送信は Railway API が行う。

## 命令（プロンプトに渡す文言）

「あなたが、Railway から取得したユーザー一覧とこの slot（morning / afternoon / evening）を見て、この slot で誰にどの nudge を送るかを 1 件ずつ決めよ。結果を **workspace/nudges/decisions_YYYY-MM-DD.json** に書け。書いたら、そのファイルの内容を Railway の API に渡して配信を依頼せよ。」

## 必須 env
| キー | 説明 |
|------|------|
| `API_BASE_URL` | Anicca API ベースURL |
| `INTERNAL_AUTH_SECRET` | admin jobs 認証 |
| `NUDGE_ALPHA_USER_ID` | alpha ルーティング用（オプション） |

## 必須 tools
- `web_fetch`（API 呼び出し）

## 入力
- 通常: body なし。slot は cron のエントリで区別（morning/afternoon/evening）。
- `proactive-app-nudge` 互換: `{ slot: "morning"|"afternoon"|"evening" }` で上書き可能。

## 実行手順
1. Railway API からユーザー一覧を取得する。
2. 上記「命令」に従い、誰に何を送るかを決め、`workspace/nudges/decisions_YYYY-MM-DD.json` に書く。
3. `POST {API_BASE_URL}/api/admin/jobs/app-nudge-sender` にその結果を渡す（または API がファイルを読む方式に合わせる）。API が `/api/mobile/nudge/pending` に enqueue。
4. iOS が pull -> ack で閉ループ。

## 出力 / 監査ログ
- `{ success: true, result }`
- runs/監査に slot と送信数を含める。
- 判断結果は必ず `nudges/decisions_YYYY-MM-DD.json` に残す。

## Slack 報告
**【絶対】** 実行結果・要約は Slack #metrics（チャンネル ID: `C091G3PKHL2`）に投稿する。成功でも失敗でも必ず投稿する。投稿しないことは許されない。

## 失敗時処理
- 5xx: 次回 cron で再実行。
- ユーザー未登録等: スキップして次へ。

## 禁止事項
- センサー依存にしない。固定スロット + server-driven のみ。

## Cron
- `app-nudge-morning`: `0 9 * * *`
- `app-nudge-afternoon`: `0 14 * * *`
- `app-nudge-evening`: `0 20 * * *`
