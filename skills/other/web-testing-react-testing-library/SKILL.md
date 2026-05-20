---
name: web-testing-react-testing-library
description: React Testing Library patterns - query hierarchy, userEvent, async utilities, renderHook, custom render with providers, accessibility-first testing
---

# React Testing Library Patterns

> **Quick Guide:** Test React components through user interactions and accessible queries. Use `getByRole` as your primary query. Prefer `userEvent` over `fireEvent`. Use `findBy*` for async content. Test user behavior, not implementation details.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the query priority hierarchy: `getByRole` > `getByLabelText` > `getByText` > `getByTestId`)**

**(You MUST use `userEvent` instead of `fireEvent` for realistic user interactions)**

**(You MUST use `findBy*` queries for async content instead of `waitFor` + `getBy*`)**

**(You MUST test user-visible behavior, NOT implementation details like internal state)**

**(You MUST use `screen` object for queries, NOT destructured render returns)**

</critical_requirements>

---

**Auto-detection:** React Testing Library, @testing-library/react, render, screen, userEvent, fireEvent, waitFor, findBy, getByRole, getByLabelText, renderHook, within, cleanup, prettyDOM, configure, logRoles, logTestingPlaygroundURL

**When to use:**

- Testing React component behavior through user interactions
- Verifying accessible element rendering and presence
- Testing form interactions, validation, and submissions
- Testing async component states (loading, error, success)
- Testing custom React hooks with `renderHook`
- Creating custom render functions with providers

**When NOT to use:**

- E2E testing spanning multiple pages (defer to your E2E testing tool)
- Network request mocking setup (defer to your API mocking solution)
- Testing pure utility functions without React (use unit tests directly)
- Test runner configuration (defer to your test runner skill)

**Key patterns covered:**

- Query hierarchy and selection strategy
- userEvent vs fireEvent for user simulation
- Async utilities (waitFor, findBy queries)
- Testing hooks with renderHook
- Custom render with providers
- Accessibility testing patterns
- Debug utilities (screen.debug, prettyDOM, logRoles)
- Scoped queries with `within`
- Global configuration options

**Detailed Resources:**

- For code examples, see `examples/` folder:
  - [examples/core.md](examples/core.md) - Query hierarchy examples
  - [examples/user-events.md](examples/user-events.md) - userEvent patterns
  - [examples/async-testing.md](examples/async-testing.md) - findBy, waitFor, waitForElementToBeRemoved
  - [examples/custom-render.md](examples/custom-render.md) - Custom render with providers
  - [examples/hooks.md](examples/hooks.md) - renderHook patterns
  - [examples/accessibility.md](examples/accessibility.md) - Accessibility testing patterns
  - [examples/debugging.md](examples/debugging.md) - Debug utilities and snapshot testing
  - [examples/scoped-queries.md](examples/scoped-queries.md) - within() for scoped queries
  - [examples/configuration.md](examples/configuration.md) - Global configuration options
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

React Testing Library is built on the guiding principle: "The more your tests resemble the way your software is used, the more confidence they can give you."

**Core Principles:**

1. **Test User Behavior, Not Implementation**: Query elements the way users find them (by role, label, text), not by test IDs or CSS selectors
2. **Accessibility-First Testing**: If your test struggles to find an element, your UI likely has accessibility issues
3. **No Implementation Details**: Avoid testing internal state, refs, or component internals - test what users see and interact with
4. **Real DOM Interactions**: Render components to a real DOM (jsdom) to catch real integration issues

**When to use React Testing Library:**

- Integration testing components with their children
- Testing user interaction flows within a component
- Verifying accessibility of interactive elements
- Testing form validation and submission
- Testing conditional rendering based on props/state

**When NOT to use:**

