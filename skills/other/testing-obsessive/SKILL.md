---
name: testing-obsessive
description: This skill should be used when the user mentions "write tests", "test coverage", "testing strategy", "unit tests", "integration tests", "e2e tests", "vitest", "jest", discusses testing approaches, asks about test patterns, or works on test files. Addresses testing fundamentals with emphasis on Vitest and Svelte component testing using pragmatic, risk-based approaches.
version: 1.0.0
---

# Testing Foundations

Comprehensive testing guidance for JavaScript/TypeScript applications, with emphasis on Vitest, Svelte component testing, and pragmatic test-after development. Addresses testing as a professional skill for portfolio evidence and code quality.

---

## When This Skill Applies

Use this skill when:
- Writing new tests for features or components
- Setting up testing infrastructure
- Debugging failing tests
- Discussing testing strategies or coverage goals
- Refactoring tests for better maintainability
- Questions about testing best practices
- Deciding what to test and when

---

## Testing Philosophy

### Why Test?

**Not for 100% coverage** - Test for:
1. **Confidence** - Deploy without fear
2. **Documentation** - Tests show how code should be used
3. **Refactoring safety** - Change implementation without breaking behaviour
4. **Regression prevention** - Bugs stay fixed
5. **Design feedback** - Hard-to-test code often signals design issues

### The Testing Pyramid
```
       /\
      /  \     E2E Tests
     /    \    (Few, slow, expensive)
    /------\
   /        \  Integration Tests
  /          \ (Some, medium speed)
 /------------\
/              \ Unit Tests
----------------  (Many, fast, cheap)
```

**Distribution target**:
- **70%** Unit tests - Fast, isolated, test single functions/modules
- **20%** Integration tests - Test component interactions, API calls
- **10%** E2E tests - Test critical user journeys

### Pragmatic Approach

**Test-after development workflow**:
1. Implement working feature
2. Manual verification
3. Assess risk (see Risk-Based Testing)
4. Write automated tests for high/medium risk code
5. Refactor with test safety net

This approach:
- Lets you prototype quickly
- Tests based on real implementation
- Focuses effort where it matters
- Builds confidence incrementally

---

## Risk-Based Testing

**Prioritize testing based on risk assessment**

### Risk Dimensions

**Impact** - What breaks if this fails?
- Critical: Data loss, security breach, payment failures
- High: Core features broken, bad UX
- Medium: Minor features affected
- Low: Cosmetic issues

**Complexity** - How likely to have bugs?
- High: Complex algorithms, async logic, edge cases
- Medium: Standard business logic
- Low: Simple CRUD, straightforward functions

**Change Frequency** - How often modified?
- High: Rapidly evolving features
- Medium: Occasional updates
- Low: Set-and-forget code

### Testing Priority Matrix
```
HIGH PRIORITY (Must test):
✓ Payment/financial logic
✓ Authentication/authorization
✓ Data validation and persistence
✓ Critical user journeys
✓ Complex algorithms
✓ API integrations
✓ Security-sensitive code
✓ Accessibility requirements (keyboard nav, screen reader, contrast)

MEDIUM PRIORITY (Should test):
✓ Business logic with multiple branches
✓ Utility functions used across codebase
✓ Form validation
✓ Data transformations
✓ Error handling paths
✓ Frequently changed features

LOW PRIORITY (Optional):
- Simple getters/setters
- UI styling/layout
- Configuration files
- Straightforward CRUD operations
- One-time scripts
```

### Risk Assessment Example
```typescript
// HIGH RISK - Must test
// Impact: Critical (payments)
// Complexity: High (currency conversion, rounding)
// Change frequency: Medium
function calculateOrderTotal(items, discounts, taxRate) {
  // Complex calculation logic
  // Write comprehensive tests
}

// MEDIUM RISK - Should test
// Impact: Medium (UX issue if broken)
// Complexity: Medium (validation rules)
// Change frequency: Low
function validateEmail(email) {
  // Standard validation
  // Write basic tests
}

// LOW RISK - Optional
// Impact: Low (cosmetic)
// Complexity: Low (simple assignment)
// Change frequency: Low
function getUserDisplayName(user) {
  return user.name || user.email;
  // Can skip testing, or add simple test
}
```

---

## Test-After Development Workflow

### Step 1: Implement Feature

