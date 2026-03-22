---
name: aitask-pr-import
description: Create an aitask from a pull request by analyzing PR data and generating a structured task with implementation plan.
user-invocable: true
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

### Step 1: PR Selection

Use `AskUserQuestion` to determine the PR source:
- Question: "How would you like to select the pull request to review?"
- Header: "PR Source"
- Options:
  - "Enter PR number" (description: "Specify a PR/MR number to import and analyze")
  - "Browse open PRs" (description: "List all open PRs and choose one")
  - "Use existing PR data" (description: "Select from previously imported PR data in .aitask-pr-data/")

#### Option: Enter PR number

- Use `AskUserQuestion`:
  - Question: "Enter the PR/MR number to review:"
  - Header: "PR number"
  - Options: free text only (use "Other")
- Run:
  ```bash
  ./.aitask-scripts/aitask_pr_import.sh --batch --pr <num> --data-only --silent
  ```
- The output is the file path (e.g., `.aitask-pr-data/42.md`)
- Read the generated intermediate file from that path

#### Option: Browse open PRs

- Run:
  ```bash
  ./.aitask-scripts/aitask_pr_import.sh --batch --list --silent
  ```
- Parse the output lines. Each line is tab-separated: `<number>\t<title>`
- If no PRs found, inform user and abort
- Present via paginated `AskUserQuestion` (3 PRs per page + "Show more" slot):

  **Pagination loop:**
  - Start with `current_offset = 0` and `page_size = 3`
  - For the current page, take PRs from index `current_offset` to `current_offset + page_size - 1`
  - Build `AskUserQuestion` options:
    - Each PR: label = `#<number> <title>` (truncated to fit), description = "PR #\<number\>"
    - If more PRs exist: add "Show more PRs" option (description: "Show next batch (N more available)")
  - If this is the last page (no "Show more" needed), show up to 4 PRs
  - Handle selection:
    - If user selects a PR → run `./.aitask-scripts/aitask_pr_import.sh --batch --pr <num> --data-only --silent`, read the output path
    - If "Show more PRs" → increment offset, loop back

- Read the generated intermediate file

#### Option: Use existing PR data

- Glob `.aitask-pr-data/*.md` files
- If no files found, inform user: "No existing PR data found. Run `./ait pr-import --batch --pr <num> --data-only` first, or select a different option." Abort or loop back to Step 1.
- Present available files via paginated `AskUserQuestion` (3 per page):
  - For each file: read YAML frontmatter to extract `pr_number` and `title`
  - Label: `#<pr_number> <title>`, description: filename
- Read the selected file

### Step 2: PR Analysis

Read the intermediate data file. It has YAML frontmatter with:
- `pr_number`, `pr_url`, `contributor`, `contributor_email`, `platform`
- `title`, `state`, `base_branch`, `head_branch`
- `additions`, `deletions`, `changed_files`, `fetched_at`

And markdown body sections: Description, Comments, Reviews, Inline Review Comments, Changed Files, Diff.

**Present structured summary to user:**

```
## PR Summary
- **Title:** <title>
- **Author:** <contributor> (<contributor_email>)
- **State:** <state>
- **Branch:** <head_branch> -> <base_branch>
- **Changes:** +<additions> -<deletions> across <changed_files> files
- **URL:** <pr_url>

## Description
<PR description, first 500 chars>

## Key Changes
<List of changed files with brief description of what changed>
```

**Then perform AI analysis covering:**

- **Purpose/Intent:** What is this PR trying to achieve? What problem does it solve?
- **Proposed Solution:** What approach does the PR take? How does it implement the solution?
- **Quality Assessment:** Code quality, test coverage, edge cases, error handling
- **Concerns:** Potential issues, missing tests, breaking changes, security implications
- **Codebase Alignment:** Does the approach match existing patterns and conventions in the project?

To perform the codebase alignment analysis, explore relevant existing code using Glob, Grep, and Read tools. Compare the PR's approach with how similar things are done elsewhere in the codebase.

Present the full analysis to the user.

### Step 3: Interactive Q&A Loop

Same pattern as aitask-explore Step 2:

**Loop:**

1. Use `AskUserQuestion`:
   - Question: "How would you like to proceed?"
   - Header: "Next step"
   - Options:
     - "Continue analyzing" (description: "Ask more questions or explore specific aspects of the PR")
     - "Create task from this PR" (description: "Generate an aitask based on the analysis")
     - "Abort" (description: "Stop without creating a task")

