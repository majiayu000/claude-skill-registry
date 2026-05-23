---
name: gog
description: Manage GOG.com library of DRM-free games, wishlist, and store deals
category: gaming
---

# GOG Skill

## Overview
Enables Claude to interact with GOG.com for managing DRM-free game library, tracking wishlist sales, claiming free games, and discovering classic and indie titles.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/gog/install.sh | bash
```

Or manually:
```bash
cp -r skills/gog ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOG_EMAIL "your-email@example.com"
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
- Browse and manage DRM-free game library
- Track wishlist and sale notifications
- Claim giveaway games
- View purchase history
- Access GOG Galaxy features

## Usage Examples
### Example 1: Wishlist Sales
```
User: "Are any of my GOG wishlist games on sale?"
Claude: I'll check your GOG wishlist for current discounts.
```

### Example 2: Library Check
```
User: "What games do I own on GOG?"
Claude: I'll browse your GOG library and list your DRM-free collection.
```

### Example 3: Free Games
```
User: "Any free games on GOG right now?"
Claude: I'll check for current GOG giveaways and claim any available.
```

## Authentication Flow
1. Navigate to gog.com via Playwright MCP
2. Click "Sign In" button
3. Enter email and password
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- 2FA Required: Wait for code via email
- Rate Limited: Implement exponential backoff
- Download Issues: Check offline installers availability

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document GOG interface changes
2. Update selectors for new layouts
3. Track giveaway schedules
4. Monitor Galaxy integration

## Notes
- All games are DRM-free
- Offline installers available
- GOG Galaxy optional but recommended
- GOG Connect for Steam library additions
