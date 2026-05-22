---
name: migrate-page-gitlab
description: Migrate Angular page from GitLab source following DDD architecture. Use when migrating pages from GitLab repository (Angular 16) to Angular 20 with domain-driven design patterns.
---

# Page Migration Command (GitLab Source)

Migrate a page from GitLab repository (Angular 16) to new one-ui monorepo (Angular 20) following DDD architecture.

## Arguments

- `$ARGUMENTS` - Format: `--page <page_name>`
  - `--page`: Page folder name in GitLab (e.g., `time`, `account`, `ddns`)

**Target Path Convention**

Target path is automatically derived as `libs/mxsecurity/{page_name}-page`
Example: `--page time` → `libs/mxsecurity/time-page`

**GitLab Source Base URL**

`https://gitlab.com/moxa/sw/f2e/networking/f2e-networking/-/tree/main/apps/mxsecurity-web/src/app/pages/{page_name}`

**GitLab Access Token**

Set environment variable `GITLAB_TOKEN` or use `private_token=${GITLAB_TOKEN}` for authenticated access.

> **Security Note**: Never hardcode tokens in skill files. Use environment variables instead.

## Workflow

### Phase 1: Fetch Source from GitLab & Analysis

**GitLab URLs (with token):**

- Tree API: `https://gitlab.com/api/v4/projects/moxa%2Fsw%2Ff2e%2Fnetworking%2Ff2e-networking/repository/tree?path=apps/mxsecurity-web/src/app/pages/{page_name}&ref=main&private_token=${GITLAB_TOKEN}`
- Raw file: `https://gitlab.com/api/v4/projects/moxa%2Fsw%2Ff2e%2Fnetworking%2Ff2e-networking/repository/files/{url_encoded_path}/raw?ref=main&private_token=${GITLAB_TOKEN}`

Use WebFetch to fetch source files (`*.component.ts`, `*.component.html`, `*.component.scss`, `*.service.ts`, `*.model.ts`).

Analyze the fetched source and create a migration analysis document in `{target}/domain/src/lib/docs/MIGRATION-ANALYSIS.md`:

1. **File Structure Analysis**
   - List all files fetched from GitLab
   - Categorize by type: components, services, models, templates, styles

2. **Component Analysis**
   - Identify all components and their relationships
   - Note parent/child relationships
   - Identify dialog components
   - Identify table/form components

3. **Form Validation Analysis**
   - List all form controls and their validators
   - Identify `Validators.*` usage that needs `OneValidators.*` replacement
   - Document custom validators

4. **API Calls Analysis**
   - List all HTTP calls (endpoints, methods, request/response types)
   - Identify API services being used
   - Document data flow

5. **Dependencies Analysis**
   - Third-party libraries used
   - Angular Material components used
   - Shared services/utils used

6. **Translation Keys Analysis (CRITICAL)**
   - **DO NOT create new translation keys**
   - **DO NOT modify existing translation keys**
   - List all translation keys used in source HTML templates
   - Copy exact keys for use in migrated components

7. **Form Layout Analysis (CRITICAL)**
   - **DO NOT change form field row groupings**
   - Analyze `fxLayout="row"` patterns in source templates
   - Document which fields appear on same row
   - Use `.form-row` class in migrated components to preserve layout

### Phase 2: DDD Structure Migration

Reference documents from `one-ui-migration` skill's `rules/` directory:

**Reference Docs** (`rules/reference/`):
- `ddd-architecture.md` - DDD layers, helper files
- `api-types.md` - API types, def files
- `checklist.md` - Full compliance checklist
- `pitfalls/` - Common migration mistakes

**Tool Docs** (`rules/tools/`):
- `forms/validators.md` - OneValidators usage, pattern constants
- `forms/error-handling.md` - Template errors, custom errors
- `ui/page-layout.md` - Page layout, breadcrumb
- `ui/forms.md` - Form layout, validation
- `ui/buttons.md` - Button types, loading states
- `ui/components.md` - File upload, form patterns
- `ui/dialogs.md` - Dialog config, viewContainerRef
- `tables/basics.md` - CommonTableComponent
- `tables/columns.md` - Column API, custom templates
- `tables/advanced.md` - Paginator config

**Guides** (`rules/guides/`):
- `create-page.md` - Page creation guide
- `create-dialog.md` - Dialog creation guide
- `create-table.md` - Table creation guide

Generate libraries using the Nx plugin:

```bash
# Generate all library types at once
nx g @one-ui/one-plugin:library mxsecurity {page-name} all

# Or generate individually if needed
nx g @one-ui/one-plugin:library mxsecurity {page-name} domain
nx g @one-ui/one-plugin:library mxsecurity {page-name} features
nx g @one-ui/one-plugin:library mxsecurity {page-name} ui
nx g @one-ui/one-plugin:library mxsecurity {page-name} shell
```

### Phase 3: Layer-by-Layer Migration

