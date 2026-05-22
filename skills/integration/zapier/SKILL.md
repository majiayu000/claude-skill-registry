---
name: zapier
description: Advanced workflow automation connecting 5000+ apps.
category: utilities
---
# Zapier Skill

Advanced workflow automation connecting 5000+ apps.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/zapier/install.sh | bash
```

Or manually:
```bash
cp -r skills/zapier ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ZAPIER_API_KEY "your_api_key"
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

1. **Create Zaps**: Build multi-step automations
2. **Run Zaps**: Trigger workflows manually
3. **Manage Zaps**: Enable, disable, edit
4. **View History**: Check task runs
5. **Transfer Data**: Move data between apps

## Usage Examples

### Trigger Zap
```
User: "Run my lead capture zap"
Assistant: Triggers the workflow
```

### Check Tasks
```
User: "Show recent Zapier tasks"
Assistant: Returns task history
```

### Toggle Zap
```
User: "Turn off the Slack notification zap"
Assistant: Disables zap
```

### View Status
```
User: "Are my zaps running?"
Assistant: Returns zap statuses
```

## Authentication Flow

1. API key authentication
2. OAuth for app connections
3. Webhook triggers
4. NLA for AI integration

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Zap Error | Step failed | Check error log |
| App Disconnected | OAuth expired | Reconnect |
| Task Limit | Plan exceeded | Upgrade |

## Notes

- 5000+ integrations
- Multi-step workflows
- Paths and filters
- Zapier Tables
- Natural Language Actions
- Enterprise features
