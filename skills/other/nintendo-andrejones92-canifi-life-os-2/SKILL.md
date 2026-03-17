---
name: nintendo
description: Manage Nintendo account, eShop, and Nintendo Switch Online features
category: gaming
---

# Nintendo Skill

## Overview
Enables Claude to interact with Nintendo services for managing game library, browsing eShop, accessing Nintendo Switch Online features, and tracking play activity.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/nintendo/install.sh | bash
```

Or manually:
```bash
cp -r skills/nintendo ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set NINTENDO_EMAIL "your-email@example.com"
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
- Browse Nintendo eShop and deals
- View game library and play history
- Access Nintendo Switch Online benefits
- Check My Nintendo rewards points
- View wish list and upcoming releases

## Usage Examples
### Example 1: eShop Deals
```
User: "What games are on sale on Nintendo eShop?"
Claude: I'll check the eShop for current deals and discounts.
```

### Example 2: Play Activity
```
User: "How much time have I spent playing Zelda?"
Claude: I'll check your play activity for The Legend of Zelda games.
```

### Example 3: Switch Online
```
User: "What classic games are on Nintendo Switch Online?"
Claude: I'll browse the Nintendo Switch Online library of classic titles.
```

## Authentication Flow
1. Navigate to nintendo.com via Playwright MCP
2. Click "Log In" button
3. Enter Nintendo Account credentials
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with Nintendo
- 2FA Required: Wait for code via email or app
- Rate Limited: Implement exponential backoff
- Region Lock: Note content availability by region

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Nintendo web interface changes
2. Update selectors for new layouts
3. Track eShop sale patterns
4. Monitor Switch Online additions

## Notes
- Nintendo Switch Online required for online play
- My Nintendo points for rewards
- Region differences in eShop content
- Family Membership available
