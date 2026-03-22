---
name: add-dingtalk
description: Add DingTalk as a channel. Uses Stream Mode (WebSocket, no public URL needed). Auto-registers groups on first message.
---

# Add DingTalk Channel

This skill adds DingTalk support to MatClaw using the skills engine for deterministic code changes, then walks through interactive setup.

## Phase 1: Pre-flight

### Check if already applied

Read `.matclaw/state.yaml`. If `dingtalk` is in `applied_skills`, skip to Phase 3 (Setup). The code changes are already in place.

### Ask the user

**Do they already have a DingTalk app configured?** If yes, collect the Client ID and Client Secret now. If no, we'll create one in Phase 3.

## Phase 2: Apply Code Changes

Run the skills engine to apply this skill's code package.

### Initialize skills system (if needed)

If `.matclaw/` directory doesn't exist yet:

```bash
npx tsx scripts/apply-skill.ts --init
```

### Apply the skill

```bash
npx tsx scripts/apply-skill.ts .claude/skills/add-dingtalk
```

This deterministically:
- Adds `src/channels/dingtalk.ts` (DingTalkChannel class with self-registration via `registerChannel`)
- Adds `src/dingtalk-auth.ts` (interactive credential setup)
- Appends `import './dingtalk.js'` to the channel barrel file `src/channels/index.ts`
- Installs the `dingtalk-stream` npm dependency
- Adds `auth:dingtalk` npm script
- Records the application in `.matclaw/state.yaml`

If the apply reports merge conflicts, read the intent file:
- `modify/src/channels/index.ts.intent.md` — what changed and invariants

### Validate code changes

```bash
npx tsc --noEmit
npm run build
```

Build must be clean before proceeding.

## Phase 3: Setup

### Create DingTalk App

If the user doesn't have a DingTalk app, share [DINGTALK_SETUP.md](DINGTALK_SETUP.md) or guide them through these steps:

1. Go to [DingTalk Open Platform](https://open-dev.dingtalk.com/fe/app#/corp/app)
2. Click "Create App" (create an H5 Micro App or Enterprise Internal App)
3. In the app settings, go to "Robot" section and enable "Robot configuration"
4. Set message receiving mode to **Stream Mode** (Stream 模式)
5. Copy the **Client ID** (AppKey) and **Client Secret** (AppSecret) from the credentials page
6. In "Permissions", grant: `qyapi_robot_sendmsg`, `qyapi_chat_manage`
7. Publish/release the app
8. Add the bot to a DingTalk group chat

Wait for the user to provide both credentials.

### Configure credentials

Run the auth script:

```bash
npm run auth:dingtalk
```

This interactively:
- Collects Client ID and Client Secret
- Tests the connection by fetching an access token
- Saves credentials to `store/dingtalk-credentials.json` (mode 0600)

Alternatively, users can create the file manually:

```json
{
  "clientId": "your-app-key",
  "clientSecret": "your-app-secret"
}
```

### Build and restart

```bash
npm run build
```

For systemd:
```bash
systemctl --user restart matclaw
```

For launchd:
```bash
launchctl kickstart -k gui/$(id -u)/com.matclaw
```

## Phase 4: Registration

DingTalk groups are **auto-registered** on first message. When a user sends a message mentioning the bot in a DingTalk group (or sends a 1-on-1 message), the channel automatically:

1. Creates a group folder (`groups/dingtalk_<id>/`)
2. Writes a default `CLAUDE.md`
3. Registers the group in the database
4. Delivers the message to the agent

No manual registration step is needed. The JID format is: `dingtalk:<conversationId>`.

## Phase 5: Verify

### Test the connection

Tell the user:

> 1. Make sure the bot has been added to your DingTalk group
> 2. Send a message in the group: `@BotName hello`
> 3. For 1-on-1 chats: send any message directly to the bot
> 4. The bot should respond within a few seconds

### Check logs if needed

```bash
tail -f logs/matclaw.log | grep -i dingtalk
```

## Troubleshooting

### Bot not responding

1. Check credentials: `cat store/dingtalk-credentials.json`
2. Verify Stream Mode is enabled in the DingTalk app settings
3. Verify the app has been published/released
4. Verify the bot has been added to the group
5. Check service is running: `systemctl --user status matclaw`

### "invalid client" error

1. Verify Client ID (AppKey) and Client Secret (AppSecret) are correct
2. Make sure the app type is "Enterprise Internal App" (not ISV)
3. Re-run `npm run auth:dingtalk` to re-enter credentials

### Bot receives messages but doesn't reply

1. Check logs for send errors: `grep "DingTalk.*send\|DingTalk.*failed" logs/matclaw.log`
2. The bot uses session webhook for replies (fast) and falls back to OpenAPI
3. Verify the app has `qyapi_robot_sendmsg` permission

### Message not reaching the bot

1. In group chats, messages must @mention the bot to trigger it
2. Check that `conversationType` is being read correctly in logs
3. Verify the group's `requiresTrigger` setting matches expectations

## After Setup

The DingTalk channel supports:
- **Group chats** — Bot responds when @mentioned (trigger required)
- **1-on-1 chats** — Bot responds to all messages (no trigger needed)
- **Auto-registration** — New groups/chats register automatically
- **Markdown formatting** — Responses use DingTalk markdown
- **Multi-channel** — Runs alongside Feishu, Slack, or other channels

## Known Limitations

- **No image upload** — DingTalk's robot API has limited image support. Plots and images generated by the agent are sent as text links rather than inline images.
- **No typing indicator** — DingTalk's Bot API does not expose a typing indicator. Users won't see "bot is typing..." while the agent works.
- **Session webhook expiry** — The session webhook (for fast replies) expires after ~1 hour. Replies after expiry use the OpenAPI fallback, which requires additional permissions.
- **Markdown subset** — DingTalk supports a limited subset of markdown. Some formatting may not render as expected.
- **No file sending** — File attachments referenced in agent output are shown as text links.
