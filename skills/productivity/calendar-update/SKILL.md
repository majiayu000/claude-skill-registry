---
name: calendar-update
description: Google Calendar の予定を更新する。「予定を変更」「イベント編集」「予定を修正」「日程変更」「時間を変える」「場所を変更」などで起動。`/shiiman-google:calendar-update` を実行して予定を更新する。
allowed-tools: [Read, Bash]
---

# Calendar Update

Google Calendar の予定を更新します。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:calendar-update` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:calendar-update` に委譲します（SSOT として扱う）。
