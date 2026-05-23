---
name: clubhouse
description: Enables Claude to manage Clubhouse rooms and audio social interactions
version: 1.0.0
author: Canifi
category: social
---

# Clubhouse Skill

## Overview
Automates Clubhouse operations including browsing rooms, managing profile, and discovering audio content through web interface automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/clubhouse/install.sh | bash
```

Or manually:
```bash
cp -r skills/clubhouse ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CLUBHOUSE_PHONE "+1234567890"
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
- Browse live rooms
- Follow and unfollow users
- View upcoming events
- Manage profile settings
- Discover clubs
- View room replays
- Search users and clubs
- Access event calendar

## Usage Examples

### Example 1: Browse Rooms
```
User: "Find interesting rooms on Clubhouse"
Claude: I'll browse available rooms.
- Navigate to Clubhouse web
- Browse hallway/lobby
- List active rooms by topic
- Present interesting conversations
```

### Example 2: Check Events
```
User: "What Clubhouse events are coming up this week?"
Claude: I'll check upcoming events.
- Navigate to events section
- Browse this week's schedule
- List upcoming rooms
- Note interesting speakers
```

### Example 3: Search Clubs
```
User: "Find tech-related clubs on Clubhouse"
Claude: I'll search for tech clubs.
- Navigate to search
- Search technology-related terms
- Browse club results
- Present active clubs
```

### Example 4: View Profile
```
User: "Check my Clubhouse follower stats"
Claude: I'll check your profile.
- Navigate to profile
- View follower count
- Check following count
- Summarize activity
```

## Authentication Flow
1. Navigate to clubhouse.com via Playwright MCP
2. Enter phone number from canifi-env
3. Wait for SMS verification (notify user via iMessage)
4. Enter verification code
5. Verify access
6. Maintain session

## Error Handling
- **Login Failed**: Request new verification code
- **Session Expired**: Re-authenticate with phone
- **Verification Expired**: Request new SMS code
- **Room Unavailable**: Room may have ended
- **User Not Found**: Verify username
- **Club Not Found**: Search with alternatives
- **Feature Not Available**: Web has limited features
- **Rate Limited**: Wait before retrying

## Self-Improvement Instructions
When encountering new Clubhouse features:
1. Document new web interface elements
2. Add support for new room types
3. Log successful patterns
4. Update for platform changes

## Notes
- Clubhouse is audio-focused
- Web interface is limited vs app
- Most features require mobile app
- Rooms are real-time audio
- Replays available for some rooms
- Clubs are community spaces
- Live participation needs app
