---
name: anchor
description: Create and distribute podcasts with Anchor (Spotify for Podcasters) - manage episodes, analytics, and distribution
category: video
---

# Anchor Skill

## Overview
Enables Claude to use Anchor (now Spotify for Podcasters) for podcast creation and distribution including managing episodes, viewing analytics, and configuring distribution settings.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/anchor/install.sh | bash
```

Or manually:
```bash
cp -r skills/anchor ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ANCHOR_EMAIL "your-email@example.com"
canifi-env set ANCHOR_PASSWORD "your-password"
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
- Manage podcast episodes
- View download and listener analytics
- Configure distribution settings
- Access listener demographics
- Manage monetization settings
- View ratings and reviews

## Usage Examples

### Example 1: Check Episode Performance
```
User: "How is my latest podcast episode performing?"
Claude: I'll check your episode analytics.
1. Opening Anchor via Playwright MCP
2. Navigating to your podcast
3. Finding the latest episode
4. Accessing analytics dashboard
5. Summarizing downloads and engagement
```

### Example 2: View Listener Stats
```
User: "Where are my podcast listeners located?"
Claude: I'll pull up listener demographics.
1. Accessing analytics section
2. Viewing geographic data
3. Compiling location breakdown
4. Summarizing top listening regions
```

### Example 3: Check Distribution
```
User: "Is my podcast available on all platforms?"
Claude: I'll check distribution status.
1. Opening distribution settings
2. Reviewing connected platforms
3. Verifying availability status
4. Listing any issues or gaps
```

## Authentication Flow
1. Navigate to podcasters.spotify.com via Playwright MCP
2. Click "Log in" with Spotify account
3. Enter email and password
4. Handle 2FA if required (via iMessage)
5. Maintain session for dashboard access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Analytics Delayed**: Note data lag timing
- **Distribution Error**: Check platform status

## Self-Improvement Instructions
When Anchor/Spotify for Podcasters updates:
1. Document new analytics features
2. Update distribution platform options
3. Track monetization changes
4. Log new podcast tools

## Notes
- Now branded as Spotify for Podcasters
- Free hosting and distribution
- Analytics have 48-hour delay
- Monetization varies by region
- Q&A and polls available
