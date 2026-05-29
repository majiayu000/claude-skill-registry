---
name: check-barrel-files
description: Check for redundant barrel files (index.ts) that only re-export a single item.
---

# Check Barrel Files Command

Check for redundant barrel files (index.ts) that only re-export a single item.

## Arguments

- `$ARGUMENTS` - The library path to check (e.g., `libs/mxsecurity/account-page`)

## Problem Description

Redundant barrel files are `index.ts` files that:
1. Only contain a single `export * from './xxx'` statement
2. Are intermediate files that add no value

### Bad Pattern

```
libs/scope/domain/features/src/
├── index.ts                    # exports from './lib/my-dialog'
└── lib/
    └── my-dialog/
        ├── index.ts            # Redundant: only exports './my-dialog.component'
        └── my-dialog.component.ts
```

### Good Pattern

```
libs/scope/domain/features/src/
├── index.ts                    # exports from './lib/my-dialog/my-dialog.component'
└── lib/
    └── my-dialog/
        └── my-dialog.component.ts   # No intermediate barrel file
```

## Check Process

### Step 1: Find All index.ts Files

Find all `index.ts` files in the target path:

```bash
find {$ARGUMENTS} -name "index.ts" -type f
```

### Step 2: Analyze Each Barrel File

For each `index.ts` file found:

1. Read the file content
2. Count the number of export statements
3. If only ONE export exists, check if it exports from a folder (barrel) or a file

### Step 3: Identify Redundant Barrels

A barrel file is redundant if:
- It contains only ONE export statement
- The export is `export * from './folder-name'`
- The target folder has its own `index.ts` that also only exports one item

### Step 4: Generate Report

Output a markdown report:

```markdown
# Barrel File Check Report

**Path:** {$ARGUMENTS}
**Date:** {current_date}

## Summary

| Total index.ts | Redundant | OK |
|----------------|-----------|-----|
| X              | Y         | Z   |

## Redundant Barrel Files

| File | Exports | Recommendation |
|------|---------|----------------|
| `lib/my-dialog/index.ts` | `./my-dialog.component` | Delete, update parent to export directly |

## Recommended Fixes

### 1. {path/to/redundant/index.ts}

**Current:**
```typescript
// src/index.ts
export * from './lib/my-dialog';

// lib/my-dialog/index.ts
export * from './my-dialog.component';
```

**Recommended:**
```typescript
// src/index.ts
export * from './lib/my-dialog/my-dialog.component';

// Delete: lib/my-dialog/index.ts
```

## Valid Barrel Files (No Action Needed)

| File | Export Count | Reason |
|------|--------------|--------|
| `domain/src/index.ts` | 5 | Multiple exports |
```

## Auto-Fix Option

After showing the report, ask the user:

> Found {N} redundant barrel files. Would you like me to fix them automatically?

If user confirms, for each redundant barrel:
1. Update the parent `index.ts` to export directly from the component file
2. Delete the redundant `index.ts` file

## Examples

### Example 1: Simple Redundant Barrel

```
Before:
  features/src/index.ts → export * from './lib/account-dialog'
  features/src/lib/account-dialog/index.ts → export * from './account-dialog.component'

After:
  features/src/index.ts → export * from './lib/account-dialog/account-dialog.component'
  (deleted: features/src/lib/account-dialog/index.ts)
```

### Example 2: Valid Multi-Export Barrel (Keep)

```
domain/src/index.ts:
  export * from './lib/account-page.api';
  export * from './lib/account-page.model';
  export * from './lib/account-page.store';

→ This is valid, do not modify
```
