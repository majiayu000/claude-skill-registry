---
name: aitask-review
description: Review code using configurable review guides, then create tasks from findings.
---

## Workflow

### Step 0a: Select Execution Profile

Execute the **Execution Profile Selection Procedure** (see `.claude/skills/task-workflow/execution-profile-selection.md`).

### Step 0c: Sync with Remote (Best-effort)

Do a best-effort sync to ensure the local state is up to date and clean up stale locks:

```bash
./.aitask-scripts/aitask_pick_own.sh --sync
```

This is non-blocking — if it fails (e.g., no network, merge conflicts), it continues silently.

### Step 1: Review Setup

#### 1a. Target Selection

Use `AskUserQuestion` to determine the review scope:
- Question: "What code areas should be reviewed?"
- Header: "Target"
- Options:
  - "Specific paths" (description: "Enter file paths, directories, or glob patterns via Other")
  - "Recent changes" (description: "Review files changed in specific commits")

**If "Specific paths":** The user enters paths via the "Other" free text input. Parse as space or comma-separated paths. Verify each path exists.

**If "Recent changes":**

1. **Fetch commits using the helper script:**

   ```bash
   ./.aitask-scripts/aitask_review_commits.sh --batch-size 10 --offset 0
   ```

   The script filters out `ait:` administrative commits and returns a pipe-delimited list (one per line):
   ```
   <display_number>|<hash>|<message>|<insertions>|<deletions>
   ```
   The last line is `HAS_MORE|<next_offset>` or `NO_MORE_COMMITS`.

   Display to the user as a numbered list:
   ```
   1. abc1234 Add feature X (+45/-12)
   2. def5678 Fix bug in Y (+3/-1)
   ...
   10. ghi9012 Refactor Z module (+120/-85)
   ```

2. Use `AskUserQuestion`: "Select commits to review:"
   - "Last 5 commits" (description: "Review changes from commits 1-5")
   - "Last 10 commits" (description: "Review changes from commits 1-10")
   - If `HAS_MORE`: "Show 10 more commits" (description: "Load next batch starting from #<next_number>")
   - "Custom selection" (description: "Enter commit indices — ranges (1-5), specific (1,3,5), or mixed (1,2-4,7)")

   If "Show 10 more commits": call the script again with the next offset:
   ```bash
   ./.aitask-scripts/aitask_review_commits.sh --batch-size 10 --offset <next_offset>
   ```
   Append results to the displayed list and re-present the selection. Continue until selection or `NO_MORE_COMMITS`.

3. If "Custom selection": user enters indices via "Other" free text input.
   Parse the input supporting: ranges (e.g., `1-5`), comma-separated (e.g., `1,3,5`), and mixed (e.g., `1, 2-4, 7`).
   Indices refer to the numbered commits displayed across all loaded batches.

4. Resolve selected commit indices to actual commit hashes (from the script output), then get changed files:
   ```bash
   git diff --name-only <oldest_selected_hash>~1...<newest_selected_hash>
   ```
   For non-contiguous selections, union the file lists from each commit:
   ```bash
   git diff-tree --no-commit-id --name-only -r <hash>
   ```

#### 1b. Review Guide Selection

**Auto-detect project environment and rank review guides** using the helper script:

Determine the files to analyze:
- If "Specific paths" was selected: use those paths
- If "Recent changes" was selected: use the changed files list resolved in Step 1a

```bash
echo "<file1>
<file2>
..." | ./.aitask-scripts/aitask_review_detect_env.sh --files-stdin --reviewguides-dir aireviewguides
```

The script uses modular scoring tests (project root markers, file extensions, shebang lines, directory patterns) and returns two sections separated by `---`:

- `ENV_SCORES`: detected environments ranked by confidence score (one per line: `<env>|<score>`)
- `REVIEW_GUIDES`: review guide files pre-sorted by relevance (one per line: `<relative_path>|<name>|<description>|<score_or_universal>`, where `relative_path` is relative to the reviewguides directory, e.g. `general/code_conventions.md`)

Modes are sorted: highest-scoring environment-specific first, then universal, then non-matching environment-specific last.

**Profile check:** If the active profile has `review_default_modes` set (comma-separated list of mode names):
- Auto-select those modes. Display: "Profile '\<name\>': using review guides: \<mode list\>"
- Skip the AskUserQuestion below