1. **Domain Layer** (`domain/`) - see `rules/reference/ddd-architecture.md`
   - API response types → use existing types from `@one-ui/mxsecurity/shared/domain` (e.g., `SRV_USER_ACCOUNT`)
   - If API type missing → create in `libs/mxsecurity/shared/domain/src/lib/models/api/`
   - Page-specific models (view models, form models) → `*.model.ts`
   - Migrate API service → `*.api.ts`
   - Create SignalStore → `*.store.ts`
   - Migrate constants → `*.def.ts`
   - Extract pure functions → `*.helper.ts` (data transformations, serialization)
   - Keep `MIGRATION-ANALYSIS.md` in `domain/src/lib/docs/` folder

2. **UI Layer** (`ui/`) - see `rules/tools/tables/basics.md`
   - Migrate tables → use `CommonTableComponent` pattern
   - Migrate forms → use `input()`, `output()` pattern
   - Table toolbar → use `mat-stroked-button` with `general.button.create`/`delete`
   - Keep components dumb (no store injection, no HTTP)

3. **Features Layer** (`features/`) - see `rules/tools/ui/forms.md`, `buttons.md` and `dialogs.md`
   - Migrate page component → smart component pattern
   - Migrate dialogs → use `smallDialogConfig`, `mediumDialogConfig`, `largeDialogConfig`
   - Form tooltips → use `mxLabelTooltip` instead of `mat-icon` with `matTooltip`
   - Inject store, pass data to UI via inputs

4. **Shell Layer** (`shell/`)
   - Create routes with resolver pattern
   - Provide store and services

5. **App Routes Registration** (see `rules/tools/ui/page-layout.md`)
   - Add route to `apps/mxsecurity/mxsecurity/src/app/app.routes.ts`
   - Register in `appRoutes` children array with breadcrumb resolver

### Phase 4: Syntax Modernization

Apply Angular 20 syntax updates (see `rules/reference/angular-20-syntax.md`):

- `*ngIf` → `@if`
- `*ngFor` → `@for (item of items; track item.id)`
- `constructor(private service: Service)` → `inject()`
- `@Input()` → `input()`
- `@Output()` → `output()`
- `BehaviorSubject` → `signal()`

**Form Validation** (see `rules/tools/forms/validators.md`):

- `Validators.required` → `OneValidators.required` (no parentheses)
- `Validators.email` → `OneValidators.email` (no parentheses)
- `Validators.minLength(n)` → `OneValidators.minLength(n)`
- Import from `@one-ui/mxsecurity/shared/domain`

**UI Patterns**:

- Buttons (see `buttons.md`):
  - `mat-raised-button` → `mat-flat-button`
  - Form tooltips: Use `mxLabelTooltip` instead of `mat-icon` with `matTooltip`
  - Loading states: Use `MxLoadingButtonDirective` with `[mxButtonIsLoading]="loading()"`

- Page Layout (see `ui/page-layout.md`):
  - `mat-card` → `<div class="content-wrapper">`

- Dialogs (see `dialogs.md`):
  - Dialog sizing: Use `smallDialogConfig`, `mediumDialogConfig`, `largeDialogConfig`
  - Dialog API calls: Call API inside dialog, close only on success via `next` callback
  - Dialog viewContainerRef: Set `viewContainerRef: this.#viewContainerRef` when dialog uses store

- Tables (see `basics.md`):
  - Table toolbar buttons: Use `mat-stroked-button` with `general.button.create`/`general.button.delete`

**Translation Keys** (see `rules/reference/pitfalls/translation-layout.md`):

- **MUST use exact same translation keys as source**
- Read source HTML templates to find correct keys
- DO NOT create new keys or modify existing ones
- Example: `{{ 'general.common.name' | translate }}` → `{{ t('general.common.name') }}`

**Number-Only Input Directive** (see `rules/reference/pitfalls/forms-services.md`):

- **MUST replace `appNumberOnly` with `oneUiNumberOnly`**
- Import `NumberOnlyDirective` from `@one-ui/mxsecurity/shared/domain`

### Phase 5: Verification

```bash
# Type check
npx tsc --noEmit --project libs/mxsecurity/{page-name}/domain/tsconfig.lib.json

# Lint
nx lint mxsecurity-{page-name}-domain
nx lint mxsecurity-{page-name}-features
nx lint mxsecurity-{page-name}-ui
nx lint mxsecurity-{page-name}-shell

# Build
nx build mxsecurity-web
```

## Output Format

After completing migration analysis (Phase 1), save the analysis to:
`{target}/domain/src/lib/docs/MIGRATION-ANALYSIS.md`

## Example Usage

```
/migrate-page-gitlab --page time
/migrate-page-gitlab --page account
/migrate-page-gitlab --page ddns
```

These will automatically migrate to:

- `libs/mxsecurity/time-page`
- `libs/mxsecurity/account-page`
- `libs/mxsecurity/ddns-page`

## Reference Examples

- MAF Account Settings: `libs/maf/act-account/`
- Switch L3 Interface: `libs/switch/l3-interface/`
- MXsecurity Login: `libs/mxsecurity/login-page/`
