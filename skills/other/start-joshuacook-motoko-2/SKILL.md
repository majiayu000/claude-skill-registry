---
name: start
description: Lean session start. Asks focus area first, then loads only relevant context. Use when "start" is said at session beginning.
allowed-tools: Read, Bash
---

# Start (Lean Session)

Minimal session start - ask focus first, load only relevant context.

## When to Activate

- User says: "start"
- Beginning of work session
- When you want focused context

## Flow

### 1. Ask Focus

Ask the user:
- What area are you working on? (creative, technical, content, strategy, system)
- What's the specific task?

### 2. Quick Context (Optional)

**Only if relevant to stated topic:**

If mentions "inbox" or "learning":
```bash
ls inbox/session-summaries/ 2>/dev/null
```

If mentions git:
```bash
git status -sb
```

Otherwise: skip context checks.

### 3. Load Relevant Role

Based on answer, read only the relevant role file from `roles/`.

### 4. Begin

```
[Role] here.

[1-2 sentence acknowledgment]

[First question or action]
```

## What NOT to Do

- Don't load ALL roles
- Don't run full context checks unless needed
- Don't greet with wall of text

## Comparison

- **start:** Lean, ask first, minimal context
- **help:** Deep assessment, suggest priorities

Use `start` for focused work without setup overhead.
