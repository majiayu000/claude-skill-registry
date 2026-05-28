---
name: park
description: Save current work context for later resumption
---

# Park

Save the current work session for later resumption.

## What to Capture

1. **Git state**
   - Current branch
   - Worktree path (if applicable)
   - Uncommitted changes summary

2. **Current task**
   - What we're doing
   - What's in progress
   - Any blockers

3. **Key decisions**
   - Choices made during this session
   - Rationale (so they don't get re-litigated)

4. **Relevant files**
   - Files created, modified, or read
   - Mark as (new), (modified), or (read)

5. **Next steps**
   - What should happen next
   - In priority order

6. **Resume prompt**
   - Suggested prompt to continue this work

## Output Location

Resolve location in order:
1. Project `CLAUDE.md` → `## Handoffs` or `## Parking` → `Location:`
2. User `~/.claude/CLAUDE.md` → same lookup
3. Default: `.parkinglot/` in project root

Ensure the directory exists. If using `.parkinglot/`, check it's gitignored.

## Output Format

```markdown
# Parked: [Topic]

**Parked:** [Date/time]
**Branch:** [branch-name]
**Worktree:** [path if applicable]

## Current State
[What's done, what's in progress, any blockers]

## Key Decisions
- [Decision 1 with brief rationale]
- [Decision 2 with brief rationale]

## Relevant Files
- path/to/file.ts (new)
- path/to/other.ts (modified)
- path/to/reference.ts (read)

## Next Steps
1. [Next step]
2. [Next step]

## Resume Prompt
[Suggested prompt to continue this work - specific enough to pick up where we left off]
```

## Filename

Use slug from topic: `[topic-slug].md`

Example: `jwt-authentication.md`, `fix-login-bug.md`

## After Parking

Report:

```
Parked to `[path]`.

To resume in a new session:
/unpark [path]
```

The `/unpark [path]` command should be copy-pasteable so the user can easily resume.
