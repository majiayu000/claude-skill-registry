---
name: slack-approval
description: Sends a Slack Block Kit message with [✅ 実行する][❌ キャンセル] buttons and waits for user response. Returns 'approved' or 'denied'. Use when any skill needs user confirmation before executing a destructive or external action (email send, form submit, install, deploy, etc.)
metadata:
  source: slack-bot-builder (sickn33/antigravity-awesome-skills, 253★) + Slack official Node.js SDK
  requires:
    bins: [node]
    npm: ["@slack/web-api", "@slack/socket-mode"]
    env: [SLACK_BOT_TOKEN, SLACK_APP_TOKEN]
---

# slack-approval

全スキル共通の承認ユーティリティ。Block Kit ボタンを Slack に投稿し、ユーザーのクリックを待つ。

## 使い方（全スキルからこの1行）

```javascript
const { requestApproval } = require('../slack-approval/scripts/approve');

const result = await requestApproval({
  channel: 'C091G3PKHL2',   // 送信先チャンネルID
  title:   '📧 メール返信',
  detail:  '宛先: 山田教授\n本文: お世話になっております...'
});

if (result === 'approved') { /* 実行 */ }
if (result === 'denied')   { /* 停止 */ }
```

## 表示される UI

```
┌─────────────────────────────────────┐
│  📧 メール返信                        │
│  宛先: 山田教授                       │
│  本文: お世話になっております...        │
│                                     │
│  [✅ 実行する]    [❌ キャンセル]      │
└─────────────────────────────────────┘

→ [✅ 実行する]  押したら: ✅ 実行しました（ボタン消える）
→ [❌ キャンセル] 押したら: ❌ キャンセルしました（ボタン消える）
```

## 戻り値

| 値 | 意味 |
|----|------|
| `'approved'` | ✅ を押した |
| `'denied'` | ❌ を押した |

timeout なし。ユーザーが押すまで待つ。

## セットアップ（初回のみ）

```bash
cd .claude/skills/slack-approval/scripts
npm install @slack/web-api @slack/socket-mode
```

## 適用スキル

naist-mail / naist-portal / naist-wiki / skill-for-you / mobile-app-factory / 全ての新規スキル
