---
name: test-smart-contracts
description: Testing patterns for Algorand smart contracts using generated clients and algorandFixture. Use when writing tests for smart contracts, setting up test fixtures and deployment, debugging failing tests, testing multi-user scenarios, or asking about E2E vs unit testing. Strong triggers include "how do I test my contract", "algorandFixture", "test is failing", "LocalNet testing", "vitest setup", "fund contract for boxes".
---

# Testing Smart Contracts

Write integration tests for Algorand smart contracts using the `algorandFixture` and generated typed clients.

## Default: Integration Tests (E2E)

**Always write integration tests unless the user explicitly requests unit tests.** Integration tests run against LocalNet and test real contract behavior.

**Test Framework**: Both Vitest (default) and Jest are supported. The examples below use Vitest syntax, but Jest equivalents work identically.

### File naming

- Integration tests: `contract.algo.e2e.spec.ts`
- Unit tests (only if requested): `contract.algo.spec.ts`

### Canonical Example

Study and adapt from: [devportal-code-examples/contracts/HelloWorld](https://github.com/algorandfoundation/devportal-code-examples/tree/main/projects/typescript-examples/contracts/HelloWorld)

```typescript
import { Config } from '@algorandfoundation/algokit-utils'
import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { Address } from 'algosdk'
import { beforeAll, beforeEach, describe, expect, test } from 'vitest'
import { MyContractFactory } from '../artifacts/clients/MyContract/MyContractClient'

describe('MyContract', () => {
  const localnet = algorandFixture()

  beforeAll(() => {
    Config.configure({ debug: true })
  })
  // 10-second timeout: LocalNet needs time to process transactions and confirm blocks
  beforeEach(localnet.newScope, 10_000)

  const deploy = async (account: Address) => {
    const factory = localnet.algorand.client.getTypedAppFactory(MyContractFactory, {
      defaultSender: account,
    })
    const { appClient } = await factory.deploy({
      onUpdate: 'append',
      onSchemaBreak: 'append',
      suppressLog: true,
    })
    return { client: appClient }
  }

  test('should call method and verify result', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    const result = await client.send.myMethod({ args: { value: 42n } })
    expect(result.return).toBe(42n)
  })
})
```

## How to proceed

1. **Locate the generated client** in `artifacts/clients/<ContractName>/<ContractName>Client.ts`
2. **Import the Factory** (e.g., `MyContractFactory`) - NOT the Client directly
3. **Use the deploy helper pattern** shown above
4. **Call methods via `client.send.methodName()`** or `client.newGroup().methodName().send()`

## Critical Rules

| Rule | Details |
|------|---------|
| **Use newGroup() for chaining** | `client.newGroup().method1().method2().send()` |
| **Struct returns are tuples** | `const [id, name] = result.return as [bigint, string]` |
| **Fund app for BoxMap** | Send payment to `client.appAddress` before box operations |
| **Opt-in before local state** | `await client.newGroup().optIn.optInToApplication().send()` |

## Common Patterns

### Fund contract for box storage

```typescript
await localnet.algorand.send.payment({
  amount: (1).algo(),
  sender: testAccount,
  receiver: client.appAddress,
})
```

### Multiple users on same contract

```typescript
// Create and fund second user
const user2 = localnet.algorand.account.random()
await localnet.algorand.send.payment({
  amount: (5).algo(),
  sender: testAccount,
  receiver: user2.addr,
})

// Get client for same app with different sender
const client2 = factory.getAppClientById({
  appId: client.appId,
  defaultSender: user2.addr,
})
```

### Box references

```typescript
import { ABIUintType } from 'algosdk'

function createBoxReference(appId: bigint, prefix: string, key: bigint) {
  const uint64Type = new ABIUintType(64)
  const encodedKey = uint64Type.encode(key)
  const boxName = new Uint8Array([...new TextEncoder().encode(prefix), ...encodedKey])
  return { appId, name: boxName }
}

await client.send.setBoxMap({
  args: { key: 1n, value: 'hello' },
  boxReferences: [createBoxReference(client.appId, 'boxMap', 1n)],
})
```

## References

- [Canonical Examples](./references/EXAMPLES.md) - Complete patterns from algorandfoundation repos
- [Unit Testing Guide](./references/UNIT_TESTS.md) - Only use if user requests unit tests
- [devportal-code-examples](https://github.com/algorandfoundation/devportal-code-examples/tree/main/projects/typescript-examples/contracts)
