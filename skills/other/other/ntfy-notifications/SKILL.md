---
name: ntfy-notifications
description: Self-hosted push notifications with ntfy — publishing, authentication, priorities, integration patterns for homelab scripts and monitoring
---

# ntfy Notifications

ntfy (pronounce "notify") is a self-hosted push notification service. Send notifications from scripts, cron jobs, and monitoring systems to your phone.

## Publishing messages

### Simple message

```bash
curl -d "Backup completed successfully" https://ntfy.example.com/my-topic
```

### With title, priority, and tags

```bash
curl -H "Title: Backup Status" \
     -H "Priority: high" \
     -H "Tags: white_check_mark,backup" \
     -d "Daily backup completed in 5 minutes" \
     https://ntfy.example.com/backups
```

### With authentication

```bash
# Token auth (preferred)
curl -H "Authorization: Bearer YOUR_TOKEN" \
     -d "Message here" \
     https://ntfy.example.com/topic

# Basic auth
curl -u username:password \
     -d "Message here" \
     https://ntfy.example.com/topic
```

### With click action and URL

```bash
curl -H "Click: https://grafana.example.com/d/alerts" \
     -H "Title: Disk Alert" \
     -H "Priority: urgent" \
     -H "Tags: warning" \
     -d "Disk usage above 90% on /dev/sda1" \
     https://ntfy.example.com/alerts
```

### With actions (buttons)

```bash
curl -H "Actions: view, Open Grafana, https://grafana.example.com; http, Restart Service, https://api.example.com/restart, method=POST" \
     -d "Service is down" \
     https://ntfy.example.com/alerts
```

### File attachment

```bash
curl -T /var/log/backup.log \
     -H "Filename: backup.log" \
     -H "Title: Backup Log" \
     https://ntfy.example.com/backups
```

## Priority levels

| Priority | Keyword | Value | Use for |
|----------|---------|-------|---------|
| Max | `max` / `urgent` | 5 | Service down, security alerts |
| High | `high` | 4 | Backup failures, disk warnings |
| Default | `default` | 3 | Routine notifications |
| Low | `low` | 2 | Info, non-urgent updates |
| Min | `min` | 1 | Debug, verbose logging |

## Tags (emoji shortcodes)

Common tags for homelab notifications:

| Tag | Emoji | Use for |
|-----|-------|---------|
| `white_check_mark` | ✅ | Success |
| `x` | ❌ | Failure |
| `warning` | ⚠️ | Warning |
| `rotating_light` | 🚨 | Critical alert |
| `floppy_disk` | 💾 | Backup |
| `whale` | 🐳 | Docker |
| `movie_camera` | 🎥 | Media/Plex |
| `gear` | ⚙️ | System/config |
| `chart_with_upwards_trend` | 📈 | Monitoring |

Full list: https://docs.ntfy.sh/emojis/

## Docker deployment

### docker-compose.yml

```yaml
services:
  ntfy:
    image: binwiederhier/ntfy
    command: serve
    ports:
      - "8090:80"
    volumes:
      - ntfy_data:/var/lib/ntfy
      - ./server.yml:/etc/ntfy/server.yml
    environment:
      TZ: Europe/Amsterdam
    restart: unless-stopped

volumes:
  ntfy_data:
```

### server.yml

```yaml
base-url: https://ntfy.example.com
auth-default-access: deny-all
behind-proxy: true
```

## User and access management

```bash
# List users
docker exec ntfy ntfy user list

# Add admin user
docker exec ntfy ntfy user add --role admin USERNAME

# Add regular user
docker exec ntfy ntfy user add USERNAME

# Delete user
docker exec ntfy ntfy user del USERNAME

# Change password
docker exec ntfy ntfy user change-pass USERNAME
```

### Access control (ACLs)

```bash
# View all ACLs
docker exec ntfy ntfy access

# Grant read-write to a topic
docker exec ntfy ntfy access USERNAME my-topic rw

# Grant read-only (subscribe only)
docker exec ntfy ntfy access USERNAME alerts ro

# Grant write-only (publish only)
docker exec ntfy ntfy access USERNAME backups wo

# Allow anonymous read access to a topic
docker exec ntfy ntfy access '*' public-topic ro
```

