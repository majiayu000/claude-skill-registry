---
name: review-changes
description: Code review of current git changes, compare to related plan if exists, identify bad engineering, over-engineering, or suboptimal solutions. Use when user asks to review changes, check git diff, validate implementation quality, or assess code changes.
---

# Review Git Changes

## Instructions

Perform thorough code review of current working copy changes, optionally compare to plan, and identify engineering issues.

### Phase 1: Discover Changes & Context

#### Step 1: Get Current Changes
```bash
# See changed files
git status

# See detailed diff
git diff

# See staged changes separately
git diff --cached

# See both staged and unstaged
git diff HEAD
```

#### Step 2: Identify Related Plan (if exists)

Search for related plan file:
- Check `.plans/` directory for relevant plan
- Look for plan mentioned in branch name
- Ask user if unsure which plan applies
- If no plan exists, review against general best practices

If plan exists:
- Read the entire plan
- Understand intended design and architecture
- Note specific requirements and constraints

#### Step 3: Categorize Changed Files

Group files by type:
- **New files**: Created from scratch
- **Modified files**: Existing files changed
- **Deleted files**: Removed files
- **Renamed/moved files**: Organizational changes

Create todo list with one item per changed file to review.

### Phase 2: Systematic File Review

For EACH changed file in the todo list:

#### Step 1: Read Current State
- Read the entire file in its current state
- Understand what it does
- Note its responsibilities

#### Step 2: Analyze the Changes

Read git diff to see exactly what changed:
- What was added?
- What was removed?
- What was modified?

#### Step 3: Assess Against Plan (if applicable)

If plan exists, check:
- **Does implementation match plan?**
  - Are planned features implemented correctly?
  - Is architecture followed?
  - Are file names as specified?

- **Scope adherence**:
  - Is this change in the plan?
  - Is it necessary for the plan's goals?
  - Is it scope creep?

- **REMOVAL SPEC compliance**:
  - If plan said to remove code, was it removed?
  - Is old code still present when it shouldn't be?

#### Step 4: Identify Engineering Issues

Check for **Bad Engineering**:
- **Bugs**: Logic errors, off-by-one, race conditions
- **Poor error handling**: Swallowed errors, generic catches
- **Missing validation**: No input validation, no null checks
- **Hard-coded values**: Magic numbers, hardcoded URLs/paths
- **Tight coupling**: Unnecessary dependencies between modules
- **Violation of SRP**: Class/function doing too many things
- **Incorrect patterns**: Misuse of design patterns
- **Type issues**: Use of `any`, missing types, wrong types
- **Missing edge cases**: Doesn't handle empty/null/error cases

Check for **Over-Engineering**:
- **Unnecessary abstraction**: Too many layers for simple logic
- **Premature optimization**: Complex code for unmeasured performance
- **Framework overuse**: Using heavy library for simple task
- **Feature creep**: Adding features not in requirements
- **Gold plating**: Excessive polish on non-critical code
- **YAGNI violations**: Code for "might need later" scenarios
- **Complexity without benefit**: Complicated when simple works

Check for **Suboptimal Solutions**:
- **Duplication**: Copy-pasted code instead of extraction
- **Reinventing wheel**: Custom code when standard library exists
- **Wrong tool**: Using inappropriate data structure/algorithm
- **Inefficient approach**: O(n²) when O(n) is obvious
- **Poor naming**: Unclear variable/function names
- **Missing reuse**: Existing utilities/types not used
- **Inconsistent patterns**: Doesn't match codebase style
- **Technical debt**: Quick hack instead of proper solution

#### Step 5: Check Code Quality

- **Readability**: Is code clear and self-documenting?
- **Maintainability**: Will this be easy to change later?
- **Testability**: Can this be tested easily?
- **Performance**: Any obvious performance issues?
- **Security**: Any security vulnerabilities?
- **Consistency**: Matches existing codebase patterns?

#### Step 6: Record Findings

Store in memory:
```
File: path/to/file.ts
Change Type: [New|Modified|Deleted]
Plan Compliance: [Matches|Deviates|Not in plan]
Issues:
  Bad Engineering:
    - [Specific issue with line number]
  Over-Engineering:
    - [Specific issue with line number]
  Suboptimal:
    - [Specific issue with line number]
Severity: [CRITICAL|HIGH|MEDIUM|LOW]
```

#### Step 7: Update Todo
Mark file as reviewed in todo list.

### Phase 2.5: Issue/Task Coverage Verification (MANDATORY)

**CRITICAL**: Before completing the review, verify that 100% of the original issue/task requirements are implemented.

#### Step 1: Identify Source Requirements

