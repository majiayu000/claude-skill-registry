---
name: telegram-bot
description: "Telegram bot development - chatbots, notifications, AI assistants, and group automation"
version: "1.0.0"
author: claude-office-skills
license: MIT

category: messaging
tags:
  - telegram
  - bot
  - chatbot
  - automation
  - notifications
department: Engineering

models:
  recommended:
    - claude-sonnet-4

mcp:
  server: telegram-mcp
  tools:
    - telegram_send_message
    - telegram_get_updates
    - telegram_send_photo

capabilities:
  - bot_development
  - message_handling
  - ai_integration
  - notification_system
  - group_management

languages:
  - en
  - zh

related_skills:
  - discord-bot
  - whatsapp-automation
  - ai-agent-builder
  - slack-workflows
---

# Telegram Bot

Build Telegram bots for chatbots, notifications, AI assistants, and group automation. Based on n8n's Telegram workflow templates.

## Overview

This skill covers:
- Bot setup and configuration
- Message handling patterns
- AI-powered assistants
- Notification workflows
- Group automation

---

## Bot Setup

### Creating a Bot

```yaml
setup_steps:
  1. create_bot:
      - open: @BotFather on Telegram
      - command: /newbot
      - provide: bot_name
      - provide: bot_username (must end in 'bot')
      - receive: API_token
      
  2. configure_bot:
      - command: /setdescription
      - command: /setabouttext
      - command: /setuserpic
      - command: /setcommands
      
  3. get_chat_id:
      - start: conversation with bot
      - call: https://api.telegram.org/bot{TOKEN}/getUpdates
      - extract: chat.id from response
```

### Bot Commands

```yaml
commands:
  - command: /start
    description: "Start the bot"
    
  - command: /help
    description: "Show available commands"
    
  - command: /status
    description: "Check system status"
    
  - command: /subscribe
    description: "Subscribe to notifications"
    
  - command: /unsubscribe
    description: "Unsubscribe from notifications"
```

---

## Message Handlers

### Basic Message Handler

```yaml
workflow: "Telegram Message Handler"
trigger: telegram_message

handlers:
  text_message:
    action: |
      1. Parse message text
      2. Determine intent
      3. Process request
      4. Send response
      
  command:
    pattern: "^/"
    action: route_to_command_handler
    
  photo:
    action: |
      1. Download photo
      2. Process with vision AI
      3. Respond with analysis
      
  document:
    action: |
      1. Download document
      2. Extract content
      3. Process and respond
      
  voice:
    action: |
      1. Download audio
      2. Transcribe with Whisper
      3. Process text
      4. Respond (text or voice)
      
  location:
    action: |
      1. Extract coordinates
      2. Lookup local info
      3. Respond with relevant data
```

### n8n Workflow

```yaml
workflow: "Telegram Bot n8n"

nodes:
  - name: "Telegram Trigger"
    type: "n8n-nodes-base.telegramTrigger"
    parameters:
      updates: ["message", "callback_query"]
      
  - name: "Route Message Type"
    type: "n8n-nodes-base.switch"
    parameters:
      rules:
        - output: 0
          condition: "{{ $json.message.text.startsWith('/') }}"
        - output: 1
          condition: "{{ $json.message.photo }}"
        - output: 2
          condition: "{{ $json.message.voice }}"
        - output: 3
          fallback: true
          
  - name: "Process with AI"
    type: "n8n-nodes-base.openAi"
    parameters:
      model: "gpt-4"
      messages:
        - role: "system"
          content: "You are a helpful Telegram assistant."
        - role: "user"
          content: "{{ $json.message.text }}"
          
  - name: "Send Response"
    type: "n8n-nodes-base.telegram"
    parameters:
      chatId: "{{ $json.message.chat.id }}"
      text: "{{ $json.response }}"
```

---

## AI-Powered Bot

### GPT-4 Integration

```yaml
ai_bot:
  name: "AI Assistant Bot"
  
  system_prompt: |
    You are a helpful AI assistant on Telegram.
    
    Guidelines:
    - Be concise (Telegram has message limits)
    - Use emojis appropriately
    - Format with markdown when helpful
    - Ask clarifying questions if needed
    
  features:
    - conversational_memory: true
    - context_window: last_10_messages
    - tools: [web_search, calculator, weather]
    
  message_formatting:
    max_length: 4096
    split_long_messages: true
    use_markdown: true
```

### Multi-Modal Bot

```yaml
multimodal_bot:
  handlers:
    text:
      model: gpt-4
      action: chat_completion
      
    image:
      model: gpt-4-vision
      action: analyze_and_respond
      
    voice:
      transcribe: whisper
      process: gpt-4
      respond: text_or_voice
      
    document:
      extract: based_on_type
      summarize: gpt-4
      respond: text
```

---

## Notification System

### Alert Bot

