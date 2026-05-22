---
name: run-tests
description: Run the test suite and identify new tests needed for recent code changes. Use when verifying changes work correctly or when asked to run tests.
---

# Run Tests

<role>
You are a **QA automation assistant** that runs tests, analyzes coverage gaps, and recommends new tests for recent code changes.
</role>

<purpose>
Run the existing test suite and analyze recent code changes to identify what new tests should be written to maintain coverage.
</purpose>

<when_to_activate>
Activate when the user:
- Says "run tests", "/run-tests", "test", "verify"
- Asks to verify recent changes
- Wants to know what tests are needed for new code
- Asks about test coverage for recent updates

**Trigger phrases:** "run tests", "test", "verify", "check coverage", "what tests"
</when_to_activate>

## Execution Steps

### Step 1: Run Existing Tests

```bash
npm run test
```

Report results:
- Number of tests passed/failed
- Any failing test details
- Test duration

### Step 2: Identify Recent Changes

Check git status and recent commits:

```bash
git diff --name-only HEAD~5
git diff --cached --name-only
git status --porcelain
```

Focus on:
- Modified `.tsx` and `.ts` files in `src/`
- New components or features
- Changes to existing components

### Step 3: Analyze Test Coverage Gaps

For each changed file, determine if tests exist:

| Source File | Test File Location |
|-------------|-------------------|
| `src/components/sections/*.tsx` | `src/tests/design-system/components.test.tsx` |
| `src/components/case-study/*.tsx` | `src/tests/case-study/case-study.test.tsx` |
| `src/components/Blog.tsx` | `src/tests/blog/blog-ux-features.test.tsx` |
| `src/lib/*.ts` | `src/tests/validation/content-validation.test.ts` |
| Navigation changes | `src/tests/navigation/navigation.test.tsx` |
| Mobile-specific | `src/tests/mobile/mobile.test.tsx` |
| Theme/CSS changes | `src/tests/design-system/css-variables.test.ts` |

### Step 4: Recommend New Tests

For each uncovered change, suggest specific tests following the project patterns:

**Test Pattern Template:**
```tsx
import { render, screen } from '@testing-library/react';
import { ThemeProvider } from '../../context/ThemeContext';
import { VariantProvider } from '../../context/VariantContext';
import { profile } from '../../lib/content';

const TestWrapper = ({ children }: { children: React.ReactNode }) => (
    <VariantProvider profile={profile}>
        <ThemeProvider>{children}</ThemeProvider>
    </VariantProvider>
);

describe('[ComponentName]', () => {
    it('should [expected behavior]', () => {
        render(
            <TestWrapper>
                <ComponentName {...props} />
            </TestWrapper>
        );

        expect(/* assertion */).toBe(/* expected */);
    });
});
```

## Output Format

```
## Test Results

**Status**: ✅ All passing | ❌ X failures
**Tests**: X passed, X failed, X total
**Duration**: Xs

### Failures (if any)
- `test name`: error message

---

## Recent Changes Analyzed

| File | Change Type | Has Tests |
|------|-------------|-----------|
| src/components/sections/ExperienceSection.tsx | Modified | ✅ Partial |

---

## Recommended New Tests

### 1. [Test Name]
**File**: `src/tests/[path]/[file].test.tsx`
**Covers**: [what it tests]

```tsx
[test code suggestion]
```

### 2. ...
```

## Test Categories

### Component Tests
- Render without crashing
- Uses CSS variables (not hardcoded colors)
- Correct props handling
- User interactions (clicks, hovers)
- Accessibility attributes

### Integration Tests
- Data flows correctly from content files
- Links render with correct URLs
- Conditional rendering works

### Responsive Tests
- Mobile layout differences
- Tablet breakpoints
- Desktop behavior

## Common Test Assertions

```tsx
// Element exists
expect(screen.getByText('text')).toBeInTheDocument();

// Has attribute
expect(element).toHaveAttribute('href', 'url');

// CSS variable usage
expect(element?.style.color).toContain('var(--color-');

// Link behavior
expect(link).toHaveAttribute('target', '_blank');
expect(link).toHaveAttribute('rel', 'noopener noreferrer');
```

## File Locations

| Purpose | Path |
|---------|------|
| Run tests | `npm run test` |
| Watch mode | `npm run test:watch` |
| Design system only | `npm run test:design-system` |
| Test config | `vitest.config.ts` (if exists) or `vite.config.ts` |
| Test setup | `src/tests/setup.ts` (if exists) |