### Token management

```bash
# Generate an access token for a user
docker exec ntfy ntfy token add USERNAME

# List tokens
docker exec ntfy ntfy token list

# Remove a token
docker exec ntfy ntfy token remove USERNAME TOKEN
```

## Homelab integration patterns

### Backup script notification

```bash
#!/bin/bash
NTFY_URL="https://ntfy.example.com/backups"
NTFY_TOKEN="YOUR_TOKEN"

if restic backup /data --json 2>&1 | tail -1 | jq -e '.message_type == "summary"' > /dev/null; then
    curl -s -H "Authorization: Bearer $NTFY_TOKEN" \
         -H "Tags: white_check_mark" \
         -d "Backup completed: $(date +%F)" "$NTFY_URL"
else
    curl -s -H "Authorization: Bearer $NTFY_TOKEN" \
         -H "Priority: high" -H "Tags: x" \
         -d "Backup FAILED: $(date +%F)" "$NTFY_URL"
fi
```

### Watchtower container updates

```yaml
# In docker-compose.yml
services:
  watchtower:
    image: containrrr/watchtower
    environment:
      WATCHTOWER_NOTIFICATION_URL: "generic://ntfy.example.com/watchtower?auth=Bearer+YOUR_TOKEN"
```

### Cron job wrapper

```bash
# Wrap any command with ntfy notification on failure
run_with_ntfy() {
    local topic="$1"; shift
    if ! "$@" 2>&1; then
        curl -s -H "Authorization: Bearer $NTFY_TOKEN" \
             -H "Priority: high" -H "Tags: x" \
             -d "Command failed: $*" "https://ntfy.example.com/$topic"
    fi
}

run_with_ntfy server-alerts certbot renew
```

### Disk space monitor

```bash
USAGE=$(df -h / | awk 'NR==2{print $5}' | tr -d '%')
if [ "$USAGE" -gt 90 ]; then
    curl -s -H "Authorization: Bearer $NTFY_TOKEN" \
         -H "Priority: high" -H "Tags: warning" \
         -H "Title: Disk Alert" \
         -d "Root partition at ${USAGE}%" \
         "https://ntfy.example.com/alerts"
fi
```

### Docker health check alerts

```bash
UNHEALTHY=$(docker ps --filter "health=unhealthy" --format '{{.Names}}' | tr '\n' ', ')
if [ -n "$UNHEALTHY" ]; then
    curl -s -H "Authorization: Bearer $NTFY_TOKEN" \
         -H "Priority: high" -H "Tags: whale,warning" \
         -H "Title: Unhealthy Containers" \
         -d "$UNHEALTHY" \
         "https://ntfy.example.com/docker"
fi
```

## Phone setup

1. Install the ntfy app (Android: Play Store / F-Droid, iOS: App Store)
2. Add your server: Settings → Add server → `https://ntfy.example.com`
3. Subscribe to topics
4. Optional: add credentials if auth is required to subscribe

## Subscribing (receiving)

```bash
# Subscribe in terminal (streaming)
curl -s https://ntfy.example.com/my-topic/sse

# Subscribe with auth
curl -s -H "Authorization: Bearer YOUR_TOKEN" \
     https://ntfy.example.com/my-topic/sse

# JSON stream
curl -s https://ntfy.example.com/my-topic/json

# Poll (last 24h)
curl -s "https://ntfy.example.com/my-topic/json?since=24h"
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| 401 Unauthorized | Check token/password, verify ACLs with `ntfy access` |
| 403 Forbidden | User lacks permission for topic. Add ACL: `ntfy access USER TOPIC rw` |
| No phone notification | Check app subscription, server URL, topic matches exactly |
| Behind reverse proxy | Set `behind-proxy: true` in server.yml, ensure proxy passes headers |
| Messages not persisting | Check volume mount for `/var/lib/ntfy`, ensure cache is enabled in config |
