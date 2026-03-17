---
name: "nextjs-frontend-testing"
description: "Use this skill whenever the user wants to set up, improve, or run frontend tests (unit, component, and E2E) for a Next.js (App Router) + TypeScript + Tailwind + shadcn/ui project using Vitest/Jest, React Testing Library, and Playwright."
---

# Next.js Frontend Testing (Vitest/Jest + Testing Library + Playwright)

## Purpose

You are a specialized assistant for **frontend testing** in modern Next.js applications that use:

- Next.js App Router (`app/` directory)
- TypeScript
- Tailwind CSS
- shadcn/ui components
- Vitest or Jest for unit/component tests
- React Testing Library for rendering and assertions
- Playwright for end-to-end (E2E) tests

Use this skill to:

- **Set up** frontend testing from scratch in a Next.js project
- **Choose and configure** Vitest vs Jest appropriately
- Add **React Testing Library** for component tests
- Set up **Playwright** for E2E testing (including config and test structure)
- Write or refactor **unit, component, and E2E tests**
- Define **test scripts** in `package.json` and recommend CI commands
- Improve test reliability (avoid flaky tests, use best practices)

Do **not** use this skill for:

- Pure backend or API-only testing (use a backend/infra skill instead)
- Load/performance testing or security testing
- Non-Next.js projects unless the user explicitly wants to reuse the same patterns

If `CLAUDE.md` exists, follow its preferences for testing tools, folders, and scripts.

---

## When to Apply This Skill

Trigger this skill when the user asks for any of the following (or similar):

- “Set up tests for this Next.js project”
- “Add Playwright E2E tests to this app”
- “Convert my Jest setup to Vitest” or “Wire in React Testing Library”
- “Write unit tests for this component/page”
- “Add tests to cover this user flow end-to-end”
- “Make my tests less flaky / fix failing tests”
- “Show me how to structure test folders in a Next.js project”

Avoid applying this skill when:

- The task is purely about routing/layout structure (use the routes/layout skill)
- The user is only adjusting UI styles with no testing aspects
- The project explicitly uses a different stack (e.g. Cypress only) and the user does not want to change it

---

## Testing Philosophy

When using this skill, follow these principles:

1. **Test behavior, not implementation details**
   - Focus on what the user sees and does, not internal React component structure.
   - Prefer queries like `getByRole`, `getByText`, `getByLabelText` in Testing Library.
   - Avoid fragile selectors tied to DOM nesting.

2. **Use the right level of tests for the job**
   - **Unit tests**: small isolated logic (pure functions, hooks, small components).
   - **Component tests**: components rendered with realistic props and mocked dependencies.
   - **E2E tests** (Playwright): critical flows through the app from the user’s perspective.

3. **Keep tests fast and deterministic**
   - Minimize use of timers, random data, network/Date dependencies.
   - Stub or mock network calls in unit/component tests.
   - Use realistic but limited test data.

4. **Embrace Next.js idioms**
   - Favor server components and server data fetching in the app; test the behavior at boundaries.
   - For client components, test interactions and side effects.
   - Use Playwright to validate integration between routes, layouts, and client interactions.

5. **Make tests easy to run**
   - Provide clear scripts in `package.json`:
     - `"test"`
     - `"test:unit"`
     - `"test:e2e"`
   - Keep consistent folder naming and structure.

---

## Project Structure Conventions

Unless the project or `CLAUDE.md` says otherwise, prefer something like:

```text
src/
  app/               # Next.js routes
  components/        # reusable components
  lib/               # utilities, hooks, etc.
tests/
  unit/              # unit & component tests (Vitest/Jest + RTL)
  e2e/               # Playwright E2E tests
```

Acceptable alternative patterns:

- colocated tests: `ComponentName.test.tsx` next to `ComponentName.tsx`
- `__tests__` folders for unit tests

Choose the pattern that best matches existing conventions in the repo.

---

## Step-by-Step Workflow

When this skill is active, follow this process:

### 1. Inspect the project’s current testing setup

- Look for:
  - `vitest.config.*` or `jest.config.*`
  - Existing `tests/`, `__tests__/`, or `.test.tsx/.spec.tsx` files
  - `playwright.config.*`
  - Test-related scripts in `package.json`
- Respect existing decisions when possible; migrate only if it clearly benefits the user.

### 2. Choose Vitest vs Jest

- If the project already uses Jest and is heavily invested, keep Jest unless the user wants to migrate.
- If no clear choice exists, prefer **Vitest** for:
  - Fast, modern, Vite-style DX
  - Great TypeScript support
- Configure the selected framework to work with React and JSX.

### 3. Set up React Testing Library

- Install necessary packages:
  - `@testing-library/react`
  - `@testing-library/jest-dom` or equivalent matchers
  - `@testing-library/user-event` for realistic interactions (if desired)
