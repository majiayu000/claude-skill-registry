---
name: testing-automation
description: Comprehensive testing patterns for Next.js 16 applications including unit tests with Vitest, integration tests, E2E tests with Playwright, component testing, and coverage reporting. Use when user wants to write tests, set up testing infrastructure, debug test failures, or implement test-driven development.
---

# Testing Automation Skill

Complete guide for implementing automated tests in The Simpsons API project using Vitest for unit/integration tests and Playwright for E2E tests.

## When to Use This Skill

Use this skill when the user requests:

✅ **Primary Use Cases**

- "Write tests for this"
- "Add unit tests"
- "Create E2E tests"
- "Set up testing"
- "Fix failing tests"
- "Improve test coverage"

✅ **Secondary Use Cases**

- "Mock this function"
- "Test this component"
- "Add integration tests"
- "Debug test failure"
- "Set up CI testing"
- "Generate coverage report"

❌ **Do NOT use when**

- Manual UI testing (use webapp-testing skill)
- Production debugging (use logging/monitoring)
- Performance testing only (use performance-optimization skill)
- Security testing (use security-specific tools)

---

## Testing Stack

| Type            | Tool                     | Config File          |
| --------------- | ------------------------ | -------------------- |
| Unit Tests      | Vitest                   | vitest.config.ts     |
| Component Tests | Vitest + Testing Library | vitest.config.ts     |
| E2E Tests       | Playwright               | playwright.config.ts |
| Coverage        | Vitest (c8/istanbul)     | vitest.config.ts     |
| Mocking         | Vitest (vi)              | Built-in             |

---

## Part 1: Setup and Configuration

### Install Testing Dependencies

```bash
# Vitest and related packages
pnpm add -D vitest @vitejs/plugin-react jsdom
pnpm add -D @testing-library/react @testing-library/dom @testing-library/jest-dom
pnpm add -D @testing-library/user-event

# Playwright for E2E
pnpm add -D @playwright/test
pnpm exec playwright install

# Coverage
pnpm add -D @vitest/coverage-v8
```

### Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./vitest.setup.ts"],
    include: ["**/*.{test,spec}.{ts,tsx}"],
    exclude: ["node_modules", ".next", "e2e/**"],
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: [
        "node_modules/",
        ".next/",
        "**/*.d.ts",
        "**/*.config.*",
        "**/types.ts",
      ],
    },
    alias: {
      "@": path.resolve(__dirname, "./"),
    },
  },
});
```

### Vitest Setup File

```typescript
// vitest.setup.ts
import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach, vi } from "vitest";

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock Next.js router
vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    back: vi.fn(),
    forward: vi.fn(),
    refresh: vi.fn(),
    prefetch: vi.fn(),
  }),
  usePathname: () => "/",
  useSearchParams: () => new URLSearchParams(),
  useParams: () => ({}),
}));

// Mock Next.js image
vi.mock("next/image", () => ({
  default: ({ src, alt, ...props }: any) => (
    // eslint-disable-next-line @next/next/no-img-element
    <img src={src} alt={alt} {...props} />
  ),
}));
```

### Playwright Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [["html"], ["list"], process.env.CI ? ["github"] : ["line"]],
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "firefox",
      use: { ...devices["Desktop Firefox"] },
    },
    {
      name: "mobile-chrome",
      use: { ...devices["Pixel 5"] },
    },
  ],
  webServer: {
    command: "pnpm dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
```

### Package.json Scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:watch": "vitest --watch",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:headed": "playwright test --headed",
    "test:all": "vitest run && playwright test"
  }
}
```

---

## Part 2: Unit Testing Patterns

### Testing Utility Functions

```typescript
// app/_lib/utils.test.ts
import { describe, it, expect } from "vitest";
import { cn, formatDate, truncate } from "./utils";

describe("cn (classname utility)", () => {
  it("merges class names correctly", () => {
    expect(cn("foo", "bar")).toBe("foo bar");
  });

  it("handles conditional classes", () => {
    expect(cn("base", false && "hidden", true && "visible")).toBe(
      "base visible",
    );
  });

  it("handles Tailwind conflicts", () => {
    expect(cn("px-2", "px-4")).toBe("px-4");
  });
});

