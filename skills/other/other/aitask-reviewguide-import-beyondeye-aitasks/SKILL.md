---
name: aitask-reviewguide-import
description: Import external content (file, URL, or repository directory) as a reviewguide with proper metadata.
---

## Workflow

### Step 1: Input Resolution

If this skill is invoked with an argument (e.g., `/aitask-reviewguide-import https://github.com/org/repo/blob/main/docs/style.md`), use the argument as the source. Proceed to **Step 1b**.

If invoked without arguments (`/aitask-reviewguide-import`), use `AskUserQuestion`:
- Question: "Enter the source to import (file path, URL, or repository directory URL):"
- Header: "Source"
- Options:
  - "Enter file path" (description: "Local file path, e.g., docs/coding-standards.md")
  - "Enter URL" (description: "URL to a markdown file or repository file/directory (GitHub, GitLab, Bitbucket)")

The user enters the actual path or URL via the "Other" free text input or by selecting an option and providing details.

#### 1b: Detect Source Type

Classify the source argument:

- **Local file:** Starts with `/`, `~`, or `./`, OR does not contain `://` and exists as a local file
- **Repository single file:** Contains `github.com` and `/blob/`, OR `gitlab.com` and `/-/blob/`, OR `bitbucket.org` and `/src/` where the last path segment has a file extension (contains `.`)
- **Repository directory:** Contains `github.com` and `/tree/`, OR `gitlab.com` and `/-/tree/`, OR `bitbucket.org` and `/src/` where the last path segment has no file extension
- **Generic URL:** Contains `://` but does not match the repository patterns above

#### 1c: Fetch Content

**Local file:**
- Read the file directly using the Read tool
- Store the file path as the `source_url` value

**Repository single file:**
- Fetch the file content using the `repo_fetch.sh` helper library:
  ```bash
  source .aitask-scripts/lib/repo_fetch.sh && repo_fetch_file "URL"
  ```
  This handles GitHub, GitLab, and Bitbucket URLs internally, using platform CLI tools (`gh`, `glab`) with automatic fallback to `curl` on raw URLs.
- If the Bash command fails, fall back to `WebFetch` with the platform-specific raw URL:
  - GitHub: replace `github.com` with `raw.githubusercontent.com` and remove `/blob`
  - GitLab: replace `/blob/` with `/-/raw/` (or `/-/blob/` with `/-/raw/`)
  - Bitbucket: replace `/src/` with `/raw/`
- Store the original URL as the `source_url` value

**Repository directory:**
- List markdown files using the `repo_fetch.sh` helper library:
  ```bash
  source .aitask-scripts/lib/repo_fetch.sh && repo_list_md_files "URL"
  ```
  This handles GitHub, GitLab, and Bitbucket directory listings internally. Requires `jq`. GitHub requires `gh` CLI; GitLab and Bitbucket fall back to public REST APIs via `curl`.
- If markdown files are found, proceed to **Step 7** (Batch Mode)
- If no markdown files found, inform the user: "No markdown files found in the directory." and end the workflow

**Generic URL:**
- Fetch content using `WebFetch` with prompt: "Extract the complete text content of this page, preserving markdown formatting, headings, and bullet points. Return the full content without summarizing."
- Store the URL as the `source_url` value

### Step 2: Content Analysis

Analyze the fetched content:

1. Identify the document type:
   - Coding standards / style guide
   - Best practices / conventions
   - Architecture / design guidelines
   - Workflow / process document
   - Security guidelines
   - Performance guidelines
   - Mixed / other

2. Extract structure:
   - List all H2 (`##`) and H3 (`###`) section headings
   - Count bullet points and actionable items per section

3. Categorize sections:
   - **Review-relevant:** Sections with actionable code review checks (patterns to look for, things to flag, standards to verify)
   - **Non-relevant:** Sections about workflows, project setup, tooling installation, organizational processes, or other content that cannot be rephrased as review instructions

Present the analysis to the user:

```
## Source Analysis

**Source:** <url_or_path>
**Document type:** <identified type>
**Total sections:** <N>

**Review-relevant sections:** (<count>)
- <heading 1> — <brief description of what it covers>
- <heading 2> — <brief description>
...

**Non-relevant sections (will be skipped):** (<count>)
- <heading> — <reason for skipping, e.g., "workflow/process", "tooling setup">
...
```

### Step 3: Transform Content

Rephrase the review-relevant content into reviewguide-compatible format:

1. **Structure:** All content goes under a single `## Review Instructions` heading, organized by H3 (`###`) topic sections

