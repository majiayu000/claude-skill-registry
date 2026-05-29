---
name: mychart
description: Access health records with MyChart - view medical records, messages, and appointment information
category: healthcare
---

# MyChart Skill

## Overview
Enables Claude to use MyChart for patient portal access including viewing health records, managing appointments, and communicating with healthcare providers.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/mychart/install.sh | bash
```

Or manually:
```bash
cp -r skills/mychart ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MYCHART_EMAIL "your-email@example.com"
canifi-env set MYCHART_PASSWORD "your-password"
canifi-env set MYCHART_ORGANIZATION "your-healthcare-org"
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
- View health summary
- Check test results
- Access appointment history
- View message inbox
- Check medications list
- Access immunization records

## Usage Examples

### Example 1: View Health Summary
```
User: "Show me my MyChart health summary"
Claude: I'll access your health summary.
1. Opening MyChart via Playwright MCP
2. Logging into your organization's portal
3. Accessing health summary
4. Viewing key health information
```

### Example 2: Check Test Results
```
User: "Are there any new test results in MyChart?"
Claude: I'll check for test results.
1. Accessing test results section
2. Viewing recent results
3. Checking for new entries
4. Summarizing available results
```

### Example 3: View Appointments
```
User: "What appointments do I have scheduled?"
Claude: I'll check your appointments.
1. Accessing appointments section
2. Viewing upcoming visits
3. Listing scheduled appointments
4. Providing details and locations
```

## Authentication Flow
1. Navigate to your organization's MyChart via Playwright MCP
2. Enter username/email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for portal access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Portal Maintenance**: Note downtime
- **Organization Error**: Verify portal URL

## Self-Improvement Instructions
When MyChart updates:
1. Document new Epic features
2. Update navigation patterns
3. Track portal enhancements
4. Log integration changes

## Notes
- Epic Systems patient portal
- Used by many health systems
- Organization-specific URLs
- Telehealth integration
- Mobile app companion
