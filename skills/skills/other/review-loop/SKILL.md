---
name: review-loop
description: Use when code changes need multi-pass automated review before merge. Use when preparing branch for PR. Use when thorough code quality check needed.
---

# MANDATORY FIRST ACTION

**STOP. Before ANY other tool call, you MUST call TaskCreate.**

If you're about to:
- Run setup.sh → STOP. TaskCreate first.
- Dispatch reviewer → STOP. TaskCreate first.
- Read any file → STOP. TaskCreate first.

## Step 1: Create Tasks

First, check if `code-simplifier:code-simplifier` subagent is available in your Task tool's subagent_type list.

**If code-simplifier IS available:**
```
TaskCreate(subject: "Simplify code", description: "Run code-simplifier before review", activeForm: "Simplifying code")
TaskCreate(subject: "Iteration 1: Review", description: "Review and fix", activeForm: "Running iteration 1", metadata: {"iteration": 1, "of": 3})
TaskCreate(subject: "Iteration 2: Review", description: "Review and fix", activeForm: "Running iteration 2", metadata: {"iteration": 2, "of": 3})
TaskCreate(subject: "Iteration 3: Review", description: "Review and fix", activeForm: "Running iteration 3", metadata: {"iteration": 3, "of": 3})
```

Then set dependencies (ITER1 blocked by SIMPLIFY):
```
TaskUpdate(taskId: ITER1, addBlockedBy: [SIMPLIFY])
TaskUpdate(taskId: ITER2, addBlockedBy: [ITER1])
TaskUpdate(taskId: ITER3, addBlockedBy: [ITER2])
TaskUpdate(taskId: SIMPLIFY, status: "in_progress")
```

**If code-simplifier is NOT available:**
```
TaskCreate(subject: "Iteration 1: Review", description: "Review and fix", activeForm: "Running iteration 1", metadata: {"iteration": 1, "of": 3})
TaskCreate(subject: "Iteration 2: Review", description: "Review and fix", activeForm: "Running iteration 2", metadata: {"iteration": 2, "of": 3})
TaskCreate(subject: "Iteration 3: Review", description: "Review and fix", activeForm: "Running iteration 3", metadata: {"iteration": 3, "of": 3})
```

Then set dependencies and start:
```
TaskUpdate(taskId: ITER2, addBlockedBy: [ITER1])
TaskUpdate(taskId: ITER3, addBlockedBy: [ITER2])
TaskUpdate(taskId: ITER1, status: "in_progress")
```

**Report to user:** "code-simplifier plugin not installed. Recommended: `claude plugin install code-simplifier@anthropic-official` from https://github.com/anthropics/claude-plugins-official"

**CHECKPOINT: Have you created tasks? If NO → do it now. If YES → continue.**

---

# Review Loop

You are an ORCHESTRATOR. You dispatch subagents. You do NOT touch code.

## Process

```dot
digraph review_loop {
    rankdir=TB;
    "TaskCreate" [shape=box, style=bold];
    "Get REVIEW_DIR/TARGET_BRANCH" [shape=box];
    "code-simplifier available?" [shape=diamond];
    "Dispatch code-simplifier" [shape=box];
    "TaskList → find unblocked" [shape=box];
    "TaskGet → read iteration metadata" [shape=box];
    "Dispatch reviewer" [shape=box];
    "Read findings + triage" [shape=box];
    "Dispatch fix subagent per issue" [shape=box];
    "CHECKPOINT" [shape=doubleoctagon, style=bold, color=red];
    "TaskUpdate completed" [shape=box];
    "iteration < of?" [shape=diamond];
    "Commit" [shape=box];

    "TaskCreate" -> "Get REVIEW_DIR/TARGET_BRANCH";
    "Get REVIEW_DIR/TARGET_BRANCH" -> "code-simplifier available?";
    "code-simplifier available?" -> "Dispatch code-simplifier" [label="yes"];
    "code-simplifier available?" -> "TaskList → find unblocked" [label="no"];
    "Dispatch code-simplifier" -> "TaskList → find unblocked";
    "TaskList → find unblocked" -> "TaskGet → read iteration metadata";
    "TaskGet → read iteration metadata" -> "Dispatch reviewer";
    "Dispatch reviewer" -> "Read findings + triage";
    "Read findings + triage" -> "Dispatch fix subagent per issue";
    "Dispatch fix subagent per issue" -> "CHECKPOINT";
    "CHECKPOINT" -> "TaskUpdate completed";
    "TaskUpdate completed" -> "iteration < of?";
    "iteration < of?" -> "TaskList → find unblocked" [label="yes, continue"];
    "iteration < of?" -> "Commit" [label="no, done"];
}
```