2. **Bullet format:** Convert all content into actionable review check bullet points using the established tone:
   - "Check that..." — for verifying a standard is followed
   - "Flag..." — for identifying antipatterns or violations
   - "Look for..." — for patterns that may indicate issues
   - "Verify that..." — for confirming expected behavior

3. **Content rules:**
   - Convert narrative paragraphs into specific, actionable bullets
   - Preserve technical specifics: exact patterns, function names, antipatterns, code examples
   - Remove non-actionable content (explanations of "why", historical context, motivation)
   - Merge redundant points that say the same thing differently
   - Each bullet should describe one specific thing to check during code review
   - Keep inline code examples where they clarify what to look for (e.g., "Flag use of `eval()` for parsing user input")

4. **Section organization:**
   - Group related checks under descriptive H3 headings
   - Keep sections focused (5-15 bullets per section is typical)
   - Use clear, scannable heading names (e.g., "### Error Handling", "### Naming Conventions")

### Step 4: Determine Placement

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

Based on the content analysis and transformed content, assign metadata:

**`name`:** Short descriptive name for the guide (e.g., "React Best Practices", "Go Error Handling"). Title case.

**`description`:** One-line description of what the guide checks during review (e.g., "Check React component patterns, hooks usage, and performance pitfalls").

**`reviewtype`:** Select the single best-fitting value from `reviewtypes.txt`. Strongly prefer existing values. The available types are: `bugs`, `code-smell`, `conventions`, `deprecations`, `performance`, `security`, `style`.

**`reviewlabels`:** Select 3-6 values from `reviewlabels.txt` that describe the guide's distinct topics. Each label should correspond to a theme covered in the content. Strongly prefer existing labels.

**`environment`:** Determine if the content is language/framework-specific or universal:
- If universal (applies to any language) → place in `general/` subdirectory, do NOT set `environment` field
- If language-specific → select one or more values from `reviewenvironments.txt`, place in the matching subdirectory (e.g., `python/`, `kotlin/`, `shell/`)
- If the needed subdirectory doesn't exist, it will be created

**`source_url`:** The original URL or file path stored in Step 1c. This field is for reference only — the review skill does not read it.

**Filename:** Generate a filename following the convention: `<topic>_<descriptor>.md` (lowercase, underscores, no spaces). Examples: `react_best_practices.md`, `go_error_handling.md`, `security_headers.md`.

**Full path:** `aireviewguides/<subdirectory>/<filename>`

### Step 5: Preview and Confirm

Show the user the complete generated reviewguide file including frontmatter and markdown body, plus the proposed file path:

```
## Import Preview

**Target path:** aireviewguides/<subdir>/<filename>.md

---
name: <name>
description: <description>
reviewtype: <type>
reviewlabels: [<labels>]
environment: [<envs>]  # omitted if general
source_url: <original_url_or_path>
---

## Review Instructions

### <Section 1>
- <bullet 1>
- <bullet 2>
...

### <Section 2>
- <bullet 1>
...
```

Use `AskUserQuestion`:
- Question: "Review the imported guide above. How would you like to proceed?"
- Header: "Import"
- Options:
  - "Save as proposed" (description: "Write the file and proceed to similarity check")
  - "Edit before saving" (description: "Make adjustments to the content or metadata before writing")
  - "Cancel" (description: "Abort this import")

**If "Edit before saving":** Use `AskUserQuestion` to ask what to change (metadata, content, filename, or subdirectory). Apply the modifications and re-show the preview. Loop until the user selects "Save as proposed" or "Cancel".

**If "Cancel":** End the workflow (or continue to the next file in batch mode).

### Step 6: Save and Classify

1. **Create subdirectory if needed:**
   ```bash
   mkdir -p aireviewguides/<subdirectory>
   ```

2. **Write the reviewguide file** to `aireviewguides/<subdirectory>/<filename>.md` using the Write tool.

3. **Run similarity comparison:**
   ```bash
   ./.aitask-scripts/aitask_reviewguide_scan.sh --compare <relative_path>
   ```
   Parse the pipe-delimited output. If the top result has a score >= 5, update the file's frontmatter to add `similar_to: <most_similar_path>`.

4. **Update vocabulary files if new values were used:**
   - If a new `reviewtype` was used:
     ```bash
     echo "<new_value>" >> aireviewguides/reviewtypes.txt && sort -o aireviewguides/reviewtypes.txt aireviewguides/reviewtypes.txt
     ```
   - If new `reviewlabels` were used:
     ```bash
     echo "<new_label>" >> aireviewguides/reviewlabels.txt && sort -o aireviewguides/reviewlabels.txt aireviewguides/reviewlabels.txt
     ```
   - If new `environment` values were used:
     ```bash
     echo "<new_env>" >> aireviewguides/reviewenvironments.txt && sort -o aireviewguides/reviewenvironments.txt aireviewguides/reviewenvironments.txt
     ```

