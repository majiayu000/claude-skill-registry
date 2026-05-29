---
name: god-intervention
description: "Guides God Committee members through executing interventions. Use for repairs, rollbacks, and emergency actions. Triggers on: intervention, repair, rollback, emergency action."
---

# God Committee Intervention Skill

## Purpose

This skill guides God Committee members through executing interventions - from minor repairs to major system modifications.

## Intervention Severity Levels

### Level 1: Minor Repair

- Fix corrupted files
- Clear stale locks
- Truncate large logs
- Fix permissions

**Consensus Required**: No

### Level 2: Process Control

- Pause execution
- Resume execution
- Terminate specific processes

**Consensus Required**: No (unless terminating all)

### Level 3: Code Modification

- Fix bugs directly
- Update configurations
- Modify skills
- Add documentation

**Consensus Required**: Recommended

### Level 4: Major Rollback

- Revert multiple commits
- Undo PRD progress
- Reset system state

**Consensus Required**: **Yes**

### Level 5: System Termination

- Stop all execution
- Archive project state
- Full system shutdown

**Consensus Required**: **Yes**

## Pre-Intervention Checklist

Before any intervention:

```markdown
## Pre-Intervention Checklist

- [ ] Issue clearly identified and documented
- [ ] Evidence gathered (logs, metrics, observations)
- [ ] Impact assessment completed
- [ ] Rollback plan prepared
- [ ] Consensus obtained (if required)
- [ ] Execution layer paused (if needed)
- [ ] Backup created (if applicable)
```

## Executing Interventions

### Level 1: Minor Repairs

```bash
# Clear stale locks
./scripts/god/powers.sh repair lock

# Clean up worktrees
./scripts/god/powers.sh repair worktrees

# Fix corrupted JSON files
./scripts/god/powers.sh repair json

# Truncate large logs
./scripts/god/powers.sh repair logs

# Fix script permissions
./scripts/god/powers.sh repair permissions

# Clean git state
./scripts/god/powers.sh repair git

# Run all repairs
./scripts/god/powers.sh repair all
```

### Level 2: Process Control

#### Pausing Execution

```bash
# Pause with reason
./scripts/god/powers.sh pause "Investigation needed: failing tests" YOUR_ID

# Check pause status
./scripts/god/powers.sh pause-status
```

#### Resuming Execution

```bash
# Resume execution
./scripts/god/powers.sh resume YOUR_ID
```

#### Terminating Processes

```bash
# Terminate orchestrator
./scripts/god/powers.sh terminate orchestrator YOUR_ID

# Terminate Aha Loop execution
./scripts/god/powers.sh terminate aha-loop YOUR_ID

# Terminate parallel explorer
./scripts/god/powers.sh terminate explorer YOUR_ID

# Terminate specific PID
./scripts/god/powers.sh terminate pid:12345 YOUR_ID

# Force kill (if terminate fails)
./scripts/god/powers.sh kill orchestrator YOUR_ID
```

### Level 3: Code Modification

#### Direct File Edits

For simple modifications:

```bash
# Append to file
./scripts/god/powers.sh modify "path/to/file" append "content" YOUR_ID

# Prepend to file
./scripts/god/powers.sh modify "path/to/file" prepend "content" YOUR_ID

# Replace file contents
./scripts/god/powers.sh modify "path/to/file" replace "new content" YOUR_ID
```

For complex edits, use your AI capabilities to directly edit files.

#### Skill Modifications

```bash
# Disable a skill
./scripts/god/powers.sh modify-skill skill-name disable YOUR_ID

# Re-enable a skill
./scripts/god/powers.sh modify-skill skill-name enable YOUR_ID
```

#### Configuration Updates

Edit `.god/config.json` or project configurations directly:

```bash
# Example: Update quorum
jq '.council.quorum = 3' .god/config.json > tmp && mv tmp .god/config.json
```

### Level 4: Major Rollback

#### Git Rollback

```bash
# Soft reset (keep changes staged)
./scripts/god/powers.sh rollback HEAD~3 soft YOUR_ID

# Mixed reset (keep changes unstaged)
./scripts/god/powers.sh rollback HEAD~3 mixed YOUR_ID

# Hard reset (discard all changes)
./scripts/god/powers.sh rollback HEAD~3 hard YOUR_ID

# Rollback to specific commit
./scripts/god/powers.sh rollback abc123 soft YOUR_ID
```

#### Restore from Stash

```bash
./scripts/god/powers.sh restore-stash YOUR_ID
```

#### PRD Rollback

To rollback PRD progress:

1. Update `project.roadmap.json`:
   ```bash
   jq '.prds |= map(if .id == "prd-xxx" then .status = "pending" else . end)' \
     project.roadmap.json > tmp && mv tmp project.roadmap.json
   ```

2. Reset story status in PRD:
   ```bash
   jq '.stories |= map(.status = "pending")' \
     docs/prd/xxx/prd.json > tmp && mv tmp docs/prd/xxx/prd.json
   ```

### Level 5: System Termination

