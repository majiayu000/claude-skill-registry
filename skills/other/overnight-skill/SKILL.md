---
name: overnight
description: Autonomous background agent — give it a big coding goal, walk away, come back to a branch of working code. Decomposes, executes, and verifies tasks unattended.
user_invocable: true
argument-hint: "[big goal description]"
---

# Overnight — Autonomous Long-Running Coding

> One big goal. Maximum decomposition. Come back to working code.

You are the **orchestrator**. The user gives you a high-level objective. You decompose it into maximum atomic tasks, then execute each in an isolated worktree session — sequentially, autonomously, until all complete or a termination condition fires.

**You do NOT write code. You decompose, dispatch, monitor, and merge.**

---

## Phase 0: Preflight

Before anything else, verify the workspace is safe to use:

```bash
# Reject dirty working tree
if [ -n "$(git status --porcelain)" ]; then
  echo "ERROR: Uncommitted changes detected. Commit or stash before running /overnight."
  exit 1
fi
```

If the working tree is dirty, **stop immediately** and tell the user to commit or stash first.

If CLAUDE.md does not exist, inform the user: "No CLAUDE.md found. The first task will generate one from codebase analysis."

---

## Phase 1: Decompose

### Step 1 — Understand the Goal

Read the project's CLAUDE.md, README, and key source files. Build enough context to decompose intelligently.

### Step 2 — Generate the Plan

Break the goal into the **maximum number** of small, single-concern tasks. More tasks = smaller blast radius = safer autonomous execution.

**Decomposition heuristics:**
- One task per public API endpoint
- One task per database model or schema change
- One task per error-handling path
- One task per configuration concern
- Test task before implementation task when adding behavior

**Task format — every task MUST follow this structure:**

```markdown
- [ ] **Task title** `overnight-<n>`
  - <EARS requirement>
  - Acceptance: `<shell command returning 0>` | REVIEW: <what to check>
  - Files: <expected files to create or modify>
```

The backtick name (`overnight-<n>`) is the **worker name** = worktree name.

### EARS Patterns

Every task uses one of the five EARS (Easy Approach to Requirements Syntax) patterns. Choose the correct one:

| Pattern | Syntax | When to use |
|---------|--------|-------------|
| **Ubiquitous** | THE SYSTEM SHALL [behavior] | Always-true behavior. No precondition. |
| **Event-driven** | WHEN [event] THE SYSTEM SHALL [behavior] | Response to a discrete trigger. |
| **State-driven** | WHILE [state] THE SYSTEM SHALL [behavior] | Behavior during a continuous condition. |
| **Unwanted behavior** | IF [condition] THEN THE SYSTEM SHALL [behavior] | Exception/error handling. |
| **Optional feature** | WHERE [feature is supported] THE SYSTEM SHALL [behavior] | Configurable capability. |

**Examples:**
```markdown
- [ ] **Expose health endpoint** `overnight-1`
  - THE SYSTEM SHALL expose a GET /health endpoint returning 200 with { status: "ok" }
  - Acceptance: `curl -sf http://localhost:3000/health | grep -q ok`
  - Files: src/routes/health.ts, tests/health.test.ts

- [ ] **Hash passwords on registration** `overnight-2`
  - WHEN a user account is created THE SYSTEM SHALL store the password using bcrypt with cost factor 12
  - Acceptance: `npm test -- --grep "password hashing"`
  - Files: src/models/user.ts, tests/user.test.ts

- [ ] **Handle duplicate email registration** `overnight-3`
  - IF a registration request uses an email that already exists THEN THE SYSTEM SHALL return 409 Conflict
  - Acceptance: `npm test -- --grep "duplicate email"`
  - Files: src/routes/auth.ts, tests/auth.test.ts

- [ ] **Maintain session during active use** `overnight-4`
  - WHILE a user session is active THE SYSTEM SHALL refresh the session TTL on each authenticated request
  - Acceptance: `npm test -- --grep "session refresh"`
  - Files: src/middleware/session.ts, tests/session.test.ts
```

### Acceptance Criteria

Two modes are allowed:

| Mode | Format | When to use |
|------|--------|-------------|
| **Machine-verifiable** | `Acceptance: \`command\`` | Tests, builds, linting, grep checks |
| **Review-required** | `Acceptance: REVIEW: <description>` | Refactoring, documentation, UI changes |

Tasks with `REVIEW:` acceptance are marked `- [R]` on completion instead of `- [x]`, signaling they need human review.

### Rules

