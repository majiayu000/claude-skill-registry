---
name: thread-user-lister
description: スレッドの参加者一覧を取得する。「スレッド参加者」「誰がいる？」「このスレッドの参加者」「スレッドメンバー」「スレッドのユーザー」「誰が返信してる」「参加者を見せて」などで起動。Pythonスクリプト `slack_message.py thread-users` を使用。
allowed-tools: [Bash]
---

# Thread User Lister

スレッドの参加者一覧を取得します。

## ワークフロー

### 1. スレッド情報の確認

以下を確認:
- チャンネルID
- スレッドのタイムスタンプ

### 2. 参加者一覧取得

Pythonスクリプトを実行:

```bash
python plugins/shiiman-slack/skills/mention-checker/scripts/slack_message.py thread-users \
  --channel C01234567 \
  --ts 1234567890.123456 \
  --format table
```

### 3. 結果の表示

スレッド参加者を表示:

```
スレッド参加者数: 3

user_id      user_name
U01234567    山田太郎
U01234568    佐藤花子
U01234569    田中一郎
```

## コマンド連携

実際の処理は `/shiiman-slack:thread-users` に委譲します（SSOT として扱う）。
