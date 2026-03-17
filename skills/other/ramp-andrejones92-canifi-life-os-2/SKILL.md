---
name: ramp
description: Corporate cards and spend management platform.
category: finance
---
# Ramp Skill

Corporate cards and spend management platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/ramp/install.sh | bash
```

Or manually:
```bash
cp -r skills/ramp ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set RAMP_API_KEY "your_api_key"
canifi-env set RAMP_CLIENT_ID "your_client_id"
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

1. **View Transactions**: See card activity
2. **Manage Cards**: Issue and control cards
3. **Expense Reports**: Auto-generate reports
4. **Budget Control**: Set spending limits
5. **Receipt Matching**: Auto-match receipts

## Usage Examples

### View Spending
```
User: "Show this month's spending"
Assistant: Returns transaction summary
```

### Issue Card
```
User: "Issue a virtual card for subscriptions"
Assistant: Creates virtual card
```

### Check Budget
```
User: "How much budget is left for marketing?"
Assistant: Returns budget status
```

### Match Receipt
```
User: "Match this receipt to my last transaction"
Assistant: Links receipt to expense
```

## Authentication Flow

1. API key authentication
2. OAuth2 available
3. Webhook support
4. Bank-level security

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Card Declined | Limit exceeded | Adjust budget |
| Not Found | Wrong ID | Verify resource |
| Permission Denied | Role restriction | Contact admin |

## Notes

- 1.5% cashback
- Real-time controls
- Accounting integrations
- Price intelligence
- Virtual cards
- Automated receipts
