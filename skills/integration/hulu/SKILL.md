---
name: hulu
description: Stream Hulu content, manage watchlist, and access live TV features
category: entertainment
---

# Hulu Skill

## Overview
Enables Claude to interact with Hulu for streaming content, managing watchlist, accessing live TV (if subscribed), and discovering new shows and movies.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/hulu/install.sh | bash
```

Or manually:
```bash
cp -r skills/hulu ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HULU_EMAIL "your-email@example.com"
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
- Browse on-demand movies and TV shows
- Access live TV channels and DVR (Hulu + Live TV)
- Manage "My Stuff" watchlist
- View watch history and continue watching
- Search for specific content or networks

## Usage Examples
### Example 1: Add to My Stuff
```
User: "Add The Handmaid's Tale to my Hulu watchlist"
Claude: I'll add The Handmaid's Tale to your My Stuff list on Hulu.
```

### Example 2: Live TV Access
```
User: "What's on ESPN right now?"
Claude: I'll check the live TV guide and show you what's currently airing on ESPN.
```

### Example 3: Continue Watching
```
User: "What was I watching on Hulu?"
Claude: I'll check your continue watching section to see your in-progress shows.
```

## Authentication Flow
1. Navigate to hulu.com via Playwright MCP
2. Click "Log In" button
3. Enter email and password
4. Select profile if multiple exist
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Live TV Unavailable: Check subscription tier and notify user
- Rate Limited: Implement exponential backoff
- Content Unavailable: Check for regional or subscription restrictions

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document interface changes
2. Update element selectors
3. Track feature availability by subscription tier
4. Log successful navigation patterns

## Notes
- Live TV features require Hulu + Live TV subscription
- Ad-supported vs ad-free tiers affect experience
- DVR functionality varies by subscription
- Some content has expiration dates
