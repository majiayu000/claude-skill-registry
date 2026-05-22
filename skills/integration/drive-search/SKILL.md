---
name: drive-search
description: Google Drive を検索する。「Drive を検索」「ドライブ検索」「ファイルを探して」「Drive で検索」「Google Drive 検索」「ファイル名で検索」「条件で検索」などで起動。`/shiiman-google:drive-search` を実行して検索結果を取得する。
allowed-tools: [Read, Bash]
---

# Drive Search

Google Drive を検索します。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:drive-search` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:drive-search` に委譲します（SSOT として扱う）。
