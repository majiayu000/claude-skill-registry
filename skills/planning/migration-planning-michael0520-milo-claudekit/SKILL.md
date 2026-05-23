---
name: migration-planning
description: Planning One-UI migrations with superpowers workflow integration. Ensures tool references are included in brainstorming and plan writing.
license: MIT
compatibility: Requires superpowers plugin and one-ui-migration skill
allowed-tools: Read, Bash, Edit, Write, Glob, Grep
---

# Migration Planning Skill

> **Purpose**: Integrate superpowers workflow with one-ui-migration tool references to ensure compliant migration plans.

## When to Use

- Before starting a migration with `superpowers:brainstorming`
- When writing migration plans with `superpowers:writing-plans`
- When you need to plan a feature migration

---

## Tool Reference Requirements

### Component-to-Tool Mapping

| If Legacy has... | You MUST reference... |
|------------------|----------------------|
| Forms | `rules/tools/form-builder.md` + `rules/tools/one-validators.md` |
| Tables | `rules/tools/common-table.md` + `rules/tools/transloco.md` |
| Dialogs | `rules/tools/ui/dialogs.md` + `rules/tools/form-builder.md` |
| State management | `rules/tools/signal-store.md` + `rules/tools/loading-states.md` |
| Status display | `rules/tools/mx-components.md` |
| Page layout | `rules/tools/ui/page-layout.md` + `rules/tools/transloco.md` |
| Authentication | `rules/tools/auth.md` |
| Translation | `rules/tools/transloco.md` |
| Route configuration | `rules/tools/routing.md` |

---

## Superpowers Integration

### During `superpowers:brainstorming`

Before proposing any design, identify which tools are needed:

```markdown
## Tool Analysis

Legacy component uses:
- [ ] Forms → Reference `form-builder.md`, `one-validators.md`
- [ ] Tables → Reference `common-table.md`
- [ ] Dialogs → Reference `ui/dialogs.md`
- [ ] State → Reference `signal-store.md`, `loading-states.md`
- [ ] MX Components → Reference `mx-components.md`
- [ ] Routes → Reference `routing.md`

**Required tools for this migration:**
1. `rules/tools/signal-store.md` - Store pattern
2. `rules/tools/form-builder.md` - Form creation
3. ...
```

### During `superpowers:writing-plans`

Every task MUST include a Tool References section:

```markdown
### Task N: Create {component}

**Layer**: domain | features | ui | shell
**Files**: libs/mxsecurity/{feature}/{layer}/src/lib/...

**Tool References**:
- [ ] `rules/tools/signal-store.md` - queryMethod/mutationMethod
- [ ] `rules/tools/one-validators.md` - OneValidators

**Implementation**:
[code here]

**Verification Checklist** (from tool files):
- [ ] No `Validators` import (use `OneValidators`)
- [ ] No `BehaviorSubject` (use `signal()`)
- [ ] No `FormBuilder` (use `NonNullableFormBuilder`)
```

---

## Tool Checklists

### signal-store.md Checklist

- [ ] Use `queryMethod` for GET requests (not `rxMethod`)
- [ ] Use `mutationMethod` for POST/PUT/DELETE
- [ ] State interface extends `LoadingState`
- [ ] No `BehaviorSubject` or `Subject<>`
- [ ] Use `loading()` signal for loading state

### form-builder.md Checklist

- [ ] Use `NonNullableFormBuilder` (not `FormBuilder`)
- [ ] Initialize with default values
- [ ] Use `getRawValue()` to submit

### one-validators.md Checklist

- [ ] Import `OneValidators` from `@one-ui/shared/domain`
- [ ] No `Validators` from `@angular/forms`
- [ ] Use `OneValidators.required`, `OneValidators.range`, etc.

### common-table.md Checklist

- [ ] Import `CommonTableComponent`, `SELECT_COLUMN_KEY`, `EDIT_COLUMN_KEY`
- [ ] Custom columns (`noAutoGenerate: true`) have `filter` function
- [ ] Import `MatSortModule` when using `mat-sort-header`
- [ ] Text cells use `gl-ellipsis-text` + `mxAutoTooltip`
- [ ] Toolbar order: Refresh -> Create -> Delete

### ui/dialogs.md Checklist

