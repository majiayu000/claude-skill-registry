---
name: health-probe
description: Health probes for both sides of the AGI stack — openclaw_gateway + arifOS MCP
user-invocable: true
---

# Health Probe — AGI Stack Monitor

Triggers: "health", "probe", "is everything ok", "check stack", "gateway health",
          "arifos health", "container health", "is arifos sick", "system status"

---

## On Trigger — Run Full Probe

### 1. arifOS MCP Side
```bash
curl -sf http://arifosmcp_server:8080/health | jq '{status, tools_loaded, version, uptime}'
```
Expected: `status: "healthy"`, `tools_loaded: 13`
Alert if: `tools_loaded < 13` or status != "healthy"

### 2. OpenClaw Gateway Self
```bash
curl -sf http://localhost:18789/ | head -c 200 2>/dev/null && echo "GATEWAY_UP" || echo "GATEWAY_UNREACHABLE"
```

### 3. All Containers Status
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -v "^NAME"
```
Flag any container NOT showing `healthy` or `Up`:
- `unhealthy` → CRITICAL
- `Exited` / `Restarting` → CRITICAL
- `Up X minutes` without `healthy` → WARNING (check if has healthcheck)

### 4. Disk Check
```bash
df -h / | awk 'NR==2 {
  used=$5+0
  if (used > 85) print "DISK_CRITICAL: " used "% used"
  else if (used > 75) print "DISK_WARNING: " used "% used"
  else print "DISK_OK: " used "% used"
}'
```

### 5. RAM Check
```bash
free -h | awk '/^Mem:/ {
  total=$2; avail=$7
  print "RAM: total=" total " available=" avail
}'
docker stats --no-stream --format "{{.Name}}: {{.MemUsage}}" | sort -t'/' -k1 -rh | head -5
```

### 6. Ollama Models Available
```bash
docker exec ollama_engine ollama list 2>/dev/null | tail -n +2
```

### 7. Log the probe result
```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"event\":\"health_probe\",\"agent\":\"arifOS_bot\"}" \
  >> ~/.openclaw/workspace/logs/audit.jsonl
```

---

## Alert Thresholds

| Metric | WARNING | CRITICAL | Action |
|--------|---------|----------|--------|
| Disk usage | >75% | >85% | Notify Arif on Telegram |
| RAM available | <3 GiB | <1.5 GiB | Notify + pause heavy tasks |
| tools_loaded | <13 | <10 | Restart arifosmcp_server |
| Container state | Restarting | Exited/unhealthy | docker compose up -d <name> |
| Model count | 0 | — | docker exec ollama_engine ollama pull qwen2.5:3b |

## Auto-Recovery Actions (within authority)

```bash
# Restart unhealthy arifOS
docker compose -f /mnt/arifos/docker-compose.yml restart arifosmcp_server

# Restart unhealthy openclaw (from host — self-restart)
docker compose -f /mnt/arifos/docker-compose.yml restart openclaw

# Clear disk if >80%
docker builder prune -f
docker image prune -f --filter "dangling=true"
```

*Run this skill on every session start to establish baseline. Alert Arif via Telegram if CRITICAL.*

---

## Telegram Alerts (when CRITICAL)

```bash
# Send alert to Arif via Telegram bot
send_telegram_alert() {
  local MESSAGE="$1"
  if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
      -d "chat_id=${TELEGRAM_CHAT_ID}" \
      -d "text=⚠️ arifOS_bot: ${MESSAGE}" \
      -d "parse_mode=Markdown" > /dev/null
  fi
}

# Example alerts:
# send_telegram_alert "🔴 arifosmcp_server UNHEALTHY — tools_loaded=$(curl ...)"
# send_telegram_alert "💿 Disk ${DISK_PCT}% — run: docker builder prune -f"
# send_telegram_alert "🧠 RAM critical — available: ${RAM_AVAIL}MiB"
```

**Note:** `TELEGRAM_CHAT_ID` is the numeric chat ID of Arif's chat with @arifOS_bot.
To get it: message the bot, then check `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getUpdates`
