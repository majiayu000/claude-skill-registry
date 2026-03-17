# /webhook

---
name: webhook
description: Manage webhook sources - list, add, test, and view incoming events
context: fork
triggers:
  - webhook
  - add webhook
  - create webhook
  - webhook setup
  - incoming webhooks
---

Manage the webhook receiver system. Use this skill to add new webhook sources, test existing ones, and view incoming events.

## What You Can Do

1. **List sources** - Show all registered webhook sources
2. **Add source** - Create a new webhook source with secure secret
3. **Test source** - Send a test webhook to verify configuration
4. **View events** - Show recent incoming webhook events
5. **Setup guide** - Get instructions for connecting external services

## Quick Reference

### Webhook Receiver

- **Public URL**: `https://webhooks.organelle.co`
- **Config**: macOS Keychain (`credential get webhook-secrets`)
- **Events directory**: `~/.claude-mind/system/senses/`

### Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/webhook/{source}` | POST | Receive webhook from source |
| `/health` | GET | Health check |
| `/status` | GET | Show registered sources |

## Instructions

### When user wants to list sources

Read and display the webhook configuration:

```bash
~/.claude-mind/system/bin/credential get webhook-secrets | jq .
```

Also check service status:

```bash
curl -s https://webhooks.organelle.co/status | jq .
```

### When user wants to add a new source

1. **Ask for source name** (lowercase, no spaces - e.g., "ifttt", "home-assistant", "backup-server")

2. **Generate a secure secret**:
```bash
openssl rand -hex 32
```

3. **Read current config, add new source, write back**:

The new source should have this structure:
```json
{
  "secret": "<generated-secret>",
  "allowed_ips": null,
  "rate_limit": "30/minute"
}
```

For IP-restricted sources (more secure), ask if they want to limit to specific IPs.

4. **Provide setup instructions** based on the service type (see Setup Guides below)

### When user wants to test a source

Generate and send a signed test webhook:

```bash
SOURCE="<source-name>"
SECRET=$(~/.claude-mind/system/bin/credential get webhook-secrets | jq -r ".sources.\"$SOURCE\".secret")
PAYLOAD='{"event":"test","message":"Test webhook from skill","timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}'
SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s -X POST "https://webhooks.organelle.co/webhook/$SOURCE" \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=$SIGNATURE" \
  -d "$PAYLOAD" | jq .
```

Then check the created event:
```bash
ls -lt ~/.claude-mind/system/senses/webhook-*.json | head -3
```

### When user wants to view recent events

```bash
# List recent webhook events
ls -lt ~/.claude-mind/system/senses/webhook-*.json 2>/dev/null | head -10

# Show content of most recent
cat $(ls -t ~/.claude-mind/system/senses/webhook-*.json 2>/dev/null | head -1) | jq .
```

## Setup Guides

Provide these instructions based on what service the user wants to connect:

### IFTTT Setup

1. Create an IFTTT account at ifttt.com
2. Create a new Applet
3. For the "Then That" action, choose "Webhooks" > "Make a web request"
4. Configure:
   - **URL**: `https://webhooks.organelle.co/webhook/ifttt`
   - **Method**: POST
   - **Content Type**: application/json
   - **Additional Headers**: `X-Webhook-Secret: <their-secret>`
   - **Body**:
   ```json
   {
     "trigger": "<<<{{EventName}}>>>",
     "occurred_at": "<<<{{OccurredAt}}>>>",
     "data": {}
   }
   ```

Note: IFTTT uses simple secret header, not HMAC signing.

### GitHub Setup

1. Go to repository Settings > Webhooks > Add webhook
2. Configure:
   - **Payload URL**: `https://webhooks.organelle.co/webhook/github`
   - **Content type**: application/json
   - **Secret**: `<their-secret>`
   - **Events**: Choose which events to receive
3. GitHub automatically signs payloads with HMAC-SHA256

### Home Assistant Setup

1. In `configuration.yaml`, add a REST command:
```yaml
rest_command:
  notify_claude:
    url: "https://webhooks.organelle.co/webhook/home-assistant"
    method: POST
    headers:
      Content-Type: application/json
      X-Webhook-Secret: "<their-secret>"
    payload: '{"event": "{{ event }}", "data": {{ data | to_json }}}'
```

2. Call from automations:
```yaml
service: rest_command.notify_claude
data:
  event: "motion_detected"
  data:
    location: "front_door"
```

### iOS Shortcut Setup

Create a shortcut with "Get Contents of URL" action:
- **URL**: `https://webhooks.organelle.co/webhook/shortcut`
- **Method**: POST
- **Headers**:
  - Content-Type: application/json
  - X-Webhook-Secret: `<their-secret>`
- **Request Body**: JSON with your data

### Generic / Custom Script

```bash
#!/bin/bash
SECRET="<your-secret>"
PAYLOAD='{"event":"your_event","data":{}}'
SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -X POST https://webhooks.organelle.co/webhook/your-source \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=$SIGNATURE" \
  -d "$PAYLOAD"
```

Or simpler (less secure, but works):
```bash
curl -X POST https://webhooks.organelle.co/webhook/your-source \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Secret: <your-secret>" \
  -d '{"event":"ping"}'
```

## Authentication Methods

The webhook receiver supports two authentication methods:

### 1. HMAC-SHA256 Signature (Recommended)

Used by GitHub and security-conscious services. Send `X-Hub-Signature-256` header:

```
X-Hub-Signature-256: sha256=<hmac-sha256-of-body-using-secret>
```

### 2. Direct Secret Header (Simpler)

For services that can't compute HMAC (like IFTTT). Send `X-Webhook-Secret` header:

```
X-Webhook-Secret: <your-secret>
```

## Event Processing

Incoming webhooks become "sense events" in `~/.claude-mind/system/senses/`. The SenseRouter picks these up and can:

- Trigger immediate attention for high-priority events
- Queue for next wake cycle
- Include in context for relevant conversations

### Priority Mapping

You can customize priority in the webhook receiver's `determine_priority()` function, but defaults are:

| Source | Condition | Priority |
|--------|-----------|----------|
| GitHub | Security-related | `immediate` |
| GitHub | PR/issue actions | `normal` |
| Any | Default | `normal` |

## Troubleshooting

### Webhook not arriving

1. Check service is running:
```bash
curl -s https://webhooks.organelle.co/health | jq .
```

2. Check source is registered:
```bash
curl -s https://webhooks.organelle.co/status | jq .
```

3. Check logs:
```bash
tail -50 ~/.claude-mind/system/logs/webhook-receiver.log
```

### Authentication failing

- For HMAC: Ensure payload bytes match exactly (no extra whitespace)
- For direct secret: Check header name is exactly `X-Webhook-Secret`
- Verify secret matches config file

### IP blocked

If using IP allowlist, check the `allowed_ips` in config. Cloudflare IPs may differ from original source.
