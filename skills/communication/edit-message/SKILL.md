---
name: edit-message
description: Slack メッセージを編集する。「メッセージ編集」「さっきのを修正」「メッセージ修正」「訂正して」「編集して」「メッセージを直す」「内容を変更」などで起動。User Token があれば自分の投稿を編集可能、なければ Bot 投稿のみ編集可能。
allowed-tools: [Bash]
---

# Message Editor

Slack メッセージを編集します。

## トークンについて

| トークン | 編集可能な投稿 |
| -------- | -------------- |
| User Token（xoxp-） | 自分の投稿 |
| Bot Token（xoxb-） | Bot の投稿のみ |

**User Token が設定されていない場合**:
Bot 投稿のみ編集可能です。自分の投稿を編集したい場合は SLACK_USER_TOKEN の設定が必要であることを通知してください。

## ワークフロー

### 1. 編集対象の確認

以下を確認:

- チャンネルID
- メッセージのタイムスタンプ
- 新しいメッセージ内容

### 2. トークン状態の確認

```bash
python plugins/shiiman-slack/skills/unread-checker/scripts/slack_message.py status
```

User Token の有無を確認し、編集可能な投稿を判定。

### 3. 編集前の確認

編集前に必ずユーザーに確認を取る:

**User Token がある場合:**

```
以下のメッセージを編集してよろしいですか？

チャンネル: #general (C01234567)
タイムスタンプ: 1234567890.123456
新しい内容: 訂正: お疲れ様でした
編集者: あなた（ユーザー名）

[はい/いいえ]
```

**User Token がない場合:**

```
User Token が設定されていないため、Bot 投稿のみ編集可能です。

チャンネル: #general (C01234567)
タイムスタンプ: 1234567890.123456
新しい内容: 訂正: お疲れ様でした

この Bot 投稿を編集してよろしいですか？
[はい/いいえ]

※ 自分の投稿を編集するには SLACK_USER_TOKEN を設定してください。
```

### 4. メッセージ編集

```bash
# ユーザーとして編集（User Token がある場合のデフォルト）
python plugins/shiiman-slack/skills/unread-checker/scripts/slack_message.py edit \
  --channel C01234567 \
  --ts 1234567890.123456 \
  --text "訂正: お疲れ様でした"

# Bot として編集（明示的に指定）
python plugins/shiiman-slack/skills/unread-checker/scripts/slack_message.py edit \
  --channel C01234567 \
  --ts 1234567890.123456 \
  --text "訂正: お疲れ様でした" \
  --as-bot
```

### 5. 結果の報告

編集したメッセージの情報を表示。

## コマンドオプション

| オプション | 必須 | 説明 |
| ---------- | ---- | ---- |
| `--channel` | Yes | チャンネルID |
| `--ts` | Yes | メッセージのタイムスタンプ |
| `--text` | Yes | 新しいメッセージテキスト |
| `--as-bot` | No | Bot として編集（User Token があっても） |

## User Token の設定方法

自分の投稿を編集するには、`.claude/settings.local.json` に `SLACK_USER_TOKEN` を設定:

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
