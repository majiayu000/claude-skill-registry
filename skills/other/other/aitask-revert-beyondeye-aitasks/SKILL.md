---
name: aitask-revert
description: Revert changes associated with completed tasks — fully or partially
user-invocable: true
---

## Arguments

- No argument: show task discovery options (Step 1)
- Numeric argument (e.g., `/aitask-revert 42` or `/aitask-revert t42`): skip discovery, go directly to task analysis (Step 2). Both `42` and `t42` are accepted — strip the leading `t` if present.

## Workflow

### Step 0: Select Execution Profile

Execute the **Execution Profile Selection Procedure** (see `.claude/skills/task-workflow/execution-profile-selection.md`).

### Step 1: Task Discovery

**If a task argument was provided** (e.g., `/aitask-revert 42` or `/aitask-revert t42`):
- Parse the argument as the task ID. If the argument starts with `t` or `T`, strip the prefix (e.g., `t42` → `42`)
- Validate the task exists:
  ```bash
  ./.aitask-scripts/aitask_query_files.sh resolve <number>
  ```
  Parse the output: if first line is `NOT_FOUND`, display error and fall through to the discovery options below. If first line is `TASK_FILE:<path>`, use that path. Also check `aitasks/archived/` for archived tasks:
  ```bash
  ./.aitask-scripts/aitask_query_files.sh archived-task <number>
  ```
  Parse: `ARCHIVED_TASK:<path>` means found in archive (filesystem), `ARCHIVED_TASK_TAR_GZ:<entry>` means found in deep archive (old.tar.gz), `NOT_FOUND` means not found.
- If found (active, archived, or in deep archive): First, ensure the task and all its children/plans are extracted from deep archive (no-op if already on filesystem):
  ```bash
  bash .aitask-scripts/aitask_zip_old.sh unpack <number>
  ```
  Then skip to **Step 2** with the resolved task file path.
- If not found: display "Task t\<N\> not found in active or archived tasks." and fall through to discovery options

**Otherwise (no argument):** Present discovery options via `AskUserQuestion`:
- Question: "How would you like to find the task to revert?"
- Header: "Discovery"
- Options:
  - "Browse recent tasks" (description: "List recently implemented tasks from git history")
  - "Search by files" (description: "Select files, then discover which tasks changed them")
  - "Enter task ID" (description: "Type a specific task number directly")

#### Path A: Browse Recent Tasks

Run the analysis script:
```bash
./.aitask-scripts/aitask_revert_analyze.sh --recent-tasks --limit 20
```

Parse the output. Each line has format: `TASK|<id>|<title>|<date>|<commit_count>`

**Pagination loop** (3 tasks per page + "Show more"):
- Start with `current_offset = 0` and `page_size = 3`
- For the current page, take tasks from index `current_offset` to `current_offset + page_size - 1`
- Build `AskUserQuestion` options:
  - For each task in the current page: label = `t<id>: <title>`, description = `<date>, <commit_count> commits`
  - If more tasks beyond this page: add "Show more tasks" (description: "Show next batch (<N> more available)")
- If this is the last page (no "Show more" needed), show up to 4 tasks
- Handle selection:
  - If user selects a task → extract task ID, proceed to **Step 2**
  - If user selects "Show more tasks" → increment `current_offset` by `page_size`, loop back

#### Path B: Search by Files

Read and follow `.claude/skills/user-file-select/SKILL.md` to get file paths. The skill returns a newline-separated list of selected file paths.

After file selection, map files to task IDs:
```bash
./.aitask-scripts/aitask_explain_extract_raw_data.sh --gather <path1> [path2...] --max-commits 50
```

