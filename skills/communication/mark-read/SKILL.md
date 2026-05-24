---
name: mark-read
description: Slack チャンネルを既読にする。「既読にして」「既読化」「チャンネル既読」「未読を消す」「既読マーク」「全部読んだことにして」「既読にしたい」などで起動。Pythonスクリプト `slack_message.py mark-read` を使用。
allowed-tools: [Bash]
---

# Mark Reader

Slack チャンネルを既読にします（一括既読化）。

## ワークフロー

### 1. チャンネルの確認

既読にするチャンネルを確認

### 2. 既読化前の確認

既読化する前に必ずユーザーに確認を取る:

```
#general の未読を既読にしますか？

[はい/いいえ]
```

### 3. 既読化実行

Pythonスクリプトを実行:

```bash
python plugins/shiiman-slack/skills/check-unread/scripts/slack_message.py mark-read \
  --channel C01234567
```

### 4. 結果の報告

既読化したチャンネル情報を表示
