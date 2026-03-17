---
skill: add-feature
description: Add new feature with full validation: $ARGUMENTS (feature name)
location: project
---

# Add New Feature: $ARGUMENTS

I'll create a complete new feature for the expense tracker app: **$ARGUMENTS**

This comprehensive workflow includes:
1. Creating an isolated git worktree for safety
2. Generating all necessary files (component, types, tests, styles)
3. Integrating the feature into the main application
4. Running full validation suite (build, lint, unit tests, e2e tests)
5. Categorizing any errors with specific remediation steps
6. Reporting results and prompting for merge decision

Let's begin!

---

## Process Steps

### 1. Create Isolated Git Worktree

First, I'll create an isolated worktree to keep the main workspace clean:

```bash
# Generate unique timestamp for worktree isolation
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
FEATURE_NAME="$ARGUMENTS"
WORKTREE_PATH="../add-feature-$FEATURE_NAME-worktree-$TIMESTAMP"
BRANCH_NAME="feature-$FEATURE_NAME-$TIMESTAMP"

echo "Creating isolated worktree for feature: $FEATURE_NAME"
echo "Worktree path: $WORKTREE_PATH"
echo "Branch name: $BRANCH_NAME"

# Create the worktree
git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"

# Navigate into the worktree
cd "$WORKTREE_PATH/expense-tracker-ai"

echo "✅ Worktree created successfully"
echo "📁 Working in: $(pwd)"
```

**Why worktree isolation?**
- Keeps main workspace untouched during development
- Allows safe experimentation
- Easy to discard if something goes wrong
- Can review changes before merging
- Prevents disrupting ongoing work

### 2. Plan Feature Structure

Analyze the feature name and determine what files to create:

```bash
echo "Planning feature structure for: $FEATURE_NAME"

# Convert feature name to different case formats
COMPONENT_NAME=$(echo "$FEATURE_NAME" | sed -E 's/(^|-)([a-z])/\U\2/g')  # PascalCase
FILE_NAME=$(echo "$FEATURE_NAME" | tr '[:upper:]' '[:lower:]')           # lowercase

echo ""
echo "Files to create:"
echo "  1. components/$COMPONENT_NAME.tsx (main component)"
echo "  2. components/$COMPONENT_NAME.test.tsx (unit tests)"
echo "  3. tests/e2e/$FILE_NAME.spec.ts (e2e tests)"
echo "  4. types/index.ts (add new types if needed)"
echo ""
```

### 3. Create Component File

Generate the main React component:

```typescript
// components/$COMPONENT_NAME.tsx

'use client';

import { useState } from 'react';

interface ${COMPONENT_NAME}Props {
  // Define props based on feature requirements
}

export default function $COMPONENT_NAME({}: ${COMPONENT_NAME}Props) {
  const [state, setState] = useState();

  return (
    <div data-testid="${FILE_NAME}" className="p-4">
      <h2 className="text-xl font-semibold mb-4">
        $FEATURE_NAME
      </h2>

      {/* Feature content */}
      <div className="space-y-4">
        {/* Add feature-specific elements */}
      </div>
    </div>
  );
}
```

**Component structure follows project patterns:**
- `'use client'` directive (all components are client-side)
- TypeScript with explicit props interface
- Descriptive `data-testid` for testing
- Tailwind CSS for styling
- Responsive design considerations

### 4. Add TypeScript Types

If the feature requires new types, add them to `types/index.ts`:

```typescript
// Add to types/index.ts

// Types for $FEATURE_NAME feature
export interface ${COMPONENT_NAME}Data {
  id: string;
  // Add feature-specific fields
}

export interface ${COMPONENT_NAME}Props {
  // Add props definition
  onUpdate?: (data: ${COMPONENT_NAME}Data) => void;
  onDelete?: (id: string) => void;
}
```

**Type conventions:**
- Use descriptive names (suffix with Data, Props, Options)
- Export all types for reusability
- Include JSDoc comments for complex types
- Follow existing patterns in types/index.ts

### 5. Create Unit Tests

