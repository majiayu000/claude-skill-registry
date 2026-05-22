---
name: nextjs-unit-test-creator
description: Generate comprehensive unit tests for Next.js 16 applications covering App Router, Server Components, Client Components, API routes, and Server Actions with industry best practices
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: test-generation
---

## What I do

I implement a complete Next.js 16 test generation workflow by extending `test-generator-framework`:

1. **Analyze Next.js Codebase**: Scan Next.js 16 application to identify components, hooks, and utilities using App Router patterns
2. **Detect Next.js Framework**: Identify specific Next.js testing setup (Vitest recommended for Next.js 16, Jest, Playwright) from `package.json`
3. **Generate Next.js-16-Specific Scenarios**: Create comprehensive test scenarios covering:
   - **App Router Components**: Server components (`page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`)
   - **Client Components**: `"use client"` components with hooks and interactions
   - **Server Actions**: `async` server action functions and mutations
   - **API Routes**: App Router API handlers (`app/api/*/route.ts`)
   - **Hooks**: Custom hooks with React-specific patterns
   - **Utility Functions**: Next.js utilities (routing, data fetching, validation)
   - **E2E Tests**: Next.js routing, page navigation, API routes (if Playwright detected)
4. **Delegate to Framework**: Use `test-generator-framework` for core test generation workflow
5. **Ensure Executability**: Verify tests run with `npm run test` - **ALL TESTS MUST PASS**
6. **Validate Next.js 16 Patterns**: Ensure tests handle Server Components, Suspense, and App Router correctly

**Critical Requirement**: All generated tests must pass (`npm run test`) before PR creation. This integrates with `nextjs-pr-workflow` to enforce test validation.

## When to use me

Use this workflow when:
- You need to create unit tests for new Next.js components
- You want to ensure all edge cases and user interactions are covered
- You need tests for utility functions in a Next.js application
- You need E2E tests for Next.js applications (Playwright)
- You prefer a systematic approach to test generation with user confirmation
- You want to ensure tests run correctly with your project's test framework

**Framework**: This skill extends `test-generator-framework` for core test generation workflow, adding Next.js-specific functionality.

## Prerequisites

- Next.js project with `package.json`
- Test framework installed (Jest, Vitest, Playwright, or other)
- Next.js source code (components, utilities, hooks)
- Appropriate file permissions to create test files

Note: The skill automatically detects the test framework from `package.json` and uses appropriate commands. For E2E tests, Playwright must be installed and explicitly requested.

## Next.js 16 Requirements

Next.js 16 introduces several testing considerations:

### App Router Architecture
- **Server Components**: Default - cannot use hooks, useState, useEffect
- **Client Components**: Requires `"use client"` directive
- **Hybrid Components**: Mix Server and Client components
- **Nested Layouts**: Test layout nesting and state sharing

### Testing Frameworks
- **Vitest**: Recommended for Next.js 16 (faster, ESM native)
- **Jest**: Still supported but may require more configuration
- **Playwright**: For E2E testing

### Server Components Testing
```typescript
// Server components are async
render(await ServerComponent())
```

### Client Components Testing
```typescript
// Client components can use hooks
render(<ClientComponent />)
await user.click(screen.getByRole('button'))
```

### Server Actions Testing
```typescript
// Server actions are async functions
const result = await serverAction(formData)
```

### API Route Testing
```typescript
// API routes are Request/Response handlers
const request = new Request('http://localhost', { method: 'POST' })
const response = await POST(request)
```

## Steps

### Step 1: Analyze Next.js Codebase
- Use glob patterns to find TypeScript/JavaScript files: `**/*.{ts,tsx,js,jsx}`
- Exclude test files: `**/*.test.{ts,tsx,js,jsx}`, `**/*.spec.{ts,tsx,js,jsx}`, `**/__tests__/**/*`
- Identify new files or functions by:
   - Checking git status for uncommitted/new files
   - Reading each file to identify:
     - Server Components: `export default function ServerComponent()`
     - Client Components: `'use client'` + `export function Component()`
     - Utility functions: `export function`, `export const`
     - Custom hooks: `use*` functions returning state/effects
- Identify import statements to understand dependencies

### Step 2: Detect Next.js Testing Framework
- Check `package.json` for test dependencies:
  ```bash
  # Check for Jest
  grep -E "(jest|@testing-library)" package.json

  # Check for Vitest
  grep -i "vitest" package.json

  # Check for Playwright
  grep -i "playwright" package.json

  # Check test scripts
  grep -A 5 '"scripts"' package.json | grep test
  ```
