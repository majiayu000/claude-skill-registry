---
name: read-thread
description: Slack スレッドの返信を取得する。「スレッドを読む」「スレッドの返信を見せて」「スレッド内容」「スレッド確認」「このスレッド見せて」「スレッドの会話」「スレッド全部」などで起動。公式Slack MCPの `slack_get_thread_replies` を使用。
allowed-tools: [FetchMcpResource]
---

# Thread Reader

Slack スレッドの返信を取得します。

## ワークフロー

### 1. スレッド情報の確認

以下を確認:
- チャンネルID
- スレッドのタイムスタンプ（親メッセージのts）

### 2. スレッド返信取得

公式Slack MCPの `slack_get_thread_replies` ツールを使用:

```
slack_get_thread_replies(
  channel_id="C01234567",
  thread_ts="1234567890.123456"
)
```

### 3. 結果の整形

スレッド返信を整形して表示:

```
# スレッドの返信

**山田太郎** (10:30) [親メッセージ]
今日のミーティングは15時からです

  **佐藤花子** (10:32) [返信]
  了解しました！

  **田中一郎** (10:35) [返信]
  参加します
```
