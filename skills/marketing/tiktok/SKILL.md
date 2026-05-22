---
name: tiktok
description: Enables Claude to manage TikTok content, engagement, and analytics through browser automation
version: 1.0.0
author: Canifi
category: social
---

# TikTok Skill

## Overview
Automates TikTok operations including uploading videos, engaging with content, managing profile, and accessing creator analytics through the web interface.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/tiktok/install.sh | bash
```

Or manually:
```bash
cp -r skills/tiktok ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TIKTOK_EMAIL "your-email@example.com"
canifi-env set TIKTOK_PASSWORD "your-password"
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
- Upload and publish videos
- Like and comment on videos
- Follow/unfollow accounts
- Search users and sounds
- View analytics and insights
- Manage video settings
- Access trending content
- Handle video descriptions and hashtags

## Usage Examples

### Example 1: Upload Video
```
User: "Post this video to TikTok with trending hashtags"
Claude: I'll upload that TikTok video.
- Navigate to tiktok.com/upload
- Upload video file
- Add description and hashtags
- Configure visibility settings
- Publish video
- Confirm posted successfully
```

### Example 2: Engage with Content
```
User: "Like videos on the For You page"
Claude: I'll engage with trending content.
- Navigate to For You page
- View and like interesting videos
- Track engagement actions
- Confirm likes registered
```

### Example 3: Check Analytics
```
User: "Show me my TikTok video performance this week"
Claude: I'll pull your analytics.
- Navigate to Creator Center
- Access Analytics section
- Gather video performance data
- Present views, likes, shares summary
```

### Example 4: Search Trending Sounds
```
User: "Find trending sounds for my next video"
Claude: I'll find trending sounds.
- Navigate to sounds search
- Browse trending audio
- List popular sounds with usage counts
- Provide sound links
```

## Authentication Flow
1. Navigate to tiktok.com via Playwright MCP
2. Click login and select email/password option
3. Enter credentials from canifi-env
4. Handle CAPTCHA if presented (notify user)
5. Complete 2FA if enabled (notify user via iMessage)
6. Verify feed access
7. Maintain session cookies

## Error Handling
- **Login Failed**: Try alternative login methods
- **Session Expired**: Re-authenticate automatically
- **CAPTCHA Required**: Notify user to complete manually
- **2FA Required**: iMessage for verification code
- **Upload Failed**: Check video format and duration
- **Rate Limited**: Wait before continuing actions
- **Content Removed**: Check community guidelines
- **Account Restricted**: Notify user of status

## Self-Improvement Instructions
When encountering new TikTok features:
1. Document new UI elements
2. Add support for new video features
3. Log successful upload patterns
4. Update for Creator Center changes

## Notes
- TikTok web has limited features vs app
- Video length limits vary by account
- Sounds library differs by region
- Creator Fund requires eligibility
- Algorithm favors consistent posting
- Duet/Stitch features in app only
- Live streaming requires followers threshold