describe("formatDate", () => {
  it("formats date correctly", () => {
    const date = new Date("2026-01-14");
    expect(formatDate(date)).toBe("January 14, 2026");
  });

  it("handles string dates", () => {
    expect(formatDate("2026-01-14")).toBe("January 14, 2026");
  });
});

describe("truncate", () => {
  it("truncates long strings", () => {
    expect(truncate("Hello World", 5)).toBe("Hello...");
  });

  it("returns short strings unchanged", () => {
    expect(truncate("Hi", 10)).toBe("Hi");
  });
});
```

### Testing Server Actions

```typescript
// app/_actions/diary.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { addDiaryEntry } from "./diary";

// Mock dependencies
vi.mock("@/app/_lib/auth", () => ({
  getCurrentUser: vi.fn(),
}));

vi.mock("@/app/_lib/db-utils", () => ({
  execute: vi.fn(),
}));

vi.mock("next/cache", () => ({
  revalidatePath: vi.fn(),
}));

describe("addDiaryEntry", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns error when not authenticated", async () => {
    const { getCurrentUser } = await import("@/app/_lib/auth");
    vi.mocked(getCurrentUser).mockResolvedValue(null);

    const formData = new FormData();
    formData.set("characterId", "1");
    formData.set("title", "Test");
    formData.set("content", "Test content");

    const result = await addDiaryEntry(formData);

    expect(result.success).toBe(false);
    expect(result.error).toContain("log in");
  });

  it("validates required fields", async () => {
    const { getCurrentUser } = await import("@/app/_lib/auth");
    vi.mocked(getCurrentUser).mockResolvedValue({
      id: "user123",
      name: "Test",
    });

    const formData = new FormData();
    formData.set("characterId", "1");
    // Missing title and content

    const result = await addDiaryEntry(formData);

    expect(result.success).toBe(false);
    expect(result.error).toContain("required");
  });

  it("creates entry when valid", async () => {
    const { getCurrentUser } = await import("@/app/_lib/auth");
    const { execute } = await import("@/app/_lib/db-utils");
    const { revalidatePath } = await import("next/cache");

    vi.mocked(getCurrentUser).mockResolvedValue({
      id: "user123",
      name: "Test",
    });
    vi.mocked(execute).mockResolvedValue(1);

    const formData = new FormData();
    formData.set("characterId", "1");
    formData.set("title", "Test Entry");
    formData.set("content", "This is test content for the diary.");

    const result = await addDiaryEntry(formData);

    expect(result.success).toBe(true);
    expect(execute).toHaveBeenCalledWith(
      expect.stringContaining("INSERT INTO"),
      expect.arrayContaining(["user123", "1", "Test Entry"]),
    );
    expect(revalidatePath).toHaveBeenCalledWith("/diary");
  });
});
```

### Testing Repository Functions

```typescript
// app/_lib/repositories.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { findCharacterById, findAllCharacters } from "./repositories";

vi.mock("./db-utils", () => ({
  query: vi.fn(),
  queryOne: vi.fn(),
}));

