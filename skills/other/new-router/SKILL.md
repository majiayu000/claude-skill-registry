---
name: new-router
description: Scaffold a new tRPC router with repository, interface, tests, and barrel exports following project conventions
disable-model-invocation: true
---

# New Router Runbook

## Files to Create

Given a domain name `<domain>` (e.g., "invoice"):

1. **Repository interface**: `src/server/repositories/<domain>-repository.ts`
2. **Repository implementation**: (in same file or separate)
3. **Router**: `src/server/routers/<domain>.ts`
4. **Unit tests**: `src/server/routers/__tests__/<domain>.test.ts`
5. **Register in app router**: `src/server/routers/_app.ts`

## Repository Template

See `src/server/CLAUDE.md` for the full repository pattern. Key points:
- Implement an interface with typed methods
- Use `Partial<SchemaType>` for update data (never `Record<string, unknown>`)
- Always scope queries by `userId` / `ownerId`
- Return typed values (never `Promise<unknown>`)

## Router Template

See `src/server/CLAUDE.md` for the router template. Key points:
- Routers are thin controllers — data access through `ctx.uow`
- Use `protectedProcedure` for reads, `writeProcedure` for mutations
- Use `proProcedure` / `teamProcedure` for gated features
- Always validate input with Zod schemas
- Use `.returning()` on insert/update

## Test Template

```typescript
import { describe, it, expect, vi, beforeEach } from "vitest";
import { createMockUow } from "@/server/test-utils";

describe("<domain> router", () => {
  const mockUow = createMockUow();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("lists items for the owner", async () => {
    // Arrange
    mockUow.<domain>.findByOwner.mockResolvedValue([]);
    // Act
    const result = await caller.list();
    // Assert
    expect(result).toEqual([]);
  });
});
```

## Registration

Add to `src/server/routers/_app.ts`:
```typescript
import { <domain>Router } from "./<domain>";
// In the router() call:
<domain>: <domain>Router,
```

## Checklist

- [ ] Repository interface with typed methods
- [ ] Router with appropriate procedure types
- [ ] Unit tests covering list, get, create, update, delete
- [ ] Registered in `_app.ts`
- [ ] Input validation with Zod
- [ ] User scoping on all queries (`ctx.portfolio.ownerId`)
