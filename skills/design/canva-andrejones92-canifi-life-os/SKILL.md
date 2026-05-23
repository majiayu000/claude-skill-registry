---
name: canva
description: Create and edit designs in Canva - manage graphics, presentations, social media posts, and marketing materials
category: design
---

# Canva Skill

## Overview
Enables Claude to use Canva for creating and editing visual content including social media graphics, presentations, posters, videos, and marketing materials using templates or custom designs.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/canva/install.sh | bash
```

Or manually:
```bash
cp -r skills/canva ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CANVA_EMAIL "your-email@example.com"
canifi-env set CANVA_PASSWORD "your-password"
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
- Create designs from templates or scratch
- Edit existing designs (text, images, colors, fonts)
- Download designs in various formats (PNG, JPG, PDF, MP4)
- Manage brand kit assets (logos, colors, fonts)
- Access and organize design folders
- Schedule social media posts directly from Canva

## Usage Examples

### Example 1: Create Social Media Post
```
User: "Create an Instagram post for my product launch"
Claude: I'll create an Instagram post design for you.
1. Opening Canva via Playwright MCP
2. Selecting Instagram Post template size
3. Applying your brand colors and fonts
4. Adding product imagery and launch text
5. Saving to your designs folder
```

### Example 2: Download Presentation
```
User: "Download my quarterly report presentation as PDF"
Claude: I'll export your presentation.
1. Navigating to your presentations in Canva
2. Opening the quarterly report design
3. Selecting PDF export with print quality
4. Downloading to your specified location
```

### Example 3: Update Brand Colors
```
User: "Update my brand kit with new primary color #2563EB"
Claude: I'll update your brand kit.
1. Accessing Brand Kit settings
2. Modifying primary color to #2563EB
3. Saving brand kit changes
4. Confirming update across templates
```

## Authentication Flow
1. Navigate to canva.com via Playwright MCP
2. Click "Log in" and enter email
3. Enter password
4. Handle Google/SSO login if configured
5. Complete 2FA if required (via iMessage notification)
6. Maintain session for subsequent operations

## Error Handling
- **Login Failed**: Retry authentication up to 3 times, then notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send notification via iMessage for code
- **Template Not Found**: Search alternatives or prompt user
- **Export Failed**: Retry export or suggest alternative format

## Self-Improvement Instructions
When encountering new Canva features or UI changes:
1. Document the new workflow or element selectors
2. Test common operations after Canva updates
3. Log any breaking changes to Notion
4. Suggest skill updates based on new capabilities

## Notes
- Some features require Canva Pro subscription
- Large designs may take longer to load and export
- Brand Kit is only available with Canva Pro/Teams
- Video exports have processing time delays
- Template availability varies by account type
