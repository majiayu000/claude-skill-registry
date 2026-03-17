---
name: ea-play
description: Manage EA Play subscription, game library, and access EA titles
category: gaming
---

# EA Play Skill

## Overview
Enables Claude to interact with EA Play for accessing subscription game library, tracking game trials, managing EA account, and discovering new EA titles.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/ea-play/install.sh | bash
```

Or manually:
```bash
cp -r skills/ea-play ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set EA_EMAIL "your-email@example.com"
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
- Browse EA Play game catalog
- Access 10-hour game trials
- View play history and stats
- Claim member rewards and discounts
- Track upcoming EA releases

## Usage Examples
### Example 1: Game Catalog
```
User: "What games are included in EA Play?"
Claude: I'll browse the EA Play vault and list available games.
```

### Example 2: Game Trial
```
User: "Can I try the new FIFA before buying?"
Claude: I'll check if a 10-hour trial is available for the latest FIFA.
```

### Example 3: Member Benefits
```
User: "What discounts do I get with EA Play?"
Claude: I'll check your EA Play member benefits and current discounts.
```

## Authentication Flow
1. Navigate to ea.com via Playwright MCP
2. Click "Sign In" button
3. Enter EA account credentials
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with EA
- 2FA Required: Wait for code via email
- Rate Limited: Implement exponential backoff
- Subscription Status: Verify EA Play membership

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document EA app and web changes
2. Update selectors for new layouts
3. Track vault additions
4. Monitor trial availability

## Notes
- EA Play included with Game Pass Ultimate
- Pro tier offers more games
- 10-hour trials for new releases
- 10% discount on EA purchases
