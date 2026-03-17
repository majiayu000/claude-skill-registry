---
name: rollback-procedures
description: Use when the Production Engineer is planning rollback strategies, reverting a bad release, handling data migration reversals, managing feature flags, implementing hotfix workflows, or preparing disaster recovery procedures. Activates when discussing rollbacks, reverts, or recovery from failed deployments.
version: 1.0.0
---

# Rollback Procedures

## When This Applies

Apply this guidance when:
- Planning rollback strategies before a merge
- Reverting a problematic release
- Handling failed deployments
- Managing emergency hotfixes
- Preparing disaster recovery plans

## Rollback Strategy Selection

### Decision Tree

```
Was the issue detected before push to production?
  YES → git reset or revert locally
  NO  → Was data affected?
    NO  → Simple git revert
    YES → Data migration reversal needed
      → Is the migration reversible?
        YES → Run reverse migration + git revert
        NO  → Manual data fix + hotfix
```

### Rollback Methods

| Method | When | Command | Risk |
|--------|------|---------|------|
| **Git revert** | After push, no data impact | `git revert <commit>` | Low |
| **Branch reset** | Before push | `git reset --hard <commit>` | Medium |
| **Revert merge** | Bad merge to main | `git revert -m 1 <merge-commit>` | Medium |
| **Hotfix** | Partial fix needed | New hotfix branch | Low |
| **Full rollback** | Everything is broken | Redeploy previous version | High |

## Git Revert Process

### Simple Revert (single commit)
```bash
git checkout main
git revert <commit-hash>
git push origin main
```

### Merge Revert (undo a merge)
```bash
# -m 1 means keep the main branch's parent
git checkout main
git revert -m 1 <merge-commit-hash>
git push origin main
```

### After Reverting a Merge

If the original work needs to be re-merged later:
```bash
# First, revert the revert to restore the changes
git revert <revert-commit-hash>
# Then apply fixes
# Then merge normally
```

## Hotfix Workflow

For urgent fixes that can't wait for the normal workflow:

1. Create hotfix branch from main: `git checkout -b hotfix/NNN-description main`
2. Apply the minimal fix
3. Run ALL tests
4. Notify Manager (via queue) about the emergency change
5. Merge to main: `git checkout main && git merge --no-ff hotfix/NNN-description`
6. Push: `git push origin main`
7. Also merge to development to keep branches in sync
8. Delete hotfix branch
9. Document in CHANGELOG.md and create a post-incident report

## Pre-Merge Rollback Planning

Before every merge to main, prepare:

1. **Rollback command** — The exact git command to revert
2. **Verification steps** — How to confirm the rollback worked
3. **Data considerations** — Whether data changes need reversing
4. **Communication plan** — Who to notify and how
5. **Estimated time** — How long a rollback would take

## Incident Response

If a production issue is discovered after merge:

1. **Assess severity** — Is the service down? Is data corrupted? Is it cosmetic?
2. **Decide action** — Rollback vs hotfix vs wait
3. **Execute** — Perform the chosen action
4. **Verify** — Confirm the issue is resolved
5. **Communicate** — Notify all roles via queue with `critical` priority
6. **Document** — Write incident report

### Severity Guide

| Severity | Description | Response Time | Action |
|----------|-------------|---------------|--------|
| P0 | Service down | Immediate | Rollback now |
| P1 | Major feature broken | Within minutes | Rollback or hotfix |
| P2 | Minor feature affected | Within session | Hotfix |
| P3 | Cosmetic issue | Next sprint | Normal fix |