1. **EARS syntax required.** Choose the correct pattern. No ambiguous descriptions.
2. **One task = one concern.** Two modules? Split. Two EARS clauses? Split.
3. **Order matters.** Sequential execution. No forward dependencies.
4. **Tests first when possible.** Test task before implementation task.
5. **File scope required.** Every task lists expected files to touch.

### Step 3 — Present the Plan and Collaborate

1. Write the plan to `overnight-plan.md`.

2. Present the plan to the user with a cost estimate:
   ```
   Overnight plan: <goal summary>
   Tasks: <N>
   Estimated cost: ~$<N × 3-5> (based on ~$3-5 per task)
   Branch: <OVERNIGHT_BRANCH> (will be created on "go")

   Full plan written to: overnight-plan.md
   ```

3. Then **discuss the plan with the user**. Prompt:
   ```
   Review the plan above. You can:
     - "add ..."        → describe a missing task to insert
     - "split N"        → break task N into smaller pieces
     - "drop N"         → remove a task
     - "edit"           → pause while you edit overnight-plan.md directly
     - "go"             → approve and start autonomous execution
   ```

4. **Stay in this loop until the user says "go".** For each refinement:
   - Apply the change to `overnight-plan.md`
   - Show the affected tasks (not the full plan)
   - Re-prompt for further input

5. On "go", create the branch and commit:
   ```bash
   OVERNIGHT_BRANCH="overnight/$(date '+%Y-%m-%d-%H%M%S')"
   git checkout -b "$OVERNIGHT_BRANCH"
   git add overnight-plan.md
   git commit -m "overnight: plan — <goal summary>"
   ```

6. **Immediately** begin Phase 2. From here on, execution is fully autonomous.

**The plan is collaborative. The execution is not.** Time spent refining the plan saves hours of wasted autonomous work.

---

## Phase 2: Execute (Orchestrator Loop)

You are the orchestrator. For each task in `overnight-plan.md`, do the following:

### 2.1 — Check Termination Conditions

Before each task, check ALL of these. Stop if any is true:

| Condition | Action |
|-----------|--------|
| `.overnight-stop` file exists | Remove file. **Print summary. End: "Stopping as requested. Here's where things stand..."** |
| 3 consecutive tasks BLOCKED | **Print summary. End: "Hit a wall — 3 tasks in a row couldn't complete. Here's what's blocking..."** |
| No `- [ ]` remain in plan | **Go to Phase 3 (Mine for More Work).** |

Only `.overnight-stop` and consecutive failures are hard stops. Completing the plan triggers Phase 3.

### 2.2 — Select Next Task

Find the first `- [ ]` task in `overnight-plan.md`. **Skip any task that contains `<!-- BLOCKED` — these have already failed and should not be retried.**

### 2.3 — Dispatch Worker

Use the **Agent tool** with `isolation: "worktree"` to spawn each worker. This gives the worker a full isolated copy of the repo where it can read, write, and execute code — then returns results back to the orchestrator.

```
Agent(
  name: "overnight-<n>",
  description: "<task title>",
  isolation: "worktree",
  mode: "bypassPermissions",
  prompt: "You are an overnight worker session.

    YOUR TASK:
    <full task block from overnight-plan.md>

    INSTRUCTIONS:
    1. Read the project's CLAUDE.md first for context.
    2. Read the code relevant to this task before changing anything.
    3. Implement ONLY this task. Do not touch anything else.
    4. Run the acceptance command: <acceptance command>
    5. If it passes, commit your changes with message: 'overnight: <task title>'
    6. If it fails, retry up to 3 times with exponential backoff:
       - First retry: wait 2 seconds, then fix and re-run
       - Second retry: wait 4 seconds, then fix and re-run
       - Third retry: wait 8 seconds, then fix and re-run
    7. If still failing after 3 retried attempts, commit what you have with message:
       'overnight: BLOCKED — <reason>'
    8. Do NOT run git checkout, git merge, or switch branches.
    9. Report what you did when done."
)
```

**This is a blocking call.** The orchestrator waits until the Agent returns. The worktree is automatically created and the worker has full file read/write/execute capabilities.

**Retry strategy:** Workers use exponential backoff when the acceptance command fails: 2s, 4s, 8s delays between retries. This avoids hammering flaky commands (e.g., servers still starting, file locks) and gives transient issues time to resolve before marking a task BLOCKED.

### 2.4 — Evaluate Result

When the Agent returns, check:

1. **Did the worker report success or BLOCKED?** Read the agent's return message.
2. **Verify with git:**
   ```bash
   # If the agent made changes, it returns the worktree path and branch
   # Check the last commit message on that branch
   git log --oneline -1 <worktree-branch>
   ```

