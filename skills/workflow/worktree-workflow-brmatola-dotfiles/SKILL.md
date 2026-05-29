---
name: worktree-workflow
description: Use to orchestrate the full development loop in a worktree - chains plan review, implementation, audit, and optional reach phases with state tracking
---

# Worktree Workflow

## Overview

Orchestrate the full development loop: review → implement → audit → finish/reach.

**Core principle:** Guided workflow with state persistence across sessions.

**Announce at start:** "I'm using the worktree-workflow skill to [start/continue] the development workflow."

**State file:** `.workflow-state.json` (repo root)

## Invocation Patterns

| Command | Behavior |
|---------|----------|
| `/worktree-workflow` | Auto-detect phase from state, continue where left off |
| `/worktree-workflow start {plan}` | Initialize workflow, run readiness review |
| `/worktree-workflow implement` | Kick off autonomous implementation |
| `/worktree-workflow audit` | Run implementation review |
| `/worktree-workflow reach` | Run reach opportunities |
| `/worktree-workflow status` | Show current state and history |
| `/worktree-workflow abort` | Abandon workflow, clean up state |

## Phase Flow

```
start → [plan-readiness-review] → markdown summary
                                        ↓
                              User: "looks good" / adjust
                                        ↓
implement → [executing-plans autonomous] → markdown summary
                                        ↓
audit → [implementation-review] → markdown summary
                                        ↓
                    AskUserQuestion: "What next?"
                         ┌──────────────┴──────────────┐
                         ↓                             ↓
                   "Done, finish branch"        "Explore reach opportunities"
                         ↓                             ↓
                   [sync-with-base]             reach → [reach-opportunities]
                         ↓                             ↓
           [finishing-a-development-branch]    pick items → implement
                         ↓                             ↓
                   [plan-complete]             back to audit
```

## State Management

### State File Location

Check for Emacs metadata first:

```bash
REPO=$(basename "$(git rev-parse --show-toplevel)")
BRANCH=$(git branch --show-current)
EMACS_METADATA="$HOME/worktrees/metadata/$REPO/$BRANCH.json"

if [[ -f "$EMACS_METADATA" ]]; then
  # Use Emacs metadata - read/write workflow as nested key
  # Read:  jq -r '.workflow // empty' "$EMACS_METADATA"
  # Write: Use Read tool, modify plist, use Write tool
  STATE_LOCATION="emacs"
else
  # Fallback for non-Emacs sessions
  STATE_LOCATION=".workflow-state.json"
  # Ensure state file is gitignored (workflow state is session-specific)
  if ! grep -q ".workflow-state.json" .gitignore 2>/dev/null; then
    echo ".workflow-state.json" >> .gitignore
  fi
fi
```

**Emacs metadata workflow key:**
```json
{
  "workflow": {
    "plan": "plan-name",
    "phase": "review",
    "started": "2026-02-01T10:00:00Z",
    "history": []
  }
}
```

