---
name: recap
description: Get session recap including preferences, recent context, and active goals. Use at the start of a session or when context seems lost.
---

# Session Recap

Retrieve the current session context from Mira including user preferences, recent decisions, and active goals.

## Instructions

1. Use the `mcp__mira__session` tool with `action="recap"`
2. Present the recap in a clear, organized format:
   - **Preferences**: User coding style, tool preferences
   - **Recent Context**: What was worked on recently
   - **Active Goals**: In-progress goals with milestones
3. Highlight any blocked or high-priority items
4. If no recap is available, suggest using `memory(action="remember")` to store context

## When to Use

- Starting a new session
- Resuming after a break
- When context about previous work is needed
- User asks "what were we working on?"
