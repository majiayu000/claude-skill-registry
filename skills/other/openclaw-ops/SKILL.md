---
name: openclaw-ops
description: "Complete OpenClaw operations skill: configure models/providers/channels/tools/agents/cron, manage sessions and sub-agents, control paired nodes (camera/location/notifications), and troubleshoot gateway issues. Use when: (1) changing AI models or providers, (2) managing cron jobs, (3) configuring channels (Telegram/Discord/WhatsApp), (4) troubleshooting gateway/model/channel failures, (5) managing sessions or sub-agents, (6) controlling paired mobile devices, (7) any 'fix yourself', 'change settings', 'what's running', 'restart', 'add model', 'phone camera', 'send notification' request."
---

# OpenClaw Ops — Self-Management Skill

One skill for all OpenClaw operations: config, troubleshoot, sessions, nodes.

## Config Location

- **Config**: `~/.openclaw/openclaw.json` (JSON5)
- **Cron**: `~/.openclaw/cron/jobs.json`
- **Logs**: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- **Sessions**: `~/.openclaw/agents/main/sessions/`

Always `cat ~/.openclaw/openclaw.json` before editing.

---

## 1. Models & Providers

### Switch primary model
Edit `agents.list[0].model.primary`:
```json5
"model": { "primary": "kimi/kimi-k2.5", "fallbacks": ["anthropic/claude-opus-4-6"] }
```

### Add provider
```json5
"models": { "providers": { "new-provider": {
  "baseUrl": "https://api.example.com/v1",
  "api": "openai-completions",  // or anthropic-messages | google-generative-ai
  "apiKey": "${NEW_API_KEY}",
  "models": [{ "id": "model-id", "name": "Name", "contextWindow": 128000, "maxTokens": 8192 }]
}}}
```

### Quick model switch (no restart)
Use `/model kimi/kimi-k2.5` in chat, or `session_status(model="anthropic/claude-opus-4-6")`.

---

## 2. Cron Jobs

```bash
openclaw cron list                                    # List all
openclaw cron add --name "Brief" --cron "0 7 * * *" \
  --tz "Asia/Kuala_Lumpur" --session isolated \
  --message "Morning summary" --announce \
  --channel telegram --to "267378578"                 # Recurring
openclaw cron add --name "Remind" --at "20m" \
  --session main --system-event "Check deploy" \
  --wake now --delete-after-run                       # One-shot
openclaw cron edit <jobId> --message "New prompt"     # Edit
openclaw cron run <jobId>                             # Force run
openclaw cron runs --id <jobId> --limit 5             # History
```

| Session type | Use for |
|---|---|
| `main` | Uses heartbeat context, shared session |
| `isolated` | Fresh per run, delivery supported |

---

## 3. Channels

### Telegram (current)
```json5
"telegram": { "enabled": true, "botToken": "...", "dmPolicy": "pairing", "streaming": "partial" }
```

### Add Discord / WhatsApp / Signal
```json5
"discord": { "enabled": true, "token": "${DISCORD_BOT_TOKEN}" }
"whatsapp": { "dmPolicy": "pairing", "allowFrom": ["+60..."] }
"signal": { "enabled": true, "allowFrom": ["+60..."] }
```

---

## 4. Tools & Agents

| Profile | Scope |
|---|---|
| `minimal` | session_status only |
| `coding` | fs + runtime + sessions + memory |
| `messaging` | messaging + sessions |
| `full` | Everything (current) |

### Multi-agent
```json5
"agents": { "list": [
  { "id": "main", "default": true, ... },
  { "id": "public", "tools": { "profile": "messaging", "deny": ["exec","browser"] } }
]},
"bindings": [{ "agentId": "public", "match": { "channel": "telegram", "peer": { "kind": "group" } } }]
```

---

## 5. Sessions & Sub-Agents

```
sessions_list()                                    # All sessions
sessions_list(activeMinutes=60)                    # Recent
sessions_history(sessionKey="<key>", limit=20)     # History
sessions_send(sessionKey="<key>", message="...")   # Send to session
```

### Spawn sub-agent
```
sessions_spawn(task="Research X", mode="run")                    # One-shot
sessions_spawn(task="Fix bug", runtime="acp", thread=true)      # Coding agent
```

### Manage
```
subagents(action="list")                          # List running
subagents(action="steer", target="<id>", message="Focus on API")
subagents(action="kill", target="<id>")           # Kill stuck
```

---

## 6. Paired Nodes (Android/iOS/macOS)

```
nodes(action="status")                                          # List devices
nodes(action="camera_snap", node="<name>", facing="back")      # Photo
nodes(action="camera_clip", node="<name>", durationMs=10000)   # Video
nodes(action="location_get", node="<name>")                    # GPS
nodes(action="notifications_list", node="<name>")              # Notifications
nodes(action="screen_record", node="<name>", durationMs=10000) # Screen
nodes(action="notify", node="<name>", title="Alert", body="Done")
nodes(action="device_status", node="<name>")                   # Battery/storage
```

Device must be **foregrounded** for camera/screen. Max video: 60s.

---

## 7. Troubleshooting

### Quick check
```bash
openclaw status                    # Gateway health
openclaw doctor --fix              # Auto-fix common issues
tail -50 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -i "error\|warn"
```

### By symptom
| Symptom | Fix |
|---|---|
| No messages | Check `channels.telegram.enabled`, bot token |
| No reply | Model provider down → check API key, fallback chain |
| Slow | Check model latency in logs |
| Cron silent | `openclaw cron list`, check timezone |
| Memory empty | Check `memory/*.md` exists |
| "Model not found" | Check `models.providers` in config |
| Sub-agent stuck | `subagents(action="kill", target="<id>")` |

### Nuclear (confirm first)
```bash
openclaw gateway restart           # Drops active sessions
```

---

## 8. Config Edit Workflow (F1 Safe)

1. Read current: `cat ~/.openclaw/openclaw.json`
2. Show diff (use `edit` tool with exact old/new)
3. **888_HOLD** for: API key rotation, channel removal, agent deletion
4. Apply edit
5. `openclaw gateway restart` if needed
6. Verify: `openclaw status`
