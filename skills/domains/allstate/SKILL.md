---
name: allstate
description: Manage Allstate insurance with Drivewise and Milewise programs.
category: insurance
---
# Allstate Skill

Manage Allstate insurance with Drivewise and Milewise programs.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/allstate/install.sh | bash
```

Or manually:
```bash
cp -r skills/allstate ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ALLSTATE_EMAIL "your_email"
canifi-env set ALLSTATE_PASSWORD "your_password"
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

1. **View Policies**: Access all insurance policies
2. **Drivewise**: View safe driving rewards
3. **File Claims**: Submit and track claims
4. **Milewise**: Pay-per-mile insurance
5. **Rewards**: Access Allstate Rewards program

## Usage Examples

### View Drivewise
```
User: "Show my Drivewise savings"
Assistant: Returns driving rewards data
```

### Check Milewise
```
User: "How many miles have I driven this month?"
Assistant: Returns mileage and cost
```

### File Claim
```
User: "File an auto claim"
Assistant: Starts claim submission
```

### View Rewards
```
User: "Show my Allstate Rewards balance"
Assistant: Returns rewards points
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Telematics integration

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Drivewise Error | Device issue | Reconnect |
| Claim Error | Missing info | Complete form |
| Rewards Error | Account issue | Contact support |

## Notes

- Drivewise safe driver program
- Milewise pay-per-mile option
- Allstate Rewards program
- No public API
- Mobile app available
- Agent network
