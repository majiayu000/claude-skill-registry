---
name: lemonade
description: AI-powered insurance for renters, homeowners, pet, and life coverage.
category: insurance
---
# Lemonade Skill

AI-powered insurance for renters, homeowners, pet, and life coverage.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/lemonade/install.sh | bash
```

Or manually:
```bash
cp -r skills/lemonade ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LEMONADE_EMAIL "your_email"
canifi-env set LEMONADE_PASSWORD "your_password"
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

1. **View Policies**: Access all Lemonade policies
2. **Instant Claims**: File claims via AI Maya
3. **Get Quotes**: Instant coverage quotes
4. **Giveback**: View social impact donations
5. **Policy Adjust**: Modify coverage instantly

## Usage Examples

### File Claim
```
User: "File a claim with Lemonade"
Assistant: Connects to AI Maya for instant claim
```

### Get Quote
```
User: "Get a Lemonade renters insurance quote"
Assistant: Returns instant pricing
```

### View Giveback
```
User: "Show my Lemonade Giveback impact"
Assistant: Returns charitable contributions
```

### Adjust Policy
```
User: "Add laptop coverage to my policy"
Assistant: Updates policy instantly
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. AI-powered interface

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Claim Denied | Coverage issue | Review policy |
| Quote Error | Location issue | Check eligibility |
| Adjustment Failed | Limit reached | Contact support |

## Notes

- AI-powered claims (Maya)
- Instant everything
- Giveback program (social good)
- B-Corp certified
- No public API
- Mobile-first design
