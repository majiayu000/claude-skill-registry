---
name: test-generator
description: Generate unit and integration tests for API routes, utilities, React components, and hooks. Use when asked to generate tests, write unit tests, create integration tests, add test coverage, or test a component/route/function.
---

# Test Generator

Before generating any output, read `config/defaults.md` and adapt all patterns, imports, and code examples to the user's configured stack.

## Process

1. Read the source file to understand its exports, dependencies, and behavior.
2. Identify the source type: API route, utility function, React component, or hook.
3. Generate test cases covering: happy path, edge cases, error handling, boundary values.
4. Write the test file using Vitest syntax (fall back to Jest if the project uses it).
5. Include proper mocking, setup/teardown, and descriptive test names.

## File Naming and Placement

- Place test file adjacent to source: `foo.ts` → `foo.test.ts`, `Foo.tsx` → `Foo.test.tsx`.
- If the project uses a `__tests__/` directory convention, follow that instead.
- For API route tests: `app/api/users/route.ts` → `app/api/users/route.test.ts`.

## Testing API Routes

Analyze the route handler and generate tests for each HTTP method.

```typescript
// Source: app/api/users/route.ts (POST handler)

// Test: app/api/users/route.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { POST } from "./route";
import { prisma } from "@/lib/prisma";

vi.mock("@/lib/prisma", () => ({
  prisma: {
    user: {
      create: vi.fn(),
      findUnique: vi.fn(),
    },
  },
}));

describe("POST /api/users", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should create a user and return 201", async () => {
    const mockUser = { id: "1", email: "test@example.com", name: "Test" };
    vi.mocked(prisma.user.create).mockResolvedValue(mockUser);

    const request = new Request("http://localhost/api/users", {
      method: "POST",
      body: JSON.stringify({ email: "test@example.com", name: "Test" }),
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(201);
    expect(data).toEqual(mockUser);
  });

  it("should return 400 when email is missing", async () => {
    const request = new Request("http://localhost/api/users", {
      method: "POST",
      body: JSON.stringify({ name: "Test" }),
    });

    const response = await POST(request);
    expect(response.status).toBe(400);
  });

  it("should return 409 when email already exists", async () => {
    vi.mocked(prisma.user.create).mockRejectedValue(
      new Error("Unique constraint failed on the fields: (`email`)")
    );

    const request = new Request("http://localhost/api/users", {
      method: "POST",
      body: JSON.stringify({ email: "taken@example.com", name: "Test" }),
    });

    const response = await POST(request);
    expect(response.status).toBe(409);
  });

  it("should return 500 on unexpected error", async () => {
    vi.mocked(prisma.user.create).mockRejectedValue(new Error("DB down"));

    const request = new Request("http://localhost/api/users", {
      method: "POST",
      body: JSON.stringify({ email: "test@example.com", name: "Test" }),
    });

    const response = await POST(request);
    expect(response.status).toBe(500);
  });
});
```

### API Route Test Checklist

- [ ] Each HTTP method has at least one happy path test
- [ ] Invalid request body returns 400
- [ ] Missing/invalid auth returns 401
- [ ] Forbidden access returns 403
- [ ] Resource not found returns 404
- [ ] Duplicate/conflict returns 409
- [ ] Unexpected errors return 500 (not leak stack traces)

## Testing Utility Functions

Focus on pure logic, null/undefined handling, and thrown errors.

```typescript
// Source: lib/utils/slugify.ts

// Test: lib/utils/slugify.test.ts
import { describe, it, expect } from "vitest";
import { slugify } from "./slugify";

describe("slugify", () => {
  it("should convert a simple string to slug", () => {
    expect(slugify("Hello World")).toBe("hello-world");
  });

  it("should handle special characters", () => {
    expect(slugify("Héllo & Wörld!")).toBe("hello-world");
  });

  it("should collapse multiple hyphens", () => {
    expect(slugify("foo---bar")).toBe("foo-bar");
  });

  it("should trim leading and trailing hyphens", () => {
    expect(slugify("-hello-")).toBe("hello");
  });

  it("should return empty string for empty input", () => {
    expect(slugify("")).toBe("");
  });

  it("should handle null/undefined gracefully", () => {
    expect(slugify(null as unknown as string)).toBe("");
  });
});
```

## Testing React Components

Use React Testing Library. Prefer `getByRole` over `getByTestId`.

