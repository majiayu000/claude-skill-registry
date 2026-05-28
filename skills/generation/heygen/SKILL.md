---
name: heygen
description: Create AI video content with HeyGen - generate avatar videos, translate content, and manage video projects
category: ai
---

# HeyGen Skill

## Overview
Enables Claude to use HeyGen for AI video generation including creating avatar videos, video translation, and managing video content projects.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/heygen/install.sh | bash
```

Or manually:
```bash
cp -r skills/heygen ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HEYGEN_EMAIL "your-email@example.com"
canifi-env set HEYGEN_PASSWORD "your-password"
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
- Create AI avatar videos
- Translate videos to other languages
- Manage video projects
- Select from avatar library
- Use video templates
- Download generated content

## Usage Examples

### Example 1: Create Avatar Video
```
User: "Create a welcome video with an AI spokesperson"
Claude: I'll create your welcome video.
1. Opening HeyGen via Playwright MCP
2. Creating new video project
3. Selecting avatar
4. Entering welcome script
5. Generating video
```

### Example 2: Translate Video
```
User: "Translate my video to Spanish"
Claude: I'll translate your video.
1. Uploading your video
2. Selecting Spanish as target
3. Initiating video translation
4. Downloading translated version
```

### Example 3: Download Video
```
User: "Download my completed HeyGen video"
Claude: I'll download your video.
1. Opening your project list
2. Finding the completed video
3. Accessing download options
4. Downloading in requested format
```

## Authentication Flow
1. Navigate to heygen.com via Playwright MCP
2. Click "Login" and enter email
3. Enter password
4. Handle Google SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Check credit balance
- **2FA Required**: Send iMessage notification
- **Generation Failed**: Retry with adjusted settings
- **Translation Error**: Check source video quality

## Self-Improvement Instructions
When HeyGen updates:
1. Document new avatars and voices
2. Update translation capabilities
3. Track feature additions
4. Log new template options

## Notes
- Credit-based video generation
- 100+ avatars available
- Video translation feature
- Custom avatar creation
- API available for integration
