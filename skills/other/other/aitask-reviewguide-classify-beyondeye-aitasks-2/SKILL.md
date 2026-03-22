---
name: aitask-reviewguide-classify
description: Classify a review guide file by assigning metadata and finding similar existing guides.
---

## Workflow

### Step 1: Mode Selection

If this skill is invoked with an argument (e.g., `/aitask-reviewguide-classify security`), proceed to **Step 2** (single-file mode).

If invoked without arguments (`/aitask-reviewguide-classify`), jump to **Step 8** (batch mode).

### Step 2: Resolve File

Use fzf to fuzzy-find the argument in the reviewguides directory:

```bash
find aireviewguides/ -name '*.md' -not -path '*/.reviewguidesignore' | sed 's|aireviewguides/||' | fzf --filter "<argument>" | head -4
```

- **If exactly 1 match:** Use it directly as the target file.
- **If 2-4 matches:** Use `AskUserQuestion`:
  - Question: "Multiple reviewguide files match '<argument>'. Which one?"
  - Header: "File"
  - Options: Each match as an option (label = relative path, description = "")
- **If 0 matches:** Inform the user: "No reviewguide files match '<argument>'." and end the workflow.

Read the resolved file's full content from `aireviewguides/<relative_path>`. Parse the YAML frontmatter to extract existing fields: `name`, `description`, `environment`, `reviewtype`, `reviewlabels`, `similar_to`.

### Step 3: Analyze Content

Read the markdown body (everything after the closing `---` of the frontmatter).

- Identify all H2/H3 section headings
- List the bullet point items under each heading
- Determine the file's primary topics and concerns based on the headings and content

This analysis drives the metadata assignment in Step 4.

### Step 4: Assign Metadata

Read the three vocabulary files:

```bash
cat aireviewguides/reviewtypes.txt
```
```bash
cat aireviewguides/reviewlabels.txt
```
```bash
cat aireviewguides/reviewenvironments.txt
```

**Assign `reviewtype`:** Select the single best-fitting value from `reviewtypes.txt`. Strongly prefer existing values — only propose a new value if none of the existing types fits at all.

**Assign `reviewlabels`:** Select 3-6 values from `reviewlabels.txt` that describe the file's distinct topics. Each label should correspond to a theme covered in the file's content. Only propose new labels if no existing label covers a topic.

**Assign `environment`:** Determine the file's subdirectory within `aireviewguides/`:
- If in `general/` → the file is universal; do NOT set an `environment` field
- If in a non-general subdirectory (e.g., `python/`, `android/`, `shell/`) → select one or more values from `reviewenvironments.txt` that match the file's scope. Use the subdirectory name as a strong hint (e.g., `python/` → `[python]`, `shell/` → `[bash, shell]`). Only propose new environment values if none exist that fit.

### Step 5: Compare to Existing Files

Run the comparison against all other reviewguide files:

```bash
./.aitask-scripts/aitask_reviewguide_scan.sh --compare <relative_path>
```

Parse the pipe-delimited output. Each line has the format:
```
<relative_path>|<name>|<similarity_score>|<shared_labels_csv>|<type_match:yes/no>|<env_overlap:yes/no>
```

Output is sorted descending by score, only showing files with score > 0.

- If the top result has a score >= 5, set `similar_to` to that file's relative path
- If the top score is < 5 (or no results), do not set `similar_to`

### Step 6: Present Results

Show the classification summary:

```
## Classification Results

**File:** <relative_path>
**Assigned reviewtype:** <type>
**Assigned reviewlabels:** [<label1>, <label2>, ...]
**Environment:** <env list or "universal (no environment field)">

### Similarity Analysis
Most similar: <file> (score: <N>, shared labels: <labels>) — or "No strong similarity found"
```

If any values differ from the file's existing metadata, highlight what is being added or changed.

### Step 7: Confirm and Apply

Use `AskUserQuestion`:
- Question: "Apply the suggested classification?"
- Header: "Classify"
- Options:
  - "Apply as proposed" (description: "Update frontmatter with the suggested metadata")
  - "Modify before applying" (description: "Adjust the suggested values before writing")
  - "Cancel" (description: "Don't modify the file")

**If "Modify before applying":** Ask the user which values to change. Apply with the modified values.

**If "Cancel":** End the workflow for this file. In batch mode, continue to the next file.

**If "Apply as proposed" or after modification:**

1. Update the file's YAML frontmatter between the `---` delimiters. Set `reviewtype`, `reviewlabels`, and optionally `environment` and `similar_to`. Preserve all existing fields (`name`, `description`) and the full markdown body unchanged.

2. If a new `reviewtype` value was used (not already in `reviewtypes.txt`):
   ```bash
   echo "<new_value>" >> aireviewguides/reviewtypes.txt && sort -o aireviewguides/reviewtypes.txt aireviewguides/reviewtypes.txt
   ```

