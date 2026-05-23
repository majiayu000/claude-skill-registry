---
name: itch-io
description: Discover and manage indie games on itch.io, track jams, and support creators
category: gaming
---

# itch.io Skill

## Overview
Enables Claude to interact with itch.io for discovering indie games, managing purchased/downloaded games, participating in game jams, and supporting independent developers.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/itch-io/install.sh | bash
```

Or manually:
```bash
cp -r skills/itch-io ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ITCHIO_EMAIL "your-email@example.com"
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
- Browse and discover indie games
- Manage owned games library
- Track game jams and submissions
- View creator pages and projects
- Access pay-what-you-want games

## Usage Examples
### Example 1: Browse Games
```
User: "Find me some free horror games on itch.io"
Claude: I'll search itch.io for free horror games with good ratings.
```

### Example 2: Game Jams
```
User: "What game jams are happening this month?"
Claude: I'll check the current and upcoming game jams on itch.io.
```

### Example 3: My Library
```
User: "What games have I claimed on itch.io?"
Claude: I'll browse your itch.io library for owned games.
```

## Authentication Flow
1. Navigate to itch.io via Playwright MCP
2. Click "Log In" button
3. Enter email and password
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- 2FA Required: Wait for code via email
- Rate Limited: Implement exponential backoff
- Download Issues: Check game availability

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document itch.io interface changes
2. Update selectors for new layouts
3. Track bundle offerings
4. Monitor jam schedules

## Notes
- Focus on indie and experimental games
- Pay-what-you-want pricing common
- Game jams foster community
- Supports game development uploads
