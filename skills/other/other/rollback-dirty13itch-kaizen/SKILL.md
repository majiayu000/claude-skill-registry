---
name: rollback
description: Emergency rollback for Kaizen deployments
---
Rollback procedure. Determine scope from $ARGUMENTS:

**Single deployment**: `kubectl rollout undo deployment/<name> -n <namespace>`
**Namespace**: Roll back all deployments in namespace
**Full stack**: Run rollback script if available, otherwise:
  1. `kubectl rollout undo` all deployments
  2. `git log --oneline -10` to identify last good commit
  3. `git revert HEAD` if needed
  4. Re-apply from last known good state

Always confirm the rollback target before executing.
