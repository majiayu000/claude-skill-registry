---
name: ring
description: Manage Ring doorbells, cameras, and alarm system
category: smarthome
---

# Ring Skill

## Overview
Enables Claude to interact with Ring for viewing doorbell and camera feeds, managing Ring Alarm, checking event history, and configuring device settings.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/ring/install.sh | bash
```

Or manually:
```bash
cp -r skills/ring ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set RING_EMAIL "your-email@example.com"
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
- View live camera and doorbell feeds
- Check motion and ring event history
- Manage Ring Alarm system
- Configure motion zones and sensitivity
- View and download video clips

## Usage Examples
### Example 1: Check Doorbell
```
User: "Who rang the doorbell while I was out?"
Claude: I'll check the Ring doorbell history for recent visitors.
```

### Example 2: Alarm Control
```
User: "Arm the Ring alarm in home mode"
Claude: I'll set your Ring Alarm to Home mode.
```

### Example 3: Camera Status
```
User: "Are all my Ring cameras online?"
Claude: I'll check the status of all your Ring cameras.
```

## Authentication Flow
1. Navigate to ring.com via Playwright MCP
2. Click "Log In" button
3. Enter Ring credentials
4. Handle 2FA via email or text
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- 2FA Required: Wait for code via email/SMS
- Rate Limited: Implement exponential backoff
- Device Offline: Report device connectivity

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Ring app/web changes
2. Update selectors for new layouts
3. Track new device features
4. Monitor subscription changes

## Notes
- Ring Protect plan for video history
- Neighbors app for community alerts
- Alexa integration available
- Professional monitoring optional
