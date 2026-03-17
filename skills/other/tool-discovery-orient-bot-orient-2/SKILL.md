---
name: tool-discovery
description: Guide for discovering and using MCP tools via the discover_tools meta-tool. Use this skill when asked to perform tasks that require finding the right tools, when you see only discover_tools in your available tools, when asked "what tools are available", "find tools for X", or when planning multi-step workflows across Slack, WhatsApp, Google, or Slides.
---

# Tool Discovery System

This MCP server uses a **discovery-based tool loading pattern** to reduce context overhead. Instead of loading all 35+ tools upfront, only the `discover_tools` meta-tool is exposed. Use it to find and load the specific tools needed for your task.

## Quick Reference

```
# List all categories
discover_tools({ mode: "list_categories" })

# Browse tools in a category
discover_tools({ mode: "browse", category: "messaging" })

# Search by natural language
discover_tools({ mode: "search", query: "send slack message" })

# Search by intent
discover_tools({ mode: "search", intent: "check team blockers" })
```

## Tool Categories

| Category    | Tools | Use For                                  |
| ----------- | ----- | ---------------------------------------- |
| `messaging` | 4     | Slack DMs, channel messages, user lookup |
| `whatsapp`  | 8     | Message history, contacts, groups, media |
| `docs`      | 11    | Google Slides, Sheets, presentations     |
| `google`    | 8     | Calendar, Gmail, Tasks (OAuth)           |
| `apps`      | 5     | Mini-app creation and management         |
| `agents`    | 3     | Agent context and handoff                |
| `context`   | 2     | Context management                       |
| `media`     | 1     | Image/video generation                   |
| `system`    | 2     | Health check, configuration              |

## Workflow: Starting a Task

**Always discover tools before attempting to use them.**

1. Identify what you need to accomplish
2. Call `discover_tools` with appropriate mode
3. Review returned tool schemas
4. Execute the discovered tools

## Examples

### Example 1: Notify Team on Slack

**Task:** "Send a message to the team channel"

```
# Step 1: Find messaging tools
discover_tools({ mode: "search", query: "send slack channel message" })
# Returns: ai_first_slack_send_channel_message

# Step 2: Send the message
ai_first_slack_send_channel_message({ channel: "#orienter", message: "Quick update..." })
```

### Example 2: Find Upcoming Meetings

**Task:** "What meetings do I have this week?"

```
# Step 1: Find calendar tools
discover_tools({ mode: "browse", category: "google" })
# Returns: google_calendar_list_events

# Step 2: List events
google_calendar_list_events({ days: 7 })
```

### Example 3: Search WhatsApp History

**Task:** "Find messages about the project deadline"

```
# Step 1: Find WhatsApp tools
discover_tools({ mode: "browse", category: "whatsapp" })
# Returns: whatsapp_search_messages, whatsapp_get_conversation, etc.

# Step 2: Search messages
whatsapp_search_messages({ text: "project deadline" })
```

### Example 4: Update Presentation Text

**Task:** "Replace placeholders in the weekly slides"

```
# Step 1: Find Slides tools
discover_tools({ mode: "browse", category: "docs" })
# Returns: ai_first_slides_update_text

# Step 2: Update text placeholders
ai_first_slides_update_text({ presentationUrl: "...", replacements: [{ placeholder: "{{WEEK_ENDING}}", replacement: "Jan 26" }] })
```

## Search Tips

- **Exact tool names** get highest scores: `discover_tools({ query: "ai_first_slack_send_channel_message" })`
- **Keywords** work well: `"blocker"`, `"sprint"`, `"slack"`, `"whatsapp"`
- **Intent phrases** find related tools: `"notify team about progress"`
- **Use limit** to reduce results: `discover_tools({ mode: "search", query: "message", limit: 5 })`

## Common Tool Names

Quick reference for frequently used tools:

**Messaging (Slack):**

- `ai_first_slack_send_dm` - Direct message
- `ai_first_slack_send_channel_message` - Channel post
- `ai_first_slack_get_channel_messages` - Read channel history

**WhatsApp:**

- `whatsapp_search_messages` - Search message history
- `whatsapp_get_conversation` - Get chat with contact
- `whatsapp_list_groups` - List groups
