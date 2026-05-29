---
name: carfax
description: Access vehicle history reports and find cars with clean records.
category: automotive
---
# Carfax Skill

Access vehicle history reports and find cars with clean records.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/carfax/install.sh | bash
```

Or manually:
```bash
cp -r skills/carfax ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CARFAX_EMAIL "your_email"
canifi-env set CARFAX_PASSWORD "your_password"
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

1. **History Reports**: Pull full vehicle history
2. **Search Cars**: Find Carfax-verified vehicles
3. **Service History**: View maintenance records
4. **Accident Check**: Identify damage history
5. **Value Estimate**: Get market valuations

## Usage Examples

### Get Report
```
User: "Pull a Carfax report for this VIN"
Assistant: Returns vehicle history
```

### Check Accidents
```
User: "Does this car have any accidents?"
Assistant: Returns accident history
```

### Find Clean Cars
```
User: "Find cars with no accidents on Carfax"
Assistant: Returns verified clean vehicles
```

### Service Records
```
User: "Show service history for this vehicle"
Assistant: Returns maintenance records
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Report credits system

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| VIN Not Found | Invalid VIN | Verify number |
| No Credits | Reports depleted | Purchase more |
| Report Error | Data unavailable | Try later |

## Notes

- Industry standard reports
- Accident detection
- Service record tracking
- Used car marketplace
- No public API
- Report subscriptions available
