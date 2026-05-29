---
name: schwab
description: View investment accounts, check portfolio, monitor positions, and research investments on Charles Schwab
category: finance
---

# Charles Schwab Skill

## Overview
Enables Claude to access Charles Schwab to view investment accounts, check portfolio performance, monitor positions, and research stocks and funds. Note: Claude cannot execute trades.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/schwab/install.sh | bash
```

Or manually:
```bash
cp -r skills/schwab ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SCHWAB_USERNAME "your-username"
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
- View all Schwab accounts and balances
- Check portfolio performance and positions
- Monitor checking and brokerage accounts
- Research stocks, ETFs, and mutual funds
- View order history and trade confirmations
- Check margin and buying power

## Usage Examples

### Example 1: Check Accounts
```
User: "What's in my Schwab accounts?"
Claude: I'll check your Schwab accounts.
- Opens schwab.com via Playwright MCP
- Logs into account
- Returns account summary:
  - Brokerage: $345,678.90
  - Roth IRA: $123,456.78
  - Schwab Checking: $12,345.67
  - Schwab One: $5,678.90
- Total: $487,160.25
- Today: +$2,890.45 (+0.60%)
```

### Example 2: View Positions
```
User: "Show my stock positions"
Claude: I'll display your holdings.
- Navigates to positions view
- Current positions:
  - AAPL: 100 shares, $17,845 (+15.2%)
  - MSFT: 50 shares, $18,956 (+22.4%)
  - SCHD: 200 shares, $14,890 (+8.7%)
  - SWTSX: $180,000 (index fund)
- Cash available: $45,678
- Margin available: $150,000
```

### Example 3: Research Stock
```
User: "Look up Nvidia on Schwab"
Claude: I'll research NVDA for you.
- Searches for NVDA
- NVIDIA Corporation
- Current price: $485.67
- 52-week range: $180 - $505
- Market cap: $1.2T
- P/E ratio: 65.4
- Schwab rating: A (Outperform)
- Analyst consensus: Strong Buy
```

## Authentication Flow
1. Navigate to schwab.com via Playwright MCP
2. Enter login ID
3. Enter password
4. Handle security verification (Symantec VIP, SMS)
5. May require security questions
6. Maintain session for account access

## Error Handling
- Login Failed: Retry, check for TD migration issues
- 2FA Required: Complete VIP Access or SMS
- Account Locked: Direct to Schwab support
- Session Expired: Re-authenticate (security)
- Rate Limited: Wait 2 minutes, retry
- TD Migration: May redirect to new platform

## Self-Improvement Instructions
After each interaction:
- Track account check patterns
- Note research preferences
- Log position tracking accuracy
- Document TD Ameritrade merger changes

Suggest updates when:
- Schwab updates interface
- TD Ameritrade integration changes
- New features added
- Auth requirements update

## Notes
- Claude CANNOT execute trades
- All access is read-only for security
- Schwab acquired TD Ameritrade
- Schwab Intelligent Portfolios for robo-advice
- Free stock trades
- Checking account has ATM rebates
- StreetSmart Edge for advanced trading (research only)
