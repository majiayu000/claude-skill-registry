---
name: slack-unanswered
description: Find unanswered Slack messages where you are mentioned or threads you created. Searches slack-sync/data/ for messages mentioning @Kohei, @Kohei Nakamura, @minicoohei, or @Kohei(TokenPocket) that have no replies.
---

# Slack Unanswered Messages Finder

This skill finds Slack messages that need your attention and helps you reply to them.

## Target Directory

All searches are performed in: `slack-sync/data/`

## Your Identifiers

Search for these names (case-insensitive):
- `@Kohei`
- `@Kohei Nakamura`
- `@minicoohei`
- `@Kohei (TokenPocket)`
- `@Kohei(TokenPocket)`
- Messages posted by: `Kohei Nakamura`, `Kohei (TokenPocket)`, `minicoohei`

---

## Workflow

### Step 1: Find Unanswered Messages

Search for messages containing your identifiers:

```bash
grep -rn -B2 -A10 -E "@Kohei|@minicoohei|Kohei Nakamura|Kohei \(TokenPocket\)" slack-sync/data/
```

### Step 2: Identify Unanswered Messages

A message is **unanswered** if:
1. It contains a mention of your name (or you posted it)
2. It ends with a question (`?`) or contains a request
3. There are NO lines starting with `> ####` immediately after it (before the next `###` or `---`)

Focus on recent messages (last 7 days). Exclude bot messages (Sentry, Vercel, etc.).

### Step 3: Present Findings

For each unanswered message, provide:
- Channel name
- Date/Time
- Sender
- Content summary
- Slack link
- Whether it needs a reply or is a follow-up

### Step 4: Generate Reply Draft

For messages that need replies, generate a draft reply in Japanese. Ask the user to review and edit.

### Step 5: Send Reply (with confirmation)

**IMPORTANT: Always get user confirmation before sending!**

The reply flow is:
1. Show the draft reply to the user
2. Ask: "この内容で送信してよろしいですか？ (修正があれば教えてください)"
3. Wait for user confirmation or edits
4. Only after explicit approval, use the reply script

---

## Replying to Messages

### Reply Script Location

```
slack-sync/scripts/reply_slack.py
```

### Usage

```bash
# Dry run (preview without sending)
python slack-sync/scripts/reply_slack.py \
  --url "https://xxx.slack.com/archives/CHANNEL/pTIMESTAMP" \
  --message "返信内容" \
  --dry-run

# Actually send (only after user confirms!)
python slack-sync/scripts/reply_slack.py \
  --url "https://xxx.slack.com/archives/CHANNEL/pTIMESTAMP" \
  --message "返信内容"
```

### Environment Variable Required

```
SLACK_USER_TOKEN=xoxp-...
```

This token needs the `chat:write` scope. See setup instructions below.

---

## Reply Flow Example

```
Claude: 以下の返信案を作成しました:

---
宛先: @Yuta Sato（佐藤 勇太）
チャンネル: datadev-ai
Slack: [リンク](https://...)

返信案:
「田村さんのSlackアカウントは @xxx です！」
---

この内容で送信してよろしいですか？ (修正があれば教えてください)

User: OKです

Claude: [reply_slack.py を実行して送信]
送信しました！
```

---

## Setup: Adding chat:write Scope

To enable reply functionality:

1. Go to [Slack API Apps](https://api.slack.com/apps)
2. Select your app (e.g., "Message Archiver")
3. Navigate to **OAuth & Permissions**
4. Under **User Token Scopes**, add:
   - `chat:write` - Post messages
5. Click **Reinstall to Workspace**
6. Copy the new `xoxp-...` token
7. Update `SLACK_USER_TOKEN` in your environment/GitHub Secrets

---

## Message Format Reference

Messages in markdown files:
- **Main message**: `### HH:MM - Sender Name [[Slack]](url)`
- **Reply**: Lines starting with `> ####`

---

## TODO File Management

### TODO File Location

```
slack-sync/TODO.md
```

### TODO Format

```markdown
- [ ] **[channel-name]** Sender名 (日付 時刻)
  - 内容: メッセージの要約
  - Slack: URL
  - 返信案: 返信内容のドラフト
```

### Workflow with TODO

1. **検索時**: 未回答メッセージを見つけたらTODO.mdに追加
2. **返信時**: 返信したらチェックボックスを `[x]` に変更
3. **完了時**: 「完了したメッセージ」セクションに移動

### Adding a Task

When you find an unanswered message, add it to `slack-sync/TODO.md`:

```markdown
- [ ] **[datadev-ai]** Yuta Satoさん (1/7 19:10)
  - 内容: 田村さんのSlackアカウント名の確認
  - Slack: https://...
  - 返信案: アカウント名を確認して回答
```

### Completing a Task

After sending a reply:
1. Change `- [ ]` to `- [x]`
2. Move the item to the "完了したメッセージ" section

---

## Quick Commands

### Find mentions in recent files:
```bash
grep -rn -B2 -A10 "@Kohei" slack-sync/data/ | head -200
```

### Find your posts:
```bash
grep -rn "### [0-9:]* - Kohei" slack-sync/data/ | head -100
```

### Find questions to you:
```bash
grep -rn -A5 "@Kohei" slack-sync/data/ | grep -E "\?$|でしょうか|ですか|ますか|ください"
```

### View current TODO:
```bash
cat slack-sync/TODO.md
```