describe("Character Repository", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("findCharacterById", () => {
    it("returns character when found", async () => {
      const mockCharacter = {
        id: 1,
        name: "Homer Simpson",
        occupation: "Safety Inspector",
      };

      const { queryOne } = await import("./db-utils");
      vi.mocked(queryOne).mockResolvedValue(mockCharacter);

      const result = await findCharacterById(1);

      expect(result).toEqual(mockCharacter);
      expect(queryOne).toHaveBeenCalledWith(
        expect.stringContaining("SELECT"),
        [1],
      );
    });

    it("returns null when not found", async () => {
      const { queryOne } = await import("./db-utils");
      vi.mocked(queryOne).mockResolvedValue(null);

      const result = await findCharacterById(999);

      expect(result).toBeNull();
    });
  });

  describe("findAllCharacters", () => {
    it("returns array of characters", async () => {
      const mockCharacters = [
        { id: 1, name: "Homer" },
        { id: 2, name: "Marge" },
      ];

      const { query } = await import("./db-utils");
      vi.mocked(query).mockResolvedValue(mockCharacters);

      const result = await findAllCharacters();

      expect(result).toHaveLength(2);
      expect(result[0].name).toBe("Homer");
    });
  });
});
```

---

## Part 3: Component Testing

### Testing Client Components

```typescript
// app/_components/FollowButton.test.tsx
import { describe, it, expect, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { FollowButton } from "./FollowButton";

// Mock the server action
vi.mock("@/app/_actions/social", () => ({
  toggleFollow: vi.fn(),
}));

describe("FollowButton", () => {
  it("renders follow button when not following", () => {
    render(
      <FollowButton characterId={1} initialFollowing={false} />
    );

    expect(screen.getByRole("button", { name: /follow/i })).toBeInTheDocument();
    expect(screen.queryByText(/unfollow/i)).not.toBeInTheDocument();
  });

  it("renders unfollow button when following", () => {
    render(
      <FollowButton characterId={1} initialFollowing={true} />
    );

    expect(screen.getByRole("button", { name: /unfollow/i })).toBeInTheDocument();
  });

  it("toggles state on click", async () => {
    const { toggleFollow } = await import("@/app/_actions/social");
    vi.mocked(toggleFollow).mockResolvedValue({ success: true });

    const user = userEvent.setup();
    render(
      <FollowButton characterId={1} initialFollowing={false} />
    );

    const button = screen.getByRole("button", { name: /follow/i });
    await user.click(button);

    await waitFor(() => {
      expect(screen.getByText(/unfollow/i)).toBeInTheDocument();
    });

    expect(toggleFollow).toHaveBeenCalledWith(1);
  });

  it("reverts on error", async () => {
    const { toggleFollow } = await import("@/app/_actions/social");
    vi.mocked(toggleFollow).mockResolvedValue({
      success: false,
      error: "Failed",
    });

    const user = userEvent.setup();
    render(
      <FollowButton characterId={1} initialFollowing={false} />
    );

    await user.click(screen.getByRole("button"));

    await waitFor(() => {
      // Should revert back to follow after error
      expect(screen.getByText(/follow/i)).toBeInTheDocument();
    });
  });

  it("is disabled while pending", async () => {
    const { toggleFollow } = await import("@/app/_actions/social");

    // Create a promise that we can control
    let resolveAction: (value: any) => void;
    const actionPromise = new Promise((resolve) => {
      resolveAction = resolve;
    });
    vi.mocked(toggleFollow).mockReturnValue(actionPromise as any);

    const user = userEvent.setup();
    render(
      <FollowButton characterId={1} initialFollowing={false} />
    );

    await user.click(screen.getByRole("button"));

    // Button should be disabled while action is pending
    expect(screen.getByRole("button")).toBeDisabled();

    // Resolve the action
    resolveAction!({ success: true });

    await waitFor(() => {
      expect(screen.getByRole("button")).not.toBeDisabled();
    });
  });
});
```

### Testing Forms

```typescript
// app/_components/DiaryForm.test.tsx
import { describe, it, expect, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { DiaryForm } from "./DiaryForm";

vi.mock("@/app/_actions/diary", () => ({
  addDiaryEntry: vi.fn(),
}));

describe("DiaryForm", () => {
  it("renders form fields", () => {
    render(<DiaryForm characterId={1} />);

    expect(screen.getByLabelText(/title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/content/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/mood/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /save/i })).toBeInTheDocument();
  });

  it("submits form with correct data", async () => {
    const { addDiaryEntry } = await import("@/app/_actions/diary");
    vi.mocked(addDiaryEntry).mockResolvedValue({ success: true });

    const user = userEvent.setup();
    render(<DiaryForm characterId={1} />);

    await user.type(screen.getByLabelText(/title/i), "My Diary Entry");
    await user.type(screen.getByLabelText(/content/i), "This is the content");
    await user.selectOptions(screen.getByLabelText(/mood/i), "happy");
    await user.click(screen.getByRole("button", { name: /save/i }));

    await waitFor(() => {
      expect(addDiaryEntry).toHaveBeenCalled();
    });

    const formData = vi.mocked(addDiaryEntry).mock.calls[0][0];
    expect(formData.get("title")).toBe("My Diary Entry");
    expect(formData.get("content")).toBe("This is the content");
    expect(formData.get("mood")).toBe("happy");
  });

  it("shows error message on failure", async () => {
    const { addDiaryEntry } = await import("@/app/_actions/diary");
    vi.mocked(addDiaryEntry).mockResolvedValue({
      success: false,
      error: "Failed to save",
    });

    const user = userEvent.setup();
    render(<DiaryForm characterId={1} />);

    await user.type(screen.getByLabelText(/title/i), "Test");
    await user.type(screen.getByLabelText(/content/i), "Content");
    await user.click(screen.getByRole("button", { name: /save/i }));

    await waitFor(() => {
      expect(screen.getByText(/failed to save/i)).toBeInTheDocument();
    });
  });

  it("shows success message on success", async () => {
    const { addDiaryEntry } = await import("@/app/_actions/diary");
    vi.mocked(addDiaryEntry).mockResolvedValue({
      success: true,
      message: "Entry saved!",
    });

    const user = userEvent.setup();
    render(<DiaryForm characterId={1} />);

    await user.type(screen.getByLabelText(/title/i), "Test");
    await user.type(screen.getByLabelText(/content/i), "Content");
    await user.click(screen.getByRole("button", { name: /save/i }));

    await waitFor(() => {
      expect(screen.getByText(/entry saved/i)).toBeInTheDocument();
    });
  });
});
```

---

## Part 4: E2E Testing with Playwright

### Basic E2E Tests

```typescript
// e2e/home.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Homepage", () => {
  test("loads successfully", async ({ page }) => {
    await page.goto("/");

    // Check title
    await expect(page).toHaveTitle(/simpsons/i);

    // Check main content
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  });

  test("navigates to characters", async ({ page }) => {
    await page.goto("/");

    // Click characters link
    await page.getByRole("link", { name: /characters/i }).click();

    // Verify navigation
    await expect(page).toHaveURL("/characters");
    await expect(
      page.getByRole("heading", { name: /characters/i }),
    ).toBeVisible();
  });
});
```

### Character Page Tests

```typescript
// e2e/characters.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Characters Page", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/characters");
  });

  test("displays character list", async ({ page }) => {
    // Wait for characters to load
    await expect(page.getByTestId("character-list")).toBeVisible();

    // Check at least one character card exists
    const characterCards = page.getByTestId("character-card");
    await expect(characterCards.first()).toBeVisible();
  });

  test("navigates to character detail", async ({ page }) => {
    // Click first character
    const firstCharacter = page.getByTestId("character-card").first();
    const characterName = await firstCharacter
      .getByRole("heading")
      .textContent();

    await firstCharacter.click();

    // Verify navigation to detail page
    await expect(page).toHaveURL(/\/characters\/\d+/);
    await expect(
      page.getByRole("heading", { name: characterName! }),
    ).toBeVisible();
  });

  test("search filters characters", async ({ page }) => {
    // Type in search
    const searchInput = page.getByPlaceholder(/search/i);
    await searchInput.fill("Homer");

    // Wait for filter
    await page.waitForTimeout(500);

    // Verify filtered results
    const cards = page.getByTestId("character-card");
    await expect(cards).toHaveCount(1);
    await expect(cards.first()).toContainText("Homer");
  });
});
```

### Authentication Tests

```typescript
// e2e/auth.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Authentication", () => {
  test("redirects unauthenticated users from diary", async ({ page }) => {
    await page.goto("/diary");

    // Should show login prompt or redirect
    await expect(
      page.getByText(/sign in|log in|please authenticate/i),
    ).toBeVisible();
  });

  test("allows authenticated users to access diary", async ({ page }) => {
    // Mock authentication (adjust based on your auth system)
    await page.route("**/api/auth/**", (route) => {
      route.fulfill({
        status: 200,
        body: JSON.stringify({ user: { id: "1", name: "Test" } }),
      });
    });

    await page.goto("/diary");

    // Should see diary content
    await expect(page.getByRole("heading", { name: /diary/i })).toBeVisible();
  });
});
```

### Visual Regression Tests

```typescript
// e2e/visual.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Visual Regression", () => {
  test("homepage looks correct", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    await expect(page).toHaveScreenshot("homepage.png", {
      fullPage: true,
      maxDiffPixelRatio: 0.02,
    });
  });

  test("character page looks correct", async ({ page }) => {
    await page.goto("/characters");
    await page.waitForLoadState("networkidle");

    await expect(page).toHaveScreenshot("characters.png", {
      fullPage: true,
    });
  });

  test("dark mode looks correct", async ({ page }) => {
    await page.goto("/");

    // Toggle dark mode
    await page.evaluate(() => {
      document.documentElement.classList.add("dark");
    });

    await expect(page).toHaveScreenshot("homepage-dark.png", {
      fullPage: true,
    });
  });
});
```

### API Mocking in E2E

```typescript
// e2e/with-mocks.spec.ts
import { test, expect } from "@playwright/test";

