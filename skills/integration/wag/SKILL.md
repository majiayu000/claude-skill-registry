---
name: wag
description: On-demand dog walking and pet sitting services.
category: homeservices
---
# Wag Skill

On-demand dog walking and pet sitting services.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/wag/install.sh | bash
```

Or manually:
```bash
cp -r skills/wag ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WAG_EMAIL "your_email"
canifi-env set WAG_PASSWORD "your_password"
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

1. **Book Walk**: Schedule dog walks
2. **Find Walkers**: Search local walkers
3. **GPS Tracking**: Live walk tracking
4. **Pet Sitting**: Book overnight care
5. **Vet Chat**: Access pet health advice

## Usage Examples

### Book Walk
```
User: "Book a dog walk for this afternoon"
Assistant: Schedules on-demand walk
```

### Track Walk
```
User: "Where is my dog right now?"
Assistant: Shows live GPS tracking
```

### Book Sitting
```
User: "Find overnight pet sitting"
Assistant: Returns available sitters
```

### Ask Vet
```
User: "Chat with a vet about my dog"
Assistant: Opens vet chat feature
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Real-time GPS integration

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| No Walkers | Location/time issue | Try later |
| Tracking Error | GPS issue | Refresh app |
| Booking Failed | Availability | Adjust time |

## Notes

- On-demand walks
- GPS live tracking
- Report cards with photos
- Background-checked walkers
- No public API
- Premium services available
