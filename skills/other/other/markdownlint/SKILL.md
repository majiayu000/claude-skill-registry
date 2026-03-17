---
name: markdownlint
description: This skill should be used when users need to format, clean, lint, or validate Markdown files using the markdownlint-cli2 command-line tool. Use this skill for tasks involving Markdown file quality checks, automatic formatting fixes, enforcing Markdown style rules, or identifying Markdown syntax issues.
---

# Markdownlint Skill

This skill provides expertise in using markdownlint-cli2, a fast and flexible linting tool for Markdown files that helps maintain consistent formatting and catches common issues.

## About Markdownlint

Markdownlint is a Node.js-based tool that checks Markdown files against a set of configurable rules to enforce consistent style and catch syntax errors. The CLI tool (markdownlint-cli2) is built on top of the markdownlint library and provides enhanced performance and configuration options.

### Key Capabilities

- **Linting**: Check Markdown files against style rules
- **Auto-fixing**: Automatically fix many common Markdown issues
- **Configuration**: Customizable rules via multiple configuration formats
- **Glob Support**: Process multiple files using glob patterns
- **Cross-platform**: Works consistently across UNIX and Windows
- **Fast**: Efficient processing of multiple Markdown files

## When to Use This Skill

Use this skill when users:

- Need to format or clean Markdown files
- Want to enforce Markdown style consistency across a project
- Need to validate Markdown syntax
- Want to identify and fix Markdown issues automatically
- Need to lint Markdown files as part of CI/CD pipelines
- Ask about Markdown best practices or style rules
- Want to configure custom Markdown linting rules

## Project-Specific Configuration

**IMPORTANT**: This project uses `.markdownlint.yaml` for configuration. Always follow these project rules:

### Key Project Rules

- **MD040 (fenced-code-language)**: ALWAYS specify a language for code fences. Never use plain ` ``` ` without a language identifier.
    - ✅ Good: ` ```bash `, ` ```python `, ` ```json `
    - ❌ Bad: ` ``` ` (no language specified)
- **MD007 (unordered-list-indent)**: Use 2-space indentation for lists
- **MD033 (no-inline-html)**: Disabled - inline HTML is allowed
- **MD041 (first-line-h1)**: Disabled - files don't need to start with H1
- **MD013 (line-length)**: Disabled - no line length restrictions
- **MD024 (no-duplicate-heading)**: Siblings only - duplicate headings allowed under different parents
- **MD038 (no-space-in-code)**: Disabled
- **MD036 (no-emphasis-as-heading)**: Disabled

When fixing or creating markdown files in this project, always ensure compliance with these rules.

## How to Use This Skill

### Basic Markdownlint Workflow

The basic command pattern is:

```bash
markdownlint-cli2 [glob patterns] [options]
```

### Common Operations

#### Linting Files

Check a single Markdown file:

```bash
markdownlint-cli2 README.md
```

Check multiple files with glob patterns:

```bash
markdownlint-cli2 "**/*.md"
markdownlint-cli2 "docs/**/*.md"
markdownlint-cli2 "*.md" "docs/**/*.md"
```

Check all Markdown files in the current directory (dot-only glob):

```bash
markdownlint-cli2 .
# This is automatically mapped to: markdownlint-cli2 "*.{md,markdown}"
```

Check all Markdown files recursively:

```bash
markdownlint-cli2 "**"
```

#### Auto-fixing Issues

Fix issues automatically where possible:

```bash
markdownlint-cli2 --fix "**/*.md"
markdownlint-cli2 --fix README.md
```

The `--fix` option will modify files in place to resolve fixable issues.

#### Excluding Files/Directories

Exclude directories using negated patterns (use `#` for cross-platform compatibility):

```bash
markdownlint-cli2 "**/*.md" "#node_modules" "#vendor"
markdownlint-cli2 "**/*.md" "#**/node_modules"
```

Note: On UNIX shells, use `#` instead of `!` for better compatibility with double-quoted arguments.

#### Using Configuration Files

Markdownlint will automatically detect configuration files in the following order:

- `.markdownlint-cli2.jsonc`
- `.markdownlint-cli2.yaml`
- `.markdownlint-cli2.cjs` or `.markdownlint-cli2.mjs`
- `.markdownlint.jsonc` or `.markdownlint.json`
- `.markdownlint.yaml` or `.markdownlint.yml`
- `.markdownlint.cjs` or `.markdownlint.mjs`
- `package.json` (under `markdownlint-cli2` key)

Specify a custom configuration file:

```bash
markdownlint-cli2 --config .markdownlint-custom.json "**/*.md"
```

#### Working with stdin

Process input from standard input:

```bash
cat README.md | markdownlint-cli2 -
echo "# Hello World" | markdownlint-cli2 -
```

#### Literal File Paths

Use `:` prefix to specify literal file paths (bypassing glob expansion):

```bash
markdownlint-cli2 ":path/to/file.md"
```

### Configuration

#### Basic Configuration File

Create a `.markdownlint.json` file:

```json
{
  "default": true,
  "MD013": false,
  "MD033": false
}
```

Or a `.markdownlint-cli2.jsonc` file with comments:

