---
name: repairpal
description: Find certified shops and get fair price estimates for car repairs.
category: automotive
---
# RepairPal Skill

Find certified shops and get fair price estimates for car repairs.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/repairpal/install.sh | bash
```

Or manually:
```bash
cp -r skills/repairpal ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set REPAIRPAL_EMAIL "your_email"
canifi-env set REPAIRPAL_PASSWORD "your_password"
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

1. **Price Estimates**: Get fair repair cost ranges
2. **Find Shops**: Locate certified repair shops
3. **Shop Reviews**: Read mechanic ratings
4. **Maintenance Guide**: Track service schedules
5. **Warranty Info**: Understand repair warranties

## Usage Examples

### Get Estimate
```
User: "How much should a timing belt replacement cost?"
Assistant: Returns fair price range
```

### Find Shop
```
User: "Find certified shops near me"
Assistant: Returns RepairPal certified locations
```

### Check Reviews
```
User: "Show reviews for this repair shop"
Assistant: Returns ratings and feedback
```

### Service Schedule
```
User: "When should I service my 2020 Accord?"
Assistant: Returns maintenance schedule
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Vehicle-specific data

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Estimate Error | Vehicle not found | Verify make/model |
| Shop Not Found | Location issue | Expand search |
| Data Error | Missing info | Complete vehicle details |

## Notes

- Fair price guarantee
- Certified shop network
- Independent estimates
- Manufacturer data
- No public API
- Consumer advocate
