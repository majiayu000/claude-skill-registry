---
name: tycana
description: Persistent task management and productivity intelligence via MCP. Captures tasks from conversation, plans your day, tracks patterns, and gives personalized recommendations that improve over time.
requires:
  mcp: [tycana]
category: project-management
---

# Tycana Productivity

Tycana gives Claude persistent memory about your work across conversations. Connect once via MCP, and every session includes your tasks, projects, deadlines, blockers, and computed intelligence from your patterns.

**Homepage**: [tycana.com](https://www.tycana.com)
**Getting started**: [tycana.com/getting-started](https://www.tycana.com/getting-started/)

## Prerequisites

- Tycana MCP server connected at `https://app.tycana.com/mcp` (OAuth 2.1)
- Or install the Tycana Claude plugin: `/plugin install tycana`

## Available Tools

| Tool | Purpose |
|------|---------|
| `capture` | Create tasks from conversation context |
| `complete` | Mark items done with outcome and notes |
| `plan_day` | Generate prioritized daily plan |
| `what_next` | Energy-aware next action recommendation |
| `review` | Progress summary with pattern analysis |
| `get_context` | Load current work context |
| `search` | Find items by keyword or filter |
| `list_items` | List items with status/project filters |
| `get_item` | Get full detail on a specific item |
| `update_item` | Modify item properties |
| `relate_items` | Create blocking/dependency relationships |
| `remember` | Store personal preferences and constraints |
| `cleanup_project` | Archive completed items in a project |
| `delete_item` | Remove an item |

## Example Prompts

```
"Plan my day"
"Remind me to update the deployment docs before Friday"
"What should I work on next? I have about an hour and low energy"
"How's the infrastructure project going?"
"Review my week"
"Brain dump — I've got a bunch of things rattling around"
```

## Key Features

- **Capture from conversation** — mention something you need to do and it's captured with effort, energy, and project inferred from context
- **Computed intelligence** — velocity tracking, slip detection, effort calibration that improves over time
- **Energy-aware recommendations** — factors in your current energy level for task suggestions
- **Project graph** — items connect via blocking chains and dependencies, not flat lists
