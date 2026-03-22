---
name: aitask-reviewguide-merge
description: Compare two similar review guide files and merge, split, or keep separate.
---

## Workflow

### Step 1: Mode Selection

If this skill is invoked with two arguments (e.g., `/aitask-reviewguide-merge security error`), both are fuzzy search patterns — proceed to **Step 2** to resolve both.

If invoked with one argument (e.g., `/aitask-reviewguide-merge security`), the argument is a fuzzy search pattern — proceed to **Step 2** to resolve it, then read its `similar_to` field for the second file.

If invoked without arguments (`/aitask-reviewguide-merge`), jump to **Step 8** (batch mode).

### Step 2: Resolve Input Files

For each argument, use fzf to fuzzy-find in the reviewguides directory:

```bash
find aireviewguides/ -name '*.md' -not -path '*/.reviewguidesignore' | sed 's|aireviewguides/||' | fzf --filter "<argument>" | head -4
```

- **If exactly 1 match:** Use it directly.
- **If 2-4 matches:** Use `AskUserQuestion`:
  - Question: "Multiple reviewguide files match '<argument>'. Which one?"
  - Header: "File"
  - Options: Each match as an option (label = relative path, description = "")
- **If 0 matches:** Inform the user: "No reviewguide files match '<argument>'." and end the workflow.

**If only one argument was provided:**
1. Read the resolved file's frontmatter, extract the `similar_to` field.
2. If `similar_to` is set and non-empty: use its value as the second file's relative path (exact path, no fzf needed).
3. If `similar_to` is empty or missing: inform the user: "File '<name>' has no `similar_to` field. Provide a second file to compare against, or run without arguments for batch mode." and end the workflow.

**Validation:** Confirm both resolved files exist in `aireviewguides/`. If both arguments resolve to the same file, inform the user and end.

Read both files' full content (frontmatter + markdown body).

### Step 3: Detailed Comparison

Parse each file:
- YAML frontmatter: `name`, `description`, `environment` (optional array), `reviewtype`, `reviewlabels` (array), `similar_to` (optional)
- Markdown body: All H2 (`##`) and H3 (`###`) section headings with their bullet points

Categorize each bullet point as:
- **Duplicate** — Same semantic review check exists in both files (may have different wording but covers the same concern)
- **Unique to A** — Only in file A
- **Unique to B** — Only in file B

Also compare metadata:
- `reviewtype`: same or different?
- `reviewlabels`: overlap set, unique to A set, unique to B set
- `environment`: same, overlapping, or different?

Compute overlap percentage: `duplicates / (duplicates + unique_A + unique_B)` (based on bullet points, not metadata).

Present the comparison:

```
## Comparison: <file_A_path> vs <file_B_path>

**<file_A name>** — <file_A description>
**<file_B name>** — <file_B description>

### Metadata
| Field | <file_A> | <file_B> |
|-------|----------|----------|
| reviewtype | <type_A> | <type_B> |
| reviewlabels | <labels_A> | <labels_B> |
| environment | <env_A or universal> | <env_B or universal> |

### Duplicate Instructions (N items)
- "<bullet from A>" == "<bullet from B>"  (section: <heading>)
...

### Unique to <file_A> (N items)
- "<bullet>" (section: <heading>)
...

### Unique to <file_B> (N items)
- "<bullet>" (section: <heading>)
...

### Overlap: N% (N duplicate / M total unique checks)
```

### Step 4: Propose Action

Based on the overlap percentage, present a recommendation with rationale:

- **>70% overlap:** "Recommendation: **Merge** — these files cover substantially the same ground. Merging avoids duplication and creates a single authoritative source."
- **30-70% overlap:** "Recommendation: **Merge or keep separate** — these files share some concerns but each has significant unique content. Consider merging if the topics belong together, or keep separate if they serve distinct review purposes."
- **<30% overlap:** "Recommendation: **Keep separate** — these files cover mostly different concerns. Remove any exact duplicates but maintain both files."

### Step 5: User Selection

