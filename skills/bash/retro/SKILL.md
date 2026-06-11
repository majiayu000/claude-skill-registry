---
name: retro
description: "Learning system interface: stats, search, graduate learnings. Backed by learning.db (SQLite + FTS5)."
user-invocable: true
argument-hint: "[status|list|search <term>|graduate]"
allowed-tools:
  - Bash
  - Read
  - Edit
  - Grep
  - Glob
routing:
  triggers:
    - "retro stats"
    - "list learnings"
    - "graduate knowledge"
    - "learning stats"
    - "search learnings"
  category: meta-tooling
  pairs_with:
    - learn
    - auto-dream
---

# Retro Knowledge Skill

## Overview

This skill wraps `scripts/learning-db.py` into a user-friendly interface for the learning system. The learning database is the single source of truth—all queries go through the Python CLI, never maintaining a parallel file store.

---

## Instructions

Parse the user's argument to determine the subcommand. Default to `status` if no argument given.

| Argument | Subcommand |
|----------|------------|
| (none), status | **status** |
| list | **list** |
| search TERM | **search** |
| graduate | **graduate** |
| what-didnt-work | **what-didnt-work** |

### Subcommand: status

**Key constraint**: Always present results in readable tables/sections, not raw JSON. When showing stats, suggest next actions (search, graduate).

Show learning system health summary.

**Step 1**: Get stats.

```bash
python3 ~/.claude/scripts/learning-db.py stats
```

**Step 2**: Present status report.

```
LEARNING SYSTEM STATUS
======================

Entries:     [total] ([high-conf] high confidence)
Categories:  [breakdown by category]
Graduated:   [N] entries embedded in agents/skills

Injection:
  Hook: session-context.py (SessionStart, ADR-147 dream system)
  Method: pre-built payload from nightly auto-dream cycle + learning.db high-confidence patterns

Next actions:
  /retro list              — see all entries
  /retro search TERM       — find specific knowledge
  /retro graduate          — embed mature entries into agents
```

### Subcommand: list

Display all accumulated knowledge.

**Key constraint**: Output must use the Python CLI as the single source of truth. Do not maintain parallel markdown files. Present results in readable grouped format, not raw JSON.

**Step 1**: Query all entries.

```bash
python3 ~/.claude/scripts/learning-db.py query
```

**Step 2**: Present grouped by category:

```
LEARNING DATABASE
=================

## [Category] ([N] entries)
- [topic/key] (conf: [N], [Nx] observations): [first line of value]
...
```

Optional flags:
- `--category design` — filter to one category
- `--min-confidence 0.7` — only high-confidence entries

### Subcommand: search

Full-text search across all learnings.

**Step 1**: Run FTS5 search.

```bash
python3 ~/.claude/scripts/learning-db.py search "TERM"
```

**Step 2**: Present results ranked by relevance:

```
SEARCH: "TERM"
==============

[N] results:

1. [topic/key] (conf: [N], category: [cat])
   [value excerpt]

2. ...
```

### Subcommand: graduate

Evaluate learning.db entries and embed mature ones into agents/skills.

**Key constraints:**
- Only graduate entries that encode non-obvious, actionable knowledge—never generic advice.
- Always present proposals and wait for user approval before editing agent/skill files.
- Do not auto-graduate without explicit user approval (even with `--auto` flag, confirm intent).
- Skip categories `error` and `effectiveness`—those are injection-only (useful in context but not suitable as permanent agent instructions).

**Step 1**: Get graduation candidates from the DB.

```bash
python3 ~/.claude/scripts/learning-db.py query --category design --category gotcha
```

**Step 2**: For each entry, evaluate graduation readiness.

For each candidate, the LLM:
- Reads the learning value
- Searches the repo for the target file (grep for related keywords)
- Determines edit type: add failure mode, add to operator context, add warning, or "not ready / keep injecting"
- Checks if the target already contains equivalent guidance (use Grep to verify before proposing)

| Question | Pass | Fail |
|----------|------|------|
| Is this specific and actionable? | "sync.Mutex for multi-field state machines" | "Use proper concurrency" |
| Is this universally applicable? | Applies across the domain | Only applied in one feature |
| Would it be wrong as a prescriptive rule? | Safe as default | Has important exceptions |
| Does the target already contain this? | Not present | Already equivalent |

**Step 3**: Present graduation plan to user.

