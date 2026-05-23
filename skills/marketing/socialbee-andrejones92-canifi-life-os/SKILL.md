---
name: socialbee
description: Manage social media scheduling with SocialBee's category-based content system.
category: marketing
---
# SocialBee Skill

Manage social media scheduling with SocialBee's category-based content system.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/socialbee/install.sh | bash
```

Or manually:
```bash
cp -r skills/socialbee ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SOCIALBEE_API_KEY "your_api_key"
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

1. **Category Scheduling**: Organize content into rotating categories
2. **Content Recycling**: Automatically recycle evergreen content
3. **Multi-platform Posting**: Post to all major social networks
4. **RSS Import**: Import content from RSS feeds
5. **Analytics**: Track posting performance and engagement

## Usage Examples

### Add Post
```
User: "Add a new post to my 'Tips' category in SocialBee"
Assistant: Creates post in specified category
```

### Schedule Category
```
User: "Set up a schedule for my blog posts category"
Assistant: Configures posting schedule for category
```

### Import RSS
```
User: "Import my latest blog posts to SocialBee"
Assistant: Imports posts from RSS feed
```

### View Queue
```
User: "Show me what's scheduled in SocialBee for this week"
Assistant: Returns scheduled posts by day
```

## Authentication Flow

1. Get API key from SocialBee account
2. Use API key for authentication
3. Key provides full account access
4. Workspaces for team management

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify API key |
| 404 Not Found | Category not found | Check category ID |
| 422 Validation Error | Invalid data | Fix request format |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Category-based content organization
- Evergreen content recycling
- Concierge service available
- Canva integration built-in
- AI content suggestions
- Affordable pricing tiers