Use `AskUserQuestion`:
- Question: "How should these files be consolidated?"
- Header: "Merge"
- Options:
  - `"Merge into <file_A name>"` (description: `"Combine all unique content into <file_A_path>, delete <file_B_path>"`)
  - `"Merge into <file_B name>"` (description: `"Combine all unique content into <file_B_path>, delete <file_A_path>"`)
  - `"Keep separate"` (description: `"Remove exact duplicates from one file, clear similar_to from both"`)
  - `"Cancel"` (description: `"No changes"`)

**If "Cancel":** End the workflow. In batch mode, continue to the next pair (Step 12).

### Step 6: Execute Action

#### If "Merge into <target>" (where target is one file and source is the other):

1. **Build merged content:** Keep the target file's overall structure (its H2/H3 headings). For each section heading that exists in both files: keep the target's bullets, then append unique bullets from the source that are not duplicates. For H3 sections that exist only in the source: add them under the most appropriate H2 in the target. If no matching H2 exists, add the section at the end of `## Review Instructions`.

2. **Update target's `reviewlabels`:** Union of both files' `reviewlabels` arrays, sorted alphabetically.

3. **Update target's `environment`:**
   - If both have `environment`: union the arrays (sorted).
   - If only one has `environment`: keep it.
   - If neither has `environment`: leave unset (both are universal).

4. **Keep target's `reviewtype`.** If the source had a different reviewtype, note it in the output but do not change.

5. **Remove `similar_to`** from the target file's frontmatter (if present).

6. **Write the updated target file** to `aireviewguides/<target_path>`.

7. **Delete the source file** from `aireviewguides/<source_path>`.

8. **Update vocabulary files if needed:** If the merged `reviewlabels` include values not in the vocabulary file:
   ```bash
   echo "<new_label>" >> aireviewguides/reviewlabels.txt && sort -o aireviewguides/reviewlabels.txt aireviewguides/reviewlabels.txt
   ```
   Same pattern for `reviewenvironments.txt` if new environment values appear.

9. **Clean up `similar_to` references:** Read all other reviewguide files. If any file has `similar_to` pointing to the deleted source file, update it to point to the target file instead (or clear it if the similarity no longer holds).

10. **Commit:**
    ```bash
    git add aireviewguides/
    git commit -m "ait: Merge reviewguide <source_name> into <target_name>"
    ```

#### If "Keep separate":

1. Identify exact duplicate bullets between the two files.

2. Remove the duplicates from whichever file has fewer unique items (it contributes less unique content, so the duplicates are better kept in the other file).

3. Clear `similar_to` from both files' frontmatter.

4. Write both updated files to `aireviewguides/`.

5. **Commit:**
   ```bash
   git add aireviewguides/
   git commit -m "ait: Deduplicate reviewguides <file_A_name> and <file_B_name>"
   ```

### Step 7: Summary

Show what was done:

**For merge:**
```
## Merge Complete

**Action:** Merged <source_name> into <target_name>
**Bullets added:** N unique instructions from <source_name>
**Bullets kept:** M instructions total
**Labels merged:** [<union of labels>]
**File deleted:** <source_path>
```

**For keep-separate:**
```
## Deduplication Complete

**Action:** Kept both files separate
**Duplicates removed:** N exact duplicate bullets removed from <file_with_fewer_unique>
**similar_to cleared:** Both files
```

---

### Step 8: Find Merge Candidates (Batch Mode)

Run the scan script:

```bash
./.aitask-scripts/aitask_reviewguide_scan.sh --find-similar
```

Parse the pipe-delimited output. Each line has the format:
```
<relative_path>|<name>|<reviewtype>|<reviewlabels_csv>|<environment_csv_or_universal>|<most_similar_path>:<overlap_count>
```

Build candidate pairs: for each file where `overlap_count > 0` and `most_similar_path != none`, create a pair `(file, most_similar_path, overlap_count)`. Deduplicate pairs (A→B and B→A are the same pair — keep the one with the higher overlap count, or the first encountered).

If no candidate pairs found: "No similar reviewguide files found. Nothing to merge." and end the workflow.

### Step 9: Optional Environment Filter

Collect all distinct environments from the candidate pairs' files.

Use `AskUserQuestion`:
- Question: "Filter merge candidates by environment?"
- Header: "Filter"
- Options: `"All environments"` (description: "Show all candidate pairs") plus one option per distinct environment detected (up to 3 environments to stay within the 4-option limit). If more than 3 environments, use "All environments" only.

