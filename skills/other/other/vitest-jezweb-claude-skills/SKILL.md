---
name: vitest
description: "Set up Vitest testing in any project — detects project type (Cloudflare Workers, React, Node), generates vitest.config.ts, test setup, utilities, and sample tests. Also covers mocking patterns, coverage config, workspace setup, and Jest migration. Trigger with 'set up vitest', 'add tests', 'configure vitest', 'migrate from jest', 'vitest config', 'add unit tests', or 'testing setup'."
license: MIT
---

# Vitest Setup

Detect the project type, generate the right Vitest configuration, and produce working test infrastructure. Not a reference card — this skill creates files.

## Workflow

1. **Detect** — scan the project to determine type and existing setup
2. **Configure** — generate vitest.config.ts tailored to the environment
3. **Scaffold** — create test setup, utilities, and a sample test
4. **Wire up** — add package.json scripts and TypeScript config

## Step 1: Detect Project Type

Read these files to determine the project:

```
package.json          → dependencies, scripts, type field
tsconfig.json         → paths, compiler options
wrangler.toml         → Cloudflare Workers project
vite.config.ts        → existing Vite setup (extend, don't replace)
vitest.config.ts      → already configured? just fill gaps
jest.config.*         → migration candidate
src/                  → source structure
```

Classify as one of:

| Type | Signals | Environment |
|------|---------|-------------|
| **Cloudflare Workers** | wrangler.toml, @cloudflare/workers-types, cloudflare vite plugin | `node` with Workers-specific setup |
| **React (Vite)** | @vitejs/plugin-react, react-dom | `jsdom` or `happy-dom` |
| **React (SSR/TanStack Start)** | @tanstack/start, vinxi | Split: `node` for server, `jsdom` for client |
| **Node/Hono API** | hono, express, no react-dom | `node` |
| **Library** | exports field, no framework deps | `node` |

If a `vite.config.ts` already exists, extend it rather than creating a separate vitest.config.ts — Vitest reads Vite config natively.

## Step 2: Install Dependencies

Generate the install command based on detected type:

```bash
# Base (always)
pnpm add -D vitest

# React projects — add jsdom and Testing Library
pnpm add -D @vitest/coverage-v8 jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event

# Workers projects — add Cloudflare test utilities
pnpm add -D @vitest/coverage-v8 @cloudflare/vitest-pool-workers

# Node/Hono projects
pnpm add -D @vitest/coverage-v8

# If migrating from Jest, also remove:
pnpm remove jest ts-jest @types/jest jest-environment-jsdom babel-jest
```

Use the project's package manager (check for pnpm-lock.yaml, yarn.lock, bun.lockb, or package-lock.json).

## Step 3: Generate vitest.config.ts

### Cloudflare Workers

```typescript
import { defineWorkersConfig } from "@cloudflare/vitest-pool-workers/config";

export default defineWorkersConfig({
  test: {
    globals: true,
    poolOptions: {
      workers: {
        wrangler: { configPath: "./wrangler.toml" },
      },
    },
  },
});
```

If the project uses the Cloudflare Vite plugin (`@cloudflare/vite-plugin`), integrate into the existing vite.config.ts instead:

```typescript
/// <reference types="vitest/config" />
import { defineConfig } from "vite";
import { cloudflare } from "@cloudflare/vite-plugin";

export default defineConfig({
  plugins: [cloudflare()],
  test: {
    globals: true,
  },
});
```

### React (Vite)

```typescript
/// <reference types="vitest/config" />
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
    css: true,
  },
});
```

If a vite.config.ts already exists, add the `test` block to it rather than creating a new file.

### Node / Hono API

```typescript
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
  },
});
```

### With Coverage (add to any config)

```typescript
  test: {
    // ... existing config
    coverage: {
      provider: "v8",
      reporter: ["text", "html", "lcov"],
      exclude: [
        "node_modules/",
        "**/*.config.*",
        "**/*.d.ts",
        "**/test/**",
      ],
    },
  },
```

## Step 4: Generate Test Setup File

Create `src/test/setup.ts` (React projects only):

```typescript
import "@testing-library/jest-dom/vitest";
```

That single import adds all the custom matchers (toBeInTheDocument, toHaveTextContent, etc.) and registers the Vitest `expect.extend` automatically.

## Step 5: Add TypeScript Config

Add to `tsconfig.json` compilerOptions:

```json
{
  "compilerOptions": {
    "types": ["vitest/globals"]
  }
}
```

For projects with multiple tsconfig files (e.g. tsconfig.app.json + tsconfig.node.json), add to the one that covers test files — usually the root tsconfig.json or create a tsconfig.test.json that extends it.

## Step 6: Add Package.json Scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui"
  }
}
```

Don't overwrite existing scripts — merge with what's there.

## Step 7: Generate Sample Test

Write one test file that demonstrates the right patterns for this specific project. Place it next to real source code, not in a separate `__tests__` directory.

### For a Hono API route (e.g. `src/routes/health.ts`):

```typescript
import { describe, it, expect } from "vitest";
import { app } from "../index";

describe("GET /health", () => {
  it("returns 200 with status ok", async () => {
    const res = await app.request("/health");
    expect(res.status).toBe(200);

    const body = await res.json();
    expect(body).toEqual({ status: "ok" });
  });
});
```

### For a React component (e.g. `src/components/Button.tsx`):

```typescript
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Button } from "./Button";

describe("Button", () => {
  it("renders with label", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole("button", { name: /click me/i })).toBeInTheDocument();
  });

  it("calls onClick when clicked", async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    await user.click(screen.getByRole("button"));
    expect(handleClick).toHaveBeenCalledOnce();
  });
});
```

### For a utility function (e.g. `src/utils/format.ts`):

```typescript
import { describe, it, expect } from "vitest";
import { formatCurrency } from "./format";

