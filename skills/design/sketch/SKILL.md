---
name: sketch
description: Design interfaces with Sketch - view designs in the web app, manage shared libraries, and collaborate on projects
category: design
---

# Sketch Skill

## Overview
Enables Claude to interact with Sketch's web platform for viewing designs, managing shared libraries, accessing design documentation, and collaborating on UI/UX projects.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/sketch/install.sh | bash
```

Or manually:
```bash
cp -r skills/sketch ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SKETCH_EMAIL "your-email@example.com"
canifi-env set SKETCH_PASSWORD "your-password"
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
- View designs in Sketch web app
- Browse and manage workspaces
- Access shared design libraries
- View and export artboards
- Review design comments
- Manage document versions

## Usage Examples

### Example 1: View Design Specs
```
User: "Show me the design specs for the login screen"
Claude: I'll pull up the login screen specs.
1. Opening Sketch web via Playwright MCP
2. Navigating to your workspace
3. Finding the login screen artboard
4. Displaying measurements and specs
5. Summarizing key design details
```

### Example 2: Export Assets
```
User: "Export icons from my design as SVGs"
Claude: I'll export your icons.
1. Opening the design document
2. Navigating to icons artboard
3. Selecting export format as SVG
4. Downloading icon assets
```

### Example 3: Check Version History
```
User: "What changes were made to the dashboard design yesterday?"
Claude: I'll check the version history.
1. Opening the dashboard document
2. Accessing version history
3. Filtering to yesterday's changes
4. Summarizing modifications made
```

## Authentication Flow
1. Navigate to sketch.com via Playwright MCP
2. Click "Sign In" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for workspace access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Document Not Found**: Search workspace or verify link
- **Export Failed**: Retry or check permissions

## Self-Improvement Instructions
When Sketch web updates:
1. Document new viewing capabilities
2. Update export workflow changes
3. Track collaboration features
4. Log library management updates

## Notes
- Full editing requires Sketch desktop app
- Web app is primarily for viewing/collaboration
- Sketch is macOS-only for editing
- Shared libraries require team plan
- Comments sync between web and desktop