```jsonc
{
  // Use default rules
  "config": {
    "default": true,
    // Disable line length rule
    "MD013": false,
    // Allow inline HTML
    "MD033": false,
    // Customize list indentation
    "MD007": {
      "indent": 2
    }
  },
  // Files to ignore
  "globs": ["**/*.md"],
  "ignores": ["node_modules", "CHANGELOG.md"]
}
```

#### Common Rules

Common markdownlint rules (prefix with MD):

- **MD001**: Heading levels should increment by one
- **MD003**: Heading style (consistent, atx, setext)
- **MD004**: Unordered list style
- **MD007**: Unordered list indentation
- **MD009**: Trailing spaces
- **MD010**: Hard tabs
- **MD012**: Multiple consecutive blank lines
- **MD013**: Line length (often disabled for flexibility)
- **MD022**: Headings should be surrounded by blank lines
- **MD024**: Multiple headings with the same content
- **MD025**: Multiple top-level headings
- **MD031**: Fenced code blocks should be surrounded by blank lines
- **MD032**: Lists should be surrounded by blank lines
- **MD033**: Inline HTML (often disabled when HTML is needed)
- **MD034**: Bare URLs
- **MD040**: Fenced code blocks should have a language ⚠️ **CRITICAL: Always specify language in this project**
- **MD041**: First line should be a top-level heading

#### Disable Rules Inline

Disable rules for specific sections using HTML comments:

```markdown
<!-- markdownlint-disable MD013 -->
This is a very long line that would normally trigger MD013 but won't because the rule is disabled.
<!-- markdownlint-enable MD013 -->

<!-- markdownlint-disable-next-line MD033 -->
<div>This HTML is allowed</div>

<!-- markdownlint-disable-file MD013 -->
Disable a rule for the entire file
```

### Cross-Platform Best Practices

For maximum compatibility across platforms:

1. **Quote glob patterns**: Always use double quotes around patterns

   ```bash
   markdownlint-cli2 "**/*.md" "#node_modules"
   ```

2. **Use `#` for negation**: Instead of `!` which can cause shell issues

   ```bash
   markdownlint-cli2 "**/*.md" "#vendor"
   ```

3. **Use forward slashes**: Always use `/` for path separators (works on all platforms)

   ```bash
   markdownlint-cli2 "docs/**/*.md"
   ```

4. **Stop processing options**: Use `--` to treat remaining arguments as literals

   ```bash
   markdownlint-cli2 -- "file-with-special-chars.md"
   ```

### Common Workflows

#### Format All Markdown in a Project

```bash
markdownlint-cli2 --fix "**/*.md" "#node_modules" "#vendor"
```

#### Check Only Docs Directory

```bash
markdownlint-cli2 "docs/**/*.md"
```

#### CI/CD Integration

Add to your CI pipeline to enforce Markdown standards:

```bash
# Fail build if any issues found
markdownlint-cli2 "**/*.md" "#node_modules"
```

#### Pre-commit Hook

Lint staged Markdown files before commit:

```bash
#!/bin/sh
markdownlint-cli2 $(git diff --cached --name-only --diff-filter=ACM | grep '\.md$')
```

#### Fix and Review

Fix issues but review changes before committing:

```bash
# Create a backup first
git add .
git commit -m "Backup before markdownlint fix"

# Apply fixes
markdownlint-cli2 --fix "**/*.md"

# Review changes
git diff

# Commit if satisfied or reset if not
git add .
git commit -m "Apply markdownlint fixes"
```

### Troubleshooting

#### No Files Matched

If markdownlint reports no files matched:

- Check that glob patterns are properly quoted
- Verify file extensions (`.md` vs `.markdown`)
- Ensure negated patterns aren't excluding everything

#### Too Many Issues

If you're overwhelmed by issues on an existing project:

1. Start by fixing auto-fixable issues: `markdownlint-cli2 --fix "**/*.md"`
2. Review the most common violations
3. Disable problematic rules initially and gradually enable them
4. Focus on high-priority rules first (headings, lists, code blocks)

#### Configuration Not Loading

If your configuration isn't being applied:

- Check file name matches expected patterns
- Validate JSON/YAML syntax
- Use `--config` to explicitly specify the file
- Check for syntax errors in configuration

### Best Practices

1. **Start with defaults**: Begin with all default rules enabled and disable
   only what's necessary
2. **Use auto-fix liberally**: Many issues are mechanical and safe to auto-fix
3. **Configure line length carefully**: MD013 (line length) is often disabled
   or set to a high value
4. **Allow necessary HTML**: Disable MD033 if your Markdown intentionally
   includes HTML
5. **Document exceptions**: Use inline comments to explain why rules are disabled
6. **Commit configuration**: Keep `.markdownlint.json` in version control for consistency
7. **Run early and often**: Integrate linting into your development workflow
8. **Review auto-fixes**: Always review changes from `--fix` before committing

## Installation

Markdownlint-cli2 can be installed via:

- **npm**: `npm install -g markdownlint-cli2`
- **yarn**: `yarn global add markdownlint-cli2`
- **pnpm**: `pnpm add -g markdownlint-cli2`
- **Homebrew**: `brew install markdownlint-cli2`

Verify installation:

```bash
markdownlint-cli2 --help
```

## Resources

- Official repository: <https://github.com/DavidAnson/markdownlint-cli2>
- Markdownlint rules: <https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md>
- Configuration schema: <https://github.com/DavidAnson/markdownlint-cli2#configuration>
