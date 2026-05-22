---
name: gmail-search
description: Gmail でメールを検索する。「メール検索」「メールを探して」「Gmail 検索」「メールを検索して」「○○からのメール」「件名で検索」などで起動。`/shiiman-google:gmail-search` を実行してメールを検索する。
allowed-tools: [Read, Bash]
---

# Gmail Search

Gmail でメールを検索します。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:gmail-search` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:gmail-search` に委譲します（SSOT として扱う）。
