---
name: you-com
description: AI search engine with multiple modes and personalization.
category: ai
---
# You.com Skill

AI search engine with multiple modes and personalization.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/you-com/install.sh | bash
```

Or manually:
```bash
cp -r skills/you-com ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set YOU_API_KEY "your_api_key"
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

1. **Smart Search**: AI-enhanced results
2. **You Chat**: Conversational AI
3. **You Write**: AI writing assistant
4. **You Code**: Programming help
5. **You Imagine**: Image generation

## Usage Examples

### Smart Search
```
User: "Search You.com for best practices"
Assistant: Returns AI-curated results
```

### You Chat
```
User: "Chat with You.com about this topic"
Assistant: Provides conversational response
```

### You Write
```
User: "Help me write an email"
Assistant: Generates writing with You Write
```

### You Code
```
User: "Explain this code snippet"
Assistant: Uses You Code for analysis
```

## Authentication Flow

1. API key authentication
2. Subscription for premium
3. OAuth integration
4. Personalization settings

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Rate Limited | Too many queries | Slow down |
| Mode Error | Unavailable mode | Try different mode |
| Search Failed | Query issue | Rephrase |

## Notes

- Multiple AI modes
- Privacy focused
- Personalization
- No ads option
- API available
- Mobile apps
