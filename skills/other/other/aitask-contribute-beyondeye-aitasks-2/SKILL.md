---
name: aitask-contribute
description: Contribute changes back to repositories by opening structured issues (GitHub, GitLab, or Bitbucket). Supports both aitasks framework contributions and project-specific contributions.
user-invocable: true
---

## Workflow

### Step 0: Target Selection

Use `AskUserQuestion`:
- Question: "What would you like to contribute to?"
- Header: "Target"
- Options:
  - "aitasks framework" (description: "Contribute improvements to the aitasks framework itself")
  - "This project" (description: "Contribute changes to the project's own codebase")

If "aitasks framework" → set `target_mode = framework`. Proceed to **Step 1**.
If "This project" → set `target_mode = project`. Proceed to **Step 0a**.

**Convention:** When `target_mode = project`, append `--target project` to all `aitask_contribute.sh` invocations in subsequent steps.

### Step 0a: Code Areas Check (project mode only)

Check if the project has a code areas map:

```bash
./.aitask-scripts/aitask_contribute.sh --list-areas --target project
```

**If the command succeeds:** Parse the output. First line: `MODE:project`. Second line: `TARGET:project`. Subsequent lines: `AREA|<name>|<path>|<description>|<parent>` — one per area. Store the areas. Proceed to **Step 2**.

**If the command fails** (exit code non-zero, `NO_CODE_AREAS` on stderr — no `code_areas.yaml` found): Proceed to **Codemap Generation Sub-workflow**.

#### Codemap Generation Sub-workflow

This workflow generates `aitasks/metadata/code_areas.yaml` incrementally. It is designed for multi-pass operation to manage context window.

1. **Scan directory structure:**
   ```bash
   ./.aitask-scripts/aitask_codemap.sh --scan
   ```
   If a partial `code_areas.yaml` already exists, use:
   ```bash
   ./.aitask-scripts/aitask_codemap.sh --scan --existing aitasks/metadata/code_areas.yaml
   ```
   Parse the output YAML skeleton. It contains area names and paths but placeholder descriptions.

2. **Generate descriptions for each unmapped area:**
   For each area (and its children) in the skeleton:
   a. Read 2-3 representative files in the area's directory (README, main entry point, config files)
   b. Generate a meaningful 1-sentence description based on the code
   c. If the area has children in the skeleton, repeat for each child

3. **Save progress:** Write the updated `code_areas.yaml` with real descriptions to `aitasks/metadata/code_areas.yaml`. Save periodically during large scans to avoid context loss.

4. **Commit:**
   ```bash
   ./ait git add aitasks/metadata/code_areas.yaml
   ./ait git commit -m "ait: Generate code areas map"
   ```

5. **Post-scan checkpoint:** Use `AskUserQuestion`:
   - Question: "Code areas map generated. How would you like to proceed?"
   - Header: "Continue"
   - Options:
     - "Continue with contribute workflow" (description: "Proceed to area selection and contribution")
     - "Abort (resume later in fresh context)" (description: "File is committed and available next session")
   - If "Abort" → end workflow
   - If "Continue" → re-run `--list-areas --target project` to load the new areas, proceed to **Step 2**

### Step 1: Prerequisites Check (framework mode only)

> **Skip this step** when `target_mode = project` — area detection was already handled in Step 0a.

Detect contribution mode and list available areas (this also validates the environment):

```bash
./.aitask-scripts/aitask_contribute.sh --list-areas
```

Parse the output:
- First line: `MODE:<clone|downstream>` — contribution mode
- Subsequent lines: `AREA|<name>|<dirs>|<description>` — one per available area

Inform user: "Detected contribution mode: **clone/fork**" or "Detected contribution mode: **downstream project**".

### Step 2: Area Selection

#### Framework mode

Use `AskUserQuestion` with `multiSelect: true`:
- Question: "Which areas of the framework did you modify?"
- Header: "Areas"
- Options: Each area from `--list-areas` output. Label = area name, description = area description + directories. If more than 4 areas, paginate (3 per page + "Show more").
- Add "Other (custom path)" option (description: "Specify a custom directory path")

If "Other" selected: Use `AskUserQuestion` to ask "Enter the custom directory path to scan for changes:" with header "Path" (free text via "Other" option). Store as `--area-path` instead of `--area`.

#### Project mode (hierarchical drill-down)

Present top-level areas from the Step 0a output (areas where the parent field is empty).

Use `AskUserQuestion` with `multiSelect: true`:
- Question: "Which areas of the project did you modify?"
- Header: "Areas"
- Options: Each top-level area. Label = area name, description = area description + path. If more than 4 areas, paginate (3 per page + "Show more").
- Add "Other (unlisted area)" option (description: "Specify an area not in the code map")

