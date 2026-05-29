---
name: haven-life
description: Simple, affordable term life insurance online.
category: insurance
---
# Haven Life Skill

Simple, affordable term life insurance online.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/haven-life/install.sh | bash
```

Or manually:
```bash
cp -r skills/haven-life ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HAVENLIFE_EMAIL "your_email"
canifi-env set HAVENLIFE_PASSWORD "your_password"
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

1. **Get Quote**: Instant term life quotes
2. **Apply Online**: Complete application digitally
3. **View Policy**: Access policy details
4. **Beneficiaries**: Manage beneficiary info
5. **Coverage Tools**: Estimate coverage needs

## Usage Examples

### Get Quote
```
User: "Get a Haven Life quote"
Assistant: Returns term life pricing
```

### Check Policy
```
User: "Show my Haven Life policy"
Assistant: Returns policy details
```

### Update Beneficiary
```
User: "Update my beneficiary information"
Assistant: Opens beneficiary management
```

### Estimate Coverage
```
User: "How much life insurance do I need?"
Assistant: Runs coverage calculator
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Backed by MassMutual

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Quote Error | Eligibility issue | Adjust parameters |
| Application Error | Medical history | Additional review |
| Update Failed | Verification needed | Contact support |

## Notes

- Simple term life
- MassMutual backed
- InstantTerm option
- Online application
- No public API
- Mobile access
