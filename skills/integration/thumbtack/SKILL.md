---
name: thumbtack
description: Find and hire local professionals for home projects and services.
category: homeservices
---
# Thumbtack Skill

Find and hire local professionals for home projects and services.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/thumbtack/install.sh | bash
```

Or manually:
```bash
cp -r skills/thumbtack ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set THUMBTACK_EMAIL "your_email"
canifi-env set THUMBTACK_PASSWORD "your_password"
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

1. **Get Quotes**: Request quotes from pros
2. **Browse Pros**: Find service professionals
3. **Compare Prices**: Review multiple estimates
4. **Schedule Service**: Book appointments
5. **Review History**: Access past projects

## Usage Examples

### Get Quotes
```
User: "Get quotes for house painting"
Assistant: Requests quotes from local painters
```

### Find Pro
```
User: "Find a plumber on Thumbtack"
Assistant: Returns matching professionals
```

### Compare Options
```
User: "Compare my painting quotes"
Assistant: Shows quote comparison
```

### Book Service
```
User: "Book this electrician"
Assistant: Schedules appointment
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Quote request system

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| No Quotes | Low availability | Expand criteria |
| Booking Failed | Pro unavailable | Try another |
| Message Failed | Account issue | Contact support |

## Notes

- Local service marketplace
- Multiple quotes system
- Reviews and ratings
- Price transparency
- No public API
- Instant match option
