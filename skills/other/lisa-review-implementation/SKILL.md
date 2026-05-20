---
name: lisa-review-implementation
description: This skill should be used when comparing a project's Lisa-managed files against Lisa's source templates to identify drift. It reads the project manifest, locates source templates, generates diffs for drifted files, and offers to upstream improvements back to Lisa.
---

# Lisa Implementation Review

This skill compares the current project's Lisa-managed files against Lisa's source templates to identify drift and offer to upstream improvements back to Lisa.

## Prerequisites

This skill requires access to the Lisa installation directory. Either:
1. Start Claude Code with `--add-dir ~/lisa` (or your Lisa path)
2. Pass the Lisa directory as an argument: `/lisa-review-implementation ~/lisa`

## Instructions

### Step 1: Locate Lisa Directory

First, determine the Lisa installation directory:

1. If an argument was provided, use that path
2. Otherwise, check if any `--add-dir` paths contain a `src/core/lisa.ts` file (Lisa's signature file)
3. Common locations to check: `~/lisa`, `~/workspace/lisa`, `../lisa`

If Lisa directory cannot be found, inform the user:
```
Unable to locate Lisa installation directory.

Please either:
1. Start Claude Code with: claude --add-dir /path/to/lisa
2. Run this command with the path: /lisa-review-implementation /path/to/lisa
```

### Step 2: Read the Manifest

Read the project's `.lisa-manifest` file to get the list of managed files.

Parse each line to extract:
- `strategy`: The copy strategy used (copy-overwrite, copy-contents, merge, create-only)
- `relativePath`: The file path relative to project root

Skip:
- Lines starting with `#` (comments)
- Empty lines
- Files with `create-only` strategy (these are meant to be customized)
- Files with `merge` strategy (these are intentionally combined)

### Step 3: Find Source Templates

For each managed file, locate its source in Lisa by checking these directories in order:
1. `npm-package/copy-overwrite/` and `npm-package/copy-contents/`
2. `cdk/copy-overwrite/` and `cdk/copy-contents/`
3. `nestjs/copy-overwrite/` and `nestjs/copy-contents/`
4. `expo/copy-overwrite/` and `expo/copy-contents/`
5. `typescript/copy-overwrite/` and `typescript/copy-contents/`
6. `all/copy-overwrite/` and `all/copy-contents/`

The FIRST match wins (most specific type takes precedence).

Detect which project types apply by checking the project for:
- `npm-package`: package.json without `"private": true` AND has `main`, `bin`, `exports`, or `files`
- `cdk`: presence of `cdk.json` or `aws-cdk` in dependencies
- `nestjs`: presence of `nest-cli.json` or `@nestjs` in dependencies
- `expo`: presence of `app.json`, `eas.json`, or `expo` in dependencies
- `typescript`: presence of `tsconfig.json` or `typescript` in dependencies

Only check type directories that match the project.

### Step 4: Compare Files

For each file, compare the project version against the Lisa source:

1. Read both files
2. If identical, mark as "in sync"
3. If different, generate a diff summary

Use the Bash tool with `diff` to generate readable diffs:
```bash
diff -u "/path/to/lisa/source" "/path/to/project/file" || true
```

### Step 5: Generate Report

Create a markdown report with these sections:

```markdown
# Lisa Implementation Review

**Project:** [project name from package.json]
**Lisa Source:** [lisa directory path]
**Generated:** [current date/time]

## Summary

- **Total managed files:** X
- **In sync:** X
- **Drifted:** X
- **Source not found:** X

## Drifted Files

### [relative/path/to/file]

**Source:** [lisa-type]/copy-overwrite/[path]
**Strategy:** copy-overwrite

<details>
<summary>View diff</summary>

```diff
[diff output]
```

</details>

**Recommendation:** [Brief analysis of whether this change should be upstreamed]

---

[Repeat for each drifted file]

## Files Not Found in Lisa

These files are in the manifest but their source templates couldn't be located:

- [list of files]

## In Sync Files

<details>
<summary>X files are in sync with Lisa</summary>

- [list of files]

</details>
```

### Step 6: Offer to Upstream Changes

After presenting the report, ask the user which drifted files they want to copy back to Lisa.

For each file the user wants to upstream:

1. Confirm the target path in Lisa (e.g., `typescript/copy-overwrite/.github/workflows/ci.yml`)
2. Use the Write tool to copy the project's version to Lisa
3. Report success

Example prompt:
```
I found X files that have drifted from Lisa's templates.

Which files would you like to copy back to Lisa?
1. .github/workflows/ci.yml - [brief description of changes]
2. .claude/settings.json - [brief description of changes]
3. All of the above
4. None - just show me the report

Select an option (or list specific numbers):
```

### Important Notes

- **Never auto-upstream without confirmation** - always ask the user first
- **Preserve the most specific type directory** - if a file exists in both `typescript/` and `all/`, upstream to where it currently exists
- **Handle binary files gracefully** - skip comparison for non-text files
- **Respect .gitignore patterns** - some generated files shouldn't be compared
- For `copy-contents` files like `.gitignore`, the comparison is trickier since the project may have additional lines - highlight only if Lisa's required lines are missing

## Example Usage

```
User: /lisa-review-implementation

Claude: I'll review your project's Lisa-managed files against the Lisa source templates.

[Locates Lisa directory]
[Reads manifest]
[Compares files]
[Generates report]

# Lisa Implementation Review

**Project:** my-awesome-app
**Lisa Source:** /Users/dev/lisa
**Generated:** 2026-01-18 10:30:00

## Summary

- **Total managed files:** 45
- **In sync:** 42
- **Drifted:** 3
- **Source not found:** 0

## Drifted Files

### .github/workflows/ci.yml

**Source:** typescript/copy-overwrite/.github/workflows/ci.yml
**Strategy:** copy-overwrite

[diff details]

**Recommendation:** This adds a new caching step that improves CI performance. Good candidate for upstreaming.

---

I found 3 files that have drifted. Would you like to upstream any of these changes back to Lisa?
```
