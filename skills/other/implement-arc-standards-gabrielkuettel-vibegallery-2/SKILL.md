---
name: implement-arc-standards
description: Implement Algorand ARC standards in smart contracts and clients. Use when needing to understand ARC-4 ABI encoding or method signatures, working with application specifications (ARC-32 or ARC-56), calling ARC-4 methods from contracts or clients, encountering ABI encoding/decoding issues, or generating typed clients from app specs. Strong triggers include "What is ARC-4?", "How do I encode ABI arguments?", "What's the difference between ARC-32 and ARC-56?", "method selector not matching", "application specification", "arc56.json".
---

# Implement ARC Standards

ARC (Algorand Request for Comments) standards define conventions for encoding, method calls, and application specifications on Algorand. This skill covers the most essential ARCs for smart contract development.

## Overview / Core Workflow

1. Understand which ARC applies to your use case
2. Implement the contract following ARC conventions
3. Generate application specification files
4. Use the app spec to build typed clients

## How to proceed

### Key ARCs for Smart Contract Development

| ARC | Purpose | When to Use |
|-----|---------|-------------|
| **ARC-4** | Application Binary Interface (ABI) | All smart contract method calls, type encoding |
| **ARC-22** | Read-only method annotation | Methods that don't modify state |
| **ARC-28** | Event logging specification | Emitting structured events |
| **ARC-32** | Application Specification (deprecated) | Legacy app specs (use ARC-56 instead) |
| **ARC-56** | Extended App Description | Modern app specs with full contract metadata |

### ARC-4: The Foundation

ARC-4 defines how to encode method calls and data types for Algorand smart contracts.

#### Method Signatures

A method signature uniquely identifies a method: `name(arg_types)return_type`

```python
# Method signature: add(uint64,uint64)uint128
# Method selector: first 4 bytes of SHA-512/256 hash

from algopy import ARC4Contract, arc4

class Calculator(ARC4Contract):
    @arc4.abimethod
    def add(self, a: arc4.UInt64, b: arc4.UInt64) -> arc4.UInt128:
        return arc4.UInt128(a.native + b.native)
```

```typescript
import { Contract } from '@algorandfoundation/algorand-typescript'
import { abimethod, UInt64, UInt128 } from '@algorandfoundation/algorand-typescript/arc4'

class Calculator extends Contract {
  @abimethod()
  add(a: UInt64, b: UInt64): UInt128 {
    return new UInt128(a.native + b.native)
  }
}
```

#### Method Selector Calculation

```
Method signature: add(uint64,uint64)uint128
SHA-512/256 hash: 8aa3b61f0f1965c3a1cbfa91d46b24e54c67270184ff89dc114e877b1753254a
Method selector: 8aa3b61f (first 4 bytes)
```

### ARC-32 vs ARC-56

| Feature | ARC-32 | ARC-56 |
|---------|--------|--------|
| State schema | Yes | Yes |
| Method descriptions | Yes | Yes |
| Named structs | No | Yes |
| Default argument values | Partial | Full |
| Source maps | No | Yes |
| Events (ARC-28) | No | Yes |
| Status | Deprecated | Current |

**Use ARC-56** for new projects. ARC-32 is maintained for backwards compatibility.

### Generating App Specs

App specs are automatically generated when compiling with PuyaPy or PuyaTs:

```bash
# Generates ContractName.arc32.json and ContractName.arc56.json
algokit project run build
```

### Using App Specs with Clients

```typescript
// TypeScript with AlgoKit Utils
import { algorandClient } from '@algorandfoundation/algokit-utils'
import appSpec from './Calculator.arc56.json'

const client = algorand.client.getTypedAppClientById(CalculatorClient, {
  appId: 12345n,
  appSpec,
})

const result = await client.send.add({ args: { a: 10n, b: 20n } })
```

```python
# Python with AlgoKit Utils
from algokit_utils import AlgorandClient
from artifacts.calculator_client import CalculatorClient

algorand = AlgorandClient.default_localnet()
client = algorand.client.get_typed_app_client(
    CalculatorClient,
    app_id=12345,
)

result = client.send.add(a=10, b=20)
```

## Important Rules / Guidelines

| Rule | Details |
|------|---------|
| **ARC-4 types only in ABI** | Use `arc4.UInt64`, `arc4.String`, etc. for method arguments and returns |
| **Reference types as arguments only** | `account`, `asset`, `application` cannot be return types |
| **15 argument limit** | Methods with 16+ args encode extras as a tuple in arg 15 |
| **Return prefix** | Return values are logged with `151f7c75` prefix |
| **Bare methods have no selector** | Bare calls use `NumAppArgs == 0` for routing |

## Common Variations / Edge Cases

| Scenario | Approach |
|----------|----------|
| Calling ARC-4 method from contract | Use `arc4.abi_call()` for type-safe inner transactions |
| Creating contract with method | Use `create="require"` in `@abimethod` decorator |
| Read-only methods (ARC-22) | Use `readonly=True` parameter in decorator |
| Emitting events (ARC-28) | Use `arc4.emit()` with typed event structs |

## References / Further Reading

- [ARC-4 ABI Details](./references/arc4-abi.md) - Types, encoding rules, method invocation
- [ARC-32/56 App Specs](./references/arc32-arc56.md) - Application specification details
- [ARC Standards](https://dev.algorand.co/arc-standards/) - Official ARC documentation
- [Call Smart Contracts](../call-smart-contracts/SKILL.md) - Using AlgoKit Utils for ABI calls
