---
name: forms-responses
description: Google Forms の回答を取得する。「フォームの回答」「回答結果を見せて」「フォーム回答取得」「アンケート結果」「回答一覧」「フォームの結果」などで起動。`/shiiman-google:forms-responses` を実行して回答を取得する。
allowed-tools: [Read, Bash]
---

# Forms Responses

Google Forms の回答を取得します。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:forms-responses` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:forms-responses` に委譲します（SSOT として扱う）。