Parse the `RUN_DIR: <path>` line to get the run directory. Read `<run_dir>/reference.yaml` and extract unique task IDs from the commit data (each commit's message contains a `(tN)` or `(tN_M)` tag).

Clean up the run directory:
```bash
./.aitask-scripts/aitask_explain_extract_raw_data.sh --cleanup <run_dir>
```

If no task IDs found: inform user "No tasks found associated with the selected files." and loop back to discovery options.

If task IDs found, present them via paginated `AskUserQuestion` (same pagination pattern as Path A):
- For each task ID: resolve the task file (active or archived), generate a brief summary
- label = `t<id>: <brief summary>`, description = relevant file associations

User selects a task → proceed to **Step 2**.

#### Path C: Enter Task ID

Use `AskUserQuestion`:
- Question: "Enter the task number to revert:"
- Header: "Task ID"
- Options: use "Other" for free text input

Parse the entered number. Validate the task exists (same resolution as direct argument above). If found → proceed to **Step 2**. If not found → inform user and loop back to discovery options.

### Step 2: Task Analysis & Confirmation

Read the task file (may be in `aitasks/` or `aitasks/archived/`). Extract a brief summary of the task description.

Run analysis commands:
```bash
./.aitask-scripts/aitask_revert_analyze.sh --task-commits <id>
./.aitask-scripts/aitask_revert_analyze.sh --task-areas <id>
```

Parse the output:
- `COMMIT|<hash>|<date>|<message>|<insertions>|<deletions>|<task_id>` — each commit
- `AREA|<dir>|<file_count>|<insertions>|<deletions>|<file_list>` — each area

For parent tasks with children: the script automatically includes child task commits. Group commits by `<task_id>` to show per-child breakdown.

**For parent tasks with children**, also run:
```bash
./.aitask-scripts/aitask_revert_analyze.sh --task-children-areas <id>
```

Parse the output:
- `CHILD_HEADER|<child_id>|<child_name>|<commit_count>` — each child task header
- `CHILD_AREA|<child_id>|<dir>|<file_count>|<insertions>|<deletions>|<file_list>` — per-child area
- `PARENT_HEADER|<parent_id>|<commit_count>` — parent-level commits header (if any)
- `PARENT_AREA|<parent_id>|<dir>|<file_count>|<insertions>|<deletions>|<file_list>` — parent-level area
- `NO_CHILDREN` — task has no children (standalone task)

Store the `--task-children-areas` data for use in Step 3b (child-level selection).

**Display summary to user:**
```
## Task t<id>: <task name>
<brief summary>

### Commits (<N> total)
- <hash> (<date>): <message> [+<ins>/-<del>]
- ...

### Areas Affected
- <dir>/ — <file_count> files, +<ins>/-<del>
  Files: <file_list>
- ...

### Per-Child Breakdown (if parent with children)
- t<id>_1 (<name>): <N> commits
  Areas: <dir1>/, <dir2>/
- t<id>_2 (<name>): <N> commits
  Areas: <dir3>/
- Parent-level: <N> commits (if any)
  Areas: <dir4>/
```

Use `AskUserQuestion`:
- Question: "Confirm this is the task to revert?"
- Header: "Confirm"
- Options:
  - "Yes, proceed with revert" (description: "Continue to revert type selection")
  - "Select different task" (description: "Go back to task discovery")
  - "Cancel" (description: "Abort the revert workflow")

- "Yes, proceed" → proceed to **Step 3**
- "Select different task" → go back to **Step 1** (discovery options)
- "Cancel" → end the workflow

### Step 3: Revert Type Selection

Use `AskUserQuestion`:
- Question: "What type of revert do you want?"
- Header: "Revert type"
- Options:
  - "Complete revert" (description: "Revert all changes from this task")
  - "Partial revert" (description: "Select which areas/components to revert and which to keep")

- "Complete revert" → proceed to **Step 3a**
- "Partial revert" → proceed to **Step 3b**

### Step 3a: Complete Revert Path

Ask post-revert disposition via `AskUserQuestion`:
- Question: "After reverting, what should happen to the original task?"
- Header: "Disposition"
- Options:
  - "Delete task and plan" (description: "Remove task and plan files entirely from the archive")
  - "Keep archived" (description: "Keep archived with revert notes added to the task file")
  - "Move back to Ready" (description: "Un-archive and set to Ready with revert notes, for potential re-implementation")

Store the selected disposition. Proceed to **Step 4**.

### Step 3b: Partial Revert Path

**For parent tasks with children** (check: the `--task-children-areas` data from Step 2 was not `NO_CHILDREN`):

First, ask selection mode via `AskUserQuestion`:
- Question: "This is a parent task with children. How do you want to select what to revert?"
- Header: "Selection"
- Options:
  - "By child task" (description: "Select which child tasks to revert — recommended for reverting entire feature slices")
  - "By area" (description: "Select directory areas to revert, then see which child tasks are affected")

#### Mode A: By child task

Present child tasks as `AskUserQuestion` with `multiSelect: true`:
- **If <= 4 items** (children + parent-level commits if present): Show all as multiSelect options
  - Each child: label = `t<child_id> (<name>)`, description = `<commit_count> commits, areas: <area_list>`
  - If parent-level commits exist: add option label = `Parent-level commits`, description = `<N> commits, areas: <area_list>`
- **If > 4 items:** List all children in the question text, then provide options:
  - "All children" (description: "Revert all child tasks")
  - First 2-3 children as individual options
  - Free text via "Other" for comma-separated child IDs (e.g., "398_1, 398_3")
- Question: "Select child tasks to REVERT (unselected will be kept):"
- Header: "Children"

After child selection, **collect per-area commit mapping** for the selected children (same `git diff-tree` logic as the area path below, but only for commits from selected children).

**Show confirmation summary:**

```
## Revert Summary

### Will REVERT:
- t<id>_1 (<name>) — <N> commits, areas: <dir1>/, <dir2>/
- t<id>_3 (<name>) — <N> commits, areas: <dir3>/

### Will KEEP:
- t<id>_2 (<name>) — <N> commits, areas: <dir4>/
```

Use `AskUserQuestion`:
- Question: "Confirm the revert selection?"
- Header: "Confirm"
- Options:
  - "Confirm selection" (description: "Proceed with this revert/keep split")
  - "Adjust selection" (description: "Go back and change which children to revert")
  - "Cancel" (description: "Abort the revert workflow")

- "Confirm" → ask disposition (same `AskUserQuestion` as Step 3a), then proceed to **Step 4**
- "Adjust" → loop back to the child selection above
- "Cancel" → end the workflow

#### Mode B: By area (with child mapping)

Present areas from the `--task-areas` output (collected in Step 2). Use `AskUserQuestion` with `multiSelect: true`:
- Question: "Select the areas to REVERT (unselected areas will be kept):"
- Header: "Areas"
- Options: each area as a selectable option
  - label = `<dir>/` , description = `<file_count> files, +<ins>/-<del>: <truncated file list>`

The user can also type free text via "Other" for more granular specification (e.g., specific files within an area).

**After selection, collect per-area commit mapping:**

For each area selected for revert, identify which commits touch files in that area. Iterate commit hashes from the Step 2 analysis. For each commit, get its file list:
```bash
git diff-tree --no-commit-id -r --name-only <hash>
```
Match files against each area's file list to build the per-area commit mapping.

**Map areas back to children:** Using the `--task-children-areas` data from Step 2, cross-reference selected areas against per-child areas. For each child, determine:
- **Fully affected:** ALL of the child's areas are in the revert selection
- **Partially affected:** SOME of the child's areas are in the revert selection
- **Not affected:** NONE of the child's areas are in the revert selection

**Show confirmation summary with child mapping:**

```
## Revert Summary

### Will REVERT:
- <dir1>/ — <files>, touched by commits: <hash1>, <hash2>
- <dir2>/ — <files>, touched by commits: <hash3>

### Will KEEP:
- <dir3>/ — <files>
- <dir4>/ — <files>

### Child Task Mapping
- t<id>_1 (<name>): FULLY AFFECTED — all areas selected for revert
- t<id>_2 (<name>): PARTIALLY AFFECTED — 1 of 2 areas selected
- t<id>_3 (<name>): NOT AFFECTED — no areas selected
```

Use `AskUserQuestion`:
- Question: "Confirm the revert selection?"
- Header: "Confirm"
- Options:
  - "Confirm selection" (description: "Proceed with this revert/keep split")
  - "Adjust selection" (description: "Go back and change which areas to revert")
  - "Cancel" (description: "Abort the revert workflow")

- "Confirm" → ask disposition (same `AskUserQuestion` as Step 3a), then proceed to **Step 4**
- "Adjust" → loop back to the area selection above
- "Cancel" → end the workflow

#### Standalone tasks (no children)

Present areas from the `--task-areas` output (collected in Step 2). Use `AskUserQuestion` with `multiSelect: true`:
- Question: "Select the areas to REVERT (unselected areas will be kept):"
- Header: "Areas"
- Options: each area as a selectable option
  - label = `<dir>/` , description = `<file_count> files, +<ins>/-<del>: <truncated file list>`

The user can also type free text via "Other" for more granular specification (e.g., specific files within an area).

**After selection, collect per-area commit mapping:**

For each area selected for revert, identify which commits touch files in that area. Iterate commit hashes from the Step 2 analysis. For each commit, get its file list:
```bash
git diff-tree --no-commit-id -r --name-only <hash>
```
Match files against each area's file list to build the per-area commit mapping.

**Show confirmation summary:**

```
## Revert Summary

### Will REVERT:
- <dir1>/ — <files>, touched by commits: <hash1>, <hash2>
- <dir2>/ — <files>, touched by commits: <hash3>

### Will KEEP:
- <dir3>/ — <files>
- <dir4>/ — <files>
```

Use `AskUserQuestion`:
- Question: "Confirm the revert selection?"
- Header: "Confirm"
- Options:
  - "Confirm selection" (description: "Proceed with this revert/keep split")
  - "Adjust selection" (description: "Go back and change which areas to revert")
  - "Cancel" (description: "Abort the revert workflow")

- "Confirm" → ask disposition (same `AskUserQuestion` as Step 3a), then proceed to **Step 4**
- "Adjust" → loop back to the area selection above
- "Cancel" → end the workflow

### Step 4: Create Revert Task

Build a self-contained task description using the data collected. The description must include ALL information needed for a future planning agent to execute the revert without re-running analysis scripts.

**Before building the description**, resolve task and plan file locations:
```bash
bash .aitask-scripts/aitask_revert_analyze.sh --find-task <id>
```
Parse the output: `TASK_LOCATION|<location_type>|<path>` and `PLAN_LOCATION|<location_type>|<path>`. Location types are `active`, `archived`, `tar_gz`, or `not_found`. Use the resolved paths in the disposition instructions below.

**For complete reverts, build the description from this template:**

```markdown
## Revert: Fully revert t<id> (<original task name>)

### Original Task Summary
<1-2 sentence summary of what the task implemented>

### Commits to Revert (newest first)
- `<hash>` (<date>): <commit message>
  Files: <file1> (+N/-M), <file2> (+N/-M)
[one entry per commit from --task-commits, with file details from --task-files]

### Areas Affected
- `<dir>/` — <file_count> files, +<ins>/-<del>: <file_list>
[one entry per area from --task-areas]

### Revert Instructions
1. Analyze each commit and determine revert approach (git revert, manual edits, or hybrid)
2. Handle conflicts with changes made after the original commits
3. Run verification/tests after reverting

### Implementation Transparency Requirements
During the planning/implementation phase for this revert task, the implementing agent MUST:
1. **Before making any changes**, produce a clear summary for user review:
   - For each file that will be modified: what changes will be reverted, what the file will look like after
   - For each file that will be deleted: confirmation it was added entirely by the original task
   - Motivation for each revert action (why it is safe to revert)
2. **Impact analysis**: Identify code in OTHER parts of the project that depends on or references the changes being reverted. List potential breakages and how they will be addressed.
3. **Present this summary to the user for approval BEFORE executing any revert changes.**

### Post-Revert Task Management
- **Disposition:** <delete task and plan | keep archived with revert notes | move back to Ready>
- **Original task file:** `<task_path>` (<location_type>)
- **Original plan file:** `<plan_path>` (<location_type>)

**If disposition is "Delete task and plan":**
1. Delete original task file: `rm <task_path>`
2. Delete original plan file: `rm <plan_path>` (if exists)
3. For parent tasks with archived children: also remove `aitasks/archived/t<id>/` and `aiplans/archived/p<id>/`
4. Commit deletions: `./ait git add <paths> && ./ait git commit -m "ait: Remove reverted task t<id>"`

**If disposition is "Keep archived":**
1. Add a Revert Notes section to the archived task file (`<task_path>`):
   ```
   ## Revert Notes
   - **Reverted by:** t<revert_task_id>
   - **Date:** <YYYY-MM-DD>
   - **Type:** Complete
   - **Areas reverted:** <list of all affected areas>
   ```
2. Commit: `./ait git add <task_path> && ./ait git commit -m "ait: Add revert notes to t<id>"`

**If disposition is "Move back to Ready":**
1. If task is archived, move to active: `mv <task_path> aitasks/`
2. If plan is archived, move to active: `mv <plan_path> aiplans/` (or `aiplans/p<id>/` for children)
3. Update task status: `bash .aitask-scripts/aitask_update.sh --batch <id> --status Ready --assigned-to ""`
4. Add Revert Notes section to the task file:
   ```
   ## Revert Notes
   - **Reverted by:** t<revert_task_id>
   - **Date:** <YYYY-MM-DD>
   - **Type:** Complete
   - **Areas reverted:** <list of all affected areas>
   ```
5. Commit: `./ait git add <paths> && ./ait git commit -m "ait: Un-archive and reset reverted task t<id>"`
```

**For partial reverts, build the description from this template:**

```markdown
## Revert: Partially revert t<id> (<original task name>)

### Original Task Summary
<1-2 sentence summary>

### Areas to REVERT
- `<dir>/` — Files: <file1>, <file2>, ...
  Commits touching this area:
  - `<hash>` (<date>): <message> — <file1> (+N/-M), <file2> (+N/-M)
[per area selected for revert, with cross-referenced commit-to-file mapping]

### Areas to KEEP (do NOT modify)
- `<dir>/` — Files: <file1>, <file2>, ...
[areas the user chose NOT to revert]

### Revert Instructions
1. Only revert changes in the "Areas to REVERT" section
2. Preserve ALL changes in "Areas to KEEP"
3. When a commit touches BOTH reverted and kept areas, manually revert only the relevant hunks (do NOT use git revert for mixed commits)
4. Run verification/tests after reverting

### Implementation Transparency Requirements
During the planning/implementation phase for this revert task, the implementing agent MUST:
1. **Before making any changes**, produce a detailed summary for user review:
   - For each area being reverted: exactly which lines/functions/features will be removed or changed back
   - For each area being kept: confirm no unintended side effects from reverting the other areas
   - Motivation: why each area is safe to revert independently of the kept areas
2. **Cross-area dependency analysis**: Check for imports, function calls, shared state, or config that crosses the boundary between reverted and kept areas. List each dependency and how it will be resolved.
3. **Impact on other project code**: Identify code OUTSIDE the original task's scope that now depends on the changes being reverted (e.g., other tasks built on top of this one, config references, documentation). List potential breakages and mitigation steps.
4. **Present this summary to the user for approval BEFORE executing any revert changes.**

### Post-Revert Task Management
- **Disposition:** <chosen disposition>
- **Original task file:** `<task_path>` (<location_type>)
- **Original plan file:** `<plan_path>` (<location_type>)

**If disposition is "Delete task and plan":**
1. Delete original task file: `rm <task_path>`
2. Delete original plan file: `rm <plan_path>` (if exists)
3. For parent tasks with archived children: also remove `aitasks/archived/t<id>/` and `aiplans/archived/p<id>/`
4. Commit deletions: `./ait git add <paths> && ./ait git commit -m "ait: Remove reverted task t<id>"`

**If disposition is "Keep archived":**
1. Add a Revert Notes section to the archived task file (`<task_path>`):
   ```
   ## Revert Notes
   - **Reverted by:** t<revert_task_id>
   - **Date:** <YYYY-MM-DD>
   - **Type:** Partial
   - **Areas reverted:** <list of reverted areas>
   - **Areas kept:** <list of kept areas>
   ```
2. Commit: `./ait git add <task_path> && ./ait git commit -m "ait: Add revert notes to t<id>"`

**If disposition is "Move back to Ready":**
1. If task is archived, move to active: `mv <task_path> aitasks/`
2. If plan is archived, move to active: `mv <plan_path> aiplans/` (or `aiplans/p<id>/` for children)
3. Update task status: `bash .aitask-scripts/aitask_update.sh --batch <id> --status Ready --assigned-to ""`
4. Add Revert Notes section to the task file:
   ```
   ## Revert Notes
   - **Reverted by:** t<revert_task_id>
   - **Date:** <YYYY-MM-DD>
   - **Type:** Partial
   - **Areas reverted:** <list of reverted areas>
   - **Areas kept:** <list of kept areas>
   ```
5. Commit: `./ait git add <paths> && ./ait git commit -m "ait: Un-archive and reset reverted task t<id>"`
```

**For partial reverts of parent tasks using child-level selection (Mode A), build the description from this template instead:**

```markdown
## Revert: Partially revert t<id> (<original task name>) — by child task

### Original Task Summary
<1-2 sentence summary>

### Children to REVERT
- t<child_id> (<name>): <N> commits
  Areas: <dir1>/, <dir2>/
  Commits:
  - `<hash>` (<date>): <message> — <file1> (+N/-M), <file2> (+N/-M)
[one entry per child selected for revert, with their commits and per-commit file stats]

### Children to KEEP (do NOT modify)
- t<child_id> (<name>): <N> commits
  Areas: <dir3>/
[children NOT selected for revert]

### Parent-level commits (if any)
- <reverted or kept, per user selection>
  Commits:
  - `<hash>` (<date>): <message> — <file1> (+N/-M)

### Revert Instructions
1. Revert ALL changes from children listed in "Children to REVERT"
2. Preserve ALL changes from children listed in "Children to KEEP"
3. When a commit from a reverted child touches files also modified by kept children, manually revert only the reverted child's hunks
4. Run verification/tests after reverting

### Implementation Transparency Requirements
During the planning/implementation phase for this revert task, the implementing agent MUST:
1. **Before making any changes**, produce a detailed summary for user review:
   - For each child being reverted: exactly which lines/functions/features will be removed or changed back
   - For each child being kept: confirm no unintended side effects from reverting the other children
   - Motivation: why each child is safe to revert independently of the kept children
2. **Cross-child dependency analysis**: Check for imports, function calls, shared state, or config that crosses the boundary between reverted and kept children. List each dependency and how it will be resolved.
3. **Impact on other project code**: Identify code OUTSIDE the original task's scope that now depends on the changes being reverted. List potential breakages and mitigation steps.
4. **Present this summary to the user for approval BEFORE executing any revert changes.**

### Post-Revert Task Management
- **Disposition:** <chosen disposition>
- **Original task file:** `<task_path>` (<location_type>)
- **Original plan file:** `<plan_path>` (<location_type>)

<same disposition handling as the standard partial revert template above>

### Per-Child Disposition
For each child task that was reverted, update the archived child task file with Revert Notes:

**Fully reverted children** (all their areas selected for revert):
Add to the archived child task file (resolve path via `--find-task <child_id>`):
   ## Revert Notes
   - **Reverted by:** t<revert_task_id>
   - **Date:** <YYYY-MM-DD>
   - **Type:** Complete (all changes from this child were reverted)
   - **Areas reverted:** <child's area list>

Children that were NOT reverted need no annotation.

Commit all child annotations: `./ait git add <paths> && ./ait git commit -m "ait: Add revert notes to t<id> children"`
```

**For partial reverts of parent tasks using area selection with child mapping (Mode B):**

Use the standard partial revert template above, but append these additional sections after "Areas to KEEP":

```markdown
### Child Task Mapping
The selected areas map to the following child tasks:
- t<child_id> (<name>): FULLY AFFECTED — all areas selected for revert
- t<child_id> (<name>): PARTIALLY AFFECTED — <N> of <M> areas selected
  Areas being reverted: <dir1>/
  Areas being kept: <dir2>/
- t<child_id> (<name>): NOT AFFECTED — no areas selected for revert
```

And append a "Per-Child Disposition" section to the Post-Revert Task Management:

```markdown
### Per-Child Disposition
For each child task that was **fully** or **partially** affected by the area selection, update the archived child task file with Revert Notes:

**Fully affected children** (all their areas in the revert selection):
Add to the archived child task file (resolve path via `--find-task <child_id>`):
   ## Revert Notes
   - **Reverted by:** t<revert_task_id>
   - **Date:** <YYYY-MM-DD>
   - **Type:** Complete (all changes from this child were reverted)
   - **Areas reverted:** <child's area list>

**Partially affected children** (some areas reverted, some kept):
Add to the archived child task file:
   ## Revert Notes
   - **Reverted by:** t<revert_task_id>
   - **Date:** <YYYY-MM-DD>
   - **Type:** Partial
   - **Areas reverted:** <list of this child's reverted areas>
   - **Areas kept:** <list of this child's kept areas>

Children that were NOT affected need no annotation.

Commit all child annotations: `./ait git add <paths> && ./ait git commit -m "ait: Add revert notes to t<id> children"`
```

**Also fetch file-level details for the description:**
```bash
./.aitask-scripts/aitask_revert_analyze.sh --task-files <id>
```
Parse the `FILE|<path>|<insertions>|<deletions>` output to populate per-commit file stats in the templates above.

**Create the task:**
```bash
./.aitask-scripts/aitask_create.sh --batch --commit --name "revert_t<id>" --type refactor --desc-file - <<'TASK_DESC'
<built description from template above>
TASK_DESC
```

Read back the created task file to confirm the assigned task ID:
```bash
git log -1 --name-only --pretty=format:'' | grep '^aitasks/t'
```

### Step 5: Decision Point

**Profile check:** If the active profile has `explore_auto_continue` set to `true`:
- Display: "Profile '\<name\>': continuing to implementation"
- Skip the AskUserQuestion below and proceed directly to the handoff

**Default when `explore_auto_continue` is not defined:** `false` (always ask the user).

Otherwise, use `AskUserQuestion`:
- Question: "Revert task created successfully. How would you like to proceed?"
- Header: "Proceed"
- Options:
  - "Continue to implementation" (description: "Start implementing the revert now via the standard workflow")
  - "Save for later" (description: "Task saved — pick it up later with /aitask-pick <N>")

**If "Save for later":**
- Inform user: "Revert task t\<N\>_revert_t\<original_id\>.md is ready. Run `/aitask-pick <N>` when you want to implement it."
- Execute the **Satisfaction Feedback Procedure** (see `.claude/skills/task-workflow/satisfaction-feedback.md`) with `skill_name` = `"revert"`.
- End the workflow.

**If "Continue to implementation":**
- Proceed to Step 6.

### Step 6: Hand Off to Shared Workflow

Set the following context variables from the created revert task, then read and follow `.claude/skills/task-workflow/SKILL.md` starting from **Step 3: Task Status Checks**:

- **task_file**: Path to the created revert task file (e.g., `aitasks/t420_revert_t106.md`)
- **task_id**: The revert task number (e.g., `420`)
- **task_name**: The filename stem (e.g., `t420_revert_t106`)
- **is_child**: `false` (revert creates standalone tasks)
- **parent_id**: null
- **parent_task_file**: null
- **active_profile**: The execution profile loaded in Step 0 (or null if no profile)
- **active_profile_filename**: The `<filename>` value from the scanner output (e.g., `fast.yaml`), or null if no profile
- **previous_status**: `Ready`
- **folded_tasks**: empty list
- **skill_name**: `"revert"`

---

## Notes

- This skill creates standalone (parent-level) revert tasks, not children
- The analysis backend script is `.aitask-scripts/aitask_revert_analyze.sh` (implemented in t398_1)
- For parent tasks with children, `--task-commits` automatically discovers and includes child task commits
- The revert task description is designed to be self-contained — when picked later, the planning agent has all commit hashes, file lists, area breakdowns, and disposition instructions without re-running analysis
- **Implementation Transparency Requirements** in the task description instruct the implementing agent to present a clear pre-revert summary (what will change, impact analysis, cross-area dependencies) and get user approval before executing any changes
- The `explore_auto_continue` profile key controls the "Continue to implementation" decision point (same as aitask-explore, default: `false`)
- When handing off to task-workflow, the revert task has status `Ready` — task-workflow Step 4 will set it to `Implementing`
- For the full Execution Profiles schema and customization guide, see `.claude/skills/task-workflow/SKILL.md`
