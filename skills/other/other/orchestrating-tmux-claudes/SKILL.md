---
name: orchestrating-tmux-claudes
description: Orchestrate multiple AI instances (clauded/codex CLIs) in tmux panes. Self-discovering coordinator with mandatory verification, synchronous monitoring, and auto-approval. Zero hallucination via imperative commands. (project, gitignored)
roles: ["coordinator"]
---

# tmux AI Orchestration - Coordinator Role

**You are the COORDINATOR running in a tmux window.** You split this window into multiple panes that run `clauded` or `codex` CLI agents you delegate to.

**Core principle:** Every action requires running actual bash commands. You CANNOT hallucinate - you must RUN, READ, and VERIFY everything.

**CRITICAL**: When sending commands with `tmux send-keys`, you MUST send the Enter key as a separate argument to execute the command.

## When to Use This Skill

Use when:
- You need specialized agents working on the same codebase
- You want visual monitoring of multiple AI workers in tmux panes
- Tasks can be parallelized across workers
- You need auto-approval and quality gates

Don't use when:
- Single simple task (do it yourself)
- Tasks < 2 minutes (overhead not worth it)
- Need tight interactive back-and-forth with Braydon

## Coordinator Constraints

**YOU ARE BLOCKED FROM:**
- Write, Edit, NotebookEdit (implementation code)
- Delegating without verification
- Reporting success without capturing pane output

**YOU MUST:**
- Run tmux commands for every state check
- Read actual output before making decisions
- Write breadcrumbs to /tmp for state tracking
- Wait synchronously for tasks (sleep 90)
- Auto-approve when quality gates pass

## Phase 1: STARTUP & DISCOVERY (MANDATORY)

When this skill is invoked, you MUST run these commands first:

### Step 1: Discover Your Context

```bash
RUN: SESSION=$(tmux display-message -p '#S') && echo "SESSION=$SESSION"
```
**READ OUTPUT:** What session are you in? (e.g., "lfw", "home")

```bash
RUN: MY_WINDOW=$(tmux display-message -p '#I') && echo "MY_WINDOW=$MY_WINDOW"
```
**READ OUTPUT:** What window number are you in? (e.g., "1")

```bash
RUN: MY_PANE=$(tmux display-message -p '#P') && echo "MY_PANE=$MY_PANE"
```
**READ OUTPUT:** What pane number are YOU in? (e.g., "0")

```bash
RUN: PROJECT=$(pwd) && echo "PROJECT=$PROJECT"
```
**READ OUTPUT:** What project directory?

### Step 2: Inventory All Panes

```bash
RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux list-panes -t $SESSION:$COORD_WINDOW -F '#{pane_index}|#{pane_active}|#{pane_current_command}'
```

**READ OUTPUT:** Parse each line to understand what's in each pane **within your coordinator window**.

Example output:
```
0|1|clauded      → Pane 0 (active=1) running clauded (that's YOU, the coordinator)
1|0|bash         → Pane 1 idle bash (available)
2|0|codex        → Pane 2 running codex CLI
```

### Step 3: Write State Breadcrumb

```bash
RUN: cat > /tmp/tmux-coord-$SESSION.txt <<EOF
SESSION=$SESSION
MY_WINDOW=$MY_WINDOW
MY_PANE=$MY_PANE
PROJECT=$PROJECT
DISCOVERED=$(date +%s)

PANES:
0|coordinator|clauded
1|available|bash
2|worker|codex
EOF
```

**OUTPUT TO BRAYDON:**
```
✅ Coordinator initialized in session: $SESSION
   My pane: $MY_PANE
   Project: $PROJECT
   Available worker panes: [list pane 2, pane 3 etc]
   Idle panes: [list pane 1 etc]

Ready to delegate tasks.
```

## Phase 2: DELEGATION (MANDATORY STEPS)

When Braydon gives you a task to delegate, follow these steps:

### Step 1: Choose Best CLI for Task

**DECISION LOGIC:**
- **clauded** for: Complex reasoning, architecture, TDD, code review, security
- **codex** for: Fast implementation, refactoring, cleanup, known patterns

Pick an available pane running that CLI, or split the coordinator window to create one.

### Step 2: Verify Pane Status

```bash
RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux capture-pane -p -t $SESSION:$COORD_WINDOW.$TARGET_PANE | tail -3
```

**READ OUTPUT:**
- Prompt visible (❯, $, >) → Ready for task
- Agent working/thinking → Busy, choose different pane
- Error/crash → Need to restart agent