3. If new `reviewlabels` values were used (not already in `reviewlabels.txt`):
   ```bash
   echo "<new_label>" >> aireviewguides/reviewlabels.txt && sort -o aireviewguides/reviewlabels.txt aireviewguides/reviewlabels.txt
   ```

4. If new `environment` values were used (not already in `reviewenvironments.txt`):
   ```bash
   echo "<new_env>" >> aireviewguides/reviewenvironments.txt && sort -o aireviewguides/reviewenvironments.txt aireviewguides/reviewenvironments.txt
   ```

5. **If in single-file mode** (not batch), or **batch autocommit mode**: commit all changes:
   ```bash
   git add aireviewguides/<relative_path> aireviewguides/reviewtypes.txt aireviewguides/reviewlabels.txt aireviewguides/reviewenvironments.txt
   git commit -m "ait: Classify reviewguide <filename>"
   ```

7. **If in batch non-autocommit mode**: stage changes but do not commit (Step 12 handles the commit).

**If `similar_to` was set:** Inform the user: "This file is similar to `<similar_to>`. Consider running `/aitask-reviewguide-merge <file> <similar_file>` to compare and potentially consolidate."

### Step 8: Scan for Incomplete Files (Batch Mode)

Run the scan for files missing metadata:

```bash
./.aitask-scripts/aitask_reviewguide_scan.sh --missing-meta
```

Parse the pipe-delimited output. Each line has the format:
```
<relative_path>|<name>|<reviewtype_or_MISSING>|<reviewlabels_csv_or_MISSING>|<environment_csv_or_universal>
```

If no files are returned, inform the user: "All reviewguide files have complete metadata. Nothing to classify." and end the workflow.

### Step 9: Present List

Show which files are missing metadata and what specifically is missing:

```
## Files Missing Metadata

| # | File | Missing Fields |
|---|------|----------------|
| 1 | general/code_conventions.md | reviewtype, reviewlabels |
| 2 | python/python_bp.md | reviewlabels, environment |
```

Determine "Missing Fields" by checking:
- `reviewtype` → shows "MISSING" in column 3
- `reviewlabels` → shows "MISSING" in column 4
- `environment` → shows "universal" in column 5 AND the file is NOT in the `general/` subdirectory

### Step 10: Autocommit Consent

Use `AskUserQuestion`:
- Question: "<N> files need classification. Auto-commit after each file?"
- Header: "Commit"
- Options:
  - "Yes, autocommit" (description: "Commit changes after each file is processed")
  - "No, single commit at end" (description: "Stage all changes, commit once when done")
  - "Cancel batch" (description: "Don't process any files")

**If "Cancel batch":** End the workflow.

### Step 11: Iterate

For each file missing metadata, run the single-file classification workflow:
- Steps 3-7 (skip Step 2 since the file path is already known from the scan)
- Read the file, analyze content, assign metadata, compare, present, confirm

Pass the autocommit context so Step 7 knows whether to commit after each file.

### Step 12: Final Commit (if not autocommit)

If "No, single commit at end" was selected in Step 10, commit all staged changes:

```bash
git add aireviewguides/ aireviewguides/reviewtypes.txt aireviewguides/reviewlabels.txt aireviewguides/reviewenvironments.txt
git commit -m "ait: Classify <N> reviewguide files"
```

### Step 13: Summary

Show a summary of the batch run:
- How many files were classified
- Any new vocabulary values added (reviewtype, reviewlabels, environment)
- Any `similar_to` relationships discovered
- If any similar_to pairs were found, suggest: "Consider running `/aitask-reviewguide-merge` to review merge candidates."

### Step 14: Satisfaction Feedback

After the workflow is complete (after Step 7 in single-file mode or Step 13 in batch mode), execute the **Satisfaction Feedback Procedure** (see `.claude/skills/task-workflow/satisfaction-feedback.md`) with `skill_name` = `"reviewguide-classify"`.

## Notes

- The argument to this skill is a **fuzzy search pattern** passed to `fzf --filter`, not necessarily an exact relative path. Partial matches work (e.g., `security` matches `general/security.md`)
- Three vocabulary files in `aireviewguides/`: `reviewtypes.txt` (classification type), `reviewlabels.txt` (topic labels), `reviewenvironments.txt` (language/framework environments). New values are only added to the `aireviewguides/` copies — the `seed/` directory is not modified by this skill.
- The `--compare` similarity score formula: `(shared_labels * 2) + (type_match ? 3 : 0) + (env_overlap ? 2 : 0)`
- The threshold for setting `similar_to` is a score of >= 5
- Files in `general/` are universal — they should NOT have an `environment` field. Files in other subdirectories (python, android, shell, etc.) should have an `environment` field with values from `reviewenvironments.txt`
- Assign 3-6 `reviewlabels` per file — enough to capture distinct topics without being too broad
- Strongly prefer existing vocabulary values over creating new ones
- This skill does not modify the `seed/` directory. All changes are written to `aireviewguides/` only.
- Commit messages use the `ait:` prefix: `ait: Classify reviewguide <filename>`
