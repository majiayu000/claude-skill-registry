---
name: copilot-delegate
description: Copilot CLIに処理を委譲するスキル。ユーザーが「Copilotに聞いて」「Copilotで確認して」「Copilotに任せて」などと明示的に依頼したときに使用する。GitHub Copilot CLIの機能を活用して、コマンドの提案やGit操作の説明などを取得する。
---

# Copilot Delegate

GitHub Copilot CLIに処理を委譲し、その結果を返す。

## 使用方法

ユーザーが明示的にCopilotへの委譲を依頼した場合、以下のコマンドを実行する：

```bash
copilot -p "依頼内容"
```

## トリガー例

- 「Copilotに聞いて」
- 「Copilotで確認して」
- 「Copilotに任せて」
- 「Copilotに相談して」

## 実行手順

1. ユーザーの依頼内容を抽出する
2. `copilot -p "依頼内容"` を実行する
3. 結果をそのままユーザーに返す

## 注意事項

- Copilot CLIがインストールされていない場合はエラーになる
- 結果はCopilot CLIの出力をそのまま表示する
