---
name: robinhood
description: View portfolio, check stock prices, research investments, and monitor positions on Robinhood
category: finance
---

# Robinhood Skill

## Overview
Enables Claude to access Robinhood to view portfolio performance, check stock and crypto prices, research investments, and monitor positions. Note: Claude cannot execute trades or transfer funds.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/robinhood/install.sh | bash
```

Or manually:
```bash
cp -r skills/robinhood ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ROBINHOOD_EMAIL "your-email@example.com"
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
- View portfolio value and performance
- Check individual stock and crypto prices
- Research company fundamentals
- View watchlists and price alerts
- Check dividend history and upcoming payments
- Monitor options positions and values

## Usage Examples

### Example 1: Check Portfolio
```
User: "How's my Robinhood portfolio doing?"
Claude: I'll check your Robinhood portfolio.
- Opens robinhood.com via Playwright MCP
- Navigates to portfolio view
- Returns: Total value: $24,567.89
- Today's change: +$312.45 (+1.29%)
- Top gainers: AAPL +3.2%, NVDA +2.8%
- Top losers: TSLA -1.5%
- All-time return: +$4,234 (+20.8%)
```

### Example 2: Check Stock Price
```
User: "What's the price of Apple stock?"
Claude: I'll look up AAPL on Robinhood.
- Searches for AAPL
- Returns: Apple Inc (AAPL)
- Current price: $178.45
- Today's change: +$5.67 (+3.28%)
- 52-week range: $142.00 - $199.62
- Market cap: $2.81T
- P/E ratio: 28.5
```

### Example 3: View Dividend Schedule
```
User: "When are my next dividends?"
Claude: I'll check your dividend calendar.
- Navigates to dividends section
- Upcoming dividends:
  - AAPL: $0.24/share on Feb 15 (12 shares = $2.88)
  - VTI: $0.85/share on March 20 (45 shares = $38.25)
  - KO: $0.46/share on April 1 (20 shares = $9.20)
- Total expected next 90 days: $50.33
```

## Authentication Flow
1. Navigate to robinhood.com via Playwright MCP
2. Click "Log In" and enter email
3. Enter password
4. Handle 2FA via SMS or authenticator (required)
5. May require device verification
6. Maintain session for read-only access

## Error Handling
- Login Failed: Retry, may need device approval
- 2FA Required: Must complete - no bypass
- Account Locked: Direct user to Robinhood support
- Session Expired: Re-authenticate (frequent for security)
- Rate Limited: Wait 2 minutes, retry
- Market Closed: Show after-hours pricing

## Self-Improvement Instructions
After each interaction:
- Track common portfolio queries
- Note price alert patterns
- Log dividend tracking accuracy
- Document UI changes

Suggest updates when:
- Robinhood updates interface
- New investment types added
- Feature limitations change
- Auth requirements update

## Notes
- Claude CANNOT execute trades or transfers
- All access is read-only for security
- Robinhood has strict security requirements
- Options data may be delayed
- Crypto trades 24/7 but stocks have market hours
- Fractional shares may show odd quantities
- Tax documents available in February
