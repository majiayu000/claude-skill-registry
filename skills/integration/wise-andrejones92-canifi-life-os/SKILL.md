---
name: wise
description: View multi-currency balances, check exchange rates, and monitor international transfers on Wise
category: finance
---

# Wise Skill

## Overview
Enables Claude to access Wise (formerly TransferWise) to view multi-currency account balances, check real-time exchange rates, monitor transfer status, and track international payment activity.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/wise/install.sh | bash
```

Or manually:
```bash
cp -r skills/wise ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WISE_EMAIL "your-email@example.com"
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
- View balances in multiple currencies
- Check live exchange rates
- Monitor ongoing transfers
- View transaction history
- Check Wise card spending
- Track recurring transfers

## Usage Examples

### Example 1: Check Balances
```
User: "What's in my Wise account?"
Claude: I'll check your Wise balances.
- Opens wise.com via Playwright MCP
- Logs into account
- Returns multi-currency balances:
  - USD: $2,345.67
  - EUR: €1,234.56
  - GBP: £567.89
  - CAD: $890.12
- Total (USD equivalent): $5,234.56
- Wise card: Active
```

### Example 2: Check Exchange Rate
```
User: "What's the USD to EUR rate on Wise?"
Claude: I'll check the current rate.
- Navigates to convert section
- USD to EUR rate: 0.9234
- $1,000 USD = €923.40 EUR
- Wise fee: $4.50 (0.45%)
- Total cost: $1,004.50 for €923.40
- Rate valid for: 24 hours
- Mid-market rate comparison: 0.9234 (matches)
```

### Example 3: Track Transfer
```
User: "Where's my transfer to the UK?"
Claude: I'll check your transfer status.
- Navigates to activity section
- Transfer to UK (£500):
  - Status: Arriving today
  - Sent: Jan 5, 2:30pm
  - Expected: Jan 6 by end of day
  - Rate locked: 0.7890
  - Fee paid: $4.25
- Recipient: John Smith (****4567)
```

## Authentication Flow
1. Navigate to wise.com via Playwright MCP
2. Enter email address
3. Enter password
4. Handle 2FA via SMS or authenticator
5. Verify balances displayed
6. Maintain session for account access

## Error Handling
- Login Failed: Retry, check for verification email
- 2FA Required: Complete verification flow
- Account Frozen: Direct to support (KYC issues)
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 60 seconds, retry
- Transfer Issue: Show support contact

## Self-Improvement Instructions
After each interaction:
- Track exchange rate queries
- Note common currency pairs
- Log transfer monitoring patterns
- Document UI changes

Suggest updates when:
- Wise updates interface
- New currencies added
- Fee structure changes
- Features expanded

## Notes
- Claude CANNOT send money or transfers
- All access is read-only for security
- Wise uses mid-market exchange rate
- Transparent fee structure
- Multi-currency card for spending abroad
- Local bank details in 10+ currencies
- Business accounts also available