5. **Commit:**
   ```bash
   git add aireviewguides/
   git commit -m "ait: Import reviewguide <filename>"
   ```

6. **Suggest merge if similar:** If `similar_to` was set, inform the user: "This guide is similar to `<similar_to>`. Consider running `/aitask-reviewguide-merge <filename> <similar_file>` to compare and potentially consolidate."

7. **Show summary:**
   ```
   ## Import Complete

   **File:** aireviewguides/<subdir>/<filename>.md
   **Source:** <source_url>
   **Type:** <reviewtype>
   **Labels:** [<reviewlabels>]
   **Environment:** <environment or "universal">
   **Similar to:** <similar_to or "none">
   **Sections:** <N sections>, <M total bullets>
   ```

### Step 7: Batch Mode (for repository directories)

This step is reached from Step 1c when the source is a repository directory containing multiple markdown files.

1. **Show available files:**
   Display the list of markdown files found in the directory.

2. **Ask user to select files:**
   Use `AskUserQuestion` (multiSelect) with pagination (max 4 options per page):

   **Pagination loop:**
   - Start with `current_offset = 0` and `page_size = 3`
   - First page always includes: **"Import all"** option (label: "Import all", description: "Import all N markdown files from this directory")
   - Remaining slots show individual files from the current offset
   - If more files remain: add "Show more files" option (description: "Show next batch (N more available)")

   **If "Import all" selected:** Mark all files for processing.
   **If individual files selected:** Mark only those for processing.
   **If "Show more files" selected:** Increment offset, loop back.

3. **Process each selected file:**
   For each file, fetch its content using `source .aitask-scripts/lib/repo_fetch.sh && repo_fetch_file "URL"` (construct the file URL from the directory URL by replacing `/tree/` or `/-/tree/` or `/src/` directory path with the corresponding file path pattern for the platform) and run Steps 2-6. Each file uses the same repository directory URL as its `source_url` base, with the specific filename appended.

4. **Show batch summary:**
   ```
   ## Batch Import Complete

   **Source directory:** <repository_directory_url>
   **Files imported:** <N>/<total>

   | # | File | Target Path | Type | Similar To |
   |---|------|-------------|------|------------|
   | 1 | source.md | aireviewguides/<path> | <type> | <similar or -> |
   | 2 | ... | ... | ... | ... |

   **New vocabulary added:**
    - reviewlabels: <new labels or "none">
    - reviewtypes: <new types or "none">
    - environments: <new envs or "none">
    ```

### Step 8: Satisfaction Feedback

After the workflow is complete (after Step 6 in single-file mode or Step 7 in batch mode), execute the **Satisfaction Feedback Procedure** (see `.claude/skills/task-workflow/satisfaction-feedback.md`) with `skill_name` = `"reviewguide-import"`.

## Notes

- The argument to this skill is a **source location**: a local file path, a URL to a markdown file, or a repository file/directory URL (GitHub, GitLab, Bitbucket)
- The `source_url` frontmatter field is for reference only. The `aitask-review` skill does NOT read this field — it only uses the markdown body after the frontmatter for review instructions. Do NOT attempt to fetch or read from the `source_url` during reviews.
- Imported files should NOT be added to `.reviewguidesignore` — they are production reviewguide files intended to be used in reviews
- This skill does **not** modify the `seed/` directory. All files are written to `aireviewguides/` only.
- The content transformation (Step 3) is the core value of this skill: converting arbitrary documentation into actionable, bullet-point review checklists that follow the established format and tone of existing guides
- Repository content fetching uses `.aitask-scripts/lib/repo_fetch.sh` which handles GitHub (`gh`), GitLab (`glab`), and Bitbucket (`curl`) with automatic fallbacks. If the Bash command fails, fall back to `WebFetch` with the platform-specific raw URL. Only `github.com`, `gitlab.com`, and `bitbucket.org` are supported (no self-hosted instances)
- Vocabulary files in `aireviewguides/`: `reviewtypes.txt`, `reviewlabels.txt`, `reviewenvironments.txt`. New values are only added to the `aireviewguides/` copies — not to `seed/`
- Commit messages use the `ait:` prefix: `ait: Import reviewguide <filename>`
- Files in `general/` are universal — they should NOT have an `environment` field. Files in other subdirectories should have an `environment` field
- Assign 3-6 `reviewlabels` per file. Strongly prefer existing vocabulary values over creating new ones
- The `AskUserQuestion` tool supports a maximum of 4 options. Pagination uses 3 items per page + "Show more" or "Import all"
