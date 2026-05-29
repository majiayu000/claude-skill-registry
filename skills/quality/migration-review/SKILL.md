---
name: migration-review
description: Review migration completeness between old and new codebase.
---

# Migration Review Command

Review migration completeness between source (old codebase) and target (new codebase).

## Arguments

- `$ARGUMENTS` - Format: `--from <source_path> --to <target_path>`
  - `--from`: Source path in old project (e.g., `/Users/jayden/f2e-networking-jayden/apps/mxsecurity-web/src/app/pages/account`)
  - `--to`: Target path in new project (e.g., `libs/mxsecurity/account-page`)

## Review Process

### Step 0: Switch to Feature Worktree

Before starting the review, switch to the feature's worktree to ensure you're working in the correct context:

```bash
cd /Users/jayden/one-ui-mxsecurity
```

This ensures the `--to` target path is accessible and you're reviewing the latest code in the feature branch.

### Step 1: Read All Files

Read all `.ts` and `.html` files from both `--from` and `--to` directories.

### Step 2: Extract and Compare Form Controls

**Reference:** `form-extraction skill`

Use the form-extraction skill to extract form controls from both source and target:

```bash
# From HTML
grep -oE 'formControlName="[^"]+"' {path}/**/*.html | sort -u
grep -oE 'formGroupName="[^"]+"' {path}/**/*.html | sort -u

# From TypeScript
grep -E '(this\.fb\.group|this\.#fb\.group|new FormGroup|new UntypedFormGroup)' {path}/**/*.ts
```

**Compare:** List all form controls from source that are missing in target.

### Step 3: Extract and Compare Form Validators

**Reference:** `form-extraction skill`

Use the form-extraction skill to extract validators:

```bash
# Source (old) - Angular Validators
grep -oE 'Validators\.(required|email|minLength|maxLength|min|max|pattern)(\([^)]*\))?' {from}/**/*.ts | sort -u

# Target (new) - OneValidators
grep -oE 'OneValidators\.[a-zA-Z]+(\([^)]*\))?' {to}/**/*.ts | sort -u

# Custom validators
grep -oE '#?[a-zA-Z]+Validator\b' {path}/**/*.ts | sort -u
```

**Compare:** For each form control, verify all validators from source exist in target.

**Validator Mapping:**

| Old (Validators) | New (OneValidators) |
| ---------------- | ------------------- |
| `Validators.required` | `OneValidators.required` |
| `Validators.email` | `OneValidators.email` |
| `Validators.minLength(n)` | `OneValidators.minLength(n)` |
| `Validators.maxLength(n)` | `OneValidators.maxLength(n)` |
| `Validators.min(n)` + `Validators.max(m)` | `OneValidators.range(n, m)` |
| `Validators.pattern(x)` | `OneValidators.pattern(x)` |

**For detailed patterns, see:** `rules/tools/forms/patterns.md`

### Step 4: Extract and Compare HTML Keys

**From HTML files, extract and compare:**

1. **CSS Classes** (functional classes only, skip styling classes)
   - Classes used in `*ngIf` conditions
   - Classes used in JavaScript/TypeScript logic

2. **Angular Directives**
   - `*ngIf` / `@if` conditions
   - `*ngFor` / `@for` iterations
   - `[ngClass]` bindings
   - `[ngStyle]` bindings

3. **Material Components**
   - All `<mat-xxx>` components used

4. **Event Bindings**
   - All `(click)`, `(submit)`, `(change)` etc.

5. **Property Bindings**
   - All `[disabled]`, `[hidden]`, `[value]` etc.

6. **Translation Keys**
   - Source (old): `{{ 'xxx' | translate }}` or `[translate]="'xxx'"`
   - Target (new): `{{ t('xxx') }}` with `*transloco="let t"`

### Step 5: UI Guidelines Review

**Check target files for UI guideline compliance:**

1. **Button Types (CRITICAL - Auto-fix)**
   - `mat-raised-button` → `mat-flat-button`
   - Search and replace all occurrences in target

