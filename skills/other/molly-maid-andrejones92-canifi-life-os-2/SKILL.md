---
name: molly-maid
description: Reliable home cleaning services with personalized cleaning plans.
category: homeservices
---
# Molly Maid Skill

Reliable home cleaning services with personalized cleaning plans.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/molly-maid/install.sh | bash
```

Or manually:
```bash
cp -r skills/molly-maid ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MOLLYMAID_EMAIL "your_email"
canifi-env set MOLLYMAID_PASSWORD "your_password"
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

1. **Book Cleaning**: Schedule house cleaning
2. **Free Estimate**: Get cleaning quotes
3. **Custom Cleaning**: Personalized service plans
4. **Recurring Visits**: Regular cleaning schedules
5. **Special Requests**: Address specific needs

## Usage Examples

### Book Cleaning
```
User: "Book Molly Maid for this week"
Assistant: Schedules cleaning service
```

### Get Estimate
```
User: "Get a free estimate from Molly Maid"
Assistant: Requests quote
```

### Custom Plan
```
User: "Create a custom cleaning plan"
Assistant: Opens plan configuration
```

### Schedule Recurring
```
User: "Set up weekly Molly Maid visits"
Assistant: Creates recurring schedule
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Local franchise system

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| No Coverage | Location outside area | Find nearby franchise |
| Booking Error | Availability issue | Try different time |
| Estimate Failed | Incomplete info | Provide details |

## Notes

- Neighborly company
- Insured and bonded
- Satisfaction guarantee
- Customizable service
- No public API
- Franchise network