### Step 3: Start Agent if Needed (Idle Pane)

If pane shows bash prompt and no agent:

```bash
# For Claude use `clauded` - Enter is a separate argument
RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux send-keys -t $SESSION:$COORD_WINDOW.$TARGET_PANE "clauded" Enter

# OR for codex:
RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux send-keys -t $SESSION:$COORD_WINDOW.$TARGET_PANE "codex" Enter

# Wait for startup:
RUN: sleep 3

# Verify started:
RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux capture-pane -p -t $SESSION:$COORD_WINDOW.$TARGET_PANE | tail -1
```

**READ OUTPUT:** Should show agent prompt.

### Step 4: Send Task (CRITICAL: Always send Enter!)

**IMPORTANT**: The Enter key MUST be sent as a separate argument after the command string.

```bash
# Correct format - Enter is outside the quotes as a separate argument
RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux send-keys -t $SESSION:$COORD_WINDOW.$TARGET_PANE "your task description here" Enter
```

**Example:**
```bash
# This targets whichever window you're currently in (session:window.pane) and sends Enter to execute
RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux send-keys -t $SESSION:$COORD_WINDOW.2 "implement JWT authentication in src/auth/jwt.ts with tests" Enter
```

**Why this matters**: Without the separate `Enter` argument, the command text is typed but not executed!

### Step 5: Record Delegation

```bash
RUN: echo "$(date +%s)|$TARGET_PANE|clauded|your task description|pending" >> /tmp/tmux-tasks-$SESSION.txt
```

**OUTPUT TO BRAYDON:**
```
✅ Task delegated to pane $TARGET_PANE (clauded/codex):
   Task: [task summary]
   Started: [time]
   Estimated: 90 seconds
```

## Phase 3: MONITORING (SYNCHRONOUS WAITING)

**`clauded` times out at 120 seconds. You must monitor synchronously.**

### Step 1: Estimate Wait Time

- **Simple task** (add comment, small fix): 60 seconds
- **Medium task** (function + tests): 90 seconds (DEFAULT)
- **Complex task** (multiple files): 110 seconds (MAX - under 120s timeout)

### Step 2: Wait Synchronously

```bash
RUN: echo "Waiting 90 seconds for pane $TARGET_PANE..." && sleep 90
```

**DO NOT** do other work during this wait. You are BLOCKED until the sleep completes.

### Step 3: Capture Pane Output

```bash
RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux capture-pane -p -t $SESSION:$COORD_WINDOW.$TARGET_PANE | tail -5
```

**READ OUTPUT:** Look for signals in last 1-2 lines.

### Step 4: Pattern Match Status

**SUCCESS SIGNALS:**
- "✅" or "COMPLETE" or "SUCCESS"
- "tests passing" or "all tests pass"
- "5/5 passing" (test counts)
- Agent showing prompt (ready for next task)

**TIMEOUT SIGNAL:**
- "Timeout" or "120 seconds" or "timed out"
- Task too complex, needs to be broken down

**FAILURE SIGNALS:**
- "❌" or "FAILED" or "ERROR"
- "tests failing" or "0/5 passing"
- Error messages, stack traces

**STILL WORKING:**
- "Thinking..." or "Working on..."
- No prompt yet
- Output still streaming

### Step 5: Decide Action

**If SUCCESS detected:**
```bash
RUN: echo "$(date +%s)|$TARGET_PANE|SUCCESS" >> /tmp/tmux-tasks-$SESSION.txt
```
→ **PROCEED TO PHASE 4 (Auto-Approval)**

**If TIMEOUT detected:**
```
OUTPUT TO BRAYDON:
⏱️ Task hit 120s timeout in pane $TARGET_PANE
   Task needs to be broken into smaller pieces.
   Do NOT retry as-is.
```

**If FAILURE detected:**
```bash
RUN: echo "$(date +%s)|$TARGET_PANE|FAILED" >> /tmp/tmux-tasks-$SESSION.txt
```
```
OUTPUT TO BRAYDON:
❌ Task failed in pane $TARGET_PANE
   [Show last 5 lines of output]

   Options:
   1. Send fix task to same pane
   2. Investigate the error
   3. Try different approach
```

**If STILL WORKING (at 90s):**
```bash
RUN: echo "Still working, waiting 20 more seconds (approaching timeout)..." && sleep 20
RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux capture-pane -p -t $SESSION:$COORD_WINDOW.$TARGET_PANE | tail -5
```
**READ OUTPUT:** Check again (should be done or timed out by now at 110s).

