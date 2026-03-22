---
name: resume-handoff
description: Resume work from a handoff document. Reads the handoff, verifies current state against documented state, and presents analysis before continuing work.
---

# Resume from Handoff

Resume work from a handoff document through analysis and verification.

## Step 1: Read Handoff Completely

**If given a handoff path:**
```bash
# Read the handoff file
cat handoffs/2026-01-12_14-30-00_oauth-integration.md
```

**If given an issue ID:**
```bash
# Find handoffs for this issue
ls handoffs/*issue-123* | sort -r | head -1

# Or search in handoff content
grep -l "issue: issue-123" handoffs/*.md | sort -r | head -1
```

**If no parameter provided:**
```bash
# List recent handoffs
ls -lt handoffs/ | head -10

# Ask user which to resume
```

## Step 2: Extract Key Information

From the handoff, identify:

**Task Status:**
- What was completed?
- What's in progress?
- What's planned?

**Critical Files:**
- Which files are most important?
- What are the line ranges mentioned?

**Key Learnings:**
- What discoveries affect our work?
- What mistakes should we avoid?

**Open Questions:**
- What needs decisions?
- What was uncertain?

**Next Steps:**
- What's the prioritized todo list?

## Step 3: Verify Current State

```bash
# Check if anything changed since handoff
git log --oneline [handoff_commit]..HEAD

# Check current branch
git branch --show-current

# Check working directory status
git status

# Compare current state to handoff state
git diff [handoff_commit]
```

## Step 4: Read Referenced Files

Read the "Critical Files" section files:

```bash
# Read each critical file mentioned
cat src/auth/oauth.ts
cat src/auth/providers.ts
# ... etc
```

**Focus on:**
- Understanding current implementation
- Verifying learnings still apply
- Finding any conflicts with changes since handoff

## Step 5: Present Analysis

```
I've analyzed the handoff from [date]. Here's the current situation:

## Original Context
[Summary of what was being worked on]

## Task Status Review

**Completed (from handoff):**
- [x] Task 1 - VERIFIED: Still complete
- [x] Task 2 - VERIFIED: Still complete

**In Progress (from handoff):**
- [ ] Task 3 - STATUS: [describe current state]

**Planned:**
- [ ] Next task 1 [Priority from handoff]
- [ ] Next task 2

## Changes Since Handoff

**Commits since handoff:**
[List any commits between handoff and now]

**Impact:**
[How these changes affect our work]

## Key Learnings Still Applicable

1. [Learning 1] - Still valid because [reason]
2. [Learning 2] - Still valid, see [file:line]

## Questions Needing Resolution

From handoff:
- [ ] [Question 1] - [Current thinking or need decision]
- [ ] [Question 2] - [Can we resolve this now?]

## Recommended Next Action

Based on the handoff priorities and current state:

**Priority 1:** [Action from handoff]
- Reason: [Why this is still the priority]
- Files: [What needs to change]
- Approach: [How to do it]

Shall I proceed with [action]?
```

## Step 6: Get Confirmation and Begin

Wait for user confirmation, then:
- Create todo list from next steps
- Start with highest priority action
- Apply learnings from handoff
- Track progress as you go

## Scenarios

### Clean Continuation
All changes present, no conflicts, proceed normally.

### Diverged Codebase
```
Changes detected since handoff:

Commit a1b2c3d: "refactor: restructure auth module"
- Affects our OAuth implementation
- Provider files moved to src/auth/providers/ directory
- Need to update our understanding

I'll read the new structure before proceeding. Let me check:
- src/auth/providers/ directory contents
- How existing patterns changed
- If our learnings still apply

[After reading]

Updated understanding:
- Providers now in separate directory (not one file)
- Pattern still the same, just reorganized
- Our work can continue with file path updates

Shall I proceed with the original plan, adapting to new structure?
```

### Incomplete Work
```
The handoff shows Task 3 was "in progress". Let me verify current state:

[Reads relevant files]

Current state: Task 3 is partially done:
- OAuth flow implemented
- Provider selection NOT YET implemented
- Error states missing

Recommended approach:
1. Complete Task 3 first (finish what was started)
2. Then proceed to planned work

Shall I complete Task 3 before moving to new work?
```

### Stale Handoff
```
The handoff is from [3 weeks ago]. Significant changes detected:

Changes:
- 47 commits since handoff
- Auth system refactored
- New OAuth library integrated

This handoff may be too stale to resume directly.

Options:
1. Review changes and adapt the plan
2. Start fresh with current codebase state
3. Cherry-pick specific unfinished work

What would you like to do?
```

## Guidelines

1. **Always verify before acting** - Don't assume handoff matches reality
2. **Apply learnings** - Use documented patterns and avoid noted pitfalls
3. **Check open questions** - Some may be resolved or need decisions now
4. **Respect priorities** - Handoff author prioritized for a reason
5. **Adapt to changes** - If codebase changed, acknowledge and adapt
6. **Create new handoff** - When this session ends, update or create new one
