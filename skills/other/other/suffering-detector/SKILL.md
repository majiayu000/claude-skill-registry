---
name: suffering-detector
description: "苦しみ/危機を検知して findings を workspace に保存し、必要なら SAFE-T interrupt を行う"
metadata: {"openclaw":{"emoji":"🚨","os":["linux"]}}
---

# suffering-detector

## 目的
web_search 等で「苦しみ/危機」を検知し、`detections[]` を作成。severity>=0.9 は SAFE-T として `crisis:detected` を emit、Slack 通知で interrupt。

## 保存先（Anicca 内・フルパス）

| 種類 | フルパス |
|------|----------|
| 検知結果 | `/home/anicca/.openclaw/workspace/suffering/findings_YYYY-MM-DD.json` |

VPS 相対: `~/.openclaw/workspace/suffering/findings_YYYY-MM-DD.json`。

## 必須 env
| キー | 説明 |
|------|------|
| （Slack 通知用等、必要に応じて） |  |

## 必須 tools
- `web_fetch`（検知ロジック内で外部 API 利用時）
- `web_search`（苦しみ/危機の検知用）

## 入力
- 通常: なし（cron 起動）。
- E2E 検証: 合成フィードをファイル等で渡す方式は実装に従う。

## 実行手順
1. VPS 上で feed を処理し、detections を作成する。
2. severity>=0.9 は `crisis:detected` emit + Slack 通知する。
3. 結果を `workspace/suffering/findings_YYYY-MM-DD.json` に書く。

## 出力 / 監査ログ
- crisis 時は Slack #agents に通知。
- 検知結果を上記パスに記録。

## Slack 報告
**【絶対】** 実行結果を Slack #metrics（チャンネル ID: `C091G3PKHL2`）に投稿する。要約禁止。**以下をそのままこの形式で投稿する。**

```
【Slack #metrics に必ず以下の形式で投稿する。要約禁止。】

1. スキル名と結果
   suffering-detector — :white_check_mark: 完了（検知N件） / :x: 失敗 / :rotating_light: SAFE-T 発動

2. 日時
   実行日付と時刻（例: 2026-02-15 06:05 UTC）

3. 結果（そのまま）
   - 検知件数と各 severity（例: 検知3件、max severity 0.4）
   - crisis 検出の有無（SAFE-T 要/不要）
   - workspace/suffering/findings_YYYY-MM-DD.json の内容を整形してそのまま貼る（全文。要約・省略禁止）

4. 備考（あれば）
   スキップ理由・エラー等
```

## 失敗時処理
- 5xx: 次回 cron で再実行（冪等）。
- 合成フィード不正: 終了。

## 禁止事項
- なし（検知のみ、送信しない）。

## Cron
`*/5 * * * *` (5分ごと)
