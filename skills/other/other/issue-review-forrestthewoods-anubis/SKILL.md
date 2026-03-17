---
name: issue-review
description: Reviews and categorizes GitHub issues by difficulty (easy/medium/hard). Use when you need to triage open issues, ask clarifying questions for incomplete issues, or write implementation plans for ready issues.
---

# Issue Review and Categorization

## Project Board

All issues are tracked on the **Anubis Issue Tracker** project board:
- **Project URL:** https://github.com/users/forrestthewoods/projects/8
- **Project Number:** 8
- **Owner:** forrestthewoods

## Board Status Workflow

| Status | Description |
|--------|-------------|
| **Backlog** | Future ideas or deferred work; not ready for action yet |
| **Triage** | New issues not yet added to the project board |
| **Needs Agent Review** | Issues ready for agent to review and categorize |
| **Needs Human Review** | Agent has questions; waiting for human clarification |
| **Ready to Implement** | Agent reviewed, wrote plan, no questions remaining |
| **Needs Code Review** | Implementation in progress (has active branch) |
| **Done** | Closed and completed (automatic via GitHub) |

**Important:** Issues in **Backlog** should be **completely ignored** by this skill. These are deferred tasks that are not ready for review. Do not triage, categorize, or write implementation plans for Backlog issues.

## Workflow Overview

1. **New issues** are created in GitHub Issues
2. Issues not in the project are placed in **Triage**
3. Issues move to **Needs Agent Review** for agent processing
4. Agent reviews each issue:
   - Labels the issue as `difficulty: easy`, `difficulty: medium`, or `difficulty: hard`
   - If clarification needed → post questions as comment → move to **Needs Human Review**
   - If no questions → write detailed implementation plan as comment → move to **Ready to Implement**
5. When implementation begins, agent creates branch using the branch naming convention
6. Issues with active branches are detected and moved to **Needs Code Review**
7. When issue is closed, GitHub automatically moves it to **Done**

## Purpose

This skill ensures the project board accurately reflects the current state of all issues by:
1. Detecting the correct status for each issue based on its actual state
2. Identifying mismatches between current board status and actual state
3. Categorizing issues by difficulty (easy, medium, hard)
4. Posting clarifying questions for incomplete issues
5. Writing detailed implementation plans for well-defined issues

## Instructions

### Step 1: Gather Complete Issue Data

Collect all information needed to determine correct status:

```bash
# Get all open issues with full details
gh issue list --state open --json number,title,body,labels,comments,assignees,state --limit 100

# Get all open branches (to detect active implementation)
git ls-remote --heads origin | grep -E 'claude/|issue-' | awk '{print $2}' | sed 's|refs/heads/||'

# Get all PRs and their linked issues
gh pr list --state open --json number,title,state,isDraft,body,url,headRefName --limit 100

# Get current board state
gh project item-list 8 --owner forrestthewoods --format json
```

For each issue, check for active branches:
```bash
# Check if issue has an active branch (branch name contains issue number)
git ls-remote --heads origin | grep -i "issue-<number>\|#<number>\|-<number>-"

# Check if issue has linked PRs
gh pr list --search "#<number>" --state all --json number,title,state,isDraft,headRefName
```

### Step 2: Determine Correct Status for Each Issue

Apply these rules **in order** (first match wins):

#### Rule 1: Issue is Closed → **Done**
```
IF issue is closed (merged PR or manually closed)
THEN status should be "Done"
Note: GitHub automation handles this automatically
```

#### Rule 2: Has Active Branch or Open PR → **Needs Code Review**
```
IF issue has an open PR that references it
OR issue has an active branch with the issue number in the name
THEN status should be "Needs Code Review"
```

#### Rule 3: Has Implementation Plan → **Ready to Implement**
```
IF issue comments contain an "## Implementation Plan" section
AND the plan appears complete (has steps, files to modify)
AND no unanswered clarifying questions
THEN status should be "Ready to Implement"
```