```tsx
// Test: components/LoginForm.test.tsx
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { LoginForm } from "./LoginForm";

describe("LoginForm", () => {
  it("should render email and password fields", () => {
    render(<LoginForm onSubmit={vi.fn()} />);

    expect(screen.getByRole("textbox", { name: /email/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });

  it("should call onSubmit with form values", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(<LoginForm onSubmit={onSubmit} />);

    await user.type(screen.getByRole("textbox", { name: /email/i }), "a@b.com");
    await user.type(screen.getByLabelText(/password/i), "secret123");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    expect(onSubmit).toHaveBeenCalledWith({
      email: "a@b.com",
      password: "secret123",
    });
  });

  it("should show validation error for invalid email", async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={vi.fn()} />);

    await user.type(screen.getByRole("textbox", { name: /email/i }), "bad");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    expect(screen.getByRole("alert")).toHaveTextContent(/valid email/i);
  });

  it("should disable submit button while loading", () => {
    render(<LoginForm onSubmit={vi.fn()} isLoading />);

    expect(screen.getByRole("button", { name: /sign in/i })).toBeDisabled();
  });
});
```

### Component Test Checklist

- [ ] Renders without crashing
- [ ] Displays correct content based on props
- [ ] Interactive elements respond to user events
- [ ] Conditional rendering works for all states (loading, error, empty, success)
- [ ] Accessible: interactive elements have roles and labels
- [ ] Form submission calls handler with correct values
- [ ] Error states display properly

## Testing Hooks

Wrap custom hooks with `renderHook` from React Testing Library.

```typescript
// Test: hooks/useDebounce.test.ts
import { describe, it, expect, vi } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { useDebounce } from "./useDebounce";

describe("useDebounce", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("should return initial value immediately", () => {
    const { result } = renderHook(() => useDebounce("hello", 500));
    expect(result.current).toBe("hello");
  });

  it("should debounce value updates", () => {
    const { result, rerender } = renderHook(
      ({ value }) => useDebounce(value, 500),
      { initialProps: { value: "hello" } }
    );

    rerender({ value: "world" });
    expect(result.current).toBe("hello"); // not yet updated

    act(() => { vi.advanceTimersByTime(500); });
    expect(result.current).toBe("world"); // now updated
  });

  it("should cancel previous timer on rapid updates", () => {
    const { result, rerender } = renderHook(
      ({ value }) => useDebounce(value, 500),
      { initialProps: { value: "a" } }
    );

    rerender({ value: "b" });
    act(() => { vi.advanceTimersByTime(300); });
    rerender({ value: "c" });
    act(() => { vi.advanceTimersByTime(500); });

    expect(result.current).toBe("c"); // skipped "b"
  });
});
```

## Mocking Patterns

### Mock a module

```typescript
vi.mock("@/lib/prisma", () => ({
  prisma: { user: { findMany: vi.fn() } },
}));
```

### Mock next/navigation

```typescript
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn(), back: vi.fn() }),
  useSearchParams: () => new URLSearchParams("q=test"),
  usePathname: () => "/dashboard",
}));
```

### Mock fetch

```typescript
const mockFetch = vi.fn();
global.fetch = mockFetch;

mockFetch.mockResolvedValueOnce({
  ok: true,
  json: () => Promise.resolve({ data: "test" }),
});
```

## Test Naming Convention

Use descriptive names following the pattern: `should [expected behavior] when [condition]`.

- `should return 401 when auth token is missing`
- `should render loading spinner when data is fetching`
- `should throw TypeError when input is not a string`

## Output Format

```
## Generated Tests

**Source**: `path/to/source.ts`
**Test file**: `path/to/source.test.ts`
**Framework**: Vitest

### Test Cases
| # | Test | Category |
|---|------|----------|
| 1 | should ... | Happy path |
| 2 | should ... | Edge case |
| 3 | should ... | Error handling |

[Generated code block]

### Coverage Notes
- [Any areas that need additional manual test cases]
```

## Verification Loop

After generating tests, run them with the project's test runner. If any test fails due to a generation error (not a legitimate bug), analyze the failure, fix the test, and re-run. Repeat up to 3 times. If a test fails because it caught a real bug in the source code, flag it clearly in the output: `REAL BUG FOUND: [description]`. Only deliver tests that either pass or explicitly flag real bugs.

## Reference

See [references/testing-patterns.md](references/testing-patterns.md) for Vitest setup, Prisma mocking, and MSW patterns.
