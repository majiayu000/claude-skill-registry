---
name: migration-lint
description: Comprehensive Angular migration compliance checker with auto-fix capabilities. Use when reviewing migrated code for DDD architecture, Angular 20 syntax, and UI pattern compliance.
---

# Migration Lint Command

Review and fix migrated Angular code for compliance. This command reads ALL migration guidelines and performs a comprehensive checklist review.

## Arguments

- `$ARGUMENTS` - Target path to review (e.g., `libs/mxsecurity/connection-management-page`)

## Workflow

### Step 1: Load ALL Migration Guidelines

**IMPORTANT:** Read the core SKILL.md first, then reference documents as needed from ``.

**Core:** `one-ui-migration skill`

| # | Topic | File | Category |
|---|-------|------|----------|
| 1 | Migration Context | rules/reference/migration-context.md | Foundation |
| 2 | Angular 20 Syntax | rules/reference/angular-20-syntax.md | Foundation |
| 3 | DDD Architecture | rules/reference/ddd-architecture.md | Architecture |
| 4 | State Management | rules/reference/state-management.md | Architecture |
| 5 | Authentication | rules/tools/auth.md | Architecture |
| 6 | Migration Checklist | rules/reference/migration-checklist.md | Foundation |
| 7 | Pitfalls Index | rules/reference/pitfalls/index.md | Pitfalls |
| 7a | Pitfalls: Translation & Layout | rules/reference/pitfalls/translation-layout.md | Pitfalls |
| 7b | Pitfalls: DDD Violations | rules/reference/pitfalls/ddd-violations.md | Pitfalls |
| 7c | Pitfalls: Angular Syntax | rules/reference/pitfalls/angular-syntax.md | Pitfalls |
| 7d | Pitfalls: Forms & Services | rules/reference/pitfalls/forms-services.md | Pitfalls |
| 8 | Validators | rules/tools/forms/validators.md | Forms |
| 9 | Error Handling | rules/tools/forms/error-handling.md | Forms |
| 10 | Form Patterns | rules/tools/forms/patterns.md | Forms |
| 11 | Page Layout | rules/tools/ui/page-layout.md | UI Patterns |
| 12a | Forms | rules/tools/ui/forms.md | UI Patterns |
| 12b | Buttons | rules/tools/ui/buttons.md | UI Patterns |
| 12c | Components | rules/tools/ui/components.md | UI Patterns |
| 13 | Dialogs | rules/tools/ui/dialogs.md | UI Patterns |
| 14 | Table Basics | rules/tools/tables/basics.md | Tables |
| 15 | Table Columns | rules/tools/tables/columns.md | Tables |
| 16 | Table Advanced | rules/tools/tables/advanced.md | Tables |
| 17 | API Type Definitions | rules/reference/api-types.md | API |
| 18 | Shared Stores | rules/reference/shared-stores.md | State |

### Step 2: Read Target Files

Read all `.ts`, `.html`, and `.scss` files in the target path:
- `{target}/domain/src/lib/**/*.ts`
- `{target}/features/src/lib/**/*.ts`
- `{target}/features/src/lib/**/*.html`
- `{target}/features/src/lib/**/*.scss`
- `{target}/ui/src/lib/**/*.ts`
- `{target}/ui/src/lib/**/*.html`
- `{target}/ui/src/lib/**/*.scss`
- `{target}/shell/src/lib/**/*.ts`

### Step 3: Comprehensive Checklist Review

**Check EVERY item from EVERY migration file:**

---

## Checklist by Category

### Category 1: Foundation & Pitfalls

#### migration-context.md
- [ ] Project follows one-ui monorepo structure
- [ ] Uses correct scope tags (`scope:mxsecurity`)
- [ ] Library types match DDD pattern (`domain`, `features`, `ui`, `shell`)

