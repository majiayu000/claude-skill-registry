---
name: project-orchestrator
description: Orchestrate multi-phase project implementation using background Claude agents for isolated development, review, and integration.
---

# Project Orchestrator Skill

## 🎯 Purpose

This skill orchestrates the complete implementation of a project plan by delegating all work to background Claude agents. The orchestrator manages the process but **NEVER writes code directly**.

**Use this skill when:**
- You have a PROJECT_PLAN.md ready for implementation
- User says "implement this plan" or "orchestrate this project"
- You need to coordinate multiple implementation phases
- You want isolated development with code review between phases

---

## 🚨 CRITICAL PRINCIPLES

### 1. **The Orchestrator Does NOT Write Code**

**BANNED:**
- ❌ Writing any implementation code yourself
- ❌ Editing files directly during orchestration
- ❌ Running tests yourself
- ❌ Fixing bugs discovered in review

**REQUIRED:**
- ✅ Delegate ALL coding to background agents
- ✅ Spawn agents with `claude --dangerously-skip-permissions -p "..."`
- ✅ Monitor agent progress via bash background jobs
- ✅ Only update PROJECT_PLAN.md and orchestration logs

### 2. **Branch Isolation is Mandatory**

Every phase gets its own isolated branch:
- Implementation happens in `<current-branch>/<phase-name>`
- Review happens in that isolated branch
- Fixes happen in the same isolated branch
- Merge only after review passes

### 3. **Review-Driven Quality Gates**

No phase advances without passing review:
- Every implementation gets reviewed
- Review must show NO critical/high priority issues
- If review fails, spawn fix agent and re-review
- Iterate until review passes

---

## Step 1: Parse the Project Plan

### 1.1: Locate and Read PROJECT_PLAN.md

```bash
# Find the project plan
PROJECT_PLAN=$(find docs/specs -name "PROJECT_PLAN.md" -type f | head -1)

# If user provided specific path, use that
# Otherwise find most recent in docs/specs/

# Read the plan
cat "$PROJECT_PLAN"
```

### 1.2: Extract Implementation Phases

Parse the "Implementation Roadmap" section:

```markdown
## Implementation Roadmap
[High-level phases or milestones for implementation]

### Phase 1: [Phase Name]
[Description of what gets built]

### Phase 2: [Phase Name]
[Description of what gets built]
```

**YOU MUST:**
- ✅ Identify each phase clearly
- ✅ Understand dependencies between phases
- ✅ Extract success criteria for each phase
- ✅ Note any blockers or prerequisites

### 1.3: Create Orchestration Tracking Section

Add to PROJECT_PLAN.md:

```markdown
## Orchestration Status

**Started:** [YYYY-MM-DD HH:MM]
**Orchestrator Branch:** [current branch name]
**Status:** In Progress

### Phase Tracking

| Phase | Branch | Status | Started | Completed | Review Status |
|-------|--------|--------|---------|-----------|---------------|
| Phase 1: [name] | [branch] | ⏳ Pending | - | - | - |
| Phase 2: [name] | [branch] | ⏳ Pending | - | - | - |
```

---

## Step 2: Set Up Orchestration Environment

### 2.1: Verify Current Branch

```bash
# Get current branch (this is the integration branch)
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Orchestrating from branch: $CURRENT_BRANCH"
```

### 2.2: Ensure Clean State

```bash
# Verify no uncommitted changes
if [[ -n $(git status -s) ]]; then
  echo "❌ Uncommitted changes detected. Commit or stash before orchestrating."
  exit 1
fi
```

### 2.3: Create Orchestration Log Directory

```bash
# Create directory for orchestration artifacts
ORCH_DIR="docs/specs/$(basename $(dirname $PROJECT_PLAN))/orchestration"
mkdir -p "$ORCH_DIR/logs"
mkdir -p "$ORCH_DIR/reviews"
```

---

## Step 3: Phase Implementation Loop

**For each phase in the Implementation Roadmap:**

### 3.1: Create Isolated Phase Branch

