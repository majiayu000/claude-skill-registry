---
name: openclaw-medicine
description: Diagnose and fix OpenClaw gateway issues — broken configs, missing tokens, dead channels, auth failures, merge bugs, and multi-instance management. Use when openclaw is unresponsive, channels aren't starting, config is corrupted, or when managing remote openclaw instances (e.g. via SSH). Also covers migrating between config strategies (Nix-managed vs local).
---

# OpenClaw Medicine 💊

Diagnose, fix, and maintain OpenClaw gateway instances — local or remote.

## Diagnosis Checklist

Run these in order to identify the problem:

1. **Gateway status**: `openclaw status` (or via SSH for remote instances)
2. **Config exists?**: `cat ~/.openclaw/openclaw.json` — if missing, gateway has no config
3. **Config valid?**: Use `gateway(action=config.get)` — check `valid`, `issues`, `warnings`
4. **Logs**: `journalctl --user -u openclaw-gateway -n 30 --no-pager` — look for:
   - `[telegram]` / `[whatsapp]` — channel startup
   - `No API key found` — missing auth profile
   - `Config invalid` / `Unrecognized key` — schema violations
   - `ECONNREFUSED` — gateway not listening on expected port
5. **Auth profile**: `cat ~/.openclaw/agents/main/agent/auth-profiles.json` — needs valid Anthropic token

## Common Issues & Fixes

### No config file
Gateway was set up by an external system (Nix activation, wizard) that no longer runs.
- Write a fresh `openclaw.json` based on a known-good config
- Must include: `channels`, `gateway` (port, auth), `agents`, `plugins`
- Use `gateway(action=config.patch)` for local instance, or write directly via SSH for remote

### Invalid config keys
OpenClaw validates strictly. Common mistakes:
- `channels.telegram.token` → **wrong**, use `tokenFile` pointing to a file containing the token
- Unknown keys cause startup failure — check `openclaw doctor --fix` output

### Missing auth profile
The file `~/.openclaw/agents/main/agent/auth-profiles.json` must exist with a valid provider token:
```json
{
  "version": 1,
  "profiles": {
    "anthropic:default": {
      "type": "token",
      "provider": "anthropic",
      "token": "<api-key>"
    }
  },
  "lastGood": { "anthropic": "anthropic:default" }
}
```

### Telegram token storage
Never put the token inline in config. Write to a file and reference it:
```bash
echo -n '<bot-token>' > ~/.openclaw/telegram-bot-token
chmod 600 ~/.openclaw/telegram-bot-token
```
Config: `"tokenFile": "/home/<user>/.openclaw/telegram-bot-token"`

### Channels not starting after restart
- Check if `plugins.entries.telegram.enabled` and `channels.telegram.enabled` are both `true`
- After config changes, the gateway needs SIGUSR1 or service restart
- Delete stale offset files if switching bots: `rm ~/.openclaw/telegram/update-offset-default.json`

### Port mismatch
Gateway port in config vs systemd service env can diverge. Check:
- Config: `gateway.port`
- Service: `systemctl --user show openclaw-gateway | grep Environment` → `OPENCLAW_GATEWAY_PORT`
- These must match

## Remote Instance Management (via SSH)

For managing another machine's OpenClaw (e.g. Romário on work PC):

```bash
# Check status
ssh user@host "export PATH=\$HOME/.npm-global/bin:\$PATH; openclaw status"

# Read logs
ssh user@host "journalctl --user -u openclaw-gateway -n 30 --no-pager"

# Write config
ssh user@host "cat > ~/.openclaw/openclaw.json << 'EOF'
{ ... }
EOF"

# Restart
ssh user@host "systemctl --user restart openclaw-gateway"
```

Always verify channels start after restart by checking logs for `[telegram] starting provider`.

## Config Architecture

OpenClaw config is a single JSON file at `~/.openclaw/openclaw.json`. It's the source of truth.

**Do not** manage it via Nix activation scripts or merge strategies — this causes override bugs where runtime config clobbers Nix-defined values (or vice versa). Let openclaw manage its own config locally.

**Nix should only manage**: workspace symlinks (identity/rules/skills) and package installation. See the `rebuild` skill for Nix operations.

## Multi-Bot Setup (Cleber + Romário)

When two bots share Telegram groups:
- Each bot's `groupAllowFrom` must include the other bot's ID
- `groups.*` and specific group entries need both IDs in `allowFrom`
- Armada Lucas group (`-1003768595045`): `requireMention: false` for bot-to-bot chat
- Cleber ID: `8372008099`, Romário ID: `8523821709`

## Retrieving Lost Bot Tokens

If a Telegram bot token is lost:
1. Open BotFather in Telegram (browser or app)
2. Send `/mybots` → select the bot → "API Token"
3. Or search BotFather chat history for "Use this token to access the HTTP API"
4. Token format: `<bot-id>:<alphanumeric-string>`
5. Store securely in `~/.openclaw/telegram-bot-token`, never in config JSON
