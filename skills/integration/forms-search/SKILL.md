---
name: forms-search
description: Google Forms を検索する。「Forms 検索」「フォーム検索」「Google Forms 検索」「フォームを探して」「Forms を見つけたい」「アンケート検索」「Google フォーム検索」などで起動。`/shiiman-google:forms-search` を実行して検索する。
allowed-tools: [Read, Bash]
---

# Forms Search

Google Forms を検索します。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:forms-search` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:forms-search` に委譲します（SSOT として扱う）。
