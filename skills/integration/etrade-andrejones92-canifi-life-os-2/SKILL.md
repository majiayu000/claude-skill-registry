---
name: etrade
description: View investment accounts, check portfolio, monitor positions, and research investments on E*TRADE
category: finance
---

# E*TRADE Skill

## Overview
Enables Claude to access E*TRADE (now part of Morgan Stanley) to view investment accounts, check portfolio performance, monitor positions, and research investments. Note: Claude cannot execute trades.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/etrade/install.sh | bash
```

Or manually:
```bash
cp -r skills/etrade ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ETRADE_USERNAME "your-username"
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
- View all E*TRADE accounts and balances
- Check portfolio performance and positions
- Monitor retirement and brokerage accounts
- Research stocks, options, and ETFs
- View trade history and confirmations
- Check Power E*TRADE platform features

## Usage Examples

### Example 1: Check Portfolio
```
User: "What's my E*TRADE portfolio worth?"
Claude: I'll check your E*TRADE accounts.
- Opens etrade.com via Playwright MCP
- Logs into account
- Returns: Total Value: $234,567.89
  - Individual Brokerage: $156,789.01
  - Roth IRA: $45,678.90
  - Traditional IRA: $32,099.98
- Today: +$1,567.89 (+0.67%)
- YTD: +14.5%
```

### Example 2: View Watchlist
```
User: "Show my E*TRADE watchlist"
Claude: I'll display your watchlist.
- Navigates to watchlist
- Watched stocks:
  - TSLA: $248.50 (+2.3% today)
  - AMD: $145.67 (-0.8% today)
  - META: $356.78 (+1.2% today)
  - GOOGL: $142.34 (+0.5% today)
- Alerts: TSLA crossed $250 target
```

### Example 3: Check Options
```
User: "What options positions do I have?"
Claude: I'll check your options holdings.
- Navigates to options positions
- Current options:
  - AAPL Jan 190 Call: 2 contracts, +$450
  - SPY Feb 480 Put: 5 contracts, -$230
- Total options value: $1,890
- Greeks and risk metrics available
```

## Authentication Flow
1. Navigate to etrade.com via Playwright MCP
2. Enter user ID
3. Enter password
4. Handle security verification (RSA token, SMS)
5. May require security questions
6. Maintain session for account access

## Error Handling
- Login Failed: Retry, check Morgan Stanley migration
- 2FA Required: Complete RSA or SMS verification
- Account Locked: Direct to E*TRADE support
- Session Expired: Re-authenticate (security)
- Rate Limited: Wait 2 minutes, retry
- Platform Switch: Note Power E*TRADE vs standard

## Self-Improvement Instructions
After each interaction:
- Track portfolio check patterns
- Note options research interest
- Log watchlist management
- Document Morgan Stanley integration changes

Suggest updates when:
- E*TRADE updates interface
- Morgan Stanley integration changes
- New features added
- Auth requirements update

## Notes
- Claude CANNOT execute trades
- All access is read-only for security
- E*TRADE now owned by Morgan Stanley
- Power E*TRADE for active traders
- Options research and analytics available
- Stock plan management for employees
- Core Portfolios for robo-investing
