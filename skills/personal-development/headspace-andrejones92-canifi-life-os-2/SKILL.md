---
name: headspace
description: Practice mindfulness with Headspace - track meditation sessions, view progress, and access meditation library
category: health
---

# Headspace Skill

## Overview
Enables Claude to use Headspace for mindfulness tracking including viewing meditation history, tracking progress, and accessing the meditation content library.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/headspace/install.sh | bash
```

Or manually:
```bash
cp -r skills/headspace ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HEADSPACE_EMAIL "your-email@example.com"
canifi-env set HEADSPACE_PASSWORD "your-password"
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
- View meditation history
- Check practice streaks
- Access meditation library
- View progress statistics
- Check completed courses
- Browse sleep content

## Usage Examples

### Example 1: Check Meditation Streak
```
User: "How's my meditation streak?"
Claude: I'll check your streak.
1. Opening Headspace via Playwright MCP
2. Accessing profile/stats
3. Viewing current streak
4. Reporting streak days
```

### Example 2: View Practice History
```
User: "What meditations have I done this week?"
Claude: I'll review your practice.
1. Navigating to history section
2. Filtering to this week
3. Listing completed sessions
4. Summarizing practice time
```

### Example 3: Check Progress
```
User: "How much total time have I meditated?"
Claude: I'll calculate your total.
1. Accessing statistics
2. Viewing total meditation time
3. Checking sessions count
4. Reporting progress summary
```

## Authentication Flow
1. Navigate to headspace.com via Playwright MCP
2. Click "Log in" and enter email
3. Enter password
4. Handle SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Content Unavailable**: Check subscription status
- **Sync Error**: Refresh and retry

## Self-Improvement Instructions
When Headspace updates:
1. Document new content categories
2. Update progress tracking features
3. Track new meditation types
4. Log interface changes

## Notes
- Subscription required for full access
- Guided meditation library
- Sleep sounds and stories
- Courses for specific topics
- Mindfulness exercises
