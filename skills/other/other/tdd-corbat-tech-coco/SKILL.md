---
name: tdd
description: Enforce test-driven development workflow. Scaffold interfaces → write FAILING tests → implement minimal code → refactor. Ensures 80%+ Vitest coverage. NEVER write implementation before tests.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# TDD — Test-Driven Development

Invoke the **tdd-guide** agent to enforce the RED → GREEN → REFACTOR cycle.

## The Non-Negotiable Rule

```
RED   → Write failing tests FIRST
GREEN → Implement minimum code to pass
REFACTOR → Improve while keeping green
```

**Never write implementation before tests. Never skip RED phase.**

## Phase 1: Interface First

Before any tests, define the contract:

```typescript
// 1a. Define input/output types
export interface FeatureInput {
  // ... explicit types, no any
}

export interface FeatureResult {
  success: boolean;
  data?: OutputType;
  error?: string;
}

// 1b. Create stub (throws "Not implemented")
export async function feature(input: FeatureInput): Promise<FeatureResult> {
  throw new Error("Not implemented — write tests first");
}
```

## Phase 2: RED — Write ALL Failing Tests

Create `src/path/my-feature.test.ts` BEFORE touching the implementation.

Write ALL test cases up front:

```typescript
import { describe, it, expect, vi, beforeEach } from "vitest";
import { feature } from "./feature.js";

// Mock LLM provider if needed
vi.mock("../../providers/index.js", () => ({ ... }));

describe("feature", () => {
  beforeEach(() => vi.clearAllMocks());

  // Group 1: Happy path
  describe("success cases", () => {
    it("processes valid input correctly", async () => { ... });
    it("handles optional parameters", async () => { ... });
  });

  // Group 2: Edge cases
  describe("edge cases", () => {
    it("handles empty input", async () => { ... });
    it("handles maximum boundary values", async () => { ... });
  });

  // Group 3: Error cases
  describe("error handling", () => {
    it("returns error for invalid input", async () => { ... });
    it("handles unexpected errors", async () => {
      await expect(feature({ input: "error" })).resolves.toMatchObject({
        success: false,
      });
    });
  });

  // Group 4: Concurrent access (if applicable)
  describe("concurrent access", () => {
    it("handles parallel calls safely", async () => { ... });
  });
});
```

Run and confirm ALL fail:
```bash
pnpm test src/path/feature.test.ts
# Should show: X tests failed ← correct!
```
✅ Tests failing = correct. Proceed.

## Phase 3: GREEN — Minimal Implementation

Write ONLY the code needed to make tests pass:
- No early optimization
- No extra features
- No future-proofing
- Just pass the tests

Run after EACH test group to confirm progress:
```bash
pnpm test src/path/feature.test.ts
```
✅ Tests passing = proceed to refactor.

## Phase 4: REFACTOR

Only after ALL tests pass:

### Refactoring Checklist
- [ ] Extract functions > 50 lines
- [ ] Remove duplication (DRY)
- [ ] Improve naming clarity
- [ ] Add JSDoc to exported functions
- [ ] Replace `console.log` with `getLogger()`
- [ ] Remove `any` types
- [ ] Add missing `.js` extensions to imports
- [ ] Simplify complex conditionals (early returns)

Run tests after EACH change:
```bash
pnpm test src/path/feature.test.ts
```

## Phase 5: Coverage Check

```bash
pnpm test:coverage -- --reporter=text src/path/
```

Check coverage report. If < 80%:
- Identify uncovered lines
- Write tests for uncovered paths
- Repeat until 80%+

| Type | Minimum |
|------|---------|
| General | 80% |
| Quality analyzers | 80% |
| Security-critical | 100% |
| Config validation | 100% |

## Phase 6: Full Suite

```bash
pnpm check  # typecheck + lint + ALL tests
```

Must be fully green before considering the feature done.

## corbat-coco Specific Patterns

### Testing Quality Analyzers
```typescript
import { analyzeComplexity } from "./complexity-analyzer.js";

it("detects deeply nested code as high complexity", async () => {
  const code = `
    function nested() {
      if (a) { if (b) { if (c) { if (d) { return 1; } } } }
    }
  `;
  const result = await analyzeComplexity(code);
  expect(result.score).toBeLessThan(60); // high complexity = low score
});
```

### Testing Tool Registry
```typescript
it("registers tool and executes successfully", async () => {
  const registry = createToolRegistry();
  registerMyTool(registry);

  expect(registry.has("myTool")).toBe(true);
  const result = await registry.execute("myTool", { valid: "input" });
  expect(result.success).toBe(true);
});
```

## Usage

```
/tdd implement the new codebase-map tool
/tdd fix the provider timeout bug (with reproducing test first)
/tdd add validation to the quality evaluator
```
