---
name: zoom
description: Enables Claude to schedule meetings, manage recordings, handle webinars, and automate Zoom workspace operations
version: 1.0.0
author: Canifi
category: communication
---

# Zoom Skill

## Overview
Automates Zoom operations including meeting scheduling, recording management, webinar setup, and account administration through the Zoom web portal.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/zoom/install.sh | bash
```

Or manually:
```bash
cp -r skills/zoom ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ZOOM_EMAIL "your-email@example.com"
canifi-env set ZOOM_PASSWORD "your-password"
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
- Schedule and manage meetings
- Access and download cloud recordings
- Create and configure webinars
- Manage meeting settings and security
- Generate meeting reports and analytics
- Handle waiting room and participant management
- Configure virtual backgrounds and settings
- Manage Zoom Phone settings (if enabled)

## Usage Examples

### Example 1: Schedule a Meeting
```
User: "Schedule a Zoom meeting for tomorrow at 2pm with the marketing team"
Claude: I'll schedule that Zoom meeting.
- Navigate to Zoom web portal
- Click Schedule Meeting
- Set topic: "Marketing Team Meeting"
- Set date/time: Tomorrow 2pm
- Enable waiting room and passcode
- Copy meeting link for sharing
```

### Example 2: Access Recordings
```
User: "Download the recording from yesterday's client call"
Claude: I'll find and download that recording.
- Navigate to Recordings section
- Locate yesterday's client call recording
- Initiate download of video file
- Confirm download location
```

### Example 3: Create a Webinar
```
User: "Set up a webinar for next Friday called 'Product Launch'"
Claude: I'll create the webinar.
- Navigate to Webinars section
- Create new webinar "Product Launch"
- Configure date, time, and duration
- Set registration options
- Generate registration link
```

### Example 4: Check Meeting Reports
```
User: "Get attendance report for last week's all-hands meeting"
Claude: I'll pull that attendance report.
- Navigate to Reports section
- Find all-hands meeting from last week
- Export participant report
- Summarize attendance data
```

## Authentication Flow
1. Navigate to zoom.us/signin via Playwright MCP
2. Enter email and password from canifi-env
3. Handle SSO redirect if configured
4. Complete 2FA if enabled (notify user via iMessage)
5. Verify dashboard access
6. Maintain session for subsequent operations

## Error Handling
- **Login Failed**: Retry with fresh context, check SSO settings
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Wait and retry with exponential backoff
- **2FA Required**: iMessage notification for code
- **Meeting Not Found**: Search by date range and title
- **Recording Unavailable**: Check processing status, retry later
- **Insufficient License**: Notify user of plan limitations
- **Webinar Limit Reached**: Notify user of capacity limits

## Self-Improvement Instructions
When encountering new Zoom features:
1. Document new UI elements and selectors
2. Add new meeting types to capabilities
3. Log successful scheduling patterns
4. Update skill with new webinar features

## Notes
- Cloud recordings may take time to process
- Some features require Pro/Business licenses
- Webinars require additional add-on license
- Large meetings have different participant limits
- SSO configurations vary by organization
- Phone features require Zoom Phone license
