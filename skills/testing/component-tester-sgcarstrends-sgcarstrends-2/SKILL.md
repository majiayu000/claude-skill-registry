---
name: component-tester
description: Run Vitest tests for a specific component with coverage. Use when making changes to React components to ensure tests pass and coverage is maintained.
---

# Component Tester Skill

This Skill automatically runs Vitest tests when React components are modified to ensure code quality and test coverage.

## When to Activate

- After creating a new React component
- When modifying existing component implementation
- Before creating a pull request with component changes
- When fixing bugs in components

## Actions Performed

1. **Identify Component**: Determine which component was created or modified
2. **Run Tests**: Execute `pnpm test -- <component-path>` without watch mode
3. **Check Coverage**: Verify test coverage meets project thresholds
4. **Report Results**: Provide clear feedback on:
   - Test pass/fail status
   - Coverage percentages (statements, branches, functions, lines)
   - Specific failing tests with error messages
   - Coverage gaps requiring additional tests

## Example Usage

```typescript
// User modifies: src/app/blog/_components/progress-bar.tsx
// Skill automatically runs:
// pnpm test -- src/app/blog/_components/progress-bar

// Output:
// ✓ should render progress bar with correct width
// ✓ should update progress on scroll
// ✓ should hide when not scrolled
// Coverage: 95% statements, 90% branches, 100% functions, 95% lines
```

## Tools Used

- **Read**: Examine component files and test files
- **Grep**: Locate related test files
- **Bash**: Execute `pnpm test` commands

## Test Naming Convention

All tests should follow the "should" convention:
- ✅ "should render title and children"
- ✅ "should display empty state when data is empty"
- ❌ "renders title and children"

## Coverage Thresholds

Flag components with coverage below:
- Statements: 80%
- Branches: 75%
- Functions: 80%
- Lines: 80%

## Related Files

- Test location: `__tests__/` directories next to components
- Test suffix: `.test.ts` or `.test.tsx`
- Configuration: `vitest.config.ts` in project root
