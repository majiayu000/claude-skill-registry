---
name: clio
description: Manage law practice with Clio's legal practice management platform.
category: legal
---
# Clio Skill

Manage law practice with Clio's legal practice management platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/clio/install.sh | bash
```

Or manually:
```bash
cp -r skills/clio ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CLIO_CLIENT_ID "your_client_id"
canifi-env set CLIO_CLIENT_SECRET "your_client_secret"
canifi-env set CLIO_ACCESS_TOKEN "your_access_token"
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

1. **Matter Management**: Track cases and legal matters
2. **Time Tracking**: Log billable time and activities
3. **Billing**: Generate invoices and collect payments
4. **Document Management**: Store and organize case documents
5. **Client Portal**: Communicate with clients securely

## Usage Examples

### Create Matter
```
User: "Create a new matter for client Johnson"
Assistant: Creates case with client association
```

### Log Time
```
User: "Log 2 hours for legal research on the Smith case"
Assistant: Creates time entry
```

### Generate Invoice
```
User: "Create an invoice for the pending time entries"
Assistant: Generates invoice from unbilled time
```

### Search Documents
```
User: "Find all documents for the patent case"
Assistant: Returns matching case documents
```

## Authentication Flow

1. Register app in Clio developer portal
2. Implement OAuth 2.0 flow
3. Get access token for API calls
4. Refresh tokens as needed

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Token expired | Refresh access token |
| 403 Forbidden | No access | Check permissions |
| 404 Not Found | Matter not found | Verify matter ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Leading legal practice management
- Time tracking and billing
- Clio Grow for intake
- Integration marketplace
- Mobile apps available
- Cloud-based platform
