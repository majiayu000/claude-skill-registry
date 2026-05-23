---
name: riot-games
description: Manage Riot Games account, track stats across League, Valorant, and more
category: gaming
---

# Riot Games Skill

## Overview
Enables Claude to interact with Riot Games account for viewing game statistics, tracking ranked progress, managing account settings, and checking event rewards across League of Legends, Valorant, and other Riot titles.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/riot-games/install.sh | bash
```

Or manually:
```bash
cp -r skills/riot-games ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set RIOT_EMAIL "your-email@example.com"
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
- View stats across Riot games
- Track ranked progress and history
- Check event passes and missions
- Manage Riot Points balance
- View match history

## Usage Examples
### Example 1: Ranked Progress
```
User: "What's my Valorant rank?"
Claude: I'll check your Valorant competitive ranking and recent matches.
```

### Example 2: Event Missions
```
User: "What missions do I have in League?"
Claude: I'll check your active League of Legends missions and event progress.
```

### Example 3: Match History
```
User: "Show me my recent Valorant games"
Claude: I'll pull up your recent Valorant match history with stats.
```

## Authentication Flow
1. Navigate to account.riotgames.com via Playwright MCP
2. Click "Sign In" button
3. Enter Riot credentials
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with Riot
- 2FA Required: Wait for code via email
- Rate Limited: Implement exponential backoff
- Region Mismatch: Handle multi-region accounts

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Riot account changes
2. Update selectors for new layouts
3. Track new game additions
4. Monitor event schedules

## Notes
- Single account for all Riot games
- Regional servers affect matchmaking
- Riot Points shared across games
- Prime Gaming rewards available
