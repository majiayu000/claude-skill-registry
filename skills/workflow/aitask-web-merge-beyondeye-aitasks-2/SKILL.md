---
name: aitask-web-merge
description: Merge completed Claude Web branches to main and archive task data.
---

## Overview

This skill runs **locally** after `aitask-pickweb` completes on Claude Code Web. It detects remote branches with completed task executions, merges code to main (excluding `.aitask-data-updated/`), copies the plan to aitask-data, archives the task, and cleans up.

**Workflow:** scan → select → pull → merge → copy plan → archive → push → cleanup

## Workflow

### Step 1: Scan for Completed Branches

Run the helper script to detect branches with completion markers:

```bash
./.aitask-scripts/aitask_web_merge.sh --fetch
```

**If output is `NONE`:** Inform user "No completed Claude Web branches found." and end the workflow.

**If completions found:** For each `COMPLETED:<branch>:<marker>` line, read the full completion marker JSON:

```bash
git show origin/<branch>:.aitask-data-updated/<marker>
```

Parse the JSON to extract: `task_id`, `task_file`, `plan_file`, `is_child`, `parent_id`, `issue_type`, `implemented_with` (if present), `completed_at`, `branch`.

Build a list of candidate branches with this metadata.

### Step 2: Select Branch

**If only one branch found:** Auto-select it and display: "Found 1 completed branch: `<branch>` (t`<task_id>`, `<issue_type>`, completed `<completed_at>`). Proceeding."

**If multiple branches found:** Use `AskUserQuestion` with pagination (3 per page + "Show more"):
- Question: "Select a completed Claude Web branch to merge:"
- Header: "Branch"
- Options:
  - Each branch: label = branch name, description = "t\<task_id\> (\<issue_type\>) completed \<completed_at\>"
  - "Process all sequentially" (description: "Merge all completed branches one by one")

If "Process all" is selected, process each branch in sequence using Steps 3-6.

### Step 3: Pull Latest Main and Merge Code

For the selected branch:

**3a. Pull latest main:**

```bash
git pull --ff-only
```

If pull fails (diverged history), use `AskUserQuestion`:
- Question: "Failed to fast-forward main. Local main has diverged from remote. How to proceed?"
- Header: "Pull"
- Options:
  - "Pull with merge" (description: "Run git pull to merge remote changes")
  - "Abort" (description: "Stop the workflow, resolve manually")
If "Pull with merge": run `git pull`. If that fails too, abort.
If "Abort": end the workflow.

**3b. Merge the web branch (excluding `.aitask-data-updated/`):**

```bash
git merge origin/<branch> --no-ff --no-commit
```

If merge conflicts occur, use `AskUserQuestion`:
- Question: "Merge conflicts detected. How to proceed?"
- Header: "Conflict"
- Options:
  - "Resolve manually" (description: "I'll resolve conflicts, then tell you to continue")
  - "Abort merge" (description: "Run git merge --abort and skip this branch")
If "Abort merge": run `git merge --abort` and skip to the next branch (or end workflow).
If "Resolve manually": wait for user to resolve, then continue.

**3c. Remove `.aitask-data-updated/` from the merge:**

```bash
git rm -rf .aitask-data-updated/ 2>/dev/null || true
```

**3d. Commit the clean merge:**

Derive a description from the task filename (strip `t<N>_` prefix and `.md` suffix, replace underscores with spaces).

```bash
git commit -m "<issue_type>: <description> (t<task_id>)"
```

### Step 4: Copy Plan to aitask-data

**4a. Read the plan from the remote branch:**

```bash
git show origin/<branch>:.aitask-data-updated/plan_t<task_id>.md
```

**4b. Determine the plan file path:**

Derive the plan filename from the task filename in the completion marker:
- Take the task file basename (e.g., `t227_2_create_aitaskwebmerge_skill.md`)
- Replace the leading `t` with `p` (e.g., `p227_2_create_aitaskwebmerge_skill.md`)

