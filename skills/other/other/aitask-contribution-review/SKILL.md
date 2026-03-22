---
name: aitask-contribution-review
description: Analyze a contribution issue, find related issues, and import as grouped or single task.
user-invocable: true
arguments: "<issue_number>"
---

## Workflow

### Step 0: Resolve Issue Number

**If `<issue_number>` argument is provided:** Use it directly and proceed to Step 1.

**If no argument is provided:** List open contribution issues using the platform-encapsulated script:

```bash
./.aitask-scripts/aitask_contribution_review.sh list-issues
```

Parse the structured output blocks:
- `@@@ISSUE:<num>@@@` — Issue separator
- `TITLE:<title>` — Issue title
- `HAS_METADATA:true|false` — Whether issue has aitask-contribute-metadata

**If output is `NO_ISSUES`:** Inform user "No open contribution issues found." and end the workflow.

**Filter** to only issues with `HAS_METADATA:true` (these are actual contribution issues).

**If no issues have metadata:** Inform user "No contribution issues with metadata found among open issues." and end the workflow.

**Present the filtered issues** via `AskUserQuestion`:
- Question: "Which contribution issue should I review?"
- Header: "Issue"
- Options: Each contribution issue (label: `#<num> — <short_title>`, description: full title)

Use the selected issue number as `<issue_number>` for Step 1.

**IMPORTANT:** Do NOT call `gh`, `glab`, `curl`, or any platform-specific CLI commands directly. Always use the `aitask_contribution_review.sh` script subcommands, which encapsulate platform detection and work on GitHub, GitLab, and Bitbucket.

### Step 1: Validate and Fetch Target Issue

Fetch the target issue using the helper script (encapsulates platform detection and API access):

```bash
./.aitask-scripts/aitask_contribution_review.sh fetch <issue_number>
```

Parse the structured output lines:
- `ISSUE_JSON:<json>` — Full issue JSON including comments
- `HAS_METADATA:true|false` — Whether the issue has `aitask-contribute-metadata`
- `CONTRIBUTOR:<name>` — Contributor username
- `EMAIL:<email>` — Contributor email
- `AREAS:<csv>` — Affected code areas
- `FILE_PATHS:<csv>` — Changed file paths
- `FILE_DIRS:<csv>` — Changed directories
- `CHANGE_TYPE:<type>` — Type of change

**If `HAS_METADATA:false`:** Inform user "Issue #N is not a contribution issue (no aitask-contribute-metadata found)" and abort.

**Display summary:**
```
## Contribution Issue #<N>
- **Title:** <from JSON>
- **Contributor:** <name> (<email>)
- **Areas:** <areas>
- **Change type:** <type>
- **Files:** <file_paths>
```

### Step 1b: Check for Duplicate Import

Check if this issue has already been imported as a task:

```bash
./.aitask-scripts/aitask_contribution_review.sh check-imported <issue_number>
```

Parse the output:
- `IMPORTED:<task_file_path>` — Issue was already imported
- `NOT_IMPORTED` — Issue has not been imported yet

**If `IMPORTED:<path>`:** Extract the task name from the path (e.g., `t387_fix_nodejs_deprecation` from `aitasks/t387_fix_nodejs_deprecation.md`). Use `AskUserQuestion`:
- Question: "Issue #<N> has already been imported as task <task_name> (<path>). How to proceed?"
- Header: "Duplicate"
- Options:
  - "Proceed anyway" (description: "Continue with the review despite the existing import")
  - "Abort" (description: "Stop — this issue is already tracked")

**If "Abort":** Inform user "Issue #<N> is already imported as <task_name>. No action taken." and end the workflow.

### Step 2: Gather Related Issues

Run the find-related subcommand:

```bash
./.aitask-scripts/aitask_contribution_review.sh find-related <issue_number>
```

Parse output lines:
- `OVERLAP:<num>:<score>` — Issue found via fingerprint overlap (score >= 4)
- `LINKED:<num>:<title>` — Issue found via `#N` references in body/comments
- `BOTH:<num>:<score>:<title>` — Issue found in both sources
- `NO_BOT_COMMENT` — No overlap analysis bot comment found
- `TOTAL_CANDIDATES:<count>` — Total unique candidate issues