## Step 2: Get Config

Capture three values — user args override setup.sh defaults:

| Variable | Source | Description |
|----------|--------|-------------|
| `REPO_PATH` | args or `pwd` | Repository root to operate in |
| `TARGET_BRANCH` | args or PR/git detection | Branch to diff against |
| `REVIEW_DIR` | setup.sh | Temp directory for review files |

If args provided (e.g., `/review-loop path=/some/repo target=main`), use them. Otherwise run:
```
~/.claude/plugins/cache/onsails-cc/review-loop/*/skills/review-loop/scripts/setup.sh
```

**All subagents MUST receive REPO_PATH.** Subagents inherit the session's original cwd, not the current shell cwd.

## Step 2.5: Code Simplification (if available)

If `code-simplifier:code-simplifier` subagent is available, dispatch it to simplify code changes between current branch and TARGET_BRANCH:
```
Task(subagent_type: "code-simplifier:code-simplifier",
     prompt: "REPO_PATH: ${REPO_PATH}
TARGET_BRANCH: ${TARGET_BRANCH}

cd to REPO_PATH first. Simplify code changes between HEAD and TARGET_BRANCH.
Focus only on files modified in this branch.")
TaskUpdate(taskId: SIMPLIFY, status: "completed")
```

## Step 3: Each Iteration

1. `TaskList` → find first unblocked iteration task
2. `TaskGet(taskId: CURRENT)` → read metadata.iteration and metadata.of
3. `TaskUpdate(taskId: CURRENT, status: "in_progress")`
4. Dispatch reviewer:
   ```
   Task(subagent_type: "review-loop:local-reviewer",
        prompt: "REPO_PATH: ${REPO_PATH}
OUTPUT: ${REVIEW_DIR}/iterN.md
TARGET_BRANCH: ${TARGET_BRANCH}

cd to REPO_PATH first.")
   ```
   **Reviewer returns a summary.** Display it to user.
5. **Read findings and triage (YOU do this, not a subagent):**
   ```
   Read(file_path: "${REVIEW_DIR}/iterN.md")
   ```
   Parse the `## Findings` section. For each issue under Critical/Major:
   - Create a fix task: `TaskCreate(subject: "Fix: [title]", description: "...", activeForm: "Fixing [title]")`
   - Block next iteration: `TaskUpdate(taskId: NEXT_ITER, addBlockedBy: [fix_task_ids])`

   Display triage table:
   ```
   | # | Severity | File:Line | Issue | Action |
   |---|----------|-----------|-------|--------|
   | 1 | critical | foo.rs:42 | SQL injection | FIX |
   | 2 | major    | bar.rs:15 | Race condition | FIX |
   | 3 | minor    | baz.rs:99 | Unused import | SKIP |
   ```

   **Skip rules:** Skip minor/suggestion severity. Skip issues that are clearly false positives.

6. **Dispatch ONE fix subagent per issue (YOU dispatch these directly):**

   For each fix task, sequentially:
   ```
   TaskUpdate(taskId: FIX_TASK, status: "in_progress")
   Task(subagent_type: "general-purpose",
        description: "Fix: [issue title]",
        prompt: "REPO_PATH: ${REPO_PATH}

cd to REPO_PATH first.

Fix this specific issue:
   File: [file]:[line]
   Issue: [description]
   Severity: [severity]

Make minimal changes to fix ONLY this issue.
Do not fix other issues. Do not refactor surrounding code.
Run relevant tests after fixing if test infrastructure exists.")
   TaskUpdate(taskId: FIX_TASK, status: "completed")
   ```

   **Each Task call = ONE fix. Never batch multiple fixes into one prompt.**
   **Wait for each subagent to complete before dispatching next.**

