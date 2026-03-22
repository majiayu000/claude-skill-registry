---
name: discord-bot
description: "Discord bot development - community management, moderation, notifications, and AI integration"
version: "1.0.0"
author: claude-office-skills
license: MIT

category: messaging
tags:
  - discord
  - bot
  - community
  - moderation
  - automation
department: Engineering

models:
  recommended:
    - claude-sonnet-4

mcp:
  server: discord-mcp
  tools:
    - discord_send_message
    - discord_create_channel
    - discord_manage_roles

capabilities:
  - bot_development
  - community_management
  - moderation
  - notification_system
  - ai_integration

languages:
  - en
  - zh

related_skills:
  - telegram-bot
  - slack-workflows
  - ai-agent-builder
---

# Discord Bot

Build Discord bots for community management, moderation, notifications, and AI integration. Based on n8n's Discord workflow templates.

## Overview

This skill covers:
- Bot setup and configuration
- Slash commands and interactions
- Moderation automation
- Notification workflows
- AI-powered features

---

## Bot Setup

### Creating a Discord Bot

```yaml
setup_steps:
  1. create_application:
      url: https://discord.com/developers/applications
      action: "New Application"
      
  2. create_bot:
      section: "Bot"
      action: "Add Bot"
      copy: token
      
  3. configure_intents:
      enable:
        - PRESENCE_INTENT
        - SERVER_MEMBERS_INTENT
        - MESSAGE_CONTENT_INTENT
        
  4. invite_bot:
      section: "OAuth2 > URL Generator"
      scopes: [bot, applications.commands]
      permissions: [based_on_needs]
      generate: invite_link
```

### Slash Commands

```yaml
slash_commands:
  - name: help
    description: "Show bot help"
    
  - name: ping
    description: "Check bot latency"
    
  - name: poll
    description: "Create a poll"
    options:
      - name: question
        type: STRING
        required: true
      - name: options
        type: STRING
        required: true
        
  - name: remind
    description: "Set a reminder"
    options:
      - name: time
        type: STRING
        required: true
      - name: message
        type: STRING
        required: true
```

---

## Moderation Bot

### Auto-Moderation

```yaml
auto_moderation:
  spam_detection:
    triggers:
      - repeated_messages: 5_in_10_seconds
      - mass_mentions: more_than_5
      - link_spam: multiple_links_no_text
    actions:
      - delete_messages
      - timeout: 5_minutes
      - log_to_mod_channel
      
  word_filter:
    blocked_words: [list_of_words]
    action:
      - delete_message
      - warn_user
      
  link_filter:
    allowed_domains: [youtube.com, github.com]
    action: delete_if_not_allowed
    
  raid_protection:
    triggers:
      - join_rate: 10_per_minute
    actions:
      - enable_verification
      - notify_mods
      - slow_mode: enable
```

### Moderation Commands

```yaml
mod_commands:
  /warn:
    permission: MODERATE_MEMBERS
    action: |
      1. Record warning
      2. DM user with reason
      3. Log to mod channel
      
  /timeout:
    permission: MODERATE_MEMBERS
    options: [user, duration, reason]
    action: |
      1. Apply timeout
      2. DM user
      3. Log action
      
  /ban:
    permission: BAN_MEMBERS
    options: [user, reason, delete_messages]
    action: |
      1. Ban user
      2. Log to mod channel
      3. Optional: post to #bans
      
  /warnings:
    permission: MODERATE_MEMBERS
    action: show_user_warning_history
```

---

## Community Features

### Welcome System

```yaml
welcome_system:
  on_member_join:
    actions:
      - assign_role: "New Member"
      - send_dm:
          template: |
            👋 Welcome to {server_name}!
            
            Here's how to get started:
            1. Read #rules
            2. Grab roles in #roles
            3. Introduce yourself in #introductions
            
            Need help? Ask in #support
            
      - post_welcome:
          channel: "#welcome"
          template: |
            🎉 Welcome {user_mention} to the server!
            
            They are member #{member_count}
            
  on_member_leave:
    channel: "#logs"
    template: "{user} left the server. Duration: {time_since_join}"
```

### Role Management

```yaml
reaction_roles:
  channel: "#roles"
  message: |
    React to get roles:
    
    🎮 - Gamer
    💻 - Developer
    🎨 - Artist
    📚 - Student
    
  mappings:
    "🎮": role_id_gamer
    "💻": role_id_developer
    "🎨": role_id_artist
    "📚": role_id_student
    
level_roles:
  system: xp_based
  roles:
    - level: 5
      role: "Active Member"
    - level: 10
      role: "Regular"
    - level: 25
      role: "Veteran"
    - level: 50
      role: "Legend"
```

### Ticket System

```yaml
ticket_system:
  create_ticket:
    trigger: button_click OR /ticket
    action:
      - create_channel: "ticket-{user}-{number}"
      - set_permissions: [user, support_team]
      - send_initial_message:
          template: |
            🎫 **Support Ticket**
            
            User: {user_mention}
            Created: {timestamp}
            
            Please describe your issue and a team member will assist you shortly.
            
            React with ✅ to close this ticket.
            
  close_ticket:
    trigger: reaction OR /close
    action:
      - save_transcript: to_logs_channel
      - delete_channel: after_5_seconds
      - dm_user: transcript_link
```

