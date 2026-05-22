---
name: testing-quality-gates
description: Comprehensive testing protocols, E2E patterns, and quality gate execution for the omer-akben portfolio. Use when writing tests, debugging test failures, or ensuring code quality.
---

# Testing & Quality Gates Skill

## Test Execution Commands

### Unit Tests (Vitest)

```bash
npm test                                      # Run all unit tests
npm test -- --watch                           # TDD mode (watch for changes)
npm test -- global-chat-button.test.tsx      # Run specific test file
npm run test:ui                              # Visual test UI
```typescript

### E2E Tests (Playwright)

```bash
npm run test:e2e                             # Run all E2E tests
npm run test:e2e -- agentic-sidebar.spec.ts # Run specific E2E test
npm run test:e2e -- --headed                 # Run with browser visible
npm run test:e2e -- --debug                  # Debug mode with inspector
```typescript

### Quality Gates

```bash
npm run lint           # ESLint check
npx tsc --noEmit      # TypeScript check
npm run build         # Production build
npm run size          # Bundle size analysis
```typescript

## Testing Protocols

### Unit Test Structure (Vitest)

**Location:** Tests colocated with components (e.g., `component.test.tsx`)

### Patterns

- Use `describe` blocks for component grouping
- Test user interactions with `userEvent` from `@testing-library/user-event`
- Mock Next.js hooks and router with `jest.mock`
- Test accessibility with `screen.getByRole`, `getByLabelText`

### Example Pattern

```typescript
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, beforeEach, vi } from "vitest";

describe("ComponentName", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should render correctly", () => {
    render(<ComponentName />);
    expect(screen.getByRole("button")).toBeInTheDocument();
  });

  it("should handle user interaction", async () => {
    const user = userEvent.setup();
    render(<ComponentName />);
    await user.click(screen.getByRole("button"));
    expect(mockFunction).toHaveBeenCalled();
  });
});
```typescript

### E2E Test Structure (Playwright)

**Location:** `e2e/*.spec.ts`

### Critical Patterns

- **Wait for hydration** - Use `page.waitForSelector` for dynamic content
- **Network monitoring** - Use `page.waitForResponse` for API calls
- **Viewport testing** - Test at multiple screen sizes
- **Accessibility** - Use `page.getByRole`, `page.getByLabel`

### Example Pattern

```typescript
import { test, expect } from "@playwright/test";

test.describe("Feature Name", () => {
  test("should complete user flow", async ({ page }) => {
    await page.goto("/");

    // Wait for hydration (critical for Next.js SSR)
    await page.waitForSelector('[data-testid="hydrated-component"]');

    // Interact with UI
    await page.getByRole("button", { name: "Open Chat" }).click();

    // Assert results
    await expect(page.getByRole("dialog")).toBeVisible();
  });
});
```typescript

### Hydration Testing for Next.js SSR

**Critical Rule:** E2E tests must wait for client-side hydration before interactions.

### Pattern

```typescript
// Add data-testid after component mounts
const [isHydrated, setIsHydrated] = useState(false);

useEffect(() => {
  setIsHydrated(true);
}, []);

return (
  <div data-testid={isHydrated ? "hydrated-component" : undefined}>
    {/* Component content */}
  </div>
);
```typescript

### Test

```typescript
await page.waitForSelector('[data-testid="hydrated-component"]');
await page.getByRole("button").click();
```typescript

## Test Coverage Requirements

### Current Coverage (January 2025)

### Unit Tests

- Total: 776 tests passing
- Focus: Component behavior, state management, tool validation
- Critical areas: Chat system (32 tests), AI tools (15+ tests per tool)

### E2E Tests

- Total: 66 passing, 14 skipped
- Focus: User journeys, cross-component interactions
- Critical flows: Chat sidebar, navigation, responsive layouts

### Coverage Goals

- **New features:** 100% unit test coverage for logic
- **UI components:** Test user interactions and accessibility
- **API routes:** Test validation, success, and error cases
- **E2E:** Cover primary user journeys

## Common Testing Patterns

### React Hook Testing

```typescript
// All hooks must be called before conditional returns
const [state, setState] = useState(false);
const mounted = useIsMounted();

// Effect dependencies must include all state that affects behavior
useEffect(() => {
  if (state) {
    // Effect logic
  }
}, [state]); // ✓ state included in dependencies
```typescript

### AI Tool Testing

```typescript
describe("Tool API Route", () => {
  it("should validate input schema", async () => {
    const invalidInput = { /* missing required fields */ };
    const response = await POST(new Request(url, {
      method: "POST",
      body: JSON.stringify(invalidInput)
    }));
    expect(response.status).toBe(400);
  });

  it("should return correct response format", async () => {
    const validInput = { /* valid fields */ };
    const response = await POST(new Request(url, {
      method: "POST",
      body: JSON.stringify(validInput)
    }));
    const data = await response.json();
    expect(data).toMatchObject(expectedShape);
  });
});
```typescript

### Brightness Mode Testing

**Critical:** Test all 8 brightness modes (-3 to +3, auto)

```typescript
describe("Component with brightness modes", () => {
  [-3, -2, -1, 0, 1, 2, 3, "auto"].forEach((mode) => {
    it(`should render correctly in brightness mode ${mode}`, () => {
      render(<Component />, { brightness: mode });
      // Assert appearance
    });
  });
});
```typescript

## Debugging Test Failures

### Unit Test Failures

1. Check mock implementations are up to date
2. Verify hook dependencies arrays include all state
3. Ensure no conditional returns before hooks
4. Check for timing issues with async operations

### E2E Test Failures

1. **Hydration mismatch:** Add data-testid after mount
2. **Element not found:** Wait for selector before interaction
3. **Timeout:** Increase timeout for slow API calls
4. **Flaky tests:** Add explicit waits for network responses

### Common Error Patterns

**Error:** "Cannot read property 'X' of undefined"
**Fix:** Add null checks or wait for data to load

**Error:** "Element is not clickable"
**Fix:** Wait for element to be visible and enabled

**Error:** "Test timeout exceeded"
**Fix:** Add `page.waitForResponse()` for API calls

## Quality Gate Failure Resolution

### ESLint Failures

- Run `npm run lint` to see all issues
- Many can be auto-fixed with `npm run lint -- --fix`
- Review ESLint rules in `eslint.config.mjs`

### TypeScript Failures

- Run `npx tsc --noEmit` to see all type errors
- Fix type mismatches, missing properties, incorrect generics
- Never use `@ts-ignore` - fix root cause

### Build Failures

- Check for runtime errors in components
- Verify all imports are correct
- Ensure environment variables are defined

### Bundle Size Failures

- Run `npm run analyze` to see bundle composition
- Use dynamic imports for large dependencies
- Verify tree-shaking is working correctly

## Test-Driven Development (TDD) Workflow

1. **Write failing test** - Define expected behavior
2. **Run test** - Confirm it fails for right reason
3. **Write minimal code** - Make test pass
4. **Refactor** - Clean up while tests remain green
5. **Repeat** - Continue with next test

```bash
# Terminal 1: Watch mode
npm test -- --watch

# Terminal 2: Development
npm run dev
```typescript

## Production-Ready Checklist

Before merging to `pre-deployment`:

- [ ] All unit tests pass (776/776)
- [ ] All E2E tests pass (66/66)
- [ ] No ESLint errors or warnings
- [ ] No TypeScript errors
- [ ] Production build succeeds
- [ ] Bundle size within limits
- [ ] Test coverage maintained or improved
- [ ] Hydration mismatches resolved
