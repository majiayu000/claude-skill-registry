---
name: rollback-protocol
description: Git checkpoint strategy, recovery procedures, and state preservation rules for project rollbacks
---

# Rollback Protocol Skill
# Project Autopilot - Checkpoint and recovery procedures
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Reference this skill for checkpoint creation, rollback execution, and state preservation during recovery operations.

---

## Checkpoint Strategy

### Automatic Checkpoints

Checkpoints are created automatically at these events:

| Event | Tag Format | Trigger |
|-------|------------|---------|
| Phase complete | `autopilot/phase-XXX-complete` | Phase exit gate passes |
| Build complete | `autopilot/build-complete` | All phases finish |
| Manual save | `autopilot/checkpoint-YYYYMMDD-HHMM` | User request |

### Tag Naming Convention

```
autopilot/phase-001-complete
autopilot/phase-002-complete
autopilot/phase-003-complete
autopilot/checkpoint-20260129-1430
autopilot/build-complete-v1.0.0
```

### Checkpoint Creation

```
FUNCTION createCheckpoint(phase, reason):

    # 1. Verify clean state
    IF git.hasUncommittedChanges():
        git.add(".")
        git.commit("chore: checkpoint before phase {phase} complete")

    # 2. Create annotated tag
    tagName = "autopilot/phase-{phase}-complete"
    message = """
    Phase {phase} complete

    Reason: {reason}
    Timestamp: {now()}
    Tasks completed: {taskCount}
    Cost: ${actualCost}
    """

    git.tag("-a", tagName, "-m", message)

    # 3. Record in STATE.md
    updateState({
        lastCheckpoint: tagName,
        checkpointTime: now(),
        checkpointReason: reason
    })

    # 4. Optionally push tag
    IF config.autoPushTags:
        git.push("origin", tagName)

    LOG "📌 Checkpoint created: {tagName}"
```

---

## Rollback Procedures

### Soft Rollback (Default)

Preserves history, creates backup:

```
FUNCTION softRollback(targetPhase):

    # 1. Create backup branch
    backupBranch = "autopilot-backup-{timestamp}"
    git.branch(backupBranch)

    # 2. Identify target checkpoint
    checkpoint = "autopilot/phase-{targetPhase}-complete"

    # 3. Get commits to revert
    commits = git.log("{checkpoint}..HEAD", "--oneline")

    # 4. Revert each commit (in reverse order)
    FOR each commit IN commits.reverse():
        git.revert(commit.sha, "--no-commit")

    # 5. Commit the revert
    git.commit("Rollback to phase {targetPhase} (from phase {currentPhase})")

    # 6. Update state
    updateStateForRollback(targetPhase)
```

### Hard Rollback

Rewrites history (use with caution):

```
FUNCTION hardRollback(targetPhase):

    # 1. Create backup branch (always)
    backupBranch = "autopilot-backup-{timestamp}"
    git.branch(backupBranch)

    # 2. Reset to checkpoint
    checkpoint = "autopilot/phase-{targetPhase}-complete"
    git.reset("--hard", checkpoint)

    # 3. Update state
    updateStateForRollback(targetPhase)

    # WARNING: This requires force push if already pushed
    # git push --force origin {branch}
```

---

## State Preservation

### What to Preserve

| Item | Preserve? | Reason |
|------|-----------|--------|
| learnings.md | ✅ Yes | Knowledge is valuable regardless of rollback |
| Global history | ✅ Yes | Maintains accurate project record |
| Estimation data | ✅ Yes | Improves future estimates |
| Phase files (future) | ❌ No | Will be recreated |
| Cost data (rolled back) | ✅ Mark | Track as "rolled back" not delete |

### Learnings Preservation

```
FUNCTION preserveLearnings():

    # 1. Read current learnings
    learnings = readFile(".autopilot/learnings.md")

    # 2. Add rollback note
    learnings += """

    ---
    ## Rollback Note ({timestamp})
    Rolled back from phase {fromPhase} to phase {toPhase}.
    Reason: {reason}

    ### Insights from rolled-back work:
    - [Any valuable learnings from phases that were reverted]
    """

    # 3. Store temporarily
    STORE learnings for restoration after rollback
```

### Global History Update

```
FUNCTION recordRollbackInHistory(projectId, fromPhase, toPhase):

    history = readJSON("~/.claude/autopilot/history.json")

    project = history.autopilots.find(p => p.id == projectId)

    # Add rollback event
    project.rollbacks = project.rollbacks OR []
    project.rollbacks.push({
        timestamp: now(),
        fromPhase: fromPhase,
        toPhase: toPhase,
        costAtRollback: project.costs.actual,
        reason: "user_initiated"
    })

    # Adjust phase counts
    project.phases.completed = toPhase

    # Mark cost as partially rolled back
    project.costs.rolledBack = project.costs.actual - costAtPhase(toPhase)

    writeJSON("~/.claude/autopilot/history.json", history)
```

