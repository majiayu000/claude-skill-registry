---
name: shipflow-context
description: Prime context for a task — calls context_continue + context_retrieve to find relevant files before starting work. Minimizes token usage by reusing cached context and only reading what's needed.
argument-hint: <what you want to do>
---

## Context

- Current directory: !`pwd`
- Project name: !`basename $(pwd)`

## Your task

Prime the session context before starting work. This avoids wasting tokens on broad file exploration.

### Step 1 — Check session memory

Call `context_continue` with the user's task as the query (`$ARGUMENTS`).

Read the response carefully:
- **Files already in memory**: do NOT re-read these — use their previews
- **Decisions already stored**: incorporate these into your plan
- **Budget remaining**: note how much read budget is left this turn

### Step 2 — Retrieve relevant files

If `context_continue` shows no prior memory OR the task needs more files, call `context_retrieve` with `$ARGUMENTS` as the query.

Read the ranked file list. Pick the top 3-5 most relevant files only.

### Step 3 — Read only what you need

For each file you actually need to understand:
- Use `context_read` with the query set to `$ARGUMENTS` (enables smart excerpting)
- Skip files where the `context_continue` preview is already sufficient
- Stop reading when budget drops below 4,000 chars

### Step 4 — Report and plan

Output a concise summary:
```
## Ready to work on: [task]

**Files in context:**
- [file] — [one line on what's relevant]

**Key constraints/decisions:**
- [any stored decisions relevant to this task]

**Plan:**
1. [step]
2. [step]

**Budget used:** X / 18,000 chars
```

Then ask: "Shall I proceed?"

### Rules

- Do NOT read files not returned by `context_retrieve` or `context_continue`
- Do NOT do Glob/Grep before Steps 1 and 2
- Do NOT read more than 5 files in this priming phase
- If the task mentions a specific file path, add it to the read list regardless of retrieve results
- If `$ARGUMENTS` is empty, ask the user: "What do you want to work on?" before proceeding
