---
name: aitask-pick
description: Select the next AI task for implementation from the `aitasks/` directory.
---

## Workflow

### Step 0a: Select Execution Profile

Execute the **Execution Profile Selection Procedure** (see `.claude/skills/task-workflow/execution-profile-selection.md`).

### Step 0b: Check for Direct Task Selection (Optional Argument)

**IMPORTANT:** Step 0a (profile selection) MUST complete before Step 0b begins. Step 0b's behavior depends on the profile (e.g., `skip_task_confirmation`). Do NOT parallelize these steps.

If this skill is invoked with a numeric argument:

**Format 1: Parent task (e.g., `/aitask-pick 16`):**
- Parse the argument as the task number
- Find the matching task file and check for children in a single call:
  ```bash
  ./.aitask-scripts/aitask_query_files.sh resolve <number>
  ```
  Parse the output: if first line is `NOT_FOUND`, the task file does not exist (fall through to error). If first line is `TASK_FILE:<path>`, use that path. If second line is `HAS_CHILDREN:<count>`, the task has children — proceed to **Step 2d**. If `NO_CHILDREN`, proceed normally.
  - If it has children → proceed to **Step 2d** (Child Task Selection)
  - If no children:
    - **Show task summary and confirm:**
      - Read the task file content
      - Generate a brief 1-2 sentence summary of the task description
      - **Profile check:** If the active profile has `skip_task_confirmation` set to `true`:
        - Display: "Profile '\<name\>': auto-confirming task selection"
        - Skip the AskUserQuestion below and proceed directly to **Step 3** (Task Status Checks)

        Otherwise, use `AskUserQuestion`:
        - Question: "Is this the correct task? Brief summary: <1-2 sentence summary of the task>"
        - Header: "Confirm task"
        - Options: "Yes, proceed" (description: "This is the correct task, continue with aitask-pick workflow") / "No, abort" (description: "Wrong task, cancel the selection")
      - If "Yes, proceed" → proceed to **Step 3** (Task Status Checks)
      - If "No, abort" → fall back to normal task selection (proceed to Step 1)

**Format 2: Child task (e.g., `/aitask-pick 16_2`):**
- Parse as child task ID (parent=16, child=2)
- Find the matching child task file:
  ```bash
  ./.aitask-scripts/aitask_query_files.sh child-file <parent> <child>
  ```
  Parse the output: `CHILD_FILE:<path>` means found (use that path), `NOT_FOUND` means not found.
- If found:
  - Set this as the selected task
  - Read the task file and parent task for context
  - **Gather archived sibling context** in a single call:
    ```bash
    ./.aitask-scripts/aitask_query_files.sh sibling-context <parent>
    ```
    Parse the output: lines prefixed `ARCHIVED_PLAN:` are archived sibling plan files (primary context source for completed siblings). Lines prefixed `ARCHIVED_TASK:` are fallback for siblings without archived plans. Lines prefixed `PENDING_SIBLING:` are pending sibling task files. Lines prefixed `PENDING_PLAN:` are pending sibling plans. If output is `NO_CONTEXT`, there are no sibling context files. Read the files listed in the output.
  - **Show task summary and confirm:**
    - Generate a brief 1-2 sentence summary of the child task description, mentioning the parent task name for context
    - **Profile check:** If the active profile has `skip_task_confirmation` set to `true`:
      - Display: "Profile '\<name\>': auto-confirming task selection"
      - Skip the AskUserQuestion below and proceed directly to **Step 3** (Task Status Checks)

      Otherwise, use `AskUserQuestion`:
      - Question: "Is this the correct task? Brief summary: <1-2 sentence summary of the child task> (Parent: <parent task name>)"
      - Header: "Confirm task"
      - Options: "Yes, proceed" (description: "This is the correct task, continue with aitask-pick workflow") / "No, abort" (description: "Wrong task, cancel the selection")
    - If "Yes, proceed" → proceed to **Step 3** (Task Status Checks)
    - If "No, abort" → fall back to normal task selection (proceed to Step 1)

**If no file is found:**
- Display error message
- Fall back to normal task selection (proceed to Step 1)

If no argument is provided, proceed with Step 1 as normal.

### Step 0c: Sync with Remote (Best-effort)

Before listing tasks, do a best-effort sync to ensure the local task list is up to date (prevents picking a task that another PC already started) and clean up stale locks:

```bash
./.aitask-scripts/aitask_pick_own.sh --sync
```

This is non-blocking — if it fails (e.g., no network, merge conflicts), it continues silently.

### Step 1: Label Filtering (Optional)

Before retrieving tasks, ask the user if they want to filter by labels.

- Read available labels from `aitasks/metadata/labels.txt`
- Use `AskUserQuestion` with multiSelect:
  - Question: "Do you want to filter tasks by specific labels? (Select labels to include, or skip to show all)"
  - Header: "Labels"
  - Options: List each label from labels.txt, plus "Show all tasks (no filter)"
- If labels selected, pass them to the task listing command using `-l label1,label2`

