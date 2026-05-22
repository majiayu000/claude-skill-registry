---
name: trpc
description: tRPC v11 API layer with Zod and Ed25519 auth. Use when working on files in src/server/.
---

# tRPC Guidelines

## Authentication

All authenticated procedures verify Ed25519 signatures:
- Verify signature matches pubkeyHash
- Verify timestamp is recent (prevent replay)
- Verify message matches request

## Patterns

**Router:**
```typescript
export const vaultRouter = router({
  create: authedProcedure
    .input(createVaultSchema)
    .mutation(async ({ ctx, input }) => { ... }),
});
```

**Schema:**
```typescript
export const createVaultSchema = z.object({
  name: z.string().min(1).max(100),
  encryptedSnapshot: z.string(),
  wrappedKey: z.string(),
});
```

## Critical Rules

1. **Never trust client data** - always validate with Zod
2. **Never store unencrypted data** - all sensitive data comes pre-encrypted
3. **Verify signatures** - every mutation must be signed
4. **Check permissions** - verify user has vault access
5. **Use transactions** - wrap multi-step operations

## Error Handling

```typescript
throw new TRPCError({
  code: "NOT_FOUND", // or "FORBIDDEN"
  message: "Vault not found",
});
```
