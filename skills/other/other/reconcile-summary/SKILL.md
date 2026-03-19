---
name: reconcile-summary
description: "Review a worker session summary and reconcile beads tasks with implementation reality. Use after a worker completes /finish-task to sync the task board with what was actually implemented. Invoked by orchestrator sessions, or with /reconcile-summary <task-id>."
allowed-tools: Read, Bash, Glob, Grep, Edit, Write, SendMessage, TeamDelete, TaskList, AskUserQuestion
---

# Reconcile Session Summary

You are an orchestrating agent reviewing a completed worker session. Your job is to ensure the beads task board accurately reflects what was actually built, not just what was originally specified.

## `--yes` Mode (Autonomous Operation)

If `$ARGUMENTS` contains `--yes`, auto-answer ALL `AskUserQuestion` prompts:
- **Which summary to process** → "All of them" (process all unreconciled summaries sequentially)
- **Update PROJECT_SPEC.md or CLAUDE.md** → "No, beads only"
- **Copy to clipboard** → "No, skip"
- **Shut down team** → "No, keep active" (caller manages team lifecycle)
- **Next action** → Skip prompt, return control to caller

Strip `--yes` from `$ARGUMENTS` before processing task IDs. The `--yes` flag is composable with `--no-cleanup` and task ID arguments.

## 1. Discover Session Summaries

The command can receive input in multiple ways. Try them in order:

### Option A: Argument provided
If the user provided a task ID as argument (`$ARGUMENTS`), look for its summary:

```bash
# Find summary file for specific task
ls -lt docs/session_summaries/${ARGUMENTS}*.txt 2>/dev/null | head -1
```

### Option B: Auto-discover from docs/session_summaries/
If no argument, scan for unreconciled summaries (excludes `reconciled/` subdirectory):

```bash
# Find summary files NOT in reconciled/ subdirectory
find docs/session_summaries/ -maxdepth 1 -name "*.txt" -type f 2>/dev/null | head -10

# Check which tasks were recently closed
bd list --all 2>/dev/null | grep -i closed | head -10
```

### Option C: User pastes summary
If no summaries found or user prefers, they can paste directly.

### Discovery Logic

1. **If `$ARGUMENTS` is a task ID**: Read that task's summary file
2. **If summaries exist**: List them and ask user which to reconcile
3. **If user pastes**: Parse the pasted content
4. **If nothing found**: Ask user to paste or provide file path

```bash
# Example: List unreconciled summaries with task IDs and timestamps
# (excludes docs/session_summaries/reconciled/)
for f in docs/session_summaries/*.txt; do
  if [ -f "$f" ]; then
    task_id=$(basename "$f" | cut -d'_' -f1)
    mod_time=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$f")
    echo "$task_id - $mod_time - $f"
  fi
done 2>/dev/null | sort -t'-' -k2 -r | head -10
```

**Note:** Summaries in `docs/session_summaries/reconciled/` have already been processed and are excluded from discovery.

If multiple summaries need reconciliation, use AskUserQuestion:

**Question:** "Found N unreconciled summaries. Which to process?"
- **Options:** List task IDs, or "All of them" / "Let me pick"
- **Header:** "Summaries"

### Parse the Summary

Once you have the summary content (from file or paste), extract:

- **Task ID** from the TASK OVERVIEW section
- **SPEC DIVERGENCES** section (critical - this tells you what changed)
- **FOLLOW-UP ISSUES CREATED** section
- **DEPENDENCIES UNBLOCKED** section
- **ARCHITECTURAL NOTES** section

## 2. Review the Original Task — With Distrust

Do NOT trust session summaries blindly. Workers may have been under context pressure. Their summaries may be incomplete, inaccurate, or optimistic.

```bash
bd show <task-id>
```

### 2a. Cross-Reference Claims Against Evidence

Extract `branch-name` from the summary's GIT ACTIVITY → Branch field. Extract `pr-number` from GIT ACTIVITY → PR field (or from the `gh pr list` output below).

For each major claim in the session summary, verify independently:

```bash
# Does the PR exist?
gh pr list --head <branch-name> --json number,state

# Do file changes match summary claims?
gh pr diff <pr-number> --stat 2>/dev/null

# Are CI checks passing?
gh pr checks <pr-number> 2>/dev/null
```

**Flag any discrepancy** between summary claims and observable evidence. If the summary says "all tests pass" but CI shows failures, note this in the reconciliation report under REMAINING CONCERNS.

Then compare the original task description against the worker's IMPLEMENTATION SUMMARY and SPEC DIVERGENCES sections.

## 3. Analyze Divergences

For each divergence documented by the worker, determine:

1. **Scope**: Does this affect only this task, or does it ripple to other tasks?
2. **Downstream impact**: Which blocked/dependent tasks need their descriptions updated?
3. **New work**: Does this divergence create new tasks that weren't anticipated?
4. **Invalidated work**: Does this make any existing tasks obsolete or redundant?

## 4. Review Related Tasks

```bash
# Show tasks that were blocked by the completed task
bd show <task-id> | grep -A 10 "BLOCKS"

# List all open tasks to check for ripple effects
bd list --status=open
```

For each potentially affected task:

```bash
bd show <affected-task-id>
```

Ask yourself:
- Does this task's description assume something that's no longer true?
- Does the implementation change how this task should be approached?
- Are there new dependencies or constraints to document?

## 5. Update Beads Tasks

For each task that needs updating, use `bd update` to modify the description:

```bash
# Update task description to reflect new reality
bd update <task-id> --description "$(cat <<'EOF'
<updated description that reflects the actual implementation>

## Updated Context
This task was updated based on implementation of <completed-task-id>.

Changes from original spec:
- <change 1>
- <change 2>

New constraints/dependencies:
- <constraint 1>
EOF
)"
```