Focus on making it work:
- Write working code
- Manual testing in browser/console
- Get feedback from users/stakeholders
- Iterate on implementation

**Don't worry about tests yet** - understand the problem first.

### Step 2: Manual Verification

Test the feature manually:
- Happy path works
- Edge cases handled
- Error states graceful
- Performance acceptable

**Document interesting cases** - these become test scenarios.

### Step 3: Risk Assessment

Ask yourself:
- What's the impact if this breaks?
- How complex is this code?
- Will this change frequently?
- Are there edge cases I'm worried about?

**Use the priority matrix** to decide testing level.

### Step 4: Write Automated Tests

Based on risk assessment:

**High priority** - Comprehensive tests:
```typescript
describe('calculateOrderTotal', () => {
  it('should calculate total with single item');
  it('should apply percentage discount');
  it('should apply fixed discount');
  it('should calculate tax correctly');
  it('should handle multiple currencies');
  it('should round to 2 decimal places');
  it('should throw on negative prices');
  it('should handle empty cart');
});
```

**Medium priority** - Essential tests:
```typescript
describe('validateEmail', () => {
  it('should accept valid email');
  it('should reject invalid format');
  it('should reject missing domain');
});
```

**Low priority** - Skip or minimal:
```typescript
// Maybe one smoke test if you're feeling thorough
it('should return user name when available', () => {
  expect(getUserDisplayName({ name: 'Alice' })).toBe('Alice');
});
```

### Step 5: Refactor with Confidence

Now that tests exist:
- Optimize performance
- Improve code structure
- Rename variables
- Extract functions

**Tests catch regressions** while you improve code.

---

## Test-Driven Bug Fixing

When bugs are found, use this workflow:

### 1. Reproduce Bug

Write failing test that reproduces the issue:
```typescript
it('should handle empty cart without crashing', () => {
  // This currently fails
  const result = calculateOrderTotal([], [], 0.2);
  expect(result).toBe(0);
});
```

### 2. Fix Bug

Implement the fix:
```typescript
function calculateOrderTotal(items, discounts, taxRate) {
  if (items.length === 0) return 0; // Fix
  
  // Rest of logic...
}
```

### 3. Verify Test Passes

Run test suite, confirm:
- New test passes
- No regressions

### 4. Keep Test for Regression

This test now prevents the bug from returning.

**Benefits**:
- Documents bug fixes
- Builds test suite organically
- Prevents regression
- Forces you to understand the bug

---

## Vitest Setup

### Installation
```bash
npm install -D vitest @vitest/ui
npm install -D @testing-library/svelte @testing-library/jest-dom
```

### Configuration (`vitest.config.ts`)
```typescript
import { defineConfig } from 'vitest/config';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte({ hot: !process.env.VITEST })],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      exclude: ['**/*.test.ts', '**/*.spec.ts', '**/types.ts']
    }
  }
});
```

### Setup File (`src/test/setup.ts`)
```typescript
import '@testing-library/jest-dom';
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/svelte';

// Cleanup after each test
afterEach(() => {
  cleanup();
});
```

---

## Basic Test Structure

### Unit Test Pattern
```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest';

describe('calculateTotal', () => {
  it('should sum array of numbers', () => {
    const result = calculateTotal([1, 2, 3]);
    expect(result).toBe(6);
  });

  it('should return 0 for empty array', () => {
    const result = calculateTotal([]);
    expect(result).toBe(0);
  });

  it('should handle negative numbers', () => {
    const result = calculateTotal([-1, -2, 3]);
    expect(result).toBe(0);
  });
});
```

### AAA Pattern (Arrange-Act-Assert)
```typescript
it('should update user profile', () => {
  // Arrange - Set up test data
  const user = { id: '1', name: 'Alice' };
  const updates = { name: 'Alicia' };
  
  // Act - Execute the code under test
  const result = updateProfile(user, updates);
  
  // Assert - Verify the outcome
  expect(result.name).toBe('Alicia');
  expect(result.id).toBe('1');
});
```

---

## Svelte Component Testing