**Hierarchical drill-down:** When a selected top-level area has children (check the stored areas from Step 0a), drill down:
```bash
./.aitask-scripts/aitask_contribute.sh --list-areas --target project --parent <area-name>
```

Use `AskUserQuestion` with `multiSelect: true`:
- Question: "Select sub-areas within <area-name>:"
- Header: "Sub-areas"
- Options: Each child area (label = name, description = description + path) + "Use all of <area-name>" (description: "Include all sub-areas") + "Other (unlisted sub-area)" (description: "Specify a sub-area not in the code map")

**If "Other (unlisted area)" or "Other (unlisted sub-area)" selected:**
- Use `AskUserQuestion` to ask for the directory path and a brief 1-sentence description
- Use `--area-path` for this area in subsequent script calls
- Store the path and description for the **dynamic area update** after contribution (see Step 7)

### Step 3: File Discovery

For each selected area, run:

```bash
./.aitask-scripts/aitask_contribute.sh --list-changes --area <area>
```

(Add `--target project` for project mode. Use `--area-path <path>` for custom paths.)

Collect all changed file paths across areas.

**If no changed files found:** Inform user: "No changes detected in the selected areas compared to upstream." Abort.

**If files found:** Present changed files to user via `AskUserQuestion` with `multiSelect: true`:
- Question: "These files have changes. Select the files you want to contribute:"
- Header: "Files"
- Options: Each file path as a selectable option. If more than 4 files, paginate (3 per page + "Show more" option).

Store selected files for subsequent steps.

### Step 4: Upstream Diff + AI Analysis

For the confirmed files, generate the diff via dry-run:

```bash
./.aitask-scripts/aitask_contribute.sh --dry-run --area <area> \
  --files "<file1,file2,...>" \
  --title "placeholder" --motivation "placeholder" \
  --scope enhancement --merge-approach "clean merge"
```

(Add `--target project` for project mode.)

Read the generated issue body from stdout. It contains the full diffs embedded in markdown.

**AI analysis:** Analyze the diffs and present a structured summary:

```
## Changes Summary
- **Mode:** <clone|downstream|project>
- **Files:** N files across M areas
- **Change groups:** (AI-identified logical groups)
  - Group 1: <description> (files: ...)
  - Group 2: <description> (files: ...)
```

Assess:
- What changed in each file (semantic understanding)
- Whether changes are logically related (one feature) or distinct (multiple contributions)
- Appropriate scope classification per change group
- Merge complexity

### Step 5: Contribution Grouping

**If only one logical group identified:** Skip this step. Proceed with all files as one contribution.

**If multiple distinct groups identified:** Use `AskUserQuestion`:
- Question: "These changes appear to cover multiple distinct improvements. Would you like to split them into separate contributions?"
- Header: "Grouping"
- Options:
  - "Split into N separate contributions" (description: "One issue per logical change group")
  - "Keep as single contribution" (description: "Submit all changes in one issue")
  - "Custom grouping" (description: "Manually adjust which files go in which contribution")

If "Custom grouping": Use follow-up `AskUserQuestion` interactions to let user assign files to groups.

Each group becomes a separate issue in Step 7.

### Step 6: Motivation and Scope per Contribution

For each contribution group (loop if multiple):

**Title:** Use `AskUserQuestion`:
- Question: "Proposed title for this contribution. Confirm or modify:"
- Header: "Title"
- Options:
  - AI-proposed title based on diff analysis
  - "Other" for free text modification

**Motivation:** Use `AskUserQuestion`:
- Question: "Why should this change be contributed? What problem does it solve or what value does it add?"
- Header: "Motivation"
- Options: free text only (use "Other")

**Scope:** Use `AskUserQuestion`:
- Question: "What type of change is this?"
- Header: "Scope"
- Options:
  - "Bug fix" (description: "Fixes incorrect behavior") — maps to `bug_fix`
  - "Enhancement" (description: "Improves existing functionality") — maps to `enhancement`
  - "New feature" (description: "Adds entirely new capability") — maps to `new_feature`
  - "Documentation" (description: "Documentation improvements") — maps to `documentation`

**Merge approach:** Use `AskUserQuestion`:
- Question: "Proposed merge approach for upstream maintainers:"
- Header: "Merge"
- Options:
  - AI-proposed approach based on change complexity (description: "Based on diff analysis")
  - "Clean merge" (description: "Standard merge, no conflicts expected")

### Step 7: Review, Confirm, and Create Issue(s)

For each contribution (loop if multiple):

