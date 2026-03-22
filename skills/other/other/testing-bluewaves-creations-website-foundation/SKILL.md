---
name: testing
description: Write and run tests using Vitest with Astro integration — mock Cloudflare bindings, test API routes, validate schemas, and use test helpers. Use when the user mentions "testing", "tests", "vitest", "mock", "test helpers", "createMockEnv", "createMockContext", "write a test", or "run tests".
---

# Testing

Website Foundation uses Vitest with Astro's `getViteConfig()` integration. Tests live in `tests/unit/` and `tests/integration/`.

## Running Tests

```bash
bun run test          # Run all tests once (42 tests, 7 files)
bun run test:watch    # Run in watch mode
```

## Configuration

`vitest.config.ts` uses Astro's Vite config wrapper:

```ts
import { getViteConfig } from "astro/config";

export default getViteConfig({
  test: {
    include: ["tests/**/*.test.ts"],
  },
});
```

## Test Helpers

`tests/setup.ts` exports two helpers:

- **`createMockEnv()`** — Returns a mock Cloudflare runtime env with all bindings (AI, SEND_EMAIL, secrets)
- **`createMockContext(request, env?)`** — Returns a mock API context with `locals.runtime.env` and request

## Key Patterns

### Mock Cloudflare modules before importing

```ts
vi.mock("cloudflare:email", () => ({
  EmailMessage: vi.fn().mockImplementation((from, to, raw) => ({ from, to, raw })),
}));
```

### Test API routes

```ts
const request = new Request("http://localhost/api/contact", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: "Test", email: "test@test.com", message: "Hello" }),
});
const context = createMockContext(request);
const response = await POST(context as any);
expect(response.status).toBe(200);
```

### Validate schemas without Astro runtime

```ts
const result = blogSchema.safeParse({ title: "Test", ... });
expect(result.success).toBe(true);
```

See [Vitest patterns](references/vitest-patterns.md) and [mock helpers](references/mock-helpers.md) for detailed examples.
