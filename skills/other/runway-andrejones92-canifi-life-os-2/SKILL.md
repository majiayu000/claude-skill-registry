---
name: runway
description: Create with AI video tools on Runway - generate videos, edit with AI, and use creative ML models
category: ai
---

# Runway Skill

## Overview
Enables Claude to use Runway for AI-powered video creation including generating videos from text, using Gen-2 AI features, and managing creative projects.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/runway/install.sh | bash
```

Or manually:
```bash
cp -r skills/runway ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set RUNWAY_EMAIL "your-email@example.com"
canifi-env set RUNWAY_PASSWORD "your-password"
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
- Generate video from text prompts
- Use image-to-video generation
- Apply AI video editing tools
- Manage generation history
- Download generated content
- Access AI creative tools

## Usage Examples

### Example 1: Generate Video from Text
```
User: "Generate a 4-second video of ocean waves at sunset"
Claude: I'll generate that video.
1. Opening Runway via Playwright MCP
2. Accessing Gen-2 text-to-video
3. Entering prompt: "ocean waves at sunset, cinematic"
4. Generating video
5. Providing download link
```

### Example 2: Image to Video
```
User: "Animate my product image"
Claude: I'll create an animated video.
1. Opening image-to-video tool
2. Uploading your product image
3. Adding motion parameters
4. Generating animated video
5. Downloading result
```

### Example 3: Check Generation History
```
User: "Show me my recent AI generations"
Claude: I'll pull up your history.
1. Opening Runway dashboard
2. Accessing generation history
3. Listing recent creations
4. Providing preview and download links
```

## Authentication Flow
1. Navigate to runwayml.com via Playwright MCP
2. Click "Sign in" and enter email
3. Enter password
4. Handle Google SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Check credit balance
- **2FA Required**: Send iMessage notification
- **Generation Failed**: Retry with modified prompt
- **Credit Depleted**: Notify about subscription

## Self-Improvement Instructions
When Runway updates:
1. Document new AI models
2. Update generation parameters
3. Track quality improvements
4. Log new creative tools

## Notes
- Credit-based generation system
- Gen-2 for advanced video
- Processing times vary
- Resolution affects credits
- Commercial use on paid plans
