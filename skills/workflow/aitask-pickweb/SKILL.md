---
name: aitask-pickweb
description: Pick and implement a task on Claude Code Web. Zero interactive prompts. No cross-branch operations — stores task data locally in .aitask-data-updated/.
---

## Overview

This skill is a sandboxed version of `aitask-pickrem` designed specifically for **Claude Code Web**, where the environment has no push access to `aitask-locks`, `aitask-data`, or `main` branches. It combines task selection and implementation into a single self-contained workflow with **zero interactive prompts** and **zero cross-branch operations**.

All task metadata (plans, completion markers) is stored in `.aitask-data-updated/` on the current working branch. A separate local skill (`aitask-web-merge`) handles merging code to main and archiving task data after the Claude Web session completes.

**Key differences from `aitask-pickrem`:**
- NO lock acquisition (`aitask_pick_own.sh`) — read-only lock check only
- NO status updates (`aitask_update.sh`) — task status stays as-is
- NO archival (`aitask_archive.sh`) — completion marker written instead
- NO `./ait git` — uses regular `git` for commits
- Plan stored in `.aitask-data-updated/` instead of `aiplans/`
- Completion marker JSON signals to `aitask-web-merge` that the branch is ready

## Arguments

**Required:** Task ID (first positional argument)
- Format 1: Parent task number (e.g., `42`)
- Format 2: Child task ID (e.g., `42_2`)

**IMPORTANT:** This skill will NOT work without a task ID argument. If invoked without one, display an error and abort.

## Workflow

### Step 0: Initialize Data Branch (if needed)

Ensure the aitask-data worktree and symlinks are set up:

```bash
./.aitask-scripts/aitask_init_data.sh
```

This is a no-op for legacy repos and already-initialized repos. Required for
Claude Code Web where `ait setup` has not been run.

Parse stdout:
- `INITIALIZED` — Display: "Data branch initialized." Proceed.
- `ALREADY_INIT` / `LEGACY_MODE` / `NO_DATA_BRANCH` — Proceed silently.

If the command fails (non-zero exit), display the error and abort.

### Step 1: Load Execution Profile

Execute the **Execution Profile Selection Procedure — Auto-Select** (see `.claude/skills/task-workflow/execution-profile-selection-auto.md`) with `mode_label` = `"Web"`.

### Step 2: Resolve Task File

Parse the task ID argument:

**Format 1: Parent task (e.g., `42`):**
- Find the matching task file and check for children in a single call:
  ```bash
  ./.aitask-scripts/aitask_query_files.sh resolve <number>
  ```
  Parse the output: if first line is `NOT_FOUND`, display error "Task t\<N\> not found" and abort. If first line is `TASK_FILE:<path>`, use that path. If second line is `HAS_CHILDREN:<count>`, display error "Task t\<N\> has child subtasks. Specify a child task ID (e.g., `\<N\>_1`) instead." Abort. If `NO_CHILDREN`, proceed with this task.

**Format 2: Child task (e.g., `42_2`):**
- Parse as child task ID (parent=42, child=2)
- Find the matching child task file:
  ```bash
  ./.aitask-scripts/aitask_query_files.sh child-file <parent> <child>
  ```
  Parse the output: `CHILD_FILE:<path>` means found (use that path), `NOT_FOUND` means not found.
- If not found: display error "Child task t\<parent\>_\<child\> not found" and abort.
- Set this as the selected task
- Read the task file and parent task file for context
- **Gather sibling context** in a single call:
  ```bash
  ./.aitask-scripts/aitask_query_files.sh sibling-context <parent>
  ```
  Parse the output: lines prefixed `ARCHIVED_PLAN:` are archived sibling plan files (primary context source for completed siblings). Lines prefixed `ARCHIVED_TASK:` are fallback for siblings without archived plans. Lines prefixed `PENDING_SIBLING:` are pending sibling task files. Lines prefixed `PENDING_PLAN:` are pending sibling plans. If output is `NO_CONTEXT`, there are no sibling context files. Read the files listed in the output.

Display: "Selected task: \<task_filename\>" with a brief 1-2 sentence summary.

