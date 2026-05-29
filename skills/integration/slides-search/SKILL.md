---
name: slides-search
description: Google Slides を検索する。「Slides 検索」「スライド検索」「Google Slides 検索」「プレゼンを探して」「スライドを検索」「Slides を見つけたい」「Google スライド検索」などで起動。`/shiiman-google:slides-search` を実行して検索する。
allowed-tools: [Read, Bash]
---

# Slides Search

Google Slides を検索します。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:slides-search` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:slides-search` に委譲します（SSOT として扱う）。
