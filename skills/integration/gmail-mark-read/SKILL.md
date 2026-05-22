---
name: gmail-mark-read
description: Gmail の未読を既読化する。「既読にする」「未読を既読」「メールを既読化」「Gmail 既読化」「未読を消す」「メールを開封扱い」「一括既読」などで起動。`/shiiman-google:gmail-mark-read` を実行して既読化する。
allowed-tools: [Read, Bash]
---

# Gmail Mark Read

Gmail の未読を既読化します。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:gmail-mark-read` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:gmail-mark-read` に委譲します（SSOT として扱う）。
