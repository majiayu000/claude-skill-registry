---
name: list-channels
description: Slack チャンネル一覧を取得する。「Slackチャンネル一覧」「チャンネルリスト」「Slackのチャンネル」「チャンネル見せて」「全チャンネル」「チャンネル確認」「どんなチャンネルがある」などで起動。公式Slack MCPの `slack_list_channels` を使用。
allowed-tools: [FetchMcpResource]
---

# Channel Lister

Slack チャンネル一覧を取得します。

## ワークフロー

### 1. チャンネル一覧取得

公式Slack MCPの `slack_list_channels` ツールを呼び出す:

```
slack_list_channels()
```

### 2. 結果の整形

チャンネル一覧を整形して表示:

```
# Slack チャンネル一覧

| チャンネル | 説明 | メンバー数 |
|------------|------|-----------|
| #general | 全体連絡用 | 50 |
| #random | 雑談 | 45 |
```
