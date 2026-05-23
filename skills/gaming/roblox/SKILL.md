---
name: roblox
description: Manage Roblox account, track favorites, and monitor Robux balance
category: gaming
---

# Roblox Skill

## Overview
Enables Claude to interact with Roblox for managing account, browsing games, tracking favorites, monitoring Robux balance, and viewing friend activity.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/roblox/install.sh | bash
```

Or manually:
```bash
cp -r skills/roblox ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ROBLOX_EMAIL "your-email@example.com"
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
- Browse and discover Roblox experiences
- Manage favorite games list
- View Robux balance and transactions
- Check friend activity and status
- Track badges and achievements

## Usage Examples
### Example 1: Favorites Check
```
User: "What are my favorite Roblox games?"
Claude: I'll check your Roblox favorites list.
```

### Example 2: Robux Balance
```
User: "How much Robux do I have?"
Claude: I'll check your current Robux balance.
```

### Example 3: Friend Activity
```
User: "What games are my Roblox friends playing?"
Claude: I'll check what experiences your friends are currently in.
```

## Authentication Flow
1. Navigate to roblox.com via Playwright MCP
2. Click "Login" button
3. Enter credentials
4. Handle 2FA via email or authenticator
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- 2FA Required: Wait for code via email
- Rate Limited: Implement exponential backoff
- Age Restrictions: Note content filtering

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Roblox web interface changes
2. Update selectors for new layouts
3. Track popular experience trends
4. Monitor platform updates

## Notes
- Parental controls may limit access
- Robux is premium currency
- Experiences range widely in type
- Creator tools available