**⚠️ This requires consensus and should be rare.**

```bash
# Step 1: Pause everything
./scripts/god/powers.sh pause "System termination initiated" YOUR_ID

# Step 2: Terminate all processes
./scripts/god/powers.sh terminate all YOUR_ID

# Step 3: Stop awakener daemon
./scripts/god/awakener.sh stop

# Step 4: Create final state snapshot
./scripts/god/observer.sh snapshot
./scripts/god/observer.sh report

# Step 5: Archive (optional)
git tag -a "god-committee-termination-$(date +%Y%m%d)" -m "System terminated by God Committee"

# Step 6: Log final entry
./scripts/god/observer.sh event "termination" "System terminated by God Committee"
```

## Intervention Patterns

### Pattern 1: Investigate and Fix

```
1. Pause execution
2. Take snapshot
3. Investigate issue
4. Fix the problem
5. Verify fix
6. Resume execution
7. Monitor for recurrence
```

### Pattern 2: Rollback and Retry

```
1. Pause execution
2. Take snapshot
3. Identify rollback point
4. Execute rollback
5. Clear any bad state
6. Modify approach if needed
7. Resume execution
```

### Pattern 3: Emergency Stop and Repair

```
1. Terminate offending process immediately
2. Take snapshot
3. Assess damage
4. Run repairs
5. Notify other members
6. Plan recovery
7. Execute recovery
8. Resume with monitoring
```

## Post-Intervention Protocol

After any intervention:

### 1. Document the Intervention

```markdown
## Intervention Report

### Intervention ID
int-[timestamp]

### Type
[repair|process_control|code_modification|rollback|termination]

### Severity
[1-5]

### Triggered By
[observation|alert|proposal|emergency]

### Description
[What was done]

### Reason
[Why it was necessary]

### Steps Taken
1. [Step 1]
2. [Step 2]
3. ...

### Outcome
[Success/Partial/Failed]

### Side Effects
[Any unintended consequences]

### Follow-up Required
[Yes/No - if yes, what]

### Lessons Learned
[What we learned]
```

### 2. Log the Event

```bash
./scripts/god/observer.sh event "intervention" "DESCRIPTION"
```

### 3. Notify Other Members

```bash
./scripts/god/council.sh send YOUR_ID "other,members" "directive" \
  "Intervention Completed" "SUMMARY"
```

### 4. Update Status

```bash
# Check intervention history
./scripts/god/powers.sh history interventions 10

# Review repair history
./scripts/god/powers.sh history repairs 10
```

### 5. Monitor for Recurrence

Set up a follow-up observation:

```bash
# Trigger immediate observation
./scripts/god/awakener.sh random

# Or use a scheduled check type
./scripts/god/awakener.sh scheduled daily
```

## Common Intervention Scenarios

### Scenario: Failing Tests

```bash
# 1. Check current state
./scripts/god/observer.sh check

# 2. Pause if needed
./scripts/god/powers.sh pause "Investigating test failures"

# 3. Analyze failures
cat test-results.json | jq '.failures'

# 4. Decide action:
#    - Minor fix: edit directly
#    - Major issue: rollback
#    - Need discussion: create proposal

# 5. Execute fix/rollback

# 6. Verify
npm test  # or equivalent

# 7. Resume
./scripts/god/powers.sh resume
```

### Scenario: Stuck Process

```bash
# 1. Identify stuck process
ps aux | grep -E "(aha-loop.sh|orchestrator|explorer)"

# 2. Check how long it's been running
# 3. Check for output/progress

# 4. If stuck, terminate
./scripts/god/powers.sh terminate pid:XXXXX

# 5. Clean up any locks
./scripts/god/powers.sh repair lock

# 6. Restart if appropriate
./scripts/aha-loop/orchestrator.sh --continue
```

### Scenario: Corrupted State

```bash
# 1. Stop everything
./scripts/god/powers.sh pause "Corrupted state detected"
./scripts/god/powers.sh terminate all

# 2. Assess damage
./scripts/god/powers.sh repair json  # Check for JSON issues
git status  # Check git state

# 3. Decide rollback point
git log --oneline -20

# 4. Execute rollback
./scripts/god/powers.sh rollback COMMIT_HASH hard

# 5. Run repairs
./scripts/god/powers.sh repair all

# 6. Verify
./scripts/god/observer.sh check

# 7. Resume
./scripts/god/powers.sh resume
```

## Safety Guidelines

### Always

- ✅ Document before acting
- ✅ Take snapshots before major changes
- ✅ Verify after intervention
- ✅ Notify other members of significant actions
- ✅ Have a rollback plan

### Never

- ❌ Make major rollbacks without consensus
- ❌ Terminate system without documentation
- ❌ Skip verification after fixes
- ❌ Hide interventions from other members
- ❌ Assume fixes worked without testing

## Power Status Check

Before intervention, verify your powers:

```bash
./scripts/god/powers.sh status
```

This shows:
- Which powers are enabled
- Current pause status
- Running processes
