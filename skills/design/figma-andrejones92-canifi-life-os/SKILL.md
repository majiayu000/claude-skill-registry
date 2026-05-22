---
name: figma
description: Design and prototype interfaces in Figma - create, edit, and manage design files, components, and collaborate on design projects
category: design
---

# Figma Skill

## Overview
Enables Claude to interact with Figma for UI/UX design work, including creating and managing design files, viewing designs, exporting assets, and managing team collaboration.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/figma/install.sh | bash
```

Or manually:
```bash
cp -r skills/figma ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FIGMA_EMAIL "your-email@example.com"
canifi-env set FIGMA_PASSWORD "your-password"
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
- View and navigate design files, frames, and pages
- Export assets in various formats (PNG, SVG, PDF, JPG)
- Access and manage team libraries and components
- Review design comments and feedback
- Check file version history and restore previous versions
- Manage file sharing and permissions

## Usage Examples

### Example 1: Export Design Assets
```
User: "Export all icons from my Figma design file as SVGs"
Claude: I'll navigate to your Figma file and export the icons.
1. Opening Figma via Playwright MCP
2. Navigating to the specified file
3. Selecting icon frames
4. Exporting as SVG format
5. Downloading to your specified location
```

### Example 2: View Design Feedback
```
User: "Show me all comments on my homepage design"
Claude: I'll pull up the comments on your homepage design.
1. Opening the design file in Figma
2. Navigating to the homepage frame
3. Displaying all comments with author and timestamp
4. Summarizing feedback themes
```

### Example 3: Check Design Versions
```
User: "What changes were made to the login screen this week?"
Claude: I'll review the version history for the login screen.
1. Accessing file version history
2. Filtering changes from this week
3. Comparing versions to identify modifications
4. Summarizing key design changes
```

## Authentication Flow
1. Navigate to figma.com via Playwright MCP
2. Enter email credentials
3. Handle password entry
4. Complete 2FA if required (via iMessage notification)
5. Maintain session cookies for subsequent requests

## Error Handling
- **Login Failed**: Retry authentication up to 3 times, then notify via iMessage
- **Session Expired**: Re-authenticate automatically using stored credentials
- **Rate Limited**: Implement exponential backoff (1s, 2s, 4s, 8s)
- **2FA Required**: Send code request notification via iMessage, wait for user input
- **File Not Found**: Prompt user to verify file URL or name
- **Permission Denied**: Notify user of access restrictions

## Self-Improvement Instructions
When encountering new Figma UI patterns or workflows:
1. Document the specific interaction pattern
2. Note any selectors or navigation paths that changed
3. Suggest updates to this skill file via PR or Notion log
4. Track success/failure rates for common operations

## Notes
- Figma files can be large; allow adequate loading time
- Some features require paid Figma plans
- Plugin interactions are limited via browser automation
- Real-time collaboration features may show other users' cursors
- FigJam boards use different UI patterns than design files