Set context variables:
- **task_file**: Path to the selected task file
- **task_id**: Task identifier (e.g., `42` or `42_2`)
- **task_name**: Filename stem (e.g., `t42_implement_auth` or `t42_2_add_login`)
- **is_child**: `true` if child task, `false` otherwise
- **parent_id**: Parent task number if child, null otherwise
- **parent_task_file**: Path to parent task file if child, null otherwise
- **previous_status**: The task's current status (before modification)

### Step 3: Read-Only Lock Check (Informational)

Run a read-only lock check to inform the user if someone else is working on this task. This does NOT acquire a lock.

```bash
./.aitask-scripts/aitask_lock.sh --check <task_num>
```

**Parse the output:**
- **Exit code 0 (locked):** The task is locked. Parse the YAML output for `locked_by`, `locked_at`, `hostname`. Display warning: "Warning: Task t\<N\> is locked by \<locked_by\> (since \<locked_at\>, hostname: \<hostname\>). Proceeding anyway (read-only check)."
- **Exit code 1 (not locked):** Display: "Lock check: task is not locked." Proceed.
- **Command fails (network error, no lock branch):** Display: "Lock check: unavailable (no lock infrastructure or network issue). Proceeding." Continue silently.

**Always proceed** regardless of lock status — this is purely informational.

### Step 4: Task Status Checks

**Check 1 — Done but unarchived task:**
- Read the task file's frontmatter `status` field
- If status is `Done`:
  - Display: "Task t\<N\> has status 'Done'. Cannot implement on Claude Web — use `aitask-web-merge` locally to archive." Abort.

**Check 2 — Orphaned parent task:**
- Check if the task file's frontmatter contains `children_to_implement: []` (empty list)
- If empty, check for archived children:
  ```bash
  ./.aitask-scripts/aitask_query_files.sh archived-children <number>
  ```
  Parse the output: `ARCHIVED_CHILD:<path>` lines mean archived children exist, `NO_ARCHIVED_CHILDREN` means none.
- If archived children exist:
  - Display: "Orphaned parent t\<N\> (all children done). Use `aitask-web-merge` locally to archive." Abort.

If neither check triggers, proceed to Step 5.

### Step 5: Create Implementation Plan

#### 5.0: Check for Existing Plan

Check if a plan file already exists at either location:
- Standard location: `aiplans/p<taskid>_*.md` or `aiplans/p<parent>/p<parent>_<child>_*.md`
- Web location: `.aitask-data-updated/plan_t<task_id>.md`

```bash
./.aitask-scripts/aitask_query_files.sh plan-file <taskid>
ls .aitask-data-updated/plan_t<task_id>.md 2>/dev/null
```
Parse the first command's output: `PLAN_FILE:<path>` means found, `NOT_FOUND` means not found.

**If a plan file exists** (check standard location first, then web location), read it.

- Read `plan_preference` from profile (default: `use_current`):
  - `use_current`: Display "Profile: using existing plan". Copy plan to `.aitask-data-updated/plan_t<task_id>.md` if not already there. Skip to **Step 5 Checkpoint**.
  - `verify`: Display "Profile: verifying existing plan". Enter plan mode (Step 5.1), starting by reading and verifying the existing plan.
  - `create_new`: Display "Profile: creating plan from scratch". Enter plan mode (Step 5.1).

**If no plan file exists**, proceed to Step 5.1.

#### 5.1: Planning

Use the `EnterPlanMode` tool to enter Claude Code's plan mode.

**If entering from the "verify" path:** Start by reading the existing plan file. Explore the current codebase to check if the plan's assumptions, file paths, and approach are still valid. Update the plan if needed.

**For child tasks:** Include context links (in priority order):
- Parent task file: `aitasks/t<parent>_<name>.md`
- Archived sibling plan files: `aiplans/archived/p<parent>/p<parent>_*_*.md`
- Archived sibling task files (fallback): `aitasks/archived/t<parent>/t<parent>_*_*.md`
- Pending sibling task files: `aitasks/t<parent>/t<parent>_*_*.md`
- Pending sibling plan files: `aiplans/p<parent>/p<parent>_*_*.md`

While in plan mode:

