---
name: check-plan
description: Audit implementation progress against a plan, verify completed work, identify remaining tasks, and validate quality. Use when user asks to check plan status, verify implementation, see what's left to do, or validate plan completion.
---

# Check Plan Implementation

## Instructions

Perform comprehensive audit of implementation progress against a plan, verify quality of completed work, and generate actionable task list for remaining items.

### Phase 1: Setup & Discovery

#### Step 1: Identify the Plan
- Ask user which plan to check (or identify from context)
- Read the plan file from `.plans/`
- Understand all plan items and requirements

#### Step 2: Get Git Context (if applicable)
```bash
# See what files changed
git status

# See detailed changes
git diff

# See commit history on this branch
git log --oneline -20
```

This helps understand scope of changes made.

#### Step 3: Identify All Affected Files

Create comprehensive list:
1. Files mentioned in the plan
2. Files shown in `git status`
3. Files that might be affected (use Glob/Grep)

Create todo list with one item per file to check.

### Phase 2: Systematic File-by-File Audit

For EACH file in the todo list:

#### Step 1: Read the File
- Use Read tool to examine current state
- Check memory/context for any previous notes about this file

#### Step 2: Map to Plan Items
Identify which plan step(s) relate to this file:
- Which implementation steps mention this file?
- What changes were supposed to be made?
- What requirements from the plan apply here?

#### Step 3: Verify Implementation

Check if planned changes are present:
- ✅ **DONE**: Implementation matches plan requirements
- ⚠️ **PARTIAL**: Some work done, but incomplete
- ❌ **NOT DONE**: No implementation yet
- 🔍 **NEEDS REVIEW**: Implementation exists but may not match plan

For each file, assess:
- Are planned features implemented?
- Is code quality good?
- Are types used correctly (no `any`)?
- Does it follow CLAUDE.md guidelines?
- Is it complete or partial?

#### Step 4: Quality Verification

Check implementation quality:
- **Correctness**: Does it work as planned?
- **Types**: Proper typing, no `any`, using existing types?
- **Naming**: Follows conventions from plan?
- **Architecture**: Matches planned design?
- **Completeness**: All details from plan step implemented?

#### Step 5: Record Assessment

Store in memory:
```
File: path/to/file.ts
Plan Item: Step X - [description]
Status: [DONE|PARTIAL|NOT DONE|NEEDS REVIEW]
Notes: [What's good, what's missing, what needs fixing]
Quality Issues: [Any problems found]
```

#### Step 6: Update Todo
Mark file as checked in the todo list.

### Phase 3: REMOVAL SPEC Verification

**CRITICAL**: Verify old code was actually removed.

#### Step 1: Read REMOVAL SPEC from Plan
Extract all items listed for removal:
- Code to be removed (with file/line numbers)
- Files to be deleted
- Deprecated functions to eliminate

#### Step 2: Verify Each Removal

For each item in REMOVAL SPEC:

1. **For code to remove**:
   ```bash
   # Check if old code still exists
   grep -n "old_function_name" path/to/file.ts
   ```
   - ✅ If not found: Code successfully removed
   - ❌ If found: Code still exists (NOT DONE)

2. **For files to delete**:
   ```bash
   # Check if file still exists
   ls path/to/old-file.ts
   ```
   - ✅ If not found: File successfully deleted
   - ❌ If found: File still exists (NOT DONE)

3. **For deprecated imports/references**:
   ```bash
   # Search entire codebase
   grep -r "old_symbol" src/
   ```
   - ✅ If not found: All references removed
   - ❌ If found: References still exist (NOT DONE)

#### Step 3: Record Removal Status
- List what was supposed to be removed
- List what actually was removed
- **Flag any items not removed as HIGH PRIORITY tasks**

### Phase 3.5: Original Issue/Task Coverage Verification (MANDATORY)

**CRITICAL**: Verify that the implementation covers 100% of the ORIGINAL issue/task requirements, not just the plan steps.

#### Step 1: Locate Original Issue/Task

Find the source requirement:
- GitHub issue that triggered this plan: `gh issue view <number>`
- Original task description or ticket
- User request that initiated the work

#### Step 2: Extract ALL Original Requirements

From the original issue/task, extract:
- Every functional requirement
- Every acceptance criterion
- Every edge case mentioned
- Every error handling requirement
- Any implicit requirements

#### Step 3: Map Requirements to Implementation

