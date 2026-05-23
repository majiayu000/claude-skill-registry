---
name: todo-files
description: >
  Manage TODO files as persistent working memory for complex patterns. Track
  design decisions, implementation progress, and context across sessions. Use
  when starting complex patterns or resuming multi-session development work.
---

# TODO Files as Working Memory

**Convention:** Maintain TODO files in `patterns/$GITHUB_USER/design/todo/` to track complex pattern development.

**Purpose:**
- Act as persistent working memory across sessions
- Document design decisions and rationale
- Track implementation progress and next steps
- Preserve context for future reference
- Help other developers understand the pattern evolution

## When to Create a TODO File

- Starting a complex pattern with multiple features
- Pattern requires research or design decisions
- Multi-session development work
- Experimental features with unclear requirements
- Pattern needs documentation of architecture/choices

**File naming:** `pattern-name.md` (matches the pattern file name)

**Example:** `patterns/jkomoros/design/todo/cheeseboard-schedule.md`

## What to Include

```markdown
# Pattern Name - Development TODO

## Overview
Brief description of what the pattern does

## Requirements
- List of features to implement
- User stories or use cases

## Design Decisions
Document key choices made during development:
- Why you chose approach X over Y
- Trade-offs considered
- Framework features used and why

## Implementation Progress
- [x] Basic structure and data fetching
- [x] Ingredient parsing
- [ ] Advanced filtering features
- [ ] Performance optimization

## Technical Notes
- Important findings during development
- Framework quirks or workarounds
- Performance considerations
- Edge cases to handle

## Testing Notes
- Test scenarios covered
- Known issues or limitations
- Browser compatibility notes

## Next Steps
- Clear list of what needs to be done next
- Priorities for future sessions
```

## Update as You Go

- Mark tasks complete when done: `- [x] Feature implemented`
- Add new learnings and decisions
- Document blockers or questions
- Update next steps

## Active Usage Workflow

**When starting work on a pattern (especially resuming):**
1. Read the TODO file FIRST before touching code
2. Review "Next Steps" to understand priorities
3. Check "Technical Notes" for important context
4. Look at "Design Decisions" to understand rationale

**During development:**
1. Update "Implementation Progress" as you complete items
2. Add to "Technical Notes" when you discover framework quirks
3. Document "Design Decisions" when you choose an approach
4. Keep "Next Steps" current with what needs doing

**When you hit a blocker:**
1. Document the blocker in TODO
2. Note what you've tried
3. Add to "Next Steps" what needs investigation

**When finishing a work session:**
1. Mark completed tasks with `[x]`
2. Update "Next Steps" with clear priorities
3. Add any new learnings to "Technical Notes"
4. Commit the TODO along with code changes

## Frequency

- Update TODO file **multiple times per session**
- Don't wait until the end - update as you work
- TODO should always reflect current state
- Think of it as your "working memory" that persists

## Benefits

- Quickly resume work in next session
- Share context with user or other developers
- Document why certain decisions were made
- Track pattern evolution over time
- Never lose important context or learnings

## Difference from SNAPSHOT.md

- TODO files are **permanent** and checked into git
- SNAPSHOT.md is **temporary** and should be deleted after reading
- TODO files document the pattern's full development journey
- SNAPSHOT.md captures immediate session state

## Related Skills

- **pattern-development** - TODO files support development workflow
- **recovery-strategies** - TODO files help track what you've tried