- **If BLOCKED:** Update `overnight-plan.md` — add `<!-- BLOCKED: reason -->` after the task line. Increment consecutive failure counter.
- **If success:** Reset consecutive failure counter to 0.
- **If REVIEW acceptance:** Mark as `- [R]` instead of `- [x]`.

### 2.5 — Merge to Overnight Branch

**If the worker made changes** (agent returned a worktree path/branch):

```bash
git checkout "$OVERNIGHT_BRANCH"

# Attempt squash-merge
if git merge --squash <worktree-branch>; then
  git commit -m "overnight: <task title>"
else
  # Merge conflict — mark as BLOCKED, abort
  git merge --abort
  # Mark task BLOCKED in overnight-plan.md
  # Increment consecutive failure counter
fi
```

**If the agent returned with no changes** (worktree auto-cleaned), the task either failed or was a no-op. Check the agent's return message to determine which.

### 2.6 — Cleanup and Update State

Worktrees from Agent tool are **automatically cleaned up** if no changes were made. If changes were made and merged:

```bash
# Find actual worktree path
WORKTREE_PATH=$(git worktree list | grep <name> | awk '{print $1}')

# Remove worktree (if still exists after merge)
git worktree remove "$WORKTREE_PATH" 2>/dev/null || true

# Force delete — squash-merge creates a new commit, so git won't recognize
# the branch as "merged" even though it is. -D is correct here.
git branch -D <worktree-branch> 2>/dev/null || true
```

Update `overnight-plan.md`: mark task `- [x]` (or `- [R]` for REVIEW tasks).

Commit the state update:

```bash
git add overnight-plan.md
git commit -m "overnight: mark <task title> complete"
```

### 2.7 — Report Progress

After each task completes and state is updated, print a progress line so the user can see status at a glance:

```
Progress: 5/18 done (28%) | 1 blocked | elapsed: 42m | success rate: 83%
```

Compute this from `overnight-plan.md`:
- **done** = count of `- [x]` + `- [R]` lines
- **total** = count of all task lines (`- [x]`, `- [R]`, `- [ ]`, BLOCKED)
- **blocked** = count of `<!-- BLOCKED` lines
- **elapsed** = wall-clock time since Phase 2 started (track the start timestamp)
- **success rate** = done / (done + blocked) as a percentage (100% if no tasks attempted yet)

This progress line keeps the session log readable for async monitoring.

### 2.8 — Next Task

Loop back to **2.1**. The next worker inherits all previous merged work because it branches from the updated overnight branch.

---

## Phase 3: Mine for More Work

When all `- [ ]` tasks are complete, **do not stop**. Actively search for more meaningful work. You may mine up to **5 cycles** before stopping.

### Mining procedure

Each cycle:

1. **Run objective checks.** Run the full test suite. Run the linter. Run the build. These are facts, not opinions.

2. **Read the code that was produced.** Actually review the implementations — don't just check if tests pass. Look at the code with fresh eyes.

3. **Systematically look for gaps across these categories:**

   | Category | What to look for |
   |----------|-----------------|
   | **Test failures** | Tests or lint errors introduced by overnight work |
   | **BLOCKED retries** | Tasks that failed before but can now be approached differently |
   | **TODOs in code** | `TODO`, `FIXME`, `HACK` left by workers |
   | **Error handling** | Missing error paths, unhandled edge cases |
   | **Integration gaps** | Components that were built separately but not wired together |
   | **Missing tests** | New code paths without test coverage |
   | **Spec compliance** | Requirements from CLAUDE.md or specs not fully met |

4. **If you find work:** Generate new tasks in the same EARS format, append to `overnight-plan.md`, commit, and loop back to **Phase 2**.

5. **If genuinely nothing found this cycle:** Stop mining. Print final summary and end.

### Mining rules

- **Be thorough, not creative.** Mine for gaps in what was built, not new features.
- **Each cycle must produce at least 1 task or stop.** No empty cycles.
- **Read the actual code, don't just grep.** Shallow checks find shallow issues.
- **BLOCKED tasks deserve a second look.** The codebase has changed since they failed — a different approach may work now.
- **If the original goal has clearly unfinished aspects, keep going.** Don't stop just because the initial plan is done if the goal isn't fully achieved.

---

## Resume & Recovery

If the orchestrator session is interrupted — context window exhausted, connection lost, or process killed — the system can recover because `overnight-plan.md` IS the persistent state.

### How recovery works