- Determine test framework:
   - **Jest**: If `jest` or `@testing-library/*` is in devDependencies
   - **Vitest**: If `vitest` is in devDependencies
   - **Playwright**: If `@playwright/test` is in devDependencies
   - **Other**: Parse test scripts to identify runner
- Store appropriate test command:
  ```bash
  # Determine test command from package.json
  if grep -q '"test":.*vitest' package.json; then
      TEST_CMD="npm run test"
      TEST_FRAMEWORK="vitest"
  elif grep -q '"test":.*jest' package.json; then
      TEST_CMD="npm run test"
      TEST_FRAMEWORK="jest"
  else
      TEST_CMD="npm run test"
      TEST_FRAMEWORK="detected"
  fi

  # Check for Playwright E2E tests
  if grep -q "@playwright/test" package.json; then
      PLAYWRIGHT_INSTALLED=true
      E2E_CMD="npm run test:e2e"
  else
      PLAYWRIGHT_INSTALLED=false
  fi
  ```
- Check for related testing libraries:
   - React Testing Library (`@testing-library/react`, `@testing-library/jest-dom`)
   - Testing Library user-event (`@testing-library/user-event`)
   - Next.js testing utilities (`@next/test-utils`)
   - Playwright (`@playwright/test`) for E2E testing
- Ask user if E2E tests are needed if Playwright is installed and user workflow suggests E2E testing

### Step 3: Generate Next.js-Specific Test Scenarios

#### Server Component Scenarios
- **SSR Behavior**: Component renders correctly on server
- **Props Passing**: Server props are passed correctly
- **Data Fetching**: Server-side data fetching works
- **Caching**: Next.js caching behavior

#### Client Component Scenarios
- **Use Client**: Component is marked with `'use client'`
- **Interactivity**: Client-side interactions work
- **State Management**: React state updates correctly

#### Utility Function Scenarios
- **Happy Path**: Valid inputs return expected outputs
- **Edge Cases**: Empty inputs, null/undefined values, boundary values
- **Error Handling**: Invalid inputs raise appropriate errors
- **Type Validation**: Type checking and coercion
- **Performance**: Large input handling
- **Async Functions**: Promises resolve/reject correctly

#### Custom Hook Scenarios
- **Initial State**: Returns correct initial values
- **State Updates**: State updates correctly after actions
- **Side Effects**: useEffect runs with correct dependencies
- **Cleanup**: useEffect cleanup functions work correctly
- **Multiple Calls**: Hook can be called multiple times
- **Dependency Changes**: Responds to dependency changes

#### E2E Test Scenarios (Playwright)
- **Page Navigation**: User can navigate between pages
- **Form Submissions**: Forms submit correctly and display results
- **Authentication**: Login/logout workflows work as expected
- **Data Display**: Data is fetched and displayed correctly
- **User Interactions**: Click events, keyboard navigation, scroll behavior
- **Responsive Design**: UI works on different screen sizes
- **Error Handling**: Error states display correctly
- **Loading States**: Loading indicators appear during async operations
- **Accessibility**: Page is accessible via keyboard and screen readers
- **Performance**: Pages load within acceptable time limits

### Step 4: Display Scenarios for Confirmation

Display formatted output:
```
📋 Generated Test Scenarios for <file_name>

**Type:** <Server Component | Client Component | Utility Function | Custom Hook>

**Item to Test:** <ComponentName | functionName>

**Scenarios:**
1. Rendering/SSR Test
   - Component renders on server correctly
   - Props are passed correctly

2. State/Interaction Test
   - State updates after interaction
   - Multiple state transitions work

3. Edge Case Test
   - Empty data handled gracefully
   - Null/undefined values don't break component

4. Accessibility Test
   - ARIA labels are present
   - Keyboard navigation works

**Total Scenarios:** <number>
**Estimated Test Lines:** <number>

**Test Framework Detected:** <Jest | Vitest | Other>
**Test Command:** <npm run test | vitest | jest>

**E2E Tests:** <Yes - Playwright | No>
**E2E Test Command:** <npm run test:e2e | n/a>

Are these scenarios acceptable? (y/n/suggest)
```

