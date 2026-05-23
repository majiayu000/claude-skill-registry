---
name: deel
description: Manage global hiring and payroll with Deel's international workforce platform.
category: hr
---
# Deel Skill

Manage global hiring and payroll with Deel's international workforce platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/deel/install.sh | bash
```

Or manually:
```bash
cp -r skills/deel ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DEEL_API_KEY "your_api_key"
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

1. **Global Hiring**: Hire employees and contractors worldwide
2. **Payroll Management**: Run payroll across multiple countries
3. **Compliance**: Ensure local labor law compliance
4. **Contract Management**: Create and manage work contracts
5. **Payments**: Process international payments and invoices

## Usage Examples

### Add Contractor
```
User: "Set up a new contractor in Germany"
Assistant: Creates contractor with compliant contract
```

### Run Payroll
```
User: "Process international payroll for November"
Assistant: Calculates and schedules payments
```

### Generate Contract
```
User: "Create an employment contract for the UK hire"
Assistant: Generates compliant employment contract
```

### View Payments
```
User: "Show me pending international payments"
Assistant: Returns payment queue
```

## Authentication Flow

1. Generate API key in Deel dashboard
2. Use API key for authentication
3. Bearer token in header
4. Organization-scoped access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 403 Forbidden | No access | Check permissions |
| 404 Not Found | Resource not found | Verify ID |
| 422 Validation Error | Invalid data | Fix request data |

## Notes

- Global payroll in 150+ countries
- EOR services included
- Contractor management
- Automated compliance
- Multiple payment options
- Fast international payments
