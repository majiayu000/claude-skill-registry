---
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, LSP, mcp__ide__getDiagnostics, Bash
description: Execute the user's plan that has been iteratively refined
disable-model-invocation: true
---

You are executing the user's plan that has been iteratively refined.

To do this, follow these steps precisely:

1. Read `.claude/plan-critique-config.json` and get `plansFolder` path from settings.
   If the file doesn't exist or `plansFolder` is not set:
   Respond with "No plans folder configured. Run `/plan:create` first to set up."
2. Get the Claude Code process ID by running: `echo $PPID`. Store this as `sessionPID`.
3. Clean up stale sessions: Scan `[plansFolder]/.sessions/` for files. For each file named with a PID, check if that
   process is still running via `kill -0 [PID] 2>/dev/null`. If the command fails (process not running), delete that
   session file. This is non-blocking cleanup.
4. Read the current session's plan from `[plansFolder]/.sessions/[sessionPID]` if it exists. Store as `sessionPlan`.
5. Scan `[plansFolder]/` for subdirectories (each subdirectory is a plan).
   Exclude `archived/` and `.sessions/` folders and any files, only list plan directories.
   If no plan folders exist: Respond with "No plans found. Create one with `/plan:create`".
6. Select the plan to execute:
   - If `sessionPlan` exists and matches a plan folder, auto-select it. Inform the user:
     "Using current session plan: [sessionPlan]"
   - Else if only one plan exists, auto-select it and inform user.
   - Otherwise, ask the user to select a plan from the list.
     Example:
     ```
     Available plans:
     1. add-user-authentication
     2. refactor-database-layer
     3. implement-caching

     Which plan would you like to execute? [1-3]
     ```
7. Update the session file `[plansFolder]/.sessions/[sessionPID]` with the selected plan slug (create if needed).
8. Check prerequisites:
   - If `[plansFolder]/[selected-plan]/plan.md` does not exist: Respond with "No plan.md found."
   - If `plan.md` is empty: Respond with "Plan file is empty. Run /plan:critique first."
9. Read `CLAUDE.md` from the project root if it exists. Hold its standards as context and ensure compliance during
   each execution step. If it does not exist, note this but do not block execution.
10. Read `[plansFolder]/[selected-plan]/critique.md` if it exists. Note the iteration number and summary.
    Inform the user: "Plan was critiqued (iteration N). Last critique summary: [brief]."
    Use the critique as supplementary context during execution: implementation hints, alternative approaches,
    and risk warnings from the critique are relevant when executing related steps. Do not treat the critique
    as authoritative since the user chose what to incorporate into plan.md.
    If critique.md does not exist, warn: "This plan has not been critiqued. Run `/plan:critique` first,
    or confirm you want to proceed without review." Wait for user confirmation before continuing.
11. Check git status by running `git status`.
    - If git repo and clean: inform user "Git available. Per-step commits will be offered after each step."
    - If git repo and dirty: warn "Uncommitted changes detected. Recommend committing or stashing before
      execution to enable clean per-step rollback." Wait for user acknowledgement.
    - If not a git repo: inform "Not a git repository. Per-step commits are not available."
    Store whether git is available for later use.
12. Check for existing execution state. If `[plansFolder]/[selected-plan]/execution-state.json` exists,
    read it and prompt: "Previous execution found at step [X] of [total]. Resume or restart?"
    Wait for user response before proceeding.
    - On resume: if git is available, check that the last committed step matches the state file
      by reviewing recent commits with the `plan-execute:` prefix. If they do not match, warn the user
      that the codebase may have diverged from the recorded state. Skip already-completed steps.
    - On restart: overwrite execution-log.md with a new header. Note the restart in the log:
      "Restarted execution (previous attempt reached step [X])."
13. Review supporting files in the `[plansFolder]/[selected-plan]/` folder. Classify each file by type
    and inferred purpose. Present to the user alongside the step list:
    "Supporting files found: schema.sql (SQL migration), mockup.png (UI reference)."
    Let the user confirm or clarify how each file should be used during execution.
