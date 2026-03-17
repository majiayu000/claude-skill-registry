---
name: testing
description: Test infrastructure reference for Shadow Master. Use when writing tests, finding existing test files, or running test suites. Covers Vitest unit tests, Playwright E2E tests, and testing patterns.
allowed-tools: Read, Grep, Glob, Bash
---

# Testing Reference

Shadow Master uses Vitest for unit/integration tests and Playwright for E2E browser tests.

## Test Commands

```bash
pnpm test              # Run all unit tests
pnpm test:watch        # Watch mode for development
pnpm test:ci           # CI mode (no watch, exits with code)
pnpm test:e2e          # Run Playwright E2E tests
pnpm test:e2e:ui       # E2E with visual UI for debugging
```

## Test Enforcement Scripts

```bash
pnpm check-tests       # Check staged files for missing tests (non-blocking)
pnpm check-tests:all   # Check all source files for missing tests
pnpm check-tests:strict # Strict mode (fails if tests are missing)
```

---

## Test File Locations

Tests are co-located with source code in `__tests__` directories:

```
/__tests__/                                    # Root level tests
/lib/auth/__tests__/                           # Auth unit tests (3 files)
/lib/storage/__tests__/                        # Storage layer tests (10 files)
/lib/security/__tests__/                       # Security tests (1 file)
/lib/rules/__tests__/                          # Core rules tests (8 files)
/lib/rules/action-resolution/__tests__/        # Action resolution tests (2 files)
/lib/rules/action-resolution/combat/__tests__/ # Combat handler tests (2 files)
/lib/rules/advancement/__tests__/              # Advancement logic tests (8 files)
/lib/rules/augmentations/__tests__/            # Augmentation tests (6 files)
/lib/rules/character/__tests__/                # Character state machine tests (1 file)
/lib/rules/encumbrance/__tests__/              # Encumbrance tests (1 file)
/lib/rules/gear/__tests__/                     # Gear validation tests (2 files)
/lib/rules/inventory/__tests__/                # Inventory tests (1 file)
/lib/rules/magic/__tests__/                    # Magic system tests (5 files)
/lib/rules/matrix/__tests__/                   # Matrix tests (1 file)
/lib/rules/qualities/__tests__/                # Quality system tests (7 files)
/lib/rules/rigging/__tests__/                  # Rigging tests (2 files)
/app/api/**/__tests__/                         # API route tests (~25 files)
/e2e/                                          # Playwright E2E tests
```

---

## Writing Tests

### Unit Test Pattern (Vitest)

```typescript
import { describe, it, expect, beforeEach } from "vitest";
import { myFunction } from "../myModule";

describe("myFunction", () => {
  beforeEach(() => {
    // Setup
  });

  it("should handle normal case", () => {
    const result = myFunction(input);
    expect(result).toBe(expected);
  });

  it("should handle edge case", () => {
    expect(() => myFunction(badInput)).toThrow();
  });
});
```

### API Route Test Pattern

```typescript
import { describe, it, expect, vi, beforeEach } from "vitest";
import { GET, POST } from "../route";
import { NextRequest } from "next/server";

// Mock auth
vi.mock("@/lib/auth/session", () => ({
  getSession: vi.fn(),
}));

describe("GET /api/endpoint", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns 401 when unauthenticated", async () => {
    const request = new NextRequest("http://localhost/api/endpoint");
    const response = await GET(request);
    expect(response.status).toBe(401);
  });
});
```

---

## Manual Testing Workflow

1. Create test user via `/signup`
2. Test character creation via `/characters/create/sheet` end-to-end
3. Check `/data` directory for persisted JSON
4. Verify authentication by signing out and back in
5. Test draft auto-save by refreshing page mid-creation (drafts persist server-side)

---

## Test Coverage Focus

Priority areas for test coverage:

1. **Rules logic** (`/lib/rules/`) - Core game mechanics must be correct
2. **Storage operations** (`/lib/storage/`) - Data integrity is critical
3. **Auth flows** (`/lib/auth/`) - Security-sensitive code
4. **API routes** (`/app/api/`) - User-facing endpoints
5. **Character creation** - Complex state management
