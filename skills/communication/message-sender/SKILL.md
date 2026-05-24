---
name: message-sender
description: Slack にメッセージを送信する。「メッセージ送信」「Slackに投稿」「#channel に送って」「メッセージを送る」「投稿して」「Slackに書き込み」「チャンネルに送信」などで起動。User Token があればユーザーとして投稿、なければ Bot として投稿。
---

# Message Sender

Slack にメッセージを送信します。

## トークンについて

| トークン | 投稿者 | 表示名 |
|---------|--------|--------|
| User Token（xoxp-） | ユーザー本人 | 自分の名前とアイコン |
| Bot Token（xoxb-） | Bot | Bot の名前とアイコン |

**User Token が設定されていない場合**:
Bot としてメッセージを投稿します。ユーザーに「Bot として投稿してよいか」を確認してから実行してください。

## ワークフロー

### 1. 送信先と内容の確認

ユーザーに以下を確認:
- 送信先チャンネル（チャンネル名を指定された場合は ID を調べる）
- メッセージ内容

### 2. トークン状態の確認

```bash
python plugins/shiiman-slack/skills/message-sender/scripts/slack_post.py status
```

User Token の有無を確認し、投稿者を決定。

### 3. 送信前の確認

送信前に必ずユーザーに確認を取る:

**User Token がある場合:**
```
以下の内容でユーザーとして送信してよろしいですか？

チャンネル: #general (C01234567)
メッセージ: お疲れ様です。本日の作業完了しました。
投稿者: あなた（ユーザー名）

[はい/いいえ]
```

**User Token がない場合:**
```
User Token が設定されていないため、Bot として送信します。

チャンネル: #general (C01234567)
メッセージ: お疲れ様です。本日の作業完了しました。
投稿者: Bot

Bot として送信してよろしいですか？
[はい/いいえ]
```

### 4. メッセージ送信

```bash
# ユーザーとして投稿（User Token がある場合のデフォルト）
python plugins/shiiman-slack/skills/message-sender/scripts/slack_post.py post \
  --channel "C01234567" \
  --text "お疲れ様です。本日の作業完了しました。"

# Bot として投稿（明示的に指定）
python plugins/shiiman-slack/skills/message-sender/scripts/slack_post.py post \
  --channel "C01234567" \
  --text "お疲れ様です。本日の作業完了しました。" \
  --as-bot
```

### 5. 送信結果の報告

送信したメッセージのタイムスタンプとチャンネル情報を表示。

## コマンドオプション

| オプション | 必須 | 説明 |
|-----------|------|------|
| `--channel`, `-c` | Yes | チャンネルID |
| `--text`, `-t` | Yes | メッセージテキスト |
| `--as-bot` | No | Bot として投稿（User Token があっても） |

## User Token の設定方法

ユーザーとして投稿するには、`.claude/settings.local.json` に `SLACK_USER_TOKEN` を設定:

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