- [ ] Pass `viewContainerRef` when opening dialog
- [ ] Cancel button uses `mat-dialog-close` (not `(click)="cancel()"`)
- [ ] `.close()` only in `next:` callback (not after mutation call)
- [ ] Submit button: `[disabled]="form.invalid || loading()"`

### mx-components.md Checklist

- [ ] `mxButtonIsLoading` requires `loading()` in `[disabled]`
- [ ] Form errors use `oneUiFormError` directive
- [ ] `mat-tab-group` has `mxTabGroup` and `animationDuration="0ms"`
- [ ] Status display uses `mx-status` component

### ui/page-layout.md Checklist

- [ ] Use `gl-page-content` (not `mat-card`)
- [ ] Content inside `<div class="content-wrapper">`
- [ ] No padding on page component

### transloco.md Checklist

- [ ] Use `*transloco="let t"` (not `| translate`)
- [ ] Do NOT create new translation keys
- [ ] Verify keys exist in Legacy `en.json`

### auth.md Checklist

- [ ] Use `sessionStorage` (not `localStorage`)
- [ ] Token key is `mx_token`

### loading-states.md Checklist

- [ ] State interface extends `LoadingState`
- [ ] Use `loadingInitialState()` for initial state
- [ ] Use `loading()` signal in templates
- [ ] Loading button: `[mxButtonIsLoading]="loading()" [disabled]="loading()"`

### routing.md Checklist

- [ ] Use `ROUTES_ALIASES` for route paths
- [ ] Use `createBreadcrumbResolver` for breadcrumb resolution
- [ ] Routes use `loadChildren` with dynamic import
- [ ] Shell module exports `createRoutes()` function

---

## Task Template

Use this template for each task in the plan:

```markdown
### Task {N}: {Description}

**Layer**: {domain | features | ui | shell}
**Files**:
- `libs/mxsecurity/{feature}/{layer}/src/lib/{file}.ts`

**Tool References**:
- `rules/tools/{tool1}.md`
- `rules/tools/{tool2}.md`

**Implementation**:
```typescript
// code
```

**Verification**:
- [ ] {checklist item from tool file}
- [ ] {checklist item from tool file}
```

---

## Migration Planning Workflow

```
1. Analyze Legacy
   └── Identify components, forms, tables, dialogs, state
   └── Map to required tools

2. superpowers:brainstorming
   └── Include Tool Analysis section
   └── List all required tool references

3. superpowers:writing-plans
   └── Each task has Tool References
   └── Each task has Verification Checklist

4. Execute Plan
   └── Read tool files before implementing
   └── Follow checklist for each task

5. Validate
   └── Run one-ui-migration-checker
   └── All 29 rules pass
```

---

## Example: User Management Migration

### Tool Analysis

Legacy `user-management` uses:
- Table with selection, edit, delete
- Create/Edit dialog with form
- Enable/disable status
- Store for state management

**Required tools**:
1. `signal-store.md` - Store pattern
2. `loading-states.md` - Loading state management
3. `common-table.md` - Table component
4. `ui/dialogs.md` - Dialog pattern
5. `form-builder.md` - Form in dialog
6. `one-validators.md` - Form validation
7. `mx-components.md` - MxStatus, mxButtonIsLoading
8. `transloco.md` - Translations
9. `routing.md` - Route configuration

### Task Example

```markdown
### Task 1: Create UserStore

**Layer**: domain
**Files**: `libs/mxsecurity/user/domain/src/lib/user.store.ts`

**Tool References**:
- `rules/tools/signal-store.md`

**Implementation**:
```typescript
export const UserStore = signalStore(
  withState(initialState),
  withMethods((store, api = inject(UserApiService)) => ({
    loadUsers: queryMethod<void, User[]>({
      store,
      observe: () => api.getAll$(),
      next: (users) => patchState(store, { users })
    }),
    deleteUser: mutationMethod<string, void>({
      store,
      observe: (id) => api.delete$(id),
      next: () => store.loadUsers()
    })
  }))
);
```

**Verification**:
- [ ] Uses `queryMethod` for GET (not `rxMethod`)
- [ ] Uses `mutationMethod` for DELETE
- [ ] State extends `LoadingState`
- [ ] No `BehaviorSubject`
```

---

## Related Skills

- `one-ui-migration` - Main migration skill
- `superpowers:brainstorming` - Design phase
- `superpowers:writing-plans` - Planning phase

## Validation

After plan execution, run:
```
check migration for libs/mxsecurity/{feature}
```
