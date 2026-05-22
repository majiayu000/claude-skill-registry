---
name: zeplin
description: Handoff designs to developers with Zeplin - access design specs, export assets, and manage style guides
category: design
---

# Zeplin Skill

## Overview
Enables Claude to use Zeplin for design-to-development handoff including accessing design specifications, downloading assets, viewing style guides, and managing design documentation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/zeplin/install.sh | bash
```

Or manually:
```bash
cp -r skills/zeplin ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ZEPLIN_EMAIL "your-email@example.com"
canifi-env set ZEPLIN_PASSWORD "your-password"
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
- View design specifications and measurements
- Download assets in multiple formats
- Access component libraries
- Review style guides and colors
- Navigate project screens
- Export CSS/code snippets

## Usage Examples

### Example 1: Get Design Specs
```
User: "What are the specifications for the header component?"
Claude: I'll pull up the header specs.
1. Opening Zeplin via Playwright MCP
2. Navigating to the project
3. Finding the header component
4. Extracting dimensions, colors, and fonts
5. Summarizing specifications
```

### Example 2: Download Assets
```
User: "Download all icons from the design system in SVG format"
Claude: I'll download the icons.
1. Opening the design system project
2. Navigating to assets section
3. Selecting all icons
4. Exporting as SVG format
5. Downloading to your folder
```

### Example 3: Get Color Palette
```
User: "Show me the color palette from our style guide"
Claude: I'll retrieve the color palette.
1. Opening the style guide project
2. Navigating to colors section
3. Listing all defined colors with hex codes
4. Organizing by category (primary, secondary, etc.)
```

## Authentication Flow
1. Navigate to app.zeplin.io via Playwright MCP
2. Click "Sign in" and enter email
3. Enter password
4. Handle SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Project Not Found**: Search workspace or verify access
- **Asset Export Failed**: Retry or try different format

## Self-Improvement Instructions
When Zeplin updates:
1. Document new specification features
2. Update asset export workflows
3. Track code snippet improvements
4. Log style guide enhancements

## Notes
- Requires projects synced from design tools
- Supports Figma, Sketch, XD integrations
- Code snippets available in multiple languages
- Assets exportable in 1x, 2x, 3x scales
- Style guide requires pro/business plans
