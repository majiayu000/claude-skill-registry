---
name: twitter-x
description: Enables Claude to manage Twitter/X posts, engagement, and account operations through browser automation
version: 1.0.0
author: Canifi
category: social
---

# Twitter/X Skill

## Overview
Automates Twitter/X operations including tweeting, engaging with content, managing followers, and analyzing metrics through the web interface.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/twitter-x/install.sh | bash
```

Or manually:
```bash
cp -r skills/twitter-x ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TWITTER_USERNAME "your-username"
canifi-env set TWITTER_PASSWORD "your-password"
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
- Create and post tweets
- Retweet and quote tweet
- Like and bookmark tweets
- Follow/unfollow accounts
- Search users and topics
- View notifications and mentions
- Access analytics
- Create and manage lists

## Usage Examples

### Example 1: Post a Tweet
```
User: "Tweet about the new product feature"
Claude: I'll post that tweet.
- Navigate to twitter.com
- Click compose tweet
- Write tweet about new feature
- Add hashtags if appropriate
- Post tweet
- Confirm published
```

### Example 2: Engage with Mentions
```
User: "Reply to my recent mentions"
Claude: I'll respond to mentions.
- Navigate to Notifications > Mentions
- Review recent mentions
- Compose appropriate replies
- Post responses
- Confirm replies sent
```

### Example 3: Create Thread
```
User: "Create a Twitter thread about our company story"
Claude: I'll create that thread.
- Compose first tweet
- Add subsequent tweets as replies
- Connect as thread
- Publish thread
- Confirm all tweets posted
```

### Example 4: Check Analytics
```
User: "Show me my tweet performance this week"
Claude: I'll pull your analytics.
- Navigate to Analytics section
- Gather impressions and engagement
- Compile this week's data
- Present performance summary
```

## Authentication Flow
1. Navigate to twitter.com/login via Playwright MCP
2. Enter username/email from canifi-env
3. Enter password
4. Handle phone/email verification if prompted
5. Complete 2FA if enabled (notify user via iMessage)
6. Verify home feed access
7. Maintain session cookies

## Error Handling
- **Login Failed**: Try email vs username, retry
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Verification Required**: Handle phone/email check
- **Rate Limited**: Wait before retrying (15+ min)
- **Tweet Failed**: Check character limit and content
- **Account Locked**: Notify user of suspension
- **Shadow Ban**: Check account status

## Self-Improvement Instructions
When encountering new Twitter/X features:
1. Document new UI elements
2. Add support for new tweet types
3. Log successful thread patterns
4. Update for X rebranding changes

## Notes
- Twitter rebranded to X
- Character limit is 280 (4000 for Premium)
- Rate limits strictly enforced
- Premium features require subscription
- Analytics need time to populate
- Lists can be public or private
- Scheduled tweets available on web
