---
name: midnight-tooling:contract-calling
description: Use when calling deployed Midnight contracts from Node.js backends, querying contract state, executing state-changing transactions, building API endpoints that interact with contracts, or automating contract interactions.
---

# Contract Calling

Interact with deployed Midnight contracts from Node.js backends, including read-only queries and state-changing transactions with proof generation.

## When to Use

- Querying contract state from a backend service
- Executing state-changing transactions
- Building API endpoints that interact with contracts
- Automating contract interactions in scripts
- Testing contract behavior programmatically

## Key Concepts

### Call Types

| Type | Proof Required | State Change | Gas Cost | Use Case |
|------|----------------|--------------|----------|----------|
| Read-only query | No | No | None | Fetching current state |
| State change | Yes | Yes | Variable | Updating ledger state |

### Contract Client Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Your Code  │────▶│   Contract   │────▶│   Prover    │
│             │     │    Client    │     │   Service   │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐     ┌─────────────┐
                    │   Indexer    │────▶│  Midnight   │
                    │    Client    │     │   Network   │
                    └──────────────┘     └─────────────┘
```

### Circuit Types in Compact

Compact contracts define circuits that can be invoked:

```compact
// Read-only circuit - no proof needed
circuit get_balance(address: Address): Uint {
  return ledger.balances[address];
}

// State-changing circuit - requires proof
circuit transfer(to: Address, amount: Uint): Void {
  // Generates proof, updates ledger
  ledger.balances[sender] -= amount;
  ledger.balances[to] += amount;
}
```

## References

| Document | Description |
|----------|-------------|
| [api-client-setup.md](references/api-client-setup.md) | SDK initialization and wallet connection |
| [error-handling.md](references/error-handling.md) | Error types, retries, and timeout handling |

## Examples

| Example | Description |
|---------|-------------|
| [read-query/](examples/read-query/) | Query contract state without proofs |
| [state-change/](examples/state-change/) | Execute state-changing transactions |

## Quick Start

### 1. Connect to Deployed Contract

```typescript
import { connectContract } from '@midnight-ntwrk/midnight-js-contracts';
import { createWallet } from '@midnight-ntwrk/midnight-js-wallet';
import { Contract } from './build/contract.cjs';

const wallet = await createWallet({ seed: process.env.WALLET_SEED! });

const contract = await connectContract({
  address: '0x1234...', // Deployed contract address
  artifact: Contract,
  wallet,
  config: {
    indexer: 'https://indexer.testnet.midnight.network',
    indexerWs: 'wss://indexer.testnet.midnight.network/ws',
    prover: 'https://prover.testnet.midnight.network',
  },
});
```

### 2. Read-Only Query

```typescript
// Call read-only circuit (no proof generation)
const balance = await contract.query.get_balance({
  address: '0xabc...',
});

console.log('Balance:', balance);
```

### 3. State-Changing Transaction

```typescript
// Call state-changing circuit (generates proof)
const result = await contract.call.transfer({
  to: '0xdef...',
  amount: 100n,
});

// Wait for confirmation
const confirmed = await result.waitForConfirmation();
console.log('Transfer confirmed:', confirmed.txHash);
```

## Common Patterns

### Building a Contract API Client

```typescript
import { connectContract } from '@midnight-ntwrk/midnight-js-contracts';
import type { ContractMethods, ContractState } from './build/contract.d.cts';

class TokenClient {
  private contract: ConnectedContract<ContractState, ContractMethods>;

  static async connect(
    address: string,
    wallet: Wallet,
    config: NetworkConfig
  ): Promise<TokenClient> {
    const client = new TokenClient();
    client.contract = await connectContract({
      address,
      artifact: Contract,
      wallet,
      config,
    });
    return client;
  }

  async getBalance(address: string): Promise<bigint> {
    return this.contract.query.get_balance({ address });
  }

  async transfer(to: string, amount: bigint): Promise<TransactionResult> {
    const result = await this.contract.call.transfer({ to, amount });
    return result.waitForConfirmation();
  }
}
```

### Batch Queries

```typescript
async function batchGetBalances(
  contract: ConnectedContract,
  addresses: string[]
): Promise<Map<string, bigint>> {
  const results = new Map<string, bigint>();

  // Run queries in parallel
  const balances = await Promise.all(
    addresses.map((addr) =>
      contract.query.get_balance({ address: addr })
        .then((balance) => ({ addr, balance }))
    )
  );

  for (const { addr, balance } of balances) {
    results.set(addr, balance);
  }

  return results;
}
```

### Transaction with Confirmation

```typescript
interface TransactionOptions {
  timeout?: number;
  confirmations?: number;
  onProofProgress?: (progress: number) => void;
}

async function executeTransaction<T>(
  callFn: () => Promise<PendingTransaction<T>>,
  options: TransactionOptions = {}
): Promise<ConfirmedTransaction<T>> {
  const { timeout = 120000, confirmations = 1, onProofProgress } = options;

  const pending = await callFn();

  // Monitor proof generation progress
  if (onProofProgress) {
    pending.onProgress(onProofProgress);
  }

  const result = await pending.waitForConfirmation({
    timeout,
    confirmations,
  });

  if (result.status !== 'confirmed') {
    throw new Error(`Transaction failed: ${result.error || 'timeout'}`);
  }

  return result;
}

// Usage
const result = await executeTransaction(
  () => contract.call.transfer({ to: recipient, amount: 100n }),
  {
    timeout: 180000,
    onProofProgress: (p) => console.log(`Proof: ${(p * 100).toFixed(0)}%`),
  }
);
```

### Handling Private Inputs

```typescript
// For circuits with private witness data
const result = await contract.call.private_transfer({
  to: recipient,
  amount: 100n,
  // Private inputs are handled by the SDK
  // They never leave your backend
});
```

## Error Handling

Common errors when calling contracts:

| Error | Cause | Solution |
|-------|-------|----------|
| `Contract not found` | Invalid address | Verify contract address |
| `Proof generation failed` | Invalid witness | Check circuit inputs |
| `Insufficient balance` | Low DUST | Fund wallet |
| `Circuit execution failed` | Assertion violated | Review circuit logic |
| `Timeout` | Slow network/prover | Increase timeout |

See [error-handling.md](references/error-handling.md) for detailed error recovery strategies.

## Related Skills

- `contract-deployment` - Deploying contracts before calling
- `lifecycle-management` - Managing contract state
- `midnight-proofs` plugin - Server-side proof optimization

## Related Commands

- `/midnight:check` - Verify environment is configured
