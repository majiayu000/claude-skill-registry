---
name: compact-core:testing-debugging
description: Use when testing Compact contracts, debugging compile errors, understanding error messages like "potential witness-value disclosure" or "circuit constraint failed", setting up TypeScript test harnesses, or mocking witness functions for unit tests.
---

# Testing & Debugging

Essential guidance for testing Compact contracts, debugging common errors, and understanding compiler/runtime error messages.

## Common Errors Quick Reference

| Error Message | Likely Cause | Quick Fix |
|---------------|--------------|-----------|
| `potential witness-value disclosure` | Witness flows to public output | Add `disclose()` or use commitment |
| `type mismatch` | Incompatible types in operation | Check type signatures, use `as` for conversion |
| `unbounded loop` | Loop bounds not compile-time constant | Use literal or `#N` parameter for bounds |
| `circuit constraint failed` | Runtime assertion failed | Check assert conditions and inputs |
| `proof generation failed` | Invalid witness values | Verify witness function returns valid data |
| `overflow` | Arithmetic exceeds type bounds | Use larger `Uint<N>` or check bounds |

## Debugging Decision Tree

```
Error during compilation?
├── "potential witness-value disclosure"
│   └── See: references/error-messages.md#disclosure-errors
├── "type mismatch" or "cannot convert"
│   └── See: references/error-messages.md#type-errors
├── "unbounded loop" or "bounds must be constant"
│   └── See: references/error-messages.md#loop-errors
└── Other compilation error
    └── See: references/error-messages.md

Error during proof generation?
├── "assert failed" or "constraint failed"
│   └── Check assertion conditions and witness values
├── "proof generation failed"
│   └── Verify witness functions return expected types
└── "overflow" or "division by zero"
    └── Check arithmetic bounds
```

## Testing Approaches

### Unit Testing Circuits

```typescript
import { TestContext } from '@midnight-ntwrk/compact-testing';

describe('MyContract', () => {
    let ctx: TestContext;

    beforeEach(async () => {
        ctx = await TestContext.create('my_contract.compact');
    });

    it('should process valid input', async () => {
        const result = await ctx.call('process', [42n]);
        expect(result.success).toBe(true);
    });
});
```

### Witness Mocking

```typescript
const mockWitness = {
    get_secret: () => BigInt('12345'),
    get_balance: () => BigInt(1000)
};

const result = await ctx.call('transfer', [recipient], mockWitness);
```

### State Verification

```typescript
// Read ledger state after circuit execution
const balance = await ctx.ledger.get('balances', userKey);
expect(balance).toBe(expectedBalance);
```

## Common Pitfalls

| Pitfall | Symptom | Solution |
|---------|---------|----------|
| Forgetting `disclose()` | Compile error | Add explicit disclosure |
| Wrong ADT choice | Inefficient proofs | Use Counter for counting, MerkleTree for membership |
| Attempting unbounded loops | Compile error | Use bounded `for i in 0..N` |
| Uint overflow | Proof failure | Use larger bit width or check bounds |
| Division by zero | Proof failure | Add zero check before division |

## References

- [Error Messages](./references/error-messages.md) - Complete error reference with solutions
- [Testing Strategy](./references/testing-strategy.md) - Testing approaches and best practices
- [Common Pitfalls](./references/common-pitfalls.md) - Frequent mistakes and how to avoid them

## Examples

- [Test Setup](./examples/test-setup.ts) - TypeScript test harness configuration
- [Mock Witnesses](./examples/mock-witnesses.ts) - Witness mocking patterns
