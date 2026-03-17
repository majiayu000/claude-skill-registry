---
name: betterment
description: View automated portfolio, track goals, monitor cash reserve, and check tax coordination on Betterment
category: finance
---

# Betterment Skill

## Overview
Enables Claude to access Betterment to view robo-advisor managed portfolios, track goal-based investing progress, check cash reserve balances, and review tax-smart features.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/betterment/install.sh | bash
```

Or manually:
```bash
cp -r skills/betterment ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BETTERMENT_EMAIL "your-email@example.com"
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
- View investment account balances and allocation
- Check Cash Reserve balance and interest
- Track individual goal progress
- Monitor tax-loss harvesting activity
- Review portfolio allocation and drift
- Check dividend reinvestment status

## Usage Examples

### Example 1: Check Goals
```
User: "How are my Betterment goals doing?"
Claude: I'll check your Betterment goals.
- Opens betterment.com via Playwright MCP
- Logs into account
- Returns goal summary:
  - Retirement: $156,789 (85% funded)
  - Safety Net: $25,000 (100%, complete)
  - Vacation Fund: $4,567 (45%)
  - General Investing: $34,567
- Total invested: $220,923
- Cash Reserve: $15,000 (4.50% APY)
```

### Example 2: View Allocation
```
User: "What's my portfolio allocation?"
Claude: I'll show your portfolio breakdown.
- Navigates to portfolio details
- Retirement goal allocation (90% stocks):
  - US Stocks: 38%
  - Developed Markets: 25%
  - Emerging Markets: 12%
  - US Bonds: 15%
  - International Bonds: 10%
- Tax-coordinated: Yes
- Last rebalance: 3 days ago
```

### Example 3: Check Tax Features
```
User: "Has Betterment done tax-loss harvesting?"
Claude: I'll review your tax activity.
- Navigates to tax section
- Tax-loss harvesting this year: $2,890
- Estimated tax savings: $723
- Tax-coordinated placement: Active
  - Bonds in IRA (tax-efficient)
  - Stocks in taxable (for LTCG rates)
- Charitable giving pending: None
```

## Authentication Flow
1. Navigate to betterment.com via Playwright MCP
2. Enter email address
3. Enter password
4. Handle 2FA via SMS or authenticator
5. Verify goal dashboard loads
6. Maintain session for account access

## Error Handling
- Login Failed: Retry, check credentials
- 2FA Required: Complete verification flow
- Account Restricted: Direct to support
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 2 minutes, retry
- Goal Sync: Wait for allocation updates

## Self-Improvement Instructions
After each interaction:
- Track goal progress queries
- Note tax feature usage
- Log allocation preferences
- Document UI changes

Suggest updates when:
- Betterment updates interface
- New goal types added
- Cash Reserve rates change
- Tax features update

## Notes
- Claude CANNOT make deposits or trades
- All access is read-only for security
- Betterment is goal-based robo-advisor
- Cash Reserve is high-yield savings
- Tax-loss harvesting automatic
- Tax-coordinated placement optimizes across accounts
- Flexible portfolio options available
