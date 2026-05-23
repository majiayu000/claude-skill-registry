---
name: context
updated: 2026-02-20
description: Context window conservation rules. Invoke when approaching context limits or before large tasks.
argument-hint: (no arguments)
allowed-tools: Read, Edit, Glob, Grep
---

# Context Conservation

Rules for maximizing work done per context window. Every token spent on exploration is a token not spent on implementation.

## Core Principles

1. **Grep first, read second** — never Read a file blind. Grep for the symbol/pattern, get line numbers, then Read with offset/limit.
2. **Narrow reads** — always use offset/limit. Aim for 10-20 lines around the target, not 100+.
3. **One read per edit** — Read the target lines, Edit them, move on. Don't re-read to verify; the Edit tool confirms success.
4. **Parallel independent calls** — if you need to read 3 files, do it in one message with 3 Read calls.
5. **No redundant searches** — if you already know the file and line from a prior Grep, go straight to Read+Edit.

## Tool Selection — Cheapest First

| Need | Use | NOT |
|------|-----|-----|
| Find a file by name | `Glob` | Explore agent, `find`, `ls -R` |
| Find a symbol in code | `Grep` (files_with_matches) | Explore agent, Read + scan |
| Read specific lines | `Read` (offset/limit) | `cat`, `head`, full-file Read |
| Simple edit | `Edit` | `sed`, `awk`, Write (full rewrite) |
| Repeated pattern edit | `Edit` with `replace_all: true` | Multiple individual Edits |

## When NOT to Use Agents

**Don't use Explore/Task agent when:**
- You know the file — just Grep + Read directly
- The search is simple — one Grep finds it
- You need < 3 lookups — do them yourself

**Do use Explore agent when:**
- Truly open-ended search across unknown files
- Need to understand an unfamiliar subsystem
- Would take 5+ Grep/Read rounds to find what you need

## When NOT to Invoke Skills

**Don't invoke a skill when:**
- The task is trivial (e.g., adding one translation key — just edit the files)
- You already know the pattern from memory/context
- The skill document is large and the task is small

**Do invoke a skill when:**
- Following a multi-step procedure with project-specific gotchas
- The task is complex enough that the skill's checklist prevents mistakes
- You genuinely don't remember the procedure

## Read Discipline

```
BAD:  Read(file, offset=1, limit=2000)     // entire file, huge context cost
BAD:  Read(file)                            // same — default reads everything
OK:   Read(file, offset=350, limit=50)      // 50 lines around target
GOOD: Read(file, offset=368, limit=5)       // just the lines you need
```

After a Grep gives line 370, read lines 368-373 (offset=368, limit=6). Not 300-450.

## Edit Discipline

- **Trust Edit output** — it confirms success. Don't Read after to verify.
- **`replace_all: true`** — for patterns repeated across a file (e.g., renaming a variable). One Edit, not N.
- **Include minimal context** — `old_string` just needs to be unique, not the whole function.

## Search Strategy

1. Start with `Grep(pattern, output_mode="files_with_matches")` — cheapest, just filenames
2. If needed, `Grep(pattern, output_mode="content", -n=true)` on the specific file — gives line numbers
3. Then `Read(file, offset=line-2, limit=10)` — surgical read
4. Edit and move on

## Multi-File Edits

For identical edits across multiple files:
1. Grep one file to find insertion point and context
2. Read the target lines from ALL files in parallel (one message, N Read calls)
3. Edit ALL files in parallel (one message, N Edit calls)

Total: 1 Grep + N Reads + N Edits. Not a skill invocation + exploration.

## Anti-Patterns

| Anti-pattern | Cost | Fix |
|---|---|---|
| Explore agent for known files | ~50K tokens | Direct Grep + Read |
| Full-file Read to find one function | ~5K tokens | Grep for function name first |
| Reading file before every Edit | 2x reads | Read once, Edit, trust output |
| Loading large skill for small task | ~3K tokens | Just do the task directly |
| Re-reading after successful Edit | Wasted read | Edit tool already confirms |
| Sequential reads that could be parallel | Wasted turns | Batch into one message |
