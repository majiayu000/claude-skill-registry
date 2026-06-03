---
name: megg-learn
description: Capture a learning to megg knowledge
user-invocable: true
arguments:
  - name: what
    description: What to capture (optional - will ask if not provided)
    required: false
---

# Capture Learning

User wants to save something to megg knowledge.

## Process

1. If argument provided, use it as the learning content
2. If no argument, ask: "What should we capture?"
3. Determine the appropriate entry type:
   - **decision**: Architectural or design choice made
   - **pattern**: How we do things here (reusable approach)
   - **gotcha**: Trap to avoid, something that caught us
   - **context**: Background info, not actionable
4. Extract or ask for relevant topics (tags for categorization)
5. Use the `mcp__megg__learn` tool to save

## Example

User: `/megg-learn always use absolute paths in hooks`

→ Capture as **pattern** with topics like `hooks`, `paths`

## Important

- Keep entries concise and actionable
- Topics should be 1-3 words each
- Title should be short (5-10 words max)
- Content can include examples or context
