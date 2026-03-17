---
name: discord
description: Manage your Discord server - post announcements, create events, moderate, and more. Use when the user mentions Discord, wants to post announcements, manage events, moderate channels, or check server status.
---

# Discord Server Management Skill

A skill for managing the Claude Code Community Ireland Discord server.

## Server Information

- **Guild ID**: 1458570944472813724
- **Server Name**: Claude Code Community Ireland

### Key Channel IDs
- General: 1458570953746288894
- Rules: 1458574326956691537
- Announcements: 1458588765059678450
- Introductions: 1458578796650434581
- Help: 1458579492720349225
- Resources: 1458580158817763488
- Beginners: 1458589852088930499
- Projects: 1458579211890458666
- Events: 1458581968521269350
- Vibeworks Events: 1458828369767432283
- Past Events: 1458834454167683246
- Training Announcements: 1458828366055473276
- Moderator Only: 1458574326956691540
- Server Guide: 1458866927085818032

### Key Role IDs
- Admin: 1458575646530998302
- Moderator: 1458576572264222873
- Event Organizer: 1458828154432126977
- @everyone: 1458570944472813724

## Instructions

When this skill is invoked, help the user manage their Discord server using the available MCP tools.

### Available Commands

Parse the user's input to determine what action they want:

**Posting & Announcements:**
- `post <channel> <message>` - Send a message to a channel
- `announce <message>` - Post to announcements channel
- `event <title> <description> <date>` - Create an event announcement

**Moderation:**
- `moderate` or `review` - Fetch and review recent messages from general
- `timeout <user_id> <minutes> [reason]` - Timeout a user
- `kick <user_id> [reason]` - Kick a user
- `ban <user_id> [reason]` - Ban a user

**Server Info:**
- `status` or `stats` - Show server overview (channels, roles, members)
- `channels` - List all channels
- `roles` - List all roles
- `members` - List server members

**AutoMod:**
- `automod` - List current AutoMod rules
- `automod add keyword <words>` - Add keyword filter
- `automod toggle <rule_id>` - Enable/disable a rule

**Help:**
- `help` - Show this command list

### Response Format

When executing commands:
1. Confirm what action you're taking
2. Use the appropriate Discord MCP tool
3. Report the result back to the user

### Examples

User: `/discord announce Welcome to our first meetup!`
Action: Post "Welcome to our first meetup!" to the announcements channel using discord_send_message

User: `/discord event "January Meetup" "Join us at Vibeworks for hands-on Claude Code learning" "January 15th 6pm"`
Action: Create a formatted event embed in the events channel using discord_send_embed

User: `/discord moderate`
Action: Fetch recent messages from general using discord_fetch_messages and summarize any issues

User: `/discord status`
Action: Use discord_list_channels, discord_list_roles, discord_list_members to give an overview

### Default Behavior

If no command is specified (just `/discord`), show a menu:

```
Discord Server Management

What would you like to do?

Announcements
   - announce <message> - Post to announcements
   - event <title> - Create event post

Moderation
   - moderate - Review recent messages
   - timeout/kick/ban - User actions

Server Info
   - status - Server overview
   - channels/roles/members - List items

AutoMod
   - automod - View/manage rules

Type /discord help for full command list
```
