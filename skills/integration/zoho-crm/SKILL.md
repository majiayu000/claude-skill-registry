---
name: zoho-crm
description: Manage customer relationships with Zoho's comprehensive CRM platform.
category: business
---
# Zoho CRM Skill

Manage customer relationships with Zoho's comprehensive CRM platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/zoho-crm/install.sh | bash
```

Or manually:
```bash
cp -r skills/zoho-crm ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ZOHO_CLIENT_ID "your_client_id"
canifi-env set ZOHO_CLIENT_SECRET "your_client_secret"
canifi-env set ZOHO_REFRESH_TOKEN "your_refresh_token"
canifi-env set ZOHO_DOMAIN "com|eu|in|com.au"
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

1. **Lead & Contact Management**: Create and manage leads, contacts, and accounts
2. **Deal Tracking**: Track deals through customizable sales stages
3. **Workflow Automation**: Set up automated workflows and triggers
4. **Analytics & Reports**: Generate custom reports and dashboards
5. **Multi-channel Communication**: Manage email, phone, and social interactions

## Usage Examples

### Create Lead
```
User: "Add a new lead in Zoho CRM for Mike Johnson from StartupXYZ"
Assistant: Creates lead with provided details
```

### Update Deal
```
User: "Update the Enterprise contract value to $25000 in Zoho"
Assistant: Updates deal amount
```

### Search Records
```
User: "Find all contacts from the technology sector in Zoho"
Assistant: Searches and returns matching contacts
```

### Get Report
```
User: "Show me the monthly sales report from Zoho CRM"
Assistant: Retrieves sales report data
```

## Authentication Flow

1. Register app in Zoho API Console
2. Implement OAuth 2.0 with authorization code
3. Get refresh token for persistent access
4. Use appropriate Zoho domain (US, EU, India, Australia)

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| INVALID_TOKEN | Token expired | Use refresh token |
| INVALID_DATA | Malformed request | Validate request format |
| LIMIT_EXCEEDED | API limit reached | Wait or upgrade plan |
| NO_PERMISSION | Insufficient access | Check user permissions |

## Notes

- Free tier for up to 3 users
- Part of Zoho One suite
- Multiple data centers worldwide
- Extensive customization options
- Native integrations with Zoho apps
- API limits vary by edition