**If `NO_BOT_COMMENT` appears in output:** Use `AskUserQuestion`:
- Question: "No overlap analysis comment found on issue #<N>. Run a local overlap check?"
- Header: "Overlap"
- Options:
  - "Run local check" (description: "Execute aitask_contribution_check.sh --dry-run to compute overlaps locally")
  - "Skip overlap check" (description: "Proceed with only linked issue references")

If "Run local check":
```bash
./.aitask-scripts/aitask_contribution_check.sh <issue_number> --dry-run --silent
```
Parse the output for `<!-- overlap-results top_overlaps: ... -->` line. Extract `N:S` pairs where score >= 4 and add them to the candidate list.

**If `TOTAL_CANDIDATES:0`** (and no local check produced results): Skip to **Step 5** with recommendation "single import, no related issues".

### Step 3: Fetch Related Issue Details

Collect all candidate issue numbers from Step 2. Fetch their full content:

```bash
./.aitask-scripts/aitask_contribution_review.sh fetch-multi <N1>,<N2>,<N3>
```

Parse the structured output. Each issue is delimited by:
- `@@@ISSUE:<num>@@@` — Issue separator
- `TITLE:<title>` — Issue title
- `CONTRIBUTOR:<name>` — Contributor username
- `>>>BODY_START` / `<<<BODY_END` — Body content boundaries