test.describe("With Mocked API", () => {
  test("shows characters from mocked API", async ({ page }) => {
    // Mock the API response
    await page.route("**/api/characters", (route) => {
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify([
          { id: 1, name: "Test Character", occupation: "Tester" },
        ]),
      });
    });

    await page.goto("/characters");

    await expect(page.getByText("Test Character")).toBeVisible();
  });

  test("handles API errors gracefully", async ({ page }) => {
    // Mock API failure
    await page.route("**/api/characters", (route) => {
      route.fulfill({
        status: 500,
        body: "Internal Server Error",
      });
    });

    await page.goto("/characters");

    // Should show error state
    await expect(page.getByText(/error|failed|try again/i)).toBeVisible();
  });
});
```

---

## Part 5: Coverage and CI

### Running with Coverage

```bash
# Run tests with coverage report
pnpm test:coverage

# View HTML report
open coverage/index.html
```

### Coverage Thresholds

```typescript
// vitest.config.ts - add coverage thresholds
export default defineConfig({
  test: {
    coverage: {
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 70,
        statements: 80,
      },
    },
  },
});
```

### GitHub Actions CI

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2
        with:
          version: 8

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - run: pnpm install

      - name: Run unit tests
        run: pnpm test:coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2
        with:
          version: 8

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - run: pnpm install

      - name: Install Playwright
        run: pnpm exec playwright install --with-deps chromium

      - name: Run E2E tests
        run: pnpm test:e2e

      - uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

---

## Best Practices

### Test Naming Conventions

```typescript
// Describe what it does, not how
describe("FollowButton", () => {
  it("displays follow state correctly", () => {});
  it("toggles state on click", () => {});
  it("handles errors gracefully", () => {});
  it("shows loading state while pending", () => {});
});

