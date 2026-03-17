---
name: hootsuite
description: Manage enterprise social media with Hootsuite's comprehensive management platform.
category: marketing
---
# Hootsuite Skill

Manage enterprise social media with Hootsuite's comprehensive management platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/hootsuite/install.sh | bash
```

Or manually:
```bash
cp -r skills/hootsuite ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HOOTSUITE_ACCESS_TOKEN "your_access_token"
canifi-env set HOOTSUITE_CLIENT_ID "your_client_id"
canifi-env set HOOTSUITE_CLIENT_SECRET "your_client_secret"
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

1. **Social Publishing**: Schedule and publish to multiple networks
2. **Stream Monitoring**: Monitor mentions, keywords, and feeds
3. **Team Management**: Manage team access and approval workflows
4. **Analytics**: Track social performance across all networks
5. **Social Listening**: Monitor brand sentiment and trends

## Usage Examples

### Schedule Message
```
User: "Schedule a post to all my Hootsuite social profiles"
Assistant: Creates scheduled message across networks
```

### Check Streams
```
User: "Show me recent mentions from my Hootsuite streams"
Assistant: Returns recent stream activity
```

### Get Analytics
```
User: "Show me this week's social media performance"
Assistant: Returns engagement metrics by platform
```

### Approve Message
```
User: "Approve the pending team posts in Hootsuite"
Assistant: Approves posts awaiting review
```

## Authentication Flow

1. Register app in Hootsuite developer portal
2. Implement OAuth 2.0 flow
3. Request appropriate scopes
4. Store and refresh tokens

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Token expired | Refresh access token |
| 403 Forbidden | Insufficient permissions | Check scopes |
| 404 Not Found | Resource not found | Verify ID |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- Enterprise-grade social management
- Supports all major social networks
- Team collaboration features
- Advanced analytics and reporting
- Social listening add-on
- Integrations marketplace