Wait for user response:
- **y**: Proceed to create test files (and E2E tests if requested)
- **n**: Ask for modifications or cancel
- **suggest**: Ask user to add/remove scenarios

Wait for user response:
- **y**: Proceed to create test files
- **n**: Ask for modifications or cancel
- **suggest**: Ask user to add/remove scenarios

Wait for user response:
- **y**: Proceed to create test files
- **n**: Ask for modifications or cancel
- **suggest**: Ask user to add/remove scenarios

### Step 5: Delegate to Test Generator Framework

**Note**: Core test generation workflow is provided by `test-generator-framework`. This skill focuses only on Next.js-specific aspects.

Refer to `test-generator-framework` for:
- Generic test file creation structure
- Framework detection and command determination
- User confirmation workflow
- Executability verification

Next.js-specific test file templates below extend the framework structure.

#### For Components (Jest + React Testing Library)
```typescript
/**
 * Test suite for <ComponentName>
 * Generated by nextjs-unit-test-creator skill
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import userEvent from '@testing-library/user-event'
import { <ComponentName> } from './<ComponentName>'

// Extend Jest to include jest-axe matchers
expect.extend(toHaveNoViolations)

describe('<ComponentName>', () => {
  const defaultProps = {
    // Default props for testing
  }

  it('renders without crashing', () => {
    render(<<ComponentName> {...defaultProps} />)
    expect(screen.getByText(/content/i)).toBeInTheDocument()
  })

  it('displays correct props', () => {
    const customProps = { ...defaultProps, title: 'Custom Title' }
    render(<<ComponentName> {...customProps} />)
    expect(screen.getByText('Custom Title')).toBeInTheDocument()
  })

  it('handles user interactions', async () => {
    const user = userEvent.setup()
    const handleClick = jest.fn()
    render(<<ComponentName> {...defaultProps} onClick={handleClick} />)

    const button = screen.getByRole('button')
    await user.click(button)

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('updates state after interaction', async () => {
    const user = userEvent.setup()
    render(<<ComponentName> {...defaultProps} />)

    const input = screen.getByLabelText(/search/i)
    await user.type(input, 'test query')

    expect(input).toHaveValue('test query')
  })

  it('handles empty state', () => {
    const emptyProps = { ...defaultProps, data: [] }
    render(<<ComponentName> {...emptyProps} />)

    expect(screen.getByText(/no data/i)).toBeInTheDocument()
  })

  it('has no accessibility violations', async () => {
    const { container } = render(<<ComponentName> {...defaultProps} />)
    const results = await axe(container)

    expect(results).toHaveNoViolations()
  })

  it('shows loading state', () => {
    const loadingProps = { ...defaultProps, isLoading: true }
    render(<<ComponentName> {...loadingProps} />)

    expect(screen.getByRole('progressbar')).toBeInTheDocument()
  })

  it('matches snapshot', () => {
    const { container } = render(<<ComponentName> {...defaultProps} />)
    expect(container).toMatchSnapshot()
  })
})
```

#### For Components (Vitest + React Testing Library)
```typescript
/**
 * Test suite for <ComponentName>
 * Generated by nextjs-unit-test-creator skill
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { <ComponentName> } from './<ComponentName>'

describe('<ComponentName>', () => {
  const defaultProps = {
    // Default props for testing
  }

  beforeEach(() => {
    // Reset mocks before each test
    vi.clearAllMocks()
  })

  it('renders without crashing', () => {
    render(<<ComponentName> {...defaultProps} />)
    expect(screen.getByText(/content/i)).toBeInTheDocument()
  })

  it('displays correct props', () => {
    const customProps = { ...defaultProps, title: 'Custom Title' }
    render(<<ComponentName> {...customProps} />)
    expect(screen.getByText('Custom Title')).toBeInTheDocument()
  })

  it('handles user interactions', async () => {
    const user = userEvent.setup()
    const handleClick = vi.fn()
    render(<<ComponentName> {...defaultProps} onClick={handleClick} />)

    const button = screen.getByRole('button')
    await user.click(button)

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('updates state after interaction', async () => {
    const user = userEvent.setup()
    render(<<ComponentName> {...defaultProps} />)

    const input = screen.getByLabelText(/search/i)
    await user.type(input, 'test query')

    expect(input).toHaveValue('test query')
  })

  it('handles empty state', () => {
    const emptyProps = { ...defaultProps, data: [] }
    render(<<ComponentName> {...emptyProps} />)

    expect(screen.getByText(/no data/i)).toBeInTheDocument()
  })

  it('shows loading state', () => {
    const loadingProps = { ...defaultProps, isLoading: true }
    render(<<ComponentName> {...loadingProps} />)

    expect(screen.getByRole('progressbar')).toBeInTheDocument()
  })
})
```

