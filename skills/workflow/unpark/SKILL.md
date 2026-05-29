---
name: unpark
description: Resume work from a parked handoff
---

# Unpark

Resume work from a parked handoff document.

## Process

### 1. Find Handoff

Check parking locations in order:
1. Project `CLAUDE.md` → `## Handoffs` or `## Parking` → `Location:`
2. User `~/.claude/CLAUDE.md` → same lookup
3. Default: `.parkinglot/` in project root

If multiple handoffs exist, list them and ask which to resume:

```
Found parked sessions:
(A) jwt-authentication.md - Parked 2026-01-30
(B) fix-login-bug.md - Parked 2026-01-29
(C) Other location
```

### 2. Read and Present

Read the handoff document and present a summary:

```
Resuming: [Topic]

Parked: [Date]
Branch: [branch]

Current state: [Brief summary]

Next steps:
1. [Step 1]
2. [Step 2]
```

### 3. Validate

Check that the handoff is still valid:

- [ ] Git branch matches (or can be checked out)
- [ ] Worktree exists (if specified)
- [ ] Key files still exist
- [ ] Decisions still seem relevant

### 4. Handle Validation Results

**If valid:**
```
Validation passed. Ready to continue with: [first next step]

Proceed?
(A) Yes, continue
(B) Review the full handoff first
(C) Adjust the plan
```

**If stale or invalid:**
```
Validation found issues:
- [Issue 1]
- [Issue 2]

Options:
(A) Update handoff and try again - I'll revise based on current state
(B) Start fresh - discard this handoff
(C) Continue anyway - I understand the context has changed
```

If option A: Update the handoff file with current findings, then recommend running `/unpark` again.

## Edge Cases

- **Branch doesn't exist:** Offer to create it or pick a different branch
- **Files deleted:** Note in validation, may still be able to continue
- **Handoff is very old:** Extra scrutiny on decisions, they may need revisiting
