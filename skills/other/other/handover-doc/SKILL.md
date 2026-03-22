---
name: vibe-handover-doc
description: Generates a session continuity document at the end of a long session or when switching context on a multi-session project. Enables seamless resumption.
user-invocable: true
---

# vibe-handover-doc

Long sessions produce context that dies when the session ends. Capture it before it's lost.

## When to Use This Skill

- End of a long development session (2+ hours of work)
- Switching context to a different project/feature
- Before taking a break on multi-session work
- When you realize "this is going to take another session"
- User says "let's continue tomorrow" or "save progress"

## When NOT to Use This Skill

- Short sessions with trivial tasks
- Work that's fully committed and tested (the code IS the handover)
- When a handover doc already exists and is current

## Steps

1. **Capture current state**:
   - What branch are we on?
   - What files were modified? (git status)
   - Are there uncommitted changes?
   - What tests are passing/failing?

2. **Document completed work**:
   - What was accomplished this session?
   - Key decisions made (reference `vibe-decision-journal` entries)
   - Problems solved and how

3. **Document remaining work**:
   - What's left to do?
   - What's blocked and on what?
   - Known issues introduced

4. **Create a resume prompt**:
   - A specific prompt that the next session can use to get up to speed quickly
   - Include: branch name, key files to read, next task to tackle

5. **Save** to project docs (e.g., `docs/HANDOVER.md` or `docs/handover/YYYY-MM-DD.md`)

## Output Format

### Handover: [Feature/Project Name]
**Date**: [Today]
**Branch**: [branch name]

### Completed This Session
- [x] [Task 1]
- [x] [Task 2]

### Remaining Work
- [ ] [Task 3] — [notes]
- [ ] [Task 4] — blocked by [X]

### Key Decisions Made
- [Decision 1] — [rationale]

### Known Issues
- [Issue 1] — [impact]

### Files Changed
```
[git status summary]
```

### Resume Prompt
> [A specific prompt to use when resuming this work in a new session. Include context, branch, and next steps.]
