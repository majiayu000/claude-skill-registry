---
name: hellosign
description: Manage electronic signatures with HelloSign's simple e-signature solution.
category: legal
---
# HelloSign Skill

Manage electronic signatures with HelloSign's simple e-signature solution.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/hellosign/install.sh | bash
```

Or manually:
```bash
cp -r skills/hellosign ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HELLOSIGN_API_KEY "your_api_key"
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

1. **Signature Requests**: Send documents for electronic signature
2. **Templates**: Create and use signature templates
3. **Team Management**: Manage team members and permissions
4. **Embedded Signing**: Embed signing experience in apps
5. **API Access**: Full API for custom integrations

## Usage Examples

### Send Signature Request
```
User: "Send this document to Sarah for signature"
Assistant: Creates and sends signature request
```

### Use Template
```
User: "Send the NDA template to the new client"
Assistant: Creates request from template
```

### Check Status
```
User: "Is the contract signed yet?"
Assistant: Returns signature request status
```

### Download Signed
```
User: "Download the signed agreement"
Assistant: Downloads completed document
```

## Authentication Flow

1. Get API key from HelloSign settings
2. Use API key for Basic Auth
3. API key provides full access
4. Test mode available

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 400 Bad Request | Invalid request | Check parameters |
| 404 Not Found | Request not found | Verify request ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Now part of Dropbox
- Simple, developer-friendly API
- Unlimited templates in Pro
- Team features available
- White-labeling options
- Competitive pricing
