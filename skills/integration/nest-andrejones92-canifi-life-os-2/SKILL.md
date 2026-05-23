---
name: nest
description: Control Nest thermostats, cameras, and doorbells through Google Home
category: smarthome
---

# Nest Skill

## Overview
Enables Claude to interact with Nest devices including thermostats, cameras, doorbells, and smoke detectors through the Google Home ecosystem.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/nest/install.sh | bash
```

Or manually:
```bash
cp -r skills/nest ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOOGLE_EMAIL "your-email@example.com"
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
- Control Nest thermostat settings
- View Nest camera feeds and history
- Manage Nest doorbell settings
- Check Nest Protect status
- Set temperature schedules

## Usage Examples
### Example 1: Thermostat Control
```
User: "Set the Nest to 72 degrees"
Claude: I'll adjust your Nest thermostat to 72 degrees.
```

### Example 2: Camera Check
```
User: "Show me the front door camera"
Claude: I'll pull up the live feed from your Nest Hello doorbell camera.
```

### Example 3: Schedule Setup
```
User: "Set my Nest to eco mode when I'm away"
Claude: I'll configure your Nest to switch to eco mode based on presence.
```

## Authentication Flow
1. Navigate to home.nest.com via Playwright MCP
2. Sign in with Google account
3. Handle 2FA if enabled
4. Access Nest devices through Google Home
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with Google
- 2FA Required: Wait for code via authenticator
- Rate Limited: Implement exponential backoff
- Device Offline: Report device connectivity

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Nest/Google Home integration changes
2. Update selectors for new layouts
3. Track new Nest product features
4. Monitor migration to Google Home

## Notes
- Migrated to Google Home ecosystem
- Nest Aware subscription for video history
- Works with Google Assistant
- Energy savings reports available
