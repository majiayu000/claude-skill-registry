---
name: aitask-create
description: Create a new AI task file with automatic numbering and proper metadata. Supports interactive agent prompts, terminal fzf, and batch mode.
---

## Workflow

### Step 1: Check for Parent Task Selection (Optional)

First, list existing active tasks to see if the user wants to create a child task:

```bash
./.aitask-scripts/aitask_ls.sh -v -s all 99
```

Use `AskUserQuestion`:
- Question: "Should this be a child task of an existing task?"
- Options:
  - "No, create standalone task (Recommended)" (description: "Create a new top-level task")
  - List each active task as an option with format "t<N> - <name>" (description: "Create as child of this task")

**If parent task selected:**
- Store the parent task number
- Get the next child number by querying all children (active + archived):
  ```bash
  ./.aitask-scripts/aitask_query_files.sh all-children <parent>
  ```
  Parse the output: `CHILD:<path>` lines are active children, `ARCHIVED_CHILD:<path>` lines are archived children. Extract child numbers from all paths (e.g., `t10_2_name.md` → `2`), find the highest, and add 1. If output is `NO_CHILDREN`, next child number is 1.
- Display: "Next child task will be: t<parent>_<child>"

**If standalone task:**
- Proceed with Step 2

### Step 2: Create Draft (No Network Needed)

Create the draft directory if needed:
```bash
mkdir -p aitasks/new
```

The task will be created as a **draft** in `aitasks/new/` with a timestamp-based filename. The real task number is assigned later during finalization (Step 8), which requires network access.

Draft filename format: `draft_<YYYYMMDD_HHMM>_<sanitized_name>.md`

Display to user: "Task will be created as a draft. Real task ID assigned on finalization."

### Step 3: Get Task Metadata from User

Use the `AskUserQuestion` tool to gather task metadata:

**3a. Priority:**
- Question: "What is the priority of this task?"
- Options:
  - "High" (description: "Critical or time-sensitive task")
  - "Medium" (description: "Normal priority task")
  - "Low" (description: "Nice-to-have, can wait")

**3b. Effort:**
- Question: "What is the estimated effort for this task?"
- Options:
  - "Low" (description: "Quick task, less than a few hours")
  - "Medium" (description: "Moderate effort, up to a day")
  - "High" (description: "Significant effort, multiple days")

**3c. Dependencies:**
First, list existing active tasks (and siblings if creating a child):
```bash
./.aitask-scripts/aitask_ls.sh -v 99
```

For child tasks, also list siblings:
```bash
./.aitask-scripts/aitask_query_files.sh active-children <parent>
```
Parse the output: `CHILD:<path>` lines list active sibling task files. If output is `NO_CHILDREN`, there are no existing siblings.

Then use `AskUserQuestion`:
- Question: "Does this task depend on any existing tasks? Select all that apply, or choose 'None' for no dependencies."
- Options: List siblings first (if child task), then parent-level tasks, plus "None" option
- multiSelect: true (allow multiple selections)

**3d. Sibling Dependency (Child Tasks Only):**
If creating a child task (t<parent>_<N> where N > 1):

Use `AskUserQuestion`:
- Question: "Should this task depend on the previous sibling (t<parent>_<N-1>)?"
- Options:
  - "Yes (Recommended)" (description: "Sequential dependency on previous sibling")
  - "No" (description: "This task can run in parallel with siblings")

If "Yes", add t<parent>_<N-1> to the dependencies.

**Validation:** Only accept task numbers that correspond to existing active tasks.

### Step 4: Get Task Name

Use `AskUserQuestion`:
- Question: "Enter a short name for this task (will be used in filename):"
- Input type: Free text (use "Other" option)

**Sanitize the name:**
1. Convert to lowercase
2. Replace spaces with underscores
3. Replace multiple consecutive underscores with single underscore
4. Remove special characters (keep only a-z, 0-9, and underscores)
5. Trim leading/trailing underscores
6. Truncate to maximum 50 characters

Display to user: "Draft file will be: aitasks/new/draft_<timestamp>_<sanitized_name>.md"

### Step 5: Get Task Definition (Iterative)

Collect the task definition iteratively, asking after each chunk if the user wants to add more or insert file references.

**5a. Initial prompt:**
Use `AskUserQuestion`:
- Question: "Enter the task definition (first part). What should be done?"
- Input type: Free text (use "Other" option)

**5b. Continue loop:**
After receiving input, use `AskUserQuestion`:
- Question: "What would you like to do next?"
- Options:
  - "Add more text" (description: "Continue entering task definition")
  - "Insert file reference" (description: "Search for a file and insert its path")
  - "Done" (description: "Finish and create the task file")

**5c. If "Add more text":**
Use `AskUserQuestion`:
- Question: "Enter additional content for the task definition:"
- Input type: Free text (use "Other" option)

Then repeat step 5b.

**5d. If "Insert file reference":**

**5d-i. Get search pattern:**
Use `AskUserQuestion`:
- Question: "Enter partial filename to search for (e.g., 'auth', 'Main', 'screen'):"
- Input type: Free text (use "Other" option)

**5d-ii. Search for matching files:**
Use the `Glob` tool to find matching files:
```
Pattern: **/*<user_input>*
```

**5d-iii. Present results:**
If matches found (limit to first 10-15 results):
- Use `AskUserQuestion` to present matching files as options
- Question: "Select a file to insert:"
- Options: List each matching file path, plus "Search again" and "Cancel" options

If no matches found:
- Inform user: "No files found matching '<pattern>'"
- Ask if they want to try a different search term or cancel

**5d-iv. Insert selected file:**
- Append the selected file path to the current task description
- Display: "Added: <file_path>"
- Return to step 5b (continue loop)

