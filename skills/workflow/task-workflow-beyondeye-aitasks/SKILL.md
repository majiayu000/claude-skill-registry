---
name: task-workflow
description: Shared implementation workflow for task-based skills. Handles status checks, assignment, environment setup, planning, implementation, review, and archival.
user-invocable: false
---

## Context Requirements

This skill is invoked by other skills (e.g., aitask-pick, aitask-explore, aitask-review) after they have selected a task. The calling skill MUST establish the following context before handing off:

| Variable | Type | Description |
|----------|------|-------------|
| `task_file` | string | Path to selected task file (e.g., `aitasks/t16_implement_auth.md` or `aitasks/t10/t10_2_add_login.md`) |
| `task_id` | string | Task identifier (e.g., `16` or `16_2`) |
| `task_name` | string | Filename stem for branches/worktrees (e.g., `t16_implement_auth` or `t16_2_add_login`) |
| `is_child` | boolean | Whether this is a child task |
| `parent_id` | string/null | Parent task number if child (e.g., `16`), null otherwise |
| `parent_task_file` | string/null | Path to parent task file if child (e.g., `aitasks/t16_implement_auth.md`), null otherwise |
| `active_profile` | object/null | Loaded execution profile from calling skill (or null if no profile) |
| `active_profile_filename` | string/null | Scanner-returned filename for the profile (e.g., `fast.yaml` or `local/fast.yaml`), null if no profile |
| `previous_status` | string | Task status before workflow began (for abort revert, e.g., `Ready`) |
| `folded_tasks` | array/null | List of task IDs folded into this task (e.g., `[106, 129_5]`), or null/empty if none. Set by aitask-explore when existing tasks are folded into a new task. |
| `skill_name` | string | Name of the calling skill for feedback tracking (e.g., `pick`, `explore`, `pr-import`) |
| `feedback_collected` | boolean | Guard flag — initialized to `false`. Set to `true` after the Satisfaction Feedback Procedure runs. Prevents double execution across workflow paths. |

## Workflow

### Step 3: Task Status Checks

After a task is selected and confirmed, perform these checks before proceeding to Step 4.

**Check 1 - Done but unarchived task:**
- Read the task file's frontmatter `status` field
- If status is `Done`:
  - Check if a plan file exists:
    ```bash
    ./.aitask-scripts/aitask_query_files.sh plan-file <taskid>
    ```
    Parse the output: `PLAN_FILE:<path>` means found, `NOT_FOUND` means not found.
  - Use `AskUserQuestion`:
    - Question: "This task has status 'Done' but hasn't been archived yet. Would you like to archive it now?"
    - Header: "Archive"
    - Options:
      - "Yes, archive it" (description: "Proceed to archive the task and plan file if found")
      - "No, skip" (description: "Leave the task as-is and end the workflow")
  - If "Yes, archive it" → skip Steps 4-8, proceed directly to **Step 9** (Post-Implementation) for parent task archival
  - If "No, skip" → end the workflow

**Check 2 - Orphaned parent task (empty children_to_implement):**
- Check if the task file's frontmatter contains `children_to_implement: []` (empty list)
- If empty, check for archived children:
  ```bash
  ./.aitask-scripts/aitask_query_files.sh archived-children <number>
  ```
  Parse the output: `ARCHIVED_CHILD:<path>` lines mean archived children exist, `NO_ARCHIVED_CHILDREN` means none.
- If archived children exist, this is an orphaned parent task:
  - Use `AskUserQuestion`:
    - Question: "This parent task has all children completed and archived, but the parent itself was not archived. Would you like to archive it now?"
    - Header: "Archive"
    - Options:
      - "Yes, archive it" (description: "Proceed to archive the parent task and plan file if found")
      - "No, skip" (description: "Leave the task as-is and end the workflow")
  - If "Yes, archive it" → skip Steps 4-8, proceed directly to **Step 9** (Post-Implementation) for parent task archival
  - If "No, skip" → end the workflow

**Note:** These checks should NOT set the task status to "Implementing" — the task is already done. Skip Step 4 (Assign Task) entirely when archiving via this step.

