---
name: tzurot-docs
description: Documentation procedures for Tzurot v3. Use when updating CURRENT.md or BACKLOG.md. Covers workflow, folder structure, and knowledge continuity.
lastUpdated: '2026-01-26'
---

# Tzurot v3 Documentation & Workflow

**Use this skill when:** Starting/ending a session, managing work items, creating documentation, or updating existing docs.

## Two-File Workflow

Work is tracked in two files. Tech debt competes for the same time as features.

| File         | Purpose                               | Update When                   |
| ------------ | ------------------------------------- | ----------------------------- |
| `CURRENT.md` | Active session - what's happening NOW | Start/end session, task done  |
| `BACKLOG.md` | Everything else - all queued work     | New ideas, triage, completion |

**Tags**: 🏗️ `[LIFT]` refactor/debt | ✨ `[FEAT]` feature | 🐛 `[FIX]` bug | 🧹 `[CHORE]` maintenance

### CURRENT.md Structure

```markdown
# Current

> **Session**: YYYY-MM-DD
> **Version**: v3.0.0-beta.XX

## Session Goal

_One sentence on what we're doing today._

## Active Task

_Cut from BACKLOG, paste here when starting work._

🏗️ `[LIFT]` **Task Name**

- [ ] Subtask 1
- [ ] Subtask 2

## Scratchpad

_Error logs, decisions, API snippets - anything Claude needs to see._

## Recent Highlights

- **beta.XX**: Brief description
```

### BACKLOG.md Structure

```markdown
## Inbox

_New items go here. Triage to appropriate section later._

## High Priority

_Top 3-5 items to pull into CURRENT next._

## Epic: [Theme Name]

_Group related work by project, not by type._

## Smaller Items

_Opportunistic work between major features._

## Icebox

_Ideas for later. Resist the shiny object._

## Deferred

_Decided not to do yet._
```

## Workflow Operations

### Intake (New Idea)

Add to **Inbox** in BACKLOG.md with a tag. Don't categorize yet.

```markdown
## Inbox

- ✨ `[FEAT]` **Feature Name** - Brief description
```

### Triage (Between Tasks)

Move items from Inbox to appropriate section:

- High Priority → If it's next
- Epic → If it belongs to a theme
- Smaller Items → If opportunistic
- Icebox → If "someday maybe"

### Start Work (Pull)

1. Cut task from BACKLOG.md
2. Paste into CURRENT.md under **Active Task**
3. Add checklist if needed
4. Update **Session Goal**

### Complete Work (Done)

1. Mark task complete in CURRENT.md
2. Move to **Recent Highlights** (keep last 3-5)
3. Pull next task from BACKLOG High Priority

### Session End

1. Update CURRENT.md with progress
2. If task incomplete, note blockers in Scratchpad
3. Commit with `wip:` prefix if needed

## Documentation Structure

```
docs/
├── reference/           # THE TRUTH - What currently exists
│   ├── architecture/    # Design decisions, system architecture
│   ├── deployment/      # Railway, infrastructure setup
│   ├── standards/       # Coding patterns, folder structure
│   └── guides/          # Developer how-tos
├── proposals/           # THE PLANS - What we want to build
│   ├── active/          # On roadmap, being worked on
│   └── backlog/         # Ideas not yet scheduled
├── incidents/           # Postmortems and lessons learned
└── research/            # Investigation notes
```

**Root files only:** README.md, CLAUDE.md, CURRENT.md, BACKLOG.md

## Decision Rules

| Question             | Answer                           |
| -------------------- | -------------------------------- |
| Is it work to do?    | → BACKLOG.md                     |
| Is it active now?    | → CURRENT.md                     |
| Is it implemented?   | → `docs/reference/`              |
| Is it a future plan? | → `docs/proposals/`              |
| Is it done/obsolete? | → Extract learnings, then DELETE |

## GitHub Releases Format

```markdown
## What's Changed

### Added

- New feature X for doing Y

### Changed

- Improved performance of A

### Fixed

- Bug where X would fail

**Full Changelog**: https://github.com/lbds137/tzurot/compare/vX.X.X...vY.Y.Y
```

## Best Practices

### ✅ Do

- Use tags consistently (🏗️, ✨, 🐛, 🧹)
- Keep CURRENT.md focused on TODAY
- Group work by Epic/Theme in BACKLOG
- Delete obsolete docs (git preserves history)
- Update at session boundaries

### ❌ Don't

- Let CURRENT.md get stale
- Mix feature types in the same Epic
- Keep "someday" items in High Priority
- Create new files when existing ones work
- Document obvious things

## Session Start Checklist

1. Read CURRENT.md - What's the active task?
2. Read BACKLOG.md High Priority - What's next?
3. Read CLAUDE.md if rules are unclear
4. Continue active task or pull next

## Related Skills

- **tzurot-git-workflow** - Commit documentation updates
- **tzurot-council-mcp** - When to consult for workflow decisions
- **tzurot-architecture** - Document architectural decisions

## References

- Current session: `CURRENT.md`
- All work items: `BACKLOG.md`
- Project guidelines: `CLAUDE.md`
- Documentation structure: `docs/README.md`