---

## State File Updates

### STATE.md After Rollback

```markdown
# Context Checkpoint
**Saved:** [Timestamp]
**Reason:** rollback

## Current State
- **Phase:** [target phase] of [total] - [Phase Name]
- **Last Task Completed:** [last task of target phase]
- **Next Task:** [first task of next phase]
- **Context Used:** ~10%

## Rollback Information
| Metric | Value |
|--------|-------|
| Rolled back from | Phase [X] |
| Rolled back to | Phase [Y] |
| Rollback time | [Timestamp] |
| Backup branch | autopilot-backup-YYYYMMDD-HHMM |
| Cost before rollback | $[X] |
| Cost after rollback | $[Y] |

## Resume Instructions
```bash
/autopilot:cockpit  # Continue from phase [Y+1]
```
```

### Phase Files Cleanup

```
FUNCTION cleanPhaseFiles(startPhase, endPhase):

    FOR phase FROM startPhase TO endPhase:
        phaseFile = ".autopilot/phases/phase-{phase}.md"

        IF exists(phaseFile):
            # Reset to template state
            resetPhaseFile(phaseFile)

        # Or delete if past original scope
        IF phase > originalMaxPhase:
            deleteFile(phaseFile)
```

---

## Recovery Scenarios

### Recover from Bad Rollback

```bash
# Find backup branch
git branch -a | grep autopilot-backup

# View what was lost
git log autopilot-backup-20260129-1430..HEAD

# Restore from backup
git checkout autopilot-backup-20260129-1430

# Or cherry-pick specific commits
git cherry-pick abc1234
```

### Partial Rollback (Single Task)

Not recommended, but possible:

```bash
# Revert specific commit
git revert abc1234

# Update STATE.md manually
# Re-run task with /autopilot:cockpit --task=X.Y
```

### Rollback with Merge Conflicts

```
FUNCTION handleRollbackConflicts(conflicts):

    LOG "Merge conflicts detected in rollback"

    # List conflicted files
    FOR each file IN conflicts:
        LOG "Conflict: {file}"

    # Provide options
    DISPLAY """
    ## Rollback Conflicts

    **Options:**
    1. Resolve manually:
       ```bash
       # Edit conflicted files
       git add .
       git commit -m "Resolved rollback conflicts"
       ```

    2. Abort rollback:
       ```bash
       git checkout {backupBranch}
       ```

    3. Force overwrite (loses local changes):
       ```bash
       git checkout --theirs .
       git add .
       git commit -m "Rollback with remote versions"
       ```
    """
```

---

## Best Practices

### When to Use Rollback

| Situation | Recommendation |
|-----------|----------------|
| Wrong implementation approach | ✅ Rollback, re-plan |
| Test failures in new phase | ❌ Fix forward |
| Budget exceeded | ✅ Rollback to safe point |
| User changed requirements | ✅ Rollback, re-scope |
| Minor bugs | ❌ Fix forward |
| Architecture issues | ✅ Rollback early |

### Rollback Checklist

Before rolling back:
- [ ] Backup branch created
- [ ] Learnings documented
- [ ] Uncommitted changes handled
- [ ] Team notified (if collaborative)
- [ ] Reason documented

After rolling back:
- [ ] STATE.md updated
- [ ] Phase files cleaned
- [ ] Global history updated
- [ ] Resume tested

---

## Integration Points

### With /autopilot:cockpit

After rollback:
```bash
/autopilot:cockpit  # Picks up from new position
```

### With /autopilot:altitude

Shows rollback history:
```markdown
## Rollback History
| Date | From | To | Reason |
|------|------|-----|--------|
| Jan 29 | Phase 5 | Phase 3 | Re-architecture |
```

### With /autopilot:compare

Excludes rolled-back costs from accuracy:
```
Actual cost: $4.85 (excluding $2.70 rolled back)
```

---

## Error Prevention

### Pre-Rollback Validation

```
FUNCTION validateRollback(targetPhase):

    errors = []

    # Check checkpoint exists
    IF NOT checkpointExists(targetPhase):
        errors.push("No checkpoint for phase {targetPhase}")

    # Check for uncommitted changes
    IF git.hasUncommittedChanges():
        errors.push("Uncommitted changes exist")

    # Check target is in the past
    IF targetPhase >= currentPhase:
        errors.push("Target phase must be before current phase")

    # Check not on main with unpushed changes
    IF git.branch() == "main" AND git.hasUnpushedCommits():
        errors.push("Unpushed commits on main - push or create branch first")

    IF errors.length > 0:
        DISPLAY errors
        RETURN false

    RETURN true
```
