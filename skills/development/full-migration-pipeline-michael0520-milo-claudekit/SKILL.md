---
name: full-migration-pipeline
description: Complete Angular migration pipeline that orchestrates all migration skills in sequence. Use when performing end-to-end page migration with analysis, implementation, quality checks, and QA verification.
---

# Full Migration Pipeline

Automated execution of the complete Angular migration workflow, orchestrating all related skills in sequence.

## Arguments

- `$ARGUMENTS` - Format: `--from <source_path> --to <target_path>` or `--page <page_name>`
  - `--from`: Legacy project path (e.g., `/Users/jayden/f2e-networking-jayden/apps/mxsecurity-web/src/app/pages/account`)
  - `--to`: New project path (e.g., `libs/mxsecurity/account-page`)
  - `--page`: GitLab page name (e.g., `time`, `account`) - When using this parameter, source code is automatically fetched from GitLab

## Pipeline Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    FULL MIGRATION PIPELINE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 1: Analysis                                               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 1.1 Execute migrate-page (analysis + document generation)│    │
│  │ 1.2 Execute form-extraction (extract form structure)     │    │
│  │     Output: MIGRATION-ANALYSIS.md                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                           ↓                                      │
│  Phase 2: Implementation (Manual)                                │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 2.1 Create Domain Layer (model, api, store, helper)      │    │
│  │ 2.2 Create UI Layer (tables, forms)                       │    │
│  │ 2.3 Create Features Layer (page, dialogs)                 │    │
│  │ 2.4 Create Shell Layer (routes)                           │    │
│  │     [Await user confirmation]                             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                           ↓                                      │
│  Phase 3: Quality Assurance                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 3.1 Execute migration-lint (compliance check + auto-fix) │    │
│  │ 3.2 Execute migration-review (migration completeness)    │    │
│  │ 3.3 Execute compare-i18n-keys (translation key compare)  │    │
│  │ 3.4 Execute check-barrel-files (check redundant barrels) │    │
│  └─────────────────────────────────────────────────────────┘    │
│                           ↓                                      │
│  Phase 4: QA Verification                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 4.1 Execute generate-qa-test-cases (generate test cases) │    │
│  │ 4.2 Execute verify-legacy-with-qa-testcases (verify old) │    │
│  │     Output: QA-TEST-CASES.md, LEGACY-VERIFICATION-REPORT.md│   │
│  └─────────────────────────────────────────────────────────┘    │
│                           ↓                                      │
│  Phase 5: Final Report                                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Output MIGRATION-SUMMARY.md (consolidate all results)    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Execution Flow

### Phase 1: Analysis

**Automated Execution:**

1. **Determine Source Type**
   - If `--page` is provided: Use GitLab API to fetch source code
   - If `--from` is provided: Use local files

2. **Execute Migration Analysis**
   ```
   Execute based on source type:
   - /migrate-page --from={source} --to={target}
   - /migrate-page-gitlab --page={page_name}
   ```

3. **Extract Form Structure** (Auxiliary Analysis)
   - Read form definitions from source code
   - List all formControlName and validators

**Output:**
- `{target}/domain/src/lib/docs/MIGRATION-ANALYSIS.md`

**User Prompt:**
> Phase 1 analysis complete. Proceed to Phase 2 implementation?

---

### Phase 2: Implementation

**Implementation Guidelines:**

Display pending implementation checklist (based on MIGRATION-ANALYSIS.md):

```markdown
## Implementation Checklist

### Domain Layer
- [ ] Create `{feature}.model.ts` - API types, view models
- [ ] Create `{feature}.api.ts` - API service (inline URLs directly, do not use constants)
- [ ] Create `{feature}.store.ts` - SignalStore
- [ ] Create `{feature}.helper.ts` - Pure functions (if needed)

### Features Layer (Implement First)
- [ ] Create Page component
- [ ] Create Dialog components (if applicable)
- [ ] Verify store injection

### UI Layer (Extract from Features)
- [ ] Extract Table components to UI layer
- [ ] Extract Form components to UI layer
- [ ] Verify input()/output() usage, no store injection

### Shell Layer
- [ ] Create routes
- [ ] Register in app.routes.ts
```

#### Important: Form/Table Extraction to UI Layer

**Implementation Order:**
1. First complete page functionality in Features Layer
2. Then extract Form and Table to UI Layer
3. Features Layer should only retain orchestration code

**Extraction Criteria:**
- `<form>` containing `<mat-form-field>` -> Extract to UI
- Tables -> Prefer `common-table` pattern (reference `libs/mxsecurity/shared/ui/src/lib/common-table`)
- Dialogs remain in Features (but forms inside Dialogs can be extracted to UI)

**Table Implementation Approach:**
- Prefer using `CommonTableComponent` with `MxColumnDef[]` for column definitions
- Only create standalone table component in UI layer for complex customization requirements

**Exceptions (No Extraction Required):**
- Extremely simple pages (e.g., only radio group without form validation)
- Components used by a single page without complex form logic

#### Patterns to Avoid

```typescript
// DO NOT use TRANSLOCO_SCOPE
providers: [{ provide: TRANSLOCO_SCOPE, useValue: { scope: 'xxx' } }]

// DO NOT use endpoint constants
readonly #ENDPOINTS = { API: '/api/xxx' };

// CORRECT: Inline URLs directly
this.#rest.get('/api/xxx');
```

#### Chunked Migration Strategy (Reducing Omission Risk)

**Principle: Process from large sections to small units, completing each before proceeding**

