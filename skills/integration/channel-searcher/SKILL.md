---
name: channel-searcher
description: Slack チャンネルを名前で検索する。「チャンネル検索」「チャンネルを探して」「チャンネル名で検索」「〇〇というチャンネル」「チャンネルを見つけたい」「チャンネルある？」「似た名前のチャンネル」などで起動。Pythonスクリプト `slack_channel.py search` を使用。
allowed-tools: [Bash]
---

# Channel Searcher

Slack チャンネルを名前で検索します。

## ワークフロー

### 1. 検索クエリの確認

ユーザーが探しているチャンネル名を確認

### 2. チャンネル検索

Pythonスクリプトで検索を実行:

```bash
python plugins/shiiman-slack/skills/channel-lister/scripts/slack_channel.py search \
  --query "project" \
  --format table
```

### 3. 結果の表示

検索結果を整形して表示:

```
検索結果: 3 件

id          name            is_private  topic                   num_members
C01234567   project-alpha   false       プロジェクトアルファ    12
C01234568   project-beta    false       プロジェクトベータ      8
C01234569   project-gamma   true        プロジェクトガンマ      5
```

## コマンド連携

実際の処理は `/shiiman-slack:channel-search` に委譲します（SSOT として扱う）。