```bash
# Get phase name (slugified)
PHASE_NAME="phase-1-foundation"  # Example from plan
PHASE_BRANCH="${CURRENT_BRANCH}/${PHASE_NAME}"

# Create and switch to phase branch
git checkout -b "$PHASE_BRANCH"

# Update PROJECT_PLAN.md status
# Mark phase as "🔄 In Progress"
```

**Update PROJECT_PLAN.md:**
```markdown
| Phase 1: Foundation | feature/proj/phase-1-foundation | 🔄 In Progress | 2025-11-17 14:30 | - | - |
```

### 3.2: Spawn Implementation Agent

**Craft the implementation prompt:**

```bash
# Create implementation task file
cat > "$ORCH_DIR/logs/phase-1-task.md" <<EOF
# Implementation Task: Phase 1 - Foundation

## Context
You are implementing Phase 1 of the project plan located at:
$PROJECT_PLAN

## Your Branch
You are working in branch: $PHASE_BRANCH

## Phase Requirements
[Copy relevant section from PROJECT_PLAN.md]

## Your Job
1. Read the PROJECT_PLAN.md completely to understand context
2. Implement ONLY what is described in Phase 1
3. Follow all patterns in AGENTS.md and api/tests/AGENTS.md
4. Use test-writer skill for ALL test code
5. Use test-runner skill to validate your work
6. Commit your changes to this branch when complete
7. DO NOT merge or push - just commit locally

## Success Criteria
- All phase 1 requirements implemented
- Tests pass (just test-all-mocked)
- Code follows project patterns
- Changes committed to $PHASE_BRANCH

## Important
- You are in an isolated branch
- Do NOT modify PROJECT_PLAN.md
- Do NOT merge this branch
- Focus ONLY on Phase 1 scope
EOF

# Spawn background agent
echo "🚀 Spawning implementation agent for Phase 1..."
claude --dangerously-skip-permissions -p "$(cat $ORCH_DIR/logs/phase-1-task.md)" \
  > "$ORCH_DIR/logs/phase-1-implementation.log" 2>&1 &

IMPL_PID=$!
echo "Implementation agent PID: $IMPL_PID"
```

### 3.3: Monitor Agent Progress

```bash
# Wait for implementation agent to complete
# Max timeout: 30 minutes (1800 seconds)
TIMEOUT=1800
START_TIME=$(date +%s)

while kill -0 $IMPL_PID 2>/dev/null; do
  ELAPSED=$(($(date +%s) - START_TIME))

  if [ $ELAPSED -gt $TIMEOUT ]; then
    echo "⚠️ Implementation agent timeout (30 min)"
    kill $IMPL_PID
    # Handle timeout - may need user intervention
    break
  fi

  echo "⏳ Implementation in progress... ${ELAPSED}s elapsed"
  sleep 30  # Check every 30 seconds
done

# Wait for process to fully complete
wait $IMPL_PID
IMPL_EXIT_CODE=$?

echo "✅ Implementation agent completed with exit code: $IMPL_EXIT_CODE"

# Show tail of implementation log
echo "=== Last 50 lines of implementation log ==="
tail -50 "$ORCH_DIR/logs/phase-1-implementation.log"
```

### 3.4: Verify Implementation Committed

```bash
# Check that agent committed changes
if [[ -z $(git log --oneline ${CURRENT_BRANCH}..${PHASE_BRANCH}) ]]; then
  echo "❌ No commits found in phase branch"
  echo "Implementation agent may have failed"
  # Return to orchestrator branch
  git checkout "$CURRENT_BRANCH"
  exit 1
fi

echo "✅ Implementation commits found:"
git log --oneline ${CURRENT_BRANCH}..${PHASE_BRANCH}
```

---

## Step 4: Code Review Cycle

### 4.1: Spawn Review Agent

