---
name: issue-lifecycle
description: Use throughout all work - ensures GitHub issues are updated continuously as work happens, not batched at the end
---

# Issue Lifecycle

## Overview

Update issues AS work happens, not in one dump at the end.

**Core principle:** The issue is the source of truth. Keep it current.

**This skill is used THROUGHOUT work, not as a separate step.**

## When to Update

Update the issue at these moments:

| Moment | Update Type |
|--------|-------------|
| Starting work | Status → In Progress |
| Hitting a blocker | Comment explaining blocker |
| Making a decision | Comment documenting decision |
| Discovering new information | Comment with findings |
| Completing acceptance criterion | Check off in body |
| Completing verification | Post verification report |
| Raising PR | Link PR to issue |
| Work complete | Status → Done |

## Update Types

### Status Updates (Project Field)

```bash
# Get item ID
ITEM_ID=$(gh project item-list [PROJECT_NUMBER] --owner @me \
  --format json | jq -r '.items[] | select(.content.number == [ISSUE_NUMBER]) | .id')

# Update status
gh project item-edit --project-id [PROJECT_ID] --id $ITEM_ID \
  --field-id [STATUS_FIELD_ID] \
  --single-select-option-id [NEW_STATUS_OPTION_ID]
```

### Comment Updates

```bash
gh issue comment [ISSUE_NUMBER] --body "## Progress Update

**Time:** $(date -u +%Y-%m-%dT%H:%M:%SZ)

### Completed
- Implemented X
- Fixed Y

### In Progress
- Working on Z

### Blockers
- None

### Next Steps
- Will do A next"
```

### Checkbox Updates (Acceptance Criteria)

When an acceptance criterion is met:

1. Read current issue body
2. Find the criterion checkbox
3. Change `- [ ]` to `- [x]`
4. Update the issue body

```bash
# Get current body
BODY=$(gh issue view [ISSUE_NUMBER] --json body -q '.body')

# Update checkbox (example with sed)
NEW_BODY=$(echo "$BODY" | sed 's/- \[ \] First criterion/- [x] First criterion/')

# Update issue
gh issue edit [ISSUE_NUMBER] --body "$NEW_BODY"
```

## Update Frequency

### Minimum Updates

At absolute minimum, update at these points:

1. **When starting** - "Starting work on this issue"
2. **When blocked** - Document the blocker immediately
3. **When unblocked** - Document resolution
4. **When PR created** - Link the PR
5. **When complete** - Final status update

### Recommended Updates

For active work, update more frequently:

- After each significant step
- When making decisions that affect approach
- When discovering unexpected complexity
- Every 30-60 minutes of active work

## What to Include in Updates

### Progress Comments

```markdown
## Progress Update - [TIME]

### Completed
- [What was done]

### Currently Working On
- [Active work]

### Decisions Made
- [Decision]: [Rationale]

### Issues Encountered
- [Issue]: [How resolved or current status]

### Next Steps
- [What comes next]
```

### Decision Comments

```markdown
## Decision: [Brief Title]

**Context:** [Why this decision was needed]

**Options Considered:**
1. [Option A] - [Pros/Cons]
2. [Option B] - [Pros/Cons]

**Decision:** [Chosen option]

**Rationale:** [Why this option was chosen]
```

### Blocker Comments

```markdown
## Blocked: [Brief Description]

**Blocked at:** [TIME]
**Blocking issue:** [What's preventing progress]

**What was tried:**
1. [Attempt 1]
2. [Attempt 2]

**Needs:** [What's needed to unblock]

**Impact:** [How this affects timeline/scope]
```

## Anti-Patterns

### Don't Do This

| Anti-Pattern | Problem |
|--------------|---------|
| Batch updates at end | No visibility during work |
| "Made progress" comments | Not specific enough |
| Updating only on success | Failures need documentation too |
| Skipping blocker documentation | Lost context on what went wrong |
| Closing without verification | Must verify before closing |

### Do This Instead

| Good Pattern | Benefit |
|--------------|---------|
| Update as you go | Real-time visibility |
| Specific progress notes | Clear record of what happened |
| Document failures | Learn from problems |
| Document blockers immediately | Faster unblocking |
| Verification before close | Ensures quality |

## Reading Issue History

Before starting work on any issue:

```bash
# View issue with all comments
gh issue view [ISSUE_NUMBER] --comments

# View timeline
gh issue view [ISSUE_NUMBER] --json timeline
```

Look for:
- Previous attempts
- Known blockers
- Decisions already made
- Related discussions

## Project Field Updates

Keep these fields current:

| Field | When to Update |
|-------|----------------|
| Status | When work state changes |
| Verification | After running verification |
| Criteria Met | After checking off criteria |
| Last Verified | After verification runs |

## Integration with Other Skills

This skill is used by:
- `issue-driven-development` - Throughout all steps
- `acceptance-criteria-verification` - Post verification reports
- `error-recovery` - Document failures

## Checklist

For each work session, ensure:

- [ ] Issue status reflects current state
- [ ] Any blockers are documented
- [ ] Decisions are recorded
- [ ] Completed criteria are checked off
- [ ] Verification reports are posted
- [ ] PRs are linked
