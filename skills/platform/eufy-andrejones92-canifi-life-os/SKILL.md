---
name: eufy
description: Control eufy smart home devices including cameras, doorbells, and robot vacuums
category: smarthome
---

# eufy Skill

## Overview
Enables Claude to interact with eufy for managing security cameras, video doorbells, robot vacuums, and other smart home devices with local storage focus.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/eufy/install.sh | bash
```

Or manually:
```bash
cp -r skills/eufy ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set EUFY_EMAIL "your-email@example.com"
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
- View camera feeds and recordings
- Control robot vacuum cleaning
- Manage video doorbell settings
- Check device status and battery
- Configure motion detection

## Usage Examples
### Example 1: Camera Check
```
User: "What did the eufy camera record today?"
Claude: I'll check your eufy HomeBase for today's recorded events.
```

### Example 2: Vacuum Control
```
User: "Start the eufy robot vacuum"
Claude: I'll start a cleaning cycle on your eufy RoboVac.
```

### Example 3: Doorbell Events
```
User: "Show me recent doorbell rings"
Claude: I'll check your eufy doorbell for recent visitor events.
```

## Authentication Flow
1. Navigate to mysecurity.eufylife.com via Playwright MCP
2. Click "Log In" button
3. Enter eufy credentials
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- 2FA Required: Wait for code via email
- Rate Limited: Implement exponential backoff
- Device Offline: Check HomeBase connectivity

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document eufy Security app changes
2. Update selectors for new layouts
3. Track new product features
4. Monitor HomeBase updates

## Notes
- Local storage with HomeBase
- No monthly fees for basic features
- Alexa and Google compatible
- Anker company product line
