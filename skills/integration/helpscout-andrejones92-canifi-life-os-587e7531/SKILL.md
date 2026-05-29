---
name: helpscout
description: Manage customer support with Help Scout's human-focused help desk.
category: business
---
# Help Scout Skill

Manage customer support with Help Scout's human-focused help desk.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/helpscout/install.sh | bash
```

Or manually:
```bash
cp -r skills/helpscout ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HELPSCOUT_API_KEY "your_api_key"
canifi-env set HELPSCOUT_APP_ID "your_app_id"
canifi-env set HELPSCOUT_APP_SECRET "your_app_secret"
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

1. **Conversation Management**: Manage customer email conversations
2. **Customer Profiles**: View customer history and data in sidebar
3. **Saved Replies**: Use and manage canned responses
4. **Docs Knowledge Base**: Create and manage help documentation
5. **Beacon Widget**: Manage website chat widget and messenger

## Usage Examples

### View Conversation
```
User: "Show me the latest Help Scout conversation from TechCorp"
Assistant: Returns recent customer conversation
```

### Create Conversation
```
User: "Start a new conversation with john@customer.com about their renewal"
Assistant: Creates new email conversation
```

### Update Status
```
User: "Close the conversation with customer #12345"
Assistant: Updates conversation status to closed
```

### Search Docs
```
User: "Find Help Scout docs about password resets"
Assistant: Searches knowledge base for matching articles
```

## Authentication Flow

1. Create OAuth application in Help Scout
2. Use OAuth 2.0 client credentials flow
3. Get access token with app ID and secret
4. API key available for basic auth

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid credentials | Verify API key or OAuth tokens |
| 403 Forbidden | Insufficient permissions | Check user role |
| 404 Not Found | Conversation not found | Verify conversation ID |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- Focus on personal customer experience
- No ticket numbers visible to customers
- Beacon for in-app messaging
- Docs for knowledge base
- Plus plan includes reporting
- Pro plan includes advanced workflows
