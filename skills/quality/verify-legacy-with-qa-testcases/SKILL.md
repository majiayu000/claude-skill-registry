---
name: verify-legacy-with-qa-testcases
description: Verify legacy code against QA test cases to confirm migration completeness.
---

# Verify Legacy Code with QA Test Cases

Use the new project's QA test cases to verify that the old (legacy) project's code implementation is complete and correct. This helps confirm migration completeness by checking if all expected behaviors exist in the legacy code.

**Important: Reports should be written in Traditional Chinese.**

## Arguments

- `$ARGUMENTS` - Path to the old project's source code to verify (e.g., `/Users/jayden/f2e-networking-jayden/apps/mxsecurity-web/src/app/pages/account`)

## Inputs

- **QA Test Cases**: Located in the new project's domain docs folder. Infer the path from the old project path structure.
  - Example: If old path is `.../pages/alg`, look for `libs/mxsecurity/alg-page/domain/src/lib/docs/QA-TEST-CASES.md`
- **Old Project Code**: `$ARGUMENTS`

## Verification Process

### Step 1: Read and Parse QA Test Cases

Read the QA-TEST-CASES.md file and extract:

1. **Form Fields and Validation Rules**
   - Field names, types, validators
   - Expected validation behavior

2. **Validation Error Messages**
   - Error conditions and expected messages

3. **Conditional Field Visibility**
   - Mode-based field visibility rules
   - Special conditions

4. **API Payload Format**
   - Expected request/response structures

5. **Boundary Test Cases**
   - Input validation boundaries

6. **Interaction Test Cases**
   - User flow expectations

### Step 2: Analyze Old Project Code

Read all relevant files from the old project path:

- `**/*.ts` - TypeScript files (components, services)
- `**/*.html` - Template files
- `**/*.component.ts` - Component logic
- `**/*.service.ts` - Service files

Extract from the old code:

1. **Form Definitions**
   - FormGroup/FormControl definitions
   - Validators used

2. **Validation Logic**
   - Validator implementations
   - Error handling

3. **Template Bindings**
   - Conditional rendering (`*ngIf`, `@if`)
   - Error message displays

4. **API Calls**
   - HTTP request payloads
   - Response handling

### Step 3: Generate Verification Report

Compare each test case requirement against the old code implementation.

**Output Format:**

````markdown
# Legacy Code Verification Report

Generated: {current_date}
QA Test Cases: {qa_test_cases_path}
Legacy Code Path: {old_project_path}

## Summary

| Category              | Total | Verified | Missing | Partial |
| --------------------- | ----- | -------- | ------- | ------- |
| Form Fields           | X     | X        | X       | X       |
| Validation Rules      | X     | X        | X       | X       |
| Error Messages        | X     | X        | X       | X       |
| Conditional Display   | X     | X        | X       | X       |
| API Payloads          | X     | X        | X       | X       |
| Boundary Test Cases   | X     | X        | X       | X       |
| Interaction Flows     | X     | X        | X       | X       |

## Detailed Verification

### 1. Form Fields Verification

| Field     | Expected                      | Found in Legacy | Status | Notes |
| --------- | ----------------------------- | --------------- | ------ | ----- |
| username  | text, required, maxLength(32) | Found           | PASS   |       |
| authority | select, required              | Found           | PASS   |       |
| ...       | ...                           | ...             | ...    | ...   |

### 2. Validation Rules Verification

| Rule                   | Expected Behavior    | Legacy Implementation              | Status |
| ---------------------- | -------------------- | ---------------------------------- | ------ |
| username.required      | Show error if empty  | `Validators.required` found        | PASS   |
| username.maxLength(32) | Limit to 32 chars    | `Validators.maxLength(32)` found   | PASS   |
| ...                    | ...                  | ...                                | ...    |

### 3. Error Messages Verification

| Field    | Error Type | Expected Key         | Found in Template | Status |
| -------- | ---------- | -------------------- | ----------------- | ------ |
| username | required   | validators.required  | Yes               | PASS   |
| username | duplicate  | validators.duplicate | No                | FAIL   |
| ...      | ...        | ...                  | ...               | ...    |

### 4. Conditional Display Verification

| Condition             | Expected Behavior | Legacy Implementation     | Status |
| --------------------- | ----------------- | ------------------------- | ------ |
| ADD mode: oldPassword | Hidden            | `*ngIf="!isAddMode"`      | PASS   |
| EDIT mode: username   | Disabled          | `[disabled]="isEditMode"` | PASS   |
| ...                   | ...               | ...                       | ...    |

### 5. API Payload Verification

| Operation       | Expected Payload                                            | Legacy Payload  | Status  | Difference    |
| --------------- | ----------------------------------------------------------- | --------------- | ------- | ------------- |
| Create (mode=1) | {userName, mode, userEnable, authority, new_pw, confirm_pw} | Matches         | PASS    |               |
| Edit (mode=3)   | {userName, mode, userEnable, authority}                     | Partial match   | PARTIAL | Missing: mode |
| ...             | ...                                                         | ...             | ...     | ...           |

### 6. Boundary Test Cases Verification

| Test Case ID | Requirement                   | Legacy Handling | Status |
| ------------ | ----------------------------- | --------------- | ------ |
| TC-USER-001  | Empty username → error        | Yes             | PASS   |
| TC-USER-006  | 33 chars → max length error   | Yes             | PASS   |
| ...          | ...                           | ...             | ...    |

