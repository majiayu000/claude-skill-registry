---
name: pm-pr-workflow
version: "1.0.0"
description: Branch protection and PR creation workflow
when_to_use: PR creation, branch operations, git push to main
category: pm-workflow
tags: [git, pr, branch-protection, pm-required]
---

# PR Workflow and Branch Protection

## Branch Protection Enforcement

**CRITICAL**: PM must enforce branch protection for main branch.

### Detection (run before any main branch operation)

```bash
git config user.email
```

### Routing Rules

- User is `bobmatnyc@users.noreply.github.com` → Can push directly to main (if explicitly requested)
- Any other user → MUST use feature branch + PR workflow

### User Request Translation

When non-privileged users request main branch operations:

| User Request | PM Action |
|--------------|-----------|
| "commit to main" | "Creating feature branch workflow instead" |
| "push to main" | "Branch protection requires PR workflow" |
| "merge to main" | "Creating PR for review" |

**Error Prevention**: PM proactively guides non-privileged users to correct workflow (don't wait for git errors).

## PR Workflow Delegation

**Default**: Main-based PRs (unless user explicitly requests stacked)

### When User Requests PRs

- Single ticket → One PR (no question needed)
- Independent features → Main-based (no question needed)
- User says "stacked" or "dependent" → Stacked PRs (no question needed)

### Recommend Main-Based When

- User doesn't specify preference
- Independent features or bug fixes
- Multiple agents working in parallel
- Simple enhancements

### Recommend Stacked PRs When

- User explicitly requests "stacked" or "dependent" PRs
- Large feature with clear phase dependencies
- User is comfortable with rebase workflows

Always delegate to version-control agent with strategy parameters.

## PR Creation Workflow

When creating PRs, delegate to version-control agent with:

```
Task:
  agent: "version-control"
  task: "Create PR for {feature}"
  context: |
    Work completed: {summary}
    Files changed: {file_list}
    Tests: {test_status}
    QA verification: {qa_evidence}
  acceptance_criteria:
    - Create feature branch from main
    - Push all commits to feature branch
    - Create PR with proper description
    - Link ticket if applicable
    - Request reviews if needed
```

## Common Patterns

### Single Feature PR
```bash
# Feature branch → PR → Main
feature/user-auth → PR #123 → main
```

### Stacked PRs (when requested)
```bash
# Stacked feature development
feature/auth-base → PR #123 → main
feature/oauth (based on auth-base) → PR #124 → feature/auth-base
feature/session (based on oauth) → PR #125 → feature/oauth
```

### Bug Fix PR
```bash
# Hotfix branch → PR → Main
fix/login-error → PR #126 → main
```

## Branch Protection Checklist

Before any main branch operation:
- [ ] Check git user email
- [ ] Verify user has main branch access
- [ ] If not privileged user, route to feature branch workflow
- [ ] Create clear user messaging about branch protection

## Integration with Git File Tracking

All file tracking should happen on feature branches before PR creation:

1. Agent creates files
2. PM tracks files immediately (git add + commit)
3. PM delegates PR creation to version-control
4. version-control pushes branch and creates PR

This ensures all work is tracked before entering PR workflow.
