---
name: freshdesk
description: Manage customer support with Freshdesk's intuitive help desk solution.
category: business
---
# Freshdesk Skill

Manage customer support with Freshdesk's intuitive help desk solution.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/freshdesk/install.sh | bash
```

Or manually:
```bash
cp -r skills/freshdesk ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FRESHDESK_DOMAIN "your_domain.freshdesk.com"
canifi-env set FRESHDESK_API_KEY "your_api_key"
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

1. **Ticket Management**: Create, manage, and resolve support tickets
2. **Multi-channel Support**: Handle tickets from email, phone, chat, and social
3. **Team Collaboration**: Assign tickets, add notes, and collaborate with team
4. **Automation Rules**: Set up auto-assignment and escalation rules
5. **Customer Portal**: Manage self-service knowledge base and forums

## Usage Examples

### Create Ticket
```
User: "Create a Freshdesk ticket for shipping delay from sarah@customer.com"
Assistant: Creates ticket with requester and subject
```

### Assign Agent
```
User: "Assign ticket #5001 to the technical support team"
Assistant: Updates ticket assignment
```

### Add Note
```
User: "Add an internal note to ticket #5001 about the escalation"
Assistant: Adds private note to ticket
```

### View Queue
```
User: "Show me my open Freshdesk tickets"
Assistant: Returns agent's open ticket queue
```

## Authentication Flow

1. Get API key from Freshdesk profile settings
2. Use Basic Auth with API key as username
3. Password should be empty or 'X'
4. Domain-specific endpoints

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify API key |
| 403 Forbidden | Agent doesn't have access | Check permissions |
| 404 Not Found | Ticket not found | Verify ticket ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Part of Freshworks suite
- Free tier for up to 10 agents
- Freddy AI for automation
- Field service management add-on
- Omnichannel support in higher tiers
- SLA management included
