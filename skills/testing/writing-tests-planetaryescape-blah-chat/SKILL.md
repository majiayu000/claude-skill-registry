---
name: writing-tests
description: Write user-centric tests following Kent C. Dodds principles. Use when asked to write tests for components, hooks, or features. Generates tests that test behavior, use accessibility queries, and mock only at boundaries.
license: MIT
---

# Writing Tests Skill

Write tests that give confidence the app works for users, not that code is structured a certain way.

## Core Philosophy

**"The more your tests resemble the way your software is used, the more confidence they can give you."** - Kent C. Dodds

1. **Test behavior, not implementation** - Test what users see and do
2. **Use accessibility queries** - `getByRole`, `getByLabelText` over `getByTestId`
3. **Mock at boundaries only** - Network/Convex hooks, not components
4. **Integration tests > unit tests** - Test real workflows

## Query Priority

| Priority | Query | When |
|----------|-------|------|
| 1 | `getByRole` | Semantic HTML elements |
| 2 | `getByLabelText` | Form fields |
| 3 | `getByText` | Buttons, links |
| 4 | `getByTestId` | **LAST RESORT** |

## Existing Infrastructure (USE THESE)

**DO NOT create new test utilities.** Use:

```typescript
// Factories - src/lib/test/factories.ts
import { createOptimisticMessage, createTestMessageData, createTestUserData, createTestConversationData, createMockIdentity } from "@/lib/test/factories";

// API helpers - src/lib/test/api-helpers.ts
import { createMockRequest, assertEnvelopeSuccess, assertEnvelopeError, unwrapData } from "@/lib/test/api-helpers";
```

## Test Patterns

### Component Tests

```typescript
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi, beforeEach } from "vitest";

// Mock BEFORE importing component
vi.mock("convex/react", () => ({
  useQuery: vi.fn(() => null),
  useMutation: vi.fn(() => vi.fn()),
}));

const mockMutation = vi.fn();
vi.mock("@/lib/hooks/mutations", () => ({
  useSendMessage: () => ({ mutate: mockMutation, isPending: false }),
}));

// Import AFTER mocks
import { MyComponent } from "../MyComponent";

describe("MyComponent", () => {
  beforeEach(() => vi.clearAllMocks());

  it("sends data when user submits", async () => {
    const user = userEvent.setup();
    render(<MyComponent {...props} />);

    // Use accessibility queries
    const input = screen.getByLabelText("Message input");
    await user.type(input, "Hello{Enter}");

    expect(mockMutation).toHaveBeenCalledWith(
      expect.objectContaining({ content: "Hello" })
    );
  });
});
```

### Convex Tests

```typescript
import { convexTest } from "convex-test";
import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { api } from "../_generated/api";
import schema from "../schema";
import { createMockIdentity, createTestUserData, createTestConversationData } from "@/lib/test/factories";

describe("conversations", () => {
  // Use fake timers if testing scheduled functions
  beforeEach(() => vi.useFakeTimers());
  afterEach(() => vi.useRealTimers());

  it("returns only user's conversations", async () => {
    const t = convexTest(schema);
    const identity = createMockIdentity();

    await t.run(async (ctx) => {
      const userId = await ctx.db.insert("users", createTestUserData({
        clerkId: identity.subject,
      }));
      await ctx.db.insert("conversations", createTestConversationData(userId));
    });

    const asUser = t.withIdentity(identity);
    // @ts-ignore - Type depth exceeded with 94+ Convex modules
    const result = await asUser.query(api.conversations.list, {});

    expect(result).toHaveLength(1);
  });
});
```

### API Route Tests

```typescript
// Mocks MUST be BEFORE imports
vi.mock("@/lib/api/dal/conversations", () => ({
  conversationsDAL: { list: vi.fn(), create: vi.fn() },
}));

import { conversationsDAL } from "@/lib/api/dal/conversations";
import { createMockRequest, assertEnvelopeSuccess } from "@/lib/test/api-helpers";

describe("/api/v1/conversations", () => {
  beforeEach(() => vi.clearAllMocks());

  it("returns list with envelope", async () => {
    vi.mocked(conversationsDAL.list).mockResolvedValue([]);

    // Dynamic import AFTER mock setup
    const { GET } = await import("../route");
    const response = await GET(createMockRequest("/api/v1/conversations"));
    const json = await response.json();

    assertEnvelopeSuccess(json);
  });
});
```

## What to Mock

**Mock:**
- `convex/react` hooks (useQuery, useMutation)
- Custom mutation hooks (`@/lib/hooks/mutations`)
- DAL modules (`@/lib/api/dal/*`)
- Browser APIs (localStorage, clipboard)
- System clock (`vi.useFakeTimers()`)

**Don't Mock:**
- Child components
- Domain objects
- React itself
- CSS/styling

## Anti-Patterns to Avoid

```typescript
// BAD: Over-mocking
vi.mock("./ChildA");
vi.mock("./ChildB");
vi.mock("../hooks/useX");

// BAD: Testing implementation
expect(component.state.loading).toBe(true);

// BAD: Snapshot for behavior
expect(component).toMatchSnapshot();

// BAD: Test IDs when a11y query works
screen.getByTestId("submit-button");
```

## File Locations

| Test Type | Location |
|-----------|----------|
| Component | `src/components/[name]/__tests__/[Name].test.tsx` |
| Convex | `convex/__tests__/[name].test.ts` |
| API Route | `src/app/api/v1/__tests__/[name].test.ts` |
| Utility | `src/lib/[path]/__tests__/[name].test.ts` |
| E2E | `e2e/[name].spec.ts` |

## Reference

Full philosophy: `docs/testing/testing-philosophy.md`
Phase docs: `docs/testing/phase-*.md`
