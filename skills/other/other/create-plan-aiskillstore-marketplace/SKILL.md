---
name: create-plan
description: Create comprehensive implementation plan in .plans directory based on analysis or report. Use when user asks to create a plan, plan implementation, design a solution, or structure work for a feature/refactor/fix.
---

# Create Implementation Plan

## Instructions

Create a detailed, high-quality implementation plan in `.plans/` directory that adheres to strict quality standards and provides complete guidance for implementation.

### Phase 1: Understanding & Validation

#### Step 0: Extract Original Issue/Task Requirements (MANDATORY)

**CRITICAL**: Before creating any plan, extract ALL requirements from the original issue/task.

```bash
# If triggered by a GitHub issue
gh issue view <number>
```

Create exhaustive requirements list:
- Every functional requirement stated
- Every acceptance criterion listed
- Every edge case mentioned
- Every error handling requirement
- Any implicit requirements (derive from context)

**Store this list - the plan MUST cover 100% of these requirements.**

#### Step 1: Understand the Request
- Review the report or analysis that triggered this plan
- **Map each requirement from Step 0 to plan items**
- Identify the type of plan needed:
  - **Feature**: New functionality
  - **Refactor**: Code restructuring
  - **Fix**: Bug fix or issue resolution
  - **Enhancement**: Improvement to existing feature

#### Step 2: Audit the Codebase
**CRITICAL**: Never create a plan without thorough codebase understanding

For each item in the report, perform comprehensive analysis:
1. **Use the audit skill** if needed for deep investigation
2. **Identify affected files** - Which files will change?
3. **Find existing patterns** - How is similar code structured?
4. **Check CLAUDE.md files** - What are the rules for this area?
5. **Analyze types** - What existing types can be reused?
6. **Identify dependencies** - What depends on what we're changing?
7. **Find naming patterns** - How should new files be named?

**DO NOT SKIP THIS STEP** - Rushed plans lead to bad implementations

#### Step 3: CLAUDE.md Compliance Check
Read ALL relevant `CLAUDE.md` files in:
- Project root
- Affected directories
- Related modules

Extract requirements:
- Naming conventions
- Architecture patterns
- Type requirements
- File organization rules
- Code style standards

### Phase 2: Plan Structure & Naming

#### Step 1: Choose Plan Name
Format: `[descriptive-name].todo.md`

Rules:
- Use kebab-case
- Be specific and descriptive
- Reflect actual work (not vague like "improvements")
- Examples:
  - `implement-user-authentication.todo.md` ✅
  - `refactor-database-layer.todo.md` ✅
  - `new-features.todo.md` ❌ (too vague)

#### Step 2: Determine File Names for Implementation

**CRITICAL RULES**:
- ❌ NEVER create migration files like `foo_v2.ts`, `foo-new.ts`, `foo-enhanced.ts`
- ❌ NEVER use temporary naming like `simple-*.ts`, `temp-*.ts`
- ✅ ALWAYS use proper, final names from the start
- ✅ ALWAYS follow existing naming patterns in the directory
- ✅ ALWAYS check CLAUDE.md for naming requirements

**Process**:
1. Identify existing file naming patterns
2. Check CLAUDE.md for conventions
3. Choose names that fit the pattern
4. If unsure, analyze similar existing files
5. Plan to replace existing files directly (not create duplicates)

### Phase 3: Plan Content - Required Sections

Create plan document with ALL of the following sections:

#### 1. Overview & Issue Coverage
```markdown
# [Plan Title]

## Summary
[2-3 sentences explaining what and why]

## Type
[Feature | Refactor | Fix | Enhancement]

## Source Issue/Task
[Link to GitHub issue or task description]

## Original Requirements (100% Coverage Required)

**ALL requirements from source issue/task that this plan MUST address:**

| # | Requirement | Plan Step(s) |
|---|-------------|--------------|
| 1 | [Requirement from issue] | Step X |
| 2 | [Requirement from issue] | Step Y, Z |
| 3 | [Requirement from issue] | Step W |

**Coverage Check**: X of X requirements mapped to plan steps (must be 100%)

## Status
Todo (will be renamed to .done.md when complete)
```