#### Rule 4: Waiting for Human Response → **Needs Human Review**
```
IF the most recent comment contains "## Clarification Needed" or similar question format
AND the issue author/maintainer hasn't responded yet
THEN status should be "Needs Human Review"
```

#### Rule 5: Has Sufficient Information for Review → **Needs Agent Review**
```
IF issue has a description
AND issue is on the project board
AND no outstanding clarifying questions have been posted
THEN status should be "Needs Agent Review"
```

#### Rule 6: Default (New/Untracked) → **Triage**
```
IF issue is not on the project board
OR none of the above apply
THEN status should be "Triage"
```

### Step 3: Review Issues in "Needs Agent Review"

For each issue in "Needs Agent Review", perform a full review:

1. **Read the issue thoroughly** - understand what is being requested
2. **Assess difficulty** - determine if it's easy, medium, or hard
3. **Check for missing information** - identify any gaps
4. **Decide next action** (mutually exclusive - pick ONE):
   - If ANY questions needed → post ONLY questions (no plan) → move to **"Needs Human Review"**
   - If NO questions → write implementation plan → move to **"Ready to Implement"**

**CRITICAL: Never mix questions and implementation plans in the same comment.** If you have questions, post only the questions and wait for answers. Only write an implementation plan when you have zero unanswered questions.

**Difficulty Assessment Criteria:**

| Difficulty | Criteria |
|------------|----------|
| **Easy** | Single file change, clear requirements, isolated scope, minimal testing needed |
| **Medium** | Multiple files, some design decisions, moderate testing, touches 1-2 modules |
| **Hard** | Architectural changes, complex logic, extensive testing, cross-cutting concerns |

**Completeness Check:**
- Does it have clear acceptance criteria?
- Are reproduction steps provided (for bugs)?
- Is the scope well-defined?
- Are there conflicting requirements?

### Step 4: Take Actions Based on Review

**For issues needing clarification (move to "Needs Human Review"):**

**Important:** Always use temp files for GitHub comments. Inline comment syntax with special characters breaks easily.

```bash
# Add difficulty label first
gh issue edit <number> --add-label "difficulty: easy|medium|hard"

# Write comment to temp file (create directory if needed)
mkdir -p ./.anubis-temp/github
```

Write the comment content to `./.anubis-temp/github/issue-<number>-comment.md`:
```markdown
## Clarification Needed

Thank you for opening this issue. Before I can create an implementation plan, I need some clarification:

1. [Specific question about requirements]
2. [Question about expected behavior]
3. [Question about scope/constraints]

Once these questions are answered, I'll write a detailed implementation plan.
```

```bash
# Post comment using the temp file
gh issue comment <number> --body-file ./.anubis-temp/github/issue-<number>-comment.md

# Move to Needs Human Review on the project board
```

**For issues ready for implementation (move to "Ready to Implement"):**

**Important:** Always use temp files for GitHub comments. Inline comment syntax with special characters breaks easily.

```bash
# Add difficulty label
gh issue edit <number> --add-label "difficulty: easy|medium|hard"

# Write comment to temp file (create directory if needed)
mkdir -p ./.anubis-temp/github
```

Write the implementation plan to `./.anubis-temp/github/issue-<number>-plan.md`:
```markdown
## Implementation Plan

**Difficulty:** [easy|medium|hard]

### Overview
[Brief description of the approach]

### Steps
1. [First implementation step]
2. [Second implementation step]
...

### Files to Modify
- `path/to/file.rs` - [what changes]

### Testing
- [Test case 1]
- [Test case 2]

### Considerations
- [Any edge cases or concerns]
```

```bash
# Post implementation plan using the temp file
gh issue comment <number> --body-file ./.anubis-temp/github/issue-<number>-plan.md

# Move to Ready to Implement on the project board
```

### Step 4a: Verify Status Updates

**CRITICAL:** After updating any issue's board status, always verify the change took effect. The GitHub API can silently fail or changes may not persist.

