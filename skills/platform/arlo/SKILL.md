---
name: arlo
description: Manage Arlo security cameras, video doorbell, and smart home security
category: smarthome
---

# Arlo Skill

## Overview
Enables Claude to interact with Arlo for viewing camera feeds, managing recordings, configuring motion detection, and controlling Arlo security system.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/arlo/install.sh | bash
```

Or manually:
```bash
cp -r skills/arlo ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ARLO_EMAIL "your-email@example.com"
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
- View live and recorded camera feeds
- Manage motion detection zones
- Configure armed/disarmed modes
- Download and share video clips
- Check battery and device status

## Usage Examples
### Example 1: View Camera
```
User: "Show me the backyard Arlo camera"
Claude: I'll pull up the live feed from your backyard Arlo camera.
```

### Example 2: Mode Control
```
User: "Arm all Arlo cameras"
Claude: I'll set your Arlo system to Armed mode.
```

### Example 3: Event History
```
User: "What motion was detected last night?"
Claude: I'll check your Arlo library for last night's motion events.
```

## Authentication Flow
1. Navigate to my.arlo.com via Playwright MCP
2. Click "Log In" button
3. Enter Arlo credentials
4. Handle 2FA via email or text
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- 2FA Required: Wait for code via email/SMS
- Rate Limited: Implement exponential backoff
- Camera Offline: Report device connectivity

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Arlo web portal changes
2. Update selectors for new layouts
3. Track new camera features
4. Monitor subscription changes

## Notes
- Arlo Secure subscription for cloud storage
- Battery-powered wireless cameras
- Works with Alexa, Google, and HomeKit
- Geofencing for automatic arming