```bash
# Create review task
cat > "$ORCH_DIR/logs/phase-1-review-task.md" <<EOF
# Code Review Task: Phase 1 - Foundation

## Your Job
Execute the /review-code command to review the implementation in branch:
$PHASE_BRANCH

## Context
Review the changes against the requirements in:
$PROJECT_PLAN

Focus on Phase 1 requirements only.

## Output Required
Generate a comprehensive review markdown file at:
$ORCH_DIR/reviews/phase-1-review.md

Follow the review checklist format from /review-code.

## Critical
- Mark status as APPROVED, NEEDS_CHANGES, or BLOCKED
- Categorize all issues as CRITICAL, HIGH, MEDIUM, or LOW
- Be thorough but fair
EOF

# Spawn review agent
echo "🔍 Spawning review agent for Phase 1..."
claude --dangerously-skip-permissions -p "$(cat $ORCH_DIR/logs/phase-1-review-task.md)" \
  > "$ORCH_DIR/logs/phase-1-review.log" 2>&1 &

REVIEW_PID=$!

# Wait for review (similar timeout logic)
wait $REVIEW_PID
echo "✅ Review agent completed"
```

### 4.2: Parse Review Results

```bash
# Check if review file exists
REVIEW_FILE="$ORCH_DIR/reviews/phase-1-review.md"

if [[ ! -f "$REVIEW_FILE" ]]; then
  echo "❌ Review file not generated"
  exit 1
fi

# Extract review status
REVIEW_STATUS=$(grep "^### Status:" "$REVIEW_FILE" | awk '{print $3}')
echo "Review Status: $REVIEW_STATUS"

# Check for critical/high priority issues
CRITICAL_COUNT=$(grep -c "Priority: CRITICAL" "$REVIEW_FILE" || echo "0")
HIGH_COUNT=$(grep -c "Priority: HIGH" "$REVIEW_FILE" || echo "0")

echo "Critical issues: $CRITICAL_COUNT"
echo "High priority issues: $HIGH_COUNT"
```

### 4.3: Review Decision Logic

```bash
if [[ "$REVIEW_STATUS" == "APPROVED" ]] && [[ $CRITICAL_COUNT -eq 0 ]] && [[ $HIGH_COUNT -eq 0 ]]; then
  echo "✅ Review PASSED - proceeding to merge"
  REVIEW_PASSED=true
else
  echo "⚠️ Review FAILED - spawning fix agent"
  REVIEW_PASSED=false
fi
```

### 4.4: Fix Cycle (if needed)

```bash
if [[ "$REVIEW_PASSED" == "false" ]]; then
  # Spawn fix agent
  cat > "$ORCH_DIR/logs/phase-1-fix-task.md" <<EOF
# Fix Task: Address Review Comments for Phase 1

## Your Branch
You are working in: $PHASE_BRANCH

## Review Comments
The code review identified issues that must be fixed.
Review file location: $REVIEW_FILE

## Your Job
1. Read the review comments carefully
2. Address ALL critical and high priority issues
3. Consider medium/low priority suggestions
4. Commit your fixes to $PHASE_BRANCH
5. DO NOT merge

## Success Criteria
- All critical issues resolved
- All high priority issues resolved
- Tests still pass
- Changes committed to branch
EOF

  echo "🔧 Spawning fix agent for Phase 1..."
  claude --dangerously-skip-permissions -p "$(cat $ORCH_DIR/logs/phase-1-fix-task.md)" \
    > "$ORCH_DIR/logs/phase-1-fix.log" 2>&1 &

  FIX_PID=$!
  wait $FIX_PID

  echo "✅ Fix agent completed"

  # Re-run review (recursive - go back to Step 4.1)
  echo "🔄 Re-running review after fixes..."
  # Loop back to 4.1
fi
```

**YOU MUST:**
- ✅ Iterate fix → review until review passes
- ✅ Track iteration count (max 5 iterations per phase)
- ✅ If 5 iterations fail, escalate to user

---

## Step 5: Merge Phase Branch

### 5.1: Return to Integration Branch

```bash
# Switch back to orchestrator branch
git checkout "$CURRENT_BRANCH"
```

### 5.2: Merge Phase Branch

```bash
# Merge phase branch (should be fast-forward or clean)
echo "🔀 Merging phase branch: $PHASE_BRANCH → $CURRENT_BRANCH"

git merge "$PHASE_BRANCH" --no-ff -m "Merge Phase 1: Foundation

Orchestrated implementation completed successfully.
Review passed with no critical/high issues.

Phase branch: $PHASE_BRANCH
Review: $REVIEW_FILE"

if [[ $? -ne 0 ]]; then
  echo "❌ Merge conflict detected"
  echo "Manual intervention required"
  exit 1
fi

echo "✅ Phase branch merged successfully"
```

