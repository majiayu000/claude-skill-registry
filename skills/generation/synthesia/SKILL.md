---
name: synthesia
description: Create AI avatar videos with Synthesia - generate spokesperson videos, manage projects, and export content
category: ai
---

# Synthesia Skill

## Overview
Enables Claude to use Synthesia for AI avatar video creation including generating videos with AI presenters, managing projects, and accessing video templates.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/synthesia/install.sh | bash
```

Or manually:
```bash
cp -r skills/synthesia ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SYNTHESIA_EMAIL "your-email@example.com"
canifi-env set SYNTHESIA_PASSWORD "your-password"
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
- Manage video projects
- Select from avatar library
- Use video templates
- Export finished videos
- Configure video settings

## Usage Examples

### Example 1: Create Avatar Video
```
User: "Create a training video with an AI presenter"
Claude: I'll create an avatar video.
1. Opening Synthesia via Playwright MCP
2. Creating new video project
3. Selecting AI avatar
4. Entering script text
5. Generating video
```

### Example 2: Use Template
```
User: "Make a product demo video using a template"
Claude: I'll create from template.
1. Browsing video templates
2. Selecting product demo template
3. Customizing text and branding
4. Generating final video
```

### Example 3: Check Project Status
```
User: "Is my video done rendering?"
Claude: I'll check the status.
1. Opening your projects
2. Finding the video
3. Checking rendering progress
4. Reporting completion status
```

## Authentication Flow
1. Navigate to synthesia.io via Playwright MCP
2. Click "Log in" and enter email
3. Enter password
4. Handle SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Check video credits
- **2FA Required**: Send iMessage notification
- **Rendering Failed**: Check script and retry
- **Credit Limit**: Notify about plan usage

## Self-Improvement Instructions
When Synthesia updates:
1. Document new avatars
2. Update template categories
3. Track language additions
4. Log new features

## Notes
- Credit-based video generation
- 140+ AI avatars available
- 120+ languages supported
- Custom avatars on enterprise
- Templates for common use cases
