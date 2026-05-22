---
name: sheets-export
description: Google Sheets をエクスポートする。「Sheets を CSV で」「スプレッドシートをエクスポート」「Sheets をダウンロード」「Excel で保存」「CSV に変換」などで起動。`/shiiman-google:sheets-export` を実行してエクスポートする。
allowed-tools: [Read, Bash]
---

# Sheets Export

Google Sheets をファイルにエクスポートします。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:sheets-export` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:sheets-export` に委譲します（SSOT として扱う）。
