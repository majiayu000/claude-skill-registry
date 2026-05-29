---
name: peloton
description: Track Peloton workouts - view class history, performance metrics, and achievement progress
category: health
---

# Peloton Skill

## Overview
Enables Claude to use Peloton for workout tracking including viewing class history, performance metrics, personal records, and achievement progress.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/peloton/install.sh | bash
```

Or manually:
```bash
cp -r skills/peloton ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set PELOTON_EMAIL "your-email@example.com"
canifi-env set PELOTON_PASSWORD "your-password"
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
- View workout history
- Check performance metrics
- Access personal records
- View achievement badges
- Check challenge progress
- Browse upcoming classes

## Usage Examples

### Example 1: Check Workout History
```
User: "What Peloton classes did I take this week?"
Claude: I'll review your workout history.
1. Opening Peloton via Playwright MCP
2. Navigating to workout history
3. Filtering to this week
4. Listing completed classes
5. Summarizing workout types
```

### Example 2: View Personal Records
```
User: "What are my personal records?"
Claude: I'll check your PRs.
1. Accessing personal records section
2. Viewing PRs by class type
3. Listing output records
4. Noting recent improvements
```

### Example 3: Check Streak
```
User: "How's my workout streak going?"
Claude: I'll check your streak.
1. Viewing achievement section
2. Checking current streak
3. Viewing workout calendar
4. Reporting streak status
```

## Authentication Flow
1. Navigate to members.onepeloton.com via Playwright MCP
2. Click "Log In" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for data access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Sync Pending**: Wait for equipment sync
- **Data Unavailable**: Check membership status

## Self-Improvement Instructions
When Peloton updates:
1. Document new class categories
2. Update metrics tracking
3. Track achievement changes
4. Log new challenge types

## Notes
- Requires Peloton membership
- Syncs from Peloton equipment
- On-demand and live classes
- Social features available
- Multiple workout types
