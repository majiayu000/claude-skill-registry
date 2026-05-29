---
name: mastodon
description: Enables Claude to manage Mastodon toots, boosts, and fediverse engagement
version: 1.0.0
author: Canifi
category: social
---

# Mastodon Skill

## Overview
Automates Mastodon operations including creating toots, boosting content, managing follows, and engaging with the fediverse through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/mastodon/install.sh | bash
```

Or manually:
```bash
cp -r skills/mastodon ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MASTODON_INSTANCE "mastodon.social"
canifi-env set MASTODON_EMAIL "your-email@example.com"
canifi-env set MASTODON_PASSWORD "your-password"
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
- Create and publish toots
- Boost and favorite posts
- Reply to toots
- Follow/unfollow accounts
- Search users and hashtags
- Manage lists
- View local and federated timelines
- Handle content warnings

## Usage Examples

### Example 1: Create a Toot
```
User: "Post to Mastodon about the open source project"
Claude: I'll create that toot.
- Navigate to Mastodon instance
- Click compose
- Write post about project
- Add relevant hashtags
- Publish toot
```

### Example 2: Boost Content
```
User: "Boost that interesting toot about federated networks"
Claude: I'll boost that toot.
- Find the original toot
- Click boost button
- Confirm boosted
- Verify in your profile
```

### Example 3: Search Hashtags
```
User: "Find posts tagged #opensource on Mastodon"
Claude: I'll search that hashtag.
- Navigate to search
- Search #opensource
- Browse results
- Present interesting toots
```

### Example 4: View Federated Timeline
```
User: "Show me what's happening on the federated timeline"
Claude: I'll check the federated feed.
- Navigate to federated timeline
- Browse recent posts
- Summarize trending topics
- Note interesting accounts
```

## Authentication Flow
1. Navigate to instance URL via Playwright MCP
2. Enter email and password from canifi-env
3. Handle 2FA if enabled (notify user via iMessage)
4. Verify home timeline access
5. Maintain session cookies

## Error Handling
- **Login Failed**: Verify instance and credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Instance Down**: Try later or notify user
- **Federation Issue**: Some content may not be available
- **Rate Limited**: Implement backoff
- **User Not Found**: Check instance and username format
- **Content Warning Required**: Add CW if needed

## Self-Improvement Instructions
When encountering new Mastodon features:
1. Document instance-specific UI elements
2. Add support for new post types
3. Log successful federation patterns
4. Update for Mastodon updates

## Notes
- Different instances have different rules
- Username format: @user@instance
- Content warnings are cultural norm
- Local timeline shows same-instance posts
- Federated timeline shows connected instances
- Some instances are invite-only
- Alt text encouraged for images
