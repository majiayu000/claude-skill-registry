---
name: freshchat
description: Enables Claude to manage Freshchat conversations, bots, and customer messaging operations
version: 1.0.0
author: Canifi
category: communication
---

# Freshchat Skill

## Overview
Automates Freshchat customer messaging operations including live chat, bot conversations, team inbox management, and campaign messaging through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/freshchat/install.sh | bash
```

Or manually:
```bash
cp -r skills/freshchat ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FRESHCHAT_EMAIL "your-email@example.com"
canifi-env set FRESHCHAT_PASSWORD "your-password"
canifi-env set FRESHCHAT_DOMAIN "your-domain.freshchat.com"
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
- Handle live chat conversations
- Manage bot-to-human handoffs
- Access user profiles and history
- Use canned responses
- Create conversation topics
- Monitor team performance
- Set away status
- Send targeted campaigns

## Usage Examples

### Example 1: Handle Bot Handoff
```
User: "Take over the chat that the bot transferred"
Claude: I'll take that conversation.
- Navigate to Freshchat inbox
- Find bot-transferred conversation
- Accept handoff
- Review bot conversation history
- Continue assisting customer
```

### Example 2: Use Canned Response
```
User: "Send the warranty info canned response"
Claude: I'll send that response.
- Open current conversation
- Access canned responses
- Select warranty information
- Insert into chat
- Send to customer
```

### Example 3: Assign to Team
```
User: "Assign this chat to the billing team"
Claude: I'll reassign the conversation.
- Open current conversation
- Click assign option
- Select billing team
- Add handoff note
- Confirm assignment
```

### Example 4: View User Journey
```
User: "Show me this customer's previous conversations"
Claude: I'll pull their history.
- Open customer profile
- Navigate to conversation history
- List previous interactions
- Summarize key issues
- Present timeline
```

## Authentication Flow
1. Navigate to domain.freshchat.com via Playwright MCP
2. Enter email and password from canifi-env
3. Handle 2FA if enabled (notify user via iMessage)
4. Verify inbox access
5. Set online status if needed
6. Maintain session cookies

## Error Handling
- **Login Failed**: Verify domain and credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Conversation Resolved**: Cannot reopen resolved chats
- **Team Not Found**: List available teams
- **Rate Limited**: Implement message queue
- **Bot Active**: Wait for handoff or force takeover
- **User Offline**: Message will be delivered later

## Self-Improvement Instructions
When encountering new Freshchat features:
1. Document new inbox UI elements
2. Add support for new message types
3. Log successful handoff patterns
4. Update for bot integration changes

## Notes
- Part of Freshworks suite
- Integrates with Freshdesk for tickets
- Bot flows defined in Freddy AI
- Campaigns require appropriate plan
- User properties affect segmentation
- In-app messaging differs from web
- Assignment rules affect routing
