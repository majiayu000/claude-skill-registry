---
name: crank
description: 'Fully autonomous epic execution. Runs until ALL children are CLOSED. Loops through beads issues, runs /implement on each, validates with /vibe. NO human prompts, NO stopping.'
---

# Crank Skill

> **Quick Ref:** Autonomous epic execution. Loops `/implement` on all issues until DONE. Output: closed issues + final vibe.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Autonomous execution: implement all issues until the epic is DONE.

**Requires:** bd CLI (beads) for issue tracking, OR in-session TaskList for task-based tracking.

## Global Limits

**MAX_EPIC_ITERATIONS = 50** (hard limit across entire epic)

This prevents infinite loops on circular dependencies or cascading failures.

**Why 50?**
- Typical epic: 5-10 issues
- With retries: ~5 iterations per issue max
- 50 = safe upper bound (10 issues × 5 retries)

**MAX_PARALLEL_AGENTS = 3** (hard limit per wave)

When multiple issues are ready, execute them in parallel using subagents. Capped at 3 to prevent context explosion.

**Why 3?**
- Each subagent returns results that accumulate in context
- 3 parallel agents = manageable context growth
- Higher parallelism risks context overflow on complex issues

## Completion Enforcement (The Sisyphus Rule)

**THE SISYPHUS RULE:** Not done until explicitly DONE.

After each task, output completion marker:
- `<promise>DONE</promise>` - Epic truly complete, all issues closed
- `<promise>BLOCKED</promise>` - Cannot proceed (with reason)
- `<promise>PARTIAL</promise>` - Incomplete (with remaining items)

**Never claim completion without the marker.**

## Execution Steps

Given `/crank [epic-id]`:

### Step 0: Load Knowledge Context (ao Integration)

**Search for relevant learnings before starting the epic:**

```bash
# If ao CLI available, inject prior knowledge about epic execution
if command -v ao &>/dev/null; then
    # Search for relevant learnings
    ao search "epic execution implementation patterns" 2>/dev/null | head -20

    # Check flywheel status
    ao flywheel status 2>/dev/null

    # Get current ratchet state
    ao ratchet status 2>/dev/null
fi
```

If ao not available, skip this step and proceed. The knowledge flywheel enhances but is not required.

### Step 1: Identify the Epic

**If epic ID provided:** Use it directly. Do NOT ask for confirmation.

**If no epic ID:** Discover it:
```bash
bd list --type epic --status open 2>/dev/null | head -5
```

If bd not available, look for a plan:
```bash
ls -lt .agents/plans/ 2>/dev/null | head -3
```

If multiple epics found, ask user which one.

### Step 1a: Initialize Iteration Counter

```bash
# Initialize crank tracking in epic notes
bd update <epic-id> --append-notes "CRANK_START: iteration=0 at $(date -Iseconds)" 2>/dev/null
```

Track in memory: `iteration=0`

### Step 2: Get Epic Details

```bash
bd show <epic-id> 2>/dev/null
```

Or read the plan document if using file-based tracking.

### Step 3: List Ready Issues (Current Wave)

Find issues that can be worked on (no blockers):
```bash
bd ready 2>/dev/null
```

**`bd ready` returns the current wave** - all unblocked issues. These can be executed in parallel because they have no dependencies on each other.

Or parse the plan document for Wave 1 issues.

Or use TaskList tool if using in-session task tracking.

### Step 3a: Pre-flight Check - Issues Exist

**Verify there are issues to work on:**

**If 0 ready issues found:**
```
STOP and return error:
  "No ready issues found for this epic. Either:
   - All issues are blocked (check dependencies)
   - Epic has no child issues (run /plan first)
   - All issues already completed"
```

Do NOT proceed with empty issue list - this produces false "epic complete" status.

### Step 4: Execute Wave (Parallel Subagents)

Ready issues are executed in parallel waves. Each wave dispatches up to MAX_PARALLEL_AGENTS (3) subagents.

**BEFORE each wave:**
```bash
# Increment iteration counter (count waves, not individual issues)
iteration=$((iteration + 1))
bd update <epic-id> --append-notes "CRANK_WAVE: $iteration at $(date -Iseconds)" 2>/dev/null

# CHECK GLOBAL LIMIT
if [[ $iteration -ge 50 ]]; then
    echo "<promise>BLOCKED</promise>"
    echo "Global iteration limit (50) reached. Remaining issues:"
    bd children <epic-id> --status open 2>/dev/null
    # STOP - do not continue
fi
```

**Wave Execution Logic:**

1. **Get ready issues from Step 3**
2. **Batch into wave** (max 3 issues per wave)
3. **Dispatch subagents in parallel using Task tool**

**FOR EACH WAVE, USE THE TASK TOOL IN PARALLEL:**

When you have N ready issues (where N ≤ 3), dispatch them in a SINGLE message with multiple Task tool calls:

```
# Example: 3 ready issues → 3 parallel Task calls in ONE message

Tool: Task (call 1)
Parameters:
  subagent_type: "general-purpose"
  description: "Implement <issue-id-1>"
  prompt: |
    Execute /implement <issue-id-1>

    Use the Skill tool to invoke the implement skill:
    - skill: "agentops:implement"
    - args: "<issue-id-1>"

    Return the completion marker when done.

Tool: Task (call 2)
Parameters:
  subagent_type: "general-purpose"
  description: "Implement <issue-id-2>"
  prompt: |
    Execute /implement <issue-id-2>

    Use the Skill tool to invoke the implement skill:
    - skill: "agentops:implement"
    - args: "<issue-id-2>"

    Return the completion marker when done.

Tool: Task (call 3)
Parameters:
  subagent_type: "general-purpose"
  description: "Implement <issue-id-3>"
  prompt: |
    Execute /implement <issue-id-3>

    Use the Skill tool to invoke the implement skill:
    - skill: "agentops:implement"
    - args: "<issue-id-3>"

    Return the completion marker when done.
```