```
Page Structure Analysis:
┌─────────────────────────────────────┐
│ Page                                │
│ ┌─────────────────────────────────┐ │
│ │ mat-tab-group                   │ │
│ │ ┌───────────┬───────────┐       │ │
│ │ │  Tab 1    │  Tab 2    │       │ │
│ │ ├───────────┴───────────┤       │ │
│ │ │ mat-card / section 1  │       │ │
│ │ ├───────────────────────┤       │ │
│ │ │ mat-card / section 2  │       │ │
│ │ └───────────────────────┘       │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

**Step 1: Segment by `mat-tab`**
- First identify the number of tabs on the page
- Process each tab independently, completing one before proceeding to the next
- Create a checklist corresponding to each tab

**Step 2: Segment by `mat-card` / `content-wrapper`**
- Within each tab, identify all cards/sections
- Treat each card as an independent migration unit
- Verify immediately after completing each card

**Step 3: Migrate and Verify Incrementally**
- Migration order: top to bottom, left to right
- Execute `/migration-lint` after completing each segment
- Compare with legacy code to confirm no omissions

**Example Checklist:**
```markdown
## Chunked Migration Progress

### Tab 1: General Settings
- [x] Card 1.1: Basic Info
- [x] Card 1.2: Network Config
- [ ] Card 1.3: Advanced Options

### Tab 2: Security
- [ ] Card 2.1: Authentication
- [ ] Card 2.2: Certificates
```

**Generate Library Structure:**
```bash
nx g @one-ui/one-plugin:library mxsecurity {page-name} all
```

**Await User Confirmation:**
> After completing the above implementation, enter "done" or "continue" to proceed to Phase 3.
> For pattern queries, use /migration-patterns <keyword>

---

### Phase 3: Quality Assurance

**Automated Execution:**

1. **Compliance Check + Auto-fix**
   ```
   /migration-lint {target}
   ```
   - Auto-fix: mat-raised-button -> mat-flat-button
   - Auto-fix: *ngIf -> @if
   - Auto-fix: Validators -> OneValidators
   - Generate compliance report

2. **Migration Completeness Check**
   ```
   /migration-review --from={source} --to={target}
   ```
   - Compare form controls
   - Compare validators
   - Compare translation keys
   - Compare event bindings

3. **Translation Key Comparison** (For primary HTML files)
   ```
   /compare-i18n-keys --from={source}/*.html --to={target}/**/*.html
   ```

4. **Check Redundant Barrel Files**
   ```
   /check-barrel-files {target}
   ```

**Output:**
- Reports for each check (displayed in conversation)
- List of auto-fixed changes

**User Prompt:**
> Phase 3 quality assurance complete. X issues auto-fixed, Y issues require manual intervention.
> Proceed to Phase 4 QA verification?

---

### Phase 4: QA Verification

**Automated Execution:**

1. **Generate QA Test Cases**
   ```
   /generate-qa-test-cases {target}
   ```
   - Extract test cases from new code
   - Generate structured test report

2. **Verify Legacy Code**
   ```
   /verify-legacy-with-qa-testcases {source}
   ```
   - Verify legacy code using test cases
   - Confirm functional consistency

**Output:**
- `{target}/domain/src/lib/docs/QA-TEST-CASES.md`
- `{target}/domain/src/lib/docs/LEGACY-VERIFICATION-REPORT.md`

---

### Phase 5: Final Report

**Auto-generate MIGRATION-SUMMARY.md:**

```markdown
# {Feature Name} Migration Summary Report

**Migration Date:** {date}
**Source:** {source_path}
**Target:** {target_path}

## Migration Status

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 1: Analysis | Complete | |
| Phase 2: Implementation | Complete | |
| Phase 3: Quality Assurance | Complete | X items auto-fixed |
| Phase 4: QA Verification | Complete | |

## Generated Documents

- [x] MIGRATION-ANALYSIS.md
- [x] QA-TEST-CASES.md
- [x] LEGACY-VERIFICATION-REPORT.md
- [x] MIGRATION-SUMMARY.md (this document)

## Compliance Report Summary

### Auto-fixed Items
{List of auto-fixed items}

### Items Requiring Manual Intervention
{List of items requiring manual intervention}

## Migration Completeness

| Category | Source | Target | Completeness |
|----------|--------|--------|--------------|
| Form Controls | X | X | 100% |
| Validators | X | X | 100% |
| Translation Keys | X | X | 100% |
| Event Bindings | X | X | 100% |

## Next Steps

1. [ ] Execute comprehensive testing
2. [ ] Code Review
3. [ ] Merge to main branch
```

**Output Location:** `{target}/domain/src/lib/docs/MIGRATION-SUMMARY.md`

---

## Usage Examples

### Migration from Local Source

```bash
/full-migration-pipeline --from=/Users/jayden/f2e-networking-jayden/apps/mxsecurity-web/src/app/pages/account --to=libs/mxsecurity/account-page
```

### Migration from GitLab

```bash
/full-migration-pipeline --page=account
```

## Interruption and Resumption

If the workflow is interrupted, continue from a specific phase:

```bash
# Execute Phase 3 quality assurance only
/migration-lint libs/mxsecurity/account-page

# Execute Phase 4 QA verification only
/generate-qa-test-cases libs/mxsecurity/account-page
/verify-legacy-with-qa-testcases /path/to/legacy
```

## Auxiliary Skills

Available for use at any point during pipeline execution:

| Skill | Purpose |
|-------|---------|
| `/migration-patterns <keyword>` | Query migration patterns |
| `/icon-replacement <icon>` | Find replacement icons |
| `/ui-layout-guide <query>` | UI layout guidelines |
