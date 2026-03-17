---
name: project-memory
description: Persist context across sessions using external memory files
---

# Project Memory Skill

Maintain persistent context across Claude Code sessions using external files as memory.

## Memory System Overview

Since Claude's context resets between sessions, we use files to persist important information:

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `docs/status.md` | Current work status | Every session |
| `docs/tech-debt.md` | Known technical debt | When identified |
| `docs/decisions/*.md` | Architecture decisions | When made |

## Session Start Protocol

When starting a new session:

1. **Read status file**
   ```bash
   cat docs/status.md
   ```

2. **Check git state**
   ```bash
   git log --oneline -10
   git status
   ```

3. **Review recent decisions**
   ```bash
   ls -la docs/decisions/ | tail -5
   ```

4. **Summarize context** before proceeding with new work

## Session End Protocol

Before ending a session:

1. **Summarize work done**
2. **Update status.md** with:
   - What was accomplished
   - What's in progress
   - Any blockers
   - Context for next session
3. **Document any decisions** in `docs/decisions/`
4. **Commit changes** with descriptive message

## Status File Format

```markdown
# Project Status

## Last Updated
[Timestamp]

## Current Focus
[Main area of work]

## In Progress
- [ ] [Task 1] - [status notes]
- [ ] [Task 2] - [status notes]

## Completed Recently
- [x] [Completed task]

## Blockers
- [Blocker description] - [what's needed]

## Decisions Made
- [Decision]: [rationale]

## Context for Next Session
- [Important point 1]
- [Important point 2]
- [Where to pick up]
```

## Decision Record Format

Create `docs/decisions/YYYY-MM-DD-topic.md`:

```markdown
# [Number]. [Title]

## Status
[Proposed | Accepted | Deprecated]

## Context
[Why this decision is needed]

## Decision
[What we decided]

## Consequences
[What this means going forward]
```

## Technical Debt Tracking

Add to `docs/tech-debt.md` when noticing debt:

```markdown
## [Priority Level]

| Item | Location | Description | Added |
|------|----------|-------------|-------|
| [Name] | [file:line] | [Description] | [Date] |
```

## Git as Memory

Git history serves as additional memory:

- **Commit messages** should explain why, not just what
- **Branch names** should describe the work
- **PR descriptions** capture context

### Useful Git Commands for Context

```bash
# Recent activity
git log --oneline -20

# What changed in a file
git log -p --follow -- path/to/file

# Search commits for keywords
git log --grep="keyword"

# Changes in current branch
git log main..HEAD --oneline
```

## Context Handoff Checklist

Before handing off to another session or team member:

- [ ] `docs/status.md` is current
- [ ] Uncommitted work is either committed or described
- [ ] Decisions are documented
- [ ] Blockers are noted
- [ ] Next steps are clear

## Best Practices

1. **Update frequently** - Don't wait until the end
2. **Be specific** - "Fixed auth" < "Fixed JWT expiry handling in refresh flow"
3. **Include blockers** - They're easy to forget
4. **Link to files** - "See src/auth/jwt.ts:45" for context
5. **Keep it scannable** - Use lists and headers