#### For Custom Hooks (Jest)
```typescript
/**
 * Test suite for use<HookName>
 * Generated by nextjs-unit-test-creator skill
 */

import { renderHook, act, waitFor } from '@testing-library/react'
import { use<HookName> } from './use<HookName>'

describe('use<HookName>', () => {
  it('returns correct initial state', () => {
    const { result } = renderHook(() => use<HookName>())
    expect(result.current.someValue).toBe(initialValue)
  })

  it('updates state correctly', async () => {
    const { result } = renderHook(() => use<HookName>())

    await act(async () => {
      result.current.someAction()
    })

    expect(result.current.someValue).toBe(newValue)
  })

  it('handles dependencies correctly', async () => {
    const { result, rerender } = renderHook(
      ({ prop }) => use<HookName>(prop),
      { initialProps: { prop: 'initial' } }
    )

    expect(result.current.value).toBe('initial')

    await act(async () => {
      rerender({ prop: 'updated' })
    })

    expect(result.current.value).toBe('updated')
  })

  it('cleans up on unmount', () => {
    const cleanup = jest.fn()
    const { unmount } = renderHook(() => use<HookName>(cleanup))

    unmount()

    expect(cleanup).toHaveBeenCalledTimes(1)
  })
})
```

#### For Custom Hooks (Vitest)
```typescript
/**
 * Test suite for use<HookName>
 * Generated by nextjs-unit-test-creator skill
 */

import { describe, it, expect, vi } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { use<HookName> } from './use<HookName>'

describe('use<HookName>', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('returns correct initial state', () => {
    const { result } = renderHook(() => use<HookName>())
    expect(result.current.someValue).toBe(initialValue)
  })

  it('updates state correctly', async () => {
    const { result } = renderHook(() => use<HookName>())

    await act(async () => {
      result.current.someAction()
    })

    expect(result.current.someValue).toBe(newValue)
  })

  it('handles dependencies correctly', async () => {
    const { result, rerender } = renderHook(
      ({ prop }) => use<HookName>(prop),
      { initialProps: { prop: 'initial' } }
    )

    expect(result.current.value).toBe('initial')

    await act(async () => {
      rerender({ prop: 'updated' })
    })

    expect(result.current.value).toBe('updated')
  })

  it('cleans up on unmount', () => {
    const cleanup = vi.fn()
    const { unmount } = renderHook(() => use<HookName>(cleanup))

    unmount()

    expect(cleanup).toHaveBeenCalledTimes(1)
  })
})
```

#### For E2E Tests (Playwright)

**Note**: Refer to `test-generator-framework` for core E2E testing structure.

Next.js-specific E2E patterns to focus on:

```typescript
import { test, expect } from '@playwright/test'

test.describe('Next.js Routing', () => {
  test('navigates between Next.js pages', async ({ page }) => {
    await page.goto('/')
    await page.click('text=About')
    await expect(page).toHaveURL('/about')
  })

  test('handles Next.js router navigation', async ({ page }) => {
    await page.goto('/dashboard')
    await page.click('[data-testid="link-profile"]')
    await expect(page).toHaveURL('/profile')
  })
})

test.describe('Next.js API Routes', () => {
  test('fetches data from API route', async ({ page }) => {
    await page.goto('/users')

    // Mock Next.js API route
    await page.route('**/api/users', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([{ id: 1, name: 'User 1' }]),
      })
    })

    await expect(page.locator('text=User 1')).toBeVisible()
  })

  test('handles API route errors', async ({ page }) => {
    await page.goto('/data')

    await page.route('**/api/data', async (route) => {
      await route.fulfill({ status: 500 })
    })

    await expect(page.locator('[data-testid="error"]')).toBeVisible()
  })
})
```

### Step 6: Verify Executability

Refer to `test-generator-framework` for core executability verification.

### Step 7: Display Summary

