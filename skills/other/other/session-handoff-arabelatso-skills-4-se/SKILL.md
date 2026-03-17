---
name: session-handoff
description: Creates structured context summaries for continuing work across AI sessions. Use when ending a session to enable seamless continuation in a new session without losing context.
---

# Session Handoff

Generates a detailed handoff document capturing the current state of work, enabling seamless continuation in a fresh AI session.

## When to Use This Skill

- Ending a long coding session that will continue later
- Switching between AI tools or models mid-task
- Context window approaching limits, need a fresh session
- Handing off work to a teammate (human or AI)

## What This Skill Does

Generate a structured handoff document with:

### 1. Current State Summary

```markdown
## Session Summary

**Task**: [What was being worked on]
**Branch**: [Current git branch]
**Status**: [In progress / Blocked / Ready for review]
**Started**: [When work began]
```

### 2. What Was Done

```markdown
## Completed Work

1. [Task 1] — [files changed, what was done]
2. [Task 2] — [files changed, what was done]

### Key Decisions Made
- Chose X over Y because [reason]
- Used pattern Z from [existing file] for consistency
```

### 3. What Remains

```markdown
## Remaining Work

1. [ ] [Next task] — [specific files, what to do]
2. [ ] [Following task] — [dependencies, approach]

### Blockers
- [Any blocking issues with context]
```

### 4. Relevant Context

```markdown
## Key Files
- `src/auth/oauth.ts` — Main implementation file (modified)
- `src/auth/types.ts` — Type definitions (new)
- `tests/auth/oauth.test.ts` — Tests (partially written)

## Patterns to Follow
- Auth middleware pattern from `src/middleware/jwt.ts`
- Error handling style from `src/errors/`

## Gotchas Discovered
- The `UserService` caches aggressively — clear cache after auth changes
- Test DB needs `--runInBand` flag to avoid connection pool exhaustion

## Commands
- Build: `npm run build`
- Test: `npm test -- --runInBand`
- Verify: `npm run typecheck`
```

### 5. Continuation Instructions

```markdown
## How to Continue

1. Read this handoff document
2. Check `git status` and `git log -5 --oneline` for current state
3. Start with [specific next task]
4. Reference [specific file] for the pattern to follow
```

## Tips

- Write the handoff BEFORE you lose context, not after
- Include specific file paths, not vague descriptions
- Document gotchas — things that surprised you during the session
- Include the exact commands needed to verify work
- Keep it under 200 lines — the next session needs room in its context window

## Example

**User**: "Create a handoff for this session"

**Output**: Generates a structured markdown document covering: 3 completed tasks with file paths, 2 remaining tasks with specific instructions, 4 key files with their roles, 2 gotchas discovered during the session, and exact build/test commands.

**Inspired by:** [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) /handoff command
