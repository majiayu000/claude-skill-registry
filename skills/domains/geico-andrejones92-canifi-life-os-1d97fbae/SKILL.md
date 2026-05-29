---
name: geico
description: Manage your GEICO insurance policies and claims.
category: insurance
---
# GEICO Skill

Manage your GEICO insurance policies and claims.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/geico/install.sh | bash
```

Or manually:
```bash
cp -r skills/geico ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GEICO_EMAIL "your_email"
canifi-env set GEICO_PASSWORD "your_password"
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

1. **View Policies**: Access all active insurance policies
2. **File Claims**: Submit and track insurance claims
3. **Get Quotes**: Request quotes for new coverage
4. **Make Payments**: Pay premiums and manage billing
5. **ID Cards**: Access digital insurance ID cards

## Usage Examples

### View Policy
```
User: "Show my GEICO auto policy"
Assistant: Returns policy details and coverage
```

### File Claim
```
User: "File a claim for my car accident"
Assistant: Starts claim submission process
```

### Get Quote
```
User: "Get a quote for renters insurance"
Assistant: Returns coverage options and pricing
```

### Make Payment
```
User: "Pay my insurance premium"
Assistant: Processes payment
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Session-based access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Policy Not Found | Inactive policy | Verify status |
| Claim Error | Missing info | Complete details |
| Payment Failed | Billing issue | Update payment |

## Notes

- Major auto insurer
- Mobile app available
- 24/7 claims support
- No public API
- Discount programs available
- Digital ID cards
