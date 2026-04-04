---
name: notepad-system
description: Use this skill when context compression is imminent, when resuming a session, or when preserving critical decisions across long tasks. Provides a durable notepad that survives compaction and lets any agent pick up exactly where the previous context left off.
---

# Notepad System — Compaction-Resistant State Preservation

Structured storage for decisions, task state, and critical context that must survive
context window compression. Extends pre-compact-state.md from manual discipline to
a concrete file-based protocol.

## The Problem

When context compresses, the following is lost:
- Why a specific approach was chosen over alternatives
- Which files were edited and what changed
- Where in a multi-step task execution was paused
- Constraints and requirements the user stated earlier in the session

Without this, the recovered context either restarts from scratch or makes assumptions
that contradict earlier decisions.

---

## Note Types

| Type | Persistence | When to Use |
|------|-------------|-------------|
| **Priority** | Permanent until explicitly deleted | Architectural decisions, user confirmed preferences, hard constraints |
| **Working** | Session-scoped, cleared at session end | Current task state, WIP progress, in-flight findings |
| **Scratch** | Cleared after use (one-time calc) | Quick calculations, temp values used once |

---

## Storage Location

```
~/.claude/projects/<project-hash>/notepad.md
```

The project hash is derived from the working directory path.
If the directory does not exist, create it before writing.

### File Format

```markdown
# Notepad

## Priority Notes

### [2026-03-29 14:22] Decision: Auth approach
JWT with refresh tokens. User confirmed.
Reason: Stateless, scalable, mobile-friendly.
Rejected: Session-based (server state, scaling issues).

### [2026-03-29 15:10] Constraint: Node version
Must stay on Node 18. Server has LTS pinned, no upgrade path in scope.

## Working Notes

### [2026-03-29 14:45] Task: API refactor — Phase 2
Completed: /users, /products, /categories endpoints
Remaining: /orders, /payments endpoints
Blocked on: Stripe webhook secret (user to provide)
Next action: Start /orders, skip payment until secret arrives

## Scratch

### [2026-03-29 15:30] Token estimate
Average response: 256 tokens. 4x safety margin = ~1024 tokens per request budget.
USED — safe to delete.
```

---

## Pre-Compact Protocol

When context compression is imminent (context window at ~80% or system warning appears):

**Step 1 — Dump active task state to Working Notes**
```
What task is in progress?
What has been completed so far?
What remains?
Are there any blockers?
What is the immediate next action when context resumes?
```

**Step 2 — Promote any pending decisions to Priority Notes**
```
Any architectural choice made this session → Priority Note
Any user-confirmed preference → Priority Note
Any external constraint discovered → Priority Note
```

**Step 3 — Record modified files**
```
List every file touched this session.
Note what changed in each (one line per file is enough).
Note whether changes are committed or uncommitted.
```

**Step 4 — Save pending decisions with their options**
```
If a decision was not yet made, record the question and the options.
This prevents re-deriving the same options after compression.
```

Do this BEFORE continuing work. State preservation takes priority.

---

## Post-Compact Recovery

When a new or compressed context begins:

**Step 1 — Read notepad.md**
```
Path: ~/.claude/projects/<project-hash>/notepad.md
```

**Step 2 — Inject Priority Notes into active context**
These are always relevant. Treat them as if the user stated them at session start.

**Step 3 — Summarize Working Notes for the user**
```
"Resuming: API refactor, Phase 2.
Completed: /users, /products, /categories.
Remaining: /orders, /payments.
Blocked: Stripe webhook secret needed.
Next: starting /orders."
```

**Step 4 — Clear Scratch notes**
They were single-use. Remove them now.

**Step 5 — Resume from last known state**
Do not ask the user to re-explain context that is in Working Notes.

---

## Note Writing Rules

- Priority notes require explicit deletion: `notepad delete priority <title>`
- Working notes are cleared at the end of each session (or when the task completes)
- Never store code in notes — reference `file.ts:line` instead
- Keep each note to 3 lines maximum (reference files for detail)
- Always include a timestamp in the note header
- Never duplicate information already in CLAUDE.md or memory — cross-reference instead

---

## CLI Operations (manual use)

Read the notepad:
```bash
cat ~/.claude/projects/<hash>/notepad.md
```

Clear working notes (session end):
```bash
# Remove the Working Notes section content, keep the headers
```

Clear scratch notes (after use):
```bash
# Remove individual scratch entries after they have been applied
```

---

## Integration

**pre-compact-state.md** — This skill is the concrete implementation of that rule.
The rule defines what to save; this skill defines where, how, and in what format.

**compass agent** — The compass agent performs context recovery. It should read
notepad.md as its first action and use the contents to construct the "Nerede kalmistik?" summary.

**Any agent** — Any agent starting work on a project should check notepad.md for
Priority Notes that constrain their approach. An architect should not propose a
solution that contradicts a Priority Note.

---

## Example Scenarios

### Scenario 1: Mid-refactor compression

Working on a large refactor across 12 files. Context at 80%.

Pre-compact dump:
```markdown
### [2026-03-29 16:00] Task: Auth system refactor — 7/12 files done
Completed: user.service.ts, auth.controller.ts, token.service.ts,
  session.middleware.ts, logout.handler.ts, login.handler.ts, refresh.handler.ts
Remaining: password.service.ts, oauth.handler.ts, 2fa.handler.ts,
  admin.auth.ts, tests/auth.test.ts
Next: start password.service.ts — method signature unchanged, internals only
```

After compression, any agent reads this and knows exactly which 5 files remain.

### Scenario 2: Decision under uncertainty

User asked about caching strategy but has not confirmed yet.

Scratch note:
```markdown
### [2026-03-29 16:15] Pending: Caching strategy
Options: (a) Redis — fast, requires infra; (b) in-memory — simple, no persistence
Awaiting user confirmation on whether Redis is available in prod.
```

This prevents re-deriving the same question after compression.

### Scenario 3: Hard constraint from early conversation

User mentioned early in a long session that they cannot use PostgreSQL — MySQL only.

Priority note created immediately:
```markdown
### [2026-03-29 10:05] Constraint: Database — MySQL only
No PostgreSQL. Server is MySQL 8.0. All queries and schema must be MySQL-compatible.
Reason: Hosting provider limitation.
```

Every subsequent agent reads this and never proposes PostgreSQL.
