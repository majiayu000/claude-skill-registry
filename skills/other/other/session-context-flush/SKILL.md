---
name: vibe-session-context-flush
description: Performs smart context summarization when the context window is approaching capacity. Identifies what to keep, what to summarize, and creates a compact resume state.
user-invocable: true
---

# vibe-session-context-flush

Context windows have limits. This skill manages the transition gracefully instead of letting context degrade silently.

## When to Use This Skill

- You notice responses getting less coherent or losing track of earlier context
- You've been working for a long session with many file reads
- The system indicates context compression is occurring
- Before starting a new major subtask in a long session

## When NOT to Use This Skill

- Short sessions with plenty of context room
- When the user wants to continue without interruption
- When you just started the session

## Steps

1. **Assess current context** — What's consuming context?
   - Large file reads that are no longer relevant
   - Completed subtask details that can be summarized
   - Exploration results that led to dead ends
   - Verbose tool outputs

2. **Triage** into:
   - **Keep** — Still actively needed (current task state, open files, error messages)
   - **Summarize** — Completed work (compress to 2-3 sentences each)
   - **Drop** — No longer relevant (old file contents, superseded plans)

3. **Create compact state**:
   ```
   ## Session State (Flushed)
   **Current task**: [what we're doing]
   **Branch**: [current branch]
   **Modified files**: [list]
   **Completed**: [summary of done work]
   **Key decisions**: [1-liner each]
   **Next step**: [immediate next action]
   **Important context**: [anything that must be preserved]
   ```

4. **Offer to the user** — "Context is getting large. Here's a compact state. Want me to continue with this summary, or start a new session with the handover doc?"

## Output Format

### Context Flush Summary

**Context pressure**: High / Medium
**Items summarized**: X
**Items dropped**: Y

[Compact state block as above]

**Recommendation**: Continue with summary / Start new session with `/vibe-handover-doc`
