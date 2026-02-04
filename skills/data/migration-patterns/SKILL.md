---
name: migration-patterns
description: Query Angular migration patterns and examples. Use when looking up patterns (table, form, dialog, layout, button, store) or asking questions about migration guidelines.
---

Query Angular migration patterns and examples. This skill loads the migration documentation and helps with pattern lookup and answering migration questions.

## Arguments

- `$ARGUMENTS` - Query keyword or question:
  - `table` - Table migration patterns (CommonTableComponent)
  - `form` - Form patterns (validators, NonNullableFormBuilder)
  - `dialog` - Dialog patterns (config, loading, viewContainerRef)
  - `layout` - Page layout (gl-page-content, content-wrapper)
  - `button` - Button patterns (mat-flat-button, loading states)
  - `ddd` - DDD architecture (domain/features/ui/shell)
  - `api` - API type definitions
  - `store` - SignalStore patterns
  - `syntax` - Angular 20 syntax (@if, @for, inject, signal)
  - `validator` - OneValidators usage
  - `error` - Error handling patterns
  - `pitfall` - Common pitfalls to avoid
  - Or ask any question about migration

**Note:** For code review/linting, use `/migration-lint` instead.

## Workflow

### Step 1: Load Relevant Documentation

Based on the query, read the appropriate documentation files from `rules/`:

| Query | Files to Read |
|-------|---------------|
| `table` | tables/basics.md, tables/columns.md, tables/advanced.md |
| `form` | forms/validators.md, forms/patterns.md, ui/forms.md |
| `dialog` | ui/dialogs.md |
| `layout` | ui/page-layout.md |
| `button` | ui/buttons.md |
| `ddd` | ddd-architecture.md |
| `api` | api-types.md |
| `store` | state-management.md |
| `syntax` | angular-syntax.md |
| `validator` | forms/validators.md |
| `error` | forms/error-handling.md |
| `pitfall` | pitfalls/index.md |

### Step 2: Process Query

**For keyword queries (table, form, etc.):**
- Summarize the key patterns and rules
- Provide code examples
- List common mistakes to avoid

**For questions:**
- Search through all migration docs
- Provide specific answers with code examples
- Reference the source document

## Quick Reference

### Table Components (UI Layer)

```typescript
// Required imports for custom column templates
import { MatSortModule } from '@angular/material/sort';
import { MatTableModule } from '@angular/material/table';

@Component({
  imports: [
    CommonTableComponent,
    MatSortModule,   // Required for mat-sort-header
    MatTableModule,  // Required for matColumnDef, *matCellDef
  ]
})
```

### Form Validation

```typescript
import { OneValidators } from '@one-ui/mxsecurity/shared/domain';

// Correct
this.#fb.group({
  name: ['', [OneValidators.required, OneValidators.maxLength(32)]],
  ip: ['', [OneValidators.required, ipv4Validator]]
});
```

### Form Field Tooltip (mxLabelTooltip)

**DO NOT use `mat-icon` with `matTooltip`**. Use `mxLabelTooltip` directive on `mat-label` instead.

```html
<!-- WRONG - Don't use mat-icon with info tooltip -->
<div class="form-row">
  <mat-form-field>
    <mat-label>{{ t('field.label') }}</mat-label>
    <mat-select formControlName="field">...</mat-select>
  </mat-form-field>
  <mat-icon class="info-icon" [matTooltip]="t('field.hint')">info</mat-icon>
</div>

<!-- CORRECT - Use mxLabelTooltip -->
<mat-form-field>
  <mat-label mxLabel [mxLabelTooltip]="t('field.hint')">
    {{ t('field.label') }}
  </mat-label>
  <mat-select formControlName="field">...</mat-select>
</mat-form-field>
```

**Required import:**

```typescript
import { MxLabelDirective } from '@moxa/formoxa/mx-label';

@Component({
  imports: [MxLabelDirective]
})
```

### Button Types

```html
<!-- Form submit button -->
<button mat-flat-button color="primary" type="submit">Apply</button>

<!-- Table toolbar button -->
<button mat-stroked-button>Create</button>
```

### Page Layout

```html
<div *transloco="let t" class="gl-page-content">
  <one-ui-breadcrumb />
  <mx-page-title [title]="t('page.title')" />

  <div class="content-wrapper">
    <!-- content here -->
  </div>
</div>
```

### Card Container (IMPORTANT)

**DO NOT use `<mat-card>`**. Always use `class="content-wrapper"` instead.

```html
<!-- WRONG - Don't use mat-card -->
<mat-card>
  <mat-card-header>...</mat-card-header>
  <mat-card-content>...</mat-card-content>
</mat-card>

<!-- CORRECT - Use content-wrapper -->
<div class="content-wrapper">
  <!-- content here -->
</div>

<!-- If you need mat-card structure, add content-wrapper class -->
<mat-card class="content-wrapper">
  <mat-card-header>...</mat-card-header>
  <mat-card-content>...</mat-card-content>
</mat-card>
```

The `content-wrapper` class provides:
- Consistent padding (16px)
- Border radius (8px)
- Surface background color
- Gap between child elements (8px)

### Dialog Config

```typescript
import { mediumDialogConfig } from '@one-ui/mxsecurity/shared/domain';

this.#dialog.open(MyDialog, {
  ...mediumDialogConfig,
  data: dialogData,
  viewContainerRef: this.#viewContainerRef  // Required if dialog uses store
});
```

## Output Format

### For keyword queries:
Provide a concise summary with:
1. Key rules (do's and don'ts)
2. Code examples
3. Common mistakes

### For questions:
Provide the answer with:
1. Direct answer
2. Code example
3. Source reference (which doc file)
