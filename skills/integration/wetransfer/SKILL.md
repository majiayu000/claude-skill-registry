---
name: wetransfer
description: Simple file sharing for large files up to 2GB.
category: utilities
---
# WeTransfer Skill

Simple file sharing for large files up to 2GB.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/wetransfer/install.sh | bash
```

Or manually:
```bash
cp -r skills/wetransfer ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WETRANSFER_API_KEY "your_api_key"
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

1. **Send Files**: Transfer large files
2. **Track Transfers**: Monitor download status
3. **Manage Transfers**: View transfer history
4. **Custom Links**: Branded transfer pages
5. **Team Transfers**: Collaborate on sends

## Usage Examples

### Send Files
```
User: "Send these files via WeTransfer"
Assistant: Creates transfer and shares link
```

### Check Status
```
User: "Has my transfer been downloaded?"
Assistant: Returns download status
```

### View History
```
User: "Show my recent transfers"
Assistant: Returns transfer list
```

### Create Link
```
User: "Create a WeTransfer link for this folder"
Assistant: Generates transfer link
```

## Authentication Flow

1. API key authentication
2. Pro features require account
3. OAuth for integrations
4. No auth for basic sends

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| File Too Large | Exceeds limit | Split or upgrade |
| Transfer Expired | Past 7 days | Resend |
| Upload Failed | Network issue | Retry |

## Notes

- Up to 2GB free
- Pro for more storage
- Custom branding
- Password protection
- API available
- Download notifications
