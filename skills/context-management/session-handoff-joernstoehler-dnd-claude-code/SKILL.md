---
name: session-handoff
description: Use this checklist at the end of a working session before context is lost.
---

# Session Handoff Skill

Use this checklist at the end of a working session before context is lost.

## When to Use

- Before ending a session (user says "wrap up", "handoff", "done for now")
- Before context compaction warnings
- After completing a major piece of work

## Handoff Checklist

### 1. Write Decisions to Files

- [ ] Any important decisions made in conversation? Write them to relevant files.
- [ ] Any brainstormed content not yet saved? Add to appropriate location.
- [ ] User corrections or clarifications? Update affected files.

### 2. Update Progress Tracking

- [ ] Update PROGRESS.md (or equivalent) with current state
- [ ] Mark completed items as done
- [ ] Add new items discovered during session
- [ ] Check for outdated notes and fix them

### 3. Add Handoff Notes (if applicable)

If work continues in another session:
- [ ] Recommended task order for next agent
- [ ] Key files to read for onboarding
- [ ] Any conventions established this session
- [ ] Warnings about pitfalls or known issues

### 4. Commit and Push

- [ ] Stage all changes: `git add -A`
- [ ] Write clear commit message summarizing session work
- [ ] Push to branch: `git push -u origin <branch>`
- [ ] Confirm push succeeded

### 5. Verify Nothing Lost

- [ ] Re-read final PROGRESS.md or handoff section
- [ ] Does it capture everything the next agent needs to know?
- [ ] Would you understand the context if you read only the files?

## Common Mistakes to Avoid

- Leaving important context only in conversation
- Forgetting to update progress percentages
- Not specifying recommended task order when it matters
- Outdated notes that contradict current state
- Uncommitted work
