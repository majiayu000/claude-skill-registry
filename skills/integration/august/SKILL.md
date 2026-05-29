---
name: august
description: Control August smart locks and manage home access
category: smarthome
---

# August Skill

## Overview
Enables Claude to interact with August smart locks for controlling door access, managing guest access, viewing access history, and configuring lock settings.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/august/install.sh | bash
```

Or manually:
```bash
cp -r skills/august ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set AUGUST_EMAIL "your-email@example.com"
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
- Lock and unlock doors remotely
- Manage guest access and schedules
- View access activity history
- Configure auto-lock settings
- Check battery status

## Usage Examples
### Example 1: Lock Control
```
User: "Lock the front door"
Claude: I'll lock the front door via your August smart lock.
```

### Example 2: Guest Access
```
User: "Give the dog walker access on weekdays at 2pm"
Claude: I'll create a scheduled guest access for weekday afternoons.
```

### Example 3: Activity Check
```
User: "Who unlocked the door today?"
Claude: I'll check the access history for today's lock activity.
```

## Authentication Flow
1. Navigate to august.com via Playwright MCP
2. Click "Sign In" button
3. Enter August credentials
4. Handle 2FA via phone verification
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- 2FA Required: Wait for phone verification
- Rate Limited: Implement exponential backoff
- Lock Offline: Check WiFi bridge status

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document August app/web changes
2. Update selectors for new layouts
3. Track new lock features
4. Monitor integration updates

## Notes
- August Connect WiFi bridge enables remote access
- Works with Alexa, Google, and HomeKit
- Keypad accessory for code entry
- Auto-lock and DoorSense features
