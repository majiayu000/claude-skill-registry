---
name: plaid
description: View connected accounts, check connection status, and manage financial data links via Plaid
category: finance
---

# Plaid Skill

## Overview
Enables Claude to access Plaid dashboard to view connected financial accounts, check connection health, monitor data sync status, and manage institutional links used by various financial apps.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/plaid/install.sh | bash
```

Or manually:
```bash
cp -r skills/plaid ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set PLAID_EMAIL "your-email@example.com"
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
- View connected financial institutions
- Check connection health and status
- Monitor which apps have data access
- Review account permissions
- Identify disconnected accounts
- Check data freshness timestamps

## Usage Examples

### Example 1: View Connected Accounts
```
User: "What accounts do I have connected through Plaid?"
Claude: I'll check your Plaid connections.
- Opens my.plaid.com via Playwright MCP
- Logs into Plaid portal
- Returns connected institutions:
  - Chase Bank: 3 accounts, healthy
  - Bank of America: 2 accounts, healthy
  - Capital One: 1 account, needs reauth
  - Fidelity: 1 account, healthy
- Total: 7 accounts across 4 institutions
```

### Example 2: Check Apps Using Data
```
User: "Which apps have access to my bank data?"
Claude: I'll review your Plaid app connections.
- Navigates to connected apps
- Apps with access:
  - Mint: All accounts, full history
  - YNAB: Chase checking only
  - Robinhood: Verification only
  - Acorns: Bank of America only
- Last data pull: Most within 24 hours
```

### Example 3: Fix Broken Connection
```
User: "Why isn't my Capital One syncing?"
Claude: I'll check the Capital One connection.
- Checks Capital One status
- Issue: Credential update required
- Reason: Bank security update
- Solution: Re-authenticate through the app using this data
- Affected apps: Mint, YNAB
- Suggests: Update credentials in Mint to fix
```

## Authentication Flow
1. Navigate to my.plaid.com via Playwright MCP
2. Enter email address
3. Enter password
4. Handle 2FA via email or SMS
5. View connected accounts dashboard
6. Maintain session for management

## Error Handling
- Login Failed: Retry, check Plaid account exists
- 2FA Required: Complete email verification
- No Accounts: User may not have used Plaid directly
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 60 seconds, retry
- Institution Down: Note temporary outage

## Self-Improvement Instructions
After each interaction:
- Track connection health patterns
- Note common disconnection reasons
- Log institution reliability
- Document portal updates

Suggest updates when:
- Plaid portal updates
- New features added
- Auth flows change
- Institution coverage changes

## Notes
- Plaid connects apps to bank accounts
- Users often don't know they use Plaid
- my.plaid.com is consumer portal
- Can revoke app access from portal
- Connection issues often require re-auth
- Some banks have better Plaid support
- Data includes transactions, balances