```bash
# After moving an issue, verify its new status
gh project item-list 8 --owner forrestthewoods --format json | findstr "<issue_number>"

# Or use GraphQL for more precise checking
gh api graphql -f query='{ user(login: "forrestthewoods") { projectV2(number: 8) { items(last: 10) { nodes { id fieldValueByName(name: "Status") { ... on ProjectV2ItemFieldSingleSelectValue { name } } content { ... on Issue { number } } } } } } }'
```

If the status doesn't match what you set, retry the `gh project item-edit` command.

### Checklist for Each Issue Reviewed

Before moving to the next issue, ensure ALL of these are complete:

- [ ] Difficulty label added (`gh issue edit <number> --add-label "difficulty: X"`)
- [ ] Comment posted (questions OR implementation plan, never both)
- [ ] Board status updated (`gh project item-edit ...`)
- [ ] **Status update verified** (check the board to confirm change took effect)

Do not batch these operations across multiple issues. Complete the full checklist for one issue before starting on the next.

### Step 5: Detect Issues with Active Branches

Scan for issues that have implementation work in progress:

```bash
# List all remote branches
git ls-remote --heads origin

# For each issue, check if there's a matching branch
# Branch patterns to look for:
# - claude/issue-<number>-*
# - issue-<number>-*
# - feature/<number>-*
# - fix/<number>-*
```

Issues with active branches should be moved to "Needs Code Review".

### Step 6: Generate Status Sync Report

```markdown
## Issue Status Sync Report

### Status Mismatches (Need Update)

| Issue | Title | Current Status | Correct Status | Reason |
|-------|-------|----------------|----------------|--------|
| #25 | Add caching | Needs Agent Review | Needs Code Review | Has active branch |
| #18 | Fix build | Needs Code Review | Ready to Implement | Branch was deleted |
| #12 | New feature | Triage | Needs Human Review | Questions posted 3 days ago |

### Issues with Active Branches

| Issue | Branch | PR | Status Should Be |
|-------|--------|-----|------------------|
| #25 | claude/issue-25-caching | #31 | Needs Code Review |
| #30 | claude/issue-30-parallel | - | Needs Code Review |

### Issues Needing Agent Review

| Issue | Title | Difficulty | Action Needed |
|-------|-------|------------|---------------|
| #8 | Add --verbose flag | Medium | Write implementation plan |
| #14 | Improve error handling | Easy | Write implementation plan |

### Issues in Needs Human Review

| Issue | Title | Days Waiting | Question Summary |
|-------|-------|--------------|------------------|
| #12 | Support ARM64 | 3 | Asked about target platforms |
| #15 | New config format | 7 | Asked about backwards compat |

### By Difficulty

| Difficulty | Count | Issues |
|------------|-------|--------|
| Easy | 5 | #3, #7, #10, #12, #20 |
| Medium | 8 | #4, #8, #11, #14, #15, #18, #22, #25 |
| Hard | 3 | #5, #9, #30 |
| Unlabeled | 2 | #1, #2 |
```

### Step 7: Generate Final Summary

```markdown
## Issue Review Summary

### Board Sync Status
- **Total Open Issues:** 20
- **Correctly Categorized:** 15
- **Need Status Update:** 5

### Actions Taken
- Reviewed issues: #8, #14, #22
- Posted clarifying questions: #12, #15 → Moved to "Needs Human Review"
- Wrote implementation plans: #8, #14 → Moved to "Ready to Implement"
- Added difficulty labels: #1, #2, #8, #14
- Detected active branches: #25, #30 → Moved to "Needs Code Review"

### Issues Ready for Work
**Easy (Quick Wins):**
- #3 - Fix typo in error message
- #7 - Update help text

**Medium:**
- #8 - Add --verbose flag (plan written)
- #14 - Improve error handling (plan written)

**Hard:**
- #9 - Refactor job system (plan written)

### Issues Needing Human Input
- #12 - Waiting for ARM64 target clarification (3 days)
- #15 - Waiting for backwards compat decision (7 days)
```

## Status Detection Examples

### Example 1: Issue with Active Branch
```
Issue #25: "Add build caching"
- Current board status: Needs Agent Review
- Has branch: claude/issue-25-add-caching
- Has open PR #31

→ Correct status: Needs Code Review
→ Action: Update board status
```

