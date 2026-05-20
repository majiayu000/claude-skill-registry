---
name: aitask-pickrem
description: Pick and implement a task in remote/non-interactive mode. All decisions from execution profile - no AskUserQuestion calls.
---

## Overview

This skill is a fully autonomous version of `aitask-pick` + `task-workflow` designed for environments where `AskUserQuestion` does not work (e.g., Claude Code Web). It combines task selection and implementation into a single self-contained workflow with **zero interactive prompts**. All decisions are driven by an execution profile.

**Key differences from `aitask-pick`:**
- Task ID is a **required** argument (no interactive browsing/selection)
- No `AskUserQuestion` calls anywhere in the workflow
- No worktree/branch management (always works on current branch)
- Auto-commits after implementation (no user review loop)
- Profile is required and auto-selected (not prompted)

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

Execute the **Execution Profile Selection Procedure — Auto-Select** (see `.claude/skills/task-workflow/execution-profile-selection-auto.md`) with `mode_label` = `"Remote"`.

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

### Step 3: Sync with Remote (Best-effort)

```bash
./.aitask-scripts/aitask_pick_own.sh --sync
```

Non-blocking — if it fails (e.g., no network, merge conflicts), continue silently.

### Step 4: Task Status Checks

**Check 1 — Done but unarchived task:**
- Read the task file's frontmatter `status` field
- If status is `Done`:
  - Read `done_task_action` from profile (default: `archive`)
  - If `archive`: display "Profile: auto-archiving Done task t\<N\>". Skip to **Step 10** (Archive).
  - If `skip`: display "Task t\<N\> has status Done, skipping per profile." End workflow.

**Check 2 — Orphaned parent task:**
- Check if the task file's frontmatter contains `children_to_implement: []` (empty list)
- If empty, check for archived children:
  ```bash
  ./.aitask-scripts/aitask_query_files.sh archived-children <number>
  ```
  Parse the output: `ARCHIVED_CHILD:<path>` lines mean archived children exist, `NO_ARCHIVED_CHILDREN` means none.
- If archived children exist:
  - Read `orphan_parent_action` from profile (default: `archive`)
  - If `archive`: display "Profile: auto-archiving orphaned parent t\<N\>". Skip to **Step 10** (Archive).
  - If `skip`: display "Orphaned parent t\<N\>, skipping per profile." End workflow.

If neither check triggers, proceed to Step 5.

### Step 5: Assign Task

- **Email resolution (priority order, non-interactive):**

  1. **Check task metadata:** Read the `assigned_to` field from the task file's frontmatter.
  2. **Check userconfig:** Read `aitasks/metadata/userconfig.yaml` and extract the `email:` field (if file exists).
  3. **Mismatch check (non-interactive):** If both `assigned_to` and userconfig email are non-empty and DIFFERENT: prefer `assigned_to`. Display warning: "Warning: assigned_to (\<email1\>) differs from userconfig (\<email2\>). Using assigned_to."
  4. **If `assigned_to` is non-empty** (and matches userconfig, or userconfig is empty): use `assigned_to`. Display: "Using email from task metadata: \<email\>"
  5. **Profile check:** Read `default_email` from profile:
     - If `"userconfig"`: Use the userconfig email (from step 2). If empty/missing, fall back to first email from `aitasks/metadata/emails.txt`. If both empty, proceed without email.
     - If `"first"`: read `aitasks/metadata/emails.txt` and use the first email address. If file is empty or missing, proceed without email.
     - If a literal email address: use that directly.
     - If not set in profile: proceed without email.

- Claim task ownership:

  If email was resolved:
  ```bash
  ./.aitask-scripts/aitask_pick_own.sh <task_num> --email "<email>"
  ```
  If no email:
  ```bash
  ./.aitask-scripts/aitask_pick_own.sh <task_num>
  ```