2. Handle selection:
   - **"Continue analyzing":** Allow the user to ask questions about the PR, explore the codebase for comparison, dive deeper into specific files or review comments. Then loop back to present the question again.
   - **"Create task from this PR":** Proceed to Step 4 (Related Task Discovery).
   - **"Abort":** Inform user "PR review ended. No task created." and stop the workflow.

**Notes:**
- Track analysis findings mentally throughout (no file writes during analysis)
- Each analysis round should provide meaningful insights
- Present findings as concise bulleted summaries

### Step 4: Related Task Discovery

Before creating a new task, check for existing pending tasks that overlap with the PR scope. This prevents duplicate tasks and ensures related work is tracked.

**List pending tasks:**

```bash
./.aitask-scripts/aitask_ls.sh -v --status all --all-levels 99 2>/dev/null
```

Filter the output to include only tasks with status `Ready` or `Editing`. Exclude:
- Tasks with children (status shows "Has children") — too complex to fold in
- Child tasks — too complex to fold in
- Tasks with status `Implementing`, `Postponed`, `Done`, or `Folded`

**Assess relevance:** Read the title and brief description (first ~5 lines of body text) of each remaining task. Based on the PR analysis from Steps 2-3, identify tasks whose scope overlaps significantly with the PR. A task is "related" if the new task would cover the same goal, fix the same problem, or implement the same feature.

**If no related tasks are found:** Inform the user: "No existing pending tasks appear related to this PR." Proceed directly to Step 5.

**If related tasks are found:** Present them to the user using `AskUserQuestion` with multiSelect:
- Question: "These existing tasks appear related to this PR. Select any that will be fully covered by the new task (they will be folded in and deleted after implementation):"
- Header: "Related tasks"
- Options: Each related task as a selectable option, with the task filename as label and a brief reason for the match as description. Include a "None — no tasks to fold in" option.

**If user selects "None" or no tasks:** Proceed to Step 5 with no folded tasks.

**If user selects one or more tasks:** Store the list of selected task IDs (e.g., `[106, 129_5]`) as the **folded_tasks** list. Read the full description of each selected task — their content will be incorporated into the new task description in Step 5. Proceed to Step 5.

**Scope rule:** Only standalone parent-level tasks without children may be folded in.

### Step 5: Task Creation

Summarize the PR analysis and propose task metadata:

**Propose task metadata based on the PR analysis:**
- **name:** Sanitized version of PR title (lowercase, underscores, no special chars)
- **priority:** Based on PR scope and urgency (default: medium)
- **effort:** Based on PR complexity (default: medium)
- **issue_type:** Based on PR content (bug, feature, refactor, etc.)
- **labels:** Based on files affected and PR context

Use `AskUserQuestion` to confirm or modify:
- Question: "Here's the proposed task from PR #\<num\>. Confirm or select 'Other' to modify:"
- Header: "Task"
- Options:
  - "Create task as proposed" (description: "<task_name> [priority: <p>, effort: <e>, type: <t>]")
  - "Modify before creating" (description: "Change the title, priority, effort, labels, or description")

**If "Modify before creating":**
- Ask the user what to change via `AskUserQuestion` or free text
- Apply their modifications

**Build the task description incorporating:**

```markdown
## PR Context

- **PR:** #<pr_number> — <title>
- **Author:** @<contributor>
- **URL:** <pr_url>
- **Branch:** <head_branch> -> <base_branch>
- **Changes:** +<additions> -<deletions> across <changed_files> files

## Analysis Summary

### Purpose
<What the PR is trying to achieve>

### Proposed Approach
<How the PR implements the solution — this is a proposal to be verified>

### Concerns and Recommendations
<Issues found, improvements suggested, codebase alignment notes>

## Implementation Approach

<Recommended implementation approach — may differ from the PR's approach based on the analysis>

### Files to Modify
<List of files that need changes, with brief descriptions>

### Testing Requirements
<What tests are needed, how to verify the changes>
```

**If folded_tasks is non-empty:** Execute the **Task Fold Content Procedure** (see `.claude/skills/task-workflow/task-fold-content.md`) with:
- **primary_description:** The task description built from the PR analysis above
- **folded_task_files:** File paths of each selected folded task

Use the returned merged description as the `TASK_DESC` for `aitask_create.sh` below.

**Create the task:**