describe("formatCurrency", () => {
  it("formats whole numbers", () => {
    expect(formatCurrency(1000)).toBe("$1,000.00");
  });

  it("formats decimals", () => {
    expect(formatCurrency(49.9)).toBe("$49.90");
  });

  it("handles zero", () => {
    expect(formatCurrency(0)).toBe("$0.00");
  });
});
```

Pick a real file from the project to test. Don't invent a fake module — the sample test should run immediately after setup.

## Step 8: Verify

Run the tests to confirm everything works:

```bash
pnpm test:run
```

If it fails, diagnose and fix. Common issues:

| Error | Fix |
|-------|-----|
| `Cannot find module 'vitest'` | Check install completed, check `node_modules/.vitest` exists |
| `ReferenceError: describe is not defined` | Add `globals: true` to config, or add `types: ["vitest/globals"]` to tsconfig |
| `document is not defined` | Wrong environment — set `environment: "jsdom"` for React tests |
| `Cannot use import.meta` | Ensure vitest.config uses `.ts` extension and project has `"type": "module"` or Vite handles transforms |
| Workers bindings undefined | Use `@cloudflare/vitest-pool-workers` instead of plain vitest, check wrangler.toml path |

---

## Mocking Reference

These patterns are for writing tests after setup is complete. Include them in the sample test or a `src/test/examples.test.ts` if the user asks for mocking examples.

### Module mocking (vi.mock)

```typescript
import { vi, describe, it, expect } from "vitest";
import { getUser } from "./api";

vi.mock("./api", () => ({
  getUser: vi.fn(),
}));

it("mocks a module function", async () => {
  vi.mocked(getUser).mockResolvedValue({ id: 1, name: "Test" });
  const user = await getUser(1);
  expect(user.name).toBe("Test");
  expect(getUser).toHaveBeenCalledWith(1);
});
```

### Spy on methods (vi.spyOn)

```typescript
it("spies on console.warn", () => {
  const spy = vi.spyOn(console, "warn").mockImplementation(() => {});
  doSomethingThatWarns();
  expect(spy).toHaveBeenCalledOnce();
  spy.mockRestore();
});
```

### Fake timers

```typescript
import { vi, beforeEach, afterEach, it, expect } from "vitest";

beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date("2026-01-15T10:00:00Z"));
});

afterEach(() => {
  vi.useRealTimers();
});

it("uses controlled time", () => {
  expect(new Date().toISOString()).toBe("2026-01-15T10:00:00.000Z");
});
```

### Global stubs

```typescript
it("stubs fetch", async () => {
  const mockFetch = vi.fn().mockResolvedValue({
    ok: true,
    json: () => Promise.resolve({ data: "test" }),
  });
  vi.stubGlobal("fetch", mockFetch);

  const res = await fetch("/api/data");
  expect(mockFetch).toHaveBeenCalledWith("/api/data");

  vi.unstubAllGlobals();
});
```

### Snapshot testing

```typescript
it("matches snapshot", () => {
  const result = generateConfig({ debug: true });
  expect(result).toMatchSnapshot();
});

it("matches inline snapshot", () => {
  expect({ status: "ok", count: 3 }).toMatchInlineSnapshot(`
    {
      "count": 3,
      "status": "ok",
    }
  `);
});
```

### Parameterized tests

```typescript
describe.each([
  { input: "hello", expected: "HELLO" },
  { input: "world", expected: "WORLD" },
  { input: "", expected: "" },
])("toUpperCase($input)", ({ input, expected }) => {
  it(`returns ${expected}`, () => {
    expect(input.toUpperCase()).toBe(expected);
  });
});
```

---

## Jest Migration

When the detected project has Jest (`jest.config.*`, `@types/jest`, `ts-jest` in dependencies):

1. **Generate the vitest.config.ts** using the steps above
2. **Update imports** in existing test files:

```typescript
// Before
import { jest } from "@jest/globals";
jest.mock("./api");
jest.fn();
jest.spyOn(obj, "method");

// After
import { vi } from "vitest";
vi.mock("./api");
vi.fn();
vi.spyOn(obj, "method");
```

3. **Remove Jest packages:**
```bash
pnpm remove jest ts-jest @types/jest jest-environment-jsdom babel-jest @jest/globals
```

4. **Update tsconfig** — replace `"types": ["jest"]` with `"types": ["vitest/globals"]`

5. **Run tests** and fix any remaining issues

Key replacements:

| Jest | Vitest |
|------|--------|
| `jest.fn()` | `vi.fn()` |
| `jest.mock()` | `vi.mock()` |
| `jest.spyOn()` | `vi.spyOn()` |
| `jest.useFakeTimers()` | `vi.useFakeTimers()` |
| `jest.clearAllMocks()` | `vi.clearAllMocks()` |
| `jest.requireActual()` | `vi.importActual()` |
| `@jest/globals` | `vitest` |
| `jest.config.js` | `vitest.config.ts` |

---

## Workspace Setup (Monorepos)

For monorepo projects with multiple packages:

```typescript
// vitest.workspace.ts
import { defineWorkspace } from "vitest/config";

export default defineWorkspace([
  "packages/*/vitest.config.ts",
]);
```

Each package gets its own config. The workspace file just points to them.

---

## What This Skill Produces

After running, the project should have:
- `vitest.config.ts` (or test block added to existing vite.config.ts)
- `src/test/setup.ts` (React projects)
- Updated `tsconfig.json` with vitest/globals type
- Updated `package.json` with test scripts
- At least one passing sample test against real source code
- Dependencies installed

The tests should pass on first run. If they don't, fix them before finishing.
