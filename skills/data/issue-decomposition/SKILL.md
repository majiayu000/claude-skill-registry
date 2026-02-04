---
name: issue-decomposition
description: Use when an issue is too large for a single task - breaks into linked sub-issues with full documentation, ensuring manageable work units
---

# Issue Decomposition

## Overview

Break large issues into manageable sub-issues. Each sub-issue should be completable in a single focused session.

**Core principle:** If an issue is too big, decompose it before starting work.

**Announce at start:** "I'm using issue-decomposition to break this large issue into manageable sub-tasks."

## When to Decompose

An issue is too large when ANY of these are true:

| Indicator | Threshold |
|-----------|-----------|
| Acceptance criteria | More than 5 criteria |
| Areas touched | More than 3 unrelated code areas |
| Estimated work | More than 1 context window |
| Deliverables | Multiple independent features |
| Dependencies | Complex internal sequencing |

**When in doubt, decompose.** Smaller issues are better than larger ones.

## The Decomposition Process

### Step 1: Analyze the Parent Issue

Read the issue thoroughly and identify:

1. **Independent work units** - Things that can be done separately
2. **Dependencies** - What must come before what
3. **Natural boundaries** - Logical separation points
4. **Acceptance criteria groupings** - Which criteria relate to each other

### Step 2: Plan Sub-Issues

Create a decomposition plan:

```markdown
## Decomposition Plan for #[PARENT_NUMBER]

### Sub-Issue 1: [Title]
**Criteria from parent:** 1, 2
**Dependencies:** None
**Deliverable:** [What this sub-issue delivers]

### Sub-Issue 2: [Title]
**Criteria from parent:** 3, 4
**Dependencies:** Sub-Issue 1
**Deliverable:** [What this sub-issue delivers]

### Sub-Issue 3: [Title]
**Criteria from parent:** 5
**Dependencies:** Sub-Issue 2
**Deliverable:** [What this sub-issue delivers]
```

### Step 3: Create Sub-Issues

For each sub-issue:

```bash
gh issue create \
  --title "[Type] [Parent Title] - [Sub-Task Title]" \
  --body "## Description

Part of #[PARENT_NUMBER]: [Parent Title]

[Specific description of this sub-task]

## Acceptance Criteria

- [ ] [Criterion 1 - copied or derived from parent]
- [ ] [Criterion 2]

## Verification Steps

[How to verify this specific sub-task]

## Dependencies

- Requires: #[PREVIOUS_SUB_ISSUE] (if any)
- Blocks: #[NEXT_SUB_ISSUE] (if any)

## Parent Issue

Closes part of #[PARENT_NUMBER]"
```

### Step 4: Label and Link

```bash
# Label sub-issues
gh issue edit [SUB_ISSUE_NUMBER] --add-label "sub-issue"

# Label parent
gh issue edit [PARENT_NUMBER] --add-label "parent"
```

### Step 5: Update Parent Issue

Add to the parent issue body:

```markdown
## Sub-Issues

This issue has been broken down into:

- [ ] #[SUB_1] - [Title]
- [ ] #[SUB_2] - [Title]
- [ ] #[SUB_3] - [Title]

Complete all sub-issues to resolve this parent issue.
```

### Step 6: Add to Project

```bash
# Add all sub-issues to project
gh project item-add [PROJECT_NUMBER] --owner @me --url [SUB_ISSUE_1_URL]
gh project item-add [PROJECT_NUMBER] --owner @me --url [SUB_ISSUE_2_URL]
# etc.

# Set status to Ready (or Backlog if blocked)
```

### Step 7: Update Memory

Store the decomposition in knowledge graph:

```
Entity: Issue [PARENT_NUMBER]
Observation: "Decomposed into sub-issues [X], [Y], [Z] on [DATE]"

Relations:
- Issue [PARENT] --has_sub_issue--> Issue [SUB_1]
- Issue [SUB_1] --blocks--> Issue [SUB_2]
```

## Sub-Issue Quality Checklist

Each sub-issue MUST have:

- [ ] Clear title indicating it's part of parent
- [ ] Reference to parent issue in description
- [ ] Own acceptance criteria (not just "see parent")
- [ ] Own verification steps
- [ ] Dependencies documented (if any)
- [ ] Added to GitHub Project
- [ ] Labeled as `sub-issue`

## Handling Dependencies

When sub-issues have dependencies:

| Dependency Type | Project Status | Notes |
|-----------------|----------------|-------|
| No dependencies | Ready | Can start immediately |
| Blocked by another sub-issue | Backlog | Move to Ready when blocker completes |
| Blocks another sub-issue | Ready | Work on this first |

## After Decomposition

Once decomposition is complete:

1. **Update memory** with decomposition record
2. **Return to Step 1** of `issue-driven-development` with first sub-issue
3. Work through sub-issues in dependency order
4. Close parent issue when all sub-issues are done

## Example Decomposition

**Parent Issue:** #100 - Implement user authentication

**Sub-Issues Created:**

| # | Title | Dependencies | Criteria |
|---|-------|--------------|----------|
| 101 | Auth - Database schema | None | User table, session table |
| 102 | Auth - Registration endpoint | #101 | Signup, validation, storage |
| 103 | Auth - Login endpoint | #101 | Login, session creation |
| 104 | Auth - Logout endpoint | #103 | Session invalidation |
| 105 | Auth - Protected route middleware | #103 | Auth check, redirect |
| 106 | Auth - UI integration | #102, #103, #104, #105 | Forms, state, routing |

## Common Mistakes

| Mistake | Correction |
|---------|------------|
| Sub-issues too vague | Each sub-issue needs specific, verifiable criteria |
| Missing dependencies | Map out order before creating sub-issues |
| Not updating parent | Parent must list all sub-issues |
| Skipping project setup | Each sub-issue must be in project with correct status |
| Criteria duplicated wrong | Derive specific criteria, don't just copy all |