#### angular-syntax.md
- [ ] Uses `@if` instead of `*ngIf`
- [ ] Uses `@for (item of items; track item.id)` instead of `*ngFor`
- [ ] Uses `@switch` instead of `ngSwitch`
- [ ] Uses `inject()` instead of constructor injection
- [ ] Uses `input()` instead of `@Input()`
- [ ] Uses `output()` instead of `@Output()`
- [ ] Uses `viewChild()` / `viewChildren()` instead of `@ViewChild()` / `@ViewChildren()`
- [ ] Uses `contentChild()` / `contentChildren()` instead of `@ContentChild()` / `@ContentChildren()`
- [ ] Uses `model()` for two-way binding where appropriate
- [ ] Components are standalone (default in Angular 20)
- [ ] Uses `ChangeDetectionStrategy.OnPush`

#### migration-checklist.md
- [ ] Domain layer contains only business logic, models, services, state
- [ ] Features layer contains smart components with store injection
- [ ] UI layer contains presentational components with input/output ONLY (NO store injection)
- [ ] Shell layer contains routing configuration
- [ ] Barrel exports (`index.ts`) are properly configured

#### pitfalls/translation-layout.md
- [ ] Translation keys match source exactly (no new keys created)
- [ ] Form layout matches source (row groupings preserved)
- [ ] No padding in page component styles
- [ ] Page uses `gl-page-content` class (not ng-container)
- [ ] Table toolbar button order: Refresh → Create/Delete (only if old code has refresh)

#### pitfalls/ddd-violations.md
- [ ] No form templates in features layer (extract to UI)
- [ ] No store injection in UI components
- [ ] Dialogs are in features layer (not UI)
- [ ] No business logic in features (move to domain)
- [ ] No HTTP calls in UI components

#### pitfalls/angular-syntax.md
- [ ] No mixing old/new control flow (`*ngIf` with `@for`)
- [ ] All `@for` loops have `track`
- [ ] No NgModule patterns (use standalone)
- [ ] `langChanged()` called at field level (not in computed)
- [ ] Uses `inject()` instead of constructor injection

#### pitfalls/forms-services.md
- [ ] `mutationMethod`/`queryMethod` imported from `@one-ui/mxsecurity/shared/domain` (NOT `shared/util`)
- [ ] No unnecessary `.def.ts` files for constants
- [ ] Uses `MxSnackbarService` (not `MatSnackBar`)
- [ ] Uses `controls.xxx` (not `.get('xxx')`)
- [ ] Form valueChanges uses `toSignal()` in effects
- [ ] Uses `EMPTY_DASH` constant (not `utils.emptyDash`)
- [ ] Uses `oneUiNumberOnly` (not `appNumberOnly`)
- [ ] Uses `mx-password-input` for password fields
- [ ] Uses `mx-key-value` for readonly displays
- [ ] No `TRANSLOCO_SCOPE` provider (use global translation keys)
- [ ] No endpoint constants (`#ENDPOINTS = {}`) - inline URLs directly in API methods

---

### Category 2: Architecture

#### ddd-architecture.md
- [ ] Domain layer has correct structure
- [ ] Features layer has correct structure
- [ ] UI layer has correct structure
- [ ] Shell layer has correct structure
- [ ] Dependencies flow correctly (UI → Domain, Features → UI/Domain)
- [ ] No UI components importing from features
- [ ] Shared domain utilities used where appropriate

#### state-management.md
- [ ] Uses NgRx SignalStore for state management
- [ ] Store follows correct naming convention (`XxxStore`)
- [ ] Uses `withEntities()` for entity management
- [ ] Uses `withRequestStatus()` for loading states
- [ ] Uses `withDataService()` for API integration
- [ ] Effects handle success/error properly
- [ ] Uses `patchState()` correctly
- [ ] Store is provided in correct scope

#### authentication.md
- [ ] Uses `AuthStore` for authentication state
- [ ] Permission checks use correct patterns
- [ ] Protected routes have guards
- [ ] API calls include proper authentication headers

---

### Category 3: Forms (forms/)