Generate comprehensive unit tests:

```typescript
// components/$COMPONENT_NAME.test.tsx

import { render, screen, fireEvent } from '@testing-library/react';
import $COMPONENT_NAME from './$COMPONENT_NAME';

describe('$COMPONENT_NAME', () => {
  // Happy path tests
  test('should render correctly', () => {
    render(<$COMPONENT_NAME />);
    expect(screen.getByTestId('${FILE_NAME}')).toBeInTheDocument();
  });

  test('should display feature heading', () => {
    render(<$COMPONENT_NAME />);
    expect(screen.getByText('$FEATURE_NAME')).toBeInTheDocument();
  });

  // Interaction tests
  test('should handle user interaction', () => {
    const mockHandler = jest.fn();
    render(<$COMPONENT_NAME onUpdate={mockHandler} />);

    // Simulate user interaction
    const button = screen.getByRole('button');
    fireEvent.click(button);

    // Verify handler called
    expect(mockHandler).toHaveBeenCalled();
  });

  // Edge cases
  test('should handle empty state', () => {
    render(<$COMPONENT_NAME />);
    // Test behavior with no data
  });

  test('should handle error state', () => {
    render(<$COMPONENT_NAME />);
    // Test error scenarios
  });

  // Accessibility
  test('should be keyboard navigable', () => {
    render(<$COMPONENT_NAME />);
    // Test keyboard navigation
  });
});
```

**Test coverage requirements:**
- Happy path scenarios (basic functionality)
- User interactions (clicks, inputs, selections)
- Edge cases (empty, null, boundary conditions)
- Error states (validation failures, API errors)
- Accessibility (keyboard nav, screen readers)

### 6. Create E2E Tests

Generate Playwright end-to-end tests:

```typescript
// tests/e2e/$FILE_NAME.spec.ts

import { test, expect } from '@playwright/test';

test.describe('$FEATURE_NAME', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the application
    await page.goto('/');

    // Clear localStorage to start fresh
    await page.evaluate(() => localStorage.clear());
    await page.reload();
  });

  test('should display $FEATURE_NAME feature', async ({ page }) => {
    // Locate the feature
    const feature = page.locator('[data-testid="${FILE_NAME}"]');
    await expect(feature).toBeVisible();
  });

  test('should handle user workflow', async ({ page }) => {
    // Test complete user workflow for this feature
    // Example: Fill form → Submit → Verify result

    await page.locator('[data-testid="${FILE_NAME}-input"]').fill('test data');
    await page.locator('[data-testid="${FILE_NAME}-submit"]').click();
    await expect(page.locator('[data-testid="${FILE_NAME}-result"]')).toBeVisible();
  });

  test('should validate inputs', async ({ page }) => {
    // Test input validation
    await page.locator('[data-testid="${FILE_NAME}-submit"]').click();
    await expect(page.locator('[data-testid="${FILE_NAME}-error"]')).toBeVisible();
  });

  test('should persist data', async ({ page }) => {
    // Test localStorage persistence if applicable
    await page.locator('[data-testid="${FILE_NAME}-input"]').fill('test data');
    await page.locator('[data-testid="${FILE_NAME}-submit"]').click();

    // Reload page
    await page.reload();

    // Verify data persisted
    await expect(page.locator('[data-testid="${FILE_NAME}-result"]')).toContainText('test data');
  });
});
```

**E2E test patterns:**
- Use `data-testid` for stable selectors
- Clear localStorage before each test
- Test complete user workflows
- Verify data persistence
- Test error states and validation

### 7. Integrate Feature into Main App

Add the feature to the main application:

```typescript
// Update app/page.tsx

// 1. Import the new component
import $COMPONENT_NAME from '@/components/$COMPONENT_NAME';

// 2. Add to component
export default function Home() {
  return (
    <div>
      {/* Existing content */}

      {/* Add new feature */}
      <$COMPONENT_NAME />
    </div>
  );
}
```