// Use describe blocks for grouping
describe("DiaryForm", () => {
  describe("validation", () => {
    it("requires title", () => {});
    it("requires content", () => {});
  });

  describe("submission", () => {
    it("calls action with form data", () => {});
    it("shows success message", () => {});
  });
});
```

### Testing Checklist

- [ ] **Unit Tests**: All utility functions
- [ ] **Unit Tests**: All server actions
- [ ] **Unit Tests**: All repository functions
- [ ] **Component Tests**: All interactive components
- [ ] **Component Tests**: Form submission
- [ ] **Component Tests**: Error states
- [ ] **E2E Tests**: Critical user flows
- [ ] **E2E Tests**: Authentication flows
- [ ] **E2E Tests**: Error handling
- [ ] **Visual Tests**: Main pages
- [ ] **Coverage**: > 80% overall

---

## Test Mock Type Safety (SonarLint Validated)

### When to Use `any` in Tests

**Rule:** Avoid `any` types even in tests. Use `Partial<T>` or specific interfaces instead.

#### ✅ Acceptable with `@ts-expect-error`

```typescript
// __tests__/example.test.ts
import { vi } from "vitest";

// ✅ ACCEPTABLE: Test mock with documented reason
vi.mock("@/infrastructure/factories", () => ({
  UseCaseFactory: {
    // @ts-expect-error - Test mock intentionally incomplete for flexibility
    createTrackEpisodeUseCase: (): any => ({
      execute: vi.fn().mockResolvedValue({ success: true }),
    }),
  },
}));
```

**When this is acceptable:**

- Mock needs to work with multiple use case variations
- Full interface implementation would bloat test code
- You document WHY with `@ts-expect-error` comment

#### ✅ Better: Use `Partial<T>`

```typescript
// __tests__/example.test.ts
import { TrackEpisodeUseCase } from "@/core/application/use-cases";

