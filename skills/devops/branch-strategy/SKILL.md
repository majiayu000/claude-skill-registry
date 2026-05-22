---
name: branch-strategy
description: Modern Git branching strategies for 2026. GitHub Flow with feature flags, trunk-based development, and branch lifecycle management.
context: fork
version: 1.0.0
author: SkillForge
tags: [git, branching, github-flow, trunk-based, workflow, feature-flags]
user-invocable: false
---

# Branch Strategy

Modern branching for 2026: GitHub Flow + Feature Flags. Simple, CI/CD-friendly, scales with team size.

## When to Use

- Setting up team workflow
- Deciding on branching model
- Managing feature development
- Planning release process

## Quick Reference: GitHub Flow

```
main ─────●───────●───────●───────●───────●──── (always deployable)
           \     / \     / \     / \     /
            ●───●   ●───●   ●───●   ●───●      (short-lived branches)
           feat    fix     feat    fix
```

**Rules:**
1. `main` is always deployable
2. Branch from `main`, PR back to `main`
3. Branches live < 1-2 days
4. Feature flags hide incomplete work
5. Delete branch after merge

---

## Branch Naming Convention

```bash
# Feature branches (link to issue)
issue/<number>-<brief-description>
issue/123-add-user-auth
issue/456-fix-login-redirect

# When no issue exists
feature/<description>
feature/add-dark-mode

fix/<description>
fix/memory-leak-dashboard

# Hotfix (urgent production fix)
hotfix/<description>
hotfix/security-patch-auth
```

---

## Standard Workflow

### 1. Start Work

```bash
# Always start from fresh main
git checkout main
git pull origin main

# Create feature branch
git checkout -b issue/123-add-user-auth
```

### 2. Do Work (Atomic Commits)

```bash
# Make changes, commit atomically
git add -p
git commit -m "feat(#123): Add User model"

git add -p
git commit -m "feat(#123): Add auth service"

git add -p
git commit -m "test(#123): Add auth unit tests"
```

### 3. Keep Updated

```bash
# Rebase on main regularly (daily)
git fetch origin
git rebase origin/main

# Resolve conflicts if any
# Then continue
git rebase --continue
```

### 4. Push & PR

```bash
# Push feature branch
git push -u origin issue/123-add-user-auth

# Create PR
gh pr create --base main --fill
```

### 5. After Merge

```bash
# Clean up
git checkout main
git pull origin main
git branch -d issue/123-add-user-auth
```

---

## Strategy Comparison

| Strategy | Best For | Pros | Cons |
|----------|----------|------|------|
| **GitHub Flow** | Small-medium teams, web apps | Simple, CI/CD friendly | Needs feature flags |
| **Trunk-Based** | Experienced teams, fast deploys | Minimal branches | Requires discipline |
| **GitFlow** | Legacy, scheduled releases | Clear structure | Complex, slow |

### 2026 Recommendation

```
┌─────────────────────────────────────────────────────────────┐
│  Team Size    │  Recommendation                             │
├───────────────┼─────────────────────────────────────────────┤
│  1-5 devs     │  GitHub Flow (simple)                       │
│  5-20 devs    │  GitHub Flow + Feature Flags                │
│  20+ devs     │  Trunk-Based + Feature Flags                │
│  Regulated    │  GitHub Flow + Release Branches             │
└─────────────────────────────────────────────────────────────┘
```

---

## Feature Flags Pattern

Hide incomplete features behind flags to merge to main safely:

```typescript
// feature-flags.ts
export const FLAGS = {
  NEW_AUTH_SYSTEM: process.env.FF_NEW_AUTH === 'true',
  DARK_MODE: process.env.FF_DARK_MODE === 'true',
};

// Usage in code
if (FLAGS.NEW_AUTH_SYSTEM) {
  return <NewLoginForm />;
} else {
  return <LegacyLoginForm />;
}
```

**Benefits:**
- Merge incomplete work to main
- Test in production with flag off
- Gradual rollout (% of users)
- Instant rollback (flip flag)

---

## Branch Lifecycle

```
┌──────────────────────────────────────────────────────────────┐
│                    BRANCH LIFECYCLE                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  CREATE          DEVELOP           MERGE           DELETE    │
│  ──────          ───────           ─────           ──────    │
│                                                              │
│  git checkout    git add -p        gh pr create    git branch│
│  -b issue/123    git commit        gh pr merge     -d issue/ │
│                  git rebase        --squash        123       │
│                                    --delete-branch           │
│                                                              │
│  Lifespan: 1-3 days maximum                                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Stale Branch Cleanup

```bash
# Find merged branches
git branch --merged main | grep -v main

# Delete merged local branches
git branch --merged main | grep -v main | xargs git branch -d

# Delete remote branches older than 2 weeks
gh pr list --state merged --json headRefName,mergedAt --jq '
  .[] | select(.mergedAt < (now - 1209600 | todate)) | .headRefName
' | xargs -I {} git push origin --delete {}
```

---

## Protected Branch Rules

Configure in GitHub Settings > Branches:

```yaml
main:
  - Require PR before merging
  - Require 1 approval
  - Require status checks:
    - ci/test
    - ci/lint
    - ci/build
  - Require branches to be up to date
  - Do not allow force pushes
  - Do not allow deletions

# Optional for larger teams:
  - Require signed commits
  - Require linear history (squash only)
```

---

## Merge Strategies

| Strategy | When to Use | Result |
|----------|-------------|--------|
| **Squash** | Most PRs | Clean history, 1 commit per PR |
| **Rebase** | Clean atomic commits | Preserves all commits |
| **Merge** | Preserve branch history | Creates merge commit |

**SkillForge Default**: Squash merge for clean history

```bash
# Squash merge (recommended)
gh pr merge 123 --squash --delete-branch

# Auto-merge when checks pass
gh pr merge 123 --auto --squash
```

---

## Anti-Patterns to Avoid

```
❌ Long-lived feature branches (> 1 week)
❌ Merging main into feature (use rebase)
❌ Direct commits to main
❌ Force push to shared branches
❌ Multiple features in one branch
❌ "WIP" commits that break tests
```

---

## Best Practices Summary

1. **Branch from main** - Always start fresh
2. **Short-lived branches** - Merge within 1-3 days
3. **Rebase, don't merge** - Keep history clean
4. **Feature flags** - Merge incomplete work safely
5. **Squash on merge** - One commit per PR
6. **Delete after merge** - No stale branches
7. **Protect main** - Require PRs and checks

## Related Skills

- atomic-commits: Commit best practices
- stacked-prs: Multi-PR workflows
- release-management: Release branching

## References

- [GitHub Flow Guide](references/github-flow.md)
- [Feature Flags](references/feature-flags.md)
- [Branch Protection](references/branch-protection.md)
