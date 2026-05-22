---
name: drive-permissions
description: Google Drive のファイルの共有設定を確認する。「共有状況確認」「誰がアクセスできる」「共有設定を見せて」「アクセス権確認」「権限一覧」「共有中のユーザー」などで起動。`/shiiman-google:drive-permissions` を実行して共有設定を取得する。
allowed-tools: [Read, Bash]
---

# Drive Permissions

Google Drive のファイルの共有設定を確認します。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:drive-permissions` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:drive-permissions` に委譲します（SSOT として扱う）。
