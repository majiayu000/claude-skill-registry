---
name: root
description: Usage-based auto insurance that rewards good driving.
category: insurance
---
# Root Insurance Skill

Usage-based auto insurance that rewards good driving.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/root/install.sh | bash
```

Or manually:
```bash
cp -r skills/root ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ROOT_EMAIL "your_email"
canifi-env set ROOT_PASSWORD "your_password"
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

1. **View Policy**: Access auto insurance policy
2. **Driving Score**: View behavior-based rating
3. **Test Drive**: Complete driving evaluation
4. **File Claims**: Submit and track claims
5. **Savings Track**: Monitor premium savings

## Usage Examples

### View Score
```
User: "What's my Root driving score?"
Assistant: Returns driving behavior rating
```

### Check Savings
```
User: "How much am I saving with Root?"
Assistant: Returns premium comparison
```

### File Claim
```
User: "File an accident claim"
Assistant: Starts claim process
```

### Test Drive
```
User: "Start my Root test drive"
Assistant: Begins driving evaluation period
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser/app automation
4. GPS telematics required

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Test Failed | Not enough data | Complete more trips |
| Score Error | GPS issue | Enable location |
| Claim Error | Missing info | Complete details |

## Notes

- Fair pricing based on driving
- Test drive evaluation period
- Mobile app required
- GPS-based tracking
- No public API
- Available in select states