#### 2. Context & Motivation
```markdown
## Context
[Why is this needed? What problem does it solve?]

## Current State
[What exists now? What are the limitations?]

## Desired State
[What will exist after? What improvements will we gain?]
```

#### 3. CLAUDE.md Compliance
```markdown
## CLAUDE.md Requirements

### Naming Conventions
- [List relevant naming rules from CLAUDE.md]

### Architecture Requirements
- [List relevant architectural rules]

### Type Requirements
- [List type-related rules]

### Other Guidelines
- [Any other relevant rules]
```

#### 4. Existing Types Analysis
```markdown
## Existing Types

### Types to Reuse
- `TypeName` from `path/to/file.ts` - [what it represents]
- [List ALL types that can be reused]

### Types to Create
- `NewTypeName` - [what it will represent, why needed]
- [Only create if NO existing type works]

### Type Guidelines
- ❌ NEVER use `any`
- ❌ NEVER use `unknown` (unless absolutely necessary with justification)
- ✅ ALWAYS prefer existing types
- ✅ ALWAYS use strict typing
```

#### 5. Impact Analysis
```markdown
## Impact Analysis

### Files to Modify
- `path/to/file1.ts` - [what changes, why]
- `path/to/file2.ts` - [what changes, why]

### Files to Create
- `path/to/newfile.ts` - [purpose, why not existing file]

### Files to Delete
- `path/to/oldfile.ts` - [why removing, what replaces it]

### Dependencies Affected
- [List what depends on changed code]
- [How will dependencies be updated?]

### Breaking Changes
- [List any breaking changes]
- [How will they be handled?]
```

#### 6. Implementation Steps
```markdown
## Implementation Steps

Each step should be:
- Specific and actionable
- Single responsibility
- Ordered correctly (dependencies first)

### Step 1: [Descriptive Title]
**File**: `path/to/file.ts`
**Action**: [What to do]
**Why**: [Why this step]
**Details**:
- [Specific implementation detail]
- [Another detail]

### Step 2: [Next Step]
[Same structure]

[Continue for all steps]
```

#### 7. REMOVAL SPECIFICATION ⚠️
```markdown
## REMOVAL SPECIFICATION

**CRITICAL**: This section tracks OLD code that must be REMOVED.

### Code to Remove

#### From `path/to/file1.ts`
- **Lines X-Y**: `function oldFunction() {...}`
  - **Why removing**: Replaced by newFunction
  - **Replacement**: Step 3 in implementation
  - **Dependencies**: Used by A, B, C (all updated in steps 5, 6, 7)

#### File to Delete: `path/to/old-file.ts`
- **Why removing**: Functionality moved to new-file.ts
- **Replacement**: Step 2 creates replacement
- **Dependencies**: Imported by X, Y, Z (all updated in steps 8, 9, 10)

### Removal Checklist
- [ ] All deprecated functions removed
- [ ] All old files deleted
- [ ] All imports updated
- [ ] All references updated
- [ ] No dead code remains

**VERIFICATION**: At completion, grep for old symbols to ensure complete removal.
```

#### 8. Anti-Patterns to Avoid
```markdown
## Anti-Patterns to Avoid

❌ **NEVER** include:
- Migration mechanisms (gradual rollout, feature flags for this)
- Fallback mechanisms (keeping old code "just in case")
- Risk mitigation (running old and new in parallel)
- Backward compatibility layers (unless external API)
- Temporary bridges between old and new

✅ **ALWAYS** instead:
- Replace completely and cleanly
- Make all necessary changes at once
- Remove old code immediately
- Trust the plan and execute fully

**Why**: Half-migrations leave bad code in the codebase forever.
```