// ✅ BETTER: Type-safe partial mock
const mockUseCase: Partial<TrackEpisodeUseCase> = {
  execute: vi.fn().mockResolvedValue({ success: true }),
};

vi.mock("@/infrastructure/factories", () => ({
  UseCaseFactory: {
    createTrackEpisodeUseCase: () => mockUseCase,
  },
}));
```

**Benefits:**

- TypeScript validates property names
- Auto-complete works
- Refactoring catches breaking changes
- No SonarLint warnings

#### ❌ Never in Production Code

```typescript
// ❌ WRONG - No `any` in production
// app/_lib/utils.ts
export function processData(input: any): any {
  return input;
}

// ✅ CORRECT - Specific types
export function processData(input: InputDTO): OutputDTO {
  return transformedData;
}
```

### Type Safety Checklist

**Production Code:**

- [ ] Zero `any` types
- [ ] Use `unknown` for truly dynamic data, then narrow
- [ ] Use `Partial<T>` for optional fields
- [ ] Use generics `<T>` for reusable types

**Test Code:**

- [ ] Prefer `Partial<Interface>` for mocks
- [ ] Use `@ts-expect-error` only when necessary
- [ ] Document WHY `any` is used
- [ ] Never use `any` without explanation

### Examples from PR #14 SonarLint Cleanup

#### Vitest Setup File Fix

**Before:**

```typescript
// vitest.setup.ts
vi.mock("next/image", () => ({
  default: (props: any) => props, // ❌ SonarLint: Avoid any type
}));
```

**After:**

```typescript
// vitest.setup.ts
vi.mock("next/image", () => ({
  default: (props: Record<string, unknown>) => props, // ✅ Explicit type
}));
```

**Why:** `Record<string, unknown>` clearly indicates props are a dynamic object with unknown values.

#### Test Mock Documentation

```typescript
// __tests__/rls-isolation.test.ts

// ✅ GOOD: Documented any usage
// @ts-expect-error - Test mock intentionally incomplete
const mockPrisma: any = {
  diaryEntry: {
    create: vi.fn(),
    findUnique: vi.fn(),
  },
};

// ✅ BETTER: Use Partial
const mockPrisma: Partial<PrismaClient> = {
  diaryEntry: {
    create: vi.fn(),
    findUnique: vi.fn(),
  } as any, // Only the nested object uses any
};
```

### Type-Safe Mock Factories

**Create reusable mock factories:**

```typescript
// __tests__/factories.ts
import { Character } from "@prisma/client";

export function createMockCharacter(
  overrides: Partial<Character> = {},
): Character {
  return {
    id: 1,
    name: "Homer Simpson",
    occupation: "Safety Inspector",
    image: "/homer.jpg",
    createdAt: new Date(),
    updatedAt: new Date(),
    ...overrides,
  };
}

// Usage in tests
const homer = createMockCharacter({ name: "Homer" });
const marge = createMockCharacter({ id: 2, name: "Marge" });
```

**Benefits:**

- Type-safe by default
- Easy to override specific fields
- Consistent test data
- No `any` types needed

### Lessons Learned (SonarLint PR #14)

**Files Validated:**

- [vitest.setup.ts](../../../vitest.setup.ts) - Fixed `any` in Next.js Image mock
- [**tests**/rls-isolation.test.ts](../../../__tests__/rls-isolation.test.ts) - Documented test mock `any` usage
- [**tests**/rls-isolation.integration.test.ts](../../../__tests__/rls-isolation.integration.test.ts) - Validated test patterns

**Impact:**

- Zero SonarLint warnings in test files
- Better type safety in mocks
- Clearer intent with `@ts-expect-error` comments
- No production code uses `any`

**Reference:** See [.traces/05-sonarlint-pr14-cleanup.md](../../../.traces/05-sonarlint-pr14-cleanup.md) for complete analysis.

---

## Testing with Row Level Security (RLS)

RLS introduces database-level security that requires special testing patterns. Unit tests can't verify RLS policies, but integration tests can.

### RLS Testing Strategy: Hybrid Approach

**Unit Tests:** Verify code uses RLS helpers correctly
**Integration Tests:** Verify RLS policies work in actual database
**Mocks:** Simulate RLS context for unit testing

### Mocking RLS Helpers for Unit Tests

```typescript
// __mocks__/prisma-rls.ts
import { vi } from "vitest";

