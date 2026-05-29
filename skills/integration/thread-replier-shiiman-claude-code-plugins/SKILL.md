---
name: thread-replier
description: Slack スレッドに返信する。「スレッドに返信」「スレッド返信して」「このスレッドに返信」「スレッドで返信」「スレッドに投稿」「スレッドに書き込み」「返信をスレッドで」などで起動。User Token があればユーザーとして返信、なければ Bot として返信。
---

# Thread Replier

Slack スレッドに返信します。

## トークンについて

| トークン | 返信者 | 表示名 |
| -------- | ------ | ------ |
| User Token（xoxp-） | ユーザー本人 | 自分の名前とアイコン |
| Bot Token（xoxb-） | Bot | Bot の名前とアイコン |

**User Token が設定されていない場合**:
Bot としてスレッドに返信します。ユーザーに「Bot として返信してよいか」を確認してから実行してください。

## ワークフロー

### 1. スレッド情報の確認

以下を確認:

- チャンネルID
- スレッドのタイムスタンプ（親メッセージのts）
- 返信内容

### 2. トークン状態の確認

```bash
python plugins/shiiman-slack/skills/thread-replier/scripts/slack_thread.py status
```

User Token の有無を確認し、返信者を決定。

### 3. 送信前の確認

送信前に必ずユーザーに確認を取る:

**User Token がある場合:**

```
以下の内容でユーザーとしてスレッドに返信してよろしいですか？

チャンネル: #general (C01234567)
スレッド: 1234567890.123456
返信: 了解しました！
投稿者: あなた（ユーザー名）

[はい/いいえ]
```

**User Token がない場合:**

```
User Token が設定されていないため、Bot として返信します。

チャンネル: #general (C01234567)
スレッド: 1234567890.123456
返信: 了解しました！
投稿者: Bot

Bot として返信してよろしいですか？
[はい/いいえ]
```

### 4. スレッド返信

```bash
# ユーザーとして返信（User Token がある場合のデフォルト）
python plugins/shiiman-slack/skills/thread-replier/scripts/slack_thread.py reply \
  --channel "C01234567" \
  --thread-ts "1234567890.123456" \
  --text "了解しました！"

# Bot として返信（明示的に指定）
python plugins/shiiman-slack/skills/thread-replier/scripts/slack_thread.py reply \
  --channel "C01234567" \
  --thread-ts "1234567890.123456" \
  --text "了解しました！" \
  --as-bot
```

### 5. 送信結果の報告

送信した返信のタイムスタンプとスレッド情報を表示。

## コマンドオプション

| オプション | 必須 | 説明 |
| ---------- | ---- | ---- |
| `--channel`, `-c` | Yes | チャンネルID |
| `--thread-ts`, `-t` | Yes | スレッドのタイムスタンプ |
| `--text`, `-m` | Yes | 返信テキスト |
| `--as-bot` | No | Bot として返信（User Token があっても） |

## User Token の設定方法

ユーザーとして返信するには、`.claude/settings.local.json` に `SLACK_USER_TOKEN` を設定:

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
