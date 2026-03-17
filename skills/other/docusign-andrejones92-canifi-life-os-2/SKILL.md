---
name: docusign
description: Manage electronic signatures and agreements with DocuSign's e-signature platform.
category: legal
---
# DocuSign Skill

Manage electronic signatures and agreements with DocuSign's e-signature platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/docusign/install.sh | bash
```

Or manually:
```bash
cp -r skills/docusign ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DOCUSIGN_INTEGRATION_KEY "your_integration_key"
canifi-env set DOCUSIGN_USER_ID "your_user_id"
canifi-env set DOCUSIGN_ACCOUNT_ID "your_account_id"
canifi-env set DOCUSIGN_PRIVATE_KEY "your_private_key"
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

1. **Send Documents**: Send documents for signature with signing order
2. **Template Management**: Create and use reusable templates
3. **Envelope Tracking**: Track signature status and reminders
4. **Bulk Send**: Send documents to multiple recipients
5. **API Integration**: Embed signing in custom applications

## Usage Examples

### Send for Signature
```
User: "Send the contract to john@company.com for signature"
Assistant: Creates envelope and sends for signing
```

### Check Status
```
User: "What's the status of the NDA I sent yesterday?"
Assistant: Returns envelope status and activity
```

### Create Template
```
User: "Create a template from this signed agreement"
Assistant: Creates reusable template
```

### Send Reminder
```
User: "Send a reminder for the unsigned contract"
Assistant: Sends reminder to pending signers
```

## Authentication Flow

1. Create integration key in DocuSign Admin
2. Configure JWT or OAuth authentication
3. Generate access token for API calls
4. Use environment-specific endpoints

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Token expired | Refresh access token |
| 400 Bad Request | Invalid envelope data | Validate document format |
| 404 Not Found | Envelope not found | Verify envelope ID |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- Industry leader in e-signatures
- ESIGN and UETA compliant
- 400+ integrations
- Advanced authentication options
- Audit trail included
- Enterprise security features
