---
name: typescript-check
description: "TypeScript type checking via tsc --noEmit with actionable error output."
user-invocable: false
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
agent: typescript-frontend-engineer
routing:
  triggers:
    - "TypeScript check"
    - "tsc noEmit"
    - "type check TypeScript"
    - "tsc errors"
    - "TypeScript type validation"
  category: code-quality
  pairs_with:
    - vitest-runner
    - code-linting
---

# TypeScript Type Check Skill

## Overview

This skill validates TypeScript code by running `tsc --noEmit` and parsing errors into structured, actionable reports organized by file. It is a **read-only validation** step (does not modify code) that implements a linear workflow: locate config → execute compiler → parse output → present results.

Use this skill when validating TypeScript code before commits, after refactors, or checking for type regressions. Do not use for linting, test execution, runtime errors, or projects without tsconfig.json.

---

## Instructions

### Step 1: Verify TypeScript Project

Locate tsconfig.json in the project. This step is mandatory—never skip it. tsc without a tsconfig.json falls back to default settings, missing project-specific configuration like paths, strict mode, and compiler targets.

```bash
ls tsconfig.json 2>/dev/null || ls */tsconfig.json 2>/dev/null
```

If no tsconfig.json exists, stop and inform the user. Do not proceed without configuration.

**Why**: Running without tsconfig.json produces unreliable results that don't match the project's actual settings.

### Step 2: Run Type Check

Execute the TypeScript compiler in type-check-only mode using `--noEmit`:

```bash
npx tsc --noEmit 2>&1
```

Capture the exit code:
- **Exit 0**: No type errors found. Report PASS.
- **Exit 1+**: Type errors detected. Continue to Step 3.

Do not install TypeScript or dependencies. If TypeScript is not installed, inform the user and suggest `npm install typescript --save-dev`. This is a read-only skill—never modify package.json or run installation commands.

**Why**: `--noEmit` prevents generating .js files and gives you a clean type-only report. The exit code tells you definitively whether compilation succeeded.

### Step 3: Parse Output

For each error line in the tsc output, extract:
- **File path**: The .ts/.tsx file containing the error (use absolute paths for direct navigation)
- **Line:Column**: Exact location in the file
- **Error code**: TS#### identifier (e.g., TS2322, TS7006)
- **Message**: Human-readable error description

Group errors by source file and sort by line number. This helps users fix issues systematically rather than jumping randomly through the codebase.

**Why**: Users need actual file paths, line numbers, and error codes to fix issues. Suppressing or summarizing this information (e.g., "5 errors found") makes errors unsolvable.

### Step 4: Present Results

Format output using this structure. Always show the full exit code and complete error details:

```
=== TypeScript Type Check ===

Status: PASS / FAIL (N errors)

Errors by File:
---------------

src/components/Button.tsx
  Line 15:3  TS2322  Type 'string' is not assignable to type 'number'
  Line 28:10 TS2339  Property 'foo' does not exist on type 'Props'

src/utils/helpers.ts
  Line 5:1   TS7006  Parameter 'x' implicitly has an 'any' type

Summary: N files, M errors
```

Never present type errors as context for auto-fixing without explicit user request. Type check is a validation step—the user may want to review errors, may disagree with a fix approach, or may have a different solution in mind.

**Why**: Including the exit code and full output gives users all the context they need to make informed decisions about fixes.

---

## Error Handling

### Error: "Cannot find tsconfig.json"

Cause: No TypeScript configuration in the project root or specified path.

Solution:
1. Search for tsconfig.json in common locations (src/, app/, packages/)
2. If found elsewhere, re-run with `--project path/to/tsconfig.json`
3. If not found anywhere, inform user this requires a TypeScript project with a tsconfig.json file

### Error: "Cannot find module 'typescript'"

Cause: TypeScript is not installed as a project dependency.

Solution:
1. Inform user that TypeScript must be installed first
2. Suggest `npm install typescript --save-dev`
3. Do not install it automatically—this is a read-only skill

### Error: "npx: command not found"

Cause: Node.js toolchain is not installed or not in PATH.

Solution:
1. Verify Node.js is installed: `node --version`
2. If Node.js is present but npx missing, try `npm exec tsc -- --noEmit`
3. If Node.js is missing, inform user to install Node.js

### Error: "Multiple tsconfig.json files found"

Cause: Project has nested or monorepo structure with multiple TypeScript configurations.

Solution:
1. List all tsconfig.json files and their paths
2. Ask user which configuration to use
3. Re-run with `--project path/to/specific/tsconfig.json`

**Why explicit error handling matters**: tsc may fail silently, produce incomplete output, or exit unexpectedly. Capturing and reporting the actual error lets the user understand what went wrong and how to fix it.

---

## References

### Common tsc Flags

| Flag | Purpose |
|------|---------|
| `--noEmit` | Type check only, do not generate .js files |
| `--project path` | Use specific tsconfig.json |
| `--skipLibCheck` | Skip type checking .d.ts files (faster on large projects) |
| `--incremental` | Use incremental compilation (faster for repeat runs) |
| `--strict` | Enable all strict type checks |

### Integration Points

- **Before pr-workflow commit**: Run type check before committing TypeScript changes
- **With vitest-runner**: Run type check first, then tests
- **With code-linting**: Run lint first, then type check

### Optional Behaviors (OFF unless enabled)

- **--strict mode**: Run with additional strict flags beyond tsconfig settings
- **--project path**: Use a specific tsconfig.json when multiple exist
- **--skipLibCheck**: Add --skipLibCheck to speed up checking on large projects
- **Specific files**: Check only named files instead of entire project
