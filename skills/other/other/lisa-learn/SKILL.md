---
name: lisa-learn
description: This skill should be used when analyzing a downstream project's git diff after Lisa was applied to identify improvements that should be upstreamed back to Lisa templates. It validates the environment, captures the diff, correlates changes with the manifest, categorizes each change, and offers to upstream improvements.
---

# Lisa Learn

Analyze the git diff in a downstream project after Lisa was applied. Identify improvements the project had that Lisa overwrote, potential breakage, safe overrides, and neutral changes. Offer to upstream improvements back to Lisa templates.

This completes a feedback loop: `/lisa-integration-test` applies and verifies, `/lisa-learn` analyzes the transition for upstream opportunities, and `/lisa-review-project` compares static drift.

## Prerequisites

This skill must be run FROM the Lisa repository directory. The target project must have Lisa applied and have uncommitted changes from a recent Lisa run.

## Instructions

### Step 1: Validate Environment

1. Confirm running from Lisa by checking for `src/core/lisa.ts`.
   - If not in Lisa, error with:
     ```
     This command must be run FROM the Lisa repository.

     Current directory does not contain src/core/lisa.ts.

     Usage: /lisa-learn /path/to/target-project
     ```

2. Extract project path from `$ARGUMENTS`. If not provided, ask the user:
   ```
   Which project would you like to analyze?

   Path: [user provides path]
   ```

3. Validate the project path:
   - Check the path exists and is a directory
   - Check `.lisa-manifest` exists in the project root
   - If missing, error with:
     ```
     Project does not have Lisa applied.

     Expected to find: {project-path}/.lisa-manifest

     Did you apply Lisa to this project? Run: bun run dev {project-path}
     ```

4. Check the project has uncommitted changes: `git -C <project-path> status --porcelain`
   - If clean (no output), stop with:
     ```
     No uncommitted changes found in the project.

     Run `bun run dev <project-path>` first, then re-run /lisa-learn to analyze what changed.
     ```

### Step 2: Read Manifest and Detect Types

1. Read `<project-path>/.lisa-manifest` line by line.
   - Skip lines starting with `#` (comments) and empty lines
   - Parse format: `strategy|relative/path/to/file`
   - Extract `strategy` and `relativePath` for each entry
   - Store as a lookup: `{ [relativePath]: strategy }`

2. Detect project types by checking the project filesystem:
   - **cdk**: `cdk.json` exists OR `aws-cdk` in package.json dependencies
   - **nestjs**: `nest-cli.json` exists OR `@nestjs` in package.json dependencies
   - **expo**: `app.json` exists OR `eas.json` exists OR `expo` in package.json dependencies
   - **typescript**: `tsconfig.json` exists OR `typescript` in package.json dependencies
   - **npm-package**: `package.json` without `"private": true` AND has `main`, `bin`, `exports`, or `files`

3. Build the type hierarchy. Example: if `expo` detected, types = `[all, typescript, expo]`
   - If no types detected, use `[all]`

### Step 3: Capture Git Diff

Run these commands against the project:

1. `git -C <project-path> diff` — full diff for modified tracked files
2. `git -C <project-path> diff --stat` — summary of changes
3. `git -C <project-path> status --porcelain` — identify new/untracked files (`??` prefix) and modified files (`M` prefix)

Store the full diff output and the list of changed files for analysis.

### Step 4: Correlate Diff with Manifest

For each file that appears in the git diff or status output:

1. Look up the file's strategy in the manifest (from Step 2)
2. Find the Lisa source template by checking type directories in reverse hierarchy order (most specific first):
   - `{type}/copy-overwrite/{relativePath}`
   - `{type}/copy-contents/{relativePath}`
   - `{type}/create-only/{relativePath}`
   - Fall back through parent types until found
   - Example for an Expo project: check `expo/` → `typescript/` → `all/`
3. Record the mapping: `{ file, strategy, sourceTemplate, diff }`
4. Flag files NOT in the manifest as "collateral changes" — these are files that Lisa didn't directly manage but were affected (e.g., lockfiles, generated files)

### Step 5: Analyze Each Changed File

Categorize each changed file based on its strategy and the nature of the diff:

| Category | Meaning | Action |
|----------|---------|--------|
| **Upstream Candidate** | Project had something better that Lisa overwrote | Offer to upstream |
| **Potential Breakage** | Lisa's change might break the project | Warn user |
| **Safe Override** | Lisa's update is correct, project was outdated | No action needed |
| **Neutral Change** | Cosmetic/formatting differences | Skip |

**Analysis rules by strategy:**

- **`copy-overwrite` files** (primary targets for learning):
  - In the diff, `-` lines = project's old version (what was there before Lisa), `+` lines = Lisa's replacement
  - Analyze if removed content (`-` lines) represents an improvement over Lisa's version:
    - Better error handling, bug fixes, additional config options, better docs → **Upstream Candidate**
    - Project-specific config (env vars, custom paths, API keys) → **Safe Override** (Lisa correctly replaced)
    - Formatting differences only → **Neutral Change**
  - Check if added content (`+` lines) might break the project:
    - Removes project-required config → **Potential Breakage**
    - Adds conflicting settings → **Potential Breakage**