#### validators.md
- [ ] Uses `OneValidators.required` (not `Validators.required`)
- [ ] Uses `OneValidators.email` (not `Validators.email`)
- [ ] Uses `OneValidators.minLength(n)` (not `Validators.minLength`)
- [ ] Uses `OneValidators.maxLength(n)` (not `Validators.maxLength`)
- [ ] Uses `OneValidators.min(n)` (not `Validators.min`)
- [ ] Uses `OneValidators.max(n)` (not `Validators.max`)
- [ ] Uses `OneValidators.pattern(x)` (not `Validators.pattern`)
- [ ] Custom validators follow correct patterns
- [ ] Cross-field validators implemented correctly
- [ ] Import from `@one-ui/mxsecurity/shared/domain`

#### error-handling.md
- [ ] Form errors displayed using `<mat-error>`
- [ ] Error messages use translation keys
- [ ] Async validators handle errors
- [ ] API errors displayed to user
- [ ] Uses `MxSnackbarService` for notifications

#### patterns.md
- [ ] Uses `NonNullableFormBuilder` (not `FormBuilder`)
- [ ] Form controls accessed via `controls.xxx` (not `.get('xxx')`)
- [ ] `getRawValue()` used for form submission
- [ ] Dynamic forms use `FormArray` correctly
- [ ] Form reset/patch follows patterns
- [ ] Forms in UI layer use `input()`/`output()` for data flow

---

### Category 4: UI Patterns (ui/)

#### ui/page-layout.md
- [ ] Root wrapper has `class="gl-page-content"`
- [ ] Uses `<one-ui-breadcrumb />` at top
- [ ] Uses `<mx-page-title [title]="t('...')">` for page title
- [ ] Content wrapped in `class="content-wrapper"` (NOT `mat-card`)
- [ ] Uses `*transloco="let t"` pattern
- [ ] Section titles use `class="gl-title-md"`

#### buttons.md
- [ ] Submit button uses `mat-flat-button color="primary"`
- [ ] Cancel button uses `mat-button`
- [ ] Toolbar buttons use `mat-stroked-button`
- [ ] NO `mat-raised-button` (use `mat-flat-button`)
- [ ] Loading state uses `[mxButtonIsLoading]` directive
- [ ] Disabled state properly handles `noPermission()`

#### forms.md
- [ ] Single form field NOT wrapped in `<div class="form-row">`
- [ ] Multiple fields on same row use `<div class="form-row">`

#### dialogs.md
- [ ] Uses shared dialog config (`smallDialogConfig`, `mediumDialogConfig`, `largeDialogConfig`)
- [ ] Has `viewContainerRef: this.#viewContainerRef` when dialog uses store
- [ ] `ConfirmDialogComponent` result checked as boolean (NOT `result?.confirm`)
- [ ] Dialog data typed properly
- [ ] Dialog returns correct type
- [ ] `afterClosed()` subscription cleaned up properly

---

### Category 5: Tables (tables/)

#### basics.md
- [ ] Uses `<mx-table>` component
- [ ] Column definitions use `MxColumnDef[]`
- [ ] Has `data-testid` attributes
- [ ] Loading state shows skeleton
- [ ] Empty state handled properly

#### columns.md
- [ ] Column types match data
- [ ] Custom templates import `MatTableModule` and `MatSortModule`
- [ ] Link columns use proper navigation
- [ ] Status columns use proper styling
- [ ] Action columns positioned correctly

#### advanced.md
- [ ] Selection implemented correctly (if applicable)
- [ ] Sorting configured properly
- [ ] Pagination implemented (if applicable)
- [ ] Filtering works correctly (if applicable)
- [ ] Toolbar buttons use `mat-stroked-button`

---

### Category 6: API & Services

#### api-types.md
- [ ] API types defined in domain layer
- [ ] Request/Response types properly typed
- [ ] Uses proper HTTP methods
- [ ] Error responses typed
- [ ] Enums defined for constants
- [ ] NO endpoint constants (`#ENDPOINTS = {...}`) - inline URL strings directly in methods

#### shared-stores.md
- [ ] Uses shared stores where appropriate (e.g., `TimeZoneStore`)
- [ ] Shared store initialization handled
- [ ] Cross-feature state accessed via shared stores
- [ ] No duplicate state management

---

### Category 7: Additional Checks