If a specific environment is selected, filter the candidate pairs to those where at least one file has that environment.

### Step 10: Present Candidate Pairs

Sort pairs by overlap count (highest first).

Use `AskUserQuestion` with pagination (max 4 options, 3 pairs per page + "Skip all" or "Show more"):

**Pagination loop:**
- Start with `current_offset = 0` and `page_size = 3`.
- For the current page, take pairs from index `current_offset` to `current_offset + page_size - 1`.
- Build options:
  - Each pair: label = `"<file_A_name> + <file_B_name>"`, description = `"Shared labels: <csv>, overlap: <N> labels"`
  - If more pairs remain: add `"Show more pairs"` (description: `"Show next batch (<N> more available)"`)
  - If no more pairs: use the last slot for `"Skip all"` (description: `"No merges needed"`)
  - Always include `"Skip all"` on the last page (show up to 3 pairs + "Skip all")
- Question: "Select a pair to compare and potentially merge:"
- Header: "Pair"

**If "Show more":** Increment offset, loop back.
**If "Skip all":** End workflow.
**If a pair is selected:** Proceed to Step 11.

### Step 11: Execute Single-Pair Workflow

For the selected pair, run Steps 3-7 with both files already resolved (skip Step 2 fzf resolution).

### Step 12: Loop

After completing a pair, use `AskUserQuestion`:
- Question: "Process another merge candidate?"
- Header: "Continue"
- Options:
  - `"Next pair"` (description: `"Re-scan and select another pair to compare"`)
  - `"Done"` (description: `"Finish merge workflow"`)

**If "Next pair":** Re-run `./.aitask-scripts/aitask_reviewguide_scan.sh --find-similar` to get updated candidates (since the merge changed the landscape). Apply the same environment filter from Step 9. Return to Step 10 with the new pairs.

**If "Done":** Proceed to Step 13.

### Step 13: Batch Summary

Show a summary of the batch session:

```
## Merge Session Summary

**Pairs processed:** N
**Files merged:** <list of source files merged into targets>
**Files kept separate:** <list of deduplicated pairs>
**Files deleted:** <list of deleted source files>
```

### Step 14: Satisfaction Feedback

After the workflow is complete (after Step 7 in single-pair mode or Step 13 in batch mode), execute the **Satisfaction Feedback Procedure** (see `.claude/skills/task-workflow/satisfaction-feedback.md`) with `skill_name` = `"reviewguide-merge"`.

## Notes

- Arguments are **fuzzy search patterns** passed to `fzf --filter`, not exact paths. Partial matches work (e.g., `security` matches `general/security.md`).
- If one argument is given, the second file comes from the first file's `similar_to` frontmatter field. If `similar_to` is not set, the skill informs the user and ends.
- The detailed comparison (Step 3) is **semantic**: bullets that express the same review concern in different words are categorized as duplicates. The LLM reads both files and makes this determination.
- The scan script's `--find-similar` output uses reviewlabel overlap counts, not bullet-point similarity. It serves as a rough heuristic for finding candidates; the detailed comparison in Step 3 is more thorough.
- This skill does **not** modify the `seed/` directory. All changes are written to `aireviewguides/` only.
- When merging, keep the target file's `reviewtype`. If the source had a different type, note it in the output but do not change the target's type.
- When merging `reviewlabels`, take the union of both files' labels (sorted). If new labels are created, add them to `aireviewguides/reviewlabels.txt` (sorted).
- When merging `environment`, take the union. If one file is universal (no environment) and the other is environment-specific, keep the environment field from the specific one.
- After deleting a source file, check all other reviewguide files for `similar_to` references pointing to the deleted file and update them to point to the target or clear them.
- Commit messages use the `ait:` prefix: `ait: Merge reviewguide <source> into <target>` or `ait: Deduplicate reviewguides <A> and <B>`.
- In batch mode, re-run `--find-similar` after each merge to get updated pair candidates, since merging changes the label landscape.
- The `AskUserQuestion` tool supports a maximum of 4 options. Pagination uses 3 items per page + "Show more" or "Skip all".
- The "split" operation (extracting common content into a new third file) is not supported in this version. It can be added later if needed.
