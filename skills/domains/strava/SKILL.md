---
name: strava
description: Track athletic activities with Strava - view workouts, analyze performance, and access training history
category: health
---

# Strava Skill

## Overview
Enables Claude to use Strava for athletic activity tracking including viewing workouts, analyzing performance metrics, and accessing training history.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/strava/install.sh | bash
```

Or manually:
```bash
cp -r skills/strava ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set STRAVA_EMAIL "your-email@example.com"
canifi-env set STRAVA_PASSWORD "your-password"
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
- View recent activities
- Access activity details and stats
- Check training log
- View performance metrics
- Access route information
- Check segment times

## Usage Examples

### Example 1: Check Recent Activities
```
User: "What workouts did I do this week?"
Claude: I'll check your recent activities.
1. Opening Strava via Playwright MCP
2. Navigating to training log
3. Filtering to this week
4. Listing all activities
5. Summarizing totals
```

### Example 2: View Activity Details
```
User: "How was my run yesterday?"
Claude: I'll pull up yesterday's run.
1. Finding yesterday's run activity
2. Viewing detailed stats
3. Checking pace and heart rate
4. Summarizing performance
```

### Example 3: Check Training Stats
```
User: "How many miles have I run this month?"
Claude: I'll calculate your monthly mileage.
1. Accessing training log
2. Filtering running activities
3. Summing distance for month
4. Reporting total mileage
```

## Authentication Flow
1. Navigate to strava.com via Playwright MCP
2. Click "Log In" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for data access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Activity Not Found**: Verify activity exists
- **Sync Pending**: Wait for device sync

## Self-Improvement Instructions
When Strava updates:
1. Document new activity metrics
2. Update training analysis features
3. Track segment changes
4. Log new social features

## Notes
- Popular for running and cycling
- GPS-based activity tracking
- Segment leaderboards
- Social features for athletes
- Premium analytics available
