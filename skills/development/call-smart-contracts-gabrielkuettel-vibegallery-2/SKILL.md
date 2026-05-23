---
name: call-smart-contracts
description: Deploy and interact with Algorand smart contracts using AlgoKit CLI and generated TypeScript clients. Use when deploying contracts to localnet/testnet/mainnet, calling contract methods, reading global/local/box state, opting in or closing out of applications, or writing interaction scripts. Strong triggers include "deploy the contract", "call the increment method", "read the contract state", "opt into the app", "write a script to interact", "getTypedAppClientById".
---

# Calling Smart Contracts

Deploy and interact with Algorand smart contracts using AlgoKit CLI and the generated TypeScript client.

## Overview / Core Workflow

1. Build the contract: `algokit project run build`
2. Deploy using CLI: `algokit project deploy localnet`
3. Write TypeScript scripts using the generated client
4. Run scripts: `npx tsx scripts/my-script.ts`

## How to proceed

### 1. Build the Contract

```bash
algokit project run build
```

This compiles your contract and generates:
- `artifacts/<ContractName>/<ContractName>.arc56.json` — ARC-56 app spec
- `artifacts/<ContractName>/client.ts` — Generated TypeScript client

### 2. Deploy to Localnet

```bash
# Start localnet if not running
algokit localnet start

# Deploy (runs deploy-config.ts)
algokit project deploy localnet
```

The deployment script (`smart_contracts/deploy-config.ts`) handles:
- Idempotent deployment (safe to re-run)
- App ID tracking
- Initial state setup

Note the App ID from the deployment output.

### 3. Interact Using Generated Client

Create scripts in your project to call contract methods. Example structure:

```typescript
// scripts/call-contract.ts
import { AlgorandClient } from '@algorandfoundation/algokit-utils'
import { CounterClient } from '../smart_contracts/artifacts/Counter/client'

async function main() {
  // Connect to localnet
  const algorand = AlgorandClient.fromEnvironment()

  // Get the default account (localnet dispenser)
  const deployer = await algorand.account.fromEnvironment('DEPLOYER')

  // Create client for deployed app
  const client = algorand.client.getTypedAppClientById(CounterClient, {
    appId: BigInt(1234), // Replace with actual App ID
    sender: deployer,
  })

  // Call a method
  const result = await client.send.increment({})
  console.log('New count:', result.return)

  // Read global state
  const state = await client.state.global.getAll()
  console.log('Global state:', state)
}

main().catch(console.error)
```

Run with:
```bash
npx tsx scripts/call-contract.ts
```

### 4. Common Operations

#### Call a Method

```typescript
// No arguments
const result = await client.send.increment({})

// With arguments
const result = await client.send.setValue({ args: { value: 42n } })

// Access return value
console.log('Return:', result.return)
```

#### Read Global State

```typescript
// Get all global state
const state = await client.state.global.getAll()

// Get specific key (if typed in contract)
const count = await client.state.global.count()
```

#### Read Local State

```typescript
// Get local state for an address
const localState = await client.state.local(address).getAll()
```

#### Opt-In to Application

```typescript
// If contract has an opt_in method
await client.send.optIn.optIn({})

// Or use bare opt-in
await client.send.optIn.bare({})
```

#### Read Box Storage

```typescript
// If contract uses boxes
const boxValue = await client.state.box.myBox()
```

#### Bulk Opt-In/Opt-Out

For batch operations across multiple assets:

```typescript
// Bulk opt-in to multiple assets
const group = algorand.newGroup()
for (const assetId of assetIds) {
  group.addAssetOptIn({ sender: account.addr, assetId })
}
await group.send()

// Bulk opt-out from multiple assets
const closeGroup = algorand.newGroup()
for (const assetId of assetIds) {
  closeGroup.addAssetOptOut({ sender: account.addr, assetId, creator: creatorAddr })
}
await closeGroup.send()
```

## Important Rules / Guidelines

- **Always build before deploying**: Run `algokit project run build` to generate fresh artifacts
- **Use generated clients**: They provide type safety and handle ABI encoding
- **Check App ID**: Get it from deployment output, don't hardcode across environments
- **Use environment variables**: Store sensitive data like mnemonics in `.env`
- **Localnet accounts**: Use `algorand.account.fromEnvironment('DEPLOYER')` for localnet

## Common Variations / Edge Cases

| Scenario | Approach |
|----------|----------|
| Deploy to testnet | `algokit project deploy testnet` (requires funded account) |
| Custom sender | Create account with `algorand.account.fromMnemonic()` |
| Multiple contracts | Create separate client instances for each |
| State not found | Ensure app is deployed and App ID is correct |
| Method not found | Rebuild contract and regenerate client |

## Environment Setup

For non-localnet deployments, set environment variables:

```bash
# .env file
ALGORAND_NETWORK=testnet
DEPLOYER_MNEMONIC="your twenty four word mnemonic phrase here"
```

## References / Further Reading

- [CLI Commands Reference](./references/REFERENCE.md)
- [AlgoKit Utils Documentation](https://dev.algorand.co/algokit/utils/typescript/)
- [ARC-56 App Spec Standard](https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0056.md)
- [Testing Contracts](../test-smart-contracts/SKILL.md)
