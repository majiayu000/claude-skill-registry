---
name: whoop
description: Track recovery and strain with WHOOP - view HRV, recovery scores, and performance optimization data
category: health
---

# WHOOP Skill

## Overview
Enables Claude to use WHOOP for performance tracking including viewing recovery scores, strain data, sleep performance, and HRV trends.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/whoop/install.sh | bash
```

Or manually:
```bash
cp -r skills/whoop ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WHOOP_EMAIL "your-email@example.com"
canifi-env set WHOOP_PASSWORD "your-password"
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
- View daily recovery score
- Check strain accumulation
- Access sleep performance data
- View HRV trends
- Check weekly performance
- Access journal correlations

## Usage Examples

### Example 1: Check Recovery
```
User: "What's my WHOOP recovery score today?"
Claude: I'll check your recovery.
1. Opening WHOOP via Playwright MCP
2. Accessing today's data
3. Viewing recovery score
4. Showing HRV and resting HR
5. Interpreting recovery level
```

### Example 2: View Strain
```
User: "How much strain have I accumulated today?"
Claude: I'll check your strain.
1. Accessing strain data
2. Viewing current day strain
3. Comparing to target
4. Summarizing activity contribution
```

### Example 3: Analyze Sleep
```
User: "How did I sleep according to WHOOP?"
Claude: I'll analyze your sleep.
1. Accessing sleep section
2. Viewing last night's sleep
3. Checking sleep stages
4. Comparing to sleep need
```

## Authentication Flow
1. Navigate to app.whoop.com via Playwright MCP
2. Click "Log In" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for data access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Sync Pending**: Wait for strap sync
- **Data Processing**: Note real-time delay

## Self-Improvement Instructions
When WHOOP updates:
1. Document new metrics
2. Update recovery algorithm changes
3. Track journal feature updates
4. Log new performance insights

## Notes
- Requires WHOOP membership
- Continuous HRV monitoring
- Recovery-focused approach
- Strain optimization
- Journal for behavior tracking
