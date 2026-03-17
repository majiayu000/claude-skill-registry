---
name: harvest
description: Time tracking and invoicing for teams.
category: hr
---
# Harvest Skill

Time tracking and invoicing for teams.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/harvest/install.sh | bash
```

Or manually:
```bash
cp -r skills/harvest ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HARVEST_ACCESS_TOKEN "your_token"
canifi-env set HARVEST_ACCOUNT_ID "your_account_id"
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

1. **Track Time**: Log hours to projects
2. **Invoicing**: Generate and send invoices
3. **Expenses**: Track project expenses
4. **Reports**: View time and budget reports
5. **Team Management**: Monitor team hours

## Usage Examples

### Log Time
```
User: "Log 3 hours to client project"
Assistant: Creates time entry
```

### Create Invoice
```
User: "Generate invoice for October"
Assistant: Creates invoice from time
```

### Track Expense
```
User: "Add $50 expense for software"
Assistant: Logs expense
```

### View Report
```
User: "Show project budget status"
Assistant: Returns budget report
```

## Authentication Flow

1. OAuth2 authentication
2. Personal access tokens
3. Account ID required
4. Webhook support

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid token | Re-authorize |
| Project Not Found | Wrong ID | Verify project |
| Invoice Error | Missing data | Complete info |
| Rate Limited | Too many requests | Slow down |

## Notes

- Time + invoicing
- QuickBooks integration
- Budget tracking
- Team management
- Full API
- Mobile apps
