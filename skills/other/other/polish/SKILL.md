---
name: polish
description: Remove AI slop, comments, and lint errors from the current branch.
disable-model-invocation: true
---

# Polish Protocol

Remove AI slop and lint errors from the current branch.
**Autonomous Mode: No confirmation required for cleanup tasks.**

# Can Be Used By Any Agent

All technical agents can invoke this skill:
- `@backend-architect`
- `@frontend-architect`
- `@mobile-architect`
- `@qa-engineer`

# Critical Rules

1.  **ONLY remove slop:** No refactoring logic, only cleanup.
2.  **ONLY fix lint/type errors:** Do not change style preferences.
3.  **NEVER change logic:** If a "better" way exists, ignore it. Only fix broken things.
4.  **NEVER touch unrelated code:** Only files in `git diff main...HEAD`.

# Slop Reference (Delete these)

- "Here is the logic" comments
- "TODO: implement this" comments (unless legitimate)
- `// ... existing code ...` markers
- `as any` type bypasses (unless absolutely necessary)
- Excessive `console.log` (unless for intentional logging)
- Dead code / Unused imports
- Commented-out code blocks
- Empty functions with no implementation

# Workflow

## Step 1: Check Git Status

```bash
git status
```

**Error Handling:**
- If not a git repo: "❌ Not a git repository. Run `git init` first."
- If no changes: "✅ No changes to polish. Branch is clean."

## Step 2: Get Changed Files

```bash
git diff --name-only main...HEAD
```

**Error Handling:**
- If `main` branch doesn't exist: Try `master` or `develop`
- If command fails: Ask user for base branch name

## Step 3: Identify File Types

Group files by type:
- **JavaScript/TypeScript:** `.js`, `.ts`, `.jsx`, `.tsx`
- **Python:** `.py`
- **Other:** (CSS, Markdown, etc.) - Skip or minimal cleanup

## Step 4: Remove Slop

For each file:
1. Read the file
2. Identify slop patterns
3. Remove/fix them
4. Save the file

**Process files in batches of 5** to avoid overwhelming the system.

## Step 5: Run Linter/Type Checker

**JavaScript/TypeScript:**
```bash
# Get changed JS/TS files
CHANGED_JS_FILES=$(git diff --name-only main...HEAD 2>/dev/null | grep -E '\.(js|ts|jsx|tsx)$' | tr '\n' ' ')

if [ -n "$CHANGED_JS_FILES" ] && [ -f "package.json" ]; then
  # Try ESLint
  if npm list eslint >/dev/null 2>&1; then
    npx eslint --fix $CHANGED_JS_FILES
  fi
  
  # Try TypeScript
  if [ -f "tsconfig.json" ]; then
    npx tsc --noEmit
  fi
fi
```

**Python:**
```bash
# Get changed Python files
CHANGED_PY_FILES=$(git diff --name-only main...HEAD 2>/dev/null | grep -E '\.py$' | tr '\n' ' ')

if [ -n "$CHANGED_PY_FILES" ]; then
  # Try Black (formatter)
  if command -v black >/dev/null 2>&1; then
    black $CHANGED_PY_FILES
  fi

  # Try Ruff (linter)
  if command -v ruff >/dev/null 2>&1; then
    ruff check --fix $CHANGED_PY_FILES
  fi
fi
```

**Error Handling:**
- If linter not found: Skip and report
- If linter fails: Show errors and ask if user wants to continue
- If type errors exist: Report them (don't auto-fix)

## Step 6: Run Prettier (if available)

```bash
# Get all changed files for formatting
CHANGED_FILES=$(git diff --name-only main...HEAD 2>/dev/null | tr '\n' ' ')

if [ -n "$CHANGED_FILES" ] && npm list prettier >/dev/null 2>&1; then
  npx prettier --write $CHANGED_FILES
fi
```

## Step 7: Summary Report

**Success:**
```
✅ Polish Complete!

📊 Summary:
- Files processed: 12
- Slop removed: 23 instances
- Lint errors fixed: 7
- Type errors: 0

✨ Branch is clean and ready for review!

➡️ Next Steps:
1. Review changes: git diff
2. Commit: git add . && git commit -m "Polish: Remove slop and fix lint"
3. Ship it: /ship-it
```

**With Warnings:**
```
⚠️ Polish Complete (with warnings)

📊 Summary:
- Files processed: 12
- Slop removed: 23 instances
- Lint errors fixed: 7
- Type errors: 3 remaining

❌ Type Errors:
1. src/utils.ts:45 - Type 'string | undefined' is not assignable to type 'string'
2. src/api.ts:78 - Property 'id' does not exist on type 'User'
3. src/components/Form.tsx:120 - 'onClick' is missing in type 'ButtonProps'

➡️ Action Required:
Fix type errors manually before committing.
```

# Error Handling Summary

**Not a git repo:**
- Error: "❌ Not a git repository. Initialize with: git init"
- Exit

**No changes detected:**
- Info: "✅ No changes to polish. Branch is clean."
- Exit

**Base branch not found:**
- Ask: "What's your base branch? (main/master/develop)"
- Retry with user input

**Linter/Formatter not installed:**
- Warn: "⚠️ [Tool] not found. Skipping [action]."
- Continue with remaining steps

**Linter fails:**
- Show errors
- Ask: "Continue with remaining files? (Yes/No)"

**File read/write errors:**
- Log: "❌ Failed to process [file]: [error]"
- Continue with next file

**No slop found:**
- Success: "✅ No slop detected. Code is clean!"
- Still run linter/formatter

# Success Criteria

- [ ] All changed files scanned
- [ ] AI slop removed
- [ ] Lint errors fixed (or reported)
- [ ] Code formatted consistently
- [ ] Summary provided
- [ ] User knows next steps