```
✅ Next.js test files created successfully!

**Test Files Created:**
- <ComponentName>.test.tsx (<number> tests)
- <useHookName>.test.tsx (<number> tests)

**Total Tests Generated:** <number>
**Test Framework:** <Jest | Vitest>

**Next.js-Specific Categories:**
- Server components: <number>
- Client components: <number>
- Next.js routing: <number>
- API routes: <number>

**To run tests:**
```bash
npm run test
```

## Next.js-Specific Scenario Rules

### Server Components
- **SSR Behavior**: Component renders correctly on server
- **Props Passing**: Server props are passed correctly
- **Data Fetching**: Server-side data fetching works
- **Caching**: Next.js caching behavior

### Client Components
- **Use Client**: Component is marked with `'use client'`
- **Interactivity**: Client-side interactions work
- **State Management**: React state updates correctly

### Next.js Utilities
- **Routing**: Next.js App Router navigation
- **API Routes**: API endpoint testing
- **Image Optimization**: Next.js image handling
- **Metadata**: Page metadata generation

#### For E2E Tests with API Mocking (Playwright)
```typescript
/**
 * E2E test suite for <PageName> with API mocking
 * Generated by nextjs-unit-test-creator skill
 */

import { test, expect } from '@playwright/test'

test.describe('<PageName> with API Mocking', () => {
  test('displays mocked data', async ({ page }) => {
    // Mock API response
    await page.route('**/api/data', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          { id: 1, name: 'Mocked Item 1' },
          { id: 2, name: 'Mocked Item 2' },
        ]),
      })
    })

    await page.goto('/<page-path>')

    // Verify mocked data is displayed
    await expect(page.locator('text=Mocked Item 1')).toBeVisible()
    await expect(page.locator('text=Mocked Item 2')).toBeVisible()
  })

  test('handles API error', async ({ page }) => {
    // Mock API error
    await page.route('**/api/data', async (route) => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal Server Error' }),
      })
    })

    await page.goto('/<page-path>')

    // Verify error message is displayed
    await expect(page.locator('[data-testid="error"]')).toBeVisible()
    await expect(page.locator('text=Failed to load data')).toBeVisible()
  })

  test('handles slow API response', async ({ page }) => {
    // Mock slow API response
    await page.route('**/api/data', async (route) => {
      // Simulate network delay
      await new Promise((resolve) => setTimeout(resolve, 2000))

      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([]),
      })
    })

    await page.goto('/<page-path>')

    // Verify loading state is shown
    await expect(page.locator('[data-testid="loading"]')).toBeVisible()

    // Wait for data to load
    await page.waitForSelector('[data-testid="data-container"]')

    // Loading should be hidden
    await expect(page.locator('[data-testid="loading"]')).not.toBeVisible()
  })
})
```

#### For E2E Tests with Authentication (Playwright)
```typescript
/**
 * E2E test suite for authentication workflows
 * Generated by nextjs-unit-test-creator skill
 */

import { test, expect } from '@playwright/test'

test.describe('Authentication', () => {
  test.beforeEach(async ({ page, context }) => {
    // Clear cookies and storage before each test
    await context.clearCookies()
  })

  test('successful login', async ({ page }) => {
    await page.goto('/login')

    // Fill login form
    await page.fill('input[name="email"]', 'test@example.com')
    await page.fill('input[name="password"]', 'password123')

    // Submit form
    await page.click('button[type="submit"]')

    // Verify redirect to dashboard
    await page.waitForURL('/dashboard')

    // Verify user is authenticated
    await expect(page.locator('text=Welcome, Test')).toBeVisible()
    await expect(page.locator('[data-testid="logout-button"]')).toBeVisible()
  })

  test('failed login with invalid credentials', async ({ page }) => {
    await page.goto('/login')

    // Fill login form with invalid credentials
    await page.fill('input[name="email"]', 'invalid@example.com')
    await page.fill('input[name="password"]', 'wrongpassword')

    // Submit form
    await page.click('button[type="submit"]')

    // Verify error message
    await expect(page.locator('[data-testid="error"]')).toBeVisible()
    await expect(page.locator('text=Invalid credentials')).toBeVisible()

    // Verify user is not redirected
    await expect(page).toHaveURL('/login')
  })

  test('successful logout', async ({ page }) => {
    // First login
    await page.goto('/login')
    await page.fill('input[name="email"]', 'test@example.com')
    await page.fill('input[name="password"]', 'password123')
    await page.click('button[type="submit"]')

    await page.waitForURL('/dashboard')

    // Logout
    await page.click('[data-testid="logout-button"]')

    // Verify redirect to login page
    await page.waitForURL('/login')

    // Verify user is logged out
    await expect(page.locator('[data-testid="logout-button"]')).not.toBeVisible()
  })

  test('protected routes require authentication', async ({ page }) => {
    // Try to access protected route without authentication
    await page.goto('/dashboard')

    // Should be redirected to login
    await page.waitForURL('/login')

    // Verify login page is displayed
    await expect(page.locator('text=Sign in')).toBeVisible()
  })
})
```

#### For E2E Tests with File Upload (Playwright)
```typescript
/**
 * E2E test suite for file upload functionality
 * Generated by nextjs-unit-test-creator skill
 */

