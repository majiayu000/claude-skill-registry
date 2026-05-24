---
name: pr-ready
description: Prepare code for a PR by checking for cleanliness, removing debug statements, ensuring DRY principles, checking React component structure, and identifying prop drilling issues.
argument-hint: [file-or-directory]
disable-model-invocation: true
---

Prepare the code for a pull request by performing a comprehensive cleanup and quality check.

## Scope

If `$ARGUMENTS` is provided, focus on that file or directory. Otherwise, use `git diff --name-only $(git merge-base HEAD main)...HEAD` to get the list of changed files on the current branch.

## Step 1: Identify Files to Review

1. If a specific path was provided, use that
2. Otherwise, get all changed files on the current branch compared to main
3. Filter to only include source files (`.ts`, `.tsx`, `.js`, `.jsx`)

## Step 2: Debug Statement Check

Search for and report any debug statements that should be removed:

- `console.log` statements (except those in legitimate logging utilities)
- `console.debug`, `console.info`, `console.warn`, `console.error` (evaluate if intentional)
- `debugger` statements
- Commented-out `console.*` statements
- `TODO` or `FIXME` comments that should be addressed before PR

For each finding, report:
- File path and line number
- The offending code
- Recommendation (remove, keep, or convert to proper logging)

## Step 3: DRY (Don't Repeat Yourself) Analysis

Look for code duplication:

1. **Repeated logic patterns**: Similar code blocks appearing in multiple places
2. **Copy-pasted functions**: Functions with minor variations that could be parameterized
3. **Repeated JSX structures**: Similar UI patterns that could be extracted into components
4. **Duplicate type definitions**: Types or interfaces defined multiple times
5. **Repeated utility code**: String manipulation, date formatting, etc. that could be centralized

For each duplication found:
- List all locations where the pattern appears
- Suggest a refactoring approach (extract to utility, create shared component, etc.)
- Estimate the code reduction

## Step 4: React Component Structure Review

For each React component, check:

### Component Size
- Components should be under 150 lines
- If larger, identify logical boundaries for splitting

### Single Responsibility
- Each component should have one clear purpose
- Flag components that do too many things

### Component Splitting Opportunities
- Large render methods that could be broken into smaller components
- Repeated JSX patterns within a component
- Complex conditional rendering that could be extracted

### Hooks Organization
- Business logic should be in custom hooks, not inline
- Related state should be grouped into custom hooks
- Effects should be organized and commented if complex

## Step 5: Prop Drilling Detection

Identify prop drilling issues where props are passed through multiple component layers:

1. **Direct prop drilling**: Props passed through 3+ component levels without being used
2. **Context candidates**: Data that's needed by many components and should use React Context
3. **State lifting issues**: State that's lifted too high and causes unnecessary re-renders

For each prop drilling issue:
- Show the prop's journey through components
- Recommend a solution:
  - Use React Context
  - Use composition (children pattern)
  - Co-locate state closer to where it's used
  - Use a state management solution

## Step 6: Additional Quality Checks

- **Unused imports**: Imports that aren't being used
- **Unused variables**: Variables declared but never referenced
- **Dead code**: Functions or components that are never called
- **Commented-out code**: Old code that should be deleted, not commented
- **Inconsistent naming**: Variables or functions that don't follow project conventions
- **Missing TypeScript types**: Any `any` types or missing type annotations

## Output Format

```
## PR Readiness Report

### Files Analyzed
- [list of files]

### Critical Issues (Must Fix Before PR)

#### Debug Statements
| File | Line | Code | Action |
|------|------|------|--------|
| ... | ... | ... | ... |

#### Dead Code & Unused Imports
| File | Line | Issue |
|------|------|-------|
| ... | ... | ... |

### Code Quality Issues

#### DRY Violations
1. **[Pattern Name]**
   - Found in: `file1.tsx:10`, `file2.tsx:25`, `file3.tsx:40`
   - Suggestion: [refactoring approach]

#### Component Structure Issues
1. **[Component Name]** (`path/to/component.tsx`)
   - Issue: [description]
   - Recommendation: [how to fix]

#### Prop Drilling Issues
1. **[Prop Name]**
   - Path: `ParentComponent` → `MiddleComponent` → `ChildComponent`
   - Recommendation: [solution]

### Summary
- Total issues found: X
- Critical (must fix): Y
- Warnings: Z
- Suggestions: W

### Recommended Actions
1. [First action to take]
2. [Second action to take]
...
```

## Step 7: Offer to Fix

After presenting the report, ask the user if they want you to:
1. Fix all critical issues automatically
2. Fix specific issues (let them choose)
3. Just report without making changes

If they want fixes applied:
- Remove debug statements
- Remove unused imports and dead code
- Extract duplicated code into utilities or components
- Split large components
- Add React Context where prop drilling is detected
