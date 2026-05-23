---
name: check-unread
description: Slack の未読メッセージを確認する。「Slack未読確認」「未読メッセージ」「未読ある？」「Slackの未読」「未読を見せて」「未読チェック」「未読メール確認」などで起動。Pythonスクリプト `slack_message.py unread` を使用。
allowed-tools: [Bash]
---

# Unread Checker

Slack の未読メッセージを確認します。

## ワークフロー

### 1. 未読メッセージ取得

Pythonスクリプトで未読メッセージ一覧を取得:

```bash
python plugins/shiiman-slack/skills/check-unread/scripts/slack_message.py unread \
  --format table
```

オプション:
- `--max <number>`: 最大取得件数（デフォルト: 20）
- `--format <table|json>`: 出力形式（デフォルト: table）

### 2. 結果の整形

チャンネルごとに未読メッセージをグループ化して表示:

```
# Slack 未読メッセージ

## #general (5件)
**山田太郎** (10:30)
今日のミーティングは15時からです

**佐藤花子** (10:32)
了解しました！

## #project-alpha (3件)
**田中一郎** (09:15)
PRレビューお願いします
```

### 3. 優先度の提示

未読メッセージの優先度を判断:
- メンション付き: 高優先度
- DMやプライベートチャンネル: 中優先度
- パブリックチャンネル: 通常優先度

## 必要な環境変数

```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
```

## 必要なスコープ

- `channels:read`
- `channels:history`
- `groups:read`
- `groups:history`
- `users:read`
