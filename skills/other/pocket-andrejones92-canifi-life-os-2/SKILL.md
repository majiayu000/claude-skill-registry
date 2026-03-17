---
name: pocket
description: Save and organize articles, videos, and web content for later reading with Pocket's read-it-later service.
category: productivity
---
# Pocket Skill

Save and organize articles, videos, and web content for later reading with Pocket's read-it-later service.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/pocket/install.sh | bash
```

Or manually:
```bash
cp -r skills/pocket ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set POCKET_CONSUMER_KEY "your_consumer_key"
canifi-env set POCKET_ACCESS_TOKEN "your_access_token"
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

1. **Save Content**: Save articles, videos, and web pages to your Pocket library for offline reading
2. **Organize Library**: Tag, archive, and favorite saved items for easy organization and retrieval
3. **Search & Retrieve**: Search your saved content by title, URL, or tags to find specific items
4. **Reading Progress**: Track reading progress and get personalized recommendations based on interests
5. **Export & Share**: Share saved articles to social media or export reading lists

## Usage Examples

### Save an Article
```
User: "Save this article to Pocket: https://example.com/interesting-article"
Assistant: Saves article to Pocket library with automatic metadata extraction
```

### Organize with Tags
```
User: "Tag my recent Pocket saves with 'AI research'"
Assistant: Applies 'AI research' tag to recently saved items
```

### Search Library
```
User: "Find all my saved articles about machine learning"
Assistant: Searches Pocket library and returns matching items with titles and URLs
```

### Get Reading List
```
User: "Show me my unread Pocket articles from this week"
Assistant: Retrieves unread items saved in the last 7 days
```

## Authentication Flow

1. Register application at getpocket.com/developer
2. Obtain consumer key from developer portal
3. Complete OAuth flow to get access token
4. Store credentials securely in environment variables

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid or expired token | Re-authenticate with OAuth flow |
| 403 Forbidden | Rate limit exceeded | Wait and retry with exponential backoff |
| 404 Not Found | Item doesn't exist | Verify item ID before operations |
| 503 Service Unavailable | Pocket API down | Retry after service restoration |

## Notes

- Free tier includes unlimited saves with basic features
- Premium tier adds permanent library backup and full-text search
- API rate limits apply: 10,000 requests per day
- Offline reading requires mobile app download
- Content is cached for 30 days in free tier