- Create a **test setup file** (e.g. `tests/setupTests.ts`) that:
  - Imports `@testing-library/jest-dom` (or similar)
  - Configures any global test utilities

- Link the setup file in the Vitest or Jest config.

### 4. Configure Vitest / Jest

- For Vitest example (rough outline):

  ```ts
  import { defineConfig } from "vitest/config";
  import react from "@vitejs/plugin-react";

  export default defineConfig({
    plugins: [react()],
    test: {
      globals: true,
      environment: "jsdom",
      setupFiles: ["./tests/setupTests.ts"],
      include: ["tests/unit/**/*.test.{ts,tsx}", "src/**/*.{test,spec}.{ts,tsx}"],
    },
  });
  ```

- Adjust paths, aliases (e.g. `@/`), and environment as needed for Next.js + TS.

### 5. Set up Playwright for E2E

- Install Playwright test runner and browsers.
- Add a `playwright.config` file with sensible defaults:
  - Base URL, port, and timeouts
  - Projects for different browsers if the user wants them (chromium, firefox, webkit)
- Create a `tests/e2e/` folder (or similar) with example specs:
  - A basic smoke test (home page loads, important UI is present)
  - A critical user journey (login, dashboard navigation, etc.)

- Add NPM scripts to `package.json`:

  ```jsonc
  {
    "scripts": {
      "test:unit": "vitest",
      "test:e2e": "playwright test",
      "test": "vitest && playwright test"
    }
  }
  ```

  Adjust for Jest/Yarn/pnpm as required.

### 6. Write or refactor unit/component tests

- For a given component, test:
  - It renders with required props.
  - It renders different variants, sizes, or states correctly.
  - It reacts to user events (clicks, typing, etc.).
  - It respects accessibility (roles, labels, ARIA attributes).

- Use React Testing Library patterns like:

  ```ts
  import { render, screen } from "@testing-library/react";
  import userEvent from "@testing-library/user-event";
  import { Button } from "@/components/ui/button";

  test("calls onClick when button is clicked", async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();

    render(<Button onClick={handleClick}>Submit</Button>);

    await user.click(screen.getByRole("button", { name: /submit/i }));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });
  ```

- Prefer role-based queries (`getByRole`) and label-based queries (`getByLabelText`) over `getByTestId` unless there is no better option.

### 7. Write or refactor E2E tests (Playwright)

- For each critical flow:
  - Use `page.goto` to open the relevant route.
  - Use `getByRole`, `getByText`, `getByPlaceholder`, etc. to interact with the UI.
  - Assert that expected content or navigation occurs.

- Example outline for a Playwright test:

  ```ts
  import { test, expect } from "@playwright/test";

  test("user can see dashboard after login", async ({ page }) => {
    await page.goto("/login");

    await page.getByLabel("Email").fill("user@example.com");
    await page.getByLabel("Password").fill("password123");
    await page.getByRole("button", { name: /log in/i }).click();

    await expect(page).toHaveURL("/dashboard");
    await expect(page.getByRole("heading", { name: /dashboard/i })).toBeVisible();
  });
  ```

- Prefer stable selectors and avoid relying on fragile text that will change often.

### 8. Integrate with CI

- Suggest a simple CI pipeline outline:
  - Install dependencies.
  - Build app if required.
  - Run `test:unit`.
  - Run `test:e2e` against a running dev or preview server.
- Use environment variables and appropriate base URLs for CI vs local environment.

### 9. Improve flaky tests and DX

- If tests are flaky:
  - Review the use of `waitFor` and timeouts.
  - Remove brittle `setTimeout` usage.
  - Ensure test cleanup is done correctly.
  - In Playwright, prefer `expect` with proper auto-waiting instead of manual sleeps.

- Suggest adjustments that simplify tests or reduce coupling with implementation details.

### 10. Summarize and document

- After modifying or setting up tests, summarize:
  - What tools are in use (Vitest/Jest, RTL, Playwright).
  - Where tests live in the repo.
  - How to run them (commands, options).
- Optionally add a section to `README.md` explaining the testing strategy.

---

## Examples of Prompts That Should Use This Skill

- “Set up Vitest + Testing Library + Playwright for this Next.js app.”
- “Add tests for this shadcn-based form component.”
- “Write E2E tests for the sign-up and login flows.”
- “Convert these Jest tests to Vitest and fix any issues.”
- “My Playwright tests are flaky; help me stabilize them.”
- “Show me how to structure unit vs E2E tests for this project.”

For these kinds of tasks, rely on this skill to drive the **testing setup, best practices,
and concrete test implementations** for Next.js frontend code, while collaborating with
other skills (e.g. app scaffold, routes/layouts, UI component smith) when routing or
component design changes are required.
