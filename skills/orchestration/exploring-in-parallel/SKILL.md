---
name: exploring-in-parallel
description: Parallelizes codebase exploration and research by launching multiple subagents simultaneously. Use when exploring codebases, researching questions, investigating bugs, gathering context from multiple sources, or any task requiring search across multiple files, patterns, or directories. Triggers on research, exploration, debugging, "why does this happen", "how does X work", or multi-file investigation.
user_invocable: true
---

# Exploring in Parallel

## Overview

**Parallelize exploration aggressively.** When researching or exploring, launch multiple subagents simultaneously instead of sequential searches. This reduces wall-clock time proportionally to the number of parallel agents.

## How to Parallelize

Use the `Task` tool with `subagent_type=Explore`. The key is to **send multiple Task calls in a single message** — this launches them concurrently.

Each subagent gets:
- `subagent_type`: `"Explore"` for codebase searches, `"general-purpose"` for web research
- `description`: Short label (3-5 words)
- `prompt`: Detailed, self-contained search instructions

**Example — investigating how auth works:**

Send in ONE message:
```
Task 1: { subagent_type: "Explore", description: "Find auth middleware", prompt: "Search for authentication middleware, auth guards, session validation..." }
Task 2: { subagent_type: "Explore", description: "Find login endpoints", prompt: "Search for login routes, /auth endpoints, credential handling..." }
Task 3: { subagent_type: "Explore", description: "Find auth config", prompt: "Search for JWT config, OAuth settings, auth environment variables..." }
```

All three run simultaneously. When results return, **synthesize** findings into a coherent answer.

## When to Parallelize

| Situation | Action |
|-----------|--------|
| Searching for multiple patterns | One subagent per pattern |
| Exploring different directories | One subagent per area |
| Investigating related questions | One subagent per question |
| Checking multiple files (>3) | Parallel reads |
| Web research on multiple topics | One subagent per topic |

## When NOT to Parallelize

- **Dependent searches**: Second search needs results from first
- **Single specific file**: Just use `Read` directly
- **Simple grep**: One pattern, one location — use `Grep` directly
- **Known target**: Know exact file/function — use `Glob`/`Read` directly

## Red Flags — STOP and Parallelize

| Thought | Action |
|---------|--------|
| "Let me search for X first, then Y" | Launch both simultaneously |
| "I'll check this file, then that one" | Parallel reads if >3 files |
| "First explore area A, then B" | Parallel subagents per area |
| "Let me see what this returns before..." | Usually can parallelize anyway |

## After Results Return

Don't just dump raw results. **Synthesize:**
1. Identify overlapping findings across agents
2. Resolve contradictions
3. Present a unified answer with file references
4. Note any gaps that need follow-up
