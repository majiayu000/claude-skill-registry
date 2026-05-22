---
name: webex
description: Enables Claude to schedule Webex meetings, manage spaces, and handle team collaboration
version: 1.0.0
author: Canifi
category: communication
---

# Webex Skill

## Overview
Automates Cisco Webex operations including meeting scheduling, space management, messaging, and collaboration features through the web interface.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/webex/install.sh | bash
```

Or manually:
```bash
cp -r skills/webex ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WEBEX_EMAIL "your-email@example.com"
canifi-env set WEBEX_PASSWORD "your-password"
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
- Create and manage spaces/teams
- Send messages in spaces
- Share files and content
- Access meeting recordings
- Manage personal meeting room
- Configure meeting settings
- Handle meeting invitations

## Usage Examples

### Example 1: Schedule Meeting
```
User: "Schedule a Webex meeting for tomorrow at 10am with the design team"
Claude: I'll schedule that meeting.
- Navigate to Webex web portal
- Click Schedule Meeting
- Set topic and time
- Add design team participants
- Configure meeting options
- Send invitations
```

### Example 2: Send Space Message
```
User: "Post an update in the Project Alpha space"
Claude: I'll post that update.
- Navigate to Spaces
- Find Project Alpha space
- Compose update message
- Send to space
- Confirm delivery
```

### Example 3: Access Recording
```
User: "Download the recording from yesterday's all-hands meeting"
Claude: I'll find that recording.
- Navigate to Recordings section
- Locate all-hands meeting
- Initiate download
- Confirm download started
```

### Example 4: Create New Space
```
User: "Create a Webex space for the new marketing campaign"
Claude: I'll create that space.
- Click create new space
- Name it "Marketing Campaign"
- Add team members
- Set space settings
- Confirm creation
```

## Authentication Flow
1. Navigate to web.webex.com via Playwright MCP
2. Enter email and password from canifi-env
3. Handle SSO redirect if configured
4. Complete 2FA if enabled (notify user via iMessage)
5. Verify dashboard access
6. Maintain session cookies

## Error Handling
- **Login Failed**: Check SSO settings, retry
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **SSO Required**: Handle organization SSO flow
- **Space Not Found**: Search by name variations
- **Recording Unavailable**: Check processing status
- **Meeting Limit**: Notify user of license limits
- **Permission Denied**: Check organization policies

## Self-Improvement Instructions
When encountering new Webex features:
1. Document new UI elements
2. Add support for new meeting types
3. Log successful scheduling patterns
4. Update for new collaboration features

## Notes
- Webex has different plans with varying features
- SSO common in enterprise deployments
- Personal room URL is persistent
- Recordings may take time to process
- Spaces integrate with Webex Teams
- Some features require desktop app
- Meeting capacity varies by license