### Example 2: Issue with Questions Pending
```
Issue #12: "Support ARM64"
- Current board status: Needs Agent Review
- Agent posted "## Clarification Needed" 3 days ago
- No response from author yet

→ Correct status: Needs Human Review
→ Action: Update board status
```

### Example 3: Issue with Implementation Plan
```
Issue #8: "Add --dry-run flag"
- Current board status: Needs Agent Review
- Has comment with "## Implementation Plan"
- Plan includes steps and files to modify
- Has "difficulty: easy" label

→ Correct status: Ready to Implement
→ Action: Update board status
```

### Example 4: New Issue Ready for Review
```
Issue #14: "Log compilation times"
- Not on project board yet
- Has clear description and acceptance criteria
- No questions needed

→ Add to project board
→ Move to: Needs Agent Review
→ Action: Review issue, assess difficulty, write plan
```

### Example 5: Issue After Human Response
```
Issue #12: "Support ARM64"
- Current board status: Needs Human Review
- Agent asked questions 5 days ago
- Author responded 1 day ago with answers

→ Correct status: Needs Agent Review (for follow-up review)
→ Action: Agent should review response and write plan
```

### Example 6: WRONG - Mixing Questions and Plan (Anti-pattern)
```
Issue #20: "Add parallel builds"
- Agent posted comment with BOTH:
  - "## Implementation Plan" with partial steps
  - "## Open Questions" asking about thread count

→ THIS IS WRONG - never mix questions and plans
→ Correct action: Post ONLY questions, move to "Needs Human Review"
→ Wait for answers, THEN post implementation plan
```

## Branch Naming Convention

When implementing an issue, create a branch following this pattern:
```
claude/issue-<number>-<short-description>
```

Examples:
- `claude/issue-25-add-caching`
- `claude/issue-12-arm64-support`
- `claude/issue-8-dry-run-flag`

This naming convention allows automatic detection of active implementation work.

## Guidelines

- **Always verify status updates** - After calling `gh project item-edit`, verify the status actually changed by querying the board. The API can silently fail. Never assume a command succeeded just because it returned no error.
- **Complete one issue fully before moving to the next** - Don't batch operations across issues. For each issue: add label → post comment → update status → verify status → then move to next issue.
- **Never mix questions and implementation plans** - If you have ANY questions about an issue, post ONLY the questions as a comment and move to "Needs Human Review". Do NOT include a partial plan. Only write an implementation plan when all questions have been answered.
- **Always use temp files for GitHub comments** - Write comment content to `./.anubis-temp/github/` and use `gh issue comment --body-file`. Inline `--body` syntax with slashes, backticks, and special characters breaks easily.
- Always check for active branches first - this indicates implementation is in progress
- Be respectful and constructive in all comments
- Implementation plans should be detailed enough for any agent to follow
- Consider existing architecture when estimating difficulty
- Look at related code before categorizing
- Check if issues are duplicates or related to existing work
- If unsure about difficulty, err on the side of marking as harder
- Prioritize getting the board status correct over other actions
- When human responds to clarifying questions, move issue back to "Needs Agent Review" for follow-up

## Detecting Active Branches

Check for branches that reference issue numbers:

```bash
# List all remote branches with issue numbers
git ls-remote --heads origin | grep -E 'issue-[0-9]+|#[0-9]+|-[0-9]+-'

# Check specific issue
git ls-remote --heads origin | grep -i "<number>"
```

Branch patterns that indicate active work:
- `claude/issue-<number>-*`
- `feature/issue-<number>-*`
- `fix/issue-<number>-*`
- `*-issue-<number>-*`

## Example Clarifying Questions

For a bug report:
- "What version of Anubis are you using?"
- "Can you share the exact error message?"
- "What operating system are you on?"
- "Can you share a minimal reproduction case?"

For a feature request:
- "What problem does this solve for you?"
- "Are there any constraints we should consider?"
- "How should this interact with [existing feature]?"
- "What's the expected behavior when [edge case]?"
