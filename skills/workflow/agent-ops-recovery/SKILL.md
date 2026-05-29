---
name: agent-ops-recovery
description: "Handle failures and errors during workflow. Use when build breaks, tests fail unexpectedly, or agent gets stuck. Semi-automatic recovery with user confirmation for destructive actions."
category: git
invokes: [agent-ops-state, agent-ops-git, agent-ops-tasks, agent-ops-debugging]
invoked_by: []
state_files:
  read: [constitution.md, baseline.md, focus.md, issues/*.md]
  write: [focus.md, issues/*.md, memory.md]
---

# Error Recovery workflow

## Trigger conditions

Use this skill when:
- Build/lint fails unexpectedly after agent changes
- Tests fail that were passing in baseline
- Agent encounters ambiguity it cannot resolve
- Implementation is stuck or going in circles

## Recovery procedure

### Step 1: Diagnose (invoke debugging)

**For non-trivial failures, invoke `agent-ops-debugging`:**

1. Apply systematic debugging process:
   - Reproduce the issue consistently
   - Define expected vs actual behavior
   - Form hypothesis about root cause
2. Use debugging output to inform recovery decision
3. If root cause unclear after initial analysis, continue debugging before recovery

### Step 2: Assess rollback options

- **Option A**: Fix forward — issue is minor, can be resolved quickly
- **Option B**: Partial rollback — revert specific file(s) to last good state
- **Option C**: Full rollback — revert all agent changes since checkpoint
- **Option D**: Escalate — document the issue, mark task blocked, ask user

### Step 3: Propose action

Present options to user with:
- What will be reverted/changed
- Risk assessment
- Recommendation

### Step 4: Execute (with confirmation)

- For non-destructive actions (fix forward): proceed
- For destructive actions (rollback): **ask user first**
- Update `.agent/focus.md` with recovery action taken

## Destructive actions (require confirmation)

- `git reset`
- `git checkout -- <file>` (discard changes)
- `git revert`
- Deleting files
- Overwriting files with previous versions

## Non-destructive actions (can proceed)

- `git stash`
- Reading files
- Running diagnostics
- Updating focus/tasks with findings

## Post-recovery

1. Update `.agent/focus.md` with what happened
2. Invoke `agent-ops-tasks` to create issue for root cause investigation
3. Update `.agent/memory.md` with "pitfall to avoid" if applicable
4. Re-run baseline comparison before continuing

## Issue Discovery After Recovery

**After recovery, invoke `agent-ops-tasks` discovery procedure:**

1) **Create issue for the incident:**
   ```
   📋 Recovery completed. Create issue to track root cause?
   
   Suggested:
   - [BUG] Investigate: {description of what failed}
     - What happened: {failure description}
     - Recovery action: {what was done}
     - Root cause: TBD
   
   Create this issue? [Y]es / [N]o
   ```

2) **If pattern detected, create prevention issue:**
   ```
   This failure pattern has occurred before. Create improvement issue?
   
   - [CHORE] Add validation to prevent {failure type}
   - [TEST] Add regression test for {scenario}
   
   Create these? [A]ll / [S]elect / [N]one
   ```

3) **After creating issues:**
   ```
   Created {N} issues for tracking. What's next?
   
   1. Investigate root cause now (BUG-0024@abc123)
   2. Continue with original work (defer investigation)
   3. Review recovery actions
   ```