When writing to Emacs metadata, merge the workflow key into existing JSON (don't overwrite other fields).

### State Schema

```json
{
  "plan": "plan-name",
  "phase": "review | implement | audit | reach | complete",
  "started": "2025-01-31T10:00:00Z",
  "history": [
    { "phase": "review", "verdict": "READY", "timestamp": "..." },
    { "phase": "implement", "tasks": "12/12", "timestamp": "..." }
  ],
  "reachIterations": 0
}
```

### Reading State

```bash
cat .workflow-state.json 2>/dev/null || echo "No workflow state"
```

### Writing State

Use Write tool to update `.workflow-state.json` after each phase.

## The Process

### On Invocation: Detect Current State

1. Check for `.workflow-state.json`
2. If exists: Resume from recorded phase
3. If not: Prompt user for plan name to start

### Phase: start

**Trigger:** `/worktree-workflow start {plan-name}` or first run with plan name

1. **Verify not on main branch:**
   ```bash
   current=$(git branch --show-current)
   if [[ "$current" == "main" || "$current" == "master" ]]; then
     echo "ERROR: Cannot run workflow on $current branch. Use a feature branch in a worktree."
     exit 1
   fi
   ```
2. Verify plan exists at `plans/active/{plan-name}/`
3. Initialize state file:
   ```json
   {
     "plan": "{plan-name}",
     "phase": "review",
     "started": "{timestamp}",
     "history": [],
     "reachIterations": 0
   }
   ```
4. **INVOKE:** gremlins:plan-readiness-review
5. Present markdown summary
6. Wait for user to approve or request changes

**If READY:** User says "looks good" → advance to implement phase
**If NEEDS WORK:** User fixes issues → re-run review

### Phase: implement

**Trigger:** User approves plan review OR `/worktree-workflow implement`

1. Update state to `"phase": "implement"`
2. **INVOKE:** gremlins:executing-plans (autonomous mode)
3. On completion, update state with task count
4. Add history entry
5. Present completion summary
6. Advance to audit phase

### Phase: audit

**Trigger:** Implementation complete OR `/worktree-workflow audit`

1. Update state to `"phase": "audit"`
2. **INVOKE:** gremlins:implementation-review
3. Add history entry with verdict

**If MERGE READY:**

Present choice using AskUserQuestion:

```
Implementation passed review. What would you like to do?

1. Done - finish the branch (merge/PR)
2. Explore reach opportunities first
```

- Option 1 → Sync with base, then **INVOKE:** gremlins:finishing-a-development-branch, then plan-complete
- Option 2 → Advance to reach phase

**If NEEDS FIXES:**
- Present issues
- User fixes
- Re-run audit

### Phase: reach

**Trigger:** User chooses "Explore reach opportunities" OR `/worktree-workflow reach`

1. Check iteration count:
   ```
   if reachIterations >= 2:
     Present: "You've done 2 reach cycles. Recommend finishing branch now."
     Offer: finish anyway OR one more reach cycle
   ```
2. Update state: `"phase": "reach"`, increment `reachIterations`
3. **INVOKE:** gremlins:reach-opportunities
4. Present opportunities
5. User picks items to implement (or none)

**If items selected:**
- Implement selected items
- Return to audit phase for re-review

**If no items selected:**
- Sync with base
- **INVOKE:** gremlins:finishing-a-development-branch
- **INVOKE:** gremlins:plan-complete
- Mark complete

### Before Finishing: Sync With Base

**Always run this before invoking finishing-a-development-branch:**

```bash
# Fetch latest from remote
git fetch origin

# Detect base branch
base_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
if [ -z "$base_branch" ]; then
  base_branch=$(git merge-base HEAD main 2>/dev/null && echo main || echo master)
fi

# Check if base has advanced since we branched
merge_base=$(git merge-base HEAD "origin/$base_branch")
if [ "$(git rev-parse origin/$base_branch)" != "$merge_base" ]; then
  echo "Base branch ($base_branch) has new commits since you started."
fi
```

**If base has advanced, present options:**

```
Base branch has new commits. How would you like to proceed?

1. Rebase on latest base (recommended - cleaner history)
2. Merge base into feature branch (preserves history)
3. Proceed anyway (PR may have conflicts)
```

**Option 1 (Rebase):**
```bash
git rebase "origin/$base_branch"
# If conflicts, stop and let user resolve
# Re-run tests after rebase
```

**Option 2 (Merge base in):**
```bash
git merge "origin/$base_branch" -m "Merge $base_branch into $(git branch --show-current)"
# If conflicts, stop and let user resolve
# Re-run tests after merge
```

**Option 3:** Proceed without sync (user accepts potential conflicts)

**If base hasn't advanced:** Skip directly to finishing-a-development-branch.

### Phase: complete

1. **INVOKE:** gremlins:plan-complete (moves plan from active/ to complete/)

2. Update state:
```json
{
  "phase": "complete",
  "history": [..., { "phase": "complete", "timestamp": "..." }]
}
```

3. Report: "Workflow complete for {plan-name}. Plan moved to complete/."

## Abort Command

`/worktree-workflow abort` handles workflow abandonment:

1. Read current state
2. Report what was completed:
   ```
   ## Workflow Aborted: {plan-name}

   ### Progress Before Abort
   | Phase | Status |
   |-------|--------|
   | review | ✓ READY |
   | implement | 8/12 tasks |

   ### Branch State
   - Branch: {branch-name}
   - Commits since start: {N}

   ### Cleanup
   - State file removed
   - Branch preserved (delete manually if needed)
   ```
3. Delete `.workflow-state.json`
4. Do NOT delete the branch or commits (user decides)

## Status Command

`/worktree-workflow status` outputs:

```
## Workflow Status: {plan-name}

**Current Phase:** {phase}
**Started:** {started}

### History
| Phase | Result | Timestamp |
|-------|--------|-----------|
| review | READY | 2025-01-31 10:00 |
| implement | 12/12 tasks | 2025-01-31 11:30 |

### Next Step
[What to do next based on current phase]
```

## Key Behaviors

- **State persists:** Pick up where you left off across sessions
- **Phases are skippable:** Can jump to audit if implemented manually
- **Reach is opt-in:** Only explore if user chooses after passing audit
- **Sub-skills do the work:** Orchestrator invokes, doesn't duplicate logic
- **Sync before finishing:** Always fetch and check base branch before merge/PR
- **Plan lifecycle:** Invokes plan-complete to move plan from active/ to complete/

## Red Flags

**Never:**
- Skip phases without user acknowledgment
- Proceed to implement without plan review passing
- Proceed to finish without audit passing
- Force reach opportunities on user

**Always:**
- Check state on every invocation
- Update state after every phase transition
- Present clear options at decision points
- Invoke sub-skills rather than duplicating their logic
- Sync with base branch before finishing (fetch + check for divergence)
- Move plan to complete/ after successful finish

## Integration

**Invokes:**
- gremlins:plan-readiness-review (start phase)
- gremlins:executing-plans (implement phase)
- gremlins:implementation-review (audit phase)
- gremlins:reach-opportunities (reach phase, opt-in)
- gremlins:finishing-a-development-branch (completion)
- gremlins:plan-complete (moves plan to complete/)

**Prerequisite:**
- gremlins:using-git-worktrees - Creates the worktree first

**Assumption:**
- Plan committed to repo before worktree created