### Basic Component Test
```typescript
import { render, screen, fireEvent } from '@testing-library/svelte';
import { describe, it, expect } from 'vitest';
import Counter from './Counter.svelte';

describe('Counter', () => {
  it('should render initial count', () => {
    render(Counter, { props: { initialCount: 0 } });
    
    expect(screen.getByText('Count: 0')).toBeInTheDocument();
  });

  it('should increment count on button click', async () => {
    render(Counter, { props: { initialCount: 0 } });
    
    const button = screen.getByRole('button', { name: /increment/i });
    await fireEvent.click(button);
    
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });
});
```

### Testing Component Props
```typescript
it('should accept and display custom label', () => {
  render(Button, { 
    props: { 
      label: 'Click Me',
      variant: 'primary' 
    } 
  });
  
  const button = screen.getByRole('button');
  expect(button).toHaveTextContent('Click Me');
  expect(button).toHaveClass('btn--primary');
});
```

### Testing Events
```typescript
it('should emit custom event on click', async () => {
  const { component } = render(Button);
  
  const handleClick = vi.fn();
  component.$on('click', handleClick);
  
  const button = screen.getByRole('button');
  await fireEvent.click(button);
  
  expect(handleClick).toHaveBeenCalledTimes(1);
});
```

### Testing Reactive Statements
```typescript
import { tick } from 'svelte';

it('should update derived value when input changes', async () => {
  const { component } = render(Calculator);
  
  const input = screen.getByLabelText('Number');
  await fireEvent.input(input, { target: { value: '5' } });
  await tick(); // Wait for reactive statements to run
  
  expect(screen.getByText('Doubled: 10')).toBeInTheDocument();
});
```

---

## Mocking Strategies

### Mocking Functions
```typescript
import { vi } from 'vitest';

it('should call API with correct parameters', async () => {
  const mockFetch = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ id: '1', name: 'Test' })
  });
  
  global.fetch = mockFetch;
  
  await fetchUser('1');
  
  expect(mockFetch).toHaveBeenCalledWith('/api/users/1');
});
```

### Mocking Modules
```typescript
import { vi } from 'vitest';

// Mock entire module
vi.mock('$lib/api', () => ({
  fetchUsers: vi.fn().mockResolvedValue([
    { id: '1', name: 'Alice' }
  ])
}));

// Or mock specific exports
vi.mock('$lib/utils', async () => {
  const actual = await vi.importActual('$lib/utils');
  return {
    ...actual,
    generateId: vi.fn(() => 'test-id')
  };
});
```

### Mocking Supabase
```typescript
import { vi } from 'vitest';

const mockSupabase = {
  from: vi.fn().mockReturnValue({
    select: vi.fn().mockReturnValue({
      eq: vi.fn().mockResolvedValue({
        data: [{ id: '1', email: 'test@example.com' }],
        error: null
      })
    }),
    insert: vi.fn().mockResolvedValue({
      data: { id: '1' },
      error: null
    })
  })
};

vi.mock('$lib/supabaseClient', () => ({
  supabase: mockSupabase
}));
```

### Mocking Stores
```typescript
import { vi } from 'vitest';
import { writable } from 'svelte/store';

// Mock store module
vi.mock('$lib/stores/user', () => ({
  userStore: writable({ id: '1', name: 'Test User' })
}));

// Or spy on store methods
it('should update store on success', async () => {
  const { subscribe, set } = writable(null);
  const setSpy = vi.spyOn({ set }, 'set');
  
  await loadUserData();
  
  expect(setSpy).toHaveBeenCalledWith({ id: '1', name: 'Alice' });
});
```

---

## Testing Async Code

### Promises
```typescript
it('should fetch user data', async () => {
  const user = await fetchUser('1');
  
  expect(user).toEqual({
    id: '1',
    name: 'Alice'
  });
});
```

### Callbacks
```typescript
it('should call callback with result', (done) => {
  fetchUser('1', (user) => {
    expect(user.name).toBe('Alice');
    done();
  });
});
```

### Waiting for DOM Updates
```typescript
import { waitFor } from '@testing-library/svelte';

it('should show loading then data', async () => {
  render(UserProfile, { props: { userId: '1' } });
  
  expect(screen.getByText('Loading...')).toBeInTheDocument();
  
  await waitFor(() => {
    expect(screen.getByText('Alice')).toBeInTheDocument();
  });
});
```

---

## Test Organization

