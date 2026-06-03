---
name: megg-state
description: Manage session state for cross-session handoff
user-invocable: true
arguments:
  - name: action
    description: clear | show (default captures state)
    required: false
---

# Session State Management

Capture or manage session state for cross-session handoff.

## Process

### Default (no argument) - Capture State

1. Review what was worked on in this session
2. Summarize into this format:

```markdown
## Working On
[One-liner: the main task/goal]

## Progress
- [What's been done]
- [Current status]

## Next
- [Immediate next steps]

## Context
[Relevant files, blockers, pending decisions - keep brief]
```

3. Call the `mcp__megg__state` tool with the content:
   ```
   mcp__megg__state({ content: "<formatted content>" })
   ```

4. Confirm to user that state was saved

### `clear` - Clear State

1. Call `mcp__megg__state({ status: "done" })`
2. Confirm state was cleared

### `show` - Display Current State

1. Call `mcp__megg__state()` with no arguments
2. Display the current state or "No active state"

## Notes

- State is ephemeral - overwritten each session
- Auto-expires after 48 hours or when marked done
- Hard limit of 2k tokens to prevent bloat
- Keep content concise and actionable
