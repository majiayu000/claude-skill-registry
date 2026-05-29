---
name: substack
description: Subscribe to newsletters and publish content on Substack's newsletter platform.
category: productivity
---
# Substack Skill

Subscribe to newsletters and publish content on Substack's newsletter platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/substack/install.sh | bash
```

Or manually:
```bash
cp -r skills/substack ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SUBSTACK_EMAIL "your_email"
canifi-env set SUBSTACK_PASSWORD "your_password"
canifi-env set SUBSTACK_PUBLICATION_URL "your_publication_url"
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

1. **Newsletter Discovery**: Discover and subscribe to newsletters across various topics
2. **Read & Engage**: Read posts, comment, and engage with newsletter content
3. **Publish Content**: Create and publish newsletter posts with rich media
4. **Subscriber Management**: Manage subscriber list and analyze audience growth
5. **Monetization**: Set up paid subscriptions and manage revenue

## Usage Examples

### Subscribe to Newsletter
```
User: "Subscribe me to the Stratechery newsletter on Substack"
Assistant: Subscribes to the newsletter using your email
```

### Get Latest Posts
```
User: "Show me the latest posts from my Substack subscriptions"
Assistant: Returns recent posts from subscribed newsletters
```

### Publish Post
```
User: "Publish my weekly newsletter about tech trends"
Assistant: Creates and publishes post to your Substack newsletter
```

### Check Stats
```
User: "How many subscribers do I have on Substack?"
Assistant: Returns subscriber count and growth metrics
```

## Authentication Flow

1. Substack uses email/password authentication
2. No official public API available
3. Use browser automation for full functionality
4. Store credentials securely for session management

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Verify email and password |
| Rate Limited | Too many requests | Implement request throttling |
| Post Failed | Content validation error | Check content formatting |
| Session Expired | Login session timeout | Re-authenticate |

## Notes

- No official public API; uses browser automation
- Free tier allows unlimited free subscribers
- Paid subscriptions take 10% platform fee
- Custom domains available for publications
- Email delivery included in platform
- Podcast hosting available for audio content