| # | Original Requirement | Plan Step | Implementation Status |
|---|---------------------|-----------|----------------------|
| 1 | [from issue] | Step X | ✅/❌/⚠️ |
| 2 | [from issue] | Step Y | ✅/❌/⚠️ |
| 3 | [from issue] | N/A (missing from plan!) | ❌ |

#### Step 4: Identify Coverage Gaps

**Two types of gaps:**
1. **Plan gaps**: Requirements from issue that weren't captured in plan
2. **Implementation gaps**: Plan steps that weren't fully implemented

Both count toward incomplete coverage.

#### Step 5: Coverage Assessment

```
Issue Coverage = (Implemented Original Requirements / Total Original Requirements) × 100%
```

**Anything less than 100% = PLAN NOT COMPLETE**

### Phase 4: Gap Analysis

#### Step 1: Identify Scope Creep
Files changed that are NOT in the plan:
- Why were they changed?
- Were changes necessary?
- Should plan be updated to reflect them?

#### Step 2: Identify Missing Work
Plan items without corresponding implementation:
- Which steps haven't been started?
- Which steps are partially complete?
- What's blocking completion?

#### Step 3: Identify Issue Coverage Gaps (HIGH PRIORITY)
Requirements from original issue not in implementation:
- Which issue requirements are missing?
- Were they missed in planning or implementation?
- These are **HIGHER PRIORITY** than plan step completion

### Phase 5: Build Progress Report

#### Step 1: Calculate Completion Percentage

```
Total Plan Steps: X
Completed Steps: Y
Partial Steps: Z
Not Started: W

Completion: (Y / X) * 100%
Weighted Completion: ((Y + 0.5*Z) / X) * 100%
```

#### Step 2: Generate Structured Report

Create report at `.plans/[plan-name].progress.md`:

```markdown
# Plan Progress Report: [Plan Name]
**Date**: [timestamp]
**Plan File**: [path]
**Status**: [In Progress | Ready for Review | Completed]

---

## Summary
- **Overall Completion**: X%
- **Steps Complete**: Y / Total
- **Steps Partial**: Z
- **Steps Not Started**: W
- **Critical Issues**: N

---

## Progress by Plan Step

### ✅ Step 1: [Description]
**Status**: DONE
**Files**: [list]
**Notes**: [Any relevant notes]

### ⚠️ Step 2: [Description]
**Status**: PARTIAL (60% complete)
**Files**: [list]
**Completed**:
- [What's done]
**Remaining**:
- [What's not done]
**Issues**: [Any problems]

### ❌ Step 3: [Description]
**Status**: NOT DONE
**Blocking**: [What's blocking this]

---

## REMOVAL SPEC Status

### ✅ Completed Removals
- `old_function` from `file.ts` - Successfully removed
- `old-file.ts` - Successfully deleted

### ❌ Pending Removals (HIGH PRIORITY)
- `legacy_code` from `file.ts:lines 50-100` - **STILL EXISTS**
- `deprecated-helper.ts` - **FILE STILL EXISTS**

**Critical**: Old code must be removed before plan can be marked complete.

---

## Quality Assessment

### Passed
- ✅ TypeScript types used correctly
- ✅ CLAUDE.md naming conventions followed
- ✅ Architecture matches plan

### Issues Found
- ⚠️ `any` type used in `file.ts:42` (should use existing type)
- ⚠️ Missing error handling in step 5 implementation

---

## Files Changed

### Planned Changes (from plan)
- ✅ `path/to/file1.ts` - DONE
- ⚠️ `path/to/file2.ts` - PARTIAL
- ❌ `path/to/file3.ts` - NOT DONE

### Unplanned Changes (scope creep)
- `path/to/unexpected.ts` - Why: [reason]

---

## Remaining Work

### High Priority
1. **Remove old code** (REMOVAL SPEC items)
   - [ ] Remove `legacy_code` from `file.ts`
   - [ ] Delete `deprecated-helper.ts`

2. **Complete Step 3**
   - [ ] Implement [specific requirement]
   - [ ] Add proper types

### Medium Priority
3. **Fix quality issues**
   - [ ] Replace `any` in `file.ts:42`
   - [ ] Add error handling in step 5

### Low Priority
4. **Polish**
   - [ ] [Minor improvements]

---

## Validation Status

### Pre-Validation
- [ ] All plan steps completed
- [ ] All REMOVAL SPEC items removed
- [ ] TypeScript compiles
- [ ] Linting passes
- [ ] No `any` types added

**Ready for Final Validation**: NO (pending items remain)

---

## Next Steps

1. Complete REMOVAL SPEC items (remove old code)
2. Finish Step 3 implementation
3. Fix quality issues
4. Run validation checks
5. Update plan status when 100% complete
```

