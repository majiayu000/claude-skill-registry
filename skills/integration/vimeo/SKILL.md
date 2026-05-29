---
name: vimeo
description: Host and manage videos with Vimeo - upload, organize, and analyze professional video content
category: video
---

# Vimeo Skill

## Overview
Enables Claude to use Vimeo for professional video hosting and management including uploading content, organizing libraries, accessing analytics, and managing video settings.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/vimeo/install.sh | bash
```

Or manually:
```bash
cp -r skills/vimeo ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set VIMEO_EMAIL "your-email@example.com"
canifi-env set VIMEO_PASSWORD "your-password"
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
- Upload and manage videos
- Organize video libraries and folders
- Access video analytics and engagement data
- Configure privacy and embed settings
- Manage video descriptions and metadata
- Download video files and data

## Usage Examples

### Example 1: Check Video Analytics
```
User: "Show me the performance stats for my latest product video"
Claude: I'll pull up your video analytics.
1. Opening Vimeo via Playwright MCP
2. Navigating to your video library
3. Finding the product video
4. Accessing analytics dashboard
5. Summarizing views, engagement, and completion rates
```

### Example 2: Organize Videos
```
User: "Create a folder for client testimonials and move relevant videos"
Claude: I'll organize your testimonial videos.
1. Creating new folder "Client Testimonials"
2. Searching for testimonial videos
3. Moving selected videos to folder
4. Confirming organization complete
```

### Example 3: Update Video Settings
```
User: "Make my training video password protected"
Claude: I'll update the privacy settings.
1. Finding the training video
2. Opening video settings
3. Enabling password protection
4. Setting your chosen password
5. Confirming settings saved
```

## Authentication Flow
1. Navigate to vimeo.com via Playwright MCP
2. Click "Log in" and enter email
3. Enter password
4. Handle Google SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Upload Failed**: Check file format and size
- **Video Not Found**: Search library or verify ID

## Self-Improvement Instructions
When Vimeo updates:
1. Document new analytics features
2. Update privacy setting options
3. Track player customization changes
4. Log new integration features

## Notes
- Upload limits vary by subscription
- Video quality depends on plan
- Analytics depth varies by tier
- Embed customization available
- Live streaming requires Pro+
