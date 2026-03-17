---
name: consulting-gemini
description: >
  Google Gemini CLIを使用した計画レビュー、実装チェック、調査。
  計画のセカンドオピニオン、実装アプローチの検証が必要な時、または
  計画レビュー, 実装確認, 調査依頼, Geminiに相談 に言及した時に使用。
allowed-tools: [Bash, Read]
user-invocable: false
---

# Geminiへの相談

## コマンド

```bash
gemini "[プロンプト]" --output-format text --sandbox
```

## ルール

- ユーザーに提示: 提案を鵜呑みにしない
- 検証: Geminiは古いデータの可能性あり
- フォールバック: CLI失敗時はワークフロー続行
