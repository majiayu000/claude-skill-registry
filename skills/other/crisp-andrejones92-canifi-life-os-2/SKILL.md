---
name: crisp
description: Enables Claude to manage Crisp chat support conversations, helpdesk tickets, and customer communications
version: 1.0.0
author: Canifi
category: communication
---

# Crisp Skill

## Overview
Automates Crisp customer messaging platform operations including live chat management, helpdesk tickets, knowledge base, and CRM features through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/crisp/install.sh | bash
```

Or manually:
```bash
cp -r skills/crisp ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CRISP_EMAIL "your-email@example.com"
canifi-env set CRISP_PASSWORD "your-password"
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
- Respond to live chat conversations
- Manage helpdesk tickets
- Access visitor and contact data
- Use canned responses
- Create knowledge base articles
- Set operator availability
- View conversation analytics
- Manage chatbot flows

## Usage Examples

### Example 1: Respond to Live Chat
```
User: "Reply to the visitor asking about pricing on Crisp"
Claude: I'll respond to that chat.
- Navigate to Crisp inbox
- Find pricing inquiry conversation
- Review visitor context and history
- Compose helpful pricing response
- Send message
- Confirm delivery
```

### Example 2: Create Ticket
```
User: "Convert this chat to a helpdesk ticket for follow-up"
Claude: I'll create that ticket.
- Open current conversation
- Click convert to ticket
- Set priority and category
- Assign to appropriate team
- Confirm ticket created
```

### Example 3: Use Canned Response
```
User: "Send the business hours canned response"
Claude: I'll send that response.
- Open active conversation
- Access canned responses shortcut
- Select "business hours" response
- Insert and send
- Confirm message sent
```

### Example 4: Update Knowledge Base
```
User: "Add a new FAQ article about returns to Crisp"
Claude: I'll create that article.
- Navigate to Knowledge Base section
- Click create new article
- Set category as FAQ
- Write returns policy content
- Publish article
- Confirm live
```

## Authentication Flow
1. Navigate to app.crisp.chat via Playwright MCP
2. Enter email and password from canifi-env
3. Select website if multiple
4. Handle 2FA if enabled (notify user via iMessage)
5. Verify inbox access
6. Maintain session cookies

## Error Handling
- **Login Failed**: Verify credentials, check for CAPTCHA
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Website Not Found**: List available websites for selection
- **Conversation Closed**: Cannot send to closed chats
- **Visitor Offline**: Message will be delivered when they return
- **Rate Limited**: Implement backoff for rapid messages
- **Permission Denied**: Check operator permissions

## Self-Improvement Instructions
When encountering new Crisp features:
1. Document new chat UI elements
2. Add support for new message types
3. Log successful response patterns
4. Update for new helpdesk features

## Notes
- Free plan has limited features
- Chatbot flows require Pro plan or higher
- Visitor data depends on tracking setup
- Knowledge base requires appropriate plan
- Multiple operators can view same conversation
- Mobile app notifications may duplicate
- Campaign features have separate interface
