---
name: discord
description: Enables Claude to manage Discord servers, send messages, moderate communities, and handle voice channel operations
version: 1.0.0
author: Canifi
category: communication
---

# Discord Skill

## Overview
Automates Discord interactions including messaging, server management, moderation, and community engagement through the Discord web application.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/discord/install.sh | bash
```

Or manually:
```bash
cp -r skills/discord ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DISCORD_EMAIL "your-email@example.com"
canifi-env set DISCORD_PASSWORD "your-password"
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
- Send direct messages and server messages
- Create and manage servers, channels, and categories
- Moderate users (kick, ban, timeout, roles)
- Search messages and users across servers
- Manage server settings and permissions
- React to messages and add emoji reactions
- Create and manage events
- Handle friend requests and relationships

## Usage Examples

### Example 1: Send a Direct Message
```
User: "Send a Discord DM to GameMaster asking about tonight's session"
Claude: I'll send that DM on Discord.
- Navigate to Discord web app
- Open DM with GameMaster
- Type and send: "Hey, are we still on for tonight's session?"
- Confirm message delivered
```

### Example 2: Post in a Server Channel
```
User: "Announce in the #announcements channel that the event is starting"
Claude: I'll post the announcement.
- Navigate to specified server
- Open #announcements channel
- Compose and send announcement message
- Confirm post successful
```

### Example 3: Moderate a User
```
User: "Give user ToxicPlayer a 1 hour timeout in the gaming server"
Claude: I'll apply the timeout.
- Navigate to the gaming server
- Find user ToxicPlayer
- Apply 1 hour timeout via moderation menu
- Confirm timeout applied
```

### Example 4: Create an Event
```
User: "Create a Discord event for Friday at 8pm called 'Game Night'"
Claude: I'll create the event.
- Navigate to server events
- Create new event "Game Night"
- Set date/time for Friday 8pm
- Confirm event created and shareable
```

## Authentication Flow
1. Navigate to discord.com/app via Playwright MCP
2. Enter email and password from canifi-env
3. Handle CAPTCHA if presented (notify user)
4. Complete 2FA via authenticator (notify user via iMessage)
5. Verify login successful by checking for servers list
6. Maintain session for subsequent operations

## Error Handling
- **Login Failed**: Clear cookies, retry 3x, then iMessage notification
- **Session Expired**: Re-authenticate with stored credentials
- **Rate Limited**: Wait for rate limit to clear (typically 5-60 seconds)
- **2FA Required**: iMessage notification for authenticator code
- **CAPTCHA Detected**: Notify user to complete manually
- **Server Not Found**: List available servers for user selection
- **Permission Denied**: Notify user of missing permissions
- **User Not Found**: Search server members and suggest matches

## Self-Improvement Instructions
When encountering new Discord features or UI changes:
1. Document updated selectors and interaction patterns
2. Add new capabilities to the list
3. Log successful moderation workflows
4. Suggest SKILL.md updates for new features

## Notes
- Discord uses dynamic content loading; wait for elements properly
- Voice channels cannot be fully automated (audio limitations)
- Some servers require phone verification
- Nitro features may not be available on free accounts
- Bot detection may trigger additional verification
- Server boosts affect available features