### File Structure
```
src/
├── lib/
│   ├── components/
│   │   ├── Button.svelte
│   │   └── Button.test.ts
│   ├── utils/
│   │   ├── date.ts
│   │   └── date.test.ts
│   └── api/
│       ├── users.ts
│       └── users.test.ts
└── test/
    ├── setup.ts
    ├── helpers.ts
    └── mocks/
        ├── supabase.ts
        └── api.ts
```

### Naming Conventions
```
✓ Button.test.ts
✓ Button.spec.ts
✗ test-button.ts
✗ ButtonTests.ts
```

### Test Helpers
```typescript
// test/helpers.ts
export function renderWithProviders(component, props = {}) {
  return render(component, {
    props,
    context: new Map([
      ['supabase', mockSupabase],
      ['user', testUser]
    ])
  });
}

export const testUser = {
  id: 'test-id',
  email: 'test@example.com',
  name: 'Test User'
};
```

---

## Coverage Goals

### What to Aim For

**Not 100%** - Diminishing returns after ~80%

**Focus coverage on**:
- ✅ Business logic functions
- ✅ Complex algorithms
- ✅ Utilities used across codebase
- ✅ Critical user journeys
- ✅ Bug-prone areas

**Lower priority**:
- ❌ Simple getters/setters
- ❌ Type definitions
- ❌ Configuration files
- ❌ Generated code

### Running Coverage
```bash
# Run tests with coverage
npm run test:coverage

# View HTML report
open coverage/index.html
```

### Coverage Configuration
```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      statements: 80,
      branches: 75,
      functions: 80,
      lines: 80,
      exclude: [
        '**/*.config.ts',
        '**/*.d.ts',
        '**/types.ts',
        'src/test/**'
      ]
    }
  }
});
```

---

## Common Pitfalls

### Over-Mocking
```typescript
// ✗ Bad: Mocking everything, testing nothing
it('should update user', async () => {
  vi.mock('./updateUser');
  const result = await updateUser(user);
  expect(result).toBeDefined(); // What are we even testing?
});

// ✓ Good: Test real code, mock external dependencies
it('should update user', async () => {
  const mockFetch = vi.fn().mockResolvedValue({ ok: true });
  global.fetch = mockFetch;
  
  const result = await updateUser(user);
  
  expect(mockFetch).toHaveBeenCalledWith('/api/users/1', {
    method: 'PUT',
    body: JSON.stringify(user)
  });
  expect(result.success).toBe(true);
});
```

### Testing Implementation Details
```typescript
// ✗ Bad: Testing internal state
it('should set loading to true', () => {
  const { component } = render(UserList);
  expect(component.loading).toBe(true); // Internal detail
});

// ✓ Good: Testing observable behaviour
it('should show loading indicator', () => {
  render(UserList);
  expect(screen.getByText('Loading...')).toBeInTheDocument();
});
```

### Brittle Selectors
```typescript
// ✗ Bad: Fragile selectors
const button = container.querySelector('.btn.btn--primary.large');

// ✓ Good: Semantic queries
const button = screen.getByRole('button', { name: 'Submit' });
```

### Not Testing Error Cases
```typescript
// ✗ Bad: Only happy path
it('should fetch user', async () => {
  const user = await fetchUser('1');
  expect(user).toBeDefined();
});

// ✓ Good: Test errors too
describe('fetchUser', () => {
  it('should return user on success', async () => {
    const user = await fetchUser('1');
    expect(user.id).toBe('1');
  });

  it('should throw on network error', async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error('Network error'));
    
    await expect(fetchUser('1')).rejects.toThrow('Network error');
  });

  it('should return null when user not found', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 404
    });
    
    const user = await fetchUser('999');
    expect(user).toBeNull();
  });
});
```

---

## Quick Reference

### Common Matchers
```typescript
// Equality
expect(value).toBe(5);              // Strict equality
expect(object).toEqual({ a: 1 });   // Deep equality
expect(array).toContain('item');    // Array contains

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeLessThanOrEqual(5);
expect(value).toBeCloseTo(0.3, 2);  // Floating point

// Strings
expect(string).toMatch(/pattern/);
expect(string).toContain('substring');

// Arrays/Objects
expect(array).toHaveLength(3);
expect(object).toHaveProperty('key', 'value');

// Errors
expect(() => fn()).toThrow();
expect(() => fn()).toThrow(Error);
expect(() => fn()).toThrow('message');

// Async
await expect(promise).resolves.toBe('value');
await expect(promise).rejects.toThrow();
```

