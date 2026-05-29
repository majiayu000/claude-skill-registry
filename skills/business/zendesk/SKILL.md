---
name: zendesk
description: Manage customer support with Zendesk's comprehensive help desk platform.
category: business
---
# Zendesk Skill

Manage customer support with Zendesk's comprehensive help desk platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/zendesk/install.sh | bash
```

Or manually:
```bash
cp -r skills/zendesk ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ZENDESK_SUBDOMAIN "your_subdomain"
canifi-env set ZENDESK_EMAIL "your_email"
canifi-env set ZENDESK_API_TOKEN "your_api_token"
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

1. **Ticket Management**: Create, update, and resolve support tickets
2. **Customer Profiles**: Manage customer information and interaction history
3. **Knowledge Base**: Search and create help center articles
4. **Macros & Automation**: Apply macros and automated responses
5. **Reporting & Analytics**: Access support metrics and agent performance

## Usage Examples

### Create Ticket
```
User: "Create a support ticket for billing inquiry from john@customer.com"
Assistant: Creates ticket with customer and category
```

### Update Status
```
User: "Mark ticket #12345 as solved"
Assistant: Updates ticket status to solved
```

### Search Tickets
```
User: "Find all open tickets from TechCorp"
Assistant: Returns open tickets for organization
```

### Apply Macro
```
User: "Apply the 'password reset' macro to this ticket"
Assistant: Applies macro with response template
```

## Authentication Flow

1. Enable API access in Zendesk Admin
2. Create API token in admin settings
3. Use email/token authentication
4. OAuth available for apps

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid credentials | Verify email and token |
| 403 Forbidden | Insufficient permissions | Check agent role |
| 404 Not Found | Ticket not found | Verify ticket ID |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- Industry-leading help desk platform
- Suite includes Support, Chat, Talk, Guide
- Extensive marketplace for apps
- Multi-brand support available
- Omnichannel routing in Suite plans
- AI-powered answer bot available
