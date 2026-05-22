---
name: gmail-read
description: Gmail メッセージ本文を表示する。「メール本文」「Gmail 本文を見たい」「メッセージ内容を表示」「メールを開いて」「Gmail を読む」「本文を見せて」「内容確認」などで起動。`/shiiman-google:gmail-read` を実行して本文を取得する。
allowed-tools: [Read, Bash]
---

# Gmail Read

Gmail メッセージ本文を表示します。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:gmail-read` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:gmail-read` に委譲します（SSOT として扱う）。
