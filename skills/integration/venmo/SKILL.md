---
name: venmo
description: Check balance, view transaction history, and manage payment requests on Venmo
category: finance
---

# Venmo Skill

## Overview
Enables Claude to access Venmo to check balance, view transaction history, review pending requests, and manage payment settings. Note: Claude cannot send money or make transfers.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/venmo/install.sh | bash
```

Or manually:
```bash
cp -r skills/venmo ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set VENMO_EMAIL "your-email@example.com"
canifi-env set VENMO_PHONE "+1234567890"
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
- Check Venmo balance
- View recent transaction history
- Review incoming payment requests
- Check pending payments status
- View friends and payment history with them
- Monitor Venmo card transactions (if applicable)

## Usage Examples

### Example 1: Check Balance
```
User: "What's my Venmo balance?"
Claude: I'll check your Venmo balance.
- Opens venmo.com via Playwright MCP
- Logs into account
- Returns: Venmo Balance: $247.50
- Venmo Card available funds: $247.50
- Last deposit: $100 on Jan 5
- Pending: None
```

### Example 2: View Recent Transactions
```
User: "Show my recent Venmo transactions"
Claude: I'll pull up your transaction history.
- Navigates to statement
- Recent transactions:
  - Jan 6: +$50 from Sarah (dinner split)
  - Jan 5: -$25 to John (movie tickets)
  - Jan 4: +$100 from Mike (rent share)
  - Jan 3: -$35 to Uber
- This week: +$90 net
```

### Example 3: Check Pending Requests
```
User: "Do I have any pending Venmo requests?"
Claude: I'll check your pending requests.
- Navigates to requests section
- Incoming requests:
  - $45 from Lisa for "brunch" - 2 days ago
  - $20 from Tom for "coffee" - 5 hours ago
- Outgoing requests:
  - $60 to Dave for "concert tickets" - pending 3 days
- Total owed to you: $60
- Total you owe: $65
```

## Authentication Flow
1. Navigate to venmo.com via Playwright MCP
2. Click "Log In" and enter email/phone
3. Enter password
4. Handle 2FA via SMS (required)
5. May need device confirmation email
6. Maintain session for account access

## Error Handling
- Login Failed: Retry with phone number
- 2FA Required: Must complete SMS verification
- Account Frozen: Direct to Venmo support
- Session Expired: Re-authenticate (security)
- Rate Limited: Wait 2 minutes, retry
- Device Not Recognized: Complete email verification

## Self-Improvement Instructions
After each interaction:
- Track balance check patterns
- Note common transaction types
- Log request reminder timing
- Document UI changes

Suggest updates when:
- Venmo updates interface
- New features added
- Security requirements change
- Payment options expand

## Notes
- Claude CANNOT send money or request payments
- All access is read-only for security
- Venmo requires phone verification
- Social feed can be set to private
- Venmo card linked to balance
- Bank transfers may take 1-3 days
- Instant transfer has small fee