If neither check triggers, proceed to Step 4 as normal.

### Step 3b: refresh execution profile
If `active_profile` was provided and is non-null, re-read the profile YAML file using the stored filename: `cat aitasks/metadata/profiles/<active_profile_filename>`. Display: "Refreshing profile: \<name\>". If the file cannot be read (missing or invalid), warn: "Warning: Could not refresh profile '\<name\>', proceeding without profile" and set `active_profile` to null.

If `active_profile` is null (either because no profile was selected by the calling skill, or because the profile name was lost during a long conversation), re-run the profile selection: execute the **Execution Profile Selection Procedure** (see `execution-profile-selection.md`).

### Step 4: Assign Task to User

- **Email resolution (priority order):**

  1. **Check task metadata:** Read the `assigned_to` field from the task file's frontmatter.
  2. **Check userconfig:** Read `aitasks/metadata/userconfig.yaml` and extract the `email:` field (if file exists).
  3. **Mismatch check:** If both `assigned_to` and userconfig email are non-empty and DIFFERENT, use `AskUserQuestion`:
     - Question: "Task is assigned to \<assigned_to\> but your userconfig email is \<userconfig_email\>. Which email to use?"
     - Header: "Email"
     - Options:
       - "Keep \<assigned_to\>" (description: "Continue with the existing assignment")
       - "Use \<userconfig_email\>" (description: "Override with your local email")
     - Use the selected email and proceed to the **Claim task ownership** step below.
  4. **If `assigned_to` is non-empty** (and matches userconfig, or userconfig is empty): use `assigned_to`. Display: "Using email from task metadata: \<email\>". Skip to **Claim task ownership**.
  5. **Profile check:** If the active profile has `default_email` set:
     - If value is `"userconfig"`: Use the userconfig email (from step 2). If userconfig is empty/missing, fall back to reading `aitasks/metadata/emails.txt` (first email). Display: "Profile '\<name\>': using email \<email\> (from userconfig)". If both are empty, fall through to the AskUserQuestion below.
     - If value is `"first"`: Read `aitasks/metadata/emails.txt` and use the first email address. Display: "Profile '\<name\>': using email \<email\>". If emails.txt is empty or missing, fall through to the AskUserQuestion below.
     - If value is a literal email address: Use that email directly. Display: "Profile '\<name\>': using email \<email\>"
     - Skip the AskUserQuestion below

  6. **Otherwise, ask for email using `AskUserQuestion`:**
     - Read stored emails: `cat aitasks/metadata/emails.txt 2>/dev/null | sort -u`
     - Question: "Enter your email to track who is working on this task (optional):"
     - Header: "Email"
     - Options:
       - List each stored email from emails.txt (if any exist)
       - "Enter new email" (description: "Add a new email address")
       - "Skip" (description: "Don't assign this task to anyone")

  - **If "Enter new email" selected:**
    - Ask user to type their email via `AskUserQuestion` with free text (use the "Other" option)

