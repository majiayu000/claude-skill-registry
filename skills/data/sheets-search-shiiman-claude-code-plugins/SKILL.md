---
name: sheets-search
description: Google Sheets を検索する。「Sheets 検索」「スプレッドシート検索」「Google Sheets 検索」「シートを探して」「スプレッドシートを検索」「Sheets を見つけたい」「Google スプレッドシート検索」などで起動。`/shiiman-google:sheets-search` を実行して検索する。
allowed-tools: [Read, Bash]
---

# Sheets Search

Google Sheets を検索します。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:sheets-search` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:sheets-search` に委譲します（SSOT として扱う）。
