---
name: calendar-delete
description: Google Calendar の予定を削除する。「予定を削除」「イベント削除」「予定をキャンセル」「予定を消して」「イベントを消して」などで起動。`/shiiman-google:calendar-delete` を実行して予定を削除する。
allowed-tools: [Read, Bash]
---

# Calendar Delete

Google Calendar の予定を削除します。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:calendar-delete` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:calendar-delete` に委譲します（SSOT として扱う）。
