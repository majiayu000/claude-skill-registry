---
name: review-flow
description: |
    PR作成後に自律的に実行する必要があるフロースキルです。
    Trigger: review, pr created, pr open
argument-hint: [url]
model: opus
---

## Description
PR $1 について理解しPR authorの身になってペアプロセッションを開始します。
レビュワーにわかりやすいように解説をしてください。

## Setup
"gh wt co $1" で対象のworktreeに切り替えます。
もしも異なるリポジトリにいる場合は先に ~/ghq/githtub.com/{owner}/{repo} に移動してください。

## Process
parallelに以下のsubagentsを実行します
- QA subagent を使用して実際のユースケースを想定した動作確認を行います。
- deslop subagent を使用して不要なコードを除去し、pushします
- fixci subagent を使用してCIの問題を修正し、pushします

## Output
以下の項目を報告し、ペアプロセッションを開始してください。
- codemap: コードの解説
- try: 動作確認手順、Shell+Expect
- session: コード理解を促進する幾つかの代理質問  
    - 〇〇のような入力があった場合、どのような挙動になりますか？
    - この処理のパフォーマンスが気になりますが、どの程度の負荷がかかりますか？
