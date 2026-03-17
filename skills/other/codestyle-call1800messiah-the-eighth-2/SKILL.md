---
name: codestyle
description: Analyze code for style violations, pattern compliance, and quality issues
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Task
  - AskUserQuestion
  - Bash(git status:*)
  - Bash(git diff:*)
  - Bash(git log:*)
  - Bash(npx nx lint:*)
  - Bash(npx eslint:*)
---

# Codestyle Skill

## Purpose
Analyze code files for compliance with project coding standards and consistent patterns used across the codebase.

**Key responsibilities:**
- Detect naming convention violations
- Check import order and patterns
- Verify Angular patterns
- Check testing compliance
- Verify accessibility standards
- Auto-fix trivial issues (import order, file naming)
- Generate detailed reports

## Invocation

### Default: Check Git Worktree
```
/codestyle
```
Checks all staged and unstaged files (git worktree changes).

### Specific Path
```
/codestyle path/to/file
/codestyle path/to/folder
```
Checks specific file or all .ts/.tsx files in folder recursively.

### Integration Mode (Called by Other Skills)
```
/codestyle --integration path/to/file
```
Returns structured results for programmatic use. Used by `/implement` and `/feature` skills.

---

## Categories (All Mandatory)

### 1. Styling (CRITICAL)

| Check                | Rule                                            | Severity |
|----------------------|-------------------------------------------------|----------|
| **SCSS files**       | All component styles in *.scss files | **CRITICAL** |
| **CSS Variables**    | Use var(--*) for colors, not hardcoded          | ERROR |

**VIOLATION patterns:**
```scss

// BAD - Hardcoded colors in SCSS
.card { color: #333; background: blue; }

// GOOD - CSS variables
.card { color: var(--color-font-muted); background: var(--color-secondary); }
```

### 2. Naming Conventions

| Check | Rule | Severity |
|-------|------|----------|
| File naming | kebab-case for .ts/.ts | ERROR |
| Component naming | PascalCase | ERROR |
| Variable naming | camelCase | WARNING |
| Type naming | PascalCase | ERROR |

**Detection patterns:**
```
# File naming - should be kebab-case
BAD:  UserProfile.ts, userProfile.ts
GOOD: user-profile.ts

# Component naming - should be PascalCase
BAD:  export class myComponent
GOOD: export class MyComponent

# Type naming - should be PascalCase
BAD:  type user = {}
GOOD: type User = {}
```

### 3. Import Order and Patterns

| Check | Rule                                | Severity |
|-------|-------------------------------------|----------|
| Import order | Angular/third-party > types > local | WARNING |
| Relative imports | Within package: use relative        | ERROR |
| Path aliases | Only for cross-package              | ERROR |

**Correct order:**
```typescript
// 1. Angular and third-party
import { Component, OnInit } from '@angular/core';
import { Observable, Subscription } from 'rxjs';

// 4. Type imports
import type { Place } from '../../models/place';

// 3. Local relative imports
import { ConfigService } from '../../../core/services/config.service';
```

**Auto-fixable**: Import order can be auto-fixed.

### 4. Testing Compliance

| Check | Rule                      | Severity |
|-------|---------------------------|----------|
| Test file exists | Components need .spec.ts | WARNING |
| Test ID naming | T-{FEAT}-{NUM} format     | WARNING |
| Co-located tests | Tests next to source      | WARNING |


---

## Workflow

### Step 1: Identify Files to Check

**Default (no args):**
```bash
# Get staged files
git diff --cached --name-only

# Get unstaged modified files
git diff --name-only

# Combine and filter to .ts/.tsx
```

**With path argument:**
```bash
# If file: check single file
# If directory: glob **/*.{ts,tsx}
```

### Step 2: Run Category Checks

For each file, run checks based on file type:

| File Pattern           | Checks                  |
|------------------------|-------------------------|
| `*.ts`                 | Naming, Imports         |
| `*.scss`               | Styling                 |
| `*.spec.ts`            | Testing compliance only |

### Step 3: Collect Violations

Group violations by severity:
- **CRITICAL**: Must fix before merge
- **ERROR**: Should fix before merge
- **WARNING**: Best practice, advisory

### Step 4: Auto-Fix Trivial Issues

**Auto-fixable with confirmation:**
- Import order reordering
- File rename to kebab-case (requires updating imports across codebase)

**Ask user before applying:**
```
Found 2 auto-fixable issues:
1. Import order in src/app/places/components/place.component.ts
3. Rename UserProfile.ts → user-profile.compoment.ts (will update 5 import statements)

Apply auto-fixes? (y/n)
```

### Step 5: Generate Report

**Output file:** `docs/code-reviews/{YYYY-MM-DD-HHmmss}-codestyle.md`

**Also print inline summary:**
```
## Codestyle Check Complete

| Category | Critical | Errors | Warnings |
|----------|----------|--------|----------|
| Naming   | 0        | 1      | 0        |
| Imports  | 0        | 0      | 3        |
| ...      | ...      | ...    | ...      |

**Total: 2 critical, 1 error, 4 warnings**

Full report: docs/code-reviews/2024-01-15-143022-codestyle.md
```

---

## Integration Mode

When called with `--integration` flag, return structured result instead of printing:

```typescript
type CodestyleResult = {
  passed: boolean;           // false if any critical/error
  critical: number;
  errors: number;
  warnings: number;
  violations: Array<{
    file: string;
    line: number;
    category: string;
    severity: 'critical' | 'error' | 'warning';
    message: string;
    autoFixable: boolean;
  }>;
  reportPath: string;
};
```

**Used by:**
- `/implement` - After implementing code
- `/feature` - Phase 5 quality gate

---

## Checklist

When running codestyle:

1. [ ] Identify files to check (git worktree or specified path)
2. [ ] Run all category checks per file type
3. [ ] Collect and categorize violations
4. [ ] Offer auto-fix for trivial issues
5. [ ] Generate markdown report
6. [ ] Print inline summary
7. [ ] Return structured result if integration mode

---

## Quick Reference: Detection Patterns

### File Naming Violation
```
Glob: **/*.{ts,html,scss}
Check: filename contains uppercase (except index.ts, types.ts)
```

### Missing SCSS file
```
Check: .ts file in shared/components without corresponding .scss
```