7. `TaskUpdate(taskId: CURRENT, status: "completed")`

### CHECKPOINT (after all fixes dispatched)

**STOP HERE. All fix subagents have completed. You MUST now check iteration progress:**

```
Current iteration: ${metadata.iteration}
Total iterations: ${metadata.of}

Is ${metadata.iteration} < ${metadata.of}?
  YES → Go to Step 3.1 (TaskList → find next unblocked)
  NO  → Go to Step 4 (Completion)
```

**DO NOT STOP after fixes complete.** Fixing is a sub-step, not the end of the loop.

**WHY 3 iterations are mandatory:**
- Reviewers find different issues on different passes
- Fixes may introduce new problems
- Context builds across iterations
- First pass often misses subtle issues

**NEVER stop early because:**
- "No issues found" → Reviewer may find different issues next pass
- "All false-positives" → Next iteration reviews with fresh perspective
- "Code looks clean" → Run all iterations anyway

## Step 4: Completion

After 3 iterations with no critical/major:

1. **Mark final iteration task completed:**
   ```
   TaskUpdate(taskId: ITER3, status: "completed")
   ```

2. **Verify all tasks completed:**
   ```
   TaskList  → All iteration tasks should show "completed"
   ```

3. **Commit changes:**
   ```bash
   git add -A && git commit -m "fix: address review issues (N iterations)"
   ```

**Do NOT leave tasks in pending/in_progress state.**

---

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "I know what review-loop does" | You pattern-matched. Read the skill. TaskCreate FIRST. |
| "Let me run setup first" | NO. TaskCreate comes before setup.sh |
| "I'll create tasks after starting" | NO. Tasks FIRST, always. |
| "Two iterations enough" | NO. Minimum 3. |
| "I'll fix this quickly" | NO. Dispatch a fix subagent per issue. |
| "I'll batch all fixes in one subagent" | NO. One Task per fix. Never batch. |
| "I'll dispatch fix coordinator" | NO. YOU triage and dispatch fix subagents directly. |
| "Would you like me to..." | NO. Never ask. Execute. |
| "Skip code-simplifier, it's optional" | Check availability first. If available, run it. |
| "No issues found, stopping early" | NO. Reviewers find different issues each pass. Run all 3. |
| "All were false-positives, done" | NO. Next iteration may find real issues. Continue. |
| "Code is clean after iteration 1" | NO. Run all 3 iterations. First pass misses subtle issues. |
| "Fixes done, I'm done" | NO. Fixing is a sub-step. Go to CHECKPOINT, check iteration count. |

## Red Flags - STOP IMMEDIATELY

If you catch yourself:
- Dispatching reviewer without tasks created → STOP
- Running setup.sh as first action → STOP
- Using Read/Edit/Grep on code → STOP
- Fixing issues directly (Edit/Write on code) → STOP
- Batching multiple fixes into one subagent → STOP
- Asking permission → STOP
- Skipping code-simplifier without checking availability → STOP
- Stopping before iteration 3 because "no issues" → STOP
- Skipping iterations because "all false-positives" → STOP
- **Ending response after fixes complete** → STOP (go to CHECKPOINT)
- **Not checking metadata.iteration after fixes** → STOP (read the task, check the count)

**All mean: You violated the skill. Go back and follow it exactly.**

## Iron Rules

1. TaskCreate BEFORE anything else
2. Check code-simplifier availability, run if present
3. MINIMUM 3 review iterations
4. ONLY Task tool on code (dispatch subagents)
5. SEQUENTIAL iterations
6. ONE fix subagent per issue — never batch
7. YOU read findings and triage — no intermediary agent
8. Never ask permission