const mockPrismaClient = {
  diaryEntry: {
    findMany: vi.fn(),
    findUnique: vi.fn(),
    create: vi.fn(),
  },
  // ... other Prisma methods
};

export const withAuthenticatedRLS = vi.fn((callback) => {
  const mockUser = { id: "test-user-id", email: "test@test.com" };
  return callback(mockPrismaClient, mockUser);
});

export const withOptionalRLS = vi.fn((callback) => {
  const mockUser = { id: "test-user-id", email: "test@test.com" };
  return callback(mockPrismaClient, mockUser);
});

export const withoutRLS = vi.fn((callback) => {
  return callback(mockPrismaClient);
});
```

### Unit Test: Server Action with RLS

```typescript
// app/_actions/diary.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { addDiaryEntry } from "./diary";

vi.mock("@/app/_lib/prisma-rls", () => ({
  withAuthenticatedRLS: vi.fn(async (callback) => {
    const mockPrisma = {
      diaryEntry: {
        create: vi.fn().mockResolvedValue({
          id: "entry-1",
          userId: "test-user",
          characterId: 1,
          createdAt: new Date(),
        }),
      },
    };
    const mockUser = { id: "test-user", email: "test@test.com" };
    return callback(mockPrisma, mockUser);
  }),
}));

vi.mock("next/cache", () => ({
  revalidatePath: vi.fn(),
}));

describe("addDiaryEntry with RLS", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls withAuthenticatedRLS", async () => {
    const { withAuthenticatedRLS } = await import("@/app/_lib/prisma-rls");

    await addDiaryEntry({
      characterId: 1,
      locationId: 1,
      description: "Springfield adventure",
    });

    expect(withAuthenticatedRLS).toHaveBeenCalled();
  });

  it("creates entry within transaction", async () => {
    const result = await addDiaryEntry({
      characterId: 1,
      locationId: 1,
      description: "Springfield adventure",
    });

    expect(result.success).toBe(true);
    expect(result.data?.userId).toBe("test-user");
  });
});
```

### Integration Test: RLS Isolation

```typescript
// __tests__/rls-isolation.test.ts
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { prisma } from "@/app/_lib/prisma";

/**
 * Integration test: Verify RLS policies enforce isolation
 * Run against actual Neon database (requires test database)
 */
