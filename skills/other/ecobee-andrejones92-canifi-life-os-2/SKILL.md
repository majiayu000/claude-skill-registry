---
name: ecobee
description: Control ecobee smart thermostats and sensors
category: smarthome
---

# ecobee Skill

## Overview
Enables Claude to interact with ecobee for controlling smart thermostats, managing room sensors, setting schedules, and optimizing home comfort and energy efficiency.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/ecobee/install.sh | bash
```

Or manually:
```bash
cp -r skills/ecobee ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ECOBEE_EMAIL "your-email@example.com"
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
- Control thermostat temperature and mode
- Manage room sensor occupancy
- Set comfort schedules
- View energy reports
- Configure vacation and away modes

## Usage Examples
### Example 1: Temperature Control
```
User: "Set the ecobee to 70 degrees"
Claude: I'll adjust your ecobee thermostat to 70 degrees.
```

### Example 2: Schedule Management
```
User: "Set my ecobee to eco mode on weekdays"
Claude: I'll configure your ecobee schedule for eco mode during weekdays.
```

### Example 3: Sensor Check
```
User: "Which rooms are currently occupied?"
Claude: I'll check your ecobee sensors for current occupancy status.
```

## Authentication Flow
1. Navigate to ecobee.com via Playwright MCP
2. Click "Log In" button
3. Enter ecobee credentials
4. Handle verification if required
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Verification Required: Complete email verification
- Rate Limited: Implement exponential backoff
- Device Offline: Report thermostat connectivity

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document ecobee web portal changes
2. Update selectors for new layouts
3. Track new sensor capabilities
4. Monitor energy feature updates

## Notes
- Room sensors for multi-zone comfort
- Smart Recovery learns heating/cooling times
- HomeKit, Alexa, and Google compatible
- Energy reports track usage patterns
