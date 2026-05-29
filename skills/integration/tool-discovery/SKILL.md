---
name: tool-discovery
description: Guide for discovering and using MCP tools via the discover_tools meta-tool. Use this skill when asked to perform tasks that require finding the right tools, when you see only discover_tools in your available tools, when asked "what tools are available", "find tools for X", or when planning multi-step workflows across JIRA, Slack, WhatsApp, or Google Docs.
---

# Tool Discovery System

This MCP server uses a **discovery-based tool loading pattern** to reduce context overhead. Instead of loading all 35+ tools upfront, only the `discover_tools` meta-tool is exposed. Use it to find and load the specific tools needed for your task.

## Quick Reference

```
# List all categories
discover_tools({ mode: "list_categories" })

# Browse tools in a category
discover_tools({ mode: "browse", category: "jira" })

# Search by natural language
discover_tools({ mode: "search", query: "send slack message" })

# Search by intent
discover_tools({ mode: "search", intent: "check team blockers" })
```

## Tool Categories

| Category    | Tools | Use For                                          |
| ----------- | ----- | ------------------------------------------------ |
| `jira`      | 14    | Issues, sprints, blockers, SLA, weekly summaries |
| `messaging` | 4     | Slack DMs, channel messages, user lookup         |
| `whatsapp`  | 8     | Message history, contacts, groups, media         |
| `docs`      | 11    | Google Slides, Sheets, presentations             |
| `system`    | 2     | Health check, configuration                      |

## Workflow: Starting a Task

**Always discover tools before attempting to use them.**

1. Identify what you need to accomplish
2. Call `discover_tools` with appropriate mode
3. Review returned tool schemas
4. Execute the discovered tools

## Examples

### Example 1: Check Team Status

**Task:** "What are the blockers for the team?"

```
# Step 1: Find blocker-related tools
discover_tools({ mode: "search", query: "blockers" })
# Returns: ai_first_get_blockers

# Step 2: Use the discovered tool
ai_first_get_blockers({})
```

### Example 2: Weekly Summary

**Task:** "Give me a weekly summary of the team's progress"

```
# Step 1: Find weekly summary tools
discover_tools({ mode: "browse", category: "jira" })
# Returns: ai_first_get_weekly_summary, ai_first_get_completed_this_week, etc.

# Step 2: Get the summary
ai_first_get_weekly_summary({})
```

### Example 3: Notify Team on Slack

**Task:** "Send a message to the team channel about blockers"

```
# Step 1: Find messaging and blocker tools
discover_tools({ mode: "search", query: "send slack channel message" })
discover_tools({ mode: "search", query: "blockers" })

# Step 2: Get blockers and send message
ai_first_get_blockers({})
ai_first_slack_send_channel_message({ channel: "#orienter", message: "Current blockers: ..." })
```

### Example 4: Search WhatsApp History

**Task:** "Find messages about the project deadline"

```
# Step 1: Find WhatsApp tools
discover_tools({ mode: "browse", category: "whatsapp" })
# Returns: whatsapp_search_messages, whatsapp_get_conversation, etc.

# Step 2: Search messages
whatsapp_search_messages({ text: "project deadline" })
```

### Example 5: Update Presentation

**Task:** "Update the weekly presentation with completed JIRA issues"

```
# Step 1: Discover needed tools across categories
discover_tools({ mode: "browse", category: "jira" })   # For completed issues
discover_tools({ mode: "browse", category: "docs" })   # For slides

# Step 2: Execute workflow
ai_first_get_completed_this_week({})
ai_first_slides_update_weekly({ presentationUrl: "..." })
```

## Search Tips

- **Exact tool names** get highest scores: `discover_tools({ query: "ai_first_get_blockers" })`
- **Keywords** work well: `"blocker"`, `"sprint"`, `"slack"`, `"whatsapp"`
- **Intent phrases** find related tools: `"notify team about progress"`
- **Use limit** to reduce results: `discover_tools({ mode: "search", query: "message", limit: 5 })`

## Common Tool Names

Quick reference for frequently used tools:

**JIRA:**

- `ai_first_get_in_progress` - Current work
- `ai_first_get_blockers` - Blocked issues
- `ai_first_get_daily_digest` - Today's summary
- `ai_first_get_weekly_summary` - Week overview

**Messaging (Slack):**

- `ai_first_slack_send_dm` - Direct message
- `ai_first_slack_send_channel_message` - Channel post
- `ai_first_slack_get_channel_messages` - Read channel history

**WhatsApp:**

- `whatsapp_search_messages` - Search message history
- `whatsapp_get_conversation` - Get chat with contact
- `whatsapp_list_groups` - List groups
