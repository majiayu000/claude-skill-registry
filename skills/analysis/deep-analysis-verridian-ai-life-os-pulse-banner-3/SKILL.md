---
name: Deep Analysis
description: Advanced problem-solving skill using sequential thinking. Use for complex architectural decisions, debugging hard problems, or planning.
---

# Deep Analysis Skill

This skill grants access to the `sequentialthinking` tool. Use this when you need to "break down" a problem before acting.

## When to use

- Debugging a complex race condition or "impossible" bug.
- Planning a large-scale refactor.
- Analyzing security implications of a change.
- When the user asks "What do you think?" or "Analyze this".

## Available Tools (Context Loaded)

- `mcp_sequential-thinking_sequentialthinking`: A tool that allows you to have an internal monologue/thought process. You can update your hypothesis, revise thoughts, and branch your thinking.

## Best Practices

1. **Don't rush**: Use multiple thought steps (`totalThoughts` > 5) for hard problems.
2. **Revise**: If a thought turns out to be wrong, use the `isRevision` flag to correct yourself.
3. **Hypothesis**: Always state a working hypothesis early in the thought chain.

## Example Workflow

1. User: "Why is the auth service crashing?"
2. Agent: Calls `sequentialthinking` with `thought="Initial hypothesis: DB connection pool exhaustion..."`.
3. Agent: Calls `sequentialthinking` with `thought="Checking logs..."` and `needsMoreThoughts=true`.
4. ... (After 5-10 thoughts) ...
5. Agent: "The issue is a deadlock in the transaction manager..."
