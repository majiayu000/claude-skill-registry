---
name: stripe
description: View payment dashboard, check balances, monitor transactions, and review payouts on Stripe
category: finance
---

# Stripe Skill

## Overview
Enables Claude to access Stripe dashboard to view payment activity, check balances, monitor transaction success rates, and review payout schedules for business payment processing.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/stripe/install.sh | bash
```

Or manually:
```bash
cp -r skills/stripe ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set STRIPE_EMAIL "your-email@example.com"
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
- View account balance and pending amounts
- Check recent payment activity
- Monitor payment success rates
- Review payout schedule and history
- View customer payment issues
- Check subscription metrics

## Usage Examples

### Example 1: Check Dashboard Overview
```
User: "How's my Stripe account doing?"
Claude: I'll check your Stripe dashboard.
- Opens dashboard.stripe.com via Playwright MCP
- Logs into account
- Returns: Account Overview
- Available balance: $4,567.89
- Pending balance: $1,234.56
- Today's volume: $2,345.67 (45 payments)
- This month: $34,567.89 gross
- Next payout: $4,567.89 on Jan 8
```

### Example 2: Check Payment Issues
```
User: "Any failed payments I should know about?"
Claude: I'll review payment issues.
- Navigates to payments section
- Failed payments (last 7 days): 12
- Failure reasons:
  - Card declined: 7 (insufficient funds)
  - Expired card: 3
  - Invalid CVC: 2
- Success rate: 96.2%
- Suggests: Consider retry logic for declined cards
```

### Example 3: View Payout History
```
User: "When was my last Stripe payout?"
Claude: I'll check your payout history.
- Navigates to payouts section
- Recent payouts:
  - Jan 5: $5,678.90 → Bank ****1234
  - Jan 3: $4,321.00 → Bank ****1234
  - Jan 1: $6,543.21 → Bank ****1234
- Payout schedule: Daily (2-day rolling)
- Next scheduled: $4,567.89 on Jan 8
```

## Authentication Flow
1. Navigate to dashboard.stripe.com via Playwright MCP
2. Enter email address
3. Enter password
4. Handle 2FA via authenticator or SMS
5. Select correct account if multiple
6. Maintain session for dashboard access

## Error Handling
- Login Failed: Retry, check for account restrictions
- 2FA Required: Complete authenticator verification
- Access Denied: Check team permissions
- Session Expired: Re-authenticate (security)
- Rate Limited: Wait 60 seconds, retry
- Test Mode: Note if viewing test vs live data

## Self-Improvement Instructions
After each interaction:
- Track payment volume patterns
- Note common failure reasons
- Log payout timing accuracy
- Document UI changes

Suggest updates when:
- Stripe updates dashboard
- New features added
- API changes affect data
- Payment methods expand

## Notes
- Claude CANNOT process payments or refunds
- All access is read-only for security
- Test and Live mode have separate data
- Stripe Radar monitors fraud
- Tax reporting available
- Multi-currency support
- Connect for marketplaces (if applicable)