**5e. If "Done":**
Concatenate all collected text chunks and file references with newline separators and proceed to Step 6.

### Step 6: Create Draft Task File

Write the draft file to `aitasks/new/draft_<YYYYMMDD_HHMM>_<name>.md`.

**File format (YAML front matter):**
```yaml
---
priority: <priority>
effort: <effort>
depends: [<dependencies>]
issue_type: feature
status: Ready
labels: []
draft: true
created_at: <YYYY-MM-DD HH:MM>
updated_at: <YYYY-MM-DD HH:MM>
---

<task definition content>
```

For child tasks, also include `parent: <parent_num>` in the frontmatter.

Where:
- `<priority>` = `high`, `medium`, or `low`
- `<effort>` = `low`, `medium`, or `high`
- `<dependencies>` = comma-separated task IDs

### Step 7: Update Parent Task (Child Tasks Only - Deferred)

For child tasks, the parent's `children_to_implement` is updated during finalization (Step 8), not here.

### Step 8: Finalize Draft (Assign Real ID & Commit)

Use the `aitask_create.sh` script to finalize the draft:

```bash
./.aitask-scripts/aitask_create.sh --batch --finalize draft_<timestamp>_<name>.md
```

This will:
1. Claim a globally unique task ID from the atomic counter (requires network)
2. Rename the file from `draft_*_<name>.md` to `t<N>_<name>.md`
3. Move from `aitasks/new/` to `aitasks/` (or `aitasks/t<parent>/` for child tasks)
4. Remove the `draft: true` field from frontmatter
5. Update parent's `children_to_implement` (if child task)
6. Stage and commit to git

If finalization fails (e.g., no network), the draft is preserved in `aitasks/new/` for later finalization.

### Step 9: Confirm Completion

Display a summary to the user:
- Task ID: t<number> (or t<parent>_<child>)
- Parent: t<parent> (if child task)
- Filename: `<filepath>`
- Priority: <priority>
- Effort: <effort>
- Dependencies: <list or "None">
- Git commit: <commit hash>

Optionally ask if the user wants to immediately start working on this task using `/aitask-pick <task_id>`.

## Edge Cases

### Task Number Already Exists
The atomic counter guarantees unique IDs. If the counter branch is not initialized, the fallback local scan will detect conflicts.

### Empty Task Definition
If the user provides no content, prompt them that a task definition is required before proceeding.

### Invalid Dependency Numbers
If the user enters a dependency number that doesn't correspond to an existing active task, warn them and ask to re-enter.

### Name Sanitization Results in Empty String
If sanitization removes all characters, use "unnamed_task" as the default name.

### Parent Task Doesn't Exist
If creating a child task and the parent doesn't exist, show an error and ask to select a different parent.

### Finalization Fails
If `--finalize` fails (no network, no counter branch), inform user: "Draft saved to aitasks/new/. Finalize later with `ait create` (interactive) or `./.aitask-scripts/aitask_create.sh --batch --finalize <file>`."

## Notes

- Use the YAML front matter format for metadata
- Dependencies should only reference active (non-archived) tasks
- For child tasks, sibling dependencies use the format `t<parent>_<sibling>` (e.g., `t1_2`)
- Draft tasks are created locally in `aitasks/new/` (gitignored) - no network needed
- Real task IDs are assigned during finalization via the atomic counter on the `aitask-ids` branch
- Child tasks are stored in `aitasks/t<parent>/` subdirectory after finalization

## Batch Mode (Non-Interactive)

For non-interactive task creation (e.g., when creating child tasks during planning), use the batch script directly:

```bash
./.aitask-scripts/aitask_create.sh --batch --name "<name>" --desc "<description>" --commit
```

Flags:
- `--batch` — Enable batch mode (required)
- `--name, -n NAME` — Task name (required, will be sanitized)
- `--desc, -d DESC` — Task description
- `--desc-file FILE` — Read description from file (use `-` for stdin)
- `--priority, -p LEVEL` — high/medium/low (default: medium)
- `--effort, -e LEVEL` — low/medium/high (default: medium)
- `--type, -t TYPE` — Issue type (default: feature)
- `--status, -s STATUS` — Ready/Editing/Implementing/Postponed (default: Ready)
- `--labels, -l LABELS` — Comma-separated labels
- `--deps DEPS` — Comma-separated dependency task numbers
- `--assigned-to, -a EMAIL` — Email of person assigned to task
- `--issue URL` — Issue tracker URL
- `--parent, -P NUM` — Create as child of specified parent task
- `--no-sibling-dep` — Skip default sibling dependency
- `--commit` — Auto-finalize with real ID (requires network)
- `--finalize FILE` — Finalize a specific draft from `aitasks/new/`
- `--finalize-all` — Finalize all drafts in `aitasks/new/`
- `--silent` — Output only the created filename (for scripting)

Examples:
```bash
# Create a standalone task (auto-finalize)
./.aitask-scripts/aitask_create.sh --batch --name "fix_login" --desc "Fix login bug" --priority high --type bug --commit

# Create first child of task t10
./.aitask-scripts/aitask_create.sh --batch --parent 10 --name "first_subtask" --desc "First subtask" --commit

# Create child without auto sibling dependency
./.aitask-scripts/aitask_create.sh --batch --parent 10 --name "parallel_task" --desc "Parallel work" --no-sibling-dep --commit

# Create as draft (no network needed), finalize later
./.aitask-scripts/aitask_create.sh --batch --name "add_feature" --desc "Add new feature"

# Read description from stdin
echo "Long description here" | ./.aitask-scripts/aitask_create.sh --batch --name "my_task" --desc-file -
```
