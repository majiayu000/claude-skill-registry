---
name: subagent-patterns
description: >
  Patterns for when and how to use Claude Code subagents via the Agent tool.
  Use when the user needs to delegate research, run parallel investigations,
  protect the main context window, or asks about subagent types like Explore or Plan.
---

# Subagent Patterns

Subagents are independent Claude instances launched via the Agent tool. They run in isolation, protecting the main context window from excessive results while enabling parallel work.

## When to Use
- User needs deep research into a codebase area without polluting main context
- Multiple independent investigations can run in parallel
- User asks about the Agent tool or subagent types
- Task requires exploring unfamiliar code before making changes
- User wants to delegate a subtask to a focused agent

## Core Patterns

### When to Use Subagents vs Direct Tools

Use subagents when:
- The search may require multiple rounds of exploration (3+ queries)
- Results would be too large for the main context
- Multiple independent tasks can run in parallel
- You need focused analysis that should not clutter the conversation

Use direct tools (Glob, Grep, Read) when:
- You know exactly what file or function to find
- A single search query will suffice
- The result is small and immediately actionable

### Subagent Types

**Explore** — For broad codebase exploration and deep research:

```
Agent tool call:
  subagent_type: "Explore"
  prompt: "Find all authentication middleware in this project.
           Identify where JWT tokens are validated, what claims
           are checked, and how unauthorized requests are handled.
           Report file paths and key function signatures."
```

Use Explore when you need to understand how a system works before modifying it.

**Plan** — For generating structured implementation plans:

```
Agent tool call:
  subagent_type: "Plan"
  prompt: "Create a plan for adding rate limiting to all API endpoints.
           Consider existing middleware, database requirements,
           and configuration needs. Output a step-by-step plan
           with file paths and code changes needed."
```

**General-purpose** (default) — For executing focused subtasks:

```
Agent tool call:
  prompt: "Read the file src/utils/validation.ts and extract
           all exported function signatures with their parameter
           types and return types. Format as a markdown table."
```

### Result Handling

Subagents return their findings as text. Structure your prompts to get actionable output:

```
Agent tool call:
  prompt: "Analyze src/api/routes/ for error handling patterns.
           For each route file, report:
           1. File path
           2. Whether it uses try/catch
           3. Whether errors are logged
           4. Whether error responses include status codes
           Format as a checklist with pass/fail for each item."
```

The main agent receives a summary and acts on it — the subagent's full exploration context is discarded, keeping the main window clean.

### Parallel Subagent Launches

Launch multiple Agent calls in a single response for independent tasks:

```
# Call 1 - Agent tool:
  prompt: "Find all database query functions in src/db/ and check
           if they use parameterized queries for SQL injection prevention."

# Call 2 - Agent tool:
  prompt: "List all API endpoints in src/routes/ and check which ones
           have authentication middleware applied."

# Call 3 - Agent tool:
  prompt: "Find all environment variable usages across the codebase
           and verify each has a fallback or validation check."
```

All three run in parallel. Results arrive independently and can be synthesized by the main agent.

### Scoping Subagent Work

Give subagents clear boundaries to prevent unbounded exploration:

```
# GOOD: Scoped prompt
Agent tool call:
  prompt: "In the directory src/components/forms/, find all form
           components that handle file uploads. Report the component
           name, accepted file types, and max size limits."

# BAD: Unbounded prompt
Agent tool call:
  prompt: "Look at all the components and tell me about them."
```

### Protecting Context Window

Use subagents as a firewall when reading large codebases:

```
# Instead of reading 20 files directly:
Agent tool call:
  subagent_type: "Explore"
  prompt: "Read all files in src/services/ (there are ~20 files).
           Summarize each service: name, purpose, dependencies,
           and exported functions. Return a concise summary table."
```

The subagent reads all 20 files in its own context. The main agent receives only the summary.

## Anti-Patterns

- **Using subagents for simple lookups**: If you know the file path, use Read directly. Launching a subagent to read one file wastes resources.
- **Duplicating subagent work**: If you delegate research to a subagent, do not also perform the same searches yourself. Trust the subagent result.
- **Vague prompts**: "Look into the auth system" produces unfocused results. Be specific about what information you need and what format to return it in.
- **Excessive subagent use**: Not every task needs a subagent. Direct tool calls are faster for simple, directed operations. Only use subagents when the task genuinely benefits from isolation or parallelism.
- **Ignoring subagent findings**: If a subagent reports an issue (security flaw, missing error handling), act on it. Do not discard the result.

## Quick Reference

| Scenario | Approach |
|----------|----------|
| Know the exact file | Read directly |
| Single grep/glob | Grep/Glob directly |
| Multi-file exploration | Subagent (Explore) |
| Implementation planning | Subagent (Plan) |
| Parallel investigations | Multiple Agent calls |
| Large result expected | Subagent (context protection) |

**Prompt structure**: State the scope, what to find, and desired output format.
**Parallelism**: Independent Agent calls in the same response run concurrently.
**Context protection**: Subagent results are summarized; raw exploration stays isolated.
