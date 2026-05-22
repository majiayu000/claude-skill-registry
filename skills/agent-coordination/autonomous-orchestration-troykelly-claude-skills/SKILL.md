---
name: autonomous-orchestration
description: Use when user requests autonomous operation across multiple issues. Orchestrates parallel workers using Task tool, monitors with TaskOutput, handles SLEEP/WAKE cycles, and works until scope is complete without user intervention.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Task
  - TaskOutput
  - mcp__github__*
  - mcp__memory__*
model: opus
---

# Autonomous Orchestration

## Overview

Orchestrates long-running autonomous work across multiple issues using the **Task tool** to spawn parallel worker agents and **TaskOutput** to monitor their progress.

**Core principle:** GitHub is the source of truth. Workers are disposable. State survives restarts.

**Announce at start:** "I'm using autonomous-orchestration to work through [SCOPE]. Starting autonomous operation now."

## Prerequisites

- `worker-dispatch` skill for spawning workers with Task tool
- `worker-protocol` skill for worker behavior
- `ci-monitoring` skill for CI/WAKE handling
- GitHub CLI (`gh`) authenticated
- GitHub Project Board configured

## Parallel Execution Model

Workers are spawned as **background agents** using the Task tool:

```
Orchestrator
    │
    ├── Task(run_in_background: true) → Worker Agent #1 (task_id: aa93f22)
    ├── Task(run_in_background: true) → Worker Agent #2 (task_id: b51e54b)
    └── Task(run_in_background: true) → Worker Agent #3 (task_id: c72f3d1)
```

Monitor progress with TaskOutput:

```
TaskOutput(task_id: "aa93f22", block: false) → "Task is still running..."
TaskOutput(task_id: "b51e54b", block: false) → Completed with result
TaskOutput(task_id: "c72f3d1", block: false) → "Task is still running..."
```

**CRITICAL:** Spawn all workers in the SAME message for true concurrent execution.

## State Management

**CRITICAL:** All persistent state is stored in GitHub. Task IDs are ephemeral session state.

| State Store | Purpose | Used For |
|-------------|---------|----------|
| Project Board Status | THE source of truth | Ready, In Progress, In Review, Blocked, Done |
| Issue Comments | Activity log | Worker assignment, progress, deviations |
| Labels | Lineage only | `spawned-from:#N`, `depth:N`, `epic-*` |
| MCP Memory | Active marker + task tracking | **Active orchestration detection**, active task_ids |
| Orchestrator memory | Ephemeral session state | Map of issue# → task_id for monitoring |

**See:** `reference/state-management.md` for detailed state queries and updates.

## Context Compaction Survival

**CRITICAL:** Orchestration must survive mid-loop context compaction.

### On Start: Write Active Marker

```bash
# Write to MCP Memory when orchestration starts
mcp__memory__create_entities([{
  "name": "ActiveOrchestration",
  "entityType": "Orchestration",
  "observations": [
    "Status: ACTIVE",
    "Scope: [MILESTONE/EPIC/unbounded]",
    "Tracking Issue: #[NUMBER]",
    "Started: [ISO_TIMESTAMP]",
    "Repository: [owner/repo]",
    "Phase: BOOTSTRAP|MAIN_LOOP",
    "Last Loop: [ISO_TIMESTAMP]"
  ]
}])
```

### On Each Loop Iteration: Update Marker

```bash
mcp__memory__add_observations({
  "observations": [{
    "entityName": "ActiveOrchestration",
    "contents": ["Last Loop: [ISO_TIMESTAMP]", "Phase: MAIN_LOOP"]
  }]
})
```

### On Complete: Remove Marker

```bash
mcp__memory__delete_entities({
  "entityNames": ["ActiveOrchestration"]
})
```

### On Session Resume (After Compaction)

Session-start skill checks for active orchestration:

```bash
# Check MCP Memory for active orchestration
ACTIVE=$(mcp__memory__open_nodes({"names": ["ActiveOrchestration"]}))

if [ -n "$ACTIVE" ]; then
  echo "⚠️ ACTIVE ORCHESTRATION DETECTED"
  echo "Scope: [from ACTIVE]"
  echo "Tracking: [from ACTIVE]"
  echo ""
  echo "Resuming orchestration loop..."
  # Invoke autonomous-orchestration skill to resume
fi
```