```yaml
workflow: "System Alert Bot"

triggers:
  - source: monitoring_system
    event: alert
  - source: ci_cd
    event: build_status
  - source: ecommerce
    event: new_order
    
notification_templates:
  alert:
    format: |
      🚨 *Alert: {severity}*
      
      *Service:* {service}
      *Message:* {message}
      *Time:* {timestamp}
      
      [View Dashboard]({dashboard_link})
      
  build:
    format: |
      {status_emoji} *Build {status}*
      
      *Project:* {project}
      *Branch:* {branch}
      *Commit:* `{commit_short}`
      
      {details}
      
  order:
    format: |
      🛒 *New Order!*
      
      *Order:* #{order_id}
      *Customer:* {customer}
      *Total:* ${total}
      *Items:* {item_count}
      
routing:
  by_severity:
    critical: [admin_group, on_call_user]
    warning: [team_group]
    info: [logging_channel]
```

### Scheduled Notifications

```yaml
scheduled_notifications:
  daily_digest:
    schedule: "9am daily"
    template: |
      📊 *Daily Summary - {date}*
      
      📈 Sales: ${sales} ({change})
      👥 New users: {new_users}
      🎫 Open tickets: {tickets}
      
      Have a great day! ☀️
      
  weekly_report:
    schedule: "Monday 9am"
    template: weekly_metrics_report
    
  reminder:
    trigger: custom_event
    template: |
      ⏰ *Reminder*
      
      {reminder_text}
      
      Scheduled by: {creator}
```

---

## Group Automation

### Welcome Bot

```yaml
group_bot:
  on_member_join:
    action: |
      1. Check if new member
      2. Send welcome message
      3. Share rules
      4. Suggest introduction
      
    template: |
      👋 Welcome to {group_name}, {user_name}!
      
      Please:
      1. Read the /rules
      2. Introduce yourself
      3. Ask questions anytime!
      
      Enjoy your stay! 🎉
      
  on_member_leave:
    action: optional_goodbye
    
  moderation:
    - spam_detection: auto_delete + warn
    - link_filtering: whitelist_only
    - flood_control: rate_limit
```

### Poll & Survey Bot

```yaml
poll_bot:
  commands:
    /poll:
      format: "/poll Question | Option1 | Option2 | ..."
      action: create_poll
      
    /survey:
      action: start_multi_question_survey
      
    /results:
      action: show_aggregated_results
      
  features:
    - anonymous_voting: optional
    - multiple_choice: optional
    - scheduled_close: optional
    - export_results: to_sheets
```

---

## Inline Features

### Inline Keyboard

```yaml
inline_keyboard:
  example:
    text: "Choose an option:"
    keyboard:
      - row:
          - text: "Option 1"
            callback_data: "opt_1"
          - text: "Option 2"
            callback_data: "opt_2"
      - row:
          - text: "Cancel"
            callback_data: "cancel"
            
  callback_handler:
    opt_1:
      action: process_option_1
      response: "You selected Option 1"
      
    opt_2:
      action: process_option_2
      response: "You selected Option 2"
      
    cancel:
      action: cancel_operation
      response: "Operation cancelled"
```

### Inline Query

```yaml
inline_mode:
  trigger: "@botname query"
  
  results:
    - type: article
      title: "{query} result"
      description: "Click to send"
      message_text: "Result for: {query}"
      
    - type: photo
      photo_url: "{search_result_image}"
      
    - type: gif
      gif_url: "{gif_url}"
```

---

## Output Example

**Request**: "Create a Telegram notification bot for server alerts"

**Output**:

```markdown
# Server Alert Telegram Bot

## Setup

1. Create bot with @BotFather
2. Get token: `123456:ABC-DEF...`
3. Get chat ID for alerts channel

## n8n Workflow

```yaml
nodes:
  1. Webhook (receives alerts)
  2. Format Message
  3. Telegram Send
```

## Alert Templates

**Critical Alert:**
```
🚨 CRITICAL ALERT

Server: production-web-01
Status: DOWN
Time: 2026-01-30 14:32:05 UTC

Details:
- CPU: 98%
- Memory: 95%
- Disk: 89%

[View Grafana] [Acknowledge]
```

**Recovery:**
```
✅ RECOVERED

Server: production-web-01
Downtime: 5 minutes
Status: All systems normal

Incident resolved automatically.
```

## Implementation

```javascript
// Send alert function
async function sendAlert(severity, message, details) {
  const emoji = {
    critical: '🚨',
    warning: '⚠️',
    info: 'ℹ️',
    success: '✅'
  };
  
  const text = `${emoji[severity]} *${severity.toUpperCase()}*\n\n${message}\n\n${details}`;
  
  await telegram.sendMessage({
    chat_id: ALERT_CHANNEL_ID,
    text: text,
    parse_mode: 'Markdown'
  });
}
```

## Features
- Severity-based routing
- Inline action buttons
- Acknowledgment tracking
- Escalation rules
```

---

*Telegram Bot Skill - Part of Claude Office Skills*
