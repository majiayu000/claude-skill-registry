---
name: gmail-star
description: Gmail のメッセージをスター化/解除する。「スターを付けて」「スター化」「星を付ける」「スター解除」「星を外す」「Gmail スター」「スターを消す」などで起動。`/shiiman-google:gmail-star` を実行してスター化/解除する。
allowed-tools: [Read, Bash]
---

# Gmail Star

Gmail のメッセージをスター化/解除します。

## ワークフロー

### 1. コマンド実行

`/shiiman-google:gmail-star` を SlashCommand ツールで実行（実装は Commands に委譲）。

## コマンド連携

実際の処理は `/shiiman-google:gmail-star` に委譲します（SSOT として扱う）。
