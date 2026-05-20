---
name: vitest-mocking
description: |
  Vitest mocking patterns and test double strategies. Use when writing tests that need mocks, spies, stubs, or fakes. Triggers include: mocking modules, stubbing globals (fetch, Date, timers), testing composables, mocking imports (default/named), creating test doubles, replacing dependencies, verifying mock calls, cleaning up mocks, or any question about "how do I mock X in Vitest". Also use when reviewing tests for proper mocking practices.
---

# Vitest Mocking

## Test Double Types

| Type | Purpose | Changes Implementation? |
|------|---------|------------------------|
| **Spy** | Record calls, verify interactions | No (uses real code) |
| **Mock** | Replace module entirely | Yes |
| **Stub** | Return canned responses | Yes |
| **Fake** | Working but simplified impl | Yes |

## Decision Guide

**Use spy when:** Verifying a function was called correctly while keeping real behavior
```ts
const fetchSpy = vi.spyOn(globalThis, "fetch");
await doSomething();
expect(fetchSpy).toHaveBeenCalledWith("https://api.example.com");
```

**Use mock when:** Replacing external dependencies (network, database, third-party modules)
```ts
vi.mock("./api-client");
vi.mocked(apiClient.fetch).mockResolvedValue({ data: "test" });
```

**Use stubGlobal when:** Replacing browser/Node globals
```ts
vi.stubGlobal("fetch", vi.fn().mockResolvedValue(mockResponse));
```

## Essential Patterns

### Mock Module (hoisted)
```ts
import { someFunc } from "./module";
vi.mock("./module"); // hoisted to top

it("test", () => {
  vi.mocked(someFunc).mockReturnValue("mocked");
});
```

### Mock with Implementation
```ts
vi.mock("./module", () => ({
  someFunc: vi.fn().mockReturnValue("mocked"),
}));
```

### Spy with Fake Return
```ts
const spy = vi.spyOn(obj, "method").mockReturnValue("fake");
```

### Mock Global Fetch
```ts
globalThis.fetch = vi.fn().mockResolvedValue({
  ok: true,
  json: async () => ({ data: "test" }),
} as Response);
```

### Fake Timers
```ts
beforeAll(() => vi.useFakeTimers());
afterAll(() => vi.useRealTimers());

it("test", async () => {
  // advance time
  await vi.advanceTimersByTimeAsync(5000);
});
```

### Clean Up
```ts
beforeEach(() => vi.clearAllMocks()); // reset call counts
afterEach(() => vi.restoreAllMocks()); // restore originals
```

## Reference

For complete examples including default imports, named imports, classes, partial mocks, snapshot testing, composables, and verification patterns, see [references/cheat-sheet.md](references/cheat-sheet.md).
