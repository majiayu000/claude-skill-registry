---
name: memory
description: Manages cross-session knowledge persistence. Triggers on "remember", "recall", "what did we", "save this decision", "todo", or session handoff.
---

# Memory

Memory is not storage. Memory is the foundation for evolution.

## Philosophy

### Why Memory?

Without memory, every session starts from zero.

```
Session 1: Makes mistake A
Session 2: Makes mistake A again
Session 3: Makes mistake A again
...forever
```

With memory, patterns emerge:

```
Session 1: Makes mistake A, records it
Session 2: Reads record, avoids A, discovers B
Session 3: Reads both, avoids A and B, finds better path
...progress
```

Memory isn't for the current session—**memory is a gift to future sessions**.

### The Deeper Purpose

Memory transforms isolated events into accumulated wisdom.

```
Individual record: "We tried X, it failed because Y"
Pattern after 5 records: "Approaches like X tend to fail when Y"
Wisdom after 20 records: "Before attempting X-like solutions, check for Y"
```

This is how learning works. Not through rules handed down, but through patterns that emerge from recorded experience.

### What to Remember

Not everything deserves memory. Record what would **hurt if forgotten**:

| Remember | Don't Remember |
|----------|----------------|
| Decisions and their rationale | Implementation details (use code) |
| Mistakes and lessons | Obvious facts (use docs) |
| Context that explains "why" | Temporary debugging notes |
| Patterns that emerged | Things Git already tracks |

The test: "Would a future agent benefit from knowing this?"

## Structure

```
.memory/
├── context.md      → Current state, active concerns (read first)
├── notes/          → Learnings, observations
├── decisions/      → ADRs: what was decided and why
├── todos/          → Tasks that span sessions
└── sessions/       → Session summaries (handoff to next)
```

### context.md

The handoff document. When a new session starts, this tells them:
- What's currently in progress
- What concerns are active
- What needs attention

Keep it current. A stale context.md is worse than none.

### Naming Convention

```
YYYY-MM-DD-kebab-slug.md
```

Natural sort order. Grep-friendly. Self-documenting.

## Core Operations

| Intent | Action |
|--------|--------|
| "Remember this" | Create note in `.memory/notes/` |
| "We decided X because Y" | Create ADR in `.memory/decisions/` |
| "What did we learn about Z?" | Search `.memory/`, summarize with citations |
| "Session ending" | Create session summary, update context.md |

### Record Format

```markdown
---
type: note | decision | todo | session
status: active | completed | archived
tags: [relevant, keywords]
created: YYYY-MM-DD
---

# Title

Content that future agents will thank you for.
```

## Integration

Memory provides context to other skills:

```
memory
  │
  ├─► orientation reads context.md at session start
  ├─► dive uses past notes to inform investigation
  ├─► engineering reads decisions before proposing new ones
  └─► refining includes relevant history in PR descriptions
```

## Understanding, Not Rules

| Tension | Resolution |
|---------|------------|
| Completeness vs Noise | Record signal, not noise. Ask: "Would this help a future agent?" |
| Structure vs Flexibility | Use consistent format, but content matters more than form |
| Writing vs Doing | Recording takes seconds; re-learning takes hours |

### The Anti-Pattern

The worst failure isn't forgetting to record—it's recording without understanding.

```
Bad: "Fixed bug in auth"
Good: "Auth was failing silently when token expired mid-request.
       Root cause: async race condition.
       Fix: Added token refresh before sensitive operations.
       Lesson: Any auth code should handle mid-operation expiry."
```

The second takes 30 seconds longer. It saves the next agent hours.

## Reference

See `reference/` for:
- [templates/](templates/) - Record templates
- [remote-sync.md](reference/remote-sync.md) - GitHub/GitLab Issues sync
- [setup.md](reference/setup.md) - Initialization options
