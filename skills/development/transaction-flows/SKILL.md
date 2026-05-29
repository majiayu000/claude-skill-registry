---
name: midnight-dapp:transaction-flows
description: Use when submitting transactions to Midnight contracts, tracking transaction status, implementing retry logic, building responsive UIs during proof generation, or understanding the build-prove-submit-confirm flow.
---

# Transaction Flows

Submit, track, and handle transactions through the complete Midnight lifecycle: build, prove, submit, and confirm.

## When to Use

- Submitting transactions to Midnight contracts
- Tracking transaction status and confirmation
- Implementing retry logic for failed submissions
- Building responsive UIs during proof generation
- Understanding the differences from Ethereum transactions

## Key Concepts

### Build-Prove-Submit-Confirm Flow

Midnight transactions go through four distinct phases:

1. **Build**: Create transaction with `contract.callTx.*` and witness data
2. **Prove**: Wallet generates ZK proof via local proof server (seconds)
3. **Submit**: Send proven transaction with `walletAPI.submitTransaction()`
4. **Confirm**: Wait for finality on the Midnight network

```typescript
// Complete transaction flow
const tx = await contract.callTx.transfer(recipient, amount, witnesses);
const provenTx = await walletAPI.balanceAndProveTransaction(tx, newCoins);
const txHash = await walletAPI.submitTransaction(provenTx);
// Wait for confirmation...
```

### User Experience Implications

Unlike Ethereum's instant signing, Midnight proof generation takes several seconds. Your UI must:

- Show loading states during proof generation
- Provide progress indicators when possible
- Handle timeouts gracefully
- Support cancellation
- Allow retries on failure

## References

| Document | Description |
|----------|-------------|
| [transaction-lifecycle.md](references/transaction-lifecycle.md) | Complete transaction flow with state transitions |
| [signing-flow.md](references/signing-flow.md) | Wallet signing and proof generation details |
| [confirmation-patterns.md](references/confirmation-patterns.md) | Polling, finality, and UI update strategies |
| [web3-comparison.md](references/web3-comparison.md) | Ethereum transaction patterns vs Midnight |

## Examples

| Example | Description |
|---------|-------------|
| [submit-transaction/](examples/submit-transaction/) | Complete transaction submission flow |
| [tx-status-tracker/](examples/tx-status-tracker/) | Transaction status tracking UI |
| [retry-patterns/](examples/retry-patterns/) | Exponential backoff and retry UI |

## Quick Start

### 1. Build the Transaction

```typescript
import type { WitnessContext } from "@midnight-ntwrk/midnight-js-types";

// Define witnesses for private data
const witnesses = {
  get_secret: ({ privateState }: WitnessContext<PrivateState>): bigint => {
    return privateState.secret;
  },
};

// Build transaction
const tx = await contract.callTx.transfer(recipient, amount, witnesses);
```

### 2. Prove and Submit

```typescript
// Show loading - this takes several seconds
setStatus("Generating proof...");

// Prove transaction (invokes local proof server)
const provenTx = await walletAPI.balanceAndProveTransaction(tx, newCoins);

// Submit to network
setStatus("Submitting...");
const txHash = await walletAPI.submitTransaction(provenTx);

setStatus("Submitted!");
console.log("Transaction hash:", txHash);
```

### 3. Track Status

```typescript
function useTxStatus(txHash: string | null) {
  const [status, setStatus] = useState<TxStatus>("pending");

  useEffect(() => {
    if (!txHash) return;

    const checkStatus = async () => {
      // Poll for transaction confirmation
      const result = await checkTransaction(txHash);
      setStatus(result.status);
    };

    const interval = setInterval(checkStatus, 3000);
    return () => clearInterval(interval);
  }, [txHash]);

  return status;
}
```

### 4. Handle Errors with Retry

```typescript
async function submitWithRetry(
  buildTx: () => Promise<Transaction>,
  maxRetries = 3
): Promise<string> {
  let lastError: Error | null = null;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const tx = await buildTx();
      const provenTx = await walletAPI.balanceAndProveTransaction(tx, newCoins);
      return await walletAPI.submitTransaction(provenTx);
    } catch (error) {
      lastError = error as Error;

      // Don't retry user rejection
      if (error.message.includes("rejected")) {
        throw error;
      }

      // Exponential backoff
      if (attempt < maxRetries) {
        await new Promise((r) => setTimeout(r, 1000 * Math.pow(2, attempt)));
      }
    }
  }

  throw lastError ?? new Error("Transaction failed");
}
```

## Common Patterns

### Transaction State Machine

```typescript
type TxState =
  | { status: "idle" }
  | { status: "building" }
  | { status: "proving" }
  | { status: "submitting" }
  | { status: "pending"; txHash: string }
  | { status: "confirmed"; txHash: string }
  | { status: "failed"; error: Error };

function txReducer(state: TxState, action: TxAction): TxState {
  switch (action.type) {
    case "START":
      return { status: "building" };
    case "PROVING":
      return { status: "proving" };
    case "SUBMITTING":
      return { status: "submitting" };
    case "SUBMITTED":
      return { status: "pending", txHash: action.txHash };
    case "CONFIRMED":
      return { status: "confirmed", txHash: action.txHash };
    case "FAILED":
      return { status: "failed", error: action.error };
    case "RESET":
      return { status: "idle" };
    default:
      return state;
  }
}
```

### Optimistic UI Updates

```typescript
async function transferWithOptimisticUpdate(
  recipient: Uint8Array,
  amount: bigint
) {
  // Optimistically update UI
  const previousBalance = balance;
  setBalance((prev) => prev - amount);

  try {
    const tx = await contract.callTx.transfer(recipient, amount, witnesses);
    const provenTx = await walletAPI.balanceAndProveTransaction(tx, newCoins);
    await walletAPI.submitTransaction(provenTx);
    // Success - optimistic update was correct
  } catch (error) {
    // Revert optimistic update
    setBalance(previousBalance);
    throw error;
  }
}
```

## Performance Considerations

| Concern | Mitigation |
|---------|------------|
| Proof generation (5-30s) | Show progress UI, allow cancellation |
| Network latency | Implement retry with exponential backoff |
| Timeout during proof | Set appropriate timeout (60s+), retry on timeout |
| User waits for confirmation | Show pending state, allow background monitoring |

## Related Skills

- `wallet-integration` - Wallet connection before transactions
- `proof-handling` - Witness construction and proof generation
- `state-management` - Reading state before/after transactions
- `error-handling` - Transaction error messages and recovery

## Related Commands

- `/dapp-check` - Validates transaction provider configuration
- `/dapp-debug transactions` - Diagnose transaction submission issues