- Explore the codebase to understand the relevant architecture
- **Folded Tasks Note:** If the task has a `folded_tasks` frontmatter field, the task description already contains all relevant content from the folded tasks. No need to read the original folded task files.
- **Complexity:** Always implement as a single task (do NOT break into child subtasks — child creation requires interactive prompts not available in web mode)
- **Testing requirement:** When the task involves code changes (not documentation/config-only tasks), the implementation plan MUST include a "Verification" section specifying:
  - What automated tests to write or update
  - What existing tests to run
  - Expected outcomes
  - For non-code tasks (documentation, config, skill files), a simple verification step (e.g., lint check, visual review of output) is sufficient
- Create a detailed implementation plan
- Include a reference to **Step 8 (Completion Marker)** for post-implementation steps
- Use `ExitPlanMode` when ready for user approval

#### Save Plan to `.aitask-data-updated/`

After the user approves the plan via `ExitPlanMode`, save it to the local data directory.

```bash
mkdir -p .aitask-data-updated
```

**File naming:** `.aitask-data-updated/plan_t<task_id>.md`

Examples:
- Parent task 42: `.aitask-data-updated/plan_t42.md`
- Child task 42_2: `.aitask-data-updated/plan_t42_2.md`

**Required metadata header:**
```markdown
---
Task: <task_filename>
Parent Task: <parent_task_path> (if child, omit if parent)
Branch: <current branch name>
---
```

#### Step 5 Checkpoint

Read `post_plan_action` from profile (default: `start_implementation`).

- `start_implementation`: Display "Profile: proceeding to implementation". Proceed to Step 6.
- If not set: proceed to Step 6 (default behavior for web mode is always to continue).

### Step 6: Implement

**Note:** aitask-pickweb intentionally skips ownership/locking — all lock acquisition, status updates, and archival are deferred to `aitask-web-merge`, which runs locally after the Claude Web session completes. No pre-implementation ownership guard is needed here.

**Record implementing agent:** Execute the **Agent Attribution Procedure** (see `../task-workflow/agent-attribution.md`) to detect which code agent and model is implementing this task. Since pickweb does not call `aitask_update.sh`, store the agent string in memory for inclusion in the completion marker JSON (Step 8).

Follow the approved plan, working in the current directory.

Update the plan file in `.aitask-data-updated/` as you progress:
- Mark steps as completed
- Note any deviations or changes from the original plan
- Record issues encountered during implementation

**Testing (when applicable):**
- After implementation is complete, run all relevant automated tests if the task involves code changes
- If tests fail, attempt to fix the issues before proceeding to Step 7
- If tests cannot be fixed after reasonable attempts, trigger the **Abort Procedure** instead of committing broken code
- If no tests are applicable (documentation, config, skill file tasks), proceed directly to build verification

