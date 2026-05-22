---
name: docs-export
description: Google Docs をエクスポートする。「Docs を PDF で」「ドキュメントをエクスポート」「Docs をダウンロード」「ドキュメントを PDF に」「Word で保存」などで起動。`/shiiman-google:docs-export` を実行してエクスポートする。
allowed-tools: [Read, Bash]
---

# Docs Export

Google Docs をファイルにエクスポートします。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:docs-export` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:docs-export` に委譲します（SSOT として扱う）。
