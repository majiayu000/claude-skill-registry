---
name: gmail-mark-read
description: Gmail の未読を既読化する。「既読にする」「未読を既読」「メールを既読化」「Gmail 既読化」「未読を消す」「メールを開封扱い」「一括既読」などで起動。
allowed-tools: [Read, Bash]
---

# Gmail Mark Read

Gmail の未読メッセージを既読化します（単体/一括）。

## 実行方法

### 特定メッセージを既読化

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py mark-read --ids <message-id>
```

### 複数メッセージを一括で既読化

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py mark-read --ids <id1>,<id2>,<id3>
```

### 未読メッセージを一括で既読化

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py mark-read --all
```

### プロファイル指定

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_gmail.py mark-read --profile <profile-name> --all
```

## オプション

- `--ids <id1,id2,...>`: 既読化するメッセージIDのリスト
- `--all`: 全ての未読メッセージを既読化

## 関連操作

- 未読一覧を確認: `gmail-list-unread` を実行

## 注意事項

- トークン未作成の場合は「Google ログイン」と言って認証を行ってください
- `--all` オプションは全ての未読を既読化するため、慎重に使用してください