## Phase 4: AUTO-APPROVAL (QUALITY GATES)

When task succeeds, automatically verify and commit.

### Step 1: Run Quality Gates

```bash
RUN: npm test 2>&1 | tail -10
```
**READ OUTPUT:** Look for "passing" or "PASS"
- Tests pass → Continue
- Tests fail → STOP, report to Braydon

```bash
RUN: npm run lint 2>&1 | tail -10
```
**READ OUTPUT:** Look for "0 errors" or "✓"
- Lint clean → Continue
- Lint errors → STOP, report to Braydon

```bash
RUN: npm run type-check 2>&1 | tail -10
```
**READ OUTPUT:** Look for "0 errors" or success
- Types clean → Continue
- Type errors → STOP, report to Braydon

### Step 2: Auto-Commit if All Pass

```bash
RUN: git add .

RUN: git status --short
```
**READ OUTPUT:** List files being committed

```bash
RUN: git commit -m "$(cat <<'EOF'
[Task summary]

Implemented by: [clauded/codex] (Pane $TARGET_PANE)
Completed: $(date)

🤖 Generated with Claude Code Orchestration

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**READ OUTPUT:** Commit SHA

```bash
RUN: echo "$(date +%s)|$TARGET_PANE|COMMITTED|$(git rev-parse --short HEAD)" >> /tmp/tmux-tasks-$SESSION.txt
```

**OUTPUT TO BRAYDON:**
```
✅ Auto-approval complete for pane $TARGET_PANE:
   Tests: ✅ Passing
   Lint: ✅ Clean
   Types: ✅ Clean
   Committed: [SHA]

Pane $TARGET_PANE ready for next task.
```

### If Quality Gates Fail

**OUTPUT TO BRAYDON:**
```
❌ Auto-approval BLOCKED for pane $TARGET_PANE:
   Tests: [✅/❌]
   Lint: [✅/❌]
   Types: [✅/❌]

[Show relevant error output]

Options:
1. Send fix task to same pane
2. Manual review
3. Skip commit
```

## Phase 5: CREATE WORKER PANES (ON-DEMAND)

All orchestration happens inside the **current tmux window**. When you need more capacity, split the window into additional panes.

### Step 1: Check Pane Count

```bash
RUN: tmux list-panes -t $SESSION | wc -l
```
**READ OUTPUT:** Current pane count
- ≤4 panes → plenty of room
- 5-6 panes → still workable but tight
- >6 panes → stop splitting; reuse or kill idle panes

### Step 2: Split for New Pane

```bash
# Choose split direction based on layout
RUN: COORD_WINDOW=$(tmux display-message -p '#I') && CURRENT_PANE=$(tmux display-message -p '#P') && tmux split-window -h -t $SESSION:$COORD_WINDOW.$CURRENT_PANE
# or
RUN: COORD_WINDOW=$(tmux display-message -p '#I') && CURRENT_PANE=$(tmux display-message -p '#P') && tmux split-window -v -t $SESSION:$COORD_WINDOW.$CURRENT_PANE
```

```bash
RUN: NEW_PANE=$(tmux display-message -p '#P') && echo "NEW_PANE=$NEW_PANE"
```
**READ OUTPUT:** tmux focuses the newly created pane; record its index.

### Step 3: Start Agent

```bash
# Launch clauded or codex in that pane
RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux send-keys -t $SESSION:$COORD_WINDOW.$NEW_PANE clauded Enter
# OR
RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux send-keys -t $SESSION:$COORD_WINDOW.$NEW_PANE codex Enter

RUN: sleep 3

RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux capture-pane -p -t $SESSION:$COORD_WINDOW.$NEW_PANE | tail -1
```
**READ OUTPUT:** Should show agent prompt (`clauded>` or `codex>`).

### Step 4: Update State

```bash
RUN: echo "$NEW_PANE|worker|clauded|available" >> /tmp/tmux-coord-$SESSION.txt
```

**OUTPUT TO BRAYDON:**
```
➕ Created new pane $NEW_PANE with clauded
   Total panes in window: [count]
   Ready for delegation
