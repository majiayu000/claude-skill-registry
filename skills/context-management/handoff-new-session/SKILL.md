---
name: handoff-new-session
description: Use when ending a session and want to spawn a continuation session in agent-deck with inline context
---

# Handoff to New Session

Spawn a continuation session in agent-deck with your current context inline.

## When to Use

- End of work session when you want immediate continuation
- Handing off to a parallel agent
- Before context gets too full and you want a fresh session

## Process

1. **Gather context** from the current conversation:
   - What task are you working on?
   - What's been completed?
   - What are the next steps?

2. **Call the MCP tool**:
   ```
   spawn_continuation_session({
     task: "Brief description of current work"
   })
   ```

3. **Report to user**:
   - Session name created
   - How to attach: `agent-deck` then select session, or run in background

## Output

Tell the user:
- The session name (e.g., `auth-refactor-abc12`)
- The handoff ID for reference
- How to attach: launch `agent-deck` TUI and select the session

## Example

User: "I need to stop here, can you hand this off?"

You:
1. Summarize current task from conversation
2. Call `spawn_continuation_session({ task: "Implementing OAuth login flow" })`
3. Report: "Created session `oauth-login-xyz89`. Run `agent-deck` and select it to continue."

## Notes

- The new session gets **inline context** - it can start working immediately
- If claude-mem is running, uses its summary (already synthesized by Haiku)
- Falls back to rolling checkpoint data if claude-mem unavailable
- Handoff is persisted for 7 days in case you need to reference it