1. **`overnight-plan.md` is the source of truth.** Checked tasks (`- [x]`, `- [R]`) are done and already merged to the overnight branch. The first unchecked `- [ ]` task (that is not `<!-- BLOCKED`) is where execution should continue.

2. **Re-invoke `/overnight` on the same branch to resume.** If an `overnight-plan.md` already exists on the current branch, the orchestrator should detect it and skip Phase 1 (decomposition). Instead, it picks up from the first incomplete task and continues the Phase 2 execution loop. No re-planning needed.

3. **Manual recovery is also possible.** A user can:
   - Check off tasks that were completed outside the session (`- [ ]` → `- [x]`)
   - Remove or edit tasks that are no longer relevant
   - Then re-run `/overnight` to continue from the updated state

### Clean up orphaned worktrees

An interrupted session may leave behind worktrees from in-progress workers. Before resuming, clean them up:

```bash
# List all worktrees — look for any overnight-* entries
git worktree list

# Remove orphaned worktrees
git worktree remove /path/to/orphaned-worktree 2>/dev/null || true

# Prune stale worktree references
git worktree prune

# Delete orphaned branches
git branch -D agent-overnight-<n> 2>/dev/null || true
```

### What about partially-completed workers?

If a worker was mid-task when the session died, its worktree may contain uncommitted or unmerged changes. The safest recovery path is:

1. Check `git worktree list` for leftover worktrees.
2. Inspect the worktree — if it has useful committed work, cherry-pick or squash-merge it manually.
3. If the work is incomplete or broken, remove the worktree and let the resumed session re-dispatch the task from scratch.

The task will still be `- [ ]` in the plan, so the resumed orchestrator will re-attempt it automatically.

---

## Final Summary

When stopping for any reason, always print a structured summary:

```
══════════════════════════════════════════
OVERNIGHT COMPLETE
══════════════════════════════════════════
Goal:      <original goal>
Branch:    <OVERNIGHT_BRANCH>
Completed: <N> tasks  [x]
Review:    <N> tasks  [R]
Blocked:   <N> tasks  <!-- BLOCKED -->
Remaining: <N> tasks  [ ]

Files changed: <output of git diff --stat main..OVERNIGHT_BRANCH>

Next steps:
  git diff main...<OVERNIGHT_BRANCH>        # review all changes
  gh pr create --head <OVERNIGHT_BRANCH>    # ship it
  git branch -D <OVERNIGHT_BRANCH>          # discard
══════════════════════════════════════════
```

### Cleanup

After printing the summary, clean up runtime artifacts from the branch:

```bash
rm -f overnight-plan.md .overnight-stop
rm -rf .overnight-logs/
git add -A
git commit -m "overnight: cleanup runtime artifacts"
```

`overnight-plan.md` served its purpose as the state machine during execution. The git history preserves the full record — the file itself is no longer needed.

Then end with: **"I'm going to bed too..."**

---

## State Machine

```
overnight-plan.md IS the state.

- [x] **Task title** `overnight-1`                          ← done, merged
- [R] **Task title** `overnight-2`                          ← done, needs human review
- [ ] **Task title** `overnight-3`                          ← next up (first unchecked)
- [ ] **Task title** <!-- BLOCKED: reason --> `overnight-4`  ← failed, SKIPPED
```

**BLOCKED tasks are skipped, never retried in Phase 2.** Phase 3 may attempt them with a different strategy.

---

## Anti-Patterns

- **"Update the API and add tests and fix the docs"** → Three tasks. Split.
- **"Make it work correctly"** → Not EARS. Which pattern? What behavior?
- **"Acceptance: looks good"** → Not verifiable. Use a command or REVIEW.
- **Orchestrator writing code** → Never. You dispatch, monitor, merge.
- **Retrying a BLOCKED task with the same approach** → Skip it. Phase 3 may try a different strategy.
- **Mining busywork** → If the task feels like filler, stop. Only objective gaps.

---

## Orchestrator Checklist

For each task iteration, you (the orchestrator) must:

1. Check termination conditions (stop file, consecutive failures, all done)
2. Select next `- [ ]` task, skipping any with `<!-- BLOCKED`
3. Spawn worker via Agent tool with `isolation: "worktree"` and `mode: "bypassPermissions"`
4. Wait for Agent to return (blocking call)
5. Evaluate result: success, REVIEW, or BLOCKED
6. If changes were made: squash-merge to overnight branch (verify success before cleanup)
7. Cleanup worktree and branch (`git branch -D` — safe after squash-merge)
8. Update `overnight-plan.md` checkbox
9. Commit state update
10. Print progress line (done/total, blocked, elapsed time, success rate)
11. Loop
