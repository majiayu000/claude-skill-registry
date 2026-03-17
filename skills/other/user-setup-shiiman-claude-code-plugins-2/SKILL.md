---
name: user-setup
description: Slack のデフォルトユーザーを設定する。「自分を設定」「ユーザー設定」「デフォルトユーザー設定」「Slackユーザー登録」「自分のIDを設定」「自分のSlackを設定」などで起動。
allowed-tools: [Bash]
---

# User Setup

Slack 操作で使用するデフォルトユーザーID を設定・管理します。

## 概要

このスキルは、shiiman-slack プラグインで使用するデフォルトユーザーID を設定します。
設定されたユーザーID は、メンション確認や未読確認などで自動的に使用されます。

## ワークフロー

### 1. 現在の設定を確認

まず現在の設定を確認：

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_config.py show
```

### 2. ユーザーID の設定

ユーザーが指定したユーザーID を設定：

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_config.py set-user --user-id U01234567
```

**ユーザーID の確認方法**:
- Slack でプロフィールを開く → 「...」→「メンバーIDをコピー」
- または `U` で始まる11文字程度のID

### 3. 設定の削除

設定をクリアしたい場合：

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/slack_config.py clear
```

## 設定ファイル

設定は `~/.config/shiiman-slack/config.json` に保存されます。

```json
{
  "default_user_id": "U01234567",
  "workspace": {
    "team_id": "T01234567",
    "team_name": "MyWorkspace"
  },
  "created_at": "2025-01-14T10:00:00Z",
  "updated_at": "2025-01-14T10:00:00Z"
}
```

## 設定後の利用

設定されたユーザーID は以下のスキルで自動的に使用されます：

- **mention-checker**: 自分へのメンションを確認
- **unread-checker**: 自分の未読メッセージを確認
- **mark-reader**: 自分としてメッセージを既読化
