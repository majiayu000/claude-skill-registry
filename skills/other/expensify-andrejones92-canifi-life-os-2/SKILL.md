---
name: expensify
description: Expense management and receipt scanning.
category: finance
---
# Expensify Skill

Expense management and receipt scanning.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/expensify/install.sh | bash
```

Or manually:
```bash
cp -r skills/expensify ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set EXPENSIFY_PARTNER_ID "your_partner_id"
canifi-env set EXPENSIFY_PARTNER_SECRET "your_secret"
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

1. **Scan Receipts**: SmartScan receipt capture
2. **Create Reports**: Build expense reports
3. **Submit Expenses**: Send for approval
4. **Track Mileage**: Log travel expenses
5. **Corporate Cards**: Manage company cards

## Usage Examples

### Scan Receipt
```
User: "Scan this receipt"
Assistant: Processes with SmartScan
```

### Create Report
```
User: "Create expense report for last trip"
Assistant: Generates report
```

### Submit Report
```
User: "Submit my expense report"
Assistant: Sends for approval
```

### Log Mileage
```
User: "Log 50 miles for client visit"
Assistant: Creates mileage entry
```

## Authentication Flow

1. Partner credentials
2. API integration
3. SSO support
4. Bank connections

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid credentials | Check partner info |
| Scan Failed | Image quality | Retake photo |
| Report Error | Missing data | Complete fields |
| Approval Failed | Policy violation | Review expense |

## Notes

- SmartScan AI
- Policy enforcement
- Multi-currency
- Corporate cards
- Accounting integrations
- Mobile receipt capture
