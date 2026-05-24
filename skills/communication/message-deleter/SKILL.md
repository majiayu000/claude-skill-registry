---
name: message-deleter
description: Slack メッセージを削除する。「メッセージ削除」「さっきのを消して」「メッセージを消す」「削除して」「メッセージ取り消し」「投稿を削除」「このメッセージ削除」などで起動。User Token があれば自分の投稿を削除可能、なければ Bot 投稿のみ削除可能。
---

# Message Deleter

Slack メッセージを削除します。

## トークンについて

| トークン | 削除可能な投稿 |
| -------- | -------------- |
| User Token（xoxp-） | 自分の投稿 |
| Bot Token（xoxb-） | Bot の投稿のみ |

**User Token が設定されていない場合**:
Bot 投稿のみ削除可能です。自分の投稿を削除したい場合は SLACK_USER_TOKEN の設定が必要であることを通知してください。

## ワークフロー

### 1. 削除対象の確認

以下を確認:

- チャンネルID
- メッセージのタイムスタンプ

### 2. トークン状態の確認

```bash
python plugins/shiiman-slack/skills/unread-checker/scripts/slack_message.py status
```

User Token の有無を確認し、削除可能な投稿を判定。

### 3. 削除前の確認

削除前に必ずユーザーに確認を取る:

**User Token がある場合:**

```
以下のメッセージを削除してよろしいですか？

チャンネル: #general (C01234567)
タイムスタンプ: 1234567890.123456
削除者: あなた（ユーザー名）

⚠️ 注意: 削除は取り消しできません

[はい/いいえ]
```

**User Token がない場合:**

```
User Token が設定されていないため、Bot 投稿のみ削除可能です。

チャンネル: #general (C01234567)
タイムスタンプ: 1234567890.123456

この Bot 投稿を削除してよろしいですか？
⚠️ 注意: 削除は取り消しできません

[はい/いいえ]

※ 自分の投稿を削除するには SLACK_USER_TOKEN を設定してください。
```

### 4. メッセージ削除

```bash
# ユーザーとして削除（User Token がある場合のデフォルト）
python plugins/shiiman-slack/skills/unread-checker/scripts/slack_message.py delete \
  --channel C01234567 \
  --ts 1234567890.123456

# Bot として削除（明示的に指定）
python plugins/shiiman-slack/skills/unread-checker/scripts/slack_message.py delete \
  --channel C01234567 \
  --ts 1234567890.123456 \
  --as-bot
```

### 5. 結果の報告

削除したメッセージの情報を表示。

## コマンドオプション

| オプション | 必須 | 説明 |
| ---------- | ---- | ---- |
| `--channel` | Yes | チャンネルID |
| `--ts` | Yes | メッセージのタイムスタンプ |
| `--as-bot` | No | Bot として削除（User Token があっても） |

## 注意事項

- 削除は取り消しできません
- 他のユーザーの投稿は削除できません

## User Token の設定方法

自分の投稿を削除するには、`.claude/settings.local.json` に `SLACK_USER_TOKEN` を設定:

```json
{
  "mcpServers": {
    "slack": {
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-bot-token",
        "SLACK_USER_TOKEN": "xoxp-your-user-token"
      }
    }
  }
}
```

User Token には `chat:write` スコープが必要です。
