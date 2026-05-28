---
name: gusto
description: Manage payroll and HR for small businesses with Gusto's platform.
category: hr
---
# Gusto Skill

Manage payroll and HR for small businesses with Gusto's platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/gusto/install.sh | bash
```

Or manually:
```bash
cp -r skills/gusto ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GUSTO_CLIENT_ID "your_client_id"
canifi-env set GUSTO_CLIENT_SECRET "your_client_secret"
canifi-env set GUSTO_ACCESS_TOKEN "your_access_token"
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

1. **Payroll Processing**: Run payroll and manage payments
2. **Employee Onboarding**: Paperless onboarding for new hires
3. **Benefits Administration**: Manage health insurance and 401k
4. **Time Tracking**: Track hours and sync to payroll
5. **Tax Filing**: Automated tax calculations and filing

## Usage Examples

### Run Payroll
```
User: "Process payroll for this pay period"
Assistant: Calculates and submits payroll
```

### Add Employee
```
User: "Onboard a new employee starting next week"
Assistant: Creates employee and sends onboarding
```

### View Benefits
```
User: "Show me current benefits enrollments"
Assistant: Returns benefits summary
```

### Check Time
```
User: "Show time entries for the marketing team"
Assistant: Returns time tracking data
```

## Authentication Flow

1. Register app in Gusto Developer Portal
2. Implement OAuth 2.0 flow
3. Get access token for API calls
4. Refresh tokens as needed

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Token expired | Refresh access token |
| 403 Forbidden | No company access | Check permissions |
| 404 Not Found | Resource not found | Verify ID |
| 422 Unprocessable | Invalid data | Fix request |

## Notes

- Full-service payroll
- Benefits brokerage included
- Tax filing automated
- State-specific compliance
- Modern interface
- Per-person pricing
