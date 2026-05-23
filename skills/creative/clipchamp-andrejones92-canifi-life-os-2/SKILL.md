---
name: clipchamp
description: Edit videos with Clipchamp (Microsoft) - create, edit, and export videos with templates and stock media
category: video
---

# Clipchamp Skill

## Overview
Enables Claude to use Microsoft Clipchamp for video editing including creating projects, using templates, accessing stock media, and exporting finished videos.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/clipchamp/install.sh | bash
```

Or manually:
```bash
cp -r skills/clipchamp ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CLIPCHAMP_EMAIL "your-email@example.com"
canifi-env set CLIPCHAMP_PASSWORD "your-password"
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
- Create and edit video projects
- Use video templates
- Access stock video and audio
- Apply filters and effects
- Export in various resolutions
- Use text-to-speech features

## Usage Examples

### Example 1: Create from Template
```
User: "Create a promo video using a template"
Claude: I'll create a promo video.
1. Opening Clipchamp via Playwright MCP
2. Browsing promotional templates
3. Selecting suitable template
4. Customizing text and media
5. Exporting the final video
```

### Example 2: Add Stock Media
```
User: "Add some stock footage of office work to my video"
Claude: I'll add stock footage.
1. Opening your video project
2. Browsing stock video library
3. Searching "office work"
4. Adding selected clips to timeline
```

### Example 3: Export Video
```
User: "Export my video in 1080p"
Claude: I'll export your video.
1. Opening your project
2. Selecting 1080p export quality
3. Initiating export
4. Downloading finished video
```

## Authentication Flow
1. Navigate to clipchamp.com via Playwright MCP
2. Click "Sign in" with Microsoft account
3. Enter email and password
4. Handle 2FA if required (via iMessage)
5. Maintain session for editing

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Export Failed**: Check project settings
- **Media Error**: Verify file formats

## Self-Improvement Instructions
When Clipchamp updates:
1. Document new editing features
2. Update template categories
3. Track AI feature additions
4. Log export quality options

## Notes
- Part of Microsoft 365
- Free tier available
- Stock media library included
- Browser-based editing
- Integrates with OneDrive