### Step 2: List and Select Task

#### 2a: Get Top Tasks

Run the task selection script to get the top 15 prioritized **parent** tasks:

```bash
./.aitask-scripts/aitask_ls.sh -v 15
```

If labels were selected in Step 1:
```bash
./.aitask-scripts/aitask_ls.sh -v -l label1,label2 15
```

**Note:** This only shows parent-level tasks, not children. Parent tasks with pending children will show as "Has children" and can be selected to drill down into child tasks.

The output format with `-v` is:
```
t<number>_<name>.md [Status: <status>, Priority: <priority>, Effort: <effort>]
```

#### 2b: Generate Task Summaries

For each task returned by the script:

- Read the corresponding task file from `aitasks/<filename>`
- Check if it has children:
  ```bash
  ./.aitask-scripts/aitask_query_files.sh has-children <number>
  ```
  Parse the output: `HAS_CHILDREN:<count>` means it has children (include the count), `NO_CHILDREN` means none.
- Generate a brief summary including child count if applicable
- Present each task in this format:

```
<filename> [Priority: <priority>, Effort: <effort>, Status: <status>]
<brief summary of task content>
Children: <N children pending> (or "None")
___________
```

#### 2c: Ask User to Select Task

**Note:** This sub-step is skipped if a task number was provided as an argument in Step 0b.

Since `AskUserQuestion` supports a maximum of 4 options, implement pagination to show all available tasks:

**Pagination loop:**

- Start with `current_offset = 0` and `page_size = 3` (3 tasks per page + 1 "Show more" slot).

- For the current page, take tasks from index `current_offset` to `current_offset + page_size - 1`.

- Build `AskUserQuestion` options:
  - For each task in the current page slice: option label = task filename, description = brief summary with metadata
  - If there are more tasks beyond this page: add a **"Show more tasks"** option (description: "Show next batch of tasks (N more available)")

- Present options via `AskUserQuestion`.

- Handle selection:
  - If user selects a task → proceed to Step 2d (if parent with children) or Step 3
  - If user selects "Show more tasks" → increment `current_offset` by `page_size`, loop back to building the page options
  - If this is the last page (no "Show more" needed), show up to 4 tasks instead of 3

#### 2d: Child Task Selection (For Parent Tasks with Children)

If the selected task is a parent task with children in `aitasks/t<N>/`:

- List all child tasks:
  ```bash
  ./.aitask-scripts/aitask_ls.sh -v --children <parent_num> 99
  ```

- Read each child task file for summaries

- Use `AskUserQuestion`:
  - Question: "This is a parent task with child subtasks. Select which to work on:"
  - Options:
    - Each ready (unblocked) child task with brief summary
    - "Work on parent directly" (only if all children are complete)

- If child selected:
  - Set child as the working task
  - **Gather sibling context** (archived + pending) in a single call:
    ```bash
    ./.aitask-scripts/aitask_query_files.sh sibling-context <parent>
    ```
    Parse the output and read files listed. `ARCHIVED_PLAN:` files are the primary reference for completed siblings. `ARCHIVED_TASK:` files are fallback. `PENDING_SIBLING:` and `PENDING_PLAN:` are pending sibling context. Include parent task file in context as well.
  - Proceed to Step 3

### Step 3: Hand Off to Shared Workflow

At this point, a task has been selected and confirmed. Set the following context variables, then read and follow `.claude/skills/task-workflow/SKILL.md` starting from **Step 3: Task Status Checks**:

- **task_file**: Path to the selected task file (e.g., `aitasks/t16_implement_auth.md` or `aitasks/t10/t10_2_add_login.md` for child tasks)
- **task_id**: The task identifier extracted from the filename (e.g., `16` or `16_2`)
- **task_name**: The full stem from the filename used for branches/worktrees (e.g., `t16_implement_auth` or `t16_2_add_login`)
- **is_child**: `true` if a child task was selected (from Step 2d or Step 0b with parent_child format), `false` otherwise
- **parent_id**: The parent task number if `is_child` is true (e.g., `16`), otherwise null
- **parent_task_file**: Path to the parent task file if `is_child` is true (e.g., `aitasks/t16_implement_auth.md`), otherwise null
- **active_profile**: The execution profile loaded in Step 0a (or null if no profile)
- **active_profile_filename**: The `<filename>` value from the scanner output for the selected profile (e.g., `fast.yaml` or `local/fast.yaml`), or null if no profile
- **previous_status**: `Ready` (the status the task had before being picked)
- **skill_name**: `"pick"`

---

## Notes

- This skill uses the project's `aitask_ls.sh` script for task prioritization
- Parent tasks with pending children show as "Has children" and are sorted normally by priority/effort
- The `--children` flag of `aitask_ls.sh` lists only children of a specific parent
- When invoked with a child task argument (e.g., `/aitask-pick 10_2`), the skill goes directly to that child task
- For the full Execution Profiles schema, shared workflow notes, and customization guide, see `.claude/skills/task-workflow/SKILL.md`
