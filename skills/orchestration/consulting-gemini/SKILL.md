---
name: consulting-gemini
description: >
  Google Gemini CLIを使用した計画レビュー、実装チェック、調査タスクのための相談。
  トリガー: /think完了, /code完了, /research実行,
  計画レビュー, 実装確認, 調査依頼, Geminiに相談.
allowed-tools: [Bash, Read]
user-invocable: false
---

# Geminiへの相談

## コマンド

```bash
gemini "[プロンプト]" --output-format text --approval-mode yolo
```

## ルール

- ユーザーに提示: 提案を鵜呑みにしない
- 検証: Gemini は古いデータの可能性あり
- フォールバック: CLI 失敗時はワークフロー続行
