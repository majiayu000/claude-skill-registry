---
name: markdownlint
description: This skill should be used when users need to format, clean, lint, or validate Markdown files using the markdownlint-cli2 command-line tool. Use this skill for tasks involving Markdown (including Quarto Markdown `.qmd`) file quality checks, automatic formatting fixes, enforcing Markdown style rules, or identifying Markdown syntax issues.
---

# Markdownlint Skill

## Contents

- [Markdownlint Skill](#markdownlint-skill)
    - [Contents](#contents)
    - [Project Configuration](#project-configuration)
    - [Basic Usage](#basic-usage)
    - [Common Operations](#common-operations)
        - [Lint Specific Paths](#lint-specific-paths)
        - [Auto-Fix](#auto-fix)
        - [Process stdin](#process-stdin)
    - [Workflow](#workflow)
        - [Standard Lint-Fix-Verify Cycle](#standard-lint-fix-verify-cycle)
        - [Safe Fix with Backup](#safe-fix-with-backup)
    - [Cross-Platform Usage](#cross-platform-usage)
    - [Troubleshooting](#troubleshooting)
        - [No Files Matched](#no-files-matched)
        - [Too Many Issues](#too-many-issues)
        - [Configuration Not Loading](#configuration-not-loading)
    - [References](#references)
    - [Installation](#installation)

## Project Configuration

**IMPORTANT**: This project uses `.markdownlint.yaml`. Always follow these rules:

| Rule | Setting | Notes |
| ------ | --------- |------- |
| **MD040** | Enabled | Always specify language for code fences |
| **MD007** | 2 spaces | List indentation |
| **MD024** | Siblings only | Duplicate headings allowed under different parents |
| **MD013** | Disabled | No line length restrictions |
| **MD033** | Disabled | Inline HTML allowed |
| **MD041** | Disabled | Files don't need to start with H1 |
| **MD038** | Disabled | Spaces in code spans allowed |
| **MD036** | Disabled | Emphasis as heading allowed |

## Basic Usage

```bash
# Lint files
markdownlint-cli2 "**/*.md"
markdownlint-cli2 README.md

# Auto-fix issues
markdownlint-cli2 --fix "**/*.md"

# Exclude directories
markdownlint-cli2 "**/*.md" "#node_modules" "#vendor"
```

## Common Operations

### Lint Specific Paths

```bash
markdownlint-cli2 README.md                    # Single file
markdownlint-cli2 "docs/**/*.md"               # Directory
markdownlint-cli2 "*.md" "docs/**/*.md"        # Multiple patterns
markdownlint-cli2 .                            # Current directory
```

### Auto-Fix

```bash
markdownlint-cli2 --fix "**/*.md"              # Fix all files
markdownlint-cli2 --fix README.md              # Fix single file
```

### Process stdin

```bash
cat README.md | markdownlint-cli2 -
```

## Workflow

### Standard Lint-Fix-Verify Cycle

1. Run lint check: `markdownlint-cli2 "**/*.md"`
2. Review reported issues
3. Apply auto-fix: `markdownlint-cli2 --fix "**/*.md"`
4. Re-run lint to verify: `markdownlint-cli2 "**/*.md"`
5. Review changes: `git diff`
6. Commit when satisfied

### Safe Fix with Backup

1. Stage current state: `git add .`
2. Create backup commit: `git commit -m "Backup before markdownlint fix"`
3. Apply fixes: `markdownlint-cli2 --fix "**/*.md"`
4. Review changes: `git diff`
5. Commit fixes or reset: `git add . && git commit -m "Apply markdownlint fixes"`

## Cross-Platform Usage

For maximum compatibility:

- **Quote glob patterns**: `markdownlint-cli2 "**/*.md"`
- **Use `#` for negation**: `markdownlint-cli2 "**/*.md" "#vendor"` (not `!`)
- **Use forward slashes**: `docs/**/*.md` (works on all platforms)
- **Stop option processing**: `markdownlint-cli2 -- "special-file.md"`

## Troubleshooting

### No Files Matched

- Verify glob patterns are quoted
- Check file extensions (`.md` vs `.markdown`)
- Ensure negated patterns don't exclude everything

### Too Many Issues

1. Start with auto-fix: `markdownlint-cli2 --fix "**/*.md"`
2. Disable problematic rules temporarily
3. Address remaining issues incrementally

### Configuration Not Loading

- Verify configuration file name matches expected patterns
- Validate JSON/YAML syntax
- Use `--config` to explicitly specify the file

## References

- [Rules Reference](references/rules.md) - Complete rule descriptions
- [Configuration Examples](references/config-examples.md) - Config templates and patterns
- [Official Documentation](https://github.com/DavidAnson/markdownlint-cli2)
- [All Rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)

## Installation

```bash
npm install -g markdownlint-cli2    # npm
brew install markdownlint-cli2      # Homebrew
markdownlint-cli2 --help            # Verify installation
```
