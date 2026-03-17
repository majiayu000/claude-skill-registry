---
name: memory-protocol
description: >-
  File-based knowledge persistence patterns: when to store discoveries,
  when to recall past solutions, and how to organize project memory.
  Activate when starting tasks, encountering errors, making decisions,
  or when context may be lost between sessions.
license: CC0-1.0
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  context: []
  phase: build
  standalone: true
---

# Memory Protocol

**Value:** Feedback -- accumulated knowledge creates compound feedback loops
across sessions. What you learn today should accelerate tomorrow's work.

## Purpose

Teaches the agent to systematically store and recall project knowledge using
file-based persistent memory. Solves the problem of context loss between
sessions, repeated debugging of known issues, and rediscovery of established
conventions.

## Practices

### Recall Before Acting

Before starting any non-trivial task, search memory for relevant past work.
Before debugging any error, search for that error message. Before making
design decisions, search for past decisions on the same topic.

**Search triggers:**
- Starting a new task
- Encountering an error or unexpected behavior
- Making architectural or design decisions
- Unsure about a project convention
- Before asking the user a question (it may already be answered)

**How to search:**
```bash
grep -r -i "search terms" ~/.claude/projects/<project-path>/memory/ --include="*.md"
```

If relevant memory is found, use it to inform your work. If not found,
proceed and store what you learn (next practice).

**Do not:**
- Skip search because "this seems simple"
- Assume you remember from a previous session (you do not)

### Store After Discovery

After solving a non-obvious problem, learning a convention, or making a
decision, store it immediately. Do not wait until later -- you will forget
or lose context.

**What to store:**
- Solutions to non-obvious problems (with the error message as keyword)
- Project conventions discovered while working
- Architectural decisions and their rationale
- User preferences for workflow or style
- Tool quirks and workarounds

**What not to store:**
- Obvious or well-documented information
- Temporary values or session-specific facts
- Verbose narratives (keep entries concise and searchable)

**Storage format:**
```markdown
# Brief Title with Keywords

**Context:** One sentence on when this applies.

**Discovery:** The key insight or solution, concise.

**Related:** Links to related memory files if any.
```

Write to the appropriate subdirectory:
```
~/.claude/projects/<project-path>/memory/
  MEMORY.md            # Quick reference (always loaded, keep under 200 lines)
  debugging/           # Error solutions
  architecture/        # Design decisions
  conventions/         # Project patterns
  tools/               # Tool quirks and workarounds
  patterns/            # Reusable approaches
```

### Keep MEMORY.md as the Index

`MEMORY.md` is loaded into context at session start. Use it as a concise
index of the most important facts -- project overview, critical conventions,
known gotchas. Link to detailed files in subdirectories for depth.

Keep MEMORY.md under 200 lines. When it grows beyond that, move details
into topic files and replace with a one-line summary and link.

### Prune Stale Knowledge

Knowledge goes stale. When you encounter a memory that is no longer accurate
(API changed, convention abandoned, bug fixed upstream), update or delete it.
Wrong memories are worse than no memories.

**Pruning triggers:**
- Memory contradicts current observed behavior
- Referenced files or APIs no longer exist
- Convention has clearly changed

### Store Before Context Loss

Before context compaction or at natural stopping points (task complete,
switching tasks), store any undocumented insights from the current session.
This is your last chance before the knowledge evaporates.

## Enforcement Note

This skill provides advisory guidance. It cannot force the agent to search
memory before acting or to store discoveries. On harnesses with persistent
memory directories (Claude Code auto memory), storage is straightforward.
On harnesses without persistent filesystems, adapt the pattern to whatever
persistence mechanism is available (project files, comments, or external
tools). The recall-before-act and store-after-discovery patterns are
universal even if the storage mechanism varies. For available enforcement
plugins, see the
[Harness Plugin Availability](../../README.md#harness-plugin-availability) table.

## Verification

After completing work guided by this skill, verify:

- [ ] Searched memory before starting the task
- [ ] Searched for error messages before debugging from scratch
- [ ] Stored solutions to any non-obvious problems encountered
- [ ] Stored any newly discovered conventions
- [ ] MEMORY.md remains under 200 lines
- [ ] No stale or contradicted memories left uncorrected

## Dependencies

This skill works standalone. For enhanced workflows, it integrates with:

- **debugging-protocol:** Search memory before starting the 4-phase investigation
- **user-input-protocol:** Store user answers to avoid re-asking the same questions
- **tdd-cycle:** Store test patterns and domain modeling insights between sessions

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill debugging-protocol
```
