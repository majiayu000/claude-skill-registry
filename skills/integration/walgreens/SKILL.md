---
name: walgreens
description: Manage prescriptions with Walgreens - check prescription status, schedule pickups, and access pharmacy services
category: healthcare
---

# Walgreens Skill

## Overview
Enables Claude to use Walgreens for pharmacy services including checking prescription status, viewing medication history, and managing account settings.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/walgreens/install.sh | bash
```

Or manually:
```bash
cp -r skills/walgreens ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WALGREENS_EMAIL "your-email@example.com"
canifi-env set WALGREENS_PASSWORD "your-password"
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
- Check prescription status
- View medication history
- Access refill information
- Check store locations
- View immunization records
- Access myWalgreens rewards

## Usage Examples

### Example 1: Check Prescription Status
```
User: "Is my Walgreens prescription ready?"
Claude: I'll check your prescription.
1. Opening Walgreens via Playwright MCP
2. Accessing pharmacy section
3. Viewing prescription status
4. Checking ready for pickup
5. Reporting availability
```

### Example 2: View Medication List
```
User: "What prescriptions do I have at Walgreens?"
Claude: I'll list your medications.
1. Accessing prescription history
2. Viewing current medications
3. Listing active prescriptions
4. Noting refill eligibility
```

### Example 3: Find Pharmacy
```
User: "Find a 24-hour Walgreens near me"
Claude: I'll find 24-hour locations.
1. Accessing store locator
2. Filtering for 24-hour
3. Finding nearest matches
4. Providing addresses
```

## Authentication Flow
1. Navigate to walgreens.com via Playwright MCP
2. Click "Sign in" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for account access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Prescription Not Found**: Verify pharmacy location
- **Store Error**: Try alternative locations

## Self-Improvement Instructions
When Walgreens updates:
1. Document new pharmacy features
2. Update digital service options
3. Track rewards program changes
4. Log clinic service updates

## Notes
- myWalgreens rewards program
- Healthcare clinic services
- Photo services available
- Drive-thru pharmacy
- Curbside pickup option
