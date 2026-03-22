---
name: reflect
description: Reflect on the current session — what went well, what didn't, and any suggestions for improving the workflow or project infrastructure.
user-invocable: true
allowed-tools: Bash
argument-hint: [optional:topic]
---

# Session Reflection

Reflect on what has happened in this session so far. Be honest and specific.

If `$ARGUMENTS` is provided, focus your reflection on that topic. Otherwise, cover everything.

## Writing the reflection

Append the reflection to the file at `$REFLECTION_FILE_PATH` using a Bash command (e.g. `cat >> "$REFLECTION_FILE_PATH" <<'EOF' ...`).

If the write fails because the file doesn't exist, tell the user — the SessionStart hook may not have run.

The appended content must follow this structure:

```
---

## Reflection — {current time}

**Topic**: {$ARGUMENTS if provided, otherwise "General"}

### What went well
- Good decisions made.
- Problems solved efficiently.
- Tools that were properly used.

### What didn't go well
- Bad communication: unclear user messages, information that could have been shared at the start of the session.
- Obstacles hit, bad approaches taken, things that were harder than they should have been.
- Tooling that did not work as expected.

### Suggestions
**Be specific**: Reference file paths, agent names, or workflow steps.

Concrete changes to:
- Project infrastructure.
- Agent instructions.
- Skills.
- Conventions.
- Workflow that would prevent the problems above from recurring.
- Tooling that should be added to the Utilities Project that would help the implementer agent.
- Tooling that could be provided by MCP servers.
```

## Constraints

- Be honest — don't pad "what went well" to soften criticism.
- Be specific — vague observations like "things were slow" are useless. Say what was slow and why.
- Be actionable — every suggestion should be something that can actually be changed in a file or workflow step.
- Reflect from memory only — do not read files or explore the codebase to inform your reflection.