#### Translation (Transloco)
- [ ] Uses `*transloco="let t"` or `@let t = translocoT`
- [ ] NO `translate` pipe
- [ ] Translation keys follow naming convention
- [ ] Parameters passed correctly to `t()`

#### Directives
- [ ] `oneUiNumberOnly` (not `appNumberOnly`)
- [ ] Custom directives use `one-ui` prefix

#### Services
- [ ] `MxSnackbarService` (not `MatSnackBar`)
- [ ] Snackbar: `snackBar.open(msg)` (not `snackBar.open(msg, '', { duration: 3000 })`)

#### Constants
- [ ] `EMPTY_DASH` from `@one-ui/mxsecurity/shared/domain` (not `utils.emptyDash`)

#### Imports
- [ ] No circular imports
- [ ] Imports from correct library paths
- [ ] No relative imports crossing library boundaries

#### Password Fields
- [ ] Uses `<mx-password-input>` for password fields

#### Readonly Display
- [ ] Uses `<mx-key-value>` for readonly key-value displays

---

### Step 4: Fix Issues

**Auto-fix the following issues:**

| Issue | Fix |
|-------|-----|
| `mat-raised-button` | → `mat-flat-button` |
| `*ngIf` | → `@if` |
| `*ngFor` | → `@for (item of items; track item.id)` |
| `Validators.required` | → `OneValidators.required` |
| `Validators.email` | → `OneValidators.email` |
| `Validators.minLength(n)` | → `OneValidators.minLength(n)` |
| `Validators.maxLength(n)` | → `OneValidators.maxLength(n)` |
| `.get('xxx')` | → `controls.xxx` |
| `class="section-title"` | → `class="gl-title-md"` |
| `appNumberOnly` | → `oneUiNumberOnly` |
| `this.utils.emptyDash` | → `EMPTY_DASH` |
| `readonly #ENDPOINTS = {` | → Remove constant, inline URLs directly in each method |
| `from '@one-ui/mxsecurity/shared/util'` (for mutationMethod/queryMethod) | → `from '@one-ui/mxsecurity/shared/domain'` |

### Step 5: Generate Report

Output a compliance report:

```markdown
## Migration Lint Report

**Path:** {target_path}
**Date:** {current_date}

### Checklist Summary

| Category | Files Checked | Pass | Fail | N/A |
|----------|---------------|------|------|-----|
| Foundation (01, 02, 06) | 3 | Pass | Fail | - |
| Architecture (03, 04, 05) | 3 | Pass | Fail | - |
| Pitfalls (08, 08a, 08b, 08c, 08d) | 5 | Pass | Fail | - |
| Forms (09a, 09b, 09c) | 3 | Pass | Fail | - |
| UI Patterns (10a, 10b, 10c) | 3 | Pass | Fail | - |
| Tables (11a, 11b, 11c) | 3 | Pass | Fail | - |
| API & Services (12, 13) | 2 | Pass | Fail | - |
| **Total** | **22** | **X** | **Y** | **Z** |

### Issues Fixed

| File | Line | Issue | Fix Applied |
|------|------|-------|-------------|
| component.html | 15 | mat-raised-button | Changed to mat-flat-button |

### Issues Found (Manual Review Needed)

| File | Line | Issue | Recommendation | Guide Ref |
|------|------|-------|----------------|-----------|
| component.ts | 42 | Missing viewContainerRef | Add viewContainerRef to dialog config | dialogs.md |
| store.ts | 20 | Store in UI layer | Move to features layer | ddd-architecture.md |

### Detailed Checklist Results

#### migration-context.md (Pass)
- [x] Project follows one-ui monorepo structure
- [x] Uses correct scope tags

#### angular-syntax.md (Warning)
- [x] Uses @if instead of *ngIf
- [ ] Uses inject() instead of constructor injection (line 45)

... (continue for all files)

### Summary

- **Migration Files Checked:** 22/22
- **Auto-fixed:** X issues
- **Manual review needed:** Y issues
- **Passed checks:** Z items
- **Failed checks:** W items
```

## Quick Reference

### Button Types