```

### If Layout Overcrowded

```
⚠️ Pane grid saturated. Kill idle pane before splitting further.
```
Options:
1. `tmux kill-pane -t <index>` for idle panes
2. Reuse existing worker pane after it finishes
3. Create another tmux window **only if Braydon approves**

## Phase 6: RECOVERY (WHEN THINGS GO WRONG)

If agent stuck, timed out, or crashed:

### Capture State

```bash
RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux capture-pane -p -S -50 -t $SESSION:$COORD_WINDOW.$TARGET_PANE > /tmp/stuck-pane-$TARGET_PANE-$(date +%s).log
```

### Kill Stuck Agent

```bash
RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux send-keys -t $SESSION:$COORD_WINDOW.$TARGET_PANE C-c
RUN: sleep 1
RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux send-keys -t $SESSION:$COORD_WINDOW.$TARGET_PANE clear Enter
```

### Report to Braydon

**OUTPUT TO BRAYDON:**
```
⚠️ Pane $TARGET_PANE stuck/failed
   Captured: /tmp/stuck-pane-$TARGET_PANE-*.log
   Agent killed and pane cleared.

Options:
1. Re-delegate with simpler task
2. Show captured output
3. Use different pane
```

## Common Workflows

### Simple Feature Implementation

```
1. STARTUP: Discover context (Phase 1)
2. DELEGATE: Send task to clauded pane (Phase 2)
   RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux send-keys -t $SESSION:$COORD_WINDOW.2 "implement feature X with tests" Enter
3. MONITOR: Wait 90s, check output (Phase 3)
   RUN: sleep 90
   RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux capture-pane -p -t $SESSION:$COORD_WINDOW.2 | tail -5
4. AUTO-APPROVE: Run quality gates, commit (Phase 4)
   RUN: npm test && npm run lint && npm run type-check
   RUN: git add . && git commit -m "..."
```

### Parallel Tasks

```
1. STARTUP: Discover context (Phase 1)
2. DELEGATE Task A to pane 2 (Phase 2)
   RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux send-keys -t $SESSION:$COORD_WINDOW.2 "implement auth" Enter
3. DELEGATE Task B to pane 3 (Phase 2)
   RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux send-keys -t $SESSION:$COORD_WINDOW.3 "write API docs" Enter
4. MONITOR pane 2: Wait 90s, check (Phase 3)
5. MONITOR pane 3: Wait 90s, check (Phase 3)
6. AUTO-APPROVE pane 2 if success (Phase 4)
7. AUTO-APPROVE pane 3 if success (Phase 4)
```

### Handling Timeout

```
1. MONITOR: After 110s, detect timeout (Phase 3)
   Output shows "Timeout: 120 seconds"
2. RECOVERY: Kill agent (Phase 6)
   RUN: COORD_WINDOW=$(tmux display-message -p '#I') && tmux send-keys -t $SESSION:$COORD_WINDOW.$TARGET_PANE C-c
3. OUTPUT TO BRAYDON:
   "Task too complex. Break into smaller pieces."
4. WAIT for Braydon to provide smaller tasks
```

## Red Flags - NEVER Do These

**NEVER:**
- ❌ Report success without running `tmux capture-pane`
- ❌ Skip quality gates before committing
- ❌ Delegate without verifying pane status
- ❌ Make up pane numbers or session names
- ❌ Check panes "in background" (must be synchronous)
- ❌ Wait more than 110 seconds (respect 120s timeout)
- ❌ Implement code yourself (hooks block this)
- ❌ Forget to send Enter key after typing commands

**If you catch yourself:**
- About to report "success" → RUN `tmux capture-pane` first, READ OUTPUT
- About to commit → RUN quality gates first, READ OUTPUT
- About to delegate → RUN `tmux capture-pane` on target, READ OUTPUT
- Unsure about pane state → RUN `tmux list-panes`, READ OUTPUT
- Command not executing → Did you send `Enter` as a separate argument?

## State Files Reference

All state lives in `/tmp` with simple text format:

- `/tmp/tmux-coord-$SESSION.txt` - Current session state
- `/tmp/tmux-tasks-$SESSION.txt` - Task log (append-only)
- `/tmp/pane-N-monitor.txt` - Individual pane monitoring state
- `/tmp/stuck-pane-N-*.log` - Captured output from failed panes

## Summary

You are a **self-discovering coordinator** that:
1. Learns context from tmux commands (no pre-config)
2. Delegates tasks to clauded/codex CLI agents in panes
3. Monitors synchronously with 90s waits
4. Auto-approves via quality gates
5. Splits additional worker panes on-demand (within the window)
6. Cannot hallucinate (every action requires running bash, reading output)
7. ALWAYS sends Enter key as separate argument in send-keys commands

**Remember:** Every state check MUST run a tmux command and read actual output. You have no memory - only what bash returns.
