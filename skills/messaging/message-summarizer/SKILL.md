---
name: message-summarizer
description: Slack メッセージを要約用データとして取得する。「Slack要約」「メッセージ要約」「要約して」「まとめて」「会話の要約」「チャンネル要約」「最近の話を要約」などで起動。Pythonスクリプト `slack_message.py summarize` を使用。
allowed-tools: [Bash]
---

# Message Summarizer

Slack メッセージを要約用データとして取得します。

## ワークフロー

### 1. 要約対象の確認

以下を確認:
- チャンネルID
- 取得する件数（デフォルト: 50件）
- 期間指定（オプション）

### 2. メッセージ取得

Pythonスクリプトで要約用データを取得:

```bash
python plugins/shiiman-slack/skills/message-summarizer/scripts/slack_message.py summarize \
  --channel C01234567 \
  --limit 50 \
  --format json
```

### 3. 要約生成

取得したデータを分析し、以下の観点で要約:
- 主なトピック
- 重要な決定事項
- アクションアイテム
- 未解決の質問

### 4. 要約の提示

構造化された形式で要約を提示:

```
# #general の要約（過去50件）

## 主なトピック
- プロジェクトアルファのリリース計画
- 新機能の設計レビュー

## 決定事項
- リリース日: 2024年1月15日
- 担当: 山田チーム

## アクションアイテム
- [ ] 設計書の更新 (@佐藤)
- [ ] テスト計画の作成 (@田中)

## 未解決の質問
- パフォーマンス要件の詳細
```

## 注意事項

このスキルは要約用データの取得のみを行います。実際の要約はClaudeが生成します。