Otherwise, present the modes in the script's pre-sorted order via `AskUserQuestion` multiSelect: "Select review guides to apply:"
- Each option: label = `name` field from script output, description = `description` field from script output
- Since `AskUserQuestion` supports max 4 options, implement pagination:
  - Show up to 3 modes per page + "Show more modes" if additional modes exist
  - On the last page, show up to 4 modes
  - Accumulate selections across pages before proceeding

#### 1c. Load Review Instructions

Read the full content of each selected review guide file from `aireviewguides/<relative_path>` (where `<relative_path>` comes from the script output, e.g. `general/code_conventions.md`). The markdown body after the YAML frontmatter contains the review instructions — these become the checklist for the automated review in Step 2.

### Step 2: Automated Review

For each selected review guide:

1. Read its review instructions (the markdown body after frontmatter)
2. Systematically explore the target paths following those instructions:
   - Use Glob to find relevant files within the target scope
   - Use Read to examine file contents
   - Use Grep to search for patterns mentioned in the review instructions
   - Use Task (Explore agents) for broader or deeper investigation when needed
3. Record each finding with:
   - **Mode:** The review guide name (e.g., "Code Conventions")
   - **Severity:** `high`, `medium`, or `low`
   - **Location:** `file_path:line_number`
   - **Description:** What the issue is
   - **Suggested fix:** How to address it

**Severity guidelines:**
- **High:** Security vulnerabilities, data loss risks, correctness bugs, broken functionality
- **Medium:** Code quality issues, missing error handling, performance concerns, inconsistent patterns
- **Low:** Style issues, minor naming inconsistencies, missing documentation, cosmetic improvements

### Step 3: Findings Presentation

**If no findings:** Inform user "No issues found across the selected review guides." and end the workflow.

**If findings exist:** Group findings by review guide, then by severity (high → medium → low). Present as markdown:

```
## Review Findings

### <Mode Name> (N findings)

**High severity:**
1. `file_path:line` — Description. *Suggested fix: ...*

**Medium severity:**
2. `file_path:line` — Description. *Suggested fix: ...*

**Low severity:**
3. `file_path:line` — Description. *Suggested fix: ...*

### <Next Mode> (N findings)
...
```

Then use `AskUserQuestion` multiSelect: "Select findings to address:"
- Since findings may exceed 4, implement pagination:
  - First option: "Select all findings" (description: "Address all N findings")
  - Then list individual findings, 3 per page + "Show more" if needed
  - Each finding option: label = short description, description = `file:line — severity`
  - Accumulate selections across pages

If the user selects no findings: inform "No findings selected. Ending review." and stop.

### Step 4: Task Creation

Use `AskUserQuestion`: "How should the selected findings become tasks?"
- "Single task" (description: "One task with all selected findings in description")
- "Group by review guide" (description: "One task per review guide that had selected findings")
- "Separate tasks" (description: "One task per individual finding")

**Determine priority from findings:** Use the highest severity among selected findings — high severity → `high` priority, medium → `medium`, low → `low`.

**For single task:**

```bash
./.aitask-scripts/aitask_create.sh --batch --commit --name "<sanitized_target>_code_review" \
  --desc-file - --priority <p> --effort <e> --type feature --labels "review" <<'TASK_DESC'
## Code Review Findings

<formatted list of all selected findings with file:line, description, severity, and suggested fix>
TASK_DESC
```

Read back the created task file:
```bash
git log -1 --name-only --pretty=format:'' | grep '^aitasks/t'
```

**For multiple tasks (group by mode or separate):**

1. Create a parent task:
   ```bash
   ./.aitask-scripts/aitask_create.sh --batch --commit --name "<sanitized_target>_code_review" \
     --desc-file - --priority <p> --effort medium --type feature --labels "review" <<'TASK_DESC'
   Code review of <target area>. Child tasks contain individual findings grouped by <mode/finding>.
   TASK_DESC
   ```

2. Read back parent task ID:
   ```bash
   git log -1 --name-only --pretty=format:'' | grep '^aitasks/t'
   ```

