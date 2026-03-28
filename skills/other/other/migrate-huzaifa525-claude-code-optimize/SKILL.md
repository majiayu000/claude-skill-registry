---
name: migrate
description: Use when the user wants to migrate, upgrade, or move from one framework, library, or API version to another.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
argument-hint: "[from] [to]"
---

Migrate from **$ARGUMENTS**.

## Steps

1. **Understand the migration**
   - What is being migrated (framework, library, API version)?
   - What are the breaking changes between versions?
   - Are there official migration guides?

2. **Audit current usage**
   - Grep for all imports/usages of the old library/API
   - Count affected files
   - Identify patterns used

3. **Create migration plan**
   ```
   ## Migration: [from] → [to]

   ### Affected Files ([count])
   - [file] — [what needs to change]

   ### Breaking Changes
   - [old API] → [new API]

   ### Steps
   1. Update dependencies
   2. [migration steps]
   3. Run tests
   ```

4. **Run tests BEFORE migration** — establish baseline
   ```
   [test command]
   ```

5. **Update dependencies first**
   ```
   npm install [new-package]@latest
   ```

6. **Apply migration file by file**
   - Replace old imports with new
   - Update API calls to new syntax
   - Handle renamed/removed functions
   - Update types if needed

7. **Run tests AFTER each file** — catch issues early

8. **Run full test suite at the end**

9. **Report:**
   ```
   ## Migration Complete

   ### Summary
   - [X] files migrated
   - [Y] API calls updated
   - All tests passing

   ### Manual Review Needed
   - [anything that couldn't be auto-migrated]
   ```

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