import { test, expect } from '@playwright/test'
import path from 'path'

test.describe('File Upload', () => {
  test('successful file upload', async ({ page }) => {
    await page.goto('/upload')

    // Select file to upload
    const fileInput = page.locator('input[type="file"]')
    await fileInput.setInputFiles(path.join(__dirname, 'test-file.txt'))

    // Upload button should be enabled
    await expect(page.locator('button[type="submit"]')).toBeEnabled()

    // Submit form
    await page.click('button[type="submit"]')

    // Verify success message
    await expect(page.locator('[data-testid="success"]')).toBeVisible()
    await expect(page.locator('text=File uploaded successfully')).toBeVisible()
  })

  test('multiple file upload', async ({ page }) => {
    await page.goto('/upload')

    // Select multiple files
    const fileInput = page.locator('input[type="file"]')
    await fileInput.setInputFiles([
      path.join(__dirname, 'file1.txt'),
      path.join(__dirname, 'file2.txt'),
    ])

    // Submit form
    await page.click('button[type="submit"]')

    // Verify success message
    await expect(page.locator('[data-testid="success"]')).toBeVisible()
    await expect(page.locator('text=2 files uploaded')).toBeVisible()
  })

  test('invalid file type', async ({ page }) => {
    await page.goto('/upload')

    // Try to upload invalid file type
    const fileInput = page.locator('input[type="file"]')
    await fileInput.setInputFiles(path.join(__dirname, 'invalid.exe'))

    // Submit form
    await page.click('button[type="submit"]')

    // Verify error message
    await expect(page.locator('[data-testid="error"]')).toBeVisible()
    await expect(page.locator('text=Invalid file type')).toBeVisible()
  })

  test('file upload progress', async ({ page }) => {
    await page.goto('/upload')

    // Mock slow upload
    await page.route('**/api/upload', async (route) => {
      await new Promise((resolve) => setTimeout(resolve, 2000))
      await route.fulfill({ status: 200 })
    })

    // Select file
    await page.locator('input[type="file"]').setInputFiles(
      path.join(__dirname, 'test-file.txt')
    )

    // Submit form
    await page.click('button[type="submit"]')

    // Verify progress bar
    await expect(page.locator('[data-testid="progress"]')).toBeVisible()

    // Wait for completion
    await page.waitForSelector('[data-testid="success"]')

    // Verify success
    await expect(page.locator('text=File uploaded successfully')).toBeVisible()
  })
})
```

### Step 6: Verify Executability
- Ensure tests can be run with the appropriate command:
  ```bash
  # Run all tests
  npm run test

  # Run specific test file
  npm run test <fileName>.test.tsx

  # Run tests in watch mode
  npm run test:watch

  # Run tests with coverage
  npm run test:coverage

  # Run tests for specific pattern
  npm run test -- <pattern>
  ```
- Verify no import errors or syntax issues
- Check that all tests are discoverable

### Step 7: Display Summary
```
✅ Test files created successfully!

**Test Files Created:**
- <ComponentName>.test.tsx (<number> tests)
- <functionName>.test.ts (<number> tests)

**Total Tests Generated:** <number>
**Test Framework:** <Jest | Vitest>

**Test Categories:**
- Rendering tests: <number>
- User interaction tests: <number>
- Edge case tests: <number>
- Accessibility tests: <number>
- State management tests: <number>

**To run tests:**
```bash
# Run all tests
npm run test

# Run specific test file
npm run test <fileName>.test.tsx

# Run tests in watch mode
npm run test:watch

# Run with coverage
npm run test:coverage
```

