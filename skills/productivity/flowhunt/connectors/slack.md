# Slack connector

Slack is the single most valuable messaging connector for most knowledge workers, because the audit can detect patterns like "user spends 90min/day across 6 Slack channels with 40% of messages being status updates to the same three people". That kind of signal is pure gold for automation recommendations.

Pick the branch matching your agent. All paths avoid creating a Slack app in the Slack developer portal — that's too much friction for a non-technical user.

---

## Claude Code / Claude Desktop — native connector

**Requires** Claude Pro or Claude Max (the connector is gated to paid plans for Slack specifically). Free tier users fall through to the OSS path below.

### Flow

1. Open the Slack connector page:
   ```bash
   open "https://claude.com/connectors/slack"
   ```
2. Click "Connect". OAuth through Slack. The connector requests read access to channels the user is a member of, plus message search.
3. **Workspace admin approval may be required** depending on the Slack org's app install policy. If the approval is blocked, tell the user to ask their workspace admin, or fall through to the OSS korotovsky path with stealth mode (which does NOT require admin approval).
4. Verify:
   ```
   mcp__claude_ai_Slack__slack_list_channels
   ```
   (Or whatever the tool name is once the connector activates. It should appear in the available tools list within a minute of connecting.)

---

## Codex CLI — ChatGPT app

1. Confirm the user is signed into Codex with a ChatGPT account (`codex auth status`).
2. Open `https://chatgpt.com/apps`. Enable Slack.
3. OAuth through Slack in the browser. Same admin-approval caveat as Claude.
4. Inside Codex composer, `$` should list Slack in the app picker.
5. Alternatively: `/plugins` inside Codex and install the curated Slack plugin.

If workspace admin blocks OAuth app install, fall through to OSS path.

---

## Gemini CLI — OSS MCP via `gemini mcp add`

Gemini has no native Slack extension. Use korotovsky/slack-mcp-server:

```bash
gemini mcp add slack stdio -- npx -y @korotovsky/slack-mcp-server
```

Then configure it via environment variables — see the "OSS path" section below. Same config, same token flow.

---

## OpenCode — OSS path (also fallback for everything above)

**Source of truth:** https://github.com/korotovsky/slack-mcp-server

This is the OSS path — open source, ~9k users, supports both OAuth (workspace admin required) and **stealth mode** using browser session tokens (xoxc + xoxd) which does NOT require admin approval. For FlowHunt purposes, stealth mode is the right default because it lets a non-admin user connect their own workspace without bothering anyone.

### Step 1 — extract xoxc and xoxd tokens from the browser

1. Open Slack in the user's browser (https://app.slack.com/client/TXXXXX, whichever workspace).
2. Open DevTools (F12 or Cmd+Opt+I).
3. Go to the **Application** tab → Storage → Cookies → `https://app.slack.com`.
4. Find the cookie named `d` and copy its value. This starts with `xoxd-`. Set aside.
5. In DevTools, switch to the **Console** tab. Run:
   ```javascript
   JSON.parse(localStorage.localConfig_v2).teams[Object.keys(JSON.parse(localStorage.localConfig_v2).teams)[0]].token
   ```
   This prints a string starting with `xoxc-`. Copy it.

These two tokens together authenticate as the user without installing a Slack app. They last as long as the browser session — typically weeks/months — and are revoked when the user logs out of Slack in that browser.

### Step 2 — add MCP config

For OpenCode, edit `~/.config/opencode/opencode.json`:

```jsonc
{
  "mcp": {
    "flowhunt-slack": {
      "type": "local",
      "command": ["npx", "-y", "@korotovsky/slack-mcp-server"],
      "environment": {
        "SLACK_MCP_XOXC_TOKEN": "xoxc-...",
        "SLACK_MCP_XOXD_TOKEN": "xoxd-..."
      },
      "enabled": true
    }
  }
}
```

For Claude Code, the equivalent block in `~/.claude.json` under `mcpServers`.

For Codex, `[mcp_servers.flowhunt-slack]` in `~/.codex/config.toml`.

For Gemini, `gemini mcp add slack stdio -- npx -y @korotovsky/slack-mcp-server` plus env vars set separately.

### Step 3 — restart the agent and verify

In a new agent session, call a Slack tool (e.g. list channels). If it returns the user's channel list, it works.

### Stealth mode caveats

- Tokens rotate when the user logs out of Slack in that browser. When the audit fails with an auth error, tell the user "re-run the token extraction, you logged out of Slack".
- Slack's ToS allows browser token use for personal automation but workspace admins may have policies against it. Warn the user: "Ten tryb używa twojego osobistego sessionu Slacka. Jest to zgodne z ToS Slacka dla personal use, ale sprawdź politykę twojego workspace'u jeśli masz wątpliwości."
- Stealth mode only sees channels the user is a member of. Archived channels, private channels they are not in, and DMs outside their reach are invisible. For FlowHunt that is the correct scope.

---

## What FlowHunt actually reads from Slack

During audit:
- List channels the user is a member of
- Count the user's own messages in the last 30 days, per channel
- **Full content** of the user's top ~100 messages (sorted by recency), plus channel name + timestamp
- Top ~50 recent DM threads with the user's own outbound message content

Content is intentional — not a privacy leak. FlowHunt's whole job is finding automation patterns in how the user communicates, and "you wrote the same two paragraphs 12 times this week" only shows up when you actually read the two paragraphs. Counts alone produce vague audits.

Privacy posture to communicate to the user when asked:
- All data stays local. The MCP tool fetches Slack, the agent (running on the user's machine) reads it, and the audit file is written to `~/.flowhunt/audits/` on their disk. No FlowHunt cloud. No third-party telemetry.
- The agent reading the data is the same agent the user opened FlowHunt in — whatever LLM they already chose to trust with their shell.
- If the user does not want Slack content ingested, they answer `no` to the Slack intake question in setup and the connector is skipped entirely. We default to reading content; users can default out.