---

## Notification Workflows

### n8n Integration

```yaml
workflow: "Discord Notifications"

triggers:
  github_release:
    action:
      channel: "#releases"
      embed:
        title: "🚀 New Release: {version}"
        description: "{release_notes}"
        color: 0x00ff00
        fields:
          - name: "Download"
            value: "[Link]({download_url})"
            
  twitch_live:
    action:
      channel: "#streams"
      message: "@everyone {streamer} is now live!"
      embed:
        title: "{stream_title}"
        image: "{thumbnail}"
        
  youtube_video:
    action:
      channel: "#videos"
      embed:
        title: "{video_title}"
        description: "{description}"
        thumbnail: "{thumbnail}"
```

### Scheduled Posts

```yaml
scheduled_posts:
  daily_question:
    schedule: "10am daily"
    channel: "#daily-discussion"
    template: |
      🤔 **Question of the Day**
      
      {random_question}
      
      Share your thoughts below! 👇
      
  weekly_recap:
    schedule: "Sunday 6pm"
    channel: "#announcements"
    template: |
      📊 **Weekly Server Recap**
      
      New members: {new_members}
      Messages: {message_count}
      Most active channel: {top_channel}
      Top contributor: {top_user}
      
      Thanks for being part of our community! ❤️
```

---

## AI Integration

### AI Chat Bot

```yaml
ai_bot:
  trigger: mention OR dm
  
  configuration:
    model: gpt-4
    system_prompt: |
      You are a helpful Discord bot assistant.
      - Be friendly and use Discord-appropriate language
      - Use emojis naturally
      - Keep responses concise
      - Help with server-related questions
      
  features:
    - conversation_memory: per_channel
    - rate_limiting: 10_per_minute
    - content_filter: enabled
    
  commands:
    /ask:
      description: "Ask the AI a question"
      action: ai_response
      
    /summarize:
      description: "Summarize recent messages"
      action: summarize_channel_history
```

### Image Generation

```yaml
image_generation:
  command: /imagine
  
  options:
    - prompt: STRING (required)
    - style: CHOICE [realistic, anime, cartoon, abstract]
    - size: CHOICE [square, portrait, landscape]
    
  workflow:
    1. receive_command
    2. send_generating_message
    3. call_dalle_api
    4. send_result_with_buttons:
        - Regenerate
        - Upscale
        - Variations
```

---

## Embeds & Components

### Rich Embed

```yaml
embed:
  title: "Server Information"
  description: "Welcome to our community!"
  color: 0x5865F2  # Discord blurple
  
  thumbnail:
    url: "{server_icon}"
    
  fields:
    - name: "📊 Members"
      value: "{member_count}"
      inline: true
    - name: "💬 Channels"
      value: "{channel_count}"
      inline: true
    - name: "🎭 Roles"
      value: "{role_count}"
      inline: true
    - name: "📅 Created"
      value: "{creation_date}"
      inline: false
      
  footer:
    text: "Last updated"
    icon_url: "{bot_avatar}"
    
  timestamp: "{current_time}"
```

### Button Components

```yaml
buttons:
  row_1:
    - type: button
      style: primary
      label: "Accept Rules"
      custom_id: "accept_rules"
      
    - type: button
      style: secondary
      label: "View Rules"
      custom_id: "view_rules"
      
  row_2:
    - type: button
      style: link
      label: "Website"
      url: "https://example.com"
      
    - type: button
      style: danger
      label: "Leave"
      custom_id: "leave_confirm"
```

---

## Output Example

**Request**: "Create a Discord welcome bot"

**Output**:

```markdown
# Discord Welcome Bot

## Configuration

```yaml
events:
  - guildMemberAdd
  - guildMemberRemove
```

## Welcome Message

```javascript
// On member join
const welcomeEmbed = {
  title: '👋 Welcome to the Server!',
  description: `Hey ${member.user}, welcome to **${guild.name}**!`,
  color: 0x00ff00,
  fields: [
    { name: '📜 Rules', value: 'Check <#rules-channel>', inline: true },
    { name: '🎭 Roles', value: 'Get roles in <#roles>', inline: true },
    { name: '💬 Chat', value: 'Say hi in <#general>', inline: true }
  ],
  thumbnail: { url: member.user.displayAvatarURL() },
  footer: { text: `Member #${guild.memberCount}` }
};

welcomeChannel.send({ embeds: [welcomeEmbed] });
```

## Auto-Role

```javascript
// Assign "New Member" role
await member.roles.add(newMemberRole);
```

## DM Welcome

```javascript
// Send DM with server info
await member.send({
  content: `Welcome to ${guild.name}! Here's everything you need to know...`,
  embeds: [infoEmbed]
});
```

## n8n Workflow

```yaml
trigger: Discord - On Member Join
actions:
  - Discord - Send Channel Message (welcome)
  - Discord - Add Role
  - Discord - Send DM
  - Google Sheets - Log new member
```
```

---

*Discord Bot Skill - Part of Claude Office Skills*
