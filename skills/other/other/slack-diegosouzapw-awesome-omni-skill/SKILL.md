---
name: slack
description: Enables Claude to manage Slack workspaces, send messages, manage channels, and automate team communication
version: 1.0.0
author: Canifi
category: communication
---

# Slack Skill

## Overview
Automates Slack workspace interactions including sending messages, managing channels, searching conversations, setting status, and handling notifications through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/slack/install.sh | bash
```

Or manually:
```bash
cp -r skills/slack ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SLACK_EMAIL "your-email@example.com"
canifi-env set SLACK_WORKSPACE_URL "your-workspace.slack.com"
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
- Send direct messages and channel messages
- Create, archive, and manage channels
- Search messages and files across workspaces
- Set user status and availability
- Manage notifications and Do Not Disturb settings
- Upload and share files in conversations
- React to messages with emojis
- Create and manage Slack Connect channels

## Usage Examples

### Example 1: Send a Direct Message
```
User: "Send a Slack message to John saying the meeting is moved to 3pm"
Claude: I'll send that message to John on Slack.
- Navigate to Slack workspace via Playwright
- Open direct message with John
- Type and send: "Hey, the meeting is moved to 3pm"
- Confirm message sent successfully
```

### Example 2: Post to a Channel
```
User: "Post in #engineering that the deployment is complete"
Claude: I'll post the update to the engineering channel.
- Navigate to #engineering channel
- Compose message: "Deployment is complete"
- Send message to channel
- Confirm delivery
```

### Example 3: Search Conversations
```
User: "Find all messages about the Q4 budget in Slack"
Claude: I'll search Slack for Q4 budget discussions.
- Use Slack search with query "Q4 budget"
- Collect matching messages and threads
- Present summary of findings with links
```

### Example 4: Set Status
```
User: "Set my Slack status to 'In a meeting' for 1 hour"
Claude: I'll update your Slack status.
- Navigate to profile settings
- Set status emoji and text: "In a meeting"
- Set expiration to 1 hour
- Confirm status updated
```

## Authentication Flow
1. Navigate to workspace URL via Playwright MCP
2. Enter email from canifi-env
3. Handle SSO or password authentication
4. Complete 2FA if prompted (notify user via iMessage)
5. Verify workspace access
6. Maintain session cookies for subsequent requests

## Error Handling
- **Login Failed**: Retry 3x with fresh browser context, then iMessage notification
- **Session Expired**: Re-authenticate automatically using stored credentials
- **Rate Limited**: Implement exponential backoff (1s, 2s, 4s, 8s)
- **2FA Required**: Send iMessage notification for user to provide code
- **Workspace Not Found**: Verify workspace URL and notify user
- **Channel Not Found**: Search for similar channel names and suggest alternatives
- **User Not Found**: Search workspace directory and suggest matches

## Self-Improvement Instructions
When encountering new Slack UI patterns or features:
1. Document the new element selectors
2. Update capability list if new features discovered
3. Log successful automation patterns for future reference
4. Suggest SKILL.md updates via commit to working-branch

## Notes
- Slack frequently updates UI; selectors may need adjustment
- Some enterprise workspaces have additional SSO requirements
- File uploads may be size-limited based on workspace plan
- Slack Connect channels require additional permissions
- Message formatting supports Slack markdown syntax