- Full user journey testing (use E2E tests)
- Testing visual appearance (use visual regression tools)
- Testing network requests directly (test component behavior with mocked responses)
- Testing third-party library behavior (trust the library's tests)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Query Priority Hierarchy

Select queries based on accessibility hierarchy. This ensures tests align with how users (including those using assistive technology) interact with your UI.

#### Query Priority Order

```typescript
// Priority 1: Accessible to Everyone
getByRole(); // BEST - queries accessibility tree
getByLabelText(); // Form fields - how users navigate forms
getByPlaceholderText(); // When no label (not ideal, but sometimes necessary)
getByText(); // Non-interactive content (divs, spans, paragraphs)
getByDisplayValue(); // Form elements by current value

// Priority 2: Semantic Queries
getByAltText(); // Images, areas, inputs with alt
getByTitle(); // Least reliable - not consistently read by screen readers

// Priority 3: Test IDs (Last Resort)
getByTestId(); // Only when other methods fail
```

See [examples/core.md](examples/core.md) for complete query examples.

**Why this hierarchy:** Users interact with your app through visible text, labels, and semantic roles - not through test IDs or CSS classes. Testing this way ensures your app is accessible.

---

### Pattern 2: userEvent Over fireEvent

Use `userEvent` for realistic user interaction simulation. It triggers the full event chain that real interactions produce.

#### Key Differences

| Action   | `fireEvent`           | `userEvent`                                                 |
| -------- | --------------------- | ----------------------------------------------------------- |
| Typing   | Single `change` event | `keyDown`, `keyPress`, `keyUp` per character                |
| Clicking | Single `click` event  | `pointerDown`, `mouseDown`, `pointerUp`, `mouseUp`, `click` |
| Focus    | Manual management     | Automatic focus management                                  |

#### Setup Pattern (userEvent v14+)

```typescript
import userEvent from "@testing-library/user-event";

// Setup BEFORE interactions - creates isolated user session
const user = userEvent.setup();

// Then use throughout test
await user.click(button);
await user.type(input, "Hello");
```

See [examples/user-events.md](examples/user-events.md) for complete userEvent examples.

**Why userEvent:** `fireEvent` dispatches DOM events directly, bypassing browser event handling. `userEvent` simulates actual user behavior, triggering the complete event chain including focus, keyboard, and pointer events.

---

### Pattern 3: Async Utilities

Use `findBy*` queries for elements that appear asynchronously. Use `waitFor` only for assertions, not element queries.

#### findBy vs waitFor

```typescript
// GOOD: findBy for async elements
const button = await screen.findByRole("button", { name: /submit/i });

// BAD: waitFor + getBy for async elements
await waitFor(() => {
  screen.getByRole("button", { name: /submit/i }); // DON'T DO THIS
});
```

#### waitFor Best Practices

```typescript
// GOOD: Single assertion in waitFor
await waitFor(() => {
  expect(screen.getByText(/success/i)).toBeInTheDocument();
});

// BAD: Multiple assertions in waitFor
await waitFor(() => {
  expect(screen.getByText(/success/i)).toBeInTheDocument();
  expect(screen.getByText(/complete/i)).toBeInTheDocument(); // DON'T
});

// BAD: Side effects in waitFor
await waitFor(() => {
  user.click(button); // DON'T - side effects outside waitFor
  expect(result).toBe(true);
});
```

See [examples/async-testing.md](examples/async-testing.md) for complete async testing examples.

**Why this matters:** `waitFor` polls until the callback stops throwing. Multiple assertions or side effects in the callback cause unpredictable behavior and slower test failures.

---

### Pattern 4: Testing Hooks with renderHook

Use `renderHook` for testing custom hooks in isolation. Prefer testing hooks through components when possible.

#### Basic renderHook Usage

```typescript
import { renderHook, act } from "@testing-library/react";

const { result } = renderHook(() => useCounter());

// Access current value
expect(result.current.count).toBe(0);

// Update state with act()
act(() => {
  result.current.increment();
});

expect(result.current.count).toBe(1);
```

#### With Context Providers

```typescript
const wrapper = ({ children }: { children: React.ReactNode }) => (
  <ThemeProvider theme="dark">{children}</ThemeProvider>
);

const { result } = renderHook(() => useTheme(), { wrapper });
```

See [examples/hooks.md](examples/hooks.md) for complete renderHook examples.

**When to use renderHook:**

- Testing library hooks you're publishing
- Testing complex hook logic in isolation
- Testing hooks with many edge cases

**When to prefer component testing:**

- The hook is tightly coupled to UI
- You want to test the hook in realistic context
- The component test is simpler to write

---

### Pattern 5: Custom Render with Providers

Create a custom render function that wraps components with all necessary providers.

#### Custom Render Setup

```typescript
// test-utils.tsx
import { render, type RenderOptions } from "@testing-library/react";
import type { ReactElement } from "react";

// Import your providers
// import { ThemeProvider } from "./theme-context";
// import { QueryClientProvider } from "@tanstack/react-query";

interface AllProvidersProps {
  children: React.ReactNode;
}

function AllProviders({ children }: AllProvidersProps) {
  // Replace with your actual providers
  return <>{children}</>;

  // Example with providers:
  // return (
  //   <ThemeProvider>
  //     <QueryClientProvider client={queryClient}>
  //       {children}
  //     </QueryClientProvider>
  //   </ThemeProvider>
  // );
}

function customRender(
  ui: ReactElement,
  options?: Omit<RenderOptions, "wrapper">
) {
  return render(ui, { wrapper: AllProviders, ...options });
}

// Re-export everything
export * from "@testing-library/react";
export { customRender as render };
```

See [examples/custom-render.md](examples/custom-render.md) for complete custom render examples.

**Why custom render:** Avoids repeating provider boilerplate in every test. Creates a consistent test environment matching your app.

---

### Pattern 6: Accessibility Testing Patterns

Use queries that enforce accessibility. If your test struggles to find an element, your UI likely has accessibility issues.

#### Role-Based Queries

```typescript
// GOOD: Tests that element is accessible
screen.getByRole("button", { name: /submit/i });
screen.getByRole("textbox", { name: /email/i });
screen.getByRole("checkbox", { name: /agree to terms/i });
screen.getByRole("combobox", { name: /country/i });

// GOOD: Verify accessible names
expect(screen.getByRole("button", { name: /submit/i })).toBeEnabled();

// BAD: Using test IDs when accessible queries work
screen.getByTestId("submit-button"); // DON'T when getByRole works
```

#### logRoles for Debugging

```typescript
import { logRoles } from "@testing-library/react";

// Log all accessible roles in a container
logRoles(container);
```

See [examples/accessibility.md](examples/accessibility.md) for complete accessibility testing examples.

**Why this matters:** Screen readers and assistive technologies use the accessibility tree. Testing with accessible queries ensures your app works for all users.

---

### Pattern 7: Debug Utilities

Use debug utilities to understand what's rendered and troubleshoot failing tests.

#### screen.debug()

```typescript
// Debug entire document
screen.debug();

// Debug specific element
screen.debug(screen.getByRole("form"));

// Debug multiple elements
screen.debug(screen.getAllByRole("listitem"));
```

#### prettyDOM for Custom Output

```typescript
import { prettyDOM } from "@testing-library/react";

// Get formatted DOM string (for logging, assertions)
const domString = prettyDOM(element);
console.log(domString);

// Customize output length
const domString = prettyDOM(element, 15000); // Increase from 7000 default
```

#### logTestingPlaygroundURL

```typescript
import { logTestingPlaygroundURL } from "@testing-library/react";

// Logs URL to Testing Playground with current DOM
logTestingPlaygroundURL();
// Visit the URL to get suggested queries
```

See [examples/debugging.md](examples/debugging.md) for complete debug examples.

**When to use debug:**

- Test is failing and you don't understand why
- Element can't be found with expected query
- Need to understand current DOM state

**Remove before committing:** Debug statements are for development only.

---

### Pattern 8: Scoped Queries with within

Use `within` to scope queries to a specific container element. Essential when testing components with repeated structures.

#### Basic Usage

```typescript
import { render, screen, within } from "@testing-library/react";

test("selects item in specific section", () => {
  render(<Dashboard />);

  // Get a specific section
  const sidebar = screen.getByRole("navigation");

  // Query only within that section
  const homeLink = within(sidebar).getByRole("link", { name: /home/i });
  expect(homeLink).toBeInTheDocument();
});
```

#### Testing List Items

```typescript
test("each row has edit button", () => {
  render(<UserTable users={mockUsers} />);

  const rows = screen.getAllByRole("row");

  // Skip header row, check each data row
  rows.slice(1).forEach((row) => {
    const editButton = within(row).getByRole("button", { name: /edit/i });
    expect(editButton).toBeInTheDocument();
  });
});
```

See [examples/scoped-queries.md](examples/scoped-queries.md) for complete within() examples.

**When to use within:**

- Components with repeated structures (tables, lists, cards)
- Multiple sections with similar elements
- Testing specific regions of a page

---

### Pattern 9: Global Configuration

Configure Testing Library defaults for your project using `configure`.

#### Configuration Options

```typescript
import { configure } from "@testing-library/react";

// In test setup file
configure({
  // Custom test ID attribute (default: "data-testid")
  testIdAttribute: "data-test-id",

  // Async utility timeout (default: 1000ms)
  asyncUtilTimeout: 5000,

  // Enable React strict mode warnings in tests
  reactStrictMode: true,
});
```

#### userEvent Setup Options

```typescript
import userEvent from "@testing-library/user-event";

// With fake timers (Vitest/Jest)
const user = userEvent.setup({
  advanceTimers: vi.advanceTimersByTime, // Required for fake timers
});

// Skip pointer events check (for elements with pointer-events: none)
const user = userEvent.setup({
  pointerEventsCheck: 0, // 0 = never check, 1 = check once, 2 = check per API
});

// Custom delay between events
const user = userEvent.setup({
  delay: null, // null = no delay (faster tests)
});
```

See [examples/configuration.md](examples/configuration.md) for complete configuration examples.

**When to configure:**

- Project uses custom test ID attribute
- Tests need longer async timeouts
- Using fake timers with userEvent

</patterns>

---

<integration>

## Integration Guide

**Works with your test runner:**

- Configure test setup file to import `@testing-library/jest-dom` for semantic matchers
- Use your test runner's lifecycle hooks for cleanup if not automatic

**Works with your mocking solution:**

- Use network-level mocking to test loading/error/success states
- Mock responses before rendering, not after

**Works with your React framework:**

- Custom render wraps with framework-specific providers
- SSR frameworks may need additional configuration

</integration>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Using `getByTestId` when accessible queries work** - Indicates UI may not be accessible, test doesn't reflect user experience
- **Using `waitFor` to find elements** - Use `findBy*` instead, produces better error messages and cleaner code
- **Using `fireEvent` for user interactions** - Use `userEvent` for realistic event chains
- **Multiple assertions in single `waitFor`** - Causes slow test failures and unpredictable behavior
- **Testing internal component state** - Test user-visible behavior, not implementation details

**Medium Priority Issues:**

- **Destructuring render return instead of using `screen`** - `screen` provides cleaner, more maintainable code
- **Manual `cleanup` calls** - Modern frameworks handle cleanup automatically
- **Wrapping `render` or `fireEvent` in `act()`** - They already wrap in `act`, double-wrapping is unnecessary
- **Using `querySelector` or CSS selectors** - Use Testing Library queries for accessibility-aligned tests

**Common Mistakes:**

- Forgetting to `await` userEvent methods (all are async in v14+)
- Using `getBy*` for elements that appear asynchronously
- Putting side effects inside `waitFor` callbacks
- Not setting up userEvent before interactions (`const user = userEvent.setup()`)

**Gotchas & Edge Cases:**

- `userEvent.setup()` must be called before any interactions (v14+ requirement)
- `queryBy*` returns `null` for missing elements (use for absence assertions only)
- `findBy*` has default timeout of 1000ms (configurable via options)
- `result.current` in renderHook is a ref - value updates on each access
- Empty `waitFor(() => {})` creates fragile timing-dependent tests

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use the query priority hierarchy: `getByRole` > `getByLabelText` > `getByText` > `getByTestId`)**

**(You MUST use `userEvent` instead of `fireEvent` for realistic user interactions)**

**(You MUST use `findBy*` queries for async content instead of `waitFor` + `getBy*`)**

**(You MUST test user-visible behavior, NOT implementation details like internal state)**

**(You MUST use `screen` object for queries, NOT destructured render returns)**

**Failure to follow these rules will produce brittle tests that don't reflect real user interactions and miss accessibility issues.**

</critical_reminders>
