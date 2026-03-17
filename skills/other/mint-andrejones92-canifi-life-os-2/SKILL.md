---
name: mint
description: Track spending, manage budgets, monitor credit score, and view financial overview with Mint
category: finance
---

# Mint Skill

## Overview
Enables Claude to access Mint's financial dashboard to view spending patterns, track budgets, monitor bills, check credit score, and get a comprehensive view of personal finances across linked accounts.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/mint/install.sh | bash
```

Or manually:
```bash
cp -r skills/mint ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MINT_EMAIL "your-email@example.com"
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
- View spending by category and trends
- Track budget progress and alerts
- Monitor upcoming bills and payments
- Check credit score and factors
- See net worth across all accounts
- Identify unusual spending patterns

## Usage Examples

### Example 1: Check Spending Summary
```
User: "How much did I spend on food this month?"
Claude: I'll check your Mint spending.
- Opens mint.intuit.com via Playwright MCP
- Navigates to spending categories
- Returns: Food & Dining: $847 this month
  - Restaurants: $523
  - Groceries: $298
  - Coffee Shops: $26
- Compared to last month: +12%
- Budget status: $847 of $800 (over by $47)
```

### Example 2: Check Budget Status
```
User: "How am I doing on my budgets?"
Claude: I'll review your budget progress.
- Navigates to budgets section
- Shows budget status:
  - Groceries: $298/$400 (75%, on track)
  - Entertainment: $156/$150 (104%, over)
  - Shopping: $412/$300 (137%, over budget)
  - Transportation: $89/$200 (45%, good)
- Alerts: Shopping budget exceeded by $112
```

### Example 3: Check Credit Score
```
User: "What's my credit score on Mint?"
Claude: I'll check your credit dashboard.
- Navigates to credit score section
- Returns: 742 (Good)
- Change: +5 points from last month
- Factors:
  - Payment history: Excellent
  - Credit utilization: 23% (Good)
  - Account age: 7.5 years (Excellent)
- Next update: January 15
```

## Authentication Flow
1. Navigate to mint.intuit.com via Playwright MCP
2. Sign in with Intuit account (shared with TurboTax)
3. Enter email and password
4. Handle 2FA via SMS or authenticator
5. Wait for accounts to sync
6. Maintain session for dashboard access

## Error Handling
- Login Failed: Retry with Intuit account recovery
- Account Sync Error: Trigger manual refresh
- Data Stale: Note last sync time, offer refresh
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 2 minutes, retry
- 2FA Required: Retrieve code via iMessage

## Self-Improvement Instructions
After each interaction:
- Track spending pattern insights
- Note budget accuracy over time
- Log credit score factors
- Document UI changes

Suggest updates when:
- Mint updates dashboard
- New features added
- Intuit authentication changes
- Budget categories change

## Notes
- Mint is free, part of Intuit (TurboTax)
- Accounts sync automatically daily
- Credit score is VantageScore, may differ from FICO
- Can't make transactions, read-only view
- Bill tracking may miss some recurring charges
- Mint data useful for LifeOS finance integration
