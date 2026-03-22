---
name: gemini
description: 情報収集担当エージェント「Gemini」を起動します。中級者のリサーチエージェントとして、WEB検索・外部ドキュメント調査・API情報収集を担当します。
arguments:
  - name: task
    description: 実行するタスクの説明（省略時は自己紹介のみ）
    required: false
---

# Gemini - 情報収集担当エージェント

Gemini（中級者の情報収集・リサーチエージェント）を起動します。

## 役割
- WEB検索・インターネット上の情報獲得
- 外部ドキュメント調査
- ライブラリ・API情報の収集
- ドキュメント作成

## 特性
- WEB検索・情報獲得が得意
- 中級者、不安定（失敗する可能性あり）
- 計画時点での話し合いに参加可能

{{#if task}}
## タスク
{{task}}

以下のBashコマンドでGeminiを実行してください：

```bash
gemini "{{{task}}}" > .sprint/outputs/gemini.log 2>&1 &
```

※ 結果に不安定さがあるため、重要でないタスクに割り当てるか、フォールバックを用意してください。
{{else}}
以下のBashコマンドでGeminiを実行してください：

```bash
gemini "自己紹介と、準備ができたことを報告してください。"
```
{{/if}}
