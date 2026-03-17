---
name: midnight-proofs:proof-verification
description: Use when verifying ZK proofs server-side, validating proofs before transaction submission, building verification gateways, implementing batch verification, or debugging proof generation issues.
---

# Proof Verification

Verify ZK proofs server-side before transaction submission to catch invalid proofs early and reduce failed transactions.

## When to Use

- Validating proofs before submitting transactions to the network
- Building a verification gateway for incoming proofs
- Implementing batch verification for high-throughput systems
- Checking proof validity as part of an API request
- Debugging proof generation issues

## Key Concepts

### Why Verify Server-Side?

| Benefit | Description |
|---------|-------------|
| **Fail fast** | Catch invalid proofs before network submission |
| **Save gas** | Avoid transaction fees for invalid proofs |
| **Better UX** | Provide immediate feedback to users |
| **Security** | Validate proofs from untrusted clients |

### Verification vs Validation

- **Verification** - Cryptographic check that proof is valid for the circuit
- **Validation** - Business logic checks (e.g., correct public inputs)

```typescript
// Both verification and validation
async function verifyAndValidate(proof: Proof, publicInputs: PublicInputs): Promise<boolean> {
  // Step 1: Cryptographic verification
  const isValidProof = await verifier.verify(proof, publicInputs);
  if (!isValidProof) return false;

  // Step 2: Business validation
  const isValidBusiness = validateBusinessRules(publicInputs);
  return isValidBusiness;
}
```

### Verification Performance

Verification is much faster than proof generation:

| Operation | Typical Duration |
|-----------|------------------|
| Proof Generation | 5-30 seconds |
| Proof Verification | 10-100 milliseconds |

## References

| Document | Description |
|----------|-------------|
| [verification-api.md](references/verification-api.md) | Verifier SDK setup and API reference |

## Examples

| Example | Description |
|---------|-------------|
| [pre-submit-validation/](examples/pre-submit-validation/) | Verify before transaction submit |
| [batch-verification/](examples/batch-verification/) | Verify multiple proofs in parallel |

## Quick Start

### 1. Set Up Verifier

```typescript
import { createVerifier } from '@midnight-ntwrk/midnight-js-verifier';

const verifier = await createVerifier({
  verificationKeysPath: './circuit-keys',
});
```

### 2. Verify a Single Proof

```typescript
async function verifyProof(
  circuitId: string,
  proof: Uint8Array,
  publicInputs: Record<string, unknown>
): Promise<boolean> {
  try {
    const result = await verifier.verify(circuitId, proof, publicInputs);
    return result.valid;
  } catch (error) {
    console.error('Verification failed:', error);
    return false;
  }
}
```

### 3. Verify Before Submit

```typescript
async function submitWithVerification(
  transaction: Transaction
): Promise<string> {
  // Extract proof and public inputs from transaction
  const { proof, publicInputs, circuitId } = transaction;

  // Verify first
  const isValid = await verifyProof(circuitId, proof, publicInputs);
  if (!isValid) {
    throw new Error('Proof verification failed');
  }

  // Submit to network
  return await submitTransaction(transaction);
}
```

## Common Patterns

### Verification Gateway

```typescript
import express from 'express';

const app = express();

app.post('/api/verify', async (req, res) => {
  const { circuitId, proof, publicInputs } = req.body;

  try {
    const result = await verifier.verify(
      circuitId,
      Buffer.from(proof, 'base64'),
      publicInputs
    );

    res.json({
      valid: result.valid,
      circuitId,
      verificationTime: result.duration,
    });
  } catch (error) {
    res.status(400).json({
      valid: false,
      error: error.message,
    });
  }
});
```

### Batch Verification

```typescript
interface ProofBatch {
  circuitId: string;
  proof: Uint8Array;
  publicInputs: Record<string, unknown>;
}

async function verifyBatch(
  proofs: ProofBatch[]
): Promise<Map<number, boolean>> {
  const results = new Map<number, boolean>();

  // Verify in parallel
  const verifications = proofs.map(async (p, index) => {
    try {
      const result = await verifier.verify(
        p.circuitId,
        p.proof,
        p.publicInputs
      );
      results.set(index, result.valid);
    } catch {
      results.set(index, false);
    }
  });

  await Promise.all(verifications);
  return results;
}
```

### Caching Verified Proofs

```typescript
import { createHash } from 'crypto';

const verifiedProofs = new Map<string, boolean>();

function proofHash(proof: Uint8Array, publicInputs: Record<string, unknown>): string {
  const data = JSON.stringify({ proof: proof.toString(), publicInputs });
  return createHash('sha256').update(data).digest('hex');
}

async function verifyWithCache(
  circuitId: string,
  proof: Uint8Array,
  publicInputs: Record<string, unknown>
): Promise<boolean> {
  const hash = proofHash(proof, publicInputs);

  // Check cache
  if (verifiedProofs.has(hash)) {
    return verifiedProofs.get(hash)!;
  }

  // Verify
  const result = await verifier.verify(circuitId, proof, publicInputs);
  verifiedProofs.set(hash, result.valid);

  return result.valid;
}
```

### Verification with Timeout

```typescript
async function verifyWithTimeout(
  circuitId: string,
  proof: Uint8Array,
  publicInputs: Record<string, unknown>,
  timeoutMs = 5000
): Promise<boolean> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const result = await verifier.verify(circuitId, proof, publicInputs, {
      signal: controller.signal,
    });
    return result.valid;
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error('Verification timeout');
    }
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}
```

### Error Classification

```typescript
enum VerificationError {
  INVALID_PROOF = 'INVALID_PROOF',
  INVALID_PUBLIC_INPUTS = 'INVALID_PUBLIC_INPUTS',
  CIRCUIT_NOT_FOUND = 'CIRCUIT_NOT_FOUND',
  MALFORMED_PROOF = 'MALFORMED_PROOF',
  TIMEOUT = 'TIMEOUT',
}

function classifyVerificationError(error: Error): VerificationError {
  if (error.message.includes('circuit')) {
    return VerificationError.CIRCUIT_NOT_FOUND;
  }
  if (error.message.includes('public input')) {
    return VerificationError.INVALID_PUBLIC_INPUTS;
  }
  if (error.message.includes('malformed')) {
    return VerificationError.MALFORMED_PROOF;
  }
  if (error.message.includes('timeout')) {
    return VerificationError.TIMEOUT;
  }
  return VerificationError.INVALID_PROOF;
}
```

## Performance Considerations

| Concern | Mitigation |
|---------|------------|
| Verification key loading | Preload keys at startup |
| High request volume | Use verification caching |
| Large batches | Limit concurrent verifications |
| Memory usage | Stream large proof batches |

## Related Skills

- `proof-generation` - Generate proofs server-side
- `proof-caching` - Cache verification results
- `prover-optimization` - Optimize prover that creates proofs

## Related Commands

None currently defined.
