---
name: calendly
description: Automated scheduling for meetings and appointments.
category: productivity
---
# Calendly Skill

Automated scheduling for meetings and appointments.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/calendly/install.sh | bash
```

Or manually:
```bash
cp -r skills/calendly ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CALENDLY_ACCESS_TOKEN "your_token"
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

1. **View Availability**: Check open time slots
2. **Create Event Types**: Set up meeting types
3. **Manage Bookings**: View and cancel meetings
4. **Share Links**: Generate scheduling links
5. **Team Scheduling**: Round robin and collective

## Usage Examples

### Check Schedule
```
User: "What meetings do I have this week?"
Assistant: Returns scheduled events
```

### Share Link
```
User: "Get my Calendly link"
Assistant: Returns scheduling URL
```

### Cancel Meeting
```
User: "Cancel my 3pm tomorrow"
Assistant: Cancels the event
```

### Create Event Type
```
User: "Create a 30-minute meeting type"
Assistant: Sets up new event type
```

## Authentication Flow

1. OAuth2 authentication
2. Personal access tokens
3. API v2 available
4. Webhook support

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid token | Re-authorize |
| Not Found | Event deleted | Verify ID |
| Conflict | Time unavailable | Choose different slot |
| Rate Limited | Too many requests | Slow down |

## Notes

- Full REST API
- Webhooks for events
- Team scheduling
- Custom branding
- Integration ecosystem
- Routing forms
