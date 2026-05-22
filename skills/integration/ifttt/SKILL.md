---
name: ifttt
description: Connect apps and automate workflows with simple applets.
category: utilities
---
# IFTTT Skill

Connect apps and automate workflows with simple applets.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/ifttt/install.sh | bash
```

Or manually:
```bash
cp -r skills/ifttt ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set IFTTT_SERVICE_KEY "your_key"
```

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## Capabilities

1. **Create Applets**: Build automation recipes
2. **Trigger Actions**: Fire manual triggers
3. **Manage Applets**: Enable/disable automations
4. **View Activity**: Check applet history
5. **Connect Services**: Link new services

## Usage Examples

### Trigger Applet
```
User: "Trigger my morning routine applet"
Assistant: Fires IFTTT trigger
```

### Check Status
```
User: "Show my active applets"
Assistant: Returns enabled applets
```

### View Activity
```
User: "What ran today?"
Assistant: Returns activity log
```

### Toggle Applet
```
User: "Disable the email notification applet"
Assistant: Turns off applet
```

## Authentication Flow

1. Service key authentication
2. OAuth for service connections
3. Webhook triggers
4. Button widgets

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check service key |
| Trigger Failed | Applet disabled | Enable applet |
| Service Error | Connection issue | Reconnect service |
| Rate Limited | Too many triggers | Slow down |

## Notes

- Simple automation
- 700+ services
- Pro for more applets
- Webhooks API
- Mobile widgets
- Filter code (Pro)
