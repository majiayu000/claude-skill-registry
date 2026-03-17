---
name: fizzy-workflow
description: |
  Use for guided Fizzy.do workflows: "set up Fizzy", "configure Fizzy for this project",
  "sync my work to Fizzy", "review my Fizzy progress", "end of session cleanup".
  Provides step-by-step guidance for common operations.
---

# Fizzy.do Guided Workflow Skill

Provides structured workflows for Fizzy.do task management. For direct operations, use the `fizzy-tasks` agent.

## Workflows

### Project Setup
**Triggers:** "set up Fizzy", "configure Fizzy for this project"

1. Check `.claude/fizzy_claude.json` for existing config
2. Verify FIZZY_TOKEN is available
3. List boards or create new one
4. Save configuration

### Sync Todos
**Triggers:** "sync my work", "sync todos to Fizzy"

1. Verify board is configured
2. Gather and summarize todos
3. Confirm card title
4. Execute `fizzy_sync_todos`

### Progress Review
**Triggers:** "review my progress", "show Fizzy status"

1. Load board config
2. Fetch and categorize cards
3. Present summary with step counts

### Session Cleanup
**Triggers:** "end of session", "wrap up"

1. Review current card from state
2. Confirm completion status
3. Close card if appropriate

## Configuration

| File | Contents |
|------|----------|
| `.claude/fizzy_claude.json` | `board_id`, `board_name` |
| `.claude/fizzy_state.json` | `card_number`, `card_title`, `step_map` |

## Related

- **Agent:** `fizzy-tasks` - Direct operations
- **Commands:** `/fizzy:configure`, `/fizzy:status`