**Integration considerations:**
- Add to appropriate tab if using tab navigation
- Pass necessary props from parent state
- Wire up event handlers
- Ensure styling is consistent
- Consider responsive layout

### 8. Run Build Validation

Compile the application to catch syntax and type errors:

```bash
echo "1/4 Running build validation..."

npm run build

if [ $? -ne 0 ]; then
  echo "❌ Build failed"
  echo ""
  echo "Common build errors:"
  echo "  - TypeScript type errors"
  echo "  - Import path issues"
  echo "  - Missing dependencies"
  echo ""
  echo "Fix errors and run: npm run build"
  exit 1
else
  echo "✅ Build passed"
fi
```

**Build errors indicate:**
- Type errors (incorrect types, missing types)
- Import issues (wrong paths, missing exports)
- Syntax errors (invalid TypeScript/JSX)
- Missing dependencies

### 9. Run Lint Validation

Check code quality and style:

```bash
echo "2/4 Running lint validation..."

npm run lint

if [ $? -ne 0 ]; then
  echo "❌ Lint failed"
  echo ""
  echo "Try auto-fix: npm run lint -- --fix"
  echo ""
  echo "Common lint issues:"
  echo "  - Unused variables"
  echo "  - Missing return types"
  echo "  - Inconsistent formatting"
  exit 1
else
  echo "✅ Lint passed"
fi
```

**Lint warnings categories:**
- Code quality (unused vars, any types)
- Style issues (formatting, spacing)
- Best practices (React hooks rules)
- Potential bugs (missing dependencies)

### 10. Run Unit Tests

Execute Jest unit tests:

```bash
echo "3/4 Running unit tests..."

npm test

if [ $? -ne 0 ]; then
  echo "❌ Unit tests failed"
  echo ""
  echo "Debug options:"
  echo "  - Watch mode: npm run test:watch"
  echo "  - Verbose: npm test -- --verbose"
  echo "  - Single file: npm test -- $COMPONENT_NAME"
  exit 1
else
  echo "✅ Unit tests passed"
fi
```

**Test failure types:**
- Assertion failures (expected vs actual)
- Import/module errors
- Mock issues
- Type errors in tests

### 11. Run E2E Tests

Execute Playwright end-to-end tests:

```bash
echo "4/4 Running e2e tests..."

npm run test:e2e

if [ $? -ne 0 ]; then
  echo "❌ E2E tests failed"
  echo ""
  echo "Debug options:"
  echo "  - UI mode: npm run test:e2e:ui"
  echo "  - Headed: npm run test:e2e -- --headed"
  echo "  - Debug: npm run test:e2e:debug"
  exit 1
else
  echo "✅ E2E tests passed"
fi
```

**E2E failure causes:**
- Selector issues (element not found)
- Timing issues (element not ready)
- Application errors (feature broken)
- Test logic errors (wrong assertions)

### 12. Categorize Errors (If Any)

If validation fails, categorize errors by type:

```markdown
## Error Report

### 🔴 Build Errors (2)

```
Error: Type 'string' is not assignable to type 'number'
  → components/$COMPONENT_NAME.tsx:42

Error: Cannot find module '@/types'
  → components/$COMPONENT_NAME.tsx:1
```

**Resolution:**
1. Fix type mismatch in $COMPONENT_NAME.tsx:42
2. Verify import path: should be '@/types' or './types'

---

### 🟠 Lint Warnings (3)

```
Warning: 'handleClick' is defined but never used
  → components/$COMPONENT_NAME.tsx:15

Warning: Unexpected any type
  → components/$COMPONENT_NAME.tsx:23
```

**Resolution:**
1. Remove unused variables or implement handlers
2. Replace `any` with proper types
3. Run `npm run lint -- --fix` for auto-fixes

---

### 🔴 Test Failures (1)

```
FAILED components/$COMPONENT_NAME.test.tsx
  ✗ should handle user interaction
    Expected mock function to have been called once
    Received: 0 calls