- **`copy-contents` files**:
  - Only `+` lines (additions are safe, they're new content Lisa added)
  - Note additions but they're typically **Safe Override**

- **`merge` / `package-lisa` files** (e.g., `package.json`):
  - Check if Lisa removed or overwrote project-specific values
  - Removed dependencies the project needs → **Potential Breakage**
  - Updated versions → **Safe Override**
  - Added governance dependencies → **Safe Override**

- **`create-only` files**:
  - These should NOT be modified by Lisa after initial creation
  - If they appear in the diff, flag as unexpected → **Potential Breakage**

- **Collateral changes** (not in manifest):
  - Lockfile changes → **Neutral Change**
  - Other changes → investigate and categorize

### Step 6: Breakage Detection (Optional)

Ask the user if they want to run verification checks:

```
Would you like to run typecheck/lint/test on the project to detect breakage?

1. Yes — run all checks
2. No — skip verification
```

If yes:
1. Detect package manager from lockfile:
   - `bun.lockb` → bun
   - `pnpm-lock.yaml` → pnpm
   - `yarn.lock` → yarn
   - `package-lock.json` → npm
2. Run in order (stop at first failure):
   - `cd <project-path> && <pm> run typecheck`
   - `cd <project-path> && <pm> run lint`
   - `cd <project-path> && <pm> run test`
3. Report results and add any failures to the **Potential Breakage** category

### Step 7: Generate Report

Create a markdown report:

```markdown
# Lisa Learn Report

**Lisa Directory:** {lisa-path}
**Target Project:** {project-path}
**Project Types:** {types}
**Project Name:** {from package.json name or directory basename}
**Generated:** {current date/time ISO}

## Summary

- **Total files changed:** X
- **Upstream Candidates:** X
- **Potential Breakage:** X
- **Safe Overrides:** X
- **Neutral Changes:** X
- **Collateral Changes:** X

## Upstream Candidates

These files had improvements that Lisa overwrote. Consider adopting them back into Lisa templates.

### {relative/path/to/file}

**Source Template:** {type}/copy-overwrite/{path}
**Strategy:** copy-overwrite

<details>
<summary>View diff (- = project's version, + = Lisa's version)</summary>

\`\`\`diff
{diff output}
\`\`\`

</details>

**Analysis:** {Why the project's version was better and what should be upstreamed}

---

[Repeat for each upstream candidate]

## Potential Breakage

These changes might break the project. Review carefully.

### {relative/path/to/file}

**Source Template:** {type}/copy-overwrite/{path}
**Strategy:** copy-overwrite

<details>
<summary>View diff</summary>

\`\`\`diff
{diff output}
\`\`\`

</details>

**Risk:** {What might break and why}

---

[Repeat for each potential breakage]

## Safe Overrides

These are correct template updates where Lisa's version is an improvement over the project's outdated version.

<details>
<summary>X files safely updated</summary>

- {file1} — {brief reason}
- {file2} — {brief reason}

</details>

## Neutral Changes

<details>
<summary>X files with cosmetic/formatting differences</summary>

- {file1}
- {file2}

</details>

## Collateral Changes

Files not in the manifest that were affected:

- {file1} — {brief description}
```

### Step 8: Offer to Upstream

For each **Upstream Candidate**, offer to copy the project's pre-Lisa version back into the corresponding Lisa template:

```
I found X upstream candidates. Would you like to upstream any improvements back to Lisa?

[List files with brief descriptions]

Options:
1. Upstream all candidates
2. Select specific files to upstream
3. Review candidates in detail first
4. Skip — no changes to Lisa
```

If the user wants to upstream:

1. For each selected file, get the project's pre-Lisa version:
   ```bash
   git -C <project-path> show HEAD:<relativePath>
   ```
2. Determine the target Lisa template path from the Step 4 mapping
3. Confirm with user: "Copy project's version of `{relativePath}` to `{sourceTemplate}`?"
4. If confirmed, write the pre-Lisa content to the Lisa template file using the Write tool
5. Report success for each file

### Step 9: Handle Breakage

If any **Potential Breakage** items were identified, offer options:

```
I found X potential breakage items. How would you like to handle them?

Options:
1. Fix in Lisa templates (upstream the fix)
2. Fix in project local overrides (*.local.* files)
3. Review each breakage item
4. Skip — handle manually later
```

For option 1 (fix upstream): Analyze the breakage, determine the fix, apply it to the Lisa template, and report.

For option 2 (fix in project): Identify the appropriate local override file (e.g., `tsconfig.local.json`, `eslint.config.local.ts`, `jest.config.local.ts`) and apply the fix there.

## Important Notes

- **Never auto-upstream without confirmation** — always ask the user before modifying Lisa templates
- **Pre-Lisa content comes from git** — use `git -C <project-path> show HEAD:<path>` to get the committed version before Lisa's uncommitted changes
- **Preserve the most specific type directory** — if a template exists in `expo/copy-overwrite/`, upstream there, not to `all/copy-overwrite/`
- **Handle missing files gracefully** — if a file appears in the diff but not in the manifest, it's a collateral change
- **Compare carefully** — some differences may be platform-specific (line endings, env vars) and should NOT be upstreamed
- **Retry loop is bounded** — if fixing breakage requires more than 3 iterations, stop and report the situation to the user
- **This skill is Lisa-only** — it is NOT distributed to downstream projects via `all/copy-overwrite/`
