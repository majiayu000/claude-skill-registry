---
name: aitask-explain
description: "Explain files in the project: functionality, usage examples, and code evolution history traced through aitasks."
---

## Workflow

### Step 1: File Selection

**Check for existing runs first:**

```bash
ls -d .aitask-explain/*/files.txt 2>/dev/null
```

If existing runs are found, read `files.txt` from each run to build a summary.

**If invoked with arguments (file/directory paths):** parse each argument:
- If argument matches `<path>:<start_line>-<end_line>` (e.g., `src/app.py:10-50`): extract the file path and store the line range as focus context for Step 4
- If argument is a plain path (no colon+range suffix): use as-is (no range)

Skip to "Proceed with files" below.

**If no arguments and existing runs exist:**

Use `AskUserQuestion`:
- Question: "How would you like to select files?"
- Header: "Files"
- Options:
  - "Use existing analysis" (description: "Reuse data from a previous aitask-explain run")
  - "Search for files" (description: "Find files by keywords, names, or functionality")
  - "Enter paths directly" (description: "Type file/directory paths manually")

**If "Use existing analysis":**
- If multiple runs exist, use `AskUserQuestion` to select which run (show timestamp + covered files summary for each)
- Once a run is selected, use `AskUserQuestion`:
  - Question: "Run from \<timestamp\> covers: \<file list\>. Use existing data or refresh?"
  - Header: "Refresh"
  - Options:
    - "Use existing data" (description: "Skip regeneration, use cached reference data")
    - "Refresh references" (description: "Re-run git analysis to update data for these files")
- If "Use existing data": set `run_dir` to the selected run's path, skip Step 3 (no regeneration needed), proceed to Step 2
- If "Refresh references": use the file list from `files.txt`, delete old run directory, proceed to Step 3

**If no arguments and no existing runs:**

Use `AskUserQuestion`:
- Question: "How would you like to select files?"
- Header: "Files"
- Options:
  - "Search for files" (description: "Find files by keywords, names, or functionality")
  - "Enter paths directly" (description: "Type file/directory paths manually")

**If "Search for files":** Read and follow `.claude/skills/user-file-select/SKILL.md` to get file paths. Once file paths are returned, proceed to "Proceed with files" below.

**If "Enter paths directly":**

Use `AskUserQuestion`:
- Question: "Which files or directories would you like explained? (enter paths separated by spaces)"
- Header: "Files"
- Options: free text only (use "Other")

**Proceed with files:**

- **Directory expansion**: If any path is a directory, the shell script expands it to all git-tracked text files within it using `git ls-files <directory>`
- **Binary file detection**: Binary files (images, compiled assets, etc.) are automatically detected by the extraction pipeline and marked with `binary: true` in `reference.yaml`. They have commit timelines but no line-level annotations. No special handling is needed at file selection — binary files are processed alongside text files.
- Validate all resolved files exist and are tracked by git

### Step 2: Mode Selection

Use `AskUserQuestion` with `multiSelect: true`:
- Question: "What would you like explained?"
- Header: "Mode"
- Options:
  - "Functionality" (description: "What the code does — purpose, components, data flow")
  - "Usage examples" (description: "How the code is used in the project — real imports and references")
  - "Code evolution" (description: "How the code changed over time — traced through commits and aitasks")

### Step 3: Generate Reference Data

Run the shell script to gather raw data and produce the YAML reference:

```bash
./.aitask-scripts/aitask_explain_extract_raw_data.sh --gather <path1> [path2...] --max-commits 50
```

- Parse the `RUN_DIR: <path>` line from output to get the run-specific directory
- The script automatically cleans up stale runs (older runs for the same source directory) after gathering
- Store the `run_dir` path for cleanup in Step 6
- Read `<run_dir>/reference.yaml` to understand the structure
- For "Code evolution" mode: also read extracted task/plan files from `<run_dir>/tasks/` and `<run_dir>/plans/`

### Step 4: Analysis and Explanation

**If a line range was specified in Step 1:** Focus analysis primarily on the specified line range. Read the full file for context, but center the explanation on the specified lines. For Code Evolution mode, prioritize commits that touched the specified range.

Based on selected modes, provide analysis:

#### Functionality Mode

- Read the target file(s) in full
- **For binary files** (marked `binary: true` in `reference.yaml`): describe the file's role based on its path, filename, and extension. Search the codebase with `Grep` for references to the file to understand how it's used. Do not attempt line-level code analysis.
- **For text files**: Provide a structured explanation covering:
  - **Purpose**: What problem does this code solve
  - **Key components**: Main functions, classes, data structures
  - **Data flow**: How data moves through the code
  - **Error handling**: How errors are managed
  - **Design patterns**: Notable patterns or conventions used
- Reference the commit history from `reference.yaml` for context on why certain patterns exist

#### Usage Examples Mode

- Search the project codebase for imports/references to the target file(s):
  - Use `Grep` to find `source` statements (for shell), `import` statements, function calls
  - Use `Grep` for filename references in documentation, configuration, etc.
