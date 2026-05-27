---
name: box
description: Enterprise cloud content management and collaboration.
category: utilities
---
# Box Skill

Enterprise cloud content management and collaboration.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/box/install.sh | bash
```

Or manually:
```bash
cp -r skills/box ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BOX_CLIENT_ID "your_client_id"
canifi-env set BOX_CLIENT_SECRET "your_client_secret"
canifi-env set BOX_ACCESS_TOKEN "your_token"
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

1. **File Management**: Upload, download, organize
2. **Collaboration**: Comments and tasks
3. **Share Content**: Create shared links
4. **Box Notes**: Collaborative documents
5. **Workflows**: Automate processes

## Usage Examples

### Upload File
```
User: "Upload this to Box"
Assistant: Uploads file to Box
```

### Share Folder
```
User: "Share this folder with the team"
Assistant: Creates collaboration
```

### Add Comment
```
User: "Comment on this document"
Assistant: Adds comment to file
```

### Search Content
```
User: "Find Q4 reports in Box"
Assistant: Returns matching content
```

## Authentication Flow

1. OAuth2 authentication
2. JWT for server apps
3. Developer tokens available
4. Enterprise SSO support

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid token | Re-authorize |
| Not Found | Wrong ID | Verify file exists |
| Forbidden | Permissions | Check access |
| Rate Limited | Too many requests | Back off |

## Notes

- Enterprise-focused
- Full REST API
- Box Platform
- Governance features
- Workflow automation
- Integration ecosystem
