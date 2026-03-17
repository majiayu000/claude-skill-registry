---
name: brex
description: Business financial platform with cards, banking, and spend management.
category: finance
---
# Brex Skill

Business financial platform with cards, banking, and spend management.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/brex/install.sh | bash
```

Or manually:
```bash
cp -r skills/brex ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BREX_API_KEY "your_api_key"
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

1. **View Accounts**: Check balances and activity
2. **Manage Cards**: Issue and control cards
3. **Transfers**: Move money between accounts
4. **Expense Management**: Track and categorize
5. **Budget Tracking**: Monitor department spend

## Usage Examples

### Check Balance
```
User: "What's my Brex balance?"
Assistant: Returns account balances
```

### Issue Card
```
User: "Create a virtual card for this vendor"
Assistant: Issues virtual card
```

### View Transactions
```
User: "Show recent transactions"
Assistant: Returns transaction list
```

### Make Transfer
```
User: "Transfer $5000 to vendor"
Assistant: Initiates transfer
```

## Authentication Flow

1. API key authentication
2. OAuth2 for some features
3. Webhook support
4. Bank-level security

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Insufficient Funds | Low balance | Add funds |
| Card Declined | Policy | Review limits |
| Transfer Failed | Verification | Complete KYC |

## Notes

- Startup-focused
- Instant virtual cards
- High limits
- Accounting sync
- Bill pay
- Treasury
