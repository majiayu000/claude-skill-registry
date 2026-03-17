---
name: calm
description: Practice wellness with Calm - track meditation and sleep sessions, view progress, and access content library
category: health
---

# Calm Skill

## Overview
Enables Claude to use Calm for wellness tracking including viewing meditation history, sleep story usage, and accessing the mindfulness content library.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/calm/install.sh | bash
```

Or manually:
```bash
cp -r skills/calm ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CALM_EMAIL "your-email@example.com"
canifi-env set CALM_PASSWORD "your-password"
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
- View session history
- Check practice streaks
- Access meditation library
- Browse sleep stories
- View progress stats
- Check completed programs

## Usage Examples

### Example 1: Check Session History
```
User: "What Calm sessions have I done this month?"
Claude: I'll review your session history.
1. Opening Calm via Playwright MCP
2. Accessing session history
3. Filtering to this month
4. Listing completed sessions
5. Summarizing usage patterns
```

### Example 2: View Streak
```
User: "How's my Daily Calm streak?"
Claude: I'll check your streak.
1. Accessing profile section
2. Viewing streak status
3. Checking consecutive days
4. Reporting current streak
```

### Example 3: Check Sleep Content
```
User: "What sleep stories are available?"
Claude: I'll browse sleep stories.
1. Navigating to sleep section
2. Viewing story library
3. Listing available stories
4. Noting narrators and themes
```

## Authentication Flow
1. Navigate to calm.com via Playwright MCP
2. Click "Log In" and enter email
3. Enter password
4. Handle Apple/Google SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Content Locked**: Check subscription status
- **Playback Error**: Retry or check connection

## Self-Improvement Instructions
When Calm updates:
1. Document new content additions
2. Update navigation patterns
3. Track new feature releases
4. Log library organization changes

## Notes
- Subscription for full library
- Daily Calm feature
- Sleep Stories popular feature
- Music and nature sounds
- Programs for specific goals
