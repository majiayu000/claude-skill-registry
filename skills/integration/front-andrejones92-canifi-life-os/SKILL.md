---
name: front
description: Manage team inbox and customer communication with Front's collaborative platform.
category: business
---
# Front Skill

Manage team inbox and customer communication with Front's collaborative platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/front/install.sh | bash
```

Or manually:
```bash
cp -r skills/front ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FRONT_API_TOKEN "your_api_token"
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

1. **Shared Inbox**: Manage shared email inboxes with team collaboration
2. **Conversation Threading**: Thread conversations across email, SMS, and chat
3. **Assignment & Tags**: Assign conversations and organize with tags
4. **Templates & Snippets**: Use shared response templates
5. **Rules & Automation**: Automate routing and responses with rules

## Usage Examples

### Get Conversations
```
User: "Show me my assigned Front conversations"
Assistant: Returns conversations assigned to you
```

### Reply to Message
```
User: "Reply to the latest customer email in Front"
Assistant: Sends reply in conversation thread
```

### Assign Conversation
```
User: "Assign the billing inquiry to Sarah"
Assistant: Updates conversation assignee
```

### Add Tag
```
User: "Tag this conversation as 'VIP Customer'"
Assistant: Adds tag to conversation
```

## Authentication Flow

1. Create API token in Front settings
2. Use Bearer token authentication
3. OAuth available for integrations
4. Token provides account access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid token | Verify API token |
| 403 Forbidden | Insufficient permissions | Check token scope |
| 404 Not Found | Conversation not found | Verify conversation ID |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- Team-focused inbox management
- Multi-channel support (email, SMS, social)
- Analytics and SLA tracking
- Extensive integrations library
- Custom rules for automation
- API rate limit: 200 requests per minute