```

**Resolution:**
1. Verify event handler is wired up correctly
2. Check test selector is finding the right element
3. Run in watch mode: `npm run test:watch -- $COMPONENT_NAME`

---

### 🔴 E2E Test Failures (1)

```
FAILED tests/e2e/$FILE_NAME.spec.ts
  ✗ should display feature
    Timeout waiting for element
```

**Resolution:**
1. Verify component is actually rendered in app
2. Check data-testid matches test selector
3. Run in UI mode: `npm run test:e2e:ui`
```

### 13. Generate Success Report

If all validations pass, create a comprehensive report:

```
✅ Feature Addition Complete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Summary:
- Feature name: $FEATURE_NAME
- Component: $COMPONENT_NAME
- Files created: 4
- Files modified: 2

📝 Files Created:
✓ components/$COMPONENT_NAME.tsx (main component, 120 lines)
✓ components/$COMPONENT_NAME.test.tsx (unit tests, 45 lines)
✓ tests/e2e/$FILE_NAME.spec.ts (e2e tests, 35 lines)

📝 Files Modified:
✓ app/page.tsx (integrated component, +8 lines)
✓ types/index.ts (added types, +15 lines)

✅ Validation Results:
✓ Build: Passed (0 errors, 0 warnings)
✓ Lint: Passed (0 errors, 0 warnings)
✓ Unit Tests: Passed (8/8 tests)
✓ E2E Tests: Passed (4/4 tests)

📊 Test Coverage:
- Happy path scenarios: 3 tests
- User interactions: 2 tests
- Edge cases: 2 tests
- Accessibility: 1 test

📁 Worktree Location:
$WORKTREE_PATH

🎯 Next Steps:
Review the feature in the worktree before merging.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 14. Prompt for Merge Decision

Ask the user what to do next:

```
✅ All validations passed successfully.

Would you like to merge this feature back to main? (yes/no)

Options:

  yes - Merge feature to main branch and clean up worktree
        • Merges branch: $BRANCH_NAME → main
        • Removes worktree: $WORKTREE_PATH
        • Deletes branch: $BRANCH_NAME
        • Ready for: git push origin main

  no  - Keep worktree for manual review
        • Worktree preserved at: $WORKTREE_PATH
        • Branch available: $BRANCH_NAME
        • You can merge manually later

What would you like to do?
```

### 15. Handle Merge (If Yes)

If user chooses to merge:

```bash
echo "Merging feature to main branch..."

# Navigate back to original repo
cd /Users/greg/code/claude-code-coursera

# Merge the feature branch
git merge "$BRANCH_NAME"

if [ $? -ne 0 ]; then
  echo "❌ Merge conflict detected"
  echo ""
  echo "Resolve conflicts manually:"
  echo "  1. git status (see conflicts)"
  echo "  2. Edit conflicting files"
  echo "  3. git add <files>"
  echo "  4. git merge --continue"
  exit 1
fi

echo "✅ Merge successful"

# Push to remote (if applicable)
echo ""
echo "Push to remote? (yes/no)"
# Wait for response

# Clean up worktree
git worktree remove "$WORKTREE_PATH"
git branch -d "$BRANCH_NAME"

echo "✅ Feature merged and worktree cleaned up"
```

### 16. Handle Keep for Review (If No)

If user chooses to keep for review:

```bash
echo "Worktree preserved for review"
echo ""
echo "📁 Location: $WORKTREE_PATH"
echo "🌿 Branch: $BRANCH_NAME"
echo ""
echo "To review the feature:"
echo "  cd $WORKTREE_PATH/expense-tracker-ai"
echo "  npm run dev"
echo ""
echo "To merge manually later:"
echo "  cd /Users/greg/code/claude-code-coursera"
echo "  git merge $BRANCH_NAME"
echo "  git push origin main"
echo ""
echo "To clean up when done:"
echo "  git worktree remove $WORKTREE_PATH"
echo "  git branch -d $BRANCH_NAME"
```

---

## Success Criteria Checklist

Before prompting for merge, verify:

- [x] Worktree created and isolated (main branch unchanged)
- [x] All feature files created:
  - [x] Main component file
  - [x] Unit test file
  - [x] E2E test file
  - [x] Types added (if needed)
- [x] Feature integrated into app
- [x] Full validation suite passed:
  - [x] `npm run build` ✓
  - [x] `npm run lint` ✓
  - [x] `npm test` ✓
  - [x] `npm run test:e2e` ✓
- [x] Clear success/failure report generated
- [x] User prompted for merge decision

---

## Example Usage

### Adding a Budget Tracker Feature

```bash
add-feature budget-tracker
```

**Expected workflow:**

```
Creating isolated worktree for feature: budget-tracker
✅ Worktree created successfully