Extract code diffs from each issue body:
- Inline diff blocks (` ```diff ` sections)
- Hidden full diffs in `<!-- full-diff:filename ... -->` HTML comment blocks

**Present summary table to user:**

```
## Related Contribution Issues

| Issue | Title | Contributor | Source | Score | Changed Files |
|-------|-------|-------------|--------|-------|---------------|
| #42   | Fix X | @user1      | Both   | 7     | foo.sh, bar.sh |
| #38   | Add Y | @user2      | Overlap| 5     | foo.sh         |
```

### Step 4: AI Analysis of Code Modifications

Read the actual diffs from all candidate issues plus the target issue. Analyze:

- **Same files/functions touched?** (strongest merge signal)
- **Same bug fixed in different ways?** (merge: pick best approach)
- **Complementary changes?** (merge: combine both)
- **Unrelated despite fingerprint similarity?** (don't merge)

Score thresholds for reference:
- Score >= 7: "high" overlap — very likely should be merged
- Score >= 4: "likely" overlap — worth investigating
- Score < 4: "low" overlap — probably unrelated

Generate a structured recommendation with rationale:

```
## Recommendation

**Action:** Merge issues #42, #38, #15 into one task
**Rationale:** All three issues modify the same functions in foo.sh...
```

### Step 5: Present Proposal to User (AskUserQuestion)

**If merge is recommended:**

Use `AskUserQuestion`:
- Question: "Group these issues into one task: #42, #38, #15 — [brief rationale]"
- Header: "Import"
- Options:
  - "Import as merged task" (description: "Merge issues into a single task with combined diffs and multi-contributor attribution")
  - "Import only #<target>" (description: "Import only the target issue as a single task")
  - "Skip" (description: "Don't import yet — cancel without creating a task")

**If no merge is recommended:**

Use `AskUserQuestion`:
- Question: "Issue #<N> appears independent — no related contributions found worth merging"
- Header: "Import"
- Options:
  - "Import as single task" (description: "Import issue #<N> as an aitask")
  - "Skip" (description: "Don't import yet — cancel without creating a task")

### Step 5b: Check for Overlapping Existing Tasks

Execute the **Related Task Discovery Procedure** (see `.claude/skills/task-workflow/related-task-discovery.md`) with:
- **Matching context:** The contribution's title, description, areas (`<areas>` from Step 1), file paths (`<file_paths>`), and change type (`<change_type>`)
- **Purpose text:** "already cover this contribution's scope (they can be folded into the imported task or updated directly)"
- **Min eligible:** 1
- **Selection mode:** ai_filtered

**If no overlapping tasks found:** Proceed to Step 6 as normal.

**If overlapping tasks found and user selected task(s):** Use `AskUserQuestion`:
- Question: "How should the overlap with existing task(s) be handled?"
- Header: "Overlap"
- Options:
  - "Fold into new imported task" (description: "Import the contribution as new task and fold the overlapping existing task(s) into it")
  - "Update existing task instead" (description: "Add contribution content to the existing task — no new task created")
  - "Ignore overlap" (description: "Proceed with normal import, leave existing tasks unchanged")

Store the user's choice and the selected task IDs for use in Steps 6/6b.

### Step 6: Execute Import

**If "Update existing task instead" was selected in Step 5b:** Skip this step and proceed to **Step 6b**.

Based on user selection:

**Merged import:**
```bash
./.aitask-scripts/aitask_issue_import.sh --batch --merge-issues <N1>,<N2>,<N3> --commit
```

**Single import:**
```bash
./.aitask-scripts/aitask_issue_import.sh --batch --issue <N> --commit
```

**Skip:** Display "No task created." and end workflow.

After successful import, display the created task file path from the script output.

**If "Fold into new imported task" was selected in Step 5b:**

After import completes:

1. Parse the import output to get the created task file path:
   - Single import: output contains `Created: <filepath>`
   - Merge import: output contains `Merged N issues into: <filepath>`
2. Extract the task number from the filename (e.g., `t42` from `aitasks/t42_foo.md`)
3. Read the created task file's description body
4. Execute the **Task Fold Content Procedure** (see `.claude/skills/task-workflow/task-fold-content.md`) with:
   - **primary_description:** The imported task's description body
   - **folded_task_files:** File paths of each selected overlapping task from Step 5b
5. Update the imported task's description with the returned merged content:
   ```bash
   ./.aitask-scripts/aitask_update.sh --batch <new_task_num> --desc-file - <<'TASK_DESC'
   <merged description>
   TASK_DESC
   ```
6. Execute the **Task Fold Marking Procedure** (see `.claude/skills/task-workflow/task-fold-marking.md`) with:
   - **primary_task_num:** `<new_task_num>`
   - **folded_task_ids:** Selected overlapping task IDs from Step 5b
   - **handle_transitive:** `true`
   - **commit_mode:** `"fresh"`

**Key constraint:** The skill produces at most **ONE task** per invocation. To process multiple unrelated contribution issues, run the skill multiple times.

### Step 6b: Update Existing Task with Contribution (Alternative)

This step is reached when the user chose "Update existing task instead" in Step 5b.

**Select target task:** If multiple overlapping tasks were selected in Step 5b, use `AskUserQuestion`:
- Question: "Which existing task should be updated with this contribution?"
- Header: "Target"
- Options: Each selected overlapping task (label: filename, description: brief summary)

If only one task was selected, use it directly.

**Append contribution content to existing task:**
1. Read the existing task file
2. Append a new section at the end of the body:
   ```markdown
   ## Contribution from <contributor_name> (Issue #<N>)

   **Areas:** <areas from Step 1>
   **Files:** <file_paths from Step 1>
   **Change type:** <change_type from Step 1>

   <contribution description/body from Step 1>
   ```
3. Write the updated content back to the task file

**Update task frontmatter:**
```bash
./.aitask-scripts/aitask_update.sh --batch <task_num> --contributor "<contributor_name>" --contributor-email "<contributor_email>" --issue "<issue_url>"
```

Where `<contributor_name>`, `<contributor_email>` are from Step 1 metadata, `<issue_url>` is the contribution issue URL, and `<task_num>` is the target task number.

**Post notification on the contribution issue:**
```bash
./.aitask-scripts/aitask_contribution_review.sh post-comment <issue_number> "This contribution has been incorporated into existing task **t<task_num>** (<task_title>). The contributor will be credited via Co-authored-by when the task is implemented."
```

**Commit changes:**
```bash
./ait git add aitasks/<task_file>
./ait git commit -m "ait: Update t<task_num> with contribution from issue #<N>"
```

**End workflow:** Display "Contribution from issue #\<N\> incorporated into existing task t\<task_num\>. No new task created."

---

## Notes

- This skill produces at most one task per invocation — ONE task group, never more
- No execution profiles are used (simple standalone skill)
- No handoff to task-workflow (import-only, no implementation step)
- Platform detection is handled by the helper script (`aitask_contribution_review.sh`), which sources `aitask_contribution_check.sh` for platform backends (GitHub `gh` CLI, GitLab `glab`+curl, Bitbucket curl)
- The `--dry-run` output from `aitask_contribution_check.sh` includes the full overlap comment with `<!-- overlap-results -->` machine-readable block
- For Bitbucket: no label-based issue filtering; overlap detection relies on metadata presence scanning
- Score thresholds: >= 7 "high", >= 4 "likely", < 4 "low"
- The `--merge-issues` flag in `aitask_issue_import.sh` requires at least 2 issue numbers
- Multi-contributor attribution: primary contributor (largest diff) gets `Co-Authored-By` trailer; others listed in commit body
