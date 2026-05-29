---
name: wyze
description: Control Wyze smart home devices including cameras, bulbs, and plugs
category: smarthome
---

# Wyze Skill

## Overview
Enables Claude to interact with Wyze for controlling cameras, smart bulbs, plugs, locks, and other affordable smart home devices.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/wyze/install.sh | bash
```

Or manually:
```bash
cp -r skills/wyze ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WYZE_EMAIL "your-email@example.com"
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
- View Wyze camera feeds and events
- Control smart bulbs and plugs
- Manage Wyze Lock access
- Check device status and battery
- Configure detection settings

## Usage Examples
### Example 1: Camera Check
```
User: "Show me the Wyze camera events from today"
Claude: I'll check your Wyze camera for today's motion and sound events.
```

### Example 2: Device Control
```
User: "Turn off all Wyze plugs"
Claude: I'll turn off all connected Wyze smart plugs.
```

### Example 3: Bulb Control
```
User: "Set the Wyze bulbs to 50% brightness"
Claude: I'll adjust all Wyze bulbs to 50% brightness.
```

## Authentication Flow
1. Navigate to wyze.com via Playwright MCP
2. Click "Log In" button
3. Enter Wyze credentials
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- 2FA Required: Wait for code via email
- Rate Limited: Implement exponential backoff
- Device Offline: Report device connectivity

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Wyze web interface changes
2. Update selectors for new layouts
3. Track new product launches
4. Monitor Cam Plus feature updates

## Notes
- Affordable smart home ecosystem
- Cam Plus for extended features
- Alexa and Google Assistant compatible
- Wide range of device types