Determine the target directory:
- **Parent task** (task_id has no underscore): `aiplans/`
- **Child task** (task_id like `227_2`): `aiplans/p<parent>/` (e.g., `aiplans/p227/`)

```bash
mkdir -p <target_directory>
```

**4c. Write the plan file** to the target path using the Write tool.

**4d. Commit the plan to aitask-data:**

```bash
./ait git add <plan_file_path>
./ait git commit -m "ait: Add web-completed plan for t<task_id>"
```

### Step 5: Apply Agent Attribution and Archive Task

**If `implemented_with` is present in the completion marker JSON:**

```bash
./.aitask-scripts/aitask_update.sh --batch <task_id> --implemented-with "<implemented_with>" --silent
```

**Run the archive script:**

```bash
./.aitask-scripts/aitask_archive.sh <task_id>
```

**Parse structured output and handle each line:**

- `ISSUE:<task_num>:<issue_url>` — Execute the **Issue Update Procedure** below for this task
- `PARENT_ISSUE:<task_num>:<issue_url>` — Execute the **Issue Update Procedure** for the parent task
- `PARENT_ARCHIVED:<path>` — Inform user: "All child tasks complete! Parent task also archived."
- `COMMITTED:<hash>` — Note the commit hash
- `ARCHIVED_TASK:<path>` / `ARCHIVED_PLAN:<path>` — Informational, display to user

### Step 6: Push and Cleanup

**6a. Push main:**

```bash
git push
```

**6b. Push aitask-data:**

```bash
./ait git push
```

**6c. Delete the remote branch:**

```bash
git push origin --delete <branch>
```

**6d. Inform user:** "Branch `<branch>` merged, task t`<task_id>` archived, remote branch deleted."

**6e. Process next branch (if applicable):**

If multiple branches were detected in Step 1 and "Process all" was selected (or more branches remain), loop back to **Step 3** for the next branch.

Otherwise, if other unprocessed branches remain, use `AskUserQuestion`:
- Question: "Merge complete. There are \<N\> more completed branches. Process the next one?"
- Header: "Continue"
- Options:
  - "Yes, process next" (description: "Continue with the next completed branch")
  - "Done for now" (description: "Stop processing branches")

### Step 7: Satisfaction Feedback

Execute the **Satisfaction Feedback Procedure** (see `.claude/skills/task-workflow/satisfaction-feedback.md`) with `skill_name` = `"web-merge"`.

---

## Issue Update Procedure

When a task or parent task has a linked issue (from archive script output):

Use `AskUserQuestion`:
- Question: "Task t\<N\> has a linked issue: \<issue_url\>. Update/close it?"
- Header: "Issue"
- Options:
  - "Close with notes" (description: "Post implementation notes + commits as comment and close")
  - "Comment only" (description: "Post implementation notes but leave open")
  - "Close silently" (description: "Close without posting a comment")
  - "Skip" (description: "Don't touch the issue")

If "Close with notes":
```bash
./.aitask-scripts/aitask_issue_update.sh --close <task_num>
```

If "Comment only":
```bash
./.aitask-scripts/aitask_issue_update.sh <task_num>
```

If "Close silently":
```bash
./.aitask-scripts/aitask_issue_update.sh --close --no-comment <task_num>
```

If "Skip": do nothing.

---

## Notes

- This skill is **interactive** (uses `AskUserQuestion`) — designed for local execution, not Claude Web
- The helper script `aitask_web_merge.sh` handles branch detection; this SKILL.md handles merge/archive orchestration
- `.aitask-data-updated/` is intentionally NOT gitignored — it's committed on the web branch and explicitly removed during merge
- The `--no-ff --no-commit` merge approach avoids `--amend` while keeping the merge commit clean
- `aitask_archive.sh` handles all archival mechanics (metadata update, file moves, lock release, parent auto-archival, git commit)
- Plan filename derivation: replace leading `t` with `p` in the task filename
- For the web-side workflow that produces the branches this skill processes, see `aitask-pickweb`
