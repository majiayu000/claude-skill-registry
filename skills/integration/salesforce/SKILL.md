---
name: salesforce
description: Manage enterprise CRM with Salesforce's comprehensive sales and customer platform.
category: business
---
# Salesforce Skill

Manage enterprise CRM with Salesforce's comprehensive sales and customer platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/salesforce/install.sh | bash
```

Or manually:
```bash
cp -r skills/salesforce ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SALESFORCE_CLIENT_ID "your_client_id"
canifi-env set SALESFORCE_CLIENT_SECRET "your_client_secret"
canifi-env set SALESFORCE_USERNAME "your_username"
canifi-env set SALESFORCE_PASSWORD "your_password"
canifi-env set SALESFORCE_SECURITY_TOKEN "your_security_token"
canifi-env set SALESFORCE_INSTANCE_URL "your_instance_url"
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

1. **Lead Management**: Create, qualify, and convert leads through the sales process
2. **Opportunity Tracking**: Manage opportunities with stages, forecasting, and analytics
3. **Account Management**: Track company accounts with full relationship history
4. **Case Management**: Handle customer support cases and service requests
5. **Report Generation**: Generate and access sales reports and dashboards

## Usage Examples

### Create Lead
```
User: "Create a new lead in Salesforce for Jane Doe at TechStartup"
Assistant: Creates lead with provided information
```

### Update Opportunity
```
User: "Update the Enterprise deal probability to 80% in Salesforce"
Assistant: Updates opportunity probability
```

### Search Accounts
```
User: "Find all Salesforce accounts in the healthcare industry"
Assistant: Queries and returns matching accounts
```

### Create Report
```
User: "Show me this quarter's closed deals from Salesforce"
Assistant: Retrieves closed opportunities for current quarter
```

## Authentication Flow

1. Create Connected App in Salesforce Setup
2. Enable OAuth settings and set callback URL
3. Implement OAuth 2.0 authorization flow
4. Use refresh token for persistent access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| INVALID_SESSION_ID | Session expired | Re-authenticate with refresh token |
| INSUFFICIENT_ACCESS | Missing permissions | Check profile permissions |
| QUERY_TOO_COMPLICATED | SOQL too complex | Simplify query |
| API_LIMIT_EXCEEDED | Daily limit reached | Wait for reset or upgrade |

## Notes

- Enterprise-grade CRM platform
- API limits vary by edition (Professional, Enterprise, Unlimited)
- Apex for custom logic and triggers
- Lightning for modern UI components
- AppExchange for third-party integrations
- Extensive customization capabilities