**CRITICAL: All Task calls for a wave MUST be in a single message to enable parallel execution.**

**If more than 3 ready issues:** Process in batches of 3. Complete one wave before starting the next.

**Check results from each subagent:**
- If `<promise>BLOCKED</promise>` returned → record blocker, continue with others
- If `<promise>PARTIAL</promise>` returned → record remaining, continue with others
- If `<promise>DONE</promise>` returned → issue complete

**Wait for all subagents in the wave to complete before proceeding to Step 5.**

### Step 5: Track Progress (No Per-Issue Vibe)

After implement completes:

1. Update issue status:
```bash
bd update <issue-id> --status closed 2>/dev/null
```
Or use TaskUpdate to mark task completed.

2. Track changed files in memory or use TaskCreate to note them.

3. **Record ratchet progress (ao integration):**
```bash
# If ao CLI available, record implementation progress
if command -v ao &>/dev/null; then
    ao ratchet record implement 2>/dev/null
    echo "Ratchet: recorded implementation of <issue-id>"
fi
```

If ao not available, skip ratchet recording.

**Note:** Skip per-issue vibe - validation is batched at the end to save context.

### Step 6: Check for More Work

After completing an issue:
1. Check if new issues are now unblocked (use `bd ready` or TaskList)
2. If yes, return to Step 4
3. If no more issues after 3 retry attempts, proceed to Step 7
4. **Max retries:** If issues remain blocked after 3 checks, escalate: "Epic blocked - cannot unblock remaining issues"

### Step 7: Final Batched Validation

When all issues complete, run ONE comprehensive vibe on recent changes:

```bash
# Get list of changed files from recent commits
git diff --name-only HEAD~10 2>/dev/null | sort -u
```

**Run vibe on recent changes:**
```
Tool: Skill
Parameters:
  skill: "agentops:vibe"
  args: "recent"
```

**If CRITICAL issues found:**
1. Fix them
2. Re-run vibe on affected files
3. Only proceed to completion when clean

### Step 8: Extract Learnings (ao Integration)

**Before reporting completion, extract learnings from the session:**

```bash
# If ao CLI available, forge learnings from this epic execution
if command -v ao &>/dev/null; then
    # Extract learnings from recent session transcripts
    ao forge transcript ~/.claude/projects/*/conversations/*.jsonl 2>/dev/null

    # Show flywheel status post-execution
    echo "=== Flywheel Status ==="
    ao flywheel status 2>/dev/null

    # Show pending learnings for review
    ao pool list --tier=pending 2>/dev/null | head -10
fi
```

If ao not available, skip learning extraction. Recommend user runs `/post-mortem` manually.

### Step 9: Report Completion

Tell the user:
1. Epic ID and title
2. Number of issues completed
3. Total iterations used (of 50 max)
4. Final vibe results
5. Flywheel status (if ao available)
6. Suggest running `/post-mortem` to review and promote learnings

**Output completion marker:**
```
<promise>DONE</promise>
Epic: <epic-id>
Issues completed: N
Iterations: M/50
Flywheel: <status from ao flywheel status>
```

If stopped early:
```
<promise>BLOCKED</promise>
Reason: <global limit reached | unresolvable blockers>
Issues remaining: N
Iterations: M/50
```

## The FIRE Loop

Crank follows FIRE for each wave:

| Phase | Action |
|-------|--------|
| **FIND** | `bd ready` - get unblocked issues |
| **IGNITE** | Dispatch up to 3 subagents in parallel (one per issue) |
| **REAP** | Collect results from all subagents |
| **ESCALATE** | Fix blockers, retry failures |

**Parallel Wave Model:**
```
Wave 1: [issue-1, issue-2, issue-3] → 3 subagents in parallel
         ↓         ↓         ↓
      DONE      DONE      BLOCKED
                            ↓
                      (retry in next wave)

Wave 2: [issue-4, issue-3-retry] → 2 subagents in parallel
         ↓         ↓
      DONE      DONE

Final vibe on all changes → Epic DONE
```

Loop until all issues are CLOSED.

## Key Rules

- **If epic ID given, USE IT** - don't ask for confirmation
- **Parallel waves** - execute up to 3 issues per wave using subagents
- **One subagent per issue** - each issue gets its own isolated agent
- **Max 3 subagents per wave** - prevents context explosion
- **Batch validation at end** - ONE vibe at the end saves context
- **Fix CRITICAL before completion** - address findings before reporting done
- **Loop until done** - don't stop until all issues closed
- **Autonomous execution** - minimize human prompts
- **Respect iteration limit** - STOP at 50 iterations (hard limit)
- **Output completion markers** - DONE, BLOCKED, or PARTIAL (required)
- **Knowledge flywheel** - load learnings at start, forge at end (ao optional)

## Without Beads

If bd CLI not available:
1. Use the plan document as the source of truth
2. Track completed issues by checking git commits
3. Mark issues done by noting in the plan document
