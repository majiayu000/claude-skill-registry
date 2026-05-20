---
name: naist-onboarding
description: Creates a personal #ai-<name> Slack channel for a new NAIST user and sends a welcome message. Use when user says "make my channel", "create my channel", "チャンネル作って", or similar onboarding requests in #ai channel.
metadata:
  source: slack-api v1.0.7 (ClawHub) API call patterns
  requires:
    bins: [node]
    npm: ["@slack/web-api"]
    env: [SLACK_BOT_TOKEN]
---

# naist-onboarding

新規ユーザーが `#ai` チャンネルで "make my channel" と言ったときに、`#ai-<name>` チャンネルを作成して招待する。

## トリガー

ユーザーが以下のいずれかを言ったとき:
- "make my channel"
- "create my channel"
- "チャンネル作って"
- "マイチャンネル作って"

## 実行手順

### 1. ユーザーIDを特定

Slack イベントから送信者の `user_id` を取得する。

### 2. onboard.js を実行

```bash
cd /Users/anicca/.openclaw/skills/naist-onboarding/scripts
node onboard.js <user_id>
```

### 3. 出力を確認して報告

スクリプトが成功すれば自動で Slack に通知される。
エラーが出た場合は `#ai` にエラー内容を投稿する。

## onboard.js が行うこと

| ステップ | 内容 |
|---------|------|
| 1 | Slack API でユーザーの display_name を取得 |
| 2 | `#ai-<lowercase-name>` チャンネルを作成（既存なら再利用） |
| 3 | ユーザーをチャンネルに招待 |
| 4 | `#ai` に `✅ #ai-<name> 作ったよ！` と通知 |
| 5 | 新チャンネルでウェルカムメッセージを送信 |

## セットアップ（初回のみ）

```bash
cd /Users/anicca/.openclaw/skills/naist-onboarding/scripts
npm install @slack/web-api
```

## Slack Bot に必要なスコープ

| スコープ | 用途 | 現状 |
|---------|------|------|
| `channels:manage` | チャンネル作成・招待 | ❌ 未付与 |
| `channels:write.invites` | ユーザーをチャンネルに招待 | ❌ 未付与 |
| `channels:join` | チャンネル参加 | ✅ 付与済み |
| `chat:write` | メッセージ送信 | ✅ 付与済み |
| `users:read` | ユーザー名取得 | ✅ 付与済み |

## ⚠️ 初回セットアップ（ユーザー作業）

1. https://api.slack.com/apps/A092UBRAJ1X を開く
2. **OAuth & Permissions** → **Bot Token Scopes** に追加:
   - `channels:manage`
   - `channels:write.invites`
3. **Install to Workspace** ボタンで再インストール
4. 新しい `SLACK_BOT_TOKEN` を `/Users/anicca/.openclaw/.env` に更新

→ セットアップ完了後、`node scripts/onboard.js <userId>` で動作確認。
