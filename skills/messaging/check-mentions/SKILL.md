---
name: check-mentions
description: Slack で自分へのメンションを確認する。「メンション確認」「Slackメンション」「自分へのメンション」「@mention を見せて」などで起動。Pythonスクリプト `slack_message.py mentions` を使用。
allowed-tools: [Bash, Read]
---

# Mention Checker

Slack で自分へのメンションを確認します。

## トリガー

- 「メンション確認」
- 「Slackメンション」
- 「自分へのメンション」
- 「@mention を見せて」
- 「メンション一覧」

## 動作

1. Pythonスクリプト `slack_message.py mentions` を実行
2. 自分へのメンションを検索
3. メンション一覧を整理して表示

## 実装

```bash
# Pythonスクリプトでメンション取得
python plugins/shiiman-slack/skills/mention-checker/scripts/slack_message.py mentions \
  --max 20 \
  --format table
```

## 出力例

```
# あなたへのメンション（直近20件）

メンション数: 5

channel         user        text                                    permalink
general         山田太郎    @you レビューお願いします               https://...
project-alpha   佐藤花子    @you 資料確認しました                   https://...
dev-team        田中一郎    @you バグ修正完了です                   https://...
random          木村さん    @you 明日の予定どうですか？             https://...
marketing       鈴木次郎    @you 新しい企画について相談したいです   https://...
```

## 機能

- **検索**: Slack Search APIで `<@USER_ID>` を検索
- **最大件数**: デフォルト20件、`--max` で変更可能
- **パーマリンク**: 各メンションへの直接リンクを表示
- **チャンネル名**: メンションがあったチャンネルを表示

## 必要な環境変数

```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
```

## 必要なスコープ

- `search:read` - メッセージ検索
- `users:read` - 自分のユーザーID取得

## 注意事項

- Slack Search APIは検索履歴の制限があります（フリープランでは直近10,000メッセージ）
- パーマリンクをクリックすると、該当メッセージに直接ジャンプできます
