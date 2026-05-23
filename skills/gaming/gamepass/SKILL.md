---
name: gamepass
description: Manage Xbox Game Pass subscription, browse catalog, and track perks
category: gaming
---

# Xbox Game Pass Skill

## Overview
Enables Claude to interact with Xbox Game Pass for browsing game catalog, tracking leaving/arriving games, accessing perks, and managing subscription across PC and console.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/gamepass/install.sh | bash
```

Or manually:
```bash
cp -r skills/gamepass ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set XBOX_EMAIL "your-email@example.com"
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
- Browse Game Pass catalog
- Track games leaving soon
- Access Game Pass perks and rewards
- View recently added games
- Manage subscription tier

## Usage Examples
### Example 1: New Additions
```
User: "What new games are on Game Pass?"
Claude: I'll check the recently added games to Game Pass.
```

### Example 2: Leaving Soon
```
User: "What games are leaving Game Pass soon?"
Claude: I'll check which games are scheduled to leave Game Pass.
```

### Example 3: Claim Perks
```
User: "What Game Pass perks are available?"
Claude: I'll check for available Game Pass Ultimate perks to claim.
```

## Authentication Flow
1. Navigate to xbox.com/gamepass via Playwright MCP
2. Click "Sign In" button
3. Enter Microsoft credentials
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with Microsoft
- 2FA Required: Wait for code via authenticator
- Rate Limited: Implement exponential backoff
- Tier Restrictions: Note PC vs Console vs Ultimate

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Game Pass interface changes
2. Update selectors for new layouts
3. Track catalog rotation patterns
4. Monitor perk availability

## Notes
- PC, Console, and Ultimate tiers
- EA Play included with Ultimate
- Cloud gaming with Ultimate
- Day one Xbox Game Studios releases
