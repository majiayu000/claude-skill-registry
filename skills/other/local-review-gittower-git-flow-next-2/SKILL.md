---
name: local-review
description: Review current changes against project guidelines before PR
allowed-tools: Read, Write, Grep, Glob, Bash
---

# Local Review

Perform a comprehensive self-review of changes before creating a pull request.

## Arguments

`/local-review [target] [--output path]`

### Target (optional)

Specifies what to review. Can be:

- **Nothing** - auto-detect new commits on current branch vs main (default)
- **Commit range** - review specific commits (e.g., `HEAD~3..HEAD`, `abc123..def456`)
- **Single commit** - review one commit (e.g., `HEAD~1`, `abc123`)
- **Branch comparison** - review branch diff (e.g., `main..feature/foo`)

### Output (optional)

`--output path` or `-o path` - where to write the review:

- A folder name within `.ai/` (e.g., `issue-59-add-no-verify-option`)
- A relative path (e.g., `.ai/issue-59-add-no-verify-option`)
- If omitted with auto-detect mode: auto-detects from branch name, writes to `.ai/`
- If omitted with explicit target: outputs directly to conversation (no file)

### Examples

```bash
# Auto-detect new commits vs main (writes to .ai/)
/local-review

# Auto-detect, specify output folder
/local-review --output issue-59-add-no-verify-option
/local-review -o .ai/my-feature

# Review specific commits (outputs to conversation)
/local-review HEAD~3..HEAD
/local-review abc123
/local-review main..feature/foo

# Review commits and save to file
/local-review HEAD~5..HEAD --output code-audit
```

## Instructions

1. **Parse Arguments**
   - Check if a commit/range target was provided
   - Check if `--output` or `-o` flag was provided
   - Determine review mode: "auto-detect" (default) or "explicit"

2. **Gather Context**

   For **auto-detect mode** (no target specified):
   - Get current branch name
   - Find associated workflow folder in `.ai/`
   - Read the original issue/concept and plan if available

   For **explicit mode** (target specified):
   - Validate the commit range/ref exists
   - No workflow folder lookup needed

3. **Detect and Get Changes**

   For **auto-detect mode**:
   - Determine the main branch: run `git config gitflow.branch.main.name` (fallback to `main`)
   - Detect new commits: run `git log <main>..HEAD --oneline`
   - If no new commits exist, inform the user and stop
   - Get the diff for those commits: `git diff <main>...HEAD`
   - List the commits being reviewed

   For **explicit mode**:
   - If range (contains `..`): `git diff <range>` and `git log <range> --oneline`
   - If single commit: `git show <commit> --stat` and `git log -1 <commit>`

   For both modes:
   - List all modified files

4. **Review Against Guidelines**

   Review the code against **[REVIEW_CRITERIA.md](REVIEW_CRITERIA.md)**, which covers:
   - Test coverage
   - Coding guidelines and architecture
   - Code quality
   - Security
   - Documentation
   - Commit messages

5. **Code Quality Checks** (auto-detect mode only)

   Skip this step for explicit mode (reviewing historical commits).

   For auto-detect mode, run:
   ```bash
   # Build check
   go build ./...

   # Test check
   go test ./...

   # Format check
   go fmt ./...

   # Vet check
   go vet ./...
   ```

6. **Determine Output Location**

   **Filename includes revision(s) being reviewed:**

   ```bash
   # For auto-detect mode: use HEAD short SHA
   HEAD_SHA=$(git rev-parse --short HEAD)
   FILENAME="review-${HEAD_SHA}.md"

   # For commit range (abc123..def456): use both endpoints
   START_SHA=$(git rev-parse --short abc123)
   END_SHA=$(git rev-parse --short def456)
   FILENAME="review-${START_SHA}-${END_SHA}.md"

   # For single commit: use that commit's short SHA
   COMMIT_SHA=$(git rev-parse --short abc123)
   FILENAME="review-${COMMIT_SHA}.md"
   ```

   If `--output` / `-o` was provided:
   - If it starts with `.ai/`, use it directly
   - Otherwise, treat it as a folder name within `.ai/` (prepend `.ai/`)
   - Create the folder if it doesn't exist
   - Write to `<folder>/<filename>`

   If no `--output` and **auto-detect mode**:
   - Extract issue number from branch name (e.g., `feature/59-...` → `59`)
   - Look for existing `.ai/issue-<number>-*` folder
   - If no `.ai/` folder exists, create one based on the branch name pattern
   - Write to `<folder>/<filename>`

   If no `--output` and **explicit mode**:
   - Output directly to the conversation (no file written)

   Examples:
   - Auto-detect at HEAD `c9625f7` → `.ai/issue-59-foo/review-c9625f7.md`
   - Range `abc123..def456` with `-o issue-59-foo` → `.ai/issue-59-foo/review-abc123-def456.md`
   - Single commit `abc123` with `-o .ai/my-feature` → `.ai/my-feature/review-abc123.md`
   - Explicit mode, no flag → output to conversation (no file)

7. **Generate Review Report**

   Write the review to file OR output directly to conversation based on step 6.

   Use this format:

   ```markdown
   # Local Review: <branch-name or commit-range>

   ## Summary
   - Revision(s): `<start-sha>` to `<end-sha>` (or single `<sha>`)
   - Files changed: <count>
   - Lines added: <count>
   - Lines removed: <count>
   - Commits reviewed: <count> (list the commit SHAs/subjects)

   ## Checklist Results

   ### Passed
   - <item 1>
   - <item 2>

   ### Must Fix
   - [ ] <issue 1> - <file:line> - <description>
   - [ ] <issue 2> - <file:line> - <description>

   ### Should Fix
   - <item 1>

   ## Quality Checks (auto-detect mode only)
   - Build: PASS/FAIL
   - Tests: PASS/FAIL (<count> passed)
   - Format: PASS/FAIL
   - Vet: PASS/FAIL

   ## Recommendations
   1. <recommendation>
   2. <recommendation>

   ## Ready for PR? (auto-detect mode only)
   <YES/NO - explain if NO>
   ```

   For explicit mode, omit "Quality Checks" and "Ready for PR?" sections.

8. **Report Findings**
   - If issues found, list them with specific file:line references
   - Suggest fixes for each issue
   - For auto-detect mode: indicate if changes are PR-ready
   - For explicit mode: provide code review feedback directly in conversation

## Issue Categories

Categorize findings using the severity levels defined in REVIEW_CRITERIA.md (Must fix, Should fix, Nit).
