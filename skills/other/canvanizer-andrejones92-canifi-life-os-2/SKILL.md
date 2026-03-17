---
name: canvanizer
description: Create and collaborate on business model canvases and strategic planning templates.
category: productivity
---
# Canvanizer Skill

Create and collaborate on business model canvases and strategic planning templates.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/canvanizer/install.sh | bash
```

Or manually:
```bash
cp -r skills/canvanizer ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CANVANIZER_EMAIL "your_email"
canifi-env set CANVANIZER_PASSWORD "your_password"
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

1. **Canvas Creation**: Create business model and lean canvases
2. **Template Library**: Access various strategic planning templates
3. **Team Collaboration**: Collaborate with team members in real-time
4. **Export Options**: Export canvases as PDF or images
5. **Brainstorming**: Use sticky notes for idea generation

## Usage Examples

### Create Canvas
```
User: "Create a new business model canvas for the startup idea"
Assistant: Creates business model canvas template
```

### Add Sticky Note
```
User: "Add a customer segment note to my canvas"
Assistant: Adds sticky note to customer segments section
```

### Share Canvas
```
User: "Share my canvas with the team"
Assistant: Generates sharing link for collaboration
```

### Export Canvas
```
User: "Export my business model canvas as PDF"
Assistant: Exports canvas to PDF format
```

## Authentication Flow

1. Create Canvanizer account
2. Use email/password for authentication
3. Session-based access
4. No official API available

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check email and password |
| Canvas Not Found | Invalid canvas ID | Verify canvas exists |
| Export Failed | Canvas too large | Reduce content |
| Session Expired | Login timeout | Re-authenticate |

## Notes

- Free tier available with limitations
- Multiple canvas templates
- Real-time collaboration
- No official API, uses browser automation
- Export to PDF, PNG, CSV
- Presentation mode available
