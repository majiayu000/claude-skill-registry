---
name: roomba
description: Control iRobot Roomba robot vacuums and Braava mops
category: smarthome
---

# Roomba Skill

## Overview
Enables Claude to interact with iRobot for controlling Roomba robot vacuums and Braava mops, scheduling cleaning jobs, viewing clean maps, and managing device settings.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/roomba/install.sh | bash
```

Or manually:
```bash
cp -r skills/roomba ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set IROBOT_EMAIL "your-email@example.com"
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
- Start, pause, and dock robot
- Schedule cleaning jobs
- View clean map history
- Configure room-specific cleaning
- Check bin status and maintenance

## Usage Examples
### Example 1: Start Cleaning
```
User: "Start the Roomba"
Claude: I'll start a cleaning cycle on your Roomba.
```

### Example 2: Room Cleaning
```
User: "Clean just the kitchen with the Roomba"
Claude: I'll start a targeted clean of the kitchen area.
```

### Example 3: Schedule Setup
```
User: "Schedule Roomba to clean every Monday and Thursday"
Claude: I'll set up a recurring cleaning schedule for those days.
```

## Authentication Flow
1. Navigate to irobot.com via Playwright MCP
2. Click "Log In" button
3. Enter iRobot credentials
4. Handle verification if required
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Verification Required: Complete email verification
- Rate Limited: Implement exponential backoff
- Robot Stuck: Report error and location

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document iRobot app/web changes
2. Update selectors for new layouts
3. Track new robot features
4. Monitor Imprint Smart Maps updates

## Notes
- Smart Maps for room recognition
- Keep Out Zones available
- Auto-empty base compatible
- Alexa and Google integration