```
GRADUATION CANDIDATES (N of M entries)

1. [topic/key] → [target file] (add anti-pattern)
   Proposed: "### AP-N: [title]\n[description]"

ALREADY APPLIED (N entries — mark graduated only)
- [topic/key] — already in [file]

NOT READY (N entries — keep injecting)
- [topic/key] — [reason]

Approve? (y/n/pick numbers)
```

**Step 4**: On user approval, apply changes.

Use the Edit tool to insert graduated content into target agent/skill files.

After embedding, mark the entry as graduated:

```bash
python3 ~/.claude/scripts/learning-db.py graduate TOPIC KEY "target:file/path"
```

Graduated entries stop being injected (the injector filters `graduated_to IS NULL`).

**Step 5**: Report.

```
GRADUATED:
  [key] → [target file] (section: [section])

Entries marked. They will no longer be injected via the hook
since they are now part of the agent's permanent knowledge.
```

### Subcommand: what-didnt-work

Print the negative-results registry, the list of experiments that lost. Read it before re-running an experiment so a known-dead path is not retried.

The registry is a doc, not a DB table: `docs/what-didnt-work.md` is capture, store, and query target. This subcommand reads and prints it, then offers an optional one-line mirror into learning.db for FTS search.

**Step 1**: Read and print the registry.

Use the Read tool on `docs/what-didnt-work.md` and present it. Group by the dated `## YYYY-MM-DD` headings; show each entry's Decision verdict (rejected / deferred / revisit-if) up front so a scan answers "did we already reject this?".

```
NEGATIVE RESULTS (docs/what-didnt-work.md)
==========================================

## [date] [experiment]
  Decision: [rejected | deferred | revisit-if <condition>]
  What happened: [one line]
...
```

If the file is missing, report that no negative results are recorded yet and point the user at the format in `CONTRIBUTING.md`.

**Step 2** (optional): Mirror one line into learning.db for full-text search.

The doc stays canonical. The mirror is one pointer row, not a parallel store. Run only when the user wants the entry FTS-searchable via `/retro search`:

```bash
python3 ~/.claude/scripts/learning-db.py learn --topic negative-results \
  "YYYY-MM-DD <experiment>: <decision> - see docs/what-didnt-work.md"
```

This reuses the existing `learn` command (no new code). Confirm with either:

```bash
# Topic listing (exact, includes the hyphen):
python3 ~/.claude/scripts/learning-db.py query --topic negative-results
# Or FTS (use a space, not the hyphen; the tokenizer splits hyphens):
python3 ~/.claude/scripts/learning-db.py search "negative results"
```

---

## Examples

### Example 1: Quick health check
User says: "/retro"
Actions: Run `learning-db.py stats`, show entry counts, injection health.

### Example 2: See what we know
User says: "/retro list"
Actions: Run `learning-db.py query`, display grouped by category.

### Example 3: Search for specific knowledge
User says: "/retro search routing"
Actions: Run `learning-db.py search "routing"`, display ranked results.

### Example 4: Graduate mature knowledge
User says: "/retro graduate"
Actions: Query design/gotcha entries, evaluate each against graduation criteria, propose edits to target agents/skills, apply approved changes, mark graduated.

---

## Error Handling

### Error: "learning.db not found"
Cause: Database not initialized yet
Solution: Report that no learnings exist yet. Hooks auto-populate during normal work.

### Error: "No graduation candidates"
Cause: No design/gotcha entries, or all already graduated
Solution: Report the stats and suggest recording more learnings via normal work.

### Common Mistakes During Graduation
- **Graduating generic advice** (e.g., "use proper error handling"): Creates noise. Agents already know general patterns. Only graduate specific, actionable findings that encode something non-obvious.
- **Proposing without target verification**: Always grep the target file for equivalent guidance before proposing. Duplication creates maintenance burden.
- **Proceeding without explicit user approval**: Graduation permanently changes agent behavior. Always present proposals in Step 3 and wait for explicit approval before applying changes in Step 4.

---

## References

- `~/.claude/scripts/learning-db.py` — Python CLI for all database operations
- `hooks/session-context.py` — Hook that injects the pre-built dream payload and high-confidence patterns at session start (ADR-147, supersedes retro-knowledge-injector.py)
- `scripts/learning.db` — SQLite database with FTS5 search index
- `docs/what-didnt-work.md`: Negative-results registry. Printed by the `what-didnt-work` subcommand; the doc is the canonical store.
