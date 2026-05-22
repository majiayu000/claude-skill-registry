---
name: apps-script-search
description: Google Apps Script を検索する。「Apps Script 検索」「GAS 検索」「スクリプト検索」「Apps Script を探して」「GAS を見つけたい」「Google スクリプト検索」「Apps Script の検索」などで起動。`/shiiman-google:apps-script-search` を実行して検索する。
allowed-tools: [Read, Bash]
---

# Apps Script Search

Google Apps Script を検索します。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:apps-script-search` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:apps-script-search` に委譲します（SSOT として扱う）。
