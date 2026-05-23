---
name: fathom
description: AI meeting assistant with automatic note-taking and summaries.
category: analytics
---
# Fathom Skill

AI meeting assistant with automatic note-taking and summaries.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/fathom/install.sh | bash
```

Or manually:
```bash
cp -r skills/fathom ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FATHOM_EMAIL "your_email"
canifi-env set FATHOM_PASSWORD "your_password"
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

1. **Auto-Record**: Join and record meetings
2. **AI Notes**: Automatic meeting notes
3. **Highlights**: Mark important moments
4. **Summaries**: Post-meeting summaries
5. **CRM Sync**: Update Salesforce/HubSpot

## Usage Examples

### View Recording
```
User: "Show my last meeting recording"
Assistant: Returns meeting video
```

### Get Notes
```
User: "Get notes from the sales call"
Assistant: Returns AI-generated notes
```

### Create Highlight
```
User: "Highlight the pricing discussion"
Assistant: Marks segment
```

### Sync to CRM
```
User: "Update Salesforce with this meeting"
Assistant: Syncs meeting data
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation
4. CRM OAuth connections

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Recording Failed | Permissions | Allow access |
| Sync Error | CRM connection | Reconnect |
| Processing Error | Video issue | Retry |

## Notes

- Free for individuals
- Auto-join meetings
- CRM integration
- Highlight clips
- No public API
- Team collaboration
