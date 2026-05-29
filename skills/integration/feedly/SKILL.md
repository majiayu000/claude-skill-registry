---
name: feedly
description: Aggregate and read RSS feeds from multiple sources with Feedly's news reader platform.
category: news
---
# Feedly Skill

Aggregate and read RSS feeds from multiple sources with Feedly's news reader platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/feedly/install.sh | bash
```

Or manually:
```bash
cp -r skills/feedly ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FEEDLY_ACCESS_TOKEN "your_access_token"
canifi-env set FEEDLY_REFRESH_TOKEN "your_refresh_token"
canifi-env set FEEDLY_USER_ID "your_user_id"
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

1. **Feed Management**: Subscribe to RSS feeds, organize into categories, and manage feed sources
2. **Article Discovery**: Discover trending articles and get AI-powered content recommendations
3. **Read & Annotate**: Read articles with highlighting, notes, and sharing capabilities
4. **Board Organization**: Create boards to save and organize articles by topic or project
5. **Integration Sync**: Sync with productivity tools like Evernote, OneNote, and Pocket

## Usage Examples

### Subscribe to Feed
```
User: "Subscribe to TechCrunch RSS feed in Feedly"
Assistant: Adds TechCrunch to your Feedly subscriptions
```

### Get Latest Articles
```
User: "Show me today's unread articles from my tech feeds"
Assistant: Returns unread articles from tech category with headlines and summaries
```

### Create Board
```
User: "Create a Feedly board for AI research articles"
Assistant: Creates new board and provides instructions for saving articles to it
```

### Search Content
```
User: "Search my Feedly for articles about GPT-4"
Assistant: Searches subscribed feeds and saved content for matching articles
```

## Authentication Flow

1. Create application at feedly.com/v3/auth/dev
2. Implement OAuth 2.0 authorization flow
3. Exchange authorization code for access and refresh tokens
4. Store tokens securely and implement refresh logic

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Token expired | Use refresh token to get new access token |
| 403 Forbidden | Insufficient permissions | Request additional OAuth scopes |
| 404 Not Found | Feed or article not found | Verify feed URL or article ID |
| 429 Rate Limited | Too many requests | Implement exponential backoff |

## Notes

- Free tier limited to 100 sources and 3 feeds
- Pro tier includes AI features like Leo for prioritization
- Enterprise tier available for team collaboration
- API supports real-time streaming for new articles
- OPML import/export available for feed migration
