---
name: revolut
description: View multi-currency accounts, check crypto holdings, and monitor spending on Revolut
category: finance
---

# Revolut Skill

## Overview
Enables Claude to access Revolut to view multi-currency account balances, check cryptocurrency holdings, monitor spending analytics, and review subscription benefits.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/revolut/install.sh | bash
```

Or manually:
```bash
cp -r skills/revolut ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set REVOLUT_EMAIL "your-email@example.com"
canifi-env set REVOLUT_PHONE "+1234567890"
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
- View balances in 30+ currencies
- Check cryptocurrency holdings
- Monitor spending analytics by category
- View Revolut card transactions
- Check subscription tier benefits
- Track savings Vaults

## Usage Examples

### Example 1: Check Accounts
```
User: "What's in my Revolut?"
Claude: I'll check your Revolut balances.
- Opens app.revolut.com via Playwright MCP
- Logs into account
- Returns account summary:
  - Main: €2,345.67 EUR
  - USD pocket: $1,234.56
  - GBP pocket: £567.89
- Crypto: 0.025 BTC ($1,050.75)
- Savings Vaults: €500
- Total (EUR): €5,234.56
```

### Example 2: View Spending Analytics
```
User: "How did I spend money last month?"
Claude: I'll show your spending breakdown.
- Navigates to analytics
- Last month spending: €2,456.78
- Categories:
  - Restaurants: €456 (19%)
  - Groceries: €389 (16%)
  - Transport: €234 (10%)
  - Shopping: €567 (23%)
  - Entertainment: €123 (5%)
- Compared to previous: +8%
```

### Example 3: Check Crypto
```
User: "How's my Revolut crypto?"
Claude: I'll check your crypto holdings.
- Navigates to crypto section
- Holdings:
  - Bitcoin: 0.025 BTC ($1,050.75)
  - Ethereum: 0.5 ETH ($825.50)
  - Solana: 10 SOL ($652.30)
- Total crypto: $2,528.55
- 24h change: +$45.67 (+1.8%)
```

## Authentication Flow
1. Navigate to app.revolut.com via Playwright MCP
2. Enter phone number
3. Receive push notification or SMS code
4. Complete verification
5. May require biometric on mobile
6. Maintain session for account access

## Error Handling
- Login Failed: Retry with app push notification
- 2FA Required: Complete push or SMS verification
- Account Frozen: Direct to support
- Session Expired: Re-authenticate (short sessions)
- Rate Limited: Wait 60 seconds, retry
- Feature Unavailable: Check subscription tier

## Self-Improvement Instructions
After each interaction:
- Track currency holding patterns
- Note spending category trends
- Log crypto monitoring frequency
- Document UI changes

Suggest updates when:
- Revolut updates interface
- New features added
- Subscription tiers change
- Crypto offerings expand

## Notes
- Claude CANNOT make transactions
- All access is read-only for security
- Revolut is primarily mobile-first
- Metal/Premium for additional benefits
- Crypto trading 24/7
- Disposable virtual cards available
- Travel insurance included with Premium+
