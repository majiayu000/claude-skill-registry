---
name: file-organization
description: Guidelines for file operations like moving, renaming, and reorganizing files. Claude should use this skill when reorganizing code structure to prefer efficient shell commands over write/delete patterns.
---

# File Organization Guidelines

When reorganizing files, moving files, or renaming files, follow these guidelines:

## Moving/Renaming Files

Use `git mv` or `mv` via Bash instead of Write + delete:

```bash
git mv old/path/File.java new/path/File.java
```

Then use Edit to update any necessary content (e.g., package declarations).

## Why This Matters

- Preserves git history - changes can be tracked across renames
- Simpler: One command instead of multiple tool calls
- Preserves file metadata (creation time, permissions)
- Conceptually cleaner: A move operation should be expressed as a move
- Less error-prone: No risk of forgetting to delete the old file

**IMPORTANT**: Never recreate files from scratch when the original exists. Move the file first, then edit its contents.

## Package Reorganization Example

When reorganizing Java packages:

```bash
# 1. Create new directory structure
mkdir -p src/main/java/com/example/newpackage

# 2. Move the file
mv src/main/java/com/example/oldpackage/MyClass.java src/main/java/com/example/newpackage/

# 3. Update the package declaration
# Use Edit tool to change: package com.example.oldpackage;
# To: package com.example.newpackage;
```

## Refactoring Cleanup

When moving files during refactoring:
1. Move files to new location
2. Verify build passes in new location
3. Delete the old empty directories immediately
4. Don't ask - empty directories after a move serve no purpose

## Refactoring Checklist

Before moving source files in a refactoring:

### 1. Inventory ALL Source Directories
- Check for `src/main/java`, `src/test/java`, AND custom source sets
- Look for `src/integrationTest`, `src/integration-test`, `src/componentTest`, `src/component-test`
- Check build.gradle for plugin-defined directories (e.g., Eventuate test plugins)

### 2. Move Complete Modules
- Move main sources AND all test sources together (unit, integration, component tests)
- A module is incomplete without its tests
- Verify test count before and after refactoring matches

**IMPORTANT**: This is one situation where `./gradlew build` passing is insufficient. You must verify that each test class has a corresponding `TEST-*.xml` file in the correct build directory. Tests may compile but not run if source sets are misconfigured.

### 3. Transfer ALL Dependencies
When converting single-module to multi-module:
- Run `git show HEAD:path/to/build.gradle` to capture original configuration
- List ALL dependency configurations (implementation, testImplementation, integrationTestImplementation, componentTestImplementation, etc.)
- For each dependency, determine which subproject needs it
- Verify build works BEFORE and AFTER refactoring with the same test command

## When to Use Write

Reserve the Write tool for:
- Creating genuinely new files
- Files where content is being substantially rewritten
- Generated files where the entire content is new

Do NOT use Write for:
- Moving files to new locations
- Renaming files
- Reorganizing directory structures

## Prefer Dedicated Tools Over Bash

Use the right tool for file discovery and inspection:

| Task | Use | Instead of |
|------|-----|------------|
| List/find files | Glob | `ls`, `find` |
| Search file contents | Grep | `grep`, `rg` |
| Read file contents | Read | `cat`, `head`, `tail` |
| Edit files | Edit | `sed`, `awk` |

The dedicated tools:
- Handle edge cases gracefully (e.g., non-existent directories)
- Provide better formatted output
- Are optimized for the task
- Don't require defensive shell scripting patterns like `command 2>/dev/null || echo "fallback"`