- Present real usage examples from the project itself
- For each usage found, provide:
  - File path and line number
  - Context of how it's being used
  - Brief explanation of the usage pattern
- If no project usages found, describe typical usage based on the code's interface

#### Code Evolution Mode

- Read `<run_dir>/reference.yaml` for the line-range-to-commit-to-task mapping
- Read relevant extracted plans from `<run_dir>/plans/` for implementation notes and context
- Read relevant extracted tasks from `<run_dir>/tasks/` for original task descriptions
- **For binary files** (marked `binary: true` in `reference.yaml`): present only the commit timeline (no `line_ranges` data exists). Show when the file was added, modified, or replaced, and which tasks/commits touched it.
- **For text files**: Present a **newest-first narrative** of how the code evolved:
  - What each significant commit/task changed
  - **Why** changes were made (extracted from plan "Final Implementation Notes")
  - How the code's architecture evolved over time
  - Key decisions documented in the plans
- Use the `line_ranges` data to connect current code sections to their historical commits

### Step 5: Interactive Follow-up Loop

Use `AskUserQuestion`:
- Question: "What would you like to do next?"
- Header: "Next"
- Options:
  - "Ask about specific code section" (description: "Ask about a line range or function — uses reference data for targeted context")
  - "Switch analysis mode" (description: "Change between functionality / usage / evolution")
  - "Analyze different files" (description: "Select new files to analyze")
  - "Done" (description: "Finish and clean up")

**Handle selection:**

- **"Ask about specific code section":**
  - Use `AskUserQuestion` to ask which section (via "Other" free text): line range (e.g., "lines 50-80"), function name (e.g., "resolve_task_file"), or a description (e.g., "the error handling logic")
  - Use the `line_ranges` from `reference.yaml` to identify which commits and tasks are relevant to that section
  - Read relevant task/plan files from `<run_dir>/tasks/` and `<run_dir>/plans/` for context
  - Provide a targeted explanation combining code analysis with historical commit/task context
  - Loop back to Step 5

- **"Switch analysis mode":**
  - Return to Step 2 (mode selection)
  - Skip Step 3 (reference data already generated)

- **"Analyze different files":**
  - Return to Step 1 (file selection)
  - New reference data will be generated in Step 3

- **"Done":**
  - Proceed to Step 6 (cleanup)

### Step 6: Cleanup

Use `AskUserQuestion`:
- Question: "Clean up the analysis data?"
- Header: "Cleanup"
- Options:
  - "Yes, delete" (description: "Remove the run directory and all generated data")
  - "No, keep" (description: "Keep the data for future sessions — can be reused with 'Use existing analysis'")

**If "Yes, delete":**

```bash
./.aitask-scripts/aitask_explain_extract_raw_data.sh --cleanup <run_dir>
```

Where `<run_dir>` is the path captured in Step 3 (e.g., `.aitask-explain/20260221_143052`).

**If "No, keep":**
- Inform user: "Analysis data preserved at `<run_dir>`. Use `/aitask-explain` again and select 'Use existing analysis' to reuse it."
- To manage existing runs later: `./.aitask-scripts/aitask_explain_runs.sh`

**Note:** Stale run cleanup (removing older runs for the same source directory) happens automatically during Step 3 gathering. Manual cleanup via Step 6 removes the current run entirely. To trigger a manual stale cleanup: `./.aitask-scripts/aitask_explain_runs.sh --cleanup-stale`

### Step 7: Satisfaction Feedback

Execute the **Satisfaction Feedback Procedure** (see `.claude/skills/task-workflow/satisfaction-feedback.md`) with `skill_name` = `"explain"`.

---

## Notes

- This skill uses `aitask_explain_extract_raw_data.sh` for raw data extraction (git log, git blame, task/plan file copying)
- Raw data is processed by `aitask_explain_process_raw_data.py` into a structured `reference.yaml` file
- Each run creates an isolated directory under `.aitask-explain/<dir_key>__<timestamp>/` where `dir_key` is derived from the common parent directory of analyzed files (e.g., `aiscripts__lib__20260226_155403`)
- The `reference.yaml` maps lines → commits → task IDs, enabling targeted "code evolution" explanations
- Commit timeline is ordered **newest first** (most recent changes have lowest timeline numbers)
- Task/plan files are copied with ID-only names (e.g., `t16.md`, `p16.md`) for simpler referencing
- Existing runs can be reused to avoid expensive re-analysis of unchanged code
- Run management (list, delete) is available via `./.aitask-scripts/aitask_explain_runs.sh`
- Accepts both individual files and directories; directories are expanded to git-tracked text files
- Binary files (images, compiled assets, etc.) are auto-detected by the extraction pipeline and marked `binary: true` in `reference.yaml`. They have commit timelines but empty `line_ranges`. The codebrowser shows "Binary file — cannot display" for content with "(binary, N commits)" in the annotation info bar.
