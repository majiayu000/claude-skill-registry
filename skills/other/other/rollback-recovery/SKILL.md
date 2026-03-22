---
name: rollback-recovery
description: Handling failed deployments, reverting changes, and recovery procedures
category: DevOps Operations
---

# Skill: rollback-recovery

## What I do

I provide the expertise to swiftly undo problematic changes and recover systems after a failure. I focus on developing clear rollback procedures, testing recovery paths, and ensuring that any deployment can be safely reversed to restore service stability.

## When to use me

- Immediately after a failed deployment or release
- To develop a rollback plan for a high-risk change
- When a production incident is triggered by a recent configuration update
- To test disaster recovery procedures in a staging environment
- When a database migration or schema change fails

## Core principles

1. **Test your rollback** — A rollback plan is not a plan until it has been successfully tested in a staging environment.
2. **Time to Recover (TTR)** — Focus on minimising the time it takes to restore service, even if the root cause is not yet known.
3. **Immutability and State** — Understand the impact of rollbacks on persistent data and state. Reverting code is easy; reverting data is hard.
4. **Kill Switches and Flags** — Use feature flags or kill switches to disable problematic functionality without a full deployment rollback.

## Patterns & examples

**Rollback Decision Criteria:**
- **Critical Failure**: Core functionality is broken for all users.
- **Widespread Regressions**: Multiple non-critical but important features are broken.
- **Data Corruption**: A change is causing incorrect data to be written.
- **Performance Collapse**: Service response times are making the system unusable.

**Rollback Sequence:**
1. **Identify**: Recognise the failure via monitoring or user reports.
2. **Evaluate**: Quickly decide if "fixing forward" or rolling back is the safest path.
3. **Execute**: Perform the rollback procedure (e.g., `git revert`, `helm rollback`, or blue/green toggle).
4. **Verify**: Ensure service is restored and no new issues are introduced by the rollback itself.

**Git Revert vs. Reset Pattern:**
```bash
# ✅ Correct: Use git revert for shared history to maintain a clear audit trail
git revert <commit_hash>
git push origin main

# ❌ Wrong: Using git reset --hard on a shared branch can break other developers' local copies
# git reset --hard <previous_commit_hash>
# git push origin main --force
```

## Anti-patterns to avoid

- ❌ **"Hope as a strategy"** — Deploying changes without a clear, documented rollback plan.
- ❌ **Ignoring data rollbacks** — Failing to consider how to revert database migrations or schema changes.
- ❌ **Manual-only rollbacks** — Relying on complex, manual steps to revert a change during an emergency.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/DevOps-Operations/Rollback Recovery.md`

## Related skills

- `incident-response` — Coordinating mitigation and response
- `release-management` — Managing the delivery lifecycle
- `monitoring` — Detecting failures and verifying recovery
- `feature-flags` — Disabling features without re-deploying
- `devops` — Core infrastructure and deployment patterns
