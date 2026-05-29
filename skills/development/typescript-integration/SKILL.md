---
name: compact-core:typescript-integration
description: Use when implementing witness functions in TypeScript, mapping Compact types to TypeScript (Field→bigint, Bytes→Uint8Array), deploying contracts, calling circuits from TypeScript, reading ledger state, or building Midnight DApps with the JavaScript SDK.
---

# TypeScript Integration

Complete guide to integrating Midnight Compact contracts with TypeScript applications.

## Type Mapping Quick Reference

| Compact Type | TypeScript Type | Notes |
|--------------|-----------------|-------|
| `Field` | `bigint` | ZK field element |
| `Uint<N>` | `bigint` | Any bit width maps to bigint |
| `Boolean` | `boolean` | Direct mapping |
| `Bytes<N>` | `Uint8Array` | Fixed-length byte array |
| `Opaque<'string'>` | `string` | UTF-8 string data |
| `Opaque<'Uint8Array'>` | `Uint8Array` | Binary data |
| `struct` | `{ field: Type, ... }` | Object with typed fields |
| `enum` | Discriminated union | `{ tag: 'Variant', value: T }` |
| `Vector<T, N>` | `T[]` | Array of mapped type |

## Witness Implementation Pattern

```typescript
import { WitnessContext } from '@midnight-ntwrk/midnight-js-types';

// Compact declaration: witness get_secret(): Field;
const witnesses = {
  get_secret: ({ privateState }: WitnessContext<PrivateState>): bigint => {
    return privateState.secret;
  }
};
```

## Contract Interaction Flow

```
1. Compile Compact → Generated TypeScript types
2. Deploy contract → Get contract address
3. Create provider → Connect to Midnight node
4. Build witnesses → Implement private data access
5. Call circuits → Execute transactions
6. Read state → Query ledger values
```

## Quick Examples

### Calling a Circuit

```typescript
import { Contract } from './contract';

const result = await contract.callTx.transfer({
  to: recipientAddress,
  amount: 1000n
}, witnesses);
```

### Reading Ledger State

```typescript
const balance = await contract.state.balances.get(userAddress);
// balance: bigint | undefined
```

### Deploying a Contract

```typescript
import { deployContract } from '@midnight-ntwrk/midnight-js-contracts';

const { contract, address } = await deployContract(provider, {
  privateStateKey: 'my-contract',
  initialPrivateState: { secret: 42n },
  witnesses
});
```

## References

For detailed documentation on each topic:

- [Type Mapping](./references/type-mapping.md) - Complete Compact ↔ TypeScript type correspondence
- [Witness Bridge](./references/witness-bridge.md) - Implementing witnesses in TypeScript
- [Contract API](./references/contract-api.md) - Generated contract interface usage
- [Deployment](./references/deployment.md) - Contract deployment from TypeScript

## Examples

Working TypeScript examples:

- [Witness Implementation](./examples/witness-impl.ts) - Complete witness patterns
- [Deploy Contract](./examples/deploy-contract.ts) - Contract deployment flow
- [Read State](./examples/read-state.ts) - Reading ledger state