### 5.3: Update PROJECT_PLAN.md

```markdown
| Phase 1: Foundation | feature/proj/phase-1-foundation | ✅ Completed | 2025-11-17 14:30 | 2025-11-17 15:45 | ✅ Approved |
```

Add completion notes:

```markdown
### Phase 1: Foundation - COMPLETED

**Completed:** 2025-11-17 15:45
**Review:** `docs/specs/project-name/orchestration/reviews/phase-1-review.md`
**Implementation Log:** `docs/specs/project-name/orchestration/logs/phase-1-implementation.log`

**Summary:**
- Implemented [list key deliverables]
- All tests passing
- Review approved with 0 critical/high issues

**Commits:**
[git log output from phase branch]
```

### 5.4: Clean Up Phase Branch (Optional)

```bash
# Optionally delete phase branch after successful merge
# git branch -d "$PHASE_BRANCH"

# Or keep for audit trail
echo "Phase branch preserved for audit: $PHASE_BRANCH"
```

---

## Step 6: Repeat for All Phases

**Loop through remaining phases:**

For each subsequent phase:
1. Create new phase branch from current integration branch
2. Spawn implementation agent
3. Monitor completion
4. Spawn review agent
5. If review fails, spawn fix agent and iterate
6. When review passes, merge phase branch
7. Update PROJECT_PLAN.md
8. Continue to next phase

---

## Step 7: Final Completion

### 7.1: Update PROJECT_PLAN.md with Final Status

```markdown
## Orchestration Status

**Started:** 2025-11-17 14:30
**Completed:** 2025-11-17 18:45
**Orchestrator Branch:** feature/new-project
**Status:** ✅ Complete

### Summary
- Total Phases: 3
- Successful: 3
- Failed: 0
- Total Time: 4h 15m

### Deliverables
- All implementation phases completed
- All reviews passed
- All changes merged to integration branch
- Tests passing
- Documentation updated
```

### 7.2: Generate Final Report

```markdown
# Orchestration Report: [Project Name]

## Project
**Plan:** $PROJECT_PLAN
**Integration Branch:** $CURRENT_BRANCH
**Duration:** [start] - [end]

## Phases Completed

### Phase 1: Foundation
- **Status:** ✅ Completed
- **Branch:** feature/proj/phase-1-foundation
- **Review:** Approved (0 critical, 0 high)
- **Iterations:** 1 (first pass)

### Phase 2: Integration
- **Status:** ✅ Completed
- **Branch:** feature/proj/phase-2-integration
- **Review:** Approved (0 critical, 0 high)
- **Iterations:** 2 (1 fix cycle)

### Phase 3: Polish
- **Status:** ✅ Completed
- **Branch:** feature/proj/phase-3-polish
- **Review:** Approved (0 critical, 0 high)
- **Iterations:** 1 (first pass)

## Artifacts
- Implementation logs: `$ORCH_DIR/logs/`
- Review reports: `$ORCH_DIR/reviews/`
- Project plan: `$PROJECT_PLAN` (updated with completion status)

## Next Steps
- [ ] Create PR from integration branch to main
- [ ] Final human review
- [ ] Merge to main when approved
```

### 7.3: Return Summary to User

```
✅ Project orchestration complete!

📋 Project: [Name]
🌿 Integration Branch: $CURRENT_BRANCH
📊 Phases: 3/3 completed

✅ All phases implemented
✅ All reviews passed
✅ All tests passing
✅ Documentation updated

📁 Orchestration artifacts: $ORCH_DIR
📄 Updated plan: $PROJECT_PLAN

Next: Review the integration branch and create PR to main
```

---

## Common Violations

### ❌ BANNED: Writing Code Yourself

**Wrong:**
```bash
# Orchestrator directly editing files
vim api/src/new_feature.py
```

**Right:**
```bash
# Orchestrator spawning agent to write code
claude --dangerously-skip-permissions -p "Implement feature X in branch Y"
```