Planning feature structure for: budget-tracker
Files to create:
  1. components/BudgetTracker.tsx
  2. components/BudgetTracker.test.tsx
  3. tests/e2e/budget-tracker.spec.ts

✓ Created components/BudgetTracker.tsx
✓ Created components/BudgetTracker.test.tsx
✓ Created tests/e2e/budget-tracker.spec.ts
✓ Updated app/page.tsx
✓ Updated types/index.ts

Running validation suite...
1/4 Build... ✅ Passed
2/4 Lint... ✅ Passed
3/4 Unit tests... ✅ Passed (12/12)
4/4 E2E tests... ✅ Passed (4/4)

✅ Feature Addition Complete

Would you like to merge this feature back to main? (yes/no)
```

### Adding a Category Manager Feature

```bash
add-feature category-manager
```

**With validation errors:**

```
Creating isolated worktree for feature: category-manager
✅ Worktree created successfully

✓ Created all files
✓ Integrated into app

Running validation suite...
1/4 Build... ✅ Passed
2/4 Lint... ❌ Failed

🟠 Lint Warnings (2)
  - Unused variable 'categories' at CategoryManager.tsx:15
  - Missing return type at CategoryManager.tsx:42

Fix errors? (yes/no)
```

---

## Troubleshooting

### Worktree Creation Fails

**Error:** `fatal: could not create work tree dir`

**Solution:**
```bash
# Ensure parent directory exists
mkdir -p "$(dirname "$WORKTREE_PATH")"

# Verify no naming conflicts
ls -la ../add-feature-*
```

### Build Fails: Module Not Found

**Error:** `Cannot find module '@/components/FeatureName'`

**Solution:**
- Verify file was created: `ls components/FeatureName.tsx`
- Check import path uses `@/` alias (configured in tsconfig.json)
- Restart dev server if running

### Tests Fail: Component Not Found

**Error:** `Unable to find element with data-testid="feature-name"`

**Solution:**
- Verify `data-testid` in component matches test
- Ensure component is properly exported
- Check component is actually rendered

### E2E Tests Timeout

**Error:** `Timeout 30000ms exceeded`

**Solution:**
```bash
# Run in headed mode to see what's happening
npm run test:e2e -- --headed

# Increase timeout in test
test('...', async ({ page }) => {
  test.setTimeout(60000); // 60 seconds
});
```

---

## Advanced: Custom Feature Templates

For specific feature types, customize the templates:

### Form-Based Features

When adding a form feature:
- Include validation logic
- Add error state handling
- Implement form submission
- Add success/error messages

### Data Display Features

When adding a display feature:
- Include loading states
- Add empty state handling
- Implement data filtering
- Add sort functionality

### Interactive Features

When adding interactive features:
- Include state management
- Add user feedback (toasts, modals)
- Implement undo/redo if applicable
- Add keyboard shortcuts

---

## Related Documentation

- **Project Patterns:** [CLAUDE.md](../../CLAUDE.md)
- **Testing Guide:** [expense-tracker-ai/docs/dev/testing-guide.md](../../expense-tracker-ai/docs/dev/testing-guide.md)
- **Component Examples:** [expense-tracker-ai/components/](../../expense-tracker-ai/components/)
- **E2E Test Examples:** [expense-tracker-ai/tests/e2e/](../../expense-tracker-ai/tests/e2e/)
- **Skills Guide:** [skills.md](../../skills.md)
