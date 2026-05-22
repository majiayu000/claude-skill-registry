---
name: debugging-ci-failures
description: Guidelines for diagnosing and fixing CI build failures. Claude should use this skill when investigating why a CI build failed.
---

# Debugging CI Build Failures

When a CI build fails, follow these guidelines to diagnose and fix the issue correctly.

## Read Before You Fix

1. Read the FULL error message carefully - note the exact file/class mentioned
2. Identify the exact line of code causing the failure
3. Understand what that line is trying to do before proposing a fix
4. If the error mentions a file not found, determine WHICH file (class? resource? config?)
5. Reproduce locally if possible before implementing a fix
6. Never assume the cause based on recent code you've seen - verify first

## Common Mistakes to Avoid

- **Don't assume based on recent changes**: Just because you recently modified something doesn't mean it's the cause
- **Don't confuse file types**: A `FileNotFoundException` for a `.yml` file is different from a missing `.class` file
- **Don't implement fixes without understanding**: If you can't explain exactly why the fix works, you don't understand the problem

## Verification Steps

1. After implementing a fix, run the same command that failed in CI
2. Verify the specific test or task that failed now passes
3. If CI fails again with the same error, your fix was wrong - go back to step 1

## Pattern-Based Problems

When fixing issues caused by naming conventions or patterns:
1. Search the entire codebase for similar occurrences before making any changes
2. Fix ALL instances in a single commit
3. Never commit partial fixes for pattern-based problems
