---
name: adobesign
description: Manage enterprise e-signatures with Adobe Sign's document signing solution.
category: legal
---
# Adobe Sign Skill

Manage enterprise e-signatures with Adobe Sign's document signing solution.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/adobesign/install.sh | bash
```

Or manually:
```bash
cp -r skills/adobesign ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ADOBE_SIGN_CLIENT_ID "your_client_id"
canifi-env set ADOBE_SIGN_CLIENT_SECRET "your_client_secret"
canifi-env set ADOBE_SIGN_ACCESS_TOKEN "your_access_token"
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

1. **Agreement Sending**: Send documents for signature with workflows
2. **Mega Sign**: Send to hundreds of recipients at once
3. **Web Forms**: Create fillable web forms for signatures
4. **Workflow Automation**: Build automated signing workflows
5. **Compliance**: Industry-specific compliance solutions

## Usage Examples

### Send Agreement
```
User: "Send the contract to the legal team for signatures"
Assistant: Creates agreement with signing workflow
```

### Create Web Form
```
User: "Create a signup form with signature field"
Assistant: Creates web form for signatures
```

### Check Status
```
User: "What agreements are pending signature?"
Assistant: Returns pending agreements
```

### Download Audit
```
User: "Download the audit trail for the signed agreement"
Assistant: Downloads audit report
```

## Authentication Flow

1. Create integration in Adobe Sign admin
2. Implement OAuth 2.0 flow
3. Get access token for API calls
4. Refresh tokens as needed

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Token expired | Refresh access token |
| 403 Forbidden | No permission | Check user permissions |
| 404 Not Found | Agreement not found | Verify agreement ID |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- Part of Adobe Document Cloud
- Enterprise-grade features
- Advanced workflows
- Compliance certifications
- Microsoft and Salesforce integrations
- Premium pricing