**Next Steps:**
1. Review generated test files
2. Update test data and expected values
3. Run tests to verify they pass
4. Update coverage badge in README.md using `coverage-readme-workflow`
5. Add any missing scenarios
6. Update snapshot tests if needed
```

## Scenario Generation Rules

### Component Tests
- **Rendering**: Component renders without errors
- **Props Display**: Verify props are correctly rendered
- **User Interactions**: Click events, form submissions, keyboard events
- **State Management**: State updates correctly after actions
- **Conditional Rendering**: Elements show/hide based on props/state
- **Accessibility**: ARIA labels, roles, keyboard navigation
- **Loading States**: Display during async operations
- **Empty States**: Display when no data available
- **Error States**: Display error messages appropriately
- **Snapshots**: Ensure UI structure consistency

### Utility Function Tests
- **Happy Path**: Valid inputs return expected outputs
- **Edge Cases**: Empty strings, null, undefined, zero, negative values
- **Error Handling**: Invalid types, out of range values
- **Type Checking**: TypeScript type correctness
- **Performance**: Large inputs handled efficiently
- **Async Handling**: Promises resolve/reject correctly

### Custom Hook Tests
- **Initial State**: Returns correct default values
- **State Updates**: State changes after actions
- **Side Effects**: useEffect runs with proper dependencies
- **Cleanup**: Cleanup functions execute correctly
- **Multiple Instances**: Multiple hook calls work independently
- **Dependency Changes**: Responds to prop changes

## Examples

### Example 1: Simple Component
**Input Code:**
```typescript
interface ButtonProps {
  label: string
  onClick: () => void
  disabled?: boolean
}

export function Button({ label, onClick, disabled = false }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  )
}
```

**Generated Scenarios:**
```
1. Rendering: Button renders without errors
2. Props Display: Label is displayed correctly
3. User Interaction: onClick callback triggered
4. Disabled State: Button is disabled when disabled=true
5. Accessibility: Button has correct role and attributes
```

**Generated Test File:**
```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Button } from './Button'

