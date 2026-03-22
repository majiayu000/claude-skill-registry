---
name: user-file-select
description: Interactive file selection with keyword search, fuzzy name matching, and functionality search. Reusable by other skills.
user-invocable: false
---

## Arguments

This skill accepts optional arguments to skip mode selection:
- No arguments: show mode selection menu (Step 1)
- `--keywords "term1 term2"`: jump directly to keyword search (Step 2a)
- `--names "partial1 partial2"`: jump directly to name search (Step 2b)
- `--describe "what the files do"`: jump directly to functionality search (Step 2c)

If arguments are provided, parse the flag and value, then skip to the corresponding step.

## Workflow

### Step 1: Mode Selection

Use `AskUserQuestion`:
- Question: "How would you like to find files?"
- Header: "Search mode"
- Options:
  - "Search by keywords" (description: "Search inside file contents for specific terms")
  - "Search by name" (description: "Fuzzy-match partial filenames or paths using fzf")
  - "Search by functionality" (description: "Describe what the code does — Claude finds relevant files")

Handle selection:
- "Search by keywords" → proceed to Step 2a
- "Search by name" → proceed to Step 2b
- "Search by functionality" → proceed to Step 2c

### Step 2a: Keyword Search

If keywords were not already provided via arguments, use `AskUserQuestion`:
- Question: "Enter keywords to search for in file contents (space-separated):"
- Header: "Keywords"
- Options: use "Other" for free text input

Run the bash helper:

```bash
./.aitask-scripts/aitask_find_files.sh --keywords "<user_keywords>" --max-results 20
```

Parse the pipe-delimited output. Each line has the format:
```
<rank>|<match_count>|<file_path>
```

If no output (no matches found), run the **No Results Handler** (see below).
If results found, proceed to Step 3 with the result list.

### Step 2b: Name Search

If names were not already provided via arguments, use `AskUserQuestion`:
- Question: "Enter partial filenames or path fragments to search for (space-separated):"
- Header: "Names"
- Options: use "Other" for free text input

Run the bash helper:

```bash
./.aitask-scripts/aitask_find_files.sh --names "<user_names>" --max-results 20
```

Parse the pipe-delimited output (same format as Step 2a).

If no output (no matches found), run the **No Results Handler**.
If results found, proceed to Step 3 with the result list.

### Step 2c: Functionality Search

If description was not already provided via arguments, use `AskUserQuestion`:
- Question: "Describe the functionality or purpose of the files you're looking for:"
- Header: "Description"
- Options: use "Other" for free text input

Use Claude's own tools (Glob, Grep, Read) to find relevant files:

1. **Analyze the description** to identify search strategies:
   - Extract technical terms, function names, patterns
   - Determine likely file types and directories

2. **Search iteratively:**
   - Use Grep to search for key terms in file contents
   - Use Glob to find files by likely naming patterns
   - Read promising files to verify relevance
   - Continue until a ranked list is assembled (target: up to 20 files)

3. **Build a ranked list** with relevance descriptions for each file

If no relevant files found, run the **No Results Handler**.
If results found, proceed to Step 3 with the result list.

### Step 3: Present Results

Display the ranked results to the user as a numbered list.

**For keyword and name modes** (from script output):
```
Found <N> matching files:

 1. .aitask-scripts/lib/task_utils.sh (score: 12)
 2. .aitask-scripts/aitask_changelog.sh (score: 8)
 3. .aitask-scripts/aitask_archive.sh (score: 6)
 ...
```

**For functionality mode** (from Claude's analysis):
```
Found <N> relevant files:

 1. .aitask-scripts/lib/task_utils.sh — Core task resolution and extraction utilities
 2. .aitask-scripts/aitask_changelog.sh — Commit parsing and task ID extraction
 ...
```

Proceed to Step 4.

### Step 4: User Selection

Use `AskUserQuestion`:
- Question: "Select files by entering indices in parentheses. Supports: individual (1,4,5), ranges (3-5), mixed (1,3-5,7), or (all)."
- Header: "Select files"
- Options: use "Other" for free text input

Parse the selection string:

1. Trim whitespace
2. Strip surrounding parentheses: if the input starts with `(` and ends with `)`, remove them (e.g., `(1,3-5)` → `1,3-5`)
3. If input is "all" (case-insensitive): select all files from the list
4. Otherwise, split by comma to get tokens
5. For each token (trimmed):
   - If it contains a hyphen (e.g., "3-5"): parse as range, expand to individual indices
   - Otherwise: parse as a single integer index
6. Validate all indices are within bounds (1 to N where N is the result count)
7. Deduplicate indices
8. Sort indices in ascending order
9. Map indices to file paths from the result list

**Validation errors:**
- If any index is out of range: warn user and re-prompt ("Index X is out of range (1-N). Please try again.")
- If input cannot be parsed: warn user and re-prompt ("Could not parse 'input'. Use format like (1,3-5,7) or (all).")

Proceed to Step 5 with the selected file paths.

### Step 5: Output and Refinement

Display the selected files:

```
Selected <M> files:
- path/to/file1.sh
- path/to/file2.sh
- ...
```

Use `AskUserQuestion`:
- Question: "Confirm file selection, or refine?"
- Header: "Confirm"
- Options:
  - "Confirm selection" (description: "Use these files")
  - "Search for more files" (description: "Run another search and add to current selection")
  - "Start over" (description: "Discard selection and search again")

**If "Confirm selection":** The skill's final output is the newline-separated list of selected file paths (relative to project root). End the workflow.

**If "Search for more files":** Go back to Step 1, keeping the current selection. After the new search and selection (Steps 1-4), merge new selections with existing ones (deduplicate by file path). Return to Step 5 with the combined list.

**If "Start over":** Clear the current selection and go back to Step 1.

---

## No Results Handler

When any search mode produces no results:

Use `AskUserQuestion`:
- Question: "No files found matching your search. What would you like to do?"
- Header: "No results"
- Options:
  - "Try again" (description: "Search again with different terms")
  - "Switch search mode" (description: "Try a different search method")
  - "Cancel" (description: "Exit file selection")

- "Try again" → loop back to the search input prompt in the current step (2a, 2b, or 2c)
- "Switch search mode" → go to Step 1
- "Cancel" → end workflow with empty result

## Notes

- This skill is designed to be invoked by other skills (aitask-explain, aitask-explore) as a reusable file selection component
- Modes 1 and 2 (keywords, names) delegate to `.aitask-scripts/aitask_find_files.sh` for efficient file-system searching
- Mode 2 uses `fzf --filter` for true fuzzy matching (e.g., "tsk_utl" matches "task_utils.sh")
- Mode 3 (functionality) uses Claude's own Glob, Grep, and Read tools for semantic search
- The output is a newline-separated list of file paths relative to the project root
- The "Search for more files" option allows iterative refinement without losing previous selections
- When invoked with arguments, the mode selection step is skipped for efficiency
- The bash helper uses `git ls-files` to restrict searches to tracked files only (respects .gitignore)
