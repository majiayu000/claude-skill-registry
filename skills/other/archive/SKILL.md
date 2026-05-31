---
allowed-tools: Read, Write, Edit, Glob, AskUserQuestion, Bash(mkdir:*), Bash(cp:*), Bash(mv:*), Bash(rm:*), Bash(echo $PPID), Bash(kill -0:*), Bash(ls:*)
description: Archive a completed or abandoned plan for future reference
disable-model-invocation: true
---

You are archiving the user's completed (or abandoned) plan for future reference.

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
   If no plan folders exist: Respond with "No plans found. Nothing to archive."
6. Select the plan to archive:
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

     Which plan would you like to archive? [1-3]
     ```
7. Check prerequisites. If `[plansFolder]/[selected-plan]/plan.md` does not exist or is empty:
   Respond with "Nothing to archive. Plan file is missing or empty."
8. Ensure `[plansFolder]/archived/` exists, create it if not.
9. Extract metadata:
   - Read `plan.md` to get the plan title (first H1 heading). If no title, use folder name.
   - Read `critique.md` to get keywords (if available)
   - Read `execution-log.md` to get execution status (if available)
10. Generate archive folder name using format: `YYYY-MM-DD_HH-MM-SS_[slug]/`
    Example: `2026-01-12_14-30-00_add-user-authentication/`
11. Create the archive folder at `[plansFolder]/archived/[folder-name]/`
12. Copy contents from `[plansFolder]/[selected-plan]/` to the archive:
    - Include: `plan.md`, `execution-log.md` (if exists), all other files (SQL, images, etc.)
    - Exclude: `critique.md`, `execution-state.json`
13. Create `archive-info.md` in the archive folder using the format in
    [archive-info-format.md](archive-info-format.md).
14. Delete the original plan folder `[plansFolder]/[selected-plan]/` entirely.
15. Clean up session references to the archived plan:
    - Delete `[plansFolder]/.sessions/[sessionPID]` if it contains the archived plan slug.
    - Scan all other session files and delete any that reference the archived plan (handles stale references).
16. Respond with confirmation:
    ```
    Plan archived to: [plansFolder]/archived/[folder-name]/

    The original plan folder has been removed.
    Create a new plan with `/plan:create`.
    ```

Notes:

- Never include critique.md in the archive (only keywords are preserved in archive-info.md)
- Always include the full original plan and all supporting files
- Include execution log only if the plan was executed
- Use current timestamp for the archive folder name
- Preserve the original file structure within the archived folder
- Always delete the original plan folder after archiving
- It is valid to archive a plan that was never executed (abandoned, reference, or superseded plans).
  In this case, the execution status will be `NOT_EXECUTED`.