### 7. Interaction Flow Verification

| Scenario           | Steps Verified | Status  | Missing Steps |
| ------------------ | -------------- | ------- | ------------- |
| Create new account | 8/8            | PASS    | None          |
| Edit account       | 7/7            | PASS    | None          |
| Change password    | 6/8            | PARTIAL | Steps 3, 4    |
| ...                | ...            | ...     | ...           |

## Issues Found

### Critical Issues (Must fix before migration)

1. **[Critical]** Missing validation: username `duplicate` validator
   - Location: `account-setting.component.ts`
   - Expected: Check for duplicate username in existing accounts
   - Found: No duplicate check implemented

2. **[Critical]** API payload mismatch: Edit operation missing `mode` field
   - Location: `account.service.ts:45`
   - Expected: `{ userName, mode: 3, userEnable, authority }`
   - Found: `{ userName, userEnable, authority }`

### Warnings (Should review)

1. **[Warning]** Different error message key
   - Expected: `validators.duplicate_password`
   - Found: `account.error.same_password`
   - Impact: Different translation key, may show wrong message

### Info (Minor differences)

1. **[Info]** Legacy code has additional validation
   - Legacy code trims username before validation
   - Not required but acceptable

## Migration Checklist

Based on verification results, these items need attention:

- [ ] Add username duplicate validation
- [ ] Fix Edit API payload to include mode field
- [ ] Update error message keys to match new standard
- [ ] Verify password comparison validation triggers correctly
- [ ] Test disable admin confirmation flow

## Reference Code Snippets

### Missing Duplicate Validator (add to new code)

```typescript
// Legacy location: account-setting.component.ts:XX
// This validation logic should be migrated:
{old_code_snippet}
```
````

### API Payload to Fix

```typescript
// Expected (from test cases):
{
  userName: string,
  mode: 3,
  userEnable: number,
  authority: number
}

// Found in legacy (account.service.ts:XX):
{old_api_payload}
```

````

### Step 4: Output Location

Save the verification report to the **new project's docs folder** (same location as QA-TEST-CASES.md):

```
{new_project_libs_path}/domain/src/lib/docs/LEGACY-VERIFICATION-REPORT.md
```

For example, if analyzing ALG page:
- QA Test Cases: `libs/mxsecurity/alg-page/domain/src/lib/docs/QA-TEST-CASES.md`
- Verification Report: `libs/mxsecurity/alg-page/domain/src/lib/docs/LEGACY-VERIFICATION-REPORT.md`

This keeps all documentation for a feature together in the new project repository.

**Important: Reports should be written in Traditional Chinese.**

## Usage Example

```bash
# Verify legacy ALG page implementation against new QA test cases
/verify-legacy-with-qa-testcases /Users/jayden/f2e-networking-jayden/apps/mxsecurity-web/src/app/pages/alg

# Verify legacy account page implementation
/verify-legacy-with-qa-testcases /Users/jayden/f2e-networking-jayden/apps/mxsecurity-web/src/app/pages/account
```

## Notes

- Reports should be written in Traditional Chinese
- Focus on functional requirements, not implementation details
- Flag differences between expected behavior (test cases) and actual code (legacy code)
- Highlight missing functionality that needs to be added during migration
- Identify outdated patterns in legacy code that should NOT be migrated

## Items NOT to Flag as Issues

The following differences are expected and handled by the new project architecture. Do not report these as issues:

1. **Apply Button Loading State** - New project always uses `[mxButtonIsLoading]="loading()"` and `[disabled]="loading()"` on Apply buttons. Legacy code may not have this.
2. **formTouchedGuard** - New project uses `canDeactivate: [formTouchedGuard]` for unsaved changes warning. Legacy code may not have this.
3. **Auto-reload after save** - New project calls `loadPageData()` after successful save. Legacy code may only show success toast.
4. **SignalStore vs HttpClient** - New project uses NgRx SignalStore. Legacy code uses direct HttpClient calls.
5. **Transloco vs ngx-translate** - New project uses `@jsverse/transloco`. Legacy code uses `@ngx-translate/core`.
6. **Standalone components** - New project uses standalone components. Legacy code may use NgModules.
7. **Breadcrumb component** - New project includes `<one-ui-breadcrumb />`. Legacy code may not have this.
8. **untracked() in effects** - New project wraps `setValue()` calls in `untracked()`. Legacy code may not.
9. **Range validator vs min/max validators** - New project uses `OneValidators.range(min, max)` for combined range validation. Legacy code uses separate `Validators.min()` and `Validators.max()`. Functionally equivalent, this is an expected difference.
10. **Apply button checks form validity** - New project uses `[disabled]="form.invalid || noPermission()"` on Apply buttons. Legacy code may only check `noPermission`. This is an improvement in the new project.
11. **Form check bugs in legacy** - Legacy project may use wrong form name in `onSubmit` method (e.g., `generalForm.invalid` instead of `serverForm.invalid`). These are legacy bugs that are fixed in the new project.
12. **Missing error messages in templates** - Legacy project may be missing error messages for certain fields (e.g., required errors). New project uses `oneUiFormError` directive to handle these automatically.