Locate the original requirements from:
- GitHub issue (`gh issue view <number>`)
- PR description referencing issues
- Task ticket or plan file in `.plans/`
- Commit messages describing the work

#### Step 2: Extract ALL Requirements

Create exhaustive checklist:
- Functional requirements (what it should do)
- Acceptance criteria (how to verify)
- Edge cases mentioned
- Error handling requirements

#### Step 3: Verify Each Requirement

| # | Requirement | Status | Evidence |
|---|-------------|--------|----------|
| 1 | [requirement] | ✅/❌/⚠️ | file:line or "Missing" |

#### Step 4: Coverage Assessment

```
Requirements Coverage = (Implemented / Total) × 100%
```

**Anything less than 100% = REQUEST CHANGES immediately**

Add to report:
```markdown
## Issue/Task Coverage

**Source**: [Issue #X / Plan file]
**Coverage**: X% (Y of Z requirements)

### Missing Requirements
- ❌ [Requirement X]: Not implemented
- ❌ [Requirement Y]: Partially implemented - [what's missing]

**VERDICT**: Coverage incomplete. Cannot approve until 100% implemented.
```

### Phase 3: Cross-File Analysis

After reviewing all files:

#### Step 1: Architectural Impact
- How do changes affect overall system architecture?
- Are there breaking changes?
- Do changes introduce new dependencies?
- Is there architectural drift from the plan?

#### Step 2: Pattern Consistency
- Are changes consistent with each other?
- Do they follow same patterns?
- Any conflicting approaches?

#### Step 3: Completeness Check
- Are all related changes present?
- Missing files that should be changed?
- Orphaned references?

### Phase 4: Generate Review Report

Create report at `.reviews/code-review-[timestamp].md`:

```markdown
# Code Review Report
**Date**: [timestamp]
**Branch**: [branch name]
**Related Plan**: [plan file or "None"]
**Files Changed**: X
**Issues Found**: Y

---

## Executive Summary
- **Critical Issues**: X (must fix before merge)
- **High Priority**: Y (should fix)
- **Medium Priority**: Z (consider fixing)
- **Low Priority**: W (suggestions)

**Overall Assessment**: [APPROVE|REQUEST CHANGES|REJECT]

---

## Plan Compliance (if applicable)

### Matches Plan ✅
- Feature X implemented correctly
- Architecture follows design
- File naming conventions followed

### Deviates from Plan ⚠️
- Implementation differs from planned approach in [area]
- Missing feature Y from plan
- Scope creep: Added Z not in plan

### REMOVAL SPEC Status
- ✅ Old code removed from `file.ts:50-100`
- ❌ Legacy function still exists in `auth.ts:42` (should be removed)

---

## Issues by Severity

### CRITICAL: Bad Engineering

#### Logic Bug in `src/services/auth.ts:125`
```typescript
// Current code:
if (user.role = 'admin') { // Assignment instead of comparison
  grantAccess()
}
```
**Issue**: Assignment operator used instead of equality check. This always evaluates to true and grants everyone admin access.
**Severity**: CRITICAL - Security vulnerability
**Fix**: Change `=` to `===`

#### Unhandled Promise in `src/api/client.ts:67`
```typescript
// Current code:
fetchData().then(data => process(data)) // No error handling
```
**Issue**: Promise rejection not handled, will crash silently
**Severity**: CRITICAL - Application stability
**Fix**: Add `.catch()` or use try/catch with async/await

### HIGH: Over-Engineering

#### Unnecessary Abstraction in `src/utils/formatter.ts`
```typescript
// Current code: 50 lines of abstraction
class FormatterFactory {
  createFormatter(type: string): IFormatter { /* ... */ }
}
class StringFormatter implements IFormatter { /* ... */ }
// ... only used once for simple string formatting
```
**Issue**: Complex factory pattern for single use case
**Severity**: HIGH - Maintenance burden
**Better Approach**: Simple function `formatString(value: string): string`

### MEDIUM: Suboptimal Solutions

#### Code Duplication in `src/components/`
**Files**: `user-form.tsx`, `admin-form.tsx`
**Issue**: Both contain identical validation logic (30 lines duplicated)
**Severity**: MEDIUM - Maintenance issue
**Better Approach**: Extract to `src/utils/form-validation.ts`

#### Not Using Existing Type in `src/types/user.ts`
```typescript
// Current code:
interface UserData {
  id: string
  email: string
  name: string
}
// But `User` type already exists with same fields in `src/models/user.ts`
```
**Issue**: Duplicate type definition
**Severity**: MEDIUM - Type inconsistency risk
**Fix**: Import and use existing `User` type

### LOW: Suggestions

#### Verbose Naming in `src/services/database-connection-manager.ts`
**Issue**: Overly verbose filename
**Suggestion**: Simplify to `src/services/database.service.ts`

---

## Issues by Category

### Bad Engineering (X issues)
- Logic bugs: X
- Missing error handling: Y
- Type issues: Z
- Missing validation: W

### Over-Engineering (Y issues)
- Unnecessary abstraction: X
- Premature optimization: Y
- Feature creep: Z

### Suboptimal Solutions (Z issues)
- Code duplication: X
- Reinventing wheel: Y
- Poor naming: Z
- Not using existing code: W

---

## Architectural Assessment

### Positive Changes
- Clean separation of concerns in new modules
- Proper use of dependency injection
- Good test coverage added

### Concerns
- New dependency introduced without discussion
- Breaking change to public API
- Coupling between previously independent modules

### Technical Debt Introduced
- Quick hack in `auth.ts:200` marked with TODO
- Temporary file `temp-processor.ts` added
- Migration code that should be removed later

---

## Detailed File Reviews

### src/services/auth.ts (Modified)
**Plan Compliance**: Matches
**Changes**: 45 lines added, 20 removed
**Issues**:
- CRITICAL: Logic bug at line 125 (assignment vs equality)
- HIGH: Missing error handling at line 89
**Positive**:
- Good use of existing types
- Clear function names

### src/components/user-form.tsx (New)
**Plan Compliance**: Not in plan (scope creep)
**Changes**: 150 lines added
**Issues**:
- MEDIUM: Duplicates logic from admin-form.tsx
- LOW: Could use existing form validation utility
**Positive**:
- Clean component structure
- Good TypeScript usage

[Continue for all changed files]

---

## Statistics

**By Severity**:
- Critical: X
- High: Y
- Medium: Z
- Low: W

**By Category**:
- Bad Engineering: X
- Over-Engineering: Y
- Suboptimal: Z

**By File Type**:
- Services: X issues
- Components: Y issues
- Utils: Z issues

---

## Recommendations

### Must Fix (Before Merge)
1. Fix logic bug in `auth.ts:125` - Security issue
2. Add error handling in `client.ts:67` - Stability issue
3. Remove temporary file `temp-processor.ts` - Plan violation

### Should Fix
1. Extract duplicated validation logic
2. Simplify over-abstracted formatter
3. Use existing types instead of duplicates

### Consider
1. Rename verbose files
2. Add more inline documentation
3. Improve variable naming in complex functions

---

## Overall Assessment

**Recommendation**: REQUEST CHANGES

**Reasoning**:
- 2 critical security/stability issues must be fixed
- Over-engineering in several areas adds unnecessary complexity
- Code duplication will cause maintenance issues
- Some scope creep not discussed in plan

**After Fixes**: Changes will be solid. Core implementation is sound, just needs cleanup and bug fixes.
```