- **Parse the script output:**
  - `OWNED:<task_id>` — Success. Display: "Task t\<N\> claimed (email: \<email\>)". Proceed to Step 6.
  - `FORCE_UNLOCKED:<previous_owner>` + `OWNED:<task_id>` — Force-unlock succeeded. Display: "Force-unlocked stale lock held by \<previous_owner\>. Task t\<N\> claimed." Proceed to Step 6.
  - `LOCK_FAILED:<owner>|<locked_at>|<hostname>` — Parse the owner from the first `|`-separated field. Read `force_unlock_stale` from profile (default: `false`):
    - If `true`: Display "Profile: force-unlocking stale lock held by \<owner\>". Re-run with `--force`:
      ```bash
      ./.aitask-scripts/aitask_pick_own.sh <task_num> --force --email "<email>"
      ```
      Parse output again. If `FORCE_UNLOCKED` + `OWNED`: proceed. Otherwise: abort.
    - If `false`: Display error: "Task t\<N\> is locked by \<owner\>. Pick a different task." Abort.
  - `LOCK_ERROR:<message>` — Display error: "Lock system error: \<message\>. Run `./.aitask-scripts/aitask_lock_diag.sh` for troubleshooting." Abort.
  - `LOCK_INFRA_MISSING` — Display error: "Lock infrastructure not initialized. Run `ait setup`." Abort.

  If the script fails entirely (non-zero exit without structured output), display the error and abort.

### Step 6: Environment Setup

Remote mode always works on the current branch. No worktree or branch management.

Display: "Working on current branch (remote mode)"

### Step 7: Create Implementation Plan

#### 7.0: Check for Existing Plan

Check if a plan file already exists:
- For parent tasks: `aiplans/p<taskid>_*.md`
- For child tasks: `aiplans/p<parent>/p<parent>_<child>_*.md`

```bash
./.aitask-scripts/aitask_query_files.sh plan-file <taskid>
```
Parse the output: `PLAN_FILE:<path>` means found, `NOT_FOUND` means not found.

**If a plan file exists**, read it.

- Read `plan_preference` from profile (default: `use_current`):
  - `use_current`: Display "Profile: using existing plan". Skip to **Step 7 Checkpoint**.
  - `verify`: Display "Profile: verifying existing plan". Enter plan mode (Step 7.1), starting by reading and verifying the existing plan.
  - `create_new`: Display "Profile: creating plan from scratch". Enter plan mode (Step 7.1).

**If no plan file exists**, proceed to Step 7.1.

#### 7.1: Planning

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
- **Complexity:** Always implement as a single task (do NOT break into child subtasks — child creation requires interactive prompts not available in remote mode)
- **Testing requirement:** When the task involves code changes (not documentation/config-only tasks), the implementation plan MUST include a "Verification" section specifying:
  - What automated tests to write or update
  - What existing tests to run
  - Expected outcomes
  - For non-code tasks (documentation, config, skill files), a simple verification step (e.g., lint check, visual review of output) is sufficient
- Create a detailed implementation plan
- Include a reference to **Step 10 (Archive)** for post-implementation cleanup
- Use `ExitPlanMode` when ready for user approval

#### Save Plan to External File

After the user approves the plan via `ExitPlanMode`, save it.

**File naming convention:**

For parent tasks:
- Location: `aiplans/`
- Filename: Replace `t` prefix with `p`
- Example: `t16_implement_auth.md` → `aiplans/p16_implement_auth.md`

For child tasks:
- Location: `aiplans/p<parent>/`
- Filename: Replace `t` prefix with `p`
- Example: `t16_2_add_login.md` → `aiplans/p16/p16_2_add_login.md`

**Required metadata header for parent tasks:**
```markdown
---
Task: t16_implement_auth.md
Branch: (current branch, remote mode)
---
```

**Required metadata header for child tasks:**
```markdown
---
Task: t16_2_add_login.md
Parent Task: aitasks/t16_implement_auth.md
Sibling Tasks: aitasks/t16/t16_1_*.md, aitasks/t16/t16_3_*.md
Archived Sibling Plans: aiplans/archived/p16/p16_*_*.md
Branch: (current branch, remote mode)
---
```

#### Step 7 Checkpoint

Read `post_plan_action` from profile (default: `start_implementation`).

- `start_implementation`: Display "Profile: proceeding to implementation". Proceed to Step 8.
- If not set: proceed to Step 8 (default behavior for remote is always to continue).

### Step 8: Implement

**Pre-implementation ownership guard:**

Before starting implementation, verify that ownership/lock was acquired (Step 5 should have done this, but this guard catches edge cases like plan mode deferral):

