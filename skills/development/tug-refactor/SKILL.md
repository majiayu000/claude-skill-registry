---
name: tug-refactor
description: |
  Semantic code refactoring using tug. Use this skill when the user wants to:
  - Rename a function, class, method, or variable across multiple files
  - Change symbol names with automatic reference updates
  - Refactor identifiers while preserving semantic correctness

  Trigger patterns: "rename X to Y", "change the name of", "refactor the name",
  "update all references", "change the function/class/variable name"

  Note: tug currently supports Python only. Rust support is planned but not yet implemented.
---

# Tug Refactoring Skill

This skill provides semantic refactoring capabilities through the `tug` CLI tool.

## When to Use This Skill

Use tug when the user requests symbol renaming or reference updates, especially:
- Multi-file renames (function used in many places)
- Class or method renames with inheritance implications
- Variable renames that must preserve scoping rules
- Any rename where manual find/replace would be error-prone

## Available Commands

- `/tug-apply-rename` - Full rename workflow with analyze, review, and apply
- `/tug-emit-rename` - Generate unified diff without applying changes
- `/tug-analyze-rename` - Analyze impact only (no changes, no diff)

## Workflow

1. **Identify the symbol**: Determine file, line, and column of the symbol to rename
2. **Get the new name**: Ask user for the desired new name if not provided
3. **Invoke command**: Use `/tug-apply-rename` for the full workflow

## Why Tug Over Manual Editing

- **Scope-aware**: Understands language scoping rules (shadowing, imports, etc.)
- **Verified**: Runs syntax verification before applying changes
- **Deterministic**: Same input always produces same output
- **Safe**: Requires explicit approval before applying changes

## CLI Quick Reference

```bash
# Analyze impact (read-only, JSON output)
tug analyze python rename --at <file:line:col> --to <new_name>

# Emit diff (read-only, unified diff output)
tug emit python rename --at <file:line:col> --to <new_name>

# Apply rename (modifies files)
tug apply python rename --at <file:line:col> --to <new_name>
```

## Example

User: "Rename the process_data function to transform_data"

Response: I'll use tug to rename this function safely across all files.
[Invoke /tug-apply-rename]
