---
name: review-pr
description: Review a PR diff for quality, security, and correctness.
---

# Review PR

The Reviewer drives this workflow. Analyze a PR's diff for quality, security, and correctness. Produce structured feedback and a verdict.

**Prerequisites:** PR diff available (pasted or accessible), context about the PR's purpose.

---

## Phase 1: Understand Scope

Understand what the PR is trying to accomplish.

### Steps

1. Read PR title and description
2. Identify the issue being addressed
3. Understand the intended behavior change
4. Note the scope (files, areas affected)

---

## Phase 2: Analyze Changes

Review the implementation against requirements and standards.

### Steps

1. Check structure — Are changes organized logically?
2. Check correctness — Does implementation achieve the goal?
3. Check conventions — Does it follow established patterns?
4. Check security — Any security implications?
5. Check tests — Adequate coverage?

### Review Principles

| Principle             | Application                             |
| --------------------- | --------------------------------------- |
| Focus on what matters | Blocking issues > style nits            |
| Be specific           | File, line, concrete suggestion         |
| Explain why           | Help author understand, not just comply |
| Acknowledge good work | Reinforcement helps                     |
| Stay in scope         | Review what's in the PR, not wishlist   |

---

## Phase 3: Provide Feedback

Present structured, actionable feedback.

### Steps

1. Determine verdict (Approve, Request Changes, Comment)
2. List blocking issues (must fix before merge)
3. List suggestions (non-blocking improvements)
4. Note positive observations

### Feedback Categories

| Category   | Meaning                               |
| ---------- | ------------------------------------- |
| Blocking   | Must be addressed before merge        |
| Important  | Should be addressed, but not blocking |
| Suggestion | Nice to have improvement              |
| Nitpick    | Style preference, optional            |

### Output

````markdown
## Context Anchors

- **PR:** #<number> - <title>
- **Author:** <author>
- **Target:** `<branch>` → `<base>`
- **Scope:** <brief description>

## Review Summary

**Verdict:** <Approve | Request Changes | Comment>

<One paragraph summary>

## Feedback

### Blocking Issues

1. **[File:Line] <Issue title>**
   - Problem: <what's wrong>
   - Suggestion: <how to fix>

### Suggestions

1. **[File:Line] <Suggestion title>**
   - Current: <what it does now>
   - Suggested: <what would be better>

### Positive Notes

- <positive observation>

## Next Step

<If Request Changes: "Address blocking issues and re-request review">
<If Approve: "Ready to merge">
<If Comment: "Consider suggestions; no changes required">

```

### ⛔ CHECKPOINT

**STOP.** Present review for confirmation before posting.

### Board Integration

When issuing an **APPROVE** verdict and merge is confirmed in the same session:

1. Read `workspace.config.yaml` for `board.project_id`, `board.fields.status.field_id`, and `board.status_options.done.option_id`
2. Set issue status to **Done**

Only perform this update if the full approve → merge cycle completes within this review session. If merge is deferred, the Done transition belongs to Orchestrator.

---

## Mechanical Review Checklist

Before providing any review verdict, verify these mechanically:

- [ ] All changed files reviewed (none skipped)
- [ ] Build passes on the branch
- [ ] Tests pass with counts reported
- [ ] No unresolved merge conflicts
- [ ] Commit messages follow conventional format
- [ ] Branch naming follows convention
- [ ] PR description references the issue
- [ ] No `TODO` or `FIXME` markers in new code (unless tracked by issue)

---

## Error Handling

| Error                    | Recovery                                                        |
| ------------------------ | --------------------------------------------------------------- |
| Missing PR context       | Request PR number or diff                                       |
| Unclear feedback         | Ask for clarification                                           |
| Conflicting requirements | Escalate to author/maintainer                                   |

```
````