#### 9. Validation Criteria
```markdown
## Validation Criteria

### Pre-Implementation Checklist
- [ ] All CLAUDE.md files reviewed
- [ ] All existing types identified
- [ ] All affected files identified
- [ ] All naming follows patterns
- [ ] Impact fully analyzed

### Post-Implementation Checklist
- [ ] All steps completed
- [ ] All old code removed (per REMOVAL SPEC)
- [ ] TypeScript compiles (`tsc --noEmit`)
- [ ] Linting passes (`npm run lint`)
- [ ] Tests pass (if applicable)
- [ ] No `any` or `unknown` types added
- [ ] CLAUDE.md compliance verified
- [ ] Single responsibility maintained
```

### Phase 4: Plan Creation & Validation

#### Step 1: Write the Plan
- Create file in `.plans/` directory
- Use `.todo.md` extension
- Include ALL required sections above
- Be thorough - never skip items

#### Step 2: Validate Plan Completeness
Checklist:
- [ ] **100% of original issue/task requirements mapped to plan steps**
- [ ] Overview section complete with requirements table
- [ ] Context & motivation clear
- [ ] CLAUDE.md compliance documented
- [ ] Existing types analyzed
- [ ] Impact analysis thorough
- [ ] Implementation steps detailed and ordered
- [ ] **Every requirement from issue appears in at least one step**
- [ ] REMOVAL SPECIFICATION complete
- [ ] Anti-patterns section included
- [ ] Validation criteria defined
- [ ] No migration/fallback mechanisms
- [ ] No temporary file names
- [ ] No `any` or `unknown` types planned

#### Step 3: Review Against Guidelines
Double-check:
- ✅ Follows naming conventions from CLAUDE.md
- ✅ Uses existing types where possible
- ✅ Single responsibility maintained
- ✅ Complete removal spec included
- ✅ No migration code planned
- ✅ All steps are specific and actionable
- ✅ No items skipped or rushed

#### Step 4: Final Audit Recommendation
Before finalizing, consider:
- Should specific areas be audited more deeply?
- Are there unknowns that need investigation?
- Is more context needed before implementation?

If yes, recommend using the audit skill for those areas.

### Phase 5: Report to User

Provide summary:
```markdown
# Plan Created: [plan-name]

## Location
`.plans/[plan-name].todo.md`

## Summary
[Brief description of what the plan covers]

## Key Points
- [Important aspect 1]
- [Important aspect 2]
- [Important aspect 3]

## Files Affected
- X files to modify
- Y files to create
- Z files to delete

## REMOVAL SPEC
- [Summary of what will be removed]

## Ready to Implement
The plan is complete and ready for implementation. All required sections are included, CLAUDE.md compliance is verified, and the removal specification is thorough.

## Next Steps
Review the plan and begin implementation when ready.
```

## Critical Principles

- **100% ISSUE COVERAGE** - Plan MUST address every requirement from original issue
- **NEVER RUSH** - Thorough planning prevents bad implementations
- **NEVER SKIP AUDIT** - Always understand the codebase first
- **NEVER CREATE MIGRATIONS** - Replace completely, not gradually
- **NEVER USE TEMPORARY NAMES** - Use final, proper names from the start
- **NEVER SKIP REMOVAL SPEC** - Track what must be deleted
- **NEVER SKIP REQUIREMENT** - Every issue requirement MUST have a plan step
- **ALWAYS USE EXISTING TYPES** - Create new types only when necessary
- **ALWAYS FOLLOW CLAUDE.MD** - Read and apply all guidelines
- **ALWAYS BE SPECIFIC** - Vague steps lead to bad implementations
- **ALWAYS THINK HOLISTICALLY** - Consider full impact of changes
- **COMPLETENESS OVER SPEED** - A complete plan prevents future problems

## Templates

See `templates/` directory for:
- `feature-plan-template.md` - Template for new features
- `refactor-plan-template.md` - Template for refactoring
- `fix-plan-template.md` - Template for bug fixes
