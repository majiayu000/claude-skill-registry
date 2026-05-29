---
name: taskrabbit
description: Hire local Taskers for everyday tasks and handyman services.
category: homeservices
---
# TaskRabbit Skill

Hire local Taskers for everyday tasks and handyman services.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/taskrabbit/install.sh | bash
```

Or manually:
```bash
cp -r skills/taskrabbit ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TASKRABBIT_EMAIL "your_email"
canifi-env set TASKRABBIT_PASSWORD "your_password"
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

1. **Find Taskers**: Search for skilled helpers nearby
2. **Book Tasks**: Schedule service appointments
3. **Task Categories**: Browse available services
4. **Chat Taskers**: Communicate with hired help
5. **Manage Bookings**: View and modify appointments

## Usage Examples

### Find Helper
```
User: "Find someone to help me move furniture"
Assistant: Returns available Taskers
```

### Book Task
```
User: "Book a Tasker for IKEA assembly"
Assistant: Schedules appointment
```

### Message Tasker
```
User: "Send a message to my Tasker"
Assistant: Opens chat interface
```

### Check Booking
```
User: "When is my TaskRabbit appointment?"
Assistant: Returns booking details
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Location-based matching

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| No Taskers | Location/time issue | Adjust search |
| Booking Failed | Tasker unavailable | Try another |
| Payment Failed | Card issue | Update payment |

## Notes

- Same-day availability
- Background checked Taskers
- Wide range of services
- IKEA partnership
- No public API
- Mobile app available
