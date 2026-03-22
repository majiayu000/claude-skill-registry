---
name: learned
description: Log a learning, discovery, or decision to the vault with full context from the current conversation.
user-invocable: true
argument-hint: "<what you learned> [--type correction|decision|discovery|pattern|gotcha]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Learned — Explicit Knowledge Capture

Log something you or the user discovered during the current conversation to the vault. This is for learnings that hooks can't auto-detect — debugging insights, root cause discoveries, architecture gotchas, performance findings, etc.

## When to use

- After debugging a tricky bug (log the root cause + fix)
- When the user shares project knowledge that isn't in code
- After discovering a non-obvious behavior or gotcha
- When making an architecture decision with rationale
- When a pattern emerges across multiple interactions

## Steps

1. **Parse the argument** — extract what was learned and the type. Default type is `discovery`.

2. **Determine metadata** from conversation context:
   - Which project does this relate to? (check `vault/shared/project-knowledge/` for registered projects, or `general`)
   - What area? (`architecture`, `debugging`, `deployment`, `api`, `database`, `tooling`, `workflow`, etc.)
   - Severity/priority: `high` if it caused a bug or could cause one again, `medium` for useful knowledge, `low` for nice-to-know

3. **Check for duplicates** — search `vault/learnings/` for similar entries. If one exists, update its `recurrence-count` and `last-seen` instead of creating a new file.

4. **Write the vault entry** to `vault/learnings/<TYPE>-<YYYYMMDD>-<SEQ>.md`:

```markdown
---
id: <TYPE>-<YYYYMMDD>-<SEQ>
logged: <ISO timestamp>
type: learning
priority: <high|medium|low>
status: new
category: <type from arg>
area: <determined from context>
agent: main
project: <determined from context>
pattern-key: <short kebab-case key for dedup>
recurrence-count: 1
first-seen: <YYYY-MM-DD>
last-seen: <YYYY-MM-DD>
tags: [<relevant tags>]
related: [<wikilinks to related entries if any>]
---

# <Concise title>

## What happened
<Brief description of the situation/context>

## What was learned
<The actual insight — be specific and actionable>

## Why it matters
<How this prevents future issues or improves workflow>

## Evidence
<Link to file, line number, error message, or conversation context>
```

5. **Confirm** — tell the user what was logged and the file path.

## Type reference

| Type | Prefix | Use for |
|------|--------|---------|
| `correction` | LRN | User corrected Claude's approach |
| `decision` | LRN | Architecture or design choice with rationale |
| `discovery` | LRN | Found something non-obvious while working |
| `pattern` | LRN | Recurring theme across interactions |
| `gotcha` | ERR | Something that fails silently or is easy to get wrong |

## Important

- Be specific — "SQLite WAL mode is fast enough" is better than "database works well"
- Include file paths and line numbers as evidence when applicable
- Don't log trivial things — if it's obvious from reading the code, skip it
- Fill in ALL fields — no placeholders. This is the whole point of this skill vs auto-hooks.
