---
name: TypeScript Build Checker
description: Check TypeScript compilation errors, run build commands, and validate the codebase. Use when the user mentions TypeScript errors, build issues, compilation problems, or wants to verify code integrity.
---

# TypeScript Build Checker

Check TypeScript compilation status and build the project.

## Quick Start

### Check for TypeScript errors
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npx tsc --noEmit
```

### Build the project
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npm run build
```

### Run development server
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npm run dev
```

## Common Commands

### Full type check with detailed output
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npx tsc --noEmit --pretty
```

### Watch mode for continuous compilation
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npx tsc --watch --noEmit
```

### Check specific file
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npx tsc --noEmit <filename>
```

## Interpreting Results

- **Exit code 0**: No errors, compilation successful
- **Exit code 1**: Errors found, check output for details
- Look for error patterns like:
  - `error TS2345`: Type mismatch
  - `error TS2339`: Property doesn't exist
  - `error TS2322`: Type not assignable
  - `error TS2304`: Cannot find name/type

## Best Practices

1. Always check TypeScript errors before committing code
2. Fix errors from top to bottom (earlier errors may cause later ones)
3. Use `--noEmit` flag to check without generating files
4. Run full build after fixing errors to ensure no runtime issues
