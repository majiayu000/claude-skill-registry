---
name: drive-share
description: Google Drive のファイルを共有する。「ファイルを共有」「共有設定」「共有して」「リンク共有」「アクセス権を追加」「閲覧権限を付与」などで起動。`/shiiman-google:drive-share` を実行して共有設定を変更する。
allowed-tools: [Read, Bash]
---

# Drive Share

Google Drive のファイルを共有します。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:drive-share` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:drive-share` に委譲します（SSOT として扱う）。
