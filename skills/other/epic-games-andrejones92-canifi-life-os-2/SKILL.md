---
name: epic-games
description: Manage Epic Games Store library, claim free games, and track wishlist
category: gaming
---

# Epic Games Skill

## Overview
Enables Claude to interact with Epic Games Store for managing game library, claiming weekly free games, tracking wishlist, and discovering new titles.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/epic-games/install.sh | bash
```

Or manually:
```bash
cp -r skills/epic-games ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set EPIC_EMAIL "your-email@example.com"
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
- Browse and manage game library
- Claim weekly free games
- Track wishlist and sales
- View purchase history
- Access Epic Games achievements

## Usage Examples
### Example 1: Claim Free Games
```
User: "What free games are on Epic this week?"
Claude: I'll check the Epic Games Store for this week's free games and claim them for you.
```

### Example 2: Library Check
```
User: "What Epic games do I own?"
Claude: I'll browse your Epic Games library and list your collection.
```

### Example 3: Wishlist Sales
```
User: "Are any Epic wishlist games on sale?"
Claude: I'll check your wishlist for current discounts.
```

## Authentication Flow
1. Navigate to store.epicgames.com via Playwright MCP
2. Click "Sign In" button
3. Enter email and password
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- 2FA Required: Wait for code via email or authenticator
- Rate Limited: Implement exponential backoff
- Game Claimed: Skip already-owned free games

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Epic Store interface changes
2. Update selectors for new layouts
3. Track free game schedule
4. Monitor launcher integration

## Notes
- Weekly free games every Thursday
- Epic exclusives may be timed
- Epic Games Launcher required for play
- Cross-platform purchases with some titles
