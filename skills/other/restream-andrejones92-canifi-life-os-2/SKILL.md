---
name: restream
description: Multistream to 30+ platforms with Restream - manage live broadcasts, chat, and analytics across channels
category: video
---

# Restream Skill

## Overview
Enables Claude to use Restream for multistreaming management including configuring destinations, viewing cross-platform analytics, and managing stream settings.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/restream/install.sh | bash
```

Or manually:
```bash
cp -r skills/restream ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set RESTREAM_EMAIL "your-email@example.com"
canifi-env set RESTREAM_PASSWORD "your-password"
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
- Configure streaming destinations
- View cross-platform analytics
- Manage stream schedules
- Access unified chat dashboard
- View recorded streams
- Configure stream branding

## Usage Examples

### Example 1: Check Connected Channels
```
User: "What platforms am I streaming to?"
Claude: I'll check your connected channels.
1. Opening Restream via Playwright MCP
2. Navigating to channels section
3. Listing all connected platforms
4. Showing enabled/disabled status
```

### Example 2: View Stream Analytics
```
User: "How did my last stream perform across platforms?"
Claude: I'll pull up cross-platform analytics.
1. Accessing analytics dashboard
2. Finding last stream data
3. Comparing performance by platform
4. Summarizing total reach and engagement
```

### Example 3: Schedule Stream
```
User: "Check if I have any scheduled streams"
Claude: I'll check your schedule.
1. Opening scheduler section
2. Viewing upcoming streams
3. Listing scheduled events
4. Confirming dates and times
```

## Authentication Flow
1. Navigate to restream.io via Playwright MCP
2. Click "Log in" and enter email
3. Enter password
4. Handle Google/Twitch SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Channel Error**: Check platform connection
- **Analytics Delayed**: Note data refresh timing

## Self-Improvement Instructions
When Restream updates:
1. Document new platform integrations
2. Update analytics capabilities
3. Track studio improvements
4. Log chat aggregation features

## Notes
- Supports 30+ streaming platforms
- Unified chat across all platforms
- Restream Studio for browser streaming
- Analytics aggregated per stream
- Scheduling with social promotion