### Common Testing Library Queries
```typescript
// Preferred (accessible)
screen.getByRole('button', { name: /submit/i });
screen.getByLabelText('Email');
screen.getByPlaceholderText('Enter email');
screen.getByText('Welcome');

// Fallbacks
screen.getByTestId('submit-button');

// Query variants
screen.getBy...    // Throws if not found
screen.queryBy...  // Returns null if not found
screen.findBy...   // Async, waits for element

// Multiple elements
screen.getAllByRole('listitem');
```

### Running Tests
```bash
# Run all tests
npm test

# Watch mode
npm test -- --watch

# Run specific file
npm test Button.test.ts

# Run tests matching pattern
npm test -- --grep "Button"

# Run with coverage
npm test -- --coverage

# UI mode
npm test -- --ui
```

---

## Portfolio Evidence

**KSBs Demonstrated by Testing**:
- **S9**: Create Analysis Artefacts (test plans, coverage reports, risk assessments)
- **S10**: Analyse Problem Reports (reproduction tests, debugging tests)
- **S11**: Apply Appropriate Recovery Techniques (regression tests)
- **S14**: Follow Company Procedures (testing standards, CI integration)

**How to Document**:
- Screenshot coverage reports showing strategic testing
- Document risk assessment decisions in README/docs
- Show test files alongside features
- Explain testing decisions in code review
- Document bug reproduction tests
- Demonstrate professional judgment about test priorities

**Evidence Example**:
```markdown
## Testing Strategy

Applied risk-based testing approach to this feature:

HIGH PRIORITY (Tested):
- Payment calculation logic - Complex algorithm, financial impact
- User authentication - Security critical
- Data validation - Prevents data corruption

MEDIUM PRIORITY (Basic tests):
- Form validation - Standard patterns, low complexity
- API error handling - Important but straightforward

LOW PRIORITY (Manual testing only):
- UI styling - Visual verification sufficient
- Configuration loading - One-time, low risk
```

---

## Accessibility Testing

Accessibility is a testable requirement, not a subjective preference. Include it in the testing strategy alongside functional tests.

### Automated Accessibility Checks
```typescript
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

it('should have no accessibility violations', async () => {
	const { container } = render(LoginForm);
	const results = await axe(container);
	expect(results).toHaveNoViolations();
});
```

### Keyboard Navigation Tests
```typescript
it('should be navigable by keyboard', async () => {
	render(LoginForm);

	// Tab to email input
	await userEvent.tab();
	expect(screen.getByLabelText('Email')).toHaveFocus();

	// Tab to password input
	await userEvent.tab();
	expect(screen.getByLabelText('Password')).toHaveFocus();

	// Tab to submit button
	await userEvent.tab();
	expect(screen.getByRole('button', { name: /log in/i })).toHaveFocus();

	// Enter submits
	await userEvent.keyboard('{Enter}');
	// Assert form submitted
});
```

### Screen Reader Assertions
```typescript
it('should announce errors to screen readers', async () => {
	render(LoginForm);

	const submitButton = screen.getByRole('button', { name: /log in/i });
	await fireEvent.click(submitButton);

	// Error messages should be associated with inputs
	const emailInput = screen.getByLabelText('Email');
	const errorId = emailInput.getAttribute('aria-describedby');
	expect(errorId).toBeTruthy();
	expect(document.getElementById(errorId)).toHaveTextContent('Email is required');
});
```

### What to Test for Accessibility
```
HIGH PRIORITY:
✓ Forms: labels, error association, keyboard submit
✓ Modals: focus trap, escape to close, focus return
✓ Navigation: keyboard traversal, skip links
✓ Dynamic content: aria-live announcements

MEDIUM PRIORITY:
✓ Colour contrast (automated via axe)
✓ Image alt text presence
✓ Heading hierarchy

AUTOMATED (run on every component):
✓ axe-core violations check
```

---

## Success Criteria

Tests are effective when they:
- Pass reliably (no flakiness)
- Run quickly (<1s for unit tests)
- Test behaviour, not implementation
- Catch real bugs before production
- Give confidence to refactor
- Focus on high-risk code
- Serve as documentation
- Reflect professional judgment about priorities
- Include accessibility checks for user-facing components