**This ensures:** Even if context compacts mid-loop, the next session will detect the active orchestration and resume it.

## Immediate Start (User Consent Implied)

**The user's request for autonomous operation IS their consent.** No additional confirmation required.

When the user requests autonomous work:

1. **Identify scope** - Parse user request for milestone, epic, specific issues, or "all"
2. **Announce intent** - Briefly state what you're about to do
3. **Start immediately** - Begin orchestration without waiting for additional input

```markdown
## Starting Autonomous Operation

**Scope:** [MILESTONE/EPIC/ISSUES or "all open issues"]
**Workers:** Up to 5 parallel
**Mode:** Continuous until complete

Beginning work now...
```

**Do NOT ask for "PROCEED" or any confirmation.** The user asked for autonomous operation - that is the confirmation.

## Automatic Scope Detection

When the user requests autonomous operation without specifying a scope:

### Priority Order

1. **User-specified scope** - If user mentions specific issues, epics, or milestones
2. **Urgent/High Priority standalone issues** - Issues with `priority:urgent` or `priority:high` labels not part of an epic
3. **Epic-based sequential work** - Work through epics in order, completing all issues within each epic
4. **Remaining standalone issues** - Any issues not part of an epic

```bash
detect_work_scope() {
  # 1. Check for urgent/high priority standalone issues first
  PRIORITY_ISSUES=$(gh issue list --state open \
    --label "priority:urgent,priority:high" \
    --json number,labels \
    --jq '[.[] | select(.labels | map(.name) | any(startswith("epic-")) | not)] | .[].number')

  if [ -n "$PRIORITY_ISSUES" ]; then
    echo "priority_standalone"
    echo "$PRIORITY_ISSUES"
    return
  fi

  # 2. Get epics in order (by creation date)
  EPICS=$(gh issue list --state open --label "type:epic" \
    --json number,title,createdAt \
    --jq 'sort_by(.createdAt) | .[].number')

  if [ -n "$EPICS" ]; then
    echo "epics"
    echo "$EPICS"
    return
  fi

  # 3. Fall back to all open issues
  ALL_ISSUES=$(gh issue list --state open --json number --jq '.[].number')
  echo "all_issues"
  echo "$ALL_ISSUES"
}
```

## Continuous Operation Until Complete

Autonomous operation continues until ALL of:
- No open issues remain in scope
- No open PRs awaiting merge
- No issues in "In Progress" or "In Review" status

The operation does NOT pause for:
- Progress updates
- Confirmation between issues
- Switching between epics
- Any user input (unless blocked by a fatal error)

## PR Resolution Bootstrap Phase

**CRITICAL:** Before spawning ANY new workers, resolve all existing open PRs first.