### Phase 6: Validation Checks

#### Step 1: Run TypeScript Check
```bash
# Run type checking
npm run typecheck
# or
tsc --noEmit
```

Record results:
- ✅ Passes: Good to go
- ❌ Errors: List errors, add to remaining work

#### Step 2: Run Linting
```bash
# Run linter
npm run lint
# or
eslint .
```

Record results:
- ✅ Passes: Good to go
- ⚠️ Warnings: List warnings
- ❌ Errors: List errors, add to remaining work

#### Step 3: Run Build (if applicable)
```bash
npm run build
```

Ensure build succeeds.

### Phase 7: Generate Task List

Create actionable todo list for remaining work:

```markdown
# Remaining Tasks for [Plan Name]

## Critical (Must Do)
- [ ] Remove `legacy_code` from `file.ts:50-100` (REMOVAL SPEC)
- [ ] Delete `deprecated-helper.ts` (REMOVAL SPEC)
- [ ] Complete Step 3: [description]

## Important (Should Do)
- [ ] Fix TypeScript error in `file.ts:42`
- [ ] Add error handling in step 5

## Polish (Nice to Have)
- [ ] [Minor improvement]

## Validation
- [ ] TypeScript passes (`npm run typecheck`)
- [ ] Linting passes (`npm run lint`)
- [ ] Build succeeds (`npm run build`)
- [ ] All REMOVAL SPEC items removed

**When all tasks complete**: Update plan file from `.todo.md` to `.done.md`
```

### Phase 8: Report to User

Provide concise summary:

```markdown
# Plan Check Complete: [Plan Name]

## Overall Status
**X% Complete** (Y of Z steps done)

## Completed ✅
- Step 1: [description]
- Step 2: [description]

## In Progress ⚠️
- Step 3: [description] (60% done)

## Not Started ❌
- Step 4: [description]

## Critical Issues 🚨
- **REMOVAL SPEC not complete**: Old code still exists
  - `legacy_code` in `file.ts` must be removed
  - `deprecated-helper.ts` must be deleted

## Quality Issues
- `any` type used in `file.ts:42`
- Missing error handling in step 5

## Validation
- ❌ TypeScript: 3 errors
- ✅ Linting: Passed
- Build: Not tested

## Next Steps
1. Remove old code (REMOVAL SPEC)
2. Complete Step 3
3. Fix quality issues
4. Run final validation

**Detailed Report**: `.plans/[plan-name].progress.md`
**Task List**: See remaining work section above
```

## Critical Principles

- **NEVER SKIP FILES** - Check every file in the comprehensive list
- **DO NOT EDIT FILES** - This is read-only audit, not implementation
- **VERIFY REMOVAL SPEC** - Critical that old code is actually removed
- **BE THOROUGH** - Think critically about each file's implementation
- **USE MEMORY** - Store context as you review files
- **RUN VALIDATION** - Always run typecheck and lint
- **BE HONEST** - Mark things as incomplete if they are
- **PROVIDE ACTIONS** - Don't just identify issues, provide todo list
- **CHECK QUALITY** - Implementation exists doesn't mean it's good
- **100% STANDARD** - Plan isn't done until 100% complete and validated

## Completion Criteria

A plan can be marked as `.done.md` ONLY when:

1. ✅ **100% of ORIGINAL ISSUE/TASK requirements implemented** (not just plan steps!)
2. ✅ **All plan steps implemented** (100% completion)
3. ✅ **All REMOVAL SPEC items removed** (old code gone)
4. ✅ **TypeScript passes** (`tsc --noEmit` succeeds)
5. ✅ **Linting passes** (no errors)
6. ✅ **Build succeeds** (if applicable)
7. ✅ **No `any` types added** (strict typing maintained)
8. ✅ **CLAUDE.md compliance** (all guidelines followed)
9. ✅ **Quality verified** (implementations match plan specs)

**CRITICAL**: Criterion #1 is the MOST IMPORTANT. A plan that completes all its steps but doesn't fulfill the original issue requirements is STILL INCOMPLETE.

**Anything less = plan stays as `.todo.md`**

## Supporting Tools

- **Grep**: Search for old code to verify removal
- **Glob**: Find all relevant files
- **Bash**: Run git, typecheck, lint, build
- **Read**: Examine file contents
- **TodoWrite**: Track file review progress
- **Memory/Pinboard**: Store context across files
