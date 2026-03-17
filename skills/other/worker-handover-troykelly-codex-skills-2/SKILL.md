---
name: worker-handover
description: Defines context handover format when workers hit turn limit. Posts structured handover to GitHub issue comments enabling replacement workers to continue seamlessly.
---

# Worker Handover

## Overview

When workers approach their turn limit (100 turns), they must create a handover that enables a replacement worker to continue without losing context.

**Core principle:** A replacement worker should understand the work as well as the original worker did.

**Announce at start:** "I'm approaching my turn limit. Creating handover for replacement worker."

## State Management

**CRITICAL:** Handover context is stored in GitHub issue comments. NO local handover files.

| State | Location | Purpose |
|-------|----------|---------|
| Handover context | Issue comment | Full context for replacement worker |
| Git changes | Branch commits | Work completed so far |
| Test status | Issue comment | Current test state |

Handover survives crashes because it's in GitHub, not local files.

## When to Handover

| Turns Used | Action |
|------------|--------|
| 85+ | Evaluate if handover needed |
| 90+ | Begin handover preparation |
| 95+ | Complete handover, prepare to exit |
| 100 | Exit (automatic) |

## Handover Format

Post to the issue with structured markers:

```markdown
<!-- HANDOVER:START -->

# Handover: Issue #[ISSUE]

## Metadata

| Field | Value |
|-------|-------|
| Issue | #[ISSUE] |
| Previous Worker | [WORKER_ID] |
| Turns Used | [N]/100 |
| Timestamp | [ISO_TIMESTAMP] |
| Orchestration | [ORCHESTRATION_ID] |
| Attempt | [N] |

## Issue Summary

[Concise summary of what the issue requires - in your own words, not copied]

## Current State

### Branch Status
- **Branch:** `[BRANCH_NAME]`
- **Commits:** [N] commits ahead of main
- **Last Commit:** `[COMMIT_HASH]` - [COMMIT_MESSAGE]

### Files Modified
[List of modified files with brief description of changes]

### Tests Status
- **Passing:** [N]
- **Failing:** [N]
- **Coverage:** [X]%

## Work Completed

### Done
- [x] [Completed task 1]
- [x] [Completed task 2]

### In Progress
- [ ] [Current task - describe state]

### Remaining
- [ ] [Remaining task 1]
- [ ] [Remaining task 2]

## Context & Decisions

### Key Decisions Made
1. **[Decision]:** [Why this choice was made]
2. **[Decision]:** [Why this choice was made]

### Approaches Tried
1. **[Approach]:** [Result/Why abandoned]

### Important Discoveries
- [Discovery that affects implementation]

## Technical Notes

### Architecture Notes
[Any architectural decisions or patterns being used]

### Gotchas
- [Thing that might trip up the next worker]
- [Non-obvious behavior discovered]

## Current Blocker (if any)
[Description of what's blocking progress, if anything]

## Recommended Next Steps
1. [Specific next action to take]
2. [Following action]
3. [Following action]

## Files to Review First
1. `[path/to/key/file.ts]` - [Why it's important]
2. `[path/to/key/file.ts]` - [Why it's important]

## Commands to Run
```bash
# Verify current state
pnpm test

# Continue development
[specific commands]
```

---
*Handover created by [WORKER_ID] at [TIMESTAMP]*

<!-- HANDOVER:END -->
```

## Creating a Handover

### Step 1: Assess State

```bash
# Check git status
git status
git log --oneline -10

# Check test status
pnpm test 2>&1 | tail -20

# Count modified files
git diff --name-only HEAD~[N]
```

### Step 2: Post Handover to Issue

```bash
ISSUE=123
WORKER_ID="worker-1234567890-123"
BRANCH=$(git branch --show-current)
LAST_COMMIT=$(git log -1 --format='%h - %s')
COMMITS_AHEAD=$(git rev-list --count main..HEAD)

gh issue comment "$ISSUE" --body "<!-- HANDOVER:START -->

# Handover: Issue #$ISSUE

## Metadata

| Field | Value |
|-------|-------|
| Issue | #$ISSUE |
| Previous Worker | $WORKER_ID |
| Turns Used | 94/100 |
| Timestamp | $(date -u +%Y-%m-%dT%H:%M:%SZ) |
| Orchestration | $ORCHESTRATION_ID |

## Current State

### Branch Status
- **Branch:** \`$BRANCH\`
- **Commits:** $COMMITS_AHEAD commits ahead of main
- **Last Commit:** \`$LAST_COMMIT\`

[... rest of handover content ...]

<!-- HANDOVER:END -->"
```

### Step 3: Commit Any Uncommitted Work

```bash
git add -A
git commit -m "chore: Save progress before handover

Worker $WORKER_ID reached turn limit.
Handover posted to issue #$ISSUE.

Orchestrator: $ORCHESTRATION_ID"
```

### Step 4: Exit Gracefully

Worker exits after posting handover. Orchestrator will spawn replacement.

## Receiving a Handover

When a replacement worker starts, it reads handover from issue comments:

### Step 1: Read Handover from GitHub

```bash
ISSUE=123

# Get latest handover from issue comments
HANDOVER=$(gh api "/repos/$OWNER/$REPO/issues/$ISSUE/comments" \
  --jq '[.[] | select(.body | contains("<!-- HANDOVER:START -->"))] | last | .body')

echo "$HANDOVER"
```

### Step 2: Verify State

```bash
# Verify branch
git branch --show-current

# Check current state matches handover
git status
git log --oneline -5

# Run tests
pnpm test
```

### Step 3: Acknowledge Receipt

Post acknowledgment to issue:

```markdown
**Handover Received**

**Replacement Worker:** [NEW_WORKER_ID]
**Continuing from:** [PREVIOUS_WORKER_ID]
**Attempt:** [N]

**Handover verified:**
- [x] Branch state matches
- [x] Tests status matches
- [x] Context understood

**Continuing with:**
[First task from "Recommended Next Steps"]

---
*Orchestration: [ORCHESTRATION_ID]*
```

### Step 4: Continue Work

Follow the "Recommended Next Steps" from the handover.

## Handover Quality Checklist

Before creating handover:

- [ ] All local changes committed
- [ ] Handover captures current state accurately
- [ ] Key decisions are documented
- [ ] Gotchas are noted
- [ ] Next steps are specific and actionable
- [ ] Files to review are listed in priority order
- [ ] Commands to run are tested and correct
- [ ] Handover posted to issue comment
- [ ] Work committed to branch

## Bad Handover Examples

### Too Vague

```markdown
## Work Completed
- Did some stuff
- Made progress

## Next Steps
- Finish the feature
```

### Missing Context

```markdown
## Work Completed
- [x] Implemented the thing

## Next Steps
- Fix the tests
```
(No explanation of WHY tests are failing)

## Good Handover Example

See the full format above for a complete, high-quality handover that includes:
- Specific commit references
- Test failure details
- Decisions with rationale
- Gotchas discovered
- Actionable next steps
- File priority list
- Verified commands

## Integration

This skill is used by:
- `worker-protocol` - Triggers handover creation
- `worker-dispatch` - Provides handover to replacement workers

This skill uses:
- GitHub issue comments for handover storage
- Git for state verification
