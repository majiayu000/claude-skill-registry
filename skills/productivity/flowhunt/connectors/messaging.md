# Optional messaging connectors

These are all opt-in. Setup never asks the user to connect them unless they ask first, or unless the user says "connect everything I have". Each one adds signal to the audit but also adds setup friction. Default: skip.

All options below are OSS or use protocols + tokens that are first-party from the platform (no SaaS brokers).

---

## iMessage (macOS only)

**Repo:** https://github.com/tink1005/imessage-mcp

OSS, uvx install, reads the local `~/Library/Messages/chat.db` file directly. Zero network calls, zero external dependencies. Setup is ~2 min including the macOS permission grant.

### Prereqs

- macOS (iMessage doesn't exist elsewhere)
- `uv` installed (`brew install uv`)
- **Full Disk Access** granted to the terminal / agent application

### Step 1 — grant Full Disk Access

The tricky step. macOS protects `~/Library/Messages/chat.db` behind Full Disk Access. The app that needs access is the process that actually runs the MCP server — usually the terminal (Warp / iTerm / Terminal) or the agent binary (`claude`, `codex`, `gemini`).

1. Open System Settings → Privacy & Security → Full Disk Access.
2. Click the + button. Add the terminal app the user runs the agent from (Warp.app, iTerm.app, Terminal.app).
3. If the user runs the agent as a background process or LaunchAgent, add the agent binary path directly.
4. Restart the terminal / agent after granting.

Tell the user: "macOS pyta o Full Disk Access bo iMessage trzyma bazę w chronionej lokalizacji. To jedyny sposób żeby to przeczytać — Apple nie daje API. Dodaj swój terminal do listy."

### Step 2 — MCP config

For Claude Code (`~/.claude.json`):

```json
{
  "mcpServers": {
    "flowhunt-imessage": {
      "command": "uvx",
      "args": ["imessage-mcp@latest", "stdio"]
    }
  }
}
```

For OpenCode (`~/.config/opencode/opencode.json`):

```jsonc
{
  "mcp": {
    "flowhunt-imessage": {
      "type": "local",
      "command": ["uvx", "imessage-mcp@latest", "stdio"],
      "enabled": true
    }
  }
}
```

For Codex (`~/.codex/config.toml`):

```toml
[mcp_servers.flowhunt-imessage]
command = "uvx"
args = ["imessage-mcp@latest", "stdio"]
```

For Gemini:

```bash
gemini mcp add imessage stdio -- uvx imessage-mcp@latest stdio
```

### Step 3 — restart agent and verify

In a new session, list contacts or recent chats. If results come back, it works. If you get "permission denied" or "chat.db not found", the Full Disk Access step was not completed or applied to the wrong app.

### What FlowHunt reads

- Contact list + group chat list
- Message counts per contact in the last 30 days
- Top 10 contacts by volume
- NO message bodies unless the user explicitly asks for them during the audit

Explain this clearly — iMessage is personal and we want to be non-creepy.

---

## Telegram (Bot API)

**Repo:** https://github.com/guangxiangdebizi/telegram-mcp

Bot API only. The user creates a bot via BotFather, adds it to groups they want FlowHunt to see, and copies the bot token. This is the ToS-clean path — the alternative (User MTProto via Telethon) requires `api_id` + `api_hash` from my.telegram.org and is developer territory.

**Limitation:** bots can only see messages in groups/channels they have been explicitly added to. DMs to the user are invisible. That's fine for work-related group chats, useless for personal DMs.

### Step 1 — create the bot

1. Open Telegram, search for `@BotFather`, start a chat.
2. Send `/newbot`. Name: `flowhunt-audit-bot`. Username: something unique ending in `bot`.
3. BotFather returns a token like `1234567890:AAEhBP...`. Copy it.

### Step 2 — add the bot to groups

The user adds the bot to any Telegram group / channel they want analyzed. For each group, promote the bot to admin at least briefly (required to read message history) then optionally demote.

### Step 3 — MCP config

Same shape as iMessage above, command:

```bash
uvx telegram-mcp@latest
```

with `TELEGRAM_BOT_TOKEN=1234567890:AAE...` in the environment block.

---

## Discord (Bot)

**Repo:** https://github.com/SaseQ/discord-mcp

Same shape as Telegram Bot. User creates a Discord Application at https://discord.com/developers/applications, generates a bot token, invites it to their servers with `READ_MESSAGES` permission. This requires the Discord developer portal and is friction-heavy — most non-technical users should skip.

Document it but default to skip. If the user insists, walk them through the developer portal step-by-step.

---

## Microsoft Teams

**No clean path.** Every Teams MCP requires Azure app registration (developer portal territory). For FlowHunt we consider Teams out of scope unless the user is a developer comfortable with Azure AD. If they insist, point them to https://github.com/floriscornel/teams-mcp and let them handle Azure themselves.

---

## Rule of thumb

Default to skip on all of the above. If the user asks for "everything", do iMessage first (cleanest on Mac), then Telegram Bot (cleanest for groups), then stop. Discord and Teams stay off the happy path.
