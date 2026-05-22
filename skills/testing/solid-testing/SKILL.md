---
name: solid-testing
description: "SolidJS testing patterns: use Vitest with @solidjs/testing-library, createRoot for cleanup, render components with function syntax, test user interactions and async behavior."
metadata:
  globs:
    - "**/*.test.*"
    - "**/*.spec.*"
    - "**/__tests__/**/*"
---

# SolidJS Testing Patterns

## Setup

### Packages

Install testing dependencies:

```bash
npm install -D vitest jsdom @solidjs/testing-library @testing-library/user-event @testing-library/jest-dom
```

### Configuration

**package.json:**
```json
{
  "scripts": {
    "test": "vitest"
  }
}
```

**vitest.config.ts (SolidStart):**
```ts
import solid from "vite-plugin-solid";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [solid()],
  resolve: {
    conditions: ["development", "browser"],
  },
});
```

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "types": ["vite/client", "@testing-library/jest-dom"]
  }
}
```

## Basic Component Testing

### Render Component

`render` from `@solidjs/testing-library` requires a **function** that returns JSX:

```tsx
import { render } from "@solidjs/testing-library";

// ✅ Correct - function syntax
const { getByRole } = render(() => <Counter />);

// ❌ Wrong - direct JSX
const { getByRole } = render(<Counter />);
```

### Test User Interactions

```tsx
import { test, expect } from "vitest";
import { render } from "@solidjs/testing-library";
import userEvent from "@testing-library/user-event";
import { Counter } from "./Counter";

const user = userEvent.setup();

test("increments value", async () => {
  const { getByRole } = render(() => <Counter />);
  const button = getByRole("button");
  
  expect(button).toHaveTextContent("1");
  await user.click(button);
  expect(button).toHaveTextContent("2");
});
```

## Queries

### Query Types

**Prefixes:**
- `getBy*`: Synchronous, throws if not found or multiple matches
- `getAllBy*`: Synchronous, throws if not found, returns array
- `queryBy*`: Synchronous, returns null if not found
- `queryAllBy*`: Synchronous, returns array (may be empty)
- `findBy*`: Asynchronous, waits up to 1000ms, throws if not found
- `findAllBy*`: Asynchronous, waits up to 1000ms, returns array

**When to use:**
- Default: `getBy*`
- Multiple elements: `getAllBy*`
- Lazy-loaded routes/resources: `findBy*` (first query)
- Testing absence: `queryAllBy*` (check for empty array)

### Query Suffixes (Priority Order)

1. **Role** - ARIA roles (semantic elements like `<button>`)
2. **LabelText** - Labels, aria-label, aria-labelledby
3. **PlaceholderText** - Input placeholders
4. **Text** - Text content (even if split)
5. **DisplayValue** - Form element values
6. **AltText** - Image alt text
7. **Title** - HTML title attribute
8. **TestId** - `data-testid` (last resort, not accessible)

## Testing Patterns

### Testing with Context

Use `wrapper` option to provide context:

```tsx
import { render } from "@solidjs/testing-library";

const wrapper = (props) => <DataContext value="test" {...props} />;

test("receives data from context", () => {
  const { getByText } = render(() => <DataConsumer />, { wrapper });
  expect(getByText("test")).toBeInTheDocument();
});
```

### Testing Routes

Use `location` option for routing tests. First query must be `findBy*`:

```tsx
const { findByText } = render(
  () => <Route path="/article/:id" component={Article} />,
  { location: "/article/12345" }
);

const heading = await findByText("Article Title");
```

### Testing Portals

Use `screen` export to query portal content:

```tsx
import { render, screen } from "@solidjs/testing-library";

test("toast renders in portal", () => {
  render(() => <Toast><p>Message</p></Toast>);
  const toast = screen.getByRole("log");
  expect(toast).toHaveTextContent("Message");
});
```

### Testing Async Behavior

For Suspense/async data, use `findBy*`:

```tsx
test("loads async data", async () => {
  const { findByText } = render(() => <DataComponent />);
  const content = await findByText("Loaded data");
  expect(content).toBeInTheDocument();
});
```

## createRoot for Testing

Always use `createRoot` for proper cleanup in tests:

```tsx
import { createRoot } from "solid-js";

test("counter works", () => {
  createRoot((dispose) => {
    const { count, increment } = createCounter();
    expect(count()).toBe(0);
    increment();
    expect(count()).toBe(1);
    dispose(); // Clean up
  });
});
```

## Testing Primitives

Test primitives outside components with `createRoot`:

```tsx
import { createRoot, createSignal } from "solid-js";

test("signal updates", () => {
  createRoot((dispose) => {
    const [count, setCount] = createSignal(0);
    expect(count()).toBe(0);
    setCount(5);
    expect(count()).toBe(5);
    dispose();
  });
});
```

## Best Practices

1. **Always use function syntax with render**: `render(() => <Component />)`
2. **Use createRoot for cleanup**: Ensures proper disposal in tests
3. **Prioritize accessible queries**: Role > LabelText > Text > TestId
4. **Use findBy* for async**: When testing Suspense, routes, or resources
5. **Use screen for portals**: Query portal content with `screen` export
6. **Test user interactions**: Use `userEvent` for realistic interactions
7. **Use wrapper for context**: Provide context via `wrapper` option
8. **Test accessibility**: Use role-based queries to ensure accessibility