describe('Button', () => {
  const defaultProps = {
    label: 'Click me',
    onClick: jest.fn(),
  }

  it('renders without crashing', () => {
    render(<Button {...defaultProps} />)
    expect(screen.getByRole('button')).toBeInTheDocument()
  })

  it('displays correct label', () => {
    render(<Button {...defaultProps} />)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('handles click events', async () => {
    const user = userEvent.setup()
    render(<Button {...defaultProps} />)

    const button = screen.getByRole('button')
    await user.click(button)

    expect(defaultProps.onClick).toHaveBeenCalledTimes(1)
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button {...defaultProps} disabled />)
    const button = screen.getByRole('button')
    expect(button).toBeDisabled()
  })

  it('has correct accessibility attributes', () => {
    render(<Button {...defaultProps} />)
    const button = screen.getByRole('button')
    expect(button).toHaveAttribute('type', 'button')
  })
})
```

### Example 2: Utility Function
**Input Code:**
```typescript
export function formatDate(date: Date): string {
  if (!(date instanceof Date) || isNaN(date.getTime())) {
    throw new Error('Invalid date')
  }

  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
```

**Generated Scenarios:**
```
1. Happy path: Valid date returns formatted string
2. Edge case: Today's date
3. Edge case: Future date
4. Error case: Non-Date object
5. Error case: Invalid Date object
6. Edge case: Epoch time
```

**Generated Test File:**
```typescript
import { formatDate } from './dateUtils'

describe('formatDate', () => {
  it('formats a valid date correctly', () => {
    const date = new Date('2024-01-15')
    const result = formatDate(date)
    expect(result).toBe('January 15, 2024')
  })

  it('handles today\'s date', () => {
    const today = new Date()
    const result = formatDate(today)
    expect(typeof result).toBe('string')
    expect(result.length).toBeGreaterThan(0)
  })

  it('handles future dates', () => {
    const futureDate = new Date('2050-12-31')
    const result = formatDate(futureDate)
    expect(result).toContain('2050')
  })

  it('throws error for non-Date object', () => {
    expect(() => formatDate('2024-01-15' as any)).toThrow('Invalid date')
    expect(() => formatDate({} as any)).toThrow('Invalid date')
  })

  it('throws error for invalid Date', () => {
    const invalidDate = new Date('invalid')
    expect(() => formatDate(invalidDate)).toThrow('Invalid date')
  })

  it('handles epoch time', () => {
    const epochDate = new Date(0)
    const result = formatDate(epochDate)
    expect(result).toContain('1970')
  })
})
```

### Example 3: Custom Hook
**Input Code:**
```typescript
import { useState, useEffect } from 'react'

export function useCounter(initialValue: number = 0) {
  const [count, setCount] = useState(initialValue)

  const increment = () => setCount((prev) => prev + 1)
  const decrement = () => setCount((prev) => prev - 1)
  const reset = () => setCount(initialValue)

  return { count, increment, decrement, reset }
}
```

**Generated Scenarios:**
```
1. Initial state: Returns correct initial value
2. Increment: Count increases by 1
3. Decrement: Count decreases by 1
4. Reset: Count resets to initial value
5. Multiple calls: Independent state between instances
6. Default initial value: Starts at 0 when not provided
```

**Generated Test File:**
```typescript
import { renderHook, act } from '@testing-library/react'
import { useCounter } from './useCounter'

describe('useCounter', () => {
  it('returns correct initial value', () => {
    const { result } = renderHook(() => useCounter(5))
    expect(result.current.count).toBe(5)
  })

  it('increments the count', () => {
    const { result } = renderHook(() => useCounter(0))

    act(() => {
      result.current.increment()
    })

    expect(result.current.count).toBe(1)
  })

  it('decrements the count', () => {
    const { result } = renderHook(() => useCounter(5))

    act(() => {
      result.current.decrement()
    })

    expect(result.current.count).toBe(4)
  })

  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(10))

    act(() => {
      result.current.increment()
      result.current.increment()
    })

    expect(result.current.count).toBe(12)

    act(() => {
      result.current.reset()
    })

    expect(result.current.count).toBe(10)
  })

  it('maintains independent state between instances', () => {
    const { result: counter1 } = renderHook(() => useCounter(0))
    const { result: counter2 } = renderHook(() => useCounter(10))

    act(() => {
      counter1.current.increment()
    })

    expect(counter1.current.count).toBe(1)
    expect(counter2.current.count).toBe(10)
  })

  it('uses default initial value when not provided', () => {
    const { result } = renderHook(() => useCounter())
    expect(result.current.count).toBe(0)
  })
})
```

## Best Practices

Refer to `test-generator-framework` for general best practices.

Next.js-specific best practices:
- **SSR Testing**: Test server components render correctly on server
- **Client Components**: Use `'use client'` directive appropriately
- **Next.js Router**: Test page navigation and routing behavior
- **API Routes**: Test Next.js API endpoints with proper mocking
- **Image Optimization**: Consider Next.js Image component behavior
- **Metadata**: Test page metadata and SEO-related aspects

## Common Issues

Refer to `test-generator-framework` for general issues.

Next.js-specific issues:

### Next.js Page Not Found in Tests
**Issue**: Tests fail to navigate to Next.js pages

**Solution**: Use proper Playwright navigation:
```typescript
await page.goto('/about')  // Not page.go('/about')
await expect(page).toHaveURL('/about')
```

### Server Component Hydration Mismatch
**Issue**: Hydration errors in server components

**Solution**: Test SSR behavior separately:
```typescript
it('renders on server', () => {
  render(<ServerComponent />)
  // Verify server-rendered output
})
```

### API Route Not Mocked
**Issue**: Tests calling Next.js API routes fail

**Solution**: Mock Next.js fetch:
```typescript
jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
}))
```

## Troubleshooting Checklist

Refer to `test-generator-framework` for general checklist.

Next.js-specific additions:
Before generating tests:
- [ ] Next.js project structure is valid
- [ ] `package.json` contains Next.js dependencies
- [ ] Server vs client components identified correctly
- [ ] Next.js routing patterns are understood

## Related Commands

Refer to `test-generator-framework` for general commands.

Next.js-specific commands:
```bash
# Build Next.js project
npm run build

# Run Next.js dev server
npm run dev

# Run Next.js linting
npm run lint

# Run Next.js type checking
npm run typecheck
```

## Related Skills

- `nextjs-standard-setup`: For creating standardized Next.js 16 applications with proper component architecture
- `test-generator-framework`: Core test generation framework
- `nextjs-pr-workflow`: For creating PRs after completing tests
- `coverage-readme-workflow`: For updating README with coverage badges
- `git-issue-creator`: For creating issues and branches for new features
- `linting-workflow`: For ensuring code quality before testing