**Build verification (if configured):**
- Read `aitasks/metadata/project_config.yaml` and check the `verify_build` field
- **If `verify_build` is absent, null, or empty (or file doesn't exist):** Display "No verify_build configured — skipping build verification." and skip.
- **If configured:** Run the command(s). If a single string, run it. If a list, run sequentially (stop on first failure).
- **If the build fails:**
  1. Analyze the error output and compare against the changes introduced by this task
  2. **If caused by this task's changes:** Go back to fix the build errors. After fixing, re-run. Repeat until the build passes.
  3. **If NOT related to this task's changes** (pre-existing issue): Log the build failure in the plan file's "Final Implementation Notes" and proceed. Do not attempt to fix pre-existing issues.

### Step 7: Auto-Commit

1. **Show change summary:**
   ```bash
   git status
   git diff --stat
   ```

2. **Check for changes:**
   ```bash
   git status --porcelain
   ```
   If no changes detected, display warning "No changes detected after implementation" and skip to Step 8.

3. **Consolidate the plan file:**
   - Read the plan file from `.aitask-data-updated/`
   - Review `git diff --stat` against the plan
   - Add or update a "Final Implementation Notes" section:
     ```markdown
     ## Final Implementation Notes
     - **Actual work done:** <summary of what was actually implemented vs planned>
     - **Deviations from plan:** <any changes from the original approach and why>
     - **Issues encountered:** <problems found and how they were resolved>
     - **Key decisions:** <technical decisions made during implementation>
     - **Test results:** <summary of automated tests run and their outcomes>
     - **Notes for sibling tasks:** <patterns, gotchas, shared code> (include if child task)
     ```
   - **IMPORTANT for child tasks:** The plan file will be used by `aitask-web-merge` during archival and serve as reference for subsequent sibling tasks.

4. **Stage and commit:**
   - Stage all implementation changes including `.aitask-data-updated/` files
   - Use regular `git` (NOT `./ait git`):
     ```bash
     git add -A
     # First execute the Contributor Attribution Procedure and the
     # Code-Agent Commit Attribution Procedure from ../task-workflow/code-agent-commit-attribution.md,
     # then compose one final commit message.
     git commit -m "$(cat <<'EOF'
     <issue_type>: <description> (t<task_id>)

     <optional Based on PR block and contributor trailer>
     <optional code-agent trailer>
     EOF
     )"
     ```
   - **Commit message format:** `<issue_type>: <description> (t<task_id>)` where `<issue_type>` is from the task's frontmatter
   - If code-agent attribution fails, continue with the contributor-only or plain commit message
   - Display: "Changes committed: \<commit_hash\>"

5. Proceed to Step 8.

### Step 8: Write Completion Marker

Write a completion marker file so `aitask-web-merge` can detect this branch as a completed Claude Web execution.

```bash
mkdir -p .aitask-data-updated
```

**File:** `.aitask-data-updated/completed_t<task_id>.json`

**Contents:**
```json
{
  "task_id": "<task_id>",
  "task_file": "<task_file path>",
  "plan_file": ".aitask-data-updated/plan_t<task_id>.md",
  "is_child": <true|false>,
  "parent_id": <"parent_num"|null>,
  "issue_type": "<issue_type from frontmatter>",
  "implemented_with": "<agent_string from Step 6>",
  "completed_at": "<YYYY-MM-DD HH:MM>",
  "branch": "<current branch name>"
}
```

Stage and commit the marker:
```bash
git add .aitask-data-updated/completed_t<task_id>.json
git commit -m "ait: Add completion marker for t<task_id>"
```

Display: "Task t\<task_id\> implementation complete on branch \<branch\>. Run `aitask-web-merge` locally to merge and archive."

### Abort Procedure

Triggered by errors during implementation. Since no cross-branch operations were performed, abort is simple:

1. Display the error message.
2. If `.aitask-data-updated/` files were created, optionally clean them up:
   ```bash
   rm -rf .aitask-data-updated/ 2>/dev/null || true
   ```
3. Display: "Task t\<N\> aborted. No cross-branch state was modified."

No status revert, no lock release, no `./ait git` operations needed.

---

## Profile Schema

This skill uses the same profile format as `aitask-pickrem` from `aitasks/metadata/profiles/`. Only a subset of fields are recognized:

| Key | Type | Default | Values | Purpose |
|-----|------|---------|--------|---------|
| `name` | string | (required) | Display name | Shown during profile load |
| `description` | string | (required) | Description text | Shown during profile load |
| `plan_preference` | string | `use_current` | `"use_current"`, `"verify"`, `"create_new"` | Step 5.0 existing plan handling |
| `post_plan_action` | string | `start_implementation` | `"start_implementation"` | Step 5 checkpoint |

**Fields from pickrem that are IGNORED** (not applicable in web mode):
- `default_email`, `force_unlock_stale` — no lock/ownership operations
- `done_task_action`, `orphan_parent_action` — Done/orphaned tasks abort instead of archive
- `review_action`, `issue_action` — no archive or issue operations
- `abort_plan_action`, `abort_revert_status` — no status to revert
- `create_worktree`, `base_branch`, `enableFeedbackQuestions` — always works on current branch and never asks feedback questions

---

## Notes

- This skill has **zero `AskUserQuestion` calls** — designed for Claude Code Web
- `EnterPlanMode`/`ExitPlanMode` are still used for plan creation (they are NOT `AskUserQuestion`)
- NO calls to: `aitask_pick_own.sh`, `aitask_update.sh`, `aitask_archive.sh`, `./ait git`
- DOES use: `aitask_init_data.sh`, `aitask_lock.sh --check`, `.aitask-data-updated/` for plans and markers
- The completion marker at `.aitask-data-updated/completed_t<task_id>.json` is the signal for `aitask-web-merge` to detect and process this branch
- Parent tasks with pending children must be addressed by specifying a child task ID directly
- For the full-featured remote workflow with cross-branch operations, use `aitask-pickrem` instead
- For the standard interactive workflow, use `aitask-pick` instead
- Profile files are stored in `aitasks/metadata/profiles/` in YAML format
