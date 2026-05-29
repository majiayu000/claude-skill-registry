---
name: zocdoc
description: Find and book doctors with Zocdoc - search providers, view availability, and manage appointments
category: healthcare
---

# Zocdoc Skill

## Overview
Enables Claude to use Zocdoc for healthcare appointment management including searching for providers, viewing availability, and managing existing appointments.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/zocdoc/install.sh | bash
```

Or manually:
```bash
cp -r skills/zocdoc ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ZOCDOC_EMAIL "your-email@example.com"
canifi-env set ZOCDOC_PASSWORD "your-password"
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
- Search for healthcare providers
- View doctor availability
- Check existing appointments
- Access provider reviews
- View insurance compatibility
- Browse provider profiles

## Usage Examples

### Example 1: Find a Doctor
```
User: "Find a dermatologist near me with good reviews"
Claude: I'll search for dermatologists.
1. Opening Zocdoc via Playwright MCP
2. Searching for dermatologists
3. Filtering by location
4. Sorting by patient reviews
5. Listing top-rated options
```

### Example 2: Check Appointments
```
User: "Do I have any upcoming Zocdoc appointments?"
Claude: I'll check your appointments.
1. Accessing your account
2. Viewing appointments section
3. Listing upcoming appointments
4. Providing appointment details
```

### Example 3: View Provider Info
```
User: "Tell me about Dr. Smith's availability"
Claude: I'll check availability.
1. Finding Dr. Smith's profile
2. Viewing available time slots
3. Checking upcoming dates
4. Summarizing openings
```

## Authentication Flow
1. Navigate to zocdoc.com via Playwright MCP
2. Click "Log in" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for account access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Provider Not Found**: Broaden search criteria
- **No Availability**: Suggest alternative dates

## Self-Improvement Instructions
When Zocdoc updates:
1. Document new search filters
2. Update provider category options
3. Track booking flow changes
4. Log insurance verification updates

## Notes
- Insurance verification available
- Patient reviews and ratings
- Real-time availability
- Appointment reminders
- Video visit options
