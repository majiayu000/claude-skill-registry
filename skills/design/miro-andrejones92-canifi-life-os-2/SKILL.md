---
name: miro
description: Collaborate on digital whiteboards with Miro - create mind maps, flowcharts, wireframes, and run brainstorming sessions
category: design
---

# Miro Skill

## Overview
Enables Claude to use Miro for visual collaboration including creating and editing boards, adding shapes and content, managing templates, and organizing brainstorming or planning sessions.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/miro/install.sh | bash
```

Or manually:
```bash
cp -r skills/miro ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MIRO_EMAIL "your-email@example.com"
canifi-env set MIRO_PASSWORD "your-password"
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
- Create and navigate Miro boards
- Add shapes, sticky notes, and text
- Create flowcharts and diagrams
- Apply templates for various workflows
- Export boards as images or PDFs
- Manage board sharing and permissions

## Usage Examples

### Example 1: Create Mind Map
```
User: "Create a mind map for our Q1 planning"
Claude: I'll create a mind map board for Q1 planning.
1. Opening Miro via Playwright MCP
2. Creating new board with mind map template
3. Adding central topic "Q1 Planning"
4. Creating branches for key initiatives
5. Sharing board link with you
```

### Example 2: Export Board
```
User: "Export the product roadmap board as PDF"
Claude: I'll export your roadmap board.
1. Navigating to the product roadmap board
2. Opening export options
3. Selecting PDF format with high quality
4. Downloading the exported file
```

### Example 3: Add Flowchart
```
User: "Add a user flow diagram to my UX board"
Claude: I'll add a user flow to your board.
1. Opening the UX board in Miro
2. Adding flowchart shapes
3. Creating connections between steps
4. Labeling each flow step
5. Organizing layout for clarity
```

## Authentication Flow
1. Navigate to miro.com via Playwright MCP
2. Click "Log in" and enter email
3. Enter password
4. Handle SSO if configured
5. Complete 2FA if required (via iMessage)
6. Maintain session for board operations

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage for verification code
- **Board Not Found**: Search boards or prompt for correct name
- **Permission Denied**: Notify about access restrictions

## Self-Improvement Instructions
When Miro updates its interface:
1. Document new tools and template locations
2. Update board navigation patterns
3. Test shape creation and editing workflows
4. Log any selector or UI changes

## Notes
- Large boards may have performance impacts
- Real-time collaboration shows other users
- Some templates require paid plans
- Export quality varies by format choice
- Embedded content may not export fully