### ❌ BANNED: Merging Without Review

**Wrong:**
```bash
# Merge immediately after implementation
git merge $PHASE_BRANCH
```

**Right:**
```bash
# Always review before merge
spawn_review_agent()
wait_for_approval()
then_merge()
```

### ❌ BANNED: Infinite Fix Loops

**Wrong:**
```bash
# No iteration limit
while review_fails; do
  spawn_fix_agent
done
```

**Right:**
```bash
# Max 5 iterations per phase
for i in {1..5}; do
  if review_passes; then break; fi
  spawn_fix_agent
done
if ! review_passes; then
  escalate_to_user
fi
```

### ❌ BANNED: Skipping Documentation Updates

**Wrong:**
```bash
# Complete phase without updating plan
merge_and_continue
```

**Right:**
```bash
# Always update PROJECT_PLAN.md
update_plan_with_completion_status
add_summary_and_artifacts
then_merge_and_continue
```

---

## Troubleshooting

### Problem: Background Agent Timeout

**Cause:** Agent takes > 30 minutes
**Solution:**
```bash
# Increase timeout for complex phases
TIMEOUT=3600  # 1 hour for complex phases

# Or split phase into smaller sub-phases
```

### Problem: Review Never Passes

**Cause:** Issues not being fixed properly, or review is too strict
**Solution:**
```bash
# After 5 iterations, escalate
if [[ $ITERATION_COUNT -ge 5 ]]; then
  echo "❌ Review failed after 5 iterations"
  echo "Manual intervention required"
  exit 1
fi
```

### Problem: Merge Conflicts

**Cause:** Phase branch diverged from integration branch
**Solution:**
```bash
# Before each phase, ensure integration branch is up to date
git checkout $CURRENT_BRANCH
git pull

# When creating phase branch, branch from latest
git checkout -b $PHASE_BRANCH
```

### Problem: Agent Exit Code Non-Zero

**Cause:** Agent crashed or failed
**Solution:**
```bash
# Check agent log for errors
tail -100 "$ORCH_DIR/logs/phase-1-implementation.log"

# Common issues:
# - Missing dependencies
# - Syntax errors in task prompt
# - Permission issues
```

---

## Success Criteria

You've successfully orchestrated a project when:

- [ ] All phases from PROJECT_PLAN.md implemented
- [ ] Each phase reviewed and approved (no critical/high issues)
- [ ] All phase branches merged to integration branch
- [ ] PROJECT_PLAN.md updated with completion status
- [ ] Orchestration artifacts (logs, reviews) preserved
- [ ] All tests passing on integration branch
- [ ] Final report generated

---

## Quick Reference

### Spawning Implementation Agent

```bash
claude --dangerously-skip-permissions -p "Implement Phase X according to $PROJECT_PLAN in branch $PHASE_BRANCH. Commit when done." > log.txt 2>&1 &
```

### Spawning Review Agent

```bash
claude --dangerously-skip-permissions -p "Run /review-code on branch $PHASE_BRANCH. Output to $REVIEW_FILE." > log.txt 2>&1 &
```

### Spawning Fix Agent

```bash
claude --dangerously-skip-permissions -p "Address review comments from $REVIEW_FILE in branch $PHASE_BRANCH. Commit fixes." > log.txt 2>&1 &
```

### Monitoring Background Job

```bash
PID=$!
while kill -0 $PID 2>/dev/null; do
  sleep 30
done
wait $PID
```

---

## Related Skills

- **project-planner**: Creates the PROJECT_PLAN.md that this skill orchestrates
- **test-runner**: Used by implementation agents for validation
- **test-writer**: Used by implementation agents for test code
- **skill-writer**: For creating/editing skills (if needed)

---

## Notes

- This skill is a **process orchestrator**, not a code implementer
- Background agents do ALL the actual work
- Orchestrator only manages branches, spawns agents, monitors progress, and updates documentation
- Each phase is isolated until reviewed and approved
- Review quality gates prevent low-quality code from advancing
- All artifacts preserved for audit trail
- Integration branch contains only reviewed, approved code