**Generate final preview:**

```bash
./.aitask-scripts/aitask_contribute.sh --dry-run --area <area> \
  --files "<files>" \
  --title "<title>" --motivation "<motivation>" \
  --scope <scope> --merge-approach "<approach>"
```

(Add `--target project` for project mode.)

Present the issue body preview to the user.

**Confirm:** Use `AskUserQuestion`:
- Question: "Create this contribution issue on the repository?"
- Header: "Confirm"
- Options:
  - "Create issue" (description: framework mode → "Submit to beyondeye/aitasks", project mode → "Submit to <project-repo>" where project-repo is auto-detected from `git remote get-url origin`)
  - "Edit" (description: "Go back and modify title, motivation, or scope")
  - "Abort" (description: "Cancel this contribution")

**Handle selection:**

- **"Create issue":** Run without `--dry-run`:
  ```bash
  ./.aitask-scripts/aitask_contribute.sh --area <area> \
    --files "<files>" \
    --title "<title>" --motivation "<motivation>" \
    --scope <scope> --merge-approach "<approach>" --silent
  ```
  (Add `--target project` for project mode.)
  The output is the issue URL. Display to user.

- **"Edit":** Loop back to Step 6 for this contribution.

- **"Abort":** Skip this contribution, continue to next (if any).

**Dynamic area update (project mode only):** If any "Other (unlisted area)" or "Other (unlisted sub-area)" was selected in Step 2 and the contribution was created successfully:
- Read the current `aitasks/metadata/code_areas.yaml`
- Append the new area entry (as a top-level area, or as a child of the selected parent area)
- Use the path and description collected in Step 2
- Commit:
  ```bash
  ./ait git add aitasks/metadata/code_areas.yaml
  ./ait git commit -m "ait: Add code area <area-name>"
  ```

**After all contributions processed:** Display summary:

```
## Contribution Summary
- Issue #X: <title> — <url>
- Issue #Y: <title> — <url>

When these issues are imported via /aitask-contribution-review,
your Co-authored-by attribution will be preserved in implementation commits.
```

---

## Notes

- **Target selection:** Step 0 determines the target. Framework mode contributes to the upstream aitasks repo (beyondeye/aitasks). Project mode contributes to the project's own repo (auto-detected from `git remote get-url origin`).
- **Codemap generation:** When `code_areas.yaml` is missing in project mode, the Codemap Generation Sub-workflow scans the directory structure and generates AI descriptions. This is a multi-pass operation designed to manage context — the post-scan checkpoint allows aborting and resuming in a fresh context.
- **`--target project` flag:** In project mode, all `aitask_contribute.sh` invocations include `--target project`. This switches area listing to read from `code_areas.yaml`, uses `git diff main` for change detection, and targets the project's own repo for issue creation.
- **`--parent` flag:** Used for hierarchical drill-down in project mode. `--list-areas --target project --parent <area>` returns only children of the specified area.
- **Dynamic area updates:** When the user selects "Other (unlisted area)" during project-mode contribution, the new area is added to `code_areas.yaml` after the contribution completes. This keeps the code map up-to-date without requiring a full rescan.
- **Project mode output:** `--list-areas --target project` outputs `MODE:project` + `TARGET:project` + `AREA|<name>|<path>|<description>|<parent>` lines (4 fields per AREA, unlike framework mode's 3 fields). The parent field is empty for top-level areas.
- This skill creates issues on repositories (GitHub by default, also supports GitLab and Bitbucket via `--source`) — it does NOT create local aitasks
- The script supports three platforms: GitHub (`gh` CLI), GitLab (`glab` CLI), and Bitbucket (`bkt` CLI)
- When using a non-default platform, pass `--source gitlab` or `--source bitbucket` to all script invocations
- No execution profiles are used (unlike aitask-pick, aitask-explore, and aitask-pr-import)
- No remote sync step needed
- No handoff to task-workflow
- The `--list-areas` output format (framework mode): first line `MODE:<mode>`, then `AREA|<name>|<dirs>|<description>` per area
- The `--list-changes` output format: one file path per line
- The `--dry-run` flag outputs the full issue markdown body to stdout
- Without `--dry-run` and with `--silent`, the script outputs only the issue URL
- Scope values map: "Bug fix" -> `bug_fix`, "Enhancement" -> `enhancement`, "New feature" -> `new_feature`, "Documentation" -> `documentation`. The "Other" option via AskUserQuestion maps to `other`
- Additional script flags available but not used interactively: `--area-path` (for custom paths), `--repo` (override upstream repo), `--diff-preview-lines` (control diff truncation), `--source` (target platform)