```bash
./.aitask-scripts/aitask_create.sh --batch --commit \
    --name "<sanitized_pr_title>" \
    --desc-file - \
    --priority "<priority>" \
    --effort "<effort>" \
    --type "<issue_type>" \
    --labels "<labels>" \
    --pull-request "<pr_url>" \
    --contributor "<contributor_username>" \
    --contributor-email "<contributor_email>" <<'TASK_DESC'
<task description (or merged description if folded_tasks is non-empty)>
TASK_DESC
```

- Read back the created task file to confirm the assigned task ID:
  ```bash
  git log -1 --name-only --pretty=format:'' | grep '^aitasks/t'
  ```

**If folded_tasks is non-empty**, execute the **Task Fold Marking Procedure** (see `.claude/skills/task-workflow/task-fold-marking.md`) with:
- **primary_task_num:** `<task_num>` (from the created task)
- **folded_task_ids:** The `folded_tasks` list
- **handle_transitive:** `true`
- **commit_mode:** `"amend"`

### Step 6: Decision Point

**Profile check:** If the active profile has `explore_auto_continue` set to `true`:
- Display: "Profile '\<name\>': continuing to implementation"
- Skip the AskUserQuestion below and proceed directly to the handoff

**Default when `explore_auto_continue` is not defined:** `false` (always ask the user).

Otherwise, use `AskUserQuestion`:
- Question: "Task created successfully. How would you like to proceed?"
- Header: "Proceed"
- Options:
  - "Save for later" (description: "Task saved — pick it up later with /aitask-pick <N>")
  - "Continue to implementation" (description: "Proceed to plan and implement now")

**Note:** Default is "Save for later" (first option) — unlike aitask-explore which defaults to "Continue to implementation". This is intentional: PR-originated tasks typically need more review before implementation.

**If "Save for later":**
- Inform user: "Task t\<N\>_\<name\>.md is ready. Run `/aitask-pick <N>` when you want to implement it."
- End the workflow.

**If "Continue to implementation":**
- Proceed to Step 7.

### Step 7: Hand Off to Shared Workflow

Set the following context variables from the created task, then read and follow `.claude/skills/task-workflow/SKILL.md` starting from **Step 3: Task Status Checks**:

- **task_file**: Path to the created task file (e.g., `aitasks/t42_review_auth_pr.md`)
- **task_id**: The task number (e.g., `42`)
- **task_name**: The filename stem (e.g., `t42_review_auth_pr`)
- **is_child**: `false` (PR review creates standalone parent tasks)
- **parent_id**: null
- **parent_task_file**: null
- **active_profile**: The execution profile loaded in Step 0a (or null if no profile)
- **active_profile_filename**: The `<filename>` value from the scanner output for the selected profile (e.g., `fast.yaml` or `local/fast.yaml`), or null if no profile
- **previous_status**: `Ready`
- **folded_tasks**: List of task IDs folded into this task (e.g., `[106, 129_5]`), or empty list if none
- **skill_name**: `"pr-import"`

---

## Notes

- This skill creates standalone (parent-level) tasks only, not children
- No files are written during the analysis phase — findings are tracked mentally until task creation
- The `explore_auto_continue` profile key controls whether to ask the user about continuing to implementation (default: `false`, always ask)
- When handing off to task-workflow, the created task has status `Ready` — task-workflow's Step 4 will set it to `Implementing`
- For the full Execution Profiles schema and customization guide, see `.claude/skills/task-workflow/SKILL.md`
- **Folded tasks:** Same behavior as aitask-explore. When existing pending tasks are folded into the new task (Step 4), their full content is incorporated using the **Task Fold Content Procedure** (structured `## Merged from t<N>` headers) and marked using the **Task Fold Marking Procedure** (both in `.claude/skills/task-workflow/`). The original folded task files are set to status `Folded` with a `folded_into` property. They exist only as references for deletion after the new task is completed (handled by task-workflow Step 9).
- Only standalone parent-level tasks without children can be folded in
- The `--data-only --silent` flag combination on `aitask_pr_import.sh` outputs just the file path (no success messages)
- The `--list --silent` flag combination outputs `<number>\t<title>` per line (tab-separated, machine-parseable)
- The intermediate data file in `.aitask-pr-data/` has YAML frontmatter with PR metadata and markdown body sections for Description, Comments, Reviews, Inline Review Comments, Changed Files, and Diff
