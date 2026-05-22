---
name: bluebubbles-setup
description: |
  Set up BlueBubbles for iMessage integration with OpenClaw. Use when:
  (1) configuring iMessage on macOS, (2) troubleshooting BlueBubbles webhooks,
  (3) fixing config validation errors, (4) setting up allowlists and policies.
  Covers Full Disk Access, Cloudflare tunnels, and OpenClaw channel config.
category: development
user-invocable: true
---

# BlueBubbles Setup

Configure BlueBubbles for iMessage integration with OpenClaw on macOS.

## Prerequisites

| Requirement | Details |
|-------------|---------|
| macOS | 15+ (Sequoia) recommended |
| BlueBubbles Server | Download from bluebubbles.app/downloads/server |
| OpenClaw | Running with gateway enabled |
| Full Disk Access | Required for BlueBubbles to read Messages database |

## Step 1: Install BlueBubbles Server

1. Download from [bluebubbles.app/downloads/server](https://bluebubbles.app/downloads/server)
2. Move to Applications folder
3. Right-click and select "Open" to bypass Gatekeeper
4. Grant Full Disk Access when prompted

### Granting Full Disk Access

If BlueBubbles shuts down requesting Full Disk Access:

1. Open System Settings
2. Go to Privacy & Security
3. Click Full Disk Access
4. Click the + button
5. Add BlueBubbles from Applications
6. Toggle it ON
7. Reopen BlueBubbles

## Step 2: Configure BlueBubbles Server

### Required Settings

| Setting | Value |
|---------|-------|
| Auto Start Method | Launch Agent |
| Prevent Sleep | ON |
| Auto Check Updates | ON |

### Server Settings

In BlueBubbles Settings, find:

| Setting | Location |
|---------|----------|
| Server URL | Connection Settings (Cloudflare recommended) |
| Server Password | Connection Settings |
| Local Port | Usually 1234 |

Note the Server URL and Password. You need these for OpenClaw.

## Step 3: Configure OpenClaw

Add BlueBubbles channel to OpenClaw config:

```json
{
  "channels": {
    "bluebubbles": {
      "enabled": true,
      "serverUrl": "https://your-cloudflare-url.trycloudflare.com",
      "password": "your-server-password",
      "webhookPath": "/bluebubbles-webhook",
      "dmPolicy": "allowlist",
      "allowFrom": ["+15551234567"],
      "groupPolicy": "disabled",
      "sendReadReceipts": true
    }
  }
}
```

### Policy Options

| Policy | Value | Requires |
|--------|-------|----------|
| dmPolicy: "allowlist" | Only respond to listed contacts | `allowFrom` array |
| dmPolicy: "pairing" | Require pairing code | Nothing extra |
| dmPolicy: "open" | Respond to everyone | `allowFrom: ["*"]` |
| groupPolicy: "disabled" | Ignore group messages | Nothing extra |
| groupPolicy: "open" | Respond in groups | `groupAllowFrom: ["*"]` |

### Critical Config Rule

**Open policies require wildcards:**
- `dmPolicy: "open"` requires `allowFrom: ["*"]`
- `groupPolicy: "open"` requires `groupAllowFrom: ["*"]`

Forgetting the wildcard crashes the gateway.

Fix with: `openclaw doctor --fix`

## Step 4: Set Up Webhook

In BlueBubbles API & Webhooks section:

1. Click to add a new webhook
2. Set URL to: `http://localhost:18789/bluebubbles-webhook?password=YOUR_PASSWORD`
3. Enable All Events
4. Save the webhook

The webhook connects BlueBubbles to OpenClaw.

## Step 5: Verify Connection

```bash
openclaw status --deep
```

Should show:
```
Channels
┌─────────────┬─────────┬────────┬─────────────┐
│ Channel     │ Enabled │ State  │ Detail      │
├─────────────┼─────────┼────────┼─────────────┤
│ BlueBubbles │ ON      │ OK     │ configured  │
└─────────────┴─────────┴────────┴─────────────┘
```

## Troubleshooting

### Gateway Crashes on Startup

**Symptom:** Gateway exits immediately after config change.

**Cause:** Open policy without wildcard.

**Fix:**
```bash
openclaw doctor --fix
openclaw gateway restart
```

### Messages Not Received

**Symptom:** Send a message but OpenClaw does not respond.

**Check:**
1. Is the sender in `allowFrom`?
2. Is the webhook URL correct?
3. Is BlueBubbles webhook showing in the list?

**Debug:**
```bash
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -i bubble
```

### Private API Not Enabled

**Symptom:** Error about "Private API not enabled."

**Impact:** Read receipts and typing indicators will not work.

**Resolution:** This is optional. Messaging still works without it.

### Pairing Codes

When using `dmPolicy: "pairing"`:
- New contacts receive a pairing code
- Approve with: `openclaw pairing approve bluebubbles CODE`
- List pending: `openclaw pairing list bluebubbles`

## Security Notes

- Keep the server password secret
- Use allowlists in production
- Avoid `dmPolicy: "open"` unless needed
- Consider `groupPolicy: "disabled"` to prevent unintended group responses

## Skill Chaining

| Chain To | When |
|----------|------|
| imessage-tone | After setup, for message formatting |
| doc-maintenance | After completing setup |

| Chains From | Condition |
|-------------|-----------|
| project-init | When iMessage integration requested |