3. Create child tasks — for each group (mode or individual finding):
   ```bash
   ./.aitask-scripts/aitask_create.sh --batch --commit --parent <parent_num> --no-sibling-dep \
     --name "<child_name>" --desc-file - --priority <p> --effort <e> --type feature --labels "review" <<'TASK_DESC'
   <findings for this group/finding with file:line, description, severity, and suggested fix>
   TASK_DESC
   ```

### Step 5: Decision Point

**Profile check:** If the active profile has `review_auto_continue` set to `true`:
- Display: "Profile '\<name\>': continuing to implementation"
- Skip the AskUserQuestion below and proceed directly to the handoff

**Default when `review_auto_continue` is not defined:** `false` (always ask the user).

**If single task was created:**

Use `AskUserQuestion`: "Task created successfully. How would you like to proceed?"
- "Continue to implementation" (description: "Start implementing the fixes now via the standard workflow")
- "Save for later" (description: "Task saved — pick it up later with /aitask-pick <N>")

**If multiple tasks (parent + children) were created:**

Use `AskUserQuestion`: "Tasks created. How would you like to proceed?"
- "Pick one to start" (description: "Select a child task to implement now")
- "Save all for later" (description: "Tasks saved — pick them up later with /aitask-pick <parent_N>")

**If "Pick one to start":** Use `AskUserQuestion` to let the user select which child task, then hand off that child.

**If "Save for later" / "Save all for later":**
- Inform user: "Tasks saved. Run `/aitask-pick <N>` when you want to implement."
- End the workflow.

### Step 6: Hand Off to Shared Workflow

When continuing to implementation, set the following context variables from the selected task, then read and follow `.claude/skills/task-workflow/SKILL.md` starting from **Step 3: Task Status Checks**:

- **task_file**: Path to the task file (e.g., `aitasks/t42_codebase_code_review.md` or `aitasks/t42/t42_1_fix_naming.md`)
- **task_id**: The task number (e.g., `42` or `42_1`)
- **task_name**: The filename stem (e.g., `t42_codebase_code_review` or `t42_1_fix_naming`)
- **is_child**: `true` if a child task was selected from a parent+children review, `false` for single task
- **parent_id**: Parent task number if child (e.g., `42`), null otherwise
- **parent_task_file**: Path to parent task file if child (e.g., `aitasks/t42_codebase_code_review.md`), null otherwise
- **active_profile**: The execution profile loaded in Step 0a (or null if no profile)
- **active_profile_filename**: The `<filename>` value from the scanner output for the selected profile (e.g., `fast.yaml` or `local/fast.yaml`), or null if no profile
- **previous_status**: `Ready`
- **folded_tasks**: Empty list (review does not fold tasks)
- **skill_name**: `"review"`

---

## Notes

- This skill creates tasks from code review findings — either a single standalone task or a parent with children
- Review guides are loaded from `aireviewguides/` (tree structure with subdirectories, e.g. `general/`, `python/`, `shell/`; installed via `ait setup`)
- Optional filter file: `aireviewguides/.reviewguidesignore` uses gitignore syntax to exclude specific modes or directories
- The frontmatter format is: `name` (string), `description` (string), `environment` (optional list), `reviewtype` (optional string), `reviewlabels` (optional list), `similar_to` (optional string)
- Metadata vocabulary files (in `aireviewguides/`): `reviewtypes.txt` (classification type), `reviewlabels.txt` (topic labels), `reviewenvironments.txt` (language/framework environments). Use `/aitask-reviewguide-classify` to assign or update metadata on reviewguide files.
- Universal modes have no `environment` field and apply to any project type. Environment-specific modes have `environment` values from `reviewenvironments.txt`.
- Environment auto-detection is handled by `./.aitask-scripts/aitask_review_detect_env.sh` — uses modular scoring tests; modes are sorted by relevance but all are available for selection
- Commit fetching for "Recent changes" is handled by `./.aitask-scripts/aitask_review_commits.sh` — returns paginated, filtered, parseable commit lists
- The `review_default_modes` profile key pre-selects modes (comma-separated names matching the `name` frontmatter field)
- The `review_auto_continue` profile key controls whether to ask about continuing to implementation (default: `false`, always ask)
- When handing off to task-workflow, the created task has status `Ready` — task-workflow's Step 4 will set it to `Implementing`
- For the full Execution Profiles schema and customization guide, see `.claude/skills/task-workflow/SKILL.md`
