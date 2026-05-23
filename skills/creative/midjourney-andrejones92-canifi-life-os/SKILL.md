---
name: midjourney
description: Generate AI art with Midjourney - create images from prompts, manage generations, and iterate on creative concepts
category: ai
---

# Midjourney Skill

## Overview
Enables Claude to interact with Midjourney for AI image generation through the web interface, including creating images from prompts, managing generated images, and iterating on designs.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/midjourney/install.sh | bash
```

Or manually:
```bash
cp -r skills/midjourney ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MIDJOURNEY_EMAIL "your-email@example.com"
canifi-env set MIDJOURNEY_PASSWORD "your-password"
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
- Generate images from text prompts
- View and manage generated images
- Upscale and create variations
- Download generated images
- Browse generation history
- Organize images into folders

## Usage Examples

### Example 1: Generate Image
```
User: "Create a Midjourney image of a futuristic city at sunset"
Claude: I'll generate that image for you.
1. Opening Midjourney web via Playwright MCP
2. Navigating to generation interface
3. Entering prompt: "futuristic city at sunset, cinematic lighting"
4. Waiting for generation to complete
5. Showing you the results
```

### Example 2: Create Variations
```
User: "Make variations of my favorite generated image"
Claude: I'll create variations.
1. Navigating to your generation history
2. Finding the specified image
3. Clicking variation option
4. Waiting for new variations
5. Displaying results for review
```

### Example 3: Download Upscaled Image
```
User: "Upscale and download the third image from my last generation"
Claude: I'll upscale and download it.
1. Finding your recent generation
2. Selecting the third image
3. Clicking upscale option
4. Waiting for upscale to complete
5. Downloading full resolution image
```

## Authentication Flow
1. Navigate to midjourney.com via Playwright MCP
2. Sign in with account credentials
3. Handle Discord OAuth if required
4. Complete 2FA if enabled (via iMessage)
5. Maintain session for generations

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Wait and retry, check subscription
- **2FA Required**: Send iMessage notification
- **Generation Failed**: Retry with modified prompt
- **Queue Full**: Wait for availability

## Self-Improvement Instructions
When Midjourney updates:
1. Document new generation parameters
2. Update prompt formatting best practices
3. Track interface changes
4. Log new features and capabilities

## Notes
- Subscription required for generations
- Generation times vary by queue
- Discord integration may be needed
- Image rights vary by plan
- Prompt crafting affects quality