describe("RLS Isolation (Integration Test)", () => {
  beforeEach(async () => {
    // Clean up test data
    await prisma.diaryEntry.deleteMany();
  });

  afterEach(async () => {
    // Clean up
    await prisma.diaryEntry.deleteMany();
  });

  it("prevents cross-user diary access", async () => {
    const userAId = "user-a-uuid";
    const userBId = "user-b-uuid";

    // User A creates entry
    await prisma.$transaction(async (tx) => {
      await tx.$executeRawUnsafe(
        `SELECT set_config('app.current_user_id', $1, true)`,
        userAId,
      );
      await tx.diaryEntry.create({
        data: {
          userId: userAId,
          characterId: 1,
          locationId: 1,
          activityDescription: "User A's private entry",
        },
      });
    });

    // User B queries diary
    const userBEntries = await prisma.$transaction(async (tx) => {
      await tx.$executeRawUnsafe(
        `SELECT set_config('app.current_user_id', $1, true)`,
        userBId,
      );
      return tx.diaryEntry.findMany();
    });

    // ✅ Verify User B cannot see User A's entry
    expect(userBEntries).toHaveLength(0);
  });

  it("allows users to see only their own data", async () => {
    const userId = "test-user-uuid";

    // Create 2 entries for this user
    await prisma.$transaction(async (tx) => {
      await tx.$executeRawUnsafe(
        `SELECT set_config('app.current_user_id', $1, true)`,
        userId,
      );

      await tx.diaryEntry.createMany({
        data: [
          {
            userId,
            characterId: 1,
            locationId: 1,
            activityDescription: "Entry 1",
          },
          {
            userId,
            characterId: 2,
            locationId: 2,
            activityDescription: "Entry 2",
          },
        ],
      });
    });

    // Query as same user
    const entries = await prisma.$transaction(async (tx) => {
      await tx.$executeRawUnsafe(
        `SELECT set_config('app.current_user_id', $1, true)`,
        userId,
      );
      return tx.diaryEntry.findMany();
    });

    // ✅ Can see their own entries
    expect(entries).toHaveLength(2);
  });
});
```

### Testing RLS Policy Violations

```typescript
// __tests__/rls-violations.test.ts
import { describe, it, expect } from "vitest";
import { prisma } from "@/app/_lib/prisma";

describe("RLS Policy Enforcement", () => {
  it("prevents UPDATE across RLS boundary", async () => {
    const userA = "user-a";
    const userB = "user-b";

    // User A creates entry
    let entryId: string;
    await prisma.$transaction(async (tx) => {
      await tx.$executeRawUnsafe(
        `SELECT set_config('app.current_user_id', $1, true)`,
        userA,
      );
      const entry = await tx.diaryEntry.create({
        data: {
          userId: userA,
          characterId: 1,
          locationId: 1,
          activityDescription: "User A's entry",
        },
      });
      entryId = entry.id;
    });

    // User B tries to UPDATE it
    await expect(async () => {
      await prisma.$transaction(async (tx) => {
        await tx.$executeRawUnsafe(
          `SELECT set_config('app.current_user_id', $1, true)`,
          userB,
        );
        // This should fail silently (0 rows updated)
        await tx.diaryEntry.update({
          where: { id: entryId },
          data: { activityDescription: "Hacked by User B" },
        });
      });
    }).rejects.toThrow();

    // ✅ Verify entry was NOT modified
    const entry = await prisma.diaryEntry.findUnique({
      where: { id: entryId },
    });
    expect(entry?.activityDescription).toBe("User A's entry");
  });
});
```

### Running RLS Tests

```bash
# Unit tests (with mocks)
pnpm test:unit

# Integration tests (against real database)
pnpm test:integration

# Only RLS isolation tests
pnpm test -- rls-isolation.test.ts

# With coverage
pnpm test:coverage -- __tests__/rls-isolation.test.ts
```

### Lessons Learned: Testing RLS

1. **Mock for speed:** Unit tests with mocks run in milliseconds
2. **Verify with integration tests:** Only integration tests can validate actual RLS policies
3. **Test data isolation:** Cross-user tests are essential for RLS validation
4. **Test policy violations:** Ensure RLS prevents unauthorized access
5. **Performance testing:** Verify RLS filtering doesn't degrade query performance

**Key Pattern:** Unit test that code _uses_ RLS, integration test that RLS _works_

---

## Related Skills

- [webapp-testing](../webapp-testing/SKILL.md) - Manual UI testing
- [server-actions-patterns](../server-actions-patterns/SKILL.md) - Testing actions with RLS
- [component-development](../component-development/SKILL.md) - Component testing
- [prisma-nextjs16](../prisma-nextjs16/SKILL.md) - RLS with Prisma patterns

---

## References

- [Vitest Documentation](https://vitest.dev/)
- [Testing Library](https://testing-library.com/)
- [Playwright Documentation](https://playwright.dev/)
- [Next.js Testing](https://nextjs.org/docs/app/building-your-application/testing)
- [PostgreSQL RLS Documentation](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)

---

**Last Updated:** January 19, 2026  
**Maintained By:** Development Team  
**Status:** ✅ Production Ready with RLS Support
