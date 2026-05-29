---
name: midnight-dapp:proof-handling
description: Use when building witness data for ZK proofs, showing proof generation progress to users, implementing disclosure consent flows, handling proof timeouts and retries, or explaining privacy guarantees.
---

# Proof Handling

Build and present zero-knowledge proofs in your Midnight DApp, from constructing witnesses to showing proof generation progress and handling privacy disclosures.

## When to Use

- Building witness data for contract transactions
- Showing proof generation progress to users
- Implementing disclosure consent flows
- Handling proof timeouts and retries
- Explaining privacy guarantees to users

## Key Concepts

### Witness Construction

Witnesses are TypeScript functions that provide private data to ZK circuits. The data stays local - only the cryptographic proof goes on-chain.

```typescript
// Witness provides private input - circuit proves you know it
const witnesses = {
  get_secret: ({ privateState }: WitnessContext<PrivateState>): bigint => {
    return privateState.secret; // Never leaves the client
  }
};
```

### Client-Side Proofs

All proof generation happens locally on the user's device:

1. **Never on remote servers** - Private data never leaves the browser
2. **Proof server runs locally** - Docker container on port 6300
3. **Takes seconds, not milliseconds** - Show progress UI to users
4. **Can timeout** - Implement retry logic for reliability

### Disclosure UX

When circuits use `disclose()`, users must understand what they're revealing:

```typescript
// This reveals the exact value on-chain
const disclosedAge = disclose(userAge);

// User should see: "This will reveal your age (25) publicly"
```

## References

| Document | Description |
|----------|-------------|
| [witness-fundamentals.md](references/witness-fundamentals.md) | Witness patterns and type mapping |
| [client-side-proofs.md](references/client-side-proofs.md) | Proof server setup and performance |
| [disclosure-ux.md](references/disclosure-ux.md) | Privacy disclosure UI patterns |
| [web3-comparison.md](references/web3-comparison.md) | Ethereum signing vs Midnight proofs |

## Examples

| Example | Description |
|---------|-------------|
| [witness-builder/](examples/witness-builder/) | Functions to construct witness objects |
| [proof-progress/](examples/proof-progress/) | Proof generation progress component |
| [disclosure-modal/](examples/disclosure-modal/) | Privacy disclosure consent modal |

## Quick Start

### 1. Define Witness Types

```typescript
interface PrivateState {
  secretKey: Uint8Array;
  credentials: Map<string, Credential>;
  balance: bigint;
}
```

### 2. Implement Witnesses

```typescript
import type { WitnessContext } from "@midnight-ntwrk/midnight-js-types";

const witnesses = {
  get_balance: ({ privateState }: WitnessContext<PrivateState>): bigint => {
    return privateState.balance;
  },

  get_credential: (
    { privateState }: WitnessContext<PrivateState>,
    credentialId: Uint8Array
  ): Credential => {
    const id = bytesToHex(credentialId);
    const credential = privateState.credentials.get(id);
    if (!credential) {
      throw new WitnessError("Credential not found", "NOT_FOUND");
    }
    return credential;
  }
};
```

### 3. Show Proof Progress

```typescript
function TransferButton({ onTransfer }) {
  const { status, progress, error, generateProof } = useProofStatus();

  const handleClick = async () => {
    const result = await generateProof(async () => {
      return contract.callTx.transfer(recipient, amount, witnesses);
    });

    if (result.success) {
      onTransfer(result.transaction);
    }
  };

  return (
    <div>
      <button onClick={handleClick} disabled={status === "generating"}>
        {status === "generating" ? "Generating Proof..." : "Transfer"}
      </button>
      {status === "generating" && <ProgressBar value={progress} />}
      {error && <ErrorMessage error={error} />}
    </div>
  );
}
```

### 4. Handle Disclosure Consent

```typescript
function DisclosureFlow({ disclosures, onConfirm, onCancel }) {
  return (
    <DisclosureModal
      disclosures={disclosures}
      onConfirm={onConfirm}
      onCancel={onCancel}
    >
      <p>This transaction will reveal the following information:</p>
      <ul>
        {disclosures.map((d) => (
          <li key={d.field}>
            <strong>{d.label}</strong>: {d.value}
          </li>
        ))}
      </ul>
    </DisclosureModal>
  );
}
```

## Common Patterns

### Witness with Validation

```typescript
const witnesses = {
  get_credential: (
    { privateState }: WitnessContext<PrivateState>,
    credentialId: Uint8Array
  ): Credential => {
    const credential = privateState.credentials.get(bytesToHex(credentialId));

    if (!credential) {
      throw new WitnessError("Credential not found", "NOT_FOUND");
    }

    // Validate before returning
    if (credential.expiry < BigInt(Date.now())) {
      throw new WitnessError("Credential expired", "EXPIRED");
    }

    return credential;
  }
};
```

### Async Witness for External Data

```typescript
const witnesses = {
  get_oracle_price: async (
    { privateState }: WitnessContext<PrivateState>,
    tokenId: Uint8Array
  ): Promise<bigint> => {
    const response = await fetch(`/api/price/${bytesToHex(tokenId)}`);
    if (!response.ok) {
      throw new WitnessError("Price unavailable", "ORACLE_ERROR");
    }
    const { price } = await response.json();
    return BigInt(price);
  }
};
```

### Proof Retry Logic

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

      // Wait before retry with exponential backoff
      if (attempt < maxRetries) {
        await new Promise((r) => setTimeout(r, 1000 * Math.pow(2, attempt)));
      }
    }
  }

  throw lastError ?? new Error("Proof generation failed");
}
```

## Security Considerations

1. **Never persist witness data** - Keep private state in memory only
2. **Clear sensitive data** - Zero out arrays after use when possible
3. **Validate all inputs** - Check parameter validity in witnesses
4. **Handle errors gracefully** - Don't leak information in error messages
5. **User consent for disclosures** - Always show what will be revealed

## Related Skills

- `wallet-integration` - Wallet connection required before proof generation
- `state-management` - Managing private state for witnesses
- `transaction-flows` - Submitting proven transactions
- `error-handling` - Proof error messages and recovery

## Related Commands

- `/dapp-check` - Validates proof server configuration
- `/dapp-debug proofs` - Diagnose proof generation issues
