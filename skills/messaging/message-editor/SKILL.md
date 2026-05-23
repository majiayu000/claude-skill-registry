---
name: message-editor
description: Slack メッセージを編集する。「メッセージ編集」「さっきのを修正」「メッセージ修正」「訂正して」「編集して」「メッセージを直す」「内容を変更」などで起動。Pythonスクリプト `slack_message.py edit` を使用。
allowed-tools: [Bash]
---

# Message Editor

Slack メッセージを編集します。

## ワークフロー

### 1. 編集対象の確認

以下を確認:
- チャンネルID
- メッセージのタイムスタンプ
- 新しいメッセージ内容

### 2. 編集前の確認

編集前に必ずユーザーに確認を取る:

```
以下のメッセージを編集してよろしいですか？

チャンネル: #general
タイムスタンプ: 1234567890.123456
新しい内容: 訂正: お疲れ様でした

[はい/いいえ]
```

### 3. メッセージ編集

Pythonスクリプトを実行:

```bash
python plugins/shiiman-slack/skills/unread-checker/scripts/slack_message.py edit \
  --channel C01234567 \
  --ts 1234567890.123456 \
  --text "訂正: お疲れ様でした"
```

### 4. 結果の報告

編集したメッセージの情報を表示

## 注意事項

- Bot が投稿したメッセージのみ編集可能です
- 他のユーザーが投稿したメッセージは編集できません

## コマンド連携

実際の処理は `/shiiman-slack:message-edit` に委譲します（SSOT として扱う）。