14. Parse the plan into discrete, executable steps using this ordering strategy:
    - Independent tasks first: changes with no dependencies on other changes
    - Small to large: within independent tasks, order from smallest to largest scope
    - Dependent tasks after: once all independent tasks are ordered, add tasks that depend on them
    - Same-level tiebreaker: for tasks at the same dependency level, order by logical grouping

    Example: If a plan has "Add utility function", "Create database migration", and "Update API endpoint
    (uses utility)", order as: 1) Add utility function, 2) Create database migration, 3) Update API endpoint
15. Use Glob and Grep to estimate which existing files each step is likely to affect.
    Present the steps to the user for confirmation, including the dependency graph and file estimates:
    ```
    I've parsed your plan into the following steps:
    1. [Step description] - likely affects: src/auth.ts, src/middleware.ts
       (no dependencies)
    2. [Step description] - creates new file: src/utils/hash.ts
       (no dependencies)
    3. [Step description] - likely affects: src/routes.ts
       (depends on step 1)
    ...

    Do you want me to proceed with execution? You can reorder or adjust steps before starting.
    ```
    Wait for the user to confirm or request changes to the ordering.
16. Execute each step sequentially:
    - Record the step start time.
    - Before each step, update execution-state.json with current progress including `stepStartedAt`
      (see [execution-state-format.md](execution-state-format.md)).
    - Ask for explicit user permission before high-risk operations:
      - Database migrations or schema changes
      - Deleting files or directories
      - Modifying configuration files
      - External API calls with side effects
      - Any irreversible operations
    - Execute the step, ensuring compliance with CLAUDE.md standards loaded in step 9.
      Reference critique.md findings when they are relevant to the current step.
    - After the step completes, run verification:
      - Use `mcp__ide__getDiagnostics` on files modified in this step. Report only NEW errors
        or warnings (compare before and after to avoid flagging pre-existing issues).
      - If new errors are found, inform the user and ask: "Fix now, continue, or stop?"
    - Show a diff summary: list files added, modified, or deleted in this step.
    - If git is available (step 11), offer to commit:
      - On the first step, ask: "Commit this step? (yes / no / yes-to-all)"
      - If the user chose "yes-to-all", commit subsequent steps automatically without asking.
      - Commit message format: `plan-execute: [plan-slug] step N - [brief description]`
      - Record the commit hash in execution-state.json under `gitCommits`.
    - Compute step duration and log results to execution-log.md including duration and files changed
      (see [execution-log-format.md](execution-log-format.md)).
    - If a step introduces architectural patterns that should be documented in `CLAUDE.md`,
      flag this to the user immediately rather than waiting until completion.
    - On error:
      - Save execution state with the failed step.
      - Diagnose the error: read the error output, identify the likely root cause.
      - Include the actual error output verbatim in the execution log (not just a summary).
      - Present recovery options to the user:
        1. Fix and retry - attempt to fix the issue, then re-execute this step.
        2. Skip step - mark as SKIPPED, warn about downstream dependencies, continue.
        3. Rollback step - if git commits are available, revert the last commit. Then stop.
        4. Stop execution - save state, stop. Resume later with `/plan:execute`.
      - Wait for user choice.
17. On successful completion:
    - Update execution log with final summary.
    - Delete execution-state.json.
    - If git was used, mention the commit count: "Plan executed across N commits.
      Review with `git log --oneline -N`."
    - Inform user: "Plan executed successfully. Run `/plan:archive` to archive this plan."

Notes:

- Never continue past a failed step automatically. Always present recovery options and wait.
- Keep the execution log updated in real-time.
- Be explicit about what changes are being made at each step.
- Reference any supporting files in the plan folder as needed during execution.
- critique.md is read as supplementary context, not as an authoritative override of plan.md.
- Git commits enable rollback of individual steps via `git revert`. This is the primary safety net.
- Verification checks (LSP diagnostics) are advisory. They surface issues early but do not block
  execution unless the user chooses to stop.
- Plans exceeding 10 steps should be flagged to the user with a recommendation to split into
  smaller plans to avoid context window exhaustion during execution.
- CLAUDE.md standards are applied during execution. If any step introduces patterns that should be
  documented in CLAUDE.md, flag this to the user immediately.
- Execution state is best-effort. If Claude crashes mid-step, the state file may not reflect the
  actual codebase state. Git commits provide the definitive record of what was completed.