```html
<!-- Form submit button -->
<button mat-flat-button color="primary" type="submit">Apply</button>

<!-- Table toolbar button -->
<button mat-stroked-button>Create</button>

<!-- Cancel/secondary button -->
<button mat-button type="button">Cancel</button>
```

### Page Layout

```html
<div *transloco="let t" class="gl-page-content">
  <one-ui-breadcrumb />
  <mx-page-title [title]="t('page.title')" />

  <div class="content-wrapper">
    <!-- content here, NO mat-card -->
  </div>
</div>
```

### Form Row

```html
<!-- Single field - NO form-row wrapper -->
<mat-form-field>
  <mat-label>{{ t('label') }}</mat-label>
  <input matInput formControlName="field" />
</mat-form-field>

<!-- Multiple fields on same row - USE form-row wrapper -->
<div class="form-row">
  <mat-form-field>...</mat-form-field>
  <mat-form-field>...</mat-form-field>
</div>
```

### Dialog Config

```typescript
import { mediumDialogConfig } from '@one-ui/mxsecurity/shared/domain';

this.#dialog.open(MyDialog, {
  ...mediumDialogConfig,
  data: dialogData,
  viewContainerRef: this.#viewContainerRef  // Required if dialog uses store
});
```

### Validators

```typescript
import { OneValidators } from '@one-ui/mxsecurity/shared/domain';

this.#fb.group({
  name: ['', [OneValidators.required, OneValidators.maxLength(32)]],
  email: ['', [OneValidators.required, OneValidators.email]],
  port: ['', [OneValidators.required, OneValidators.min(1), OneValidators.max(65535)]]
});
```

### ConfirmDialogComponent

```typescript
// ConfirmDialogComponent returns boolean, NOT { confirm: boolean }
const dialogRef = this.#dialog.open<ConfirmDialogComponent, ConfirmDialogData, boolean>(
  ConfirmDialogComponent,
  {
    ...mediumDialogConfig,
    viewContainerRef: this.#viewContainerRef,
    data: { title: '...', desc: '...' }
  }
);

dialogRef.afterClosed().subscribe((result) => {
  if (result) {  // result is boolean
    this.doSomething();
  }
});
```

### Snackbar Service

```typescript
// Use MxSnackbarService instead of MatSnackBar
import { MxSnackbarService } from '@moxa/formoxa/mx-snackbar';

readonly #snackBar = inject(MxSnackbarService);

// Simple usage
this.#snackBar.open('Success message');

// Persistent message (no auto-dismiss)
this.#snackBar.open('Saving...', { duration: 0 });
```

### Section Title

```html
<!-- Use gl-title-md class (global style) -->
<h3 class="gl-title-md">{{ t('section.title') }}</h3>

<!-- NOT section-title (requires custom SCSS) -->
<h3 class="section-title">{{ t('section.title') }}</h3>
```

### Form Controls Access

```typescript
// .get() - no type safety
const value = this.form.get('username')?.value;

// controls.xxx - type safe
const value = this.form.controls.username.value;

// In ValidatorFn - use type assertion
#myValidator(): ValidatorFn {
  return (formGroup: AbstractControl): null => {
    const controls = (formGroup as typeof this.form).controls;
    const fieldValue = controls.fieldName.value;
    return null;
  };
}
```

### Password Input

```html
<!-- Use mx-password-input for password fields -->
<mx-password-input
  formControlName="password"
  [maxlength]="32"
></mx-password-input>
```

### Key-Value Display

```html
<!-- Use mx-key-value for readonly displays -->
<mx-key-value [key]="t('label')" [value]="displayValue"></mx-key-value>
```

### UI Component Pattern

```typescript
// UI components use input()/output() ONLY - NO store injection
export class MyUiComponent {
  readonly data = input<MyData>();
  readonly isLoading = input<boolean>(false);

  readonly save = output<MyData>();
  readonly cancel = output<void>();
}
```

### Features Component Pattern

```typescript
// Features components can inject stores
export class MyFeatureComponent {
  readonly #store = inject(MyStore);

  readonly data = this.#store.data;
  readonly isLoading = this.#store.isLoading;
}
```