- **Userconfig sync check:** After email is resolved, if the final email differs from the userconfig email (or userconfig doesn't exist):
  - Use `AskUserQuestion`:
    - Question: "The selected email (\<email\>) differs from your userconfig (\<userconfig_email\>). Update userconfig.yaml?"
    - Header: "Userconfig"
    - Options:
      - "Yes, update userconfig" (description: "Save this email to userconfig.yaml for future use")
      - "No, keep current userconfig" (description: "Use this email for now but don't change userconfig")
  - If "Yes": Write `email: <email>` to `aitasks/metadata/userconfig.yaml` (create file if needed with comment header `# Local user configuration (gitignored, not shared)`)
  - If "No": Proceed without updating
  - **Skip this check** if: the final email matches userconfig, or email was resolved from userconfig itself, or no email was selected ("Skip")

- **Claim task ownership (lock, update status, commit, push):**

  If email was provided (new or selected):
  ```bash
  ./.aitask-scripts/aitask_pick_own.sh <task_num> --email "<email>"
  ```
  If no email (user selected "Skip"):
  ```bash
  ./.aitask-scripts/aitask_pick_own.sh <task_num>
  ```

  **Parse the script output:**
  - `OWNED:<task_id>` — Success. Proceed to Step 5.
  - `FORCE_UNLOCKED:<previous_owner>` + `OWNED:<task_id>` — Force-unlock succeeded. Inform user: "Force-unlocked stale lock held by \<previous_owner\>." Proceed to Step 5.
  - `LOCK_FAILED:<owner>|<locked_at>|<hostname>` — Task is locked by another user/PC. Parse the `|`-separated fields for lock details. Use `AskUserQuestion`:
    - Question: "Task t\<N\> is locked by \<owner\> (since \<locked_at\>, hostname: \<hostname\>). Force unlock?"
    - Header: "Lock"
    - Options:
      - "Force unlock and claim" (description: "Override the stale lock and claim this task")
      - "Pick a different task" (description: "Leave the lock intact and select another task")
    - If "Force unlock and claim": Re-run ownership with `--force`:
      ```bash
      ./.aitask-scripts/aitask_pick_own.sh <task_num> --force --email "<email>"
      ```
      Parse the output again. If `FORCE_UNLOCKED` + `OWNED`: proceed. Otherwise: abort.
    - If "Pick a different task": Return to the calling skill's task selection. Do NOT proceed.
  - `LOCK_ERROR:<message>` — Lock system error (fetch failure, race exhaustion, etc.). Display the error and suggest running `./.aitask-scripts/aitask_lock_diag.sh` for troubleshooting. Use `AskUserQuestion`:
    - Question: "Lock system error: \<message\>. How to proceed?"
    - Header: "Lock error"
    - Options:
      - "Retry" (description: "Try acquiring the lock again")
      - "Continue without lock" (description: "Proceed without locking (risky if multiple users)")
      - "Abort" (description: "Stop the workflow")
    - If "Retry": Re-run `aitask_pick_own.sh` (same command). Parse output again.
    - If "Continue without lock": Skip lock acquisition, proceed to Step 5 (task status will be updated but no lock held).
    - If "Abort": End the workflow.
  - `LOCK_INFRA_MISSING` — Lock infrastructure not initialized. Inform user to run `ait setup` and abort.

  **Note:** The script handles email storage, lock acquisition, task metadata update (`status` → Implementing, `assigned_to`), and git add/commit/push internally. If the script fails entirely (non-zero exit without structured output), display the error and abort.

- **Store previous status for potential abort** (remember the `previous_status` from context)

### Step 5: Environment and Branch Setup

> **Note:** For fully autonomous remote workflows (Claude Code Web), use the `aitask-pickrem` skill instead — it skips all environment setup and always works on the current branch.

- **Profile check:** If the active profile has `create_worktree` set:
  - If `true`: Create worktree. Display: "Profile '\<name\>': creating worktree"
  - If `false`: Work on current branch. Display: "Profile '\<name\>': working on current branch"
  - Skip the AskUserQuestion below

  Otherwise, use `AskUserQuestion` to ask:
  - "Do you want to create a separate branch and worktree for this task?"
  - Options: "No, work on current branch" (default, first option) / "Yes, create worktree (recommended for complex features or when working in parallel on multiple features)"

**If Yes:**

- Extract `<task_name>` from the filename
  - For parent: `t16_implement_channel_settings` from `t16_implement_channel_settings.md`
  - For child: `t16_2_add_login` from `t16_2_add_login.md`

- **Profile check:** If the active profile has `base_branch` set:
  - Use the specified branch name. Display: "Profile '\<name\>': using base branch \<branch\>"
  - Skip the AskUserQuestion below

  Otherwise, ask which branch to base the new branch on using `AskUserQuestion`:
  - "Which branch should the new task branch be based on?"
  - Options: "main (Recommended)" / "Other branch"
  - If "Other branch", ask user to specify the branch name

- Create worktree directory:
  ```bash
  mkdir -p aiwork
  ```

- Create both the branch and worktree in a single command:
  ```bash
  git worktree add -b aitask/<task_name> aiwork/<task_name> <base-branch>
  ```
  Where `<base-branch>` is `main` or the user-specified branch.

- Work in the `aiwork/<task_name>/` directory for implementation

**If No:**
- Work directly on the current branch in the current directory

### Step 6: Create Implementation Plan

> **Full planning workflow:** Read `planning.md` for the complete Step 6 procedure including:
> - 6.0: Check for Existing Plan (profile-aware)
> - 6.1: Planning (EnterPlanMode, child tasks, complexity assessment)
> - Child Task Documentation Requirements
> - Save Plan to External File (naming conventions, metadata headers)
> - Checkpoint (post-plan action)
>
> After the checkpoint in `planning.md`:
> - If child tasks were created and the child checkpoint returned "Stop here" → collect **Satisfaction Feedback Procedure** (see `satisfaction-feedback.md`) with `skill_name` from context variables, then **END the workflow** (do NOT proceed to Step 7/8/9)
> - If child tasks were created and the child checkpoint returned "Start first child" → restart with `/aitask-pick <parent>_1` (do NOT proceed to Step 7)
> - Otherwise (normal single-task plan) → proceed to Step 7

### Step 7: Implement

**Pre-implementation ownership guard:**

Before starting implementation, verify that ownership/lock was acquired (Step 4 should have done this, but this guard catches edge cases like plan mode deferral):

- Read the task file's frontmatter `status` and `assigned_to` fields
- Resolve the current user's email: use the email from Step 4 if available, otherwise read from `aitasks/metadata/userconfig.yaml`
- **If status is `Implementing` AND `assigned_to` matches the current user's email:** Ownership was already acquired in Step 4. Proceed normally.
- **Otherwise** (status is not `Implementing`, or `assigned_to` is empty/missing, or `assigned_to` does not match the current user's email): Ownership was not properly acquired. Display: "Guard: task ownership not confirmed — acquiring ownership now."
  - Run the ownership claim:
    ```bash
    ./.aitask-scripts/aitask_pick_own.sh <task_num> --email "<email>"
    ```
  - Parse output as in Step 4:
    - `OWNED:<task_id>` — Success. Proceed.
    - `LOCK_FAILED:<owner>|<locked_at>|<hostname>` — Parse the `|`-separated fields. Use `AskUserQuestion` with options: "Force unlock and claim" / "Abort task". If force unlock, re-run with `--force`. If abort, execute the **Task Abort Procedure** (see `task-abort.md`).
    - `LOCK_ERROR:<message>` — Display error. Use `AskUserQuestion`: "Retry" / "Continue without lock" / "Abort". Handle as in Step 4.
    - `LOCK_INFRA_MISSING` — Inform user to run `ait setup` and abort.
    - Script fails entirely — display error and abort.

**Record implementing agent:** Execute the **Agent Attribution Procedure** (see `agent-attribution.md`) to record which code agent and model is implementing this task.

**Repository structure awareness:** Before starting implementation, read `repo-structure.md`

Follow the approved plan, working in the directory specified in the plan metadata.

Update the external plan file as you progress:
- Mark steps as completed
- Note any deviations or changes from the original plan
- Record issues encountered during implementation

**IMPORTANT:** Do NOT commit changes automatically after implementation. Proceed to Step 8 for user review and approval.

**Note:** When committing implementation changes (in Step 8), the commit message must follow the `<issue_type>: <description> (t<task_id>)` format. See Step 8 for details.

### Step 8: User Review and Approval

After implementation is complete, the user MUST be given the opportunity to review and test changes before any commits are made.

- **Show change summary:**
  ```bash
  git status
  git diff --stat
  ```

- **Ask for user approval using `AskUserQuestion`:**
  - Question: "Implementation complete. Please review and test the changes. When ready, select an option:"
  - Header: "Review"
  - Options:
    - "Commit changes" (description: "Changes reviewed and tested, ready to commit")
    - "Need more changes" (description: "Adjustments needed before committing")
    - "Abort task" (description: "Discard changes and revert task status")

- **If "Commit changes":**
  - **Consolidate the plan file** before committing:
    - Read the current plan file from `aiplans/`
    - Review `git diff --stat` against the plan to identify any changes not yet documented
    - Add or update a "Final Implementation Notes" section at the end of the plan:
      ```markdown
      ## Final Implementation Notes
      - **Actual work done:** <summary of what was actually implemented vs what was originally planned>
      - **Deviations from plan:** <any changes from the original approach and why>
      - **Issues encountered:** <problems found during implementation and how they were resolved>
      - **Key decisions:** <technical decisions made during implementation>
      - **Notes for sibling tasks:** <patterns established, gotchas discovered, shared code created, or other information useful for subsequent child tasks> (include this section if this is a child task)
      ```
    - **IMPORTANT for child tasks:** The plan file will be archived and serve as the primary reference for subsequent sibling tasks. Ensure the Final Implementation Notes are comprehensive enough that a fresh context can understand what was done and learn from the experience.
    - The plan file should now serve as a complete record of: the original plan, any post-review change requests (from the "Need more changes" loop), and final implementation notes
  - **Contributor attribution:** Execute the **Contributor Attribution Procedure** (see `contributor-attribution.md`) to determine whether the commit needs an imported-contributor block.
  - **Code-agent attribution:** Execute the **Code-Agent Commit Attribution Procedure** (see `code-agent-commit-attribution.md`) to resolve a `Co-Authored-By` trailer from `implemented_with`. If agent attribution fails, continue with the contributor-only or plain commit message as applicable.
  - **Commit code changes and plan file separately** (code uses regular `git`, plan uses `./ait git`):
    1. **Code commit** — Stage and commit source code changes:
       ```bash
       git add <changed_code_files>
       git commit -m "$(cat <<'EOF'
       <issue_type>: <description> (t<task_id>)

       <optional imported contributor block>
       <optional code-agent trailer>
       EOF
       )"
       ```
       Only include implementation files — never include `aitasks/` or `aiplans/` paths. Skip this commit if there are no code changes. If neither attribution procedure returns content, the code commit can remain a single-line subject.
    2. **Plan file commit** — Stage and commit the updated plan file:
       ```bash
       ./ait git add aiplans/<plan_file>
       ./ait git commit -m "ait: Update plan for t<task_id>"
       ```
       Skip if the plan file was not modified.
  - **IMPORTANT — Commit message conventions:**
    - **Code commits** MUST use `<issue_type>: <description> (t<task_id>)` format, where `<issue_type>` comes from the task's `issue_type` frontmatter (one of: `bug`, `chore`, `documentation`, `feature`, `performance`, `refactor`, `style`, `test`). The `(t<task_id>)` suffix is used by `aitask_issue_update.sh` to find commits. Examples: `feature: Add channel settings screen (t16)`, `bug: Fix login validation (t16_2)`.
    - **When attribution is present,** compose one final multiline commit message: subject first, imported contributor block second, code-agent trailer last. For PR-imported tasks the contributor block includes `Based on PR:`; for issue-imported contributor metadata it may be only the contributor trailer.
    - **Plan/task file commits** use the `ait:` prefix (e.g., `ait: Update plan for t16`). Administrative commits (status changes, archival) also use `ait:` and must NOT include the `(t<task_id>)` tag.
    - **Never mix** code files and `aitasks/`/`aiplans/` files in the same `git add` or commit. Code uses regular `git`; task/plan files use `./ait git`. This separation is required when task data lives on a separate branch, and is safe in legacy mode where `./ait git` passes through to plain `git`.
  - Proceed to Step 8b

- **If "Need more changes":**
  - Ask user what needs to change
  - Make the requested changes
  - **Update the plan file** to log what was changed:
    - Append a "Post-Review Changes" section (if not already present) to the plan file in `aiplans/`
    - Add a numbered change request entry with timestamp:
      ```markdown
      ## Post-Review Changes

      ### Change Request 1 (YYYY-MM-DD HH:MM)
      - **Requested by user:** <summary of what the user asked for>
      - **Changes made:** <summary of what was actually implemented>
      - **Files affected:** <list of modified files>
      ```
    - Increment the change request number for each review iteration
  - Return to the beginning of Step 8

- **If "Abort":**
  - Execute the **Task Abort Procedure** (see `task-abort.md`)

### Step 8b: Test Follow-up Task (Optional)

After code is committed and before post-implementation cleanup, optionally create a follow-up task for testing.

Execute the **Test Follow-up Task Procedure** (see `test-followup-task.md`).

Proceed to Step 9.

### Step 9: Post-Implementation

Execute the post-implementation cleanup steps.

**If a separate branch was created:**

**IMPORTANT:** Use `AskUserQuestion` to ask: "Proceed with merge of code changes to main branch?" with options "Yes, proceed with merge" / "No, not yet". Do NOT proceed until the user approves.

- **Check for uncommitted changes:**
  ```bash
  git status --porcelain
  ```

- **Merge branch into main:**
  ```bash
  git checkout main
  git merge aitask/<task_name>
  ```

- **Handle merge conflicts:** Ask user for guidance if needed.

- **Verify build (if configured):**
  - Read `aitasks/metadata/project_config.yaml` and check the `verify_build` field
  - **If `verify_build` is absent, null, or empty (or file doesn't exist):** Display "No verify_build configured — skipping build verification." and skip this step.
  - **If `verify_build` is a single command string:** Run it.
  - **If `verify_build` is a list of commands:** Run each sequentially (stop on first failure).
  - **If the build fails:**
    1. Analyze the error output and compare against the changes introduced by this task (`git diff` against the base)
    2. **If the failure is caused by this task's changes:** Go back to the implementation to fix the build errors. After fixing, re-run the build command(s). Repeat until the build passes.
    3. **If the failure is NOT related to this task's changes** (pre-existing issue, environment problem, etc.): Log the build failure details in the plan file's "Final Implementation Notes" section under a "Build verification" entry and proceed with the workflow. Do not attempt to fix pre-existing issues.

- **Clean up branch and worktree:**
  ```bash
  git worktree remove aiwork/<task_name>
  rm -rf aiwork/<task_name>
  git branch -d aitask/<task_name>
  ```

**For child tasks — verify plan completeness before archival:**

- Read the plan file from `aiplans/p<parent>/<child_plan>`
- Verify it contains a "Final Implementation Notes" section with comprehensive details
- If missing or incomplete, add/update it now — the archived plan will serve as the primary reference for subsequent sibling tasks
- Ensure the notes include: actual work done, issues encountered and resolutions, and any information useful for sibling tasks

**Run the archive script:**

All archival operations (metadata updates, file moves, lock releases, folded task cleanup, git staging, and commit) are handled by a single script call:

For parent tasks:
```bash
./.aitask-scripts/aitask_archive.sh <task_num>
```

For child tasks:
```bash
./.aitask-scripts/aitask_archive.sh <parent>_<child>
```

The script automatically handles:
- Updating task metadata (status → Done, updated_at, completed_at)
- Creating archive directories and moving task/plan files
- For child tasks: removing child from parent's children_to_implement
- For child tasks: archiving parent too if all children are complete
- Releasing task locks (and parent locks if parent was also archived)
- For parent tasks: deleting folded tasks (if any, where status is not Implementing/Done)
- Git staging and committing all changes

**Parse the script output and handle interactive follow-ups:**

The script outputs structured lines. Parse each line and handle accordingly:

- `ISSUE:<task_num>:<issue_url>` — Execute the **Issue Update Procedure** (see `issue-update.md`) for the task
- `RELATED_ISSUE:<task_num>:<issue_url>` — A related/merged issue. Execute the **Related Issue Update Procedure** (see `issue-update.md`, "Related Issues" section) using `--issue-url`
- `PARENT_ISSUE:<task_num>:<issue_url>` — Execute the **Issue Update Procedure** (see `issue-update.md`) for the parent task
- `PARENT_RELATED_ISSUE:<task_num>:<issue_url>` — A related/merged issue on the parent. Execute the **Related Issue Update Procedure** (see `issue-update.md`, "Related Issues" section) using `--issue-url`
- `FOLDED_RELATED_ISSUE:<folded_task_num>:<issue_url>` — A related issue on a folded task (file deleted). Handle identically to `FOLDED_ISSUE:` below (same AskUserQuestion, same `--issue-url` commands, same `task_id` note)
- `FOLDED_ISSUE:<folded_task_num>:<issue_url>` — The folded task's file has been deleted, so the standard Issue Update Procedure cannot be used (it requires the task file). Instead, handle inline:
  - Use `AskUserQuestion`:
    - Question: "Folded task t<folded_task_num> had a linked issue: <issue_url>. Update/close it?"
    - Header: "Issue"
    - Options:
      - "Close with notes" (description: "Post implementation notes from primary task and close")
      - "Comment only" (description: "Post implementation notes but leave open")
      - "Close silently" (description: "Close without posting a comment")
      - "Skip" (description: "Don't touch the issue")
  - If "Close with notes":
    ```bash
    ./.aitask-scripts/aitask_issue_update.sh --issue-url "<issue_url>" --close <task_id>
    ```
  - If "Comment only":
    ```bash
    ./.aitask-scripts/aitask_issue_update.sh --issue-url "<issue_url>" <task_id>
    ```
  - If "Close silently":
    ```bash
    ./.aitask-scripts/aitask_issue_update.sh --issue-url "<issue_url>" --close --no-comment <task_id>
    ```
  - If "Skip": do nothing
  - Note: Uses the primary `task_id` (not `folded_task_num`) so the comment references the primary task's commits and plan file
- `PR:<task_num>:<pr_url>` — Execute the **PR Close/Decline Procedure** (see `pr-close-decline.md`) for the task
- `PARENT_PR:<task_num>:<pr_url>` — Execute the **PR Close/Decline Procedure** (see `pr-close-decline.md`) for the parent task
- `FOLDED_PR:<folded_task_num>:<pr_url>` — The folded task's file has been deleted, so the standard PR Close/Decline Procedure cannot be used. Instead, handle inline:
  - Use `AskUserQuestion`:
    - Question: "Folded task t<folded_task_num> had a linked PR: <pr_url>. Close/decline it?"
    - Header: "PR"
    - Options:
      - "Close with notes" (description: "Post implementation notes from primary task and close/decline")
      - "Comment only" (description: "Post implementation notes but leave open")
      - "Close silently" (description: "Close/decline without posting a comment")
      - "Skip" (description: "Don't touch the PR")
  - If "Close with notes":
    ```bash
    ./.aitask-scripts/aitask_pr_close.sh --pr-url "<pr_url>" --close <task_id>
    ```
  - If "Comment only":
    ```bash
    ./.aitask-scripts/aitask_pr_close.sh --pr-url "<pr_url>" <task_id>
    ```
  - If "Close silently":
    ```bash
    ./.aitask-scripts/aitask_pr_close.sh --pr-url "<pr_url>" --close --no-comment <task_id>
    ```
  - If "Skip": do nothing
  - Note: Uses the primary `task_id` (not `folded_task_num`) so the comment references the primary task's commits and plan file
- `FOLDED_WARNING:<task_num>:<status>` — Warn the user: "Folded task t<N> has status '<status>' — skipping automatic deletion. Please handle it manually."
- `PARENT_ARCHIVED:<path>` — Inform user: "All child tasks complete! Parent task also archived."
- `COMMITTED:<hash>` — Archival commit was created

**Push after archival:**

```bash
./ait git push
```

### Step 9b: Satisfaction Feedback

Execute the **Satisfaction Feedback Procedure** (see `satisfaction-feedback.md`) with `skill_name` from the context variables.

### Procedures

The following procedures are in individual files — read on demand when referenced:

- **Task Abort Procedure** (`task-abort.md`) — Lock release, status revert, worktree cleanup. Referenced from Step 6 checkpoint and Step 8.
- **Issue Update Procedure** (`issue-update.md`) — Update/close linked issues during archival. Referenced from Step 9.
- **PR Close/Decline Procedure** (`pr-close-decline.md`) — Close/decline linked pull requests during archival. Referenced from Step 9.
- **Contributor Attribution Procedure** (`contributor-attribution.md`) — Credit PR contributors in commit messages. Referenced from Step 8.
- **Code-Agent Commit Attribution Procedure** (`code-agent-commit-attribution.md`) — Resolve code-agent Co-Authored-By trailer. Referenced from Step 8.
- **Model Self-Detection Sub-Procedure** (`model-self-detection.md`) — Detect the current code agent and model. Referenced from Agent Attribution and Satisfaction Feedback.
- **Agent Attribution Procedure** (`agent-attribution.md`) — Record implementing code agent and model. Referenced from Step 7.
- **Test Follow-up Task Procedure** (`test-followup-task.md`) — Optionally create testing follow-up task. Referenced from Step 8b.
- **Satisfaction Feedback Procedure** (`satisfaction-feedback.md`) — Collect user feedback and update verified model scores. Referenced from Step 9b and standalone skills.
- **Lock Release Procedure** (`lock-release.md`) — Release task locks. Referenced from Task Abort Procedure.
- **Execution Profile Selection Procedure** (`execution-profile-selection.md`) — Interactive profile scan and selection. Referenced from Step 0a in calling skills and Step 3b.
- **Execution Profile Selection Procedure — Auto-Select** (`execution-profile-selection-auto.md`) — Non-interactive auto-select for remote/web skills. Referenced from Step 1 in aitask-pickrem/aitask-pickweb.

---

## Notes

- When working on a child task, always include links to parent and sibling task files for context, plus archived sibling plan files as primary reference for completed siblings
- **Archived sibling context priority:** When gathering context for a child task, prefer archived **plan files** (`aiplans/archived/p<parent>/`) over archived task files (`aitasks/archived/t<parent>/`). Plan files contain the full implementation record; task files are just initial proposals. Only use archived task files as fallback when no corresponding plan exists.
- Child tasks are archived to `aitasks/archived/t<parent>/` preserving the directory structure
- Child plans are archived to `aiplans/archived/p<parent>/` preserving the directory structure
- **IMPORTANT:** When modifying any task file, always update the `updated_at` field in frontmatter to the current date/time using format `YYYY-MM-DD HH:MM`
- **Child task naming:** Use format `t{parent}_{child}_description.md` where both parent and child identifiers are **numbers only**. Do not insert tasks "in-between" (e.g., no `t10_1b` between `t10_1` and `t10_2`). If you discover a missing implementation step, add it as the next available number and adjust dependencies accordingly
- When archiving a task with an `issue` field, the workflow offers to update/close the linked issue using `aitask_issue_update.sh`. The SKILL.md workflow is platform-agnostic; the script handles platform specifics (GitHub, GitLab, etc.). It auto-detects commits and includes "Final Implementation Notes" from the archived plan file.
- **Folded tasks:** When a task has a `folded_tasks` frontmatter field (set by aitask-explore or aitask-fold), the listed tasks are deleted during Step 9 archival. Folded tasks have status `Folded` with a `folded_into` property pointing to the primary task. They are deleted (not archived) because their full content was incorporated into the primary task's description at creation/fold time.
- **Note:** Folded tasks are handled by `handle_folded_tasks()` in both parent and child archival paths. `/aitask-fold` and manual folding can add `folded_tasks` to any task type.
- **Symlinks and data worktree:** When the project uses a separate `aitask-data` branch, `aitasks/` and `aiplans/` are symlinks to `.aitask-data/`. See `repo-structure.md` for the full architecture and rules.

### Project Configuration

Project-level settings are stored in `aitasks/metadata/project_config.yaml` (git-tracked, shared across team). This is separate from execution profiles (workflow behavior) and `userconfig.yaml` (per-user, gitignored).

| Key | Type | Default | Description | Used in |
|-----|------|---------|-------------|---------|
| `verify_build` | string or list | (none — skip) | Shell command(s) to verify the build after implementation | Step 9 |

If the file does not exist or a field is absent, the corresponding feature is skipped.

### Execution Profiles

> **Full reference:** See `profiles.md` for the complete profile schema, available keys, and customization guide.

Profiles are YAML files in `aitasks/metadata/profiles/` that pre-answer workflow questions. Default profiles: **default** (all questions asked) and **fast** (skip confirmations).
