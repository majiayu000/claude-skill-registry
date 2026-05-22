---
name: wistia
description: Host marketing videos with Wistia - manage video content, track engagement, and capture leads
category: video
---

# Wistia Skill

## Overview
Enables Claude to use Wistia for marketing-focused video hosting including managing video libraries, accessing detailed analytics, configuring lead capture, and customizing player settings.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/wistia/install.sh | bash
```

Or manually:
```bash
cp -r skills/wistia ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WISTIA_EMAIL "your-email@example.com"
canifi-env set WISTIA_PASSWORD "your-password"
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
- Manage video libraries and projects
- Access detailed engagement analytics
- Configure lead capture forms
- Customize video player appearance
- View viewer heatmaps and data
- Manage channels and playlists

## Usage Examples

### Example 1: Review Engagement Data
```
User: "Show me viewer engagement for my demo video"
Claude: I'll pull up the engagement data.
1. Opening Wistia via Playwright MCP
2. Navigating to your media library
3. Finding the demo video
4. Accessing engagement heatmap
5. Summarizing watch patterns and drop-offs
```

### Example 2: Add Lead Capture
```
User: "Add an email capture form to my webinar recording"
Claude: I'll configure lead capture.
1. Opening the webinar video settings
2. Navigating to Turnstile settings
3. Enabling email gate at start
4. Configuring form fields
5. Saving lead capture settings
```

### Example 3: Check Lead Stats
```
User: "How many leads did my product video capture this month?"
Claude: I'll check your lead stats.
1. Opening video analytics
2. Filtering to this month
3. Viewing lead capture data
4. Summarizing conversion metrics
```

## Authentication Flow
1. Navigate to wistia.com via Playwright MCP
2. Click "Login" and enter email
3. Enter password
4. Handle SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Analytics Unavailable**: Check video processing status
- **Integration Error**: Verify API connections

## Self-Improvement Instructions
When Wistia updates:
1. Document new analytics features
2. Update lead capture options
3. Track player customization changes
4. Log new integration capabilities

## Notes
- Wistia focuses on marketing use cases
- Detailed viewer-level analytics available
- Integration with marketing automation tools
- Custom player branding on paid plans
- Channels feature for video series