- Read the task file's frontmatter `status` and `assigned_to` fields
- Resolve the current user's email: use the email from Step 5 if available, otherwise from `aitasks/metadata/userconfig.yaml` or profile `default_email`
- **If status is `Implementing` AND `assigned_to` matches the current user's email:** Ownership was already acquired in Step 5. Proceed normally.
- **Otherwise** (status is not `Implementing`, or `assigned_to` is empty/missing, or `assigned_to` does not match the current user's email): Ownership was not properly acquired. Display: "Guard: task ownership not confirmed — acquiring ownership now."
  - Run the ownership claim:
    ```bash
    ./.aitask-scripts/aitask_pick_own.sh <task_num> --email "<email>"
    ```
  - Parse output: `OWNED` → proceed. Any failure (`LOCK_FAILED`, `LOCK_ERROR`, `LOCK_INFRA_MISSING`, or script error) → trigger the **Abort Procedure**.
  - No `AskUserQuestion` calls (remote mode constraint).

**Record implementing agent:** Execute the **Agent Attribution Procedure** (see `../task-workflow/agent-attribution.md`) to record which code agent and model is implementing this task.

Follow the approved plan, working in the current directory.

Update the external plan file as you progress:
- Mark steps as completed
- Note any deviations or changes from the original plan
- Record issues encountered during implementation

**Testing (when applicable):**
- After implementation is complete, run all relevant automated tests if the task involves code changes
- If tests fail, attempt to fix the issues before proceeding to Step 9
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

### Step 9: Auto-Commit

Read `review_action` from profile (default: `commit`).

1. **Show change summary:**
   ```bash
   git status
   git diff --stat
   ```

2. **Check for changes:**
   ```bash
   git status --porcelain
   ```
   If no changes detected, display warning "No changes detected after implementation" and skip to Step 10.

3. **Consolidate the plan file:**
   - Read the current plan file from `aiplans/`
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
   - **IMPORTANT for child tasks:** The plan file will be archived and serve as the primary reference for subsequent sibling tasks. Ensure the Final Implementation Notes are comprehensive.

4. **Commit code changes and plan file separately:**
   - **Code commit:**
     ```bash
     git add <changed_code_files>
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
     Only include implementation files — never `aitasks/` or `aiplans/` paths. Skip if no code changes. The `<issue_type>` comes from the task's frontmatter. Examples: `feature: Add channel settings (t16)`, `bug: Fix login validation (t16_2)`. If code-agent attribution fails, continue with the contributor-only or plain commit message.
   - **Plan file commit:**
     ```bash
     ./ait git add aiplans/<plan_file>
     ./ait git commit -m "ait: Update plan for t<task_id>"
     ```
     Skip if plan file was not modified.
   - **Never mix** code files and `aitasks/`/`aiplans/` files in the same `git add` or commit.
   - Display: "Changes committed: \<commit_hash\>"

5. Proceed to Step 10.

### Step 10: Archive and Push

**For child tasks — verify plan completeness:**
- Read the plan file
- Verify it contains a "Final Implementation Notes" section with comprehensive details
- If missing or incomplete, add/update it now

**Run the archive script:**

For parent tasks:
```bash
./.aitask-scripts/aitask_archive.sh <task_num>
```

For child tasks:
```bash
./.aitask-scripts/aitask_archive.sh <parent>_<child>
```

**Parse structured output and handle without prompts:**

Read `issue_action` from profile (default: `close_with_notes`).

- `ISSUE:<task_num>:<issue_url>` — Handle based on `issue_action`:
  - `close_with_notes`:
    ```bash
    ./.aitask-scripts/aitask_issue_update.sh --close <task_num>
    ```
  - `comment_only`:
    ```bash
    ./.aitask-scripts/aitask_issue_update.sh <task_num>
    ```
  - `close_silent`:
    ```bash
    ./.aitask-scripts/aitask_issue_update.sh --close --no-comment <task_num>
    ```
  - `skip`: do nothing

- `PARENT_ISSUE:<task_num>:<url>` — Same handling as `ISSUE` using `issue_action`

- `FOLDED_ISSUE:<folded_task_num>:<issue_url>` — Same handling, but use the primary `task_id` for the script call:
  - `close_with_notes`:
    ```bash
    ./.aitask-scripts/aitask_issue_update.sh --issue-url "<issue_url>" --close <task_id>
    ```
  - `comment_only`:
    ```bash
    ./.aitask-scripts/aitask_issue_update.sh --issue-url "<issue_url>" <task_id>
    ```
  - `close_silent`:
    ```bash
    ./.aitask-scripts/aitask_issue_update.sh --issue-url "<issue_url>" --close --no-comment <task_id>
    ```
  - `skip`: do nothing

- `FOLDED_WARNING:<task_num>:<status>` — Display warning: "Folded task t\<N\> has status '\<status\>' — skipping deletion."

- `PARENT_ARCHIVED:<path>` — Display: "All child tasks complete! Parent task also archived."

- `COMMITTED:<hash>` — Display: "Archival committed: \<hash\>"

**Push:**
```bash
./ait git push
```

Display: "Task t\<task_id\> completed and archived."

### Abort Procedure

Triggered by errors after Step 5 (task was claimed). Not triggered by user interaction.

1. Read `abort_plan_action` from profile (default: `keep`):
   - `keep`: leave plan file in `aiplans/`
   - `delete`: remove plan file

2. Read `abort_revert_status` from profile (default: `Ready`)

3. Release lock:
   ```bash
   ./.aitask-scripts/aitask_lock.sh --unlock <task_num> 2>/dev/null || true
   ```

4. Revert status:
   ```bash
   ./.aitask-scripts/aitask_update.sh --batch <task_num> --status <status> --assigned-to ""
   ```

5. Commit:
   ```bash
   ./ait git add aitasks/
   ./ait git commit -m "ait: Abort t<N>: revert status to <status>"
   ```

6. Display: "Task t\<N\> aborted and reverted to '\<status\>'."

---

## Extended Profile Schema

The remote skill uses the standard profile format from `aitasks/metadata/profiles/` with additional fields. Fields from the standard schema that are recognized:

| Key | Type | Default | Values | Purpose |
|-----|------|---------|--------|---------|
| `name` | string | (required) | Display name | Shown during profile load |
| `description` | string | (required) | Description text | Shown during profile load |
| `skip_task_confirmation` | bool | `true` | (hardcoded, not used) | Always skipped in remote mode |
| `default_email` | string | — | `"first"` or email address | Step 5 email assignment |
| `plan_preference` | string | `use_current` | `"use_current"`, `"verify"`, `"create_new"` | Step 7.0 existing plan handling |
| `post_plan_action` | string | `start_implementation` | `"start_implementation"` | Step 7 checkpoint |
| `enableFeedbackQuestions` | bool | `false` | `true`, `false` | Defined in the shared schema but not used here because remote mode has no feedback prompt |

**Remote-specific fields** (only recognized by this skill):

| Key | Type | Default | Values | Purpose |
|-----|------|---------|--------|---------|
| `force_unlock_stale` | bool | `false` | `true`, `false` | Step 5: Auto force-unlock stale locks |
| `done_task_action` | string | `archive` | `"archive"`, `"skip"` | Step 4: Done task handling |
| `orphan_parent_action` | string | `archive` | `"archive"`, `"skip"` | Step 4: Orphan parent handling |
| `complexity_action` | string | `single_task` | `"single_task"` | Always single task (no child creation in remote) |
| `review_action` | string | `commit` | `"commit"` | Step 9: Auto-commit behavior |
| `issue_action` | string | `close_with_notes` | `"skip"`, `"close_with_notes"`, `"comment_only"`, `"close_silent"` | Step 10: Issue handling |
| `abort_plan_action` | string | `keep` | `"keep"`, `"delete"` | Abort: Plan file action |
| `abort_revert_status` | string | `Ready` | `"Ready"`, `"Editing"` | Abort: Revert status |

Fields from the standard schema that are **ignored** (not applicable in remote mode): `create_worktree`, `base_branch`.

---

## Notes

- This skill has **zero `AskUserQuestion` calls** — designed for environments where that tool does not work (e.g., Claude Code Web)
- `EnterPlanMode`/`ExitPlanMode` are still used for plan creation (they are NOT `AskUserQuestion`)
- Parent tasks with pending children must be addressed by specifying a child task ID directly
- No worktree or branch management — always works on the current branch in the current directory
- All profile fields have sensible defaults — the profile only needs `name` and `description` to function, though providing all fields is recommended
- The commit message format follows the project convention: `<issue_type>: <description> (t<task_id>)` for implementation commits, `ait:` prefix for administrative commits (archival, abort)
- For the standard interactive workflow, use `aitask-pick` instead
- Profile files are stored in `aitasks/metadata/profiles/` in YAML format