2. **Page Layout Structure (CRITICAL - Tables won't display without this!)**
   - Root wrapper **MUST** have `class="gl-page-content"` - without this, tables and content may not display!
   - Content must be wrapped in `class="content-wrapper"`
   - `<one-ui-breadcrumb />` should come first
   - `<mx-page-title>` should use `[title]` input binding (not content projection)
   - Use `<div *transloco="let t" class="gl-page-content">` NOT `<ng-container>`

3. **Dialog Configuration**
   - Should use shared dialog config (`smallDialogConfig`, `mediumDialogConfig`, etc.)
   - Should NOT have custom `min-width` in SCSS
   - Should NOT use `panelClass` for sizing

4. **Table Toolbar**
   - Action buttons should use `#rightToolbarTemplate`
   - Icons should use `svgIcon="icon:xxx"` format
   - Should include `data-testid` attributes

5. **Translation**
   - Should use `transloco` (not `translate` pipe)
   - Should use `*transloco="let t"` pattern

6. **Form Error Display** (Reference: `form-extraction skill`)
   - `required`, `minLength`, `maxLength`, `range`, `rangeLength`, `email` → **MUST** use `<mat-error oneUiFormError="field">`
   - **All other validators** (`pattern`, `duplicate`, custom, etc.) → **MUST** use `@if/@else` with custom message

7. **Special Input Fields**
   - Password fields → Must use `<mx-password-input>` (not manual toggle)
   - Number-only fields → Must use `oneUiNumberOnly` directive (not `appNumberOnly`)

8. **Tab Groups**
   - Must use `mxTabGroup` directive: `<mat-tab-group mxTabGroup animationDuration="0ms">`

**Auto-fix:** If `mat-raised-button` is found, automatically replace with `mat-flat-button`.

### Step 6: Generate Report

Output a markdown report with the following sections:

```markdown
# Migration Review Report

**Source:** {from_path}
**Target:** {to_path}
**Date:** {current_date}

## Summary

| Category            | Source | Target | Missing | Completeness |
| ------------------- | ------ | ------ | ------- | ------------ |
| Form Controls       | X      | Y      | Z       | XX%          |
| Form Validators     | X      | Y      | Z       | XX%          |
| Material Components | X      | Y      | Z       | XX%          |
| Event Bindings      | X      | Y      | Z       | XX%          |
| Translation Keys    | X      | Y      | Z       | XX%          |
| UI Guidelines       | -      | X      | Y       | XX%          |

**Overall Completeness: XX%**

## UI Guidelines Compliance

| Rule                  | Status     | Notes                    |
| --------------------- | ---------- | ------------------------ |
| mat-flat-button       | OK/FIXED   | Auto-fixed X occurrences |
| Page Layout Structure | OK/MISSING | Details...               |
| Dialog Config         | OK/MISSING | Details...               |
| Table Toolbar         | OK/MISSING | Details...               |
| Translation Pattern   | OK/MISSING | Details...               |
| Form Error Display    | OK/MISSING | Non-basic validators use @if/@else? |
| Password Fields       | OK/MISSING | Using mx-password-input? |
| Number Input          | OK/MISSING | Using oneUiNumberOnly? |
| Tab Groups            | OK/MISSING | Using mxTabGroup? |

## Critical Missing Items

### Form Controls (CRITICAL)

- [ ] `controlName` - not found in target

### Form Validators (CRITICAL)

- [ ] `controlName: Validators.required` - not found in target

## Warnings

- Source uses `*ngIf` but target should use `@if`
- Source uses `*ngFor` but target should use `@for`

## Detailed Comparison

### Form Controls

| Control Name | In Source | In Target | Status  |
| ------------ | --------- | --------- | ------- |
| username     | Yes       | Yes       | OK      |
| password     | Yes       | No        | MISSING |

### Form Validators

| Control  | Validator | In Source | In Target | Status  |
| -------- | --------- | --------- | --------- | ------- |
| username | required  | Yes       | Yes       | OK      |
| username | maxLength | Yes       | No        | MISSING |

### Material Components

...
```

## Focus Areas

1. **Form Validation Completeness** - This is CRITICAL
   - Every validator in source must exist in target
   - Pay attention to custom validators
   - Check group-level validators (cross-field validation)
   - **Error display**: Only `required`, `minLength`, `maxLength`, `range`, `rangeLength`, `email` use `oneUiFormError`; all others MUST use `@if/@else`

2. **HTML Key Migration** - This is CRITICAL
   - Every `formControlName` must exist
   - Every event binding must be migrated

3. **UI Guidelines Compliance** - This is CRITICAL (Auto-fix)
   - `mat-raised-button` → `mat-flat-button` (auto-fix)
   - Page layout structure (`gl-page-content`, `content-wrapper`)
   - Dialog config (use shared configs)
   - Table toolbar patterns

4. **Syntax Modernization** (Warnings only)
   - `*ngIf` → `@if`
   - `*ngFor` → `@for`
   - `Validators.*` → `OneValidators.*`
   - `appNumberOnly` → `oneUiNumberOnly`
   - Password manual toggle → `mx-password-input`

## Step 7: Generate MIGRATION-ANALYSIS.md (REQUIRED)

**IMPORTANT:** Always generate the migration analysis document after completing the review.

**Location:** `{target}/domain/src/lib/docs/MIGRATION-ANALYSIS.md`

**Required Sections:**
1. Overview (source, target, date, status)
2. Migration Summary table
3. UI Guidelines Compliance table
4. File Structure
5. Detailed Comparison (form controls, validators, translation keys, API endpoints)
6. DDD Architecture Compliance
7. Syntax Modernization
8. Issues Fixed During Migration
9. Notes

**Example:**
```bash
mkdir -p {target}/domain/src/lib/docs
```

Then create the file with full migration analysis content.