**Bootstrap Flow:** Get open PRs (exclude release/*, release-placeholder, do-not-merge) → For each: Check CI → Verify review → Merge if ready → Then start main loop

### Bootstrap Implementation

```bash
resolve_existing_prs() {
  echo "=== PR RESOLUTION BOOTSTRAP ==="

  # Get all open PRs, excluding release placeholders
  OPEN_PRS=$(gh pr list --json number,headRefName,labels \
    --jq '[.[] | select(
      (.headRefName | startswith("release/") | not) and
      (.labels | map(.name) | index("release-placeholder") | not)
    )] | .[].number')

  if [ -z "$OPEN_PRS" ]; then
    echo "No actionable PRs to resolve. Proceeding to main loop."
    return 0
  fi

  echo "Found PRs to resolve: $OPEN_PRS"

  for pr in $OPEN_PRS; do
    echo "Processing PR #$pr..."

    # Get CI status
    ci_status=$(gh pr checks "$pr" --json state --jq '.[].state' 2>/dev/null | sort -u)

    # Get linked issue
    ISSUE=$(gh pr view "$pr" --json body --jq '.body' | grep -oE 'Closes #[0-9]+' | grep -oE '[0-9]+' | head -1)

    if [ -z "$ISSUE" ]; then
      echo "  ⚠ No linked issue found, skipping"
      continue
    fi

    # Check if CI passed
    if echo "$ci_status" | grep -q "FAILURE"; then
      echo "  ❌ CI failing - triggering ci-monitoring for PR #$pr"
      # Invoke ci-monitoring skill to fix
      handle_ci_failure "$pr"
      continue
    fi

    if echo "$ci_status" | grep -q "PENDING"; then
      echo "  ⏳ CI pending for PR #$pr, will check in main loop"
      continue
    fi

    if echo "$ci_status" | grep -q "SUCCESS"; then
      # Verify review artifact
      REVIEW_EXISTS=$(gh api "/repos/$OWNER/$REPO/issues/$ISSUE/comments" \
        --jq '[.[] | select(.body | contains("<!-- REVIEW:START -->"))] | length' 2>/dev/null || echo "0")

      if [ "$REVIEW_EXISTS" = "0" ]; then
        echo "  ⚠ No review artifact - requesting review for #$ISSUE"
        gh issue comment "$ISSUE" --body "## Review Required

PR #$pr has passing CI but no review artifact.

**Action needed:** Complete comprehensive-review and post artifact to this issue.

---
*Bootstrap phase - Orchestrator*"
        continue
      fi

      # All checks pass - merge
      echo "  ✅ Merging PR #$pr"
      gh pr merge "$pr" --squash --delete-branch
      mark_issue_done "$ISSUE"
    fi
  done

  echo "=== BOOTSTRAP COMPLETE ==="
}
```

### Release Placeholder Detection

PRs are excluded from bootstrap resolution if:

| Condition | Example |
|-----------|---------|
| Branch starts with `release/` | `release/v2.0.0`, `release/2025-01` |
| Has `release-placeholder` label | Manual exclusion |
| Has `do-not-merge` label | Explicit hold |

## Orchestration Loop

**Main Loop Flow:** Monitor workers (TaskOutput) + Check CI/PRs + Spawn workers (Task) → Evaluate state (complete/sleep/continue)

### Loop Steps

1. **Monitor Active Workers** - Use `TaskOutput(block: false)` for each active task_id
2. **Handle Completed Workers** - Check GitHub for PR/completion status
3. **Check CI/PRs** - Monitor for merge readiness, verify review artifacts
4. **MERGE GREEN PRs** - Any PR with passing CI is merged IMMEDIATELY
5. **Spawn Workers** - Up to 5 parallel workers using `Task(run_in_background: true)`
6. **Evaluate State** - Determine next action (continue, sleep, complete)
7. **Brief Pause** - 30 second interval between iterations

### Worker Monitoring with TaskOutput

Each loop iteration checks all active workers:

```markdown
## Monitor Active Workers

For each task_id in active_workers:
  TaskOutput(task_id: "[ID]", block: false, timeout: 1000)

Interpret results:
- "Task is still running..." → Continue monitoring
- Completed → Check GitHub for PR, update project board, remove from active list
- Error → Handle failure, potentially spawn replacement
```

### Spawning Parallel Workers

Spawn multiple workers in ONE message for concurrent execution:

```markdown
## Dispatch Workers

1. Count available slots: 5 - len(active_workers)
2. Get Ready issues from project board
3. For each issue to dispatch:

Task(
  description: "Issue #123 worker",
  prompt: [WORKER_PROMPT],
  subagent_type: "general-purpose",
  run_in_background: true
)

4. Store returned task_id → issue mapping
```

### CRITICAL: Merge Green PRs Immediately

**Every loop iteration must check for and merge passing PRs:**

```bash
# In each loop iteration
for pr in $(gh pr list --json number,statusCheckRollup --jq '.[] | select(.statusCheckRollup | all(.conclusion == "SUCCESS")) | .number'); do
  # Check for do-not-merge label
  if ! gh pr view "$pr" --json labels --jq '.labels[].name' | grep -q "do-not-merge"; then
    echo "Merging PR #$pr (CI passed)"
    gh pr merge "$pr" --squash --delete-branch

    # Get linked issue and mark done
    ISSUE=$(gh pr view "$pr" --json body --jq '.body' | grep -oE 'Closes #[0-9]+' | grep -oE '[0-9]+' | head -1)
    if [ -n "$ISSUE" ]; then
      # Update project board status to Done
      mark_issue_done "$ISSUE"
    fi
  fi
done
```

**Do NOT:**
- Report "PRs are ready for merge" and stop
- Wait for user to request merge
- Summarize completed work and ask for next steps

**The loop continues until scope is complete. Green PR = immediate merge.**

## Scope Types

### Milestone

```bash
gh issue list --milestone "v1.0.0" --state open --json number --jq '.[].number'
```

### Epic

```bash
gh issue list --label "epic-dark-mode" --state open --json number --jq '.[].number'
```

### Unbounded (All Open Issues)

```bash
gh issue list --state open --json number --jq '.[].number'
```

**Do NOT ask for "UNBOUNDED" confirmation.** The user's request is their consent.

## Failure Handling

Workers that fail do NOT immediately become blocked:

```
Attempt 1 → Research → Attempt 2 → Research → Attempt 3 → Research → Attempt 4 → BLOCKED
```

Only after 3+ research cycles is an issue marked as blocked.

**See:** `reference/failure-recovery.md` for research cycle implementation.

### Blocked Determination

An issue is only marked blocked when:
- Multiple research cycles completed (3+)
- Research concludes "impossible without external input"
- Examples: missing credentials, requires human decision, external service down

## SLEEP/WAKE

### Entering SLEEP

Orchestration sleeps when:
- All issues are either blocked or in review
- No work can proceed without external event

State is posted to GitHub tracking issue (survives crashes).

### WAKE Mechanisms

- **SessionStart hook** - Checks CI status on new Claude session
- **Manual** - `claude --resume [SESSION_ID]`

## Checklist

Before starting orchestration:

- [ ] Scope identified (explicit or auto-detected)
- [ ] GitHub CLI authenticated (`gh auth status`)
- [ ] Tracking issue exists with `orchestration-tracking` label
- [ ] Project board configured with Status field
- [ ] Active marker written to MCP Memory

Bootstrap phase:

- [ ] Existing open PRs detected
- [ ] Release placeholders excluded (`release/*`, `release-placeholder`, `do-not-merge` labels)
- [ ] CI status checked for each PR
- [ ] Review artifacts verified before merge
- [ ] PRs merged or flagged for attention
- [ ] Bootstrap complete before spawning workers

During orchestration:

- [ ] Workers spawned using `Task(run_in_background: true)`
- [ ] Task IDs stored for each worker (issue# → task_id mapping)
- [ ] Worker status monitored with `TaskOutput(block: false)`
- [ ] Completed workers detected and handled
- [ ] Project board status updated (In Progress, In Review, Done)
- [ ] CI status monitored for open PRs
- [ ] Green PRs merged IMMEDIATELY
- [ ] Review artifacts verified before PR merge
- [ ] Failed workers trigger research cycles
- [ ] Handovers spawn replacement workers
- [ ] SLEEP entered when only waiting on CI
- [ ] Deviation resolution checked each loop
- [ ] Status posted to tracking issue

## Review Enforcement

**CRITICAL:** The orchestrator verifies review compliance:

1. **Before PR merge:**
   - Review artifact exists in issue comments
   - Review status is COMPLETE
   - Unaddressed findings = 0

2. **Child issues (from deferred findings):**
   - Follow full `issue-driven-development` process
   - Have their own code reviews
   - Track via `spawned-from:#N` label

3. **Deviation handling:**
   - Parent status set to Blocked on project board
   - Resumes only when all children closed

## Integration

This skill coordinates:

| Skill | Purpose |
|-------|---------|
| `worker-dispatch` | Spawning workers |
| `worker-protocol` | Worker behavior |
| `worker-handover` | Context passing |
| `ci-monitoring` | CI and WAKE handling |
| `research-after-failure` | Research cycles |
| `issue-driven-development` | Worker follows this |
| `comprehensive-review` | Workers must complete before PR |
| `project-board-enforcement` | ALL state queries and updates |

## Reference Files

- `reference/state-management.md` - State queries, updates, deviation handling
- `reference/loop-implementation.md` - Full loop code and helpers
- `reference/failure-recovery.md` - Research cycles, blocked handling, SLEEP/WAKE