### Phase 5: Summary for User

Provide concise summary:

```markdown
# Code Review Complete

## Assessment: [APPROVE|REQUEST CHANGES|REJECT]

## Critical Issues (X)
- Security bug in `auth.ts:125` - assignment vs equality
- Unhandled promise in `client.ts:67` - will crash

## High Priority (Y)
- Over-engineering in `formatter.ts` - unnecessary abstraction
- Missing error handling in multiple files

## Medium Priority (Z)
- Code duplication between forms
- Not using existing types

## Plan Compliance
- ✅ Core features implemented correctly
- ⚠️ Some scope creep (user-form not in plan)
- ❌ REMOVAL SPEC incomplete (legacy code still exists)

## Must Fix Before Merge
1. Fix logic bug in auth.ts
2. Add error handling
3. Remove legacy code per REMOVAL SPEC

**Full Report**: `.reviews/code-review-[timestamp].md`
```

## Critical Principles

- **NEVER EDIT FILES** - This is review only, not implementation
- **BE THOROUGH** - Review every changed file
- **BE SPECIFIC** - Point to exact line numbers
- **BE CONSTRUCTIVE** - Explain why and suggest better approach
- **CHECK PLAN** - If plan exists, verify compliance
- **VERIFY REMOVAL SPEC** - Ensure old code was removed
- **IDENTIFY PATTERNS** - Note systemic issues across files
- **BE HONEST** - Don't approve bad code to be nice
- **SUGGEST ALTERNATIVES** - Don't just criticize, help improve

## Success Criteria

A complete code review includes:
- **100% of issue/task requirements verified as implemented**
- All changed files reviewed
- Plan compliance verified (if plan exists)
- All engineering issues identified and categorized
- Severity assigned to each issue
- Specific line numbers referenced
- Alternative approaches suggested
- Overall assessment provided
- Structured report generated

**CRITICAL**: If issue/task coverage is less than 100%, the review MUST request changes regardless of code quality.
