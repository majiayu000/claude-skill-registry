---
name: dev-markdown-lint
description: Check and fix markdown formatting issues with markdownlint-cli2
argument-hint: "[--fix]"
disable-model-invocation: false
---

Check markdown files for formatting and style issues using markdownlint-cli2.

**When to use this skill:**

- Before committing changes to markdown files
- After creating or updating lessons, READMEs, or documentation
- When CI markdown linting checks fail
- To ensure consistent markdown style across the project

**AI auto-invocation:**

The model should automatically invoke this skill:

- **After creating/updating markdown files** — Run `npx markdownlint-cli2 "**/*.md"` to check
- **Before git commits touching markdown** — Verify no linting errors
- **If errors found** — Attempt auto-fix with `--fix` flag first, then fix remaining errors manually
- **Always verify after fixes** — Re-run to ensure all errors resolved

## Arguments

- `--fix` (optional): Automatically fix auto-fixable issues

If no arguments provided, runs in check-only mode.

## What it does

1. **Check mode** (default): Reports errors without modifying files
2. **Fix mode** (`--fix`): Automatically fixes issues like:
   - Missing blank lines around headings
   - Inconsistent list formatting
   - Trailing whitespace
   - Some language tag issues (if the content type is obvious)

**Note:** Not all errors are auto-fixable. Some require manual intervention (like choosing the right language tag for a code block).

## Configuration

The project uses `.markdownlint-cli2.jsonc` for configuration:

**Strict rules (must follow):**

- **MD040**: Code blocks MUST have language tags (`` ```text ``, `` ```c ``, `` ```bash ``, etc.)
- **MD060**: Tables must have consistent column alignment

**Lenient rules:**

- Line length (MD013): Disabled — lessons need flexibility
- Blank lines (MD031/MD032): Lenient — formatting varies by context
- Duplicate headings (MD024): Allowed at different levels
- HTML (MD033): Allowed when needed for formatting

**CRITICAL — Configuration is non-negotiable:**

- **NEVER** disable or remove lint rules to make errors pass
- **NEVER** relax existing rules (e.g., turning MD040 from error to warning)
- **NEVER** modify `.markdownlint-cli2.jsonc` to bypass validation
- **NEVER** remove or disable the CI workflow (`.github/workflows/markdown-lint.yml`)

If linting fails, fix the markdown — do not weaken the linter. Quality checks
protect learning quality for all users.

## Common errors and fixes

### MD040: Missing language tag on code block

**Error:**

```text
README.md:45 MD040/fenced-code-language Fenced code blocks should have a language specified
```

**Problem:** Code block missing language identifier:

````text
```
some code here
```
````

**Fix:** Add appropriate language tag:

````text
```c
some code here
```
````

**Common tags:**

- `bash` — Shell commands, scripts
- `c` — C code
- `text` — Plain text, output, diagrams, directory trees
- `markdown` — Markdown examples
- `cmake` — CMake files
- `hlsl` — Shader code

**Nested code blocks:** When showing a code block inside a code block (like in documentation), use 4 backticks for the outer fence:

`````text
````markdown
# Example
```c
code here
```
````
`````

### MD060: Table columns should have consistent alignment

**Error:**

```text
README.md:80 MD060/table-column-count Table row column count
```

**Problem:** Table rows have different numbers of columns, or alignment is inconsistent.

**Fix:** Ensure all rows have the same number of columns:

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

## Running the skill

### Check for errors

```bash
/dev-markdown-lint
```

Or manually:

```bash
npx markdownlint-cli2 "**/*.md"
```

### Auto-fix issues

```bash
/dev-markdown-lint --fix
```

Or manually:

```bash
npx markdownlint-cli2 --fix "**/*.md"
```

## Workflow

### Before committing

Always run markdown linting before creating a commit with markdown changes:

```bash
npx markdownlint-cli2 "**/*.md"
```

If errors are found:

1. Try auto-fix: `npx markdownlint-cli2 --fix "**/*.md"`
2. Review remaining errors and fix manually
3. Re-run to verify: `npx markdownlint-cli2 "**/*.md"`

### In CI

The `.github/workflows/markdown-lint.yml` workflow runs automatically on:

- Pull requests touching markdown files
- Pushes to main with markdown changes

If CI fails, run the linter locally to see the errors.

## Implementation

When this skill is invoked:

1. **Parse arguments:**
   - Check if `--fix` flag is present
   - Default to check-only mode

2. **Run markdownlint-cli2:**

   ```bash
   npx markdownlint-cli2 [--fix] "**/*.md"
   ```

3. **Interpret results:**
   - Exit code 0: All files pass ✓
   - Exit code 1: Errors found

4. **Report to user:**
   - If errors found: List them with file:line and error code
   - Suggest fixes for common errors (MD040, MD060)
   - If `--fix` was used, report what was auto-fixed
   - Show command to re-run manually if needed

5. **Next steps:**
   - If errors remain after auto-fix, guide user to fix manually
   - Suggest running the skill again to verify fixes

## Tips

- **Always add language tags** to code blocks — it improves readability and syntax highlighting
- **Use `text` for non-code blocks** like output, diagrams, directory trees
- **Nested code blocks** require different fence lengths (outer uses 4+ backticks)
- **Run before committing** to catch issues early
- **Auto-fix first** then handle remaining errors manually
- **Check the config** (`.markdownlint-cli2.jsonc`) to understand which rules are enabled

## Example output

**All files pass:**

```text
markdownlint-cli2 v0.20.0 (markdownlint v0.40.0)
Finding: **/*.md
Linting: 20 file(s)
Summary: 0 error(s)
```

**Errors found:**

```text
markdownlint-cli2 v0.20.0 (markdownlint v0.40.0)
Finding: **/*.md
Linting: 20 file(s)
README.md:45 MD040/fenced-code-language Fenced code blocks should have a language specified
lessons/math/01-vectors/README.md:180 MD040/fenced-code-language Fenced code blocks should have a language specified
common/math/DESIGN.md:85 MD040/fenced-code-language Fenced code blocks should have a language specified
Summary: 3 error(s)
```

## Related documentation

- [markdownlint rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- Project config: `.markdownlint-cli2.jsonc`
- CI workflow: `.github/workflows/markdown-lint.yml`
- CLAUDE.md section on markdown linting
