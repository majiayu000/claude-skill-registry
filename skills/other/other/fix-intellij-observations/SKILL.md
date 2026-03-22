---
name: fix-intellij-observations
description: "Fix IntelliJ observations in changed files. Use when the user asks to fix IntelliJ observations, warnings, inspections, or code problems. No need to list specific warnings — the skill discovers them automatically."
user-invocable: true
---

# Fix IntelliJ Observations

Fix all IntelliJ IDEA observations (both warnings AND errors) in changed files. The skill automatically discovers which files to check and what problems exist — the user does NOT need to list specific warnings or errors.

## Workflow

### Step 1: Identify changed files

Determine which files need inspection using the following priority:

#### Priority 1 — Changed but not staged files

Run `git diff --name-only` (unstaged changes) and `git diff --cached --name-only` (staged changes). If either returns results, use that combined set of files as the target list.

#### Priority 2 — Diff against base branch

If there are NO unstaged or staged changes (working tree is clean), fall back to comparing against the base branch:

1. **Try to detect the base branch from a pull request.** Run:
   ```bash
   gh pr view --json baseRefName --jq '.baseRefName' 2>/dev/null
   ```
   If this succeeds and returns a branch name, use that as the base branch.

2. **If no PR exists** (the command fails or returns empty), detect the repository's default branch:
   ```bash
   gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name' 2>/dev/null
   ```
   If this succeeds, use the returned branch name. Otherwise, fall back to `develop`.

3. Get the changed files:
   ```bash
   git diff <base-branch>...HEAD --name-only
   ```

#### Filtering

After obtaining the file list from either priority path:
- Filter out deleted files (i.e., files that no longer exist on disk).
- Filter to only `.java` files.
- Exclude any files under `core/src/main/java/com/jetbrains/youtrackdb/internal/core/sql/parser/` (these are generated).

If no files remain after filtering, inform the user and stop.

### Step 2: Get problems for each file

For each changed Java file, call `mcp__jetbrains__get_file_problems` with:
- `filePath`: the file path relative to the project root
- `errorsOnly`: **false** (IMPORTANT: must be false to include both warnings AND errors)
- `projectPath`: the project root path

Process files in parallel where possible to speed up analysis.

If no problems are found across all files, inform the user and stop.

### Step 3: Fix the problems

For each reported problem:
1. Read the file to understand the context around the problem location
2. Determine the appropriate fix based on the problem description and severity
3. Apply the fix using the Edit tool or `mcp__jetbrains__replace_text_in_file`
4. If a problem is unclear or the fix would change behavior, ask the user before proceeding

Common fixes include:
- Adding missing `@Override` annotations
- Removing unused imports or variables
- Fixing null-safety issues (adding null checks, using `@Nullable`/`@NotNull`)
- Replacing raw types with parameterized types
- Fixing redundant casts or type arguments
- Addressing deprecation warnings
- Fixing resource leak warnings (try-with-resources)
- Correcting access modifier visibility

### Step 4: Verify fixes

After applying fixes, re-run `mcp__jetbrains__get_file_problems` (with `errorsOnly: false`) on each modified file to confirm all observations are resolved. If new problems were introduced, fix those too.

### Step 5: Build validation

Run `mcp__jetbrains__build_project` to ensure the fixes compile correctly. If build errors occur, fix them before finishing.

## Important Notes

- The user does NOT need to paste or list specific warnings/errors — this skill discovers them automatically.
- Always set `errorsOnly` to `false` when calling `get_file_problems` — the goal is to fix ALL observations, not just errors.
- Do not modify generated code (SQL parser files, Gremlin DSL files).
- Preserve existing code style: 2-space indent, 100-char line width, braces always required.
- If a warning is a false positive or intentional, add a suppression annotation (`@SuppressWarnings`) with a comment explaining why.
