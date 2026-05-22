---
name: drive-list
description: Google Drive のファイル一覧を取得する。「Drive 一覧」「ドライブのファイルを見たい」「最近のファイル」「Drive の一覧を出して」「ファイルリスト」「Google Drive 一覧」「ドライブを表示」などで起動。`/shiiman-google:drive-list` を実行して一覧を取得する。
allowed-tools: [Read, Bash]
---

# Drive List

Google Drive のファイル一覧を取得します。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:drive-list` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:drive-list` に委譲します（SSOT として扱う）。
