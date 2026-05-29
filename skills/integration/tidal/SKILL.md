---
name: tidal
description: Stream high-fidelity music on TIDAL, manage playlists, and access exclusive content
category: entertainment
---

# TIDAL Skill

## Overview
Enables Claude to interact with TIDAL for streaming high-fidelity audio, managing playlists, accessing exclusive artist content, and discovering music with lossless quality.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/tidal/install.sh | bash
```

Or manually:
```bash
cp -r skills/tidal ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TIDAL_EMAIL "your-email@example.com"
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
- Stream music in HiFi and Master quality
- Create and manage playlists
- Access exclusive artist content and videos
- View listening history
- Discover new music through TIDAL Rising

## Usage Examples
### Example 1: Create Playlist
```
User: "Create a jazz playlist on TIDAL"
Claude: I'll create a new jazz playlist and add some high-quality jazz tracks.
```

### Example 2: Find HiFi Content
```
User: "Play some Master quality albums"
Claude: I'll find albums available in Master quality for the best audio experience.
```

### Example 3: Artist Content
```
User: "Show me exclusive content from Beyonce on TIDAL"
Claude: I'll browse for exclusive Beyonce content including videos and interviews.
```

## Authentication Flow
1. Navigate to tidal.com via Playwright MCP
2. Click "Log In" button
3. Enter email and password
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Rate Limited: Implement exponential backoff
- Quality Unavailable: Check subscription tier for HiFi/Master
- Content Exclusive: Verify access to exclusive content

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document TIDAL interface changes
2. Update selectors for new layouts
3. Track audio quality availability
4. Monitor exclusive content releases

## Notes
- HiFi Plus required for Master quality
- Artist-owned platform with exclusives
- Dolby Atmos available on select content
- Credits feature shows song contributors