### Common Updates

**If a task is now obsolete:**
```bash
bd close <task-id> --reason="Obsoleted by implementation of <task-id>. <brief explanation>"
```

**If a task needs new dependencies:**
```bash
# Execution-order dependency (task can't start until dependency finishes)
# For parent-child containment, use: bd update <task-id> --parent <epic-id>
bd dep add <task-id> <new-dependency-id>
```

**If scope expanded and needs splitting:**
```bash
bd create --title="<split-off work>" --type=task --priority=2 --parent <parent-epic-id>
# Execution dependency on original — only if the split genuinely depends on it
bd dep add <new-task-id> <original-task-id>
```

**If implementation discovered new required work:**
```bash
bd create --title="<discovered work>" --type=task --priority=2 --parent <epic-id>
# Add execution-order dependencies only if genuinely blocked:
# bd dep add <new-task-id> <blocker-task-id>
```

## 6. Sync Changes

```bash
bd sync
```

## 7. Report Reconciliation

Output a reconciliation report:

```
===============================================
RECONCILIATION REPORT
===============================================

REVIEWED TASK
-------------
ID: <task-id>
Title: <title>
Status: Closed

DIVERGENCES PROCESSED
---------------------
<For each divergence from the session summary>

1. <Divergence title>
   Action taken: <what you did - updated task X, created task Y, closed task Z>

TASKS UPDATED
-------------
<List each task that was modified>

- <task-id>: <brief description of change>
- <task-id>: <brief description of change>

TASKS CREATED
-------------
<List any new tasks created>

- <task-id>: <title>

TASKS CLOSED
------------
<List any tasks closed as obsolete>

- <task-id>: <reason>

REMAINING CONCERNS
------------------
<Any issues that couldn't be automatically resolved, need human decision, or require discussion>

TASK BOARD STATUS
-----------------
Ready tasks: <count from bd ready>
Blocked tasks: <count>
Total open: <count>

===============================================
END RECONCILIATION REPORT
===============================================
```

## 8. Update Architectural Documentation (If Needed)

If divergences represent significant architectural changes (not just implementation details), consider updating project-level documentation:

**PROJECT_SPEC.md** - Update if:
- Core architecture changed (different services, data flow, etc.)
- Technology choices changed (different libraries, frameworks)
- API contracts changed significantly
- Data models changed

**Project CLAUDE.md** - Update if:
- New patterns or conventions were established
- New commands or workflows were added
- Critical rules changed (e.g., "never do X")

```bash
# Check if these files exist
ls -la PROJECT_SPEC.md CLAUDE.md 2>/dev/null
```

Use AskUserQuestion to confirm before modifying these files:

**Question:** "Divergence '<title>' represents an architectural change. Update PROJECT_SPEC.md or CLAUDE.md?"
- **Options:** "Yes, update docs" / "No, beads only" / "Ask me about each file"

## 9. Copy Reconciliation Report (Optional)

Use AskUserQuestion to offer copying the report to clipboard:

**Question:** "Copy reconciliation report to clipboard?"
- **Options:** "Yes, copy to clipboard" / "No, skip"
- **Header:** "Clipboard"

If the user selects "Yes, copy to clipboard", copy the full reconciliation report.

## 10. Mark Summary as Reconciled

Move the processed summary file to a `reconciled/` subdirectory to prevent re-processing:

```bash
# Create reconciled directory if needed
mkdir -p docs/session_summaries/reconciled

# Move the processed summary
mv "$SUMMARY_FILE" docs/session_summaries/reconciled/

echo "Summary moved to docs/session_summaries/reconciled/"
```

This ensures the discovery step (Step 1) won't pick up already-reconciled summaries.

## 11. Prompt for Next Action

After reconciliation, ask the user:

"Reconciliation complete. What would you like to do next?"
- **Review changes** - Show the updated tasks in detail
- **Continue orchestrating** - Return to normal orchestration
- **Dispatch more workers** - Spin up workers for newly unblocked tasks
- **Reconcile another** - Process the next pending summary

## 12. Team Cleanup (Same-Session Only)

**Note:** If `$ARGUMENTS` contains `--no-cleanup`, skip this step entirely.

After reconciling, check if unreconciled summaries remain:

```bash
REMAINING=$(find docs/session_summaries/ -maxdepth 1 -name "*.txt" -type f 2>/dev/null | wc -l)
```

**If remaining == 0:**

Check for active team context by running TaskList. If TaskList returns results (team context exists in this session):

Use AskUserQuestion: "All summaries reconciled. Shut down the team and clean up?"
- Options: "Yes, shut down" / "No, keep active"

If confirmed:
1. Send shutdown_request to each teammate via SendMessage
2. Wait briefly for confirmations (teammates auto-approve or reject)
3. Run TeamDelete to remove team config and ephemeral task list
4. Report: "Team shut down. All task state persists in beads."

If no team context (TaskList returns empty — new session or no team): Skip cleanup, note: "No active team in this session. If team resources need cleanup, start a session in the original terminal or manually remove ~/.claude/teams/<team-name>/."

**If summaries remain:** Skip cleanup, report count remaining.

---

## Important Guidelines

1. **Be thorough** - A divergence in one task often ripples to many others
2. **Preserve intent** - When updating task descriptions, keep the original goal clear
3. **Document reasoning** - Future agents need to understand why specs changed
4. **Don't over-correct** - Only update tasks that are actually affected
5. **Ask when uncertain** - If a divergence has unclear implications, ask the user
6. **Verify, don't trust** — Session summaries are self-reported. Cross-reference claims against git/CI evidence before updating the task board. (Inspired by obra/superpowers subagent distrust model)
