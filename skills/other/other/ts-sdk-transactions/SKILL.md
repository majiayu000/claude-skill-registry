---
name: ts-sdk-transactions
description:
  "How to build, sign, submit, and simulate transactions in @aptos-labs/ts-sdk. Covers build.simple(),
  signAndSubmitTransaction(), waitForTransaction(), simulate, sponsored (fee payer), and multi-agent. Triggers on:
  'build.simple', 'signAndSubmitTransaction', 'transaction.build', 'waitForTransaction', 'signAsFeePayer', 'SDK
  transaction', 'sponsored transaction', 'multi-agent transaction'."
license: MIT
metadata:
  author: aptos-labs
  version: "1.0"
  category: sdk
  tags: ["typescript", "sdk", "transaction", "submit", "simulate", "sponsored", "multi-agent"]
  priority: high
---

# TypeScript SDK: Transactions

## Purpose

Guide **building, signing, submitting, and simulating** transactions with `@aptos-labs/ts-sdk`. Use the build → sign →
submit → wait pattern; optionally simulate before submit.

## ALWAYS

1. **Call `aptos.waitForTransaction({ transactionHash })` after submit** – do not assume transaction is committed after
   `signAndSubmitTransaction`.
2. **Use `aptos.transaction.build.simple()` for entry function payloads** – pass `sender` and
   `data: { function, functionArguments, typeArguments? }`.
3. **Simulate before submit for critical/high-value flows** – use `aptos.transaction.simulate.simple()` and check
   `success` and `vm_status`.
4. **Use the same Account instance for signer** that you use for `sender` address when building (e.g.
   `account.accountAddress` as sender, `account` as signer).

## NEVER

1. **Do not skip `waitForTransaction`** – submission returns when the tx is accepted, not when it is committed.
2. **Do not use deprecated `scriptComposer`** (removed in v6) – use separate transactions or batch patterns.
3. **Do not use `number` for u64/u128/u256 in `functionArguments`** – use `bigint` where required to avoid precision
   loss.

---

## Standard flow (simple transaction)

```typescript
import { Aptos, AptosConfig, Network } from "@aptos-labs/ts-sdk";

const aptos = new Aptos(new AptosConfig({ network: Network.TESTNET }));
const MODULE_ADDRESS = "0x...";

// 1. Build
const transaction = await aptos.transaction.build.simple({
  sender: account.accountAddress,
  data: {
    function: `${MODULE_ADDRESS}::counter::increment`,
    functionArguments: []
  }
});

// 2. Sign and submit
const pendingTx = await aptos.signAndSubmitTransaction({
  signer: account,
  transaction
});

// 3. Wait for commitment
const committedTx = await aptos.waitForTransaction({
  transactionHash: pendingTx.hash
});

if (!committedTx.success) {
  throw new Error(`Tx failed: ${committedTx.vm_status}`);
}
```

---

## Build options

```typescript
// With type arguments (e.g. coin type)
const transaction = await aptos.transaction.build.simple({
  sender: account.accountAddress,
  data: {
    function: "0x1::coin::transfer",
    typeArguments: ["0x1::aptos_coin::AptosCoin"],
    functionArguments: [recipientAddress, amount]
  }
});

// Optional: max gas, expiry, etc. (see SDK types for full options)
const transactionWithOptions = await aptos.transaction.build.simple({
  sender: account.accountAddress,
  data: { function: "...", functionArguments: [] },
  options: {
    maxGasAmount: 2000n,
    gasUnitPrice: 100n,
    expireTimestamp: BigInt(Math.floor(Date.now() / 1000) + 600)
  }
});
```

---

## Simulation (before submit)

```typescript
const transaction = await aptos.transaction.build.simple({
  sender: account.accountAddress,
  data: {
    function: `${MODULE_ADDRESS}::counter::increment`,
    functionArguments: []
  }
});

const [simResult] = await aptos.transaction.simulate.simple({
  signerPublicKey: account.publicKey,
  transaction
});

if (!simResult.success) {
  throw new Error(`Simulation failed: ${simResult.vm_status}`);
}
console.log("Gas used:", simResult.gas_used);
```

---

## Sponsored transactions (fee payer)

```typescript
// 1. Build with fee payer
const transaction = await aptos.transaction.build.simple({
  sender: sender.accountAddress,
  withFeePayer: true,
  data: {
    function: `${MODULE_ADDRESS}::counter::increment`,
    functionArguments: []
  }
});

// 2. Sender signs
const senderAuth = aptos.transaction.sign({
  signer: sender,
  transaction
});

// 3. Fee payer signs (different method)
const feePayerAuth = aptos.transaction.signAsFeePayer({
  signer: feePayer,
  transaction
});

// 4. Submit with both authenticators
const pendingTx = await aptos.transaction.submit.simple({
  transaction,
  senderAuthenticator: senderAuth,
  feePayerAuthenticator: feePayerAuth
});

await aptos.waitForTransaction({ transactionHash: pendingTx.hash });
```

---

## Multi-agent transactions

```typescript
const transaction = await aptos.transaction.build.multiAgent({
  sender: alice.accountAddress,
  secondarySignerAddresses: [bob.accountAddress],
  data: {
    function: `${MODULE_ADDRESS}::escrow::exchange`,
    functionArguments: [itemAddress, amount]
  }
});

const aliceAuth = aptos.transaction.sign({ signer: alice, transaction });
const bobAuth = aptos.transaction.sign({ signer: bob, transaction });

const pendingTx = await aptos.transaction.submit.multiAgent({
  transaction,
  senderAuthenticator: aliceAuth,
  additionalSignersAuthenticators: [bobAuth]
});

await aptos.waitForTransaction({ transactionHash: pendingTx.hash });
```

---

## waitForTransaction options

```typescript
const committed = await aptos.waitForTransaction({
  transactionHash: pendingTx.hash,
  options: {
    timeoutSecs: 60,
    checkSuccess: true // throw if tx failed
  }
});
```

---

## Gas profiling

```typescript
const gasProfile = await aptos.gasProfile({
  sender: account.accountAddress,
  data: {
    function: `${MODULE_ADDRESS}::module::function_name`,
    functionArguments: []
  }
});
console.log("Gas profile:", gasProfile);
```

---

## Common mistakes

| Mistake                        | Correct approach                                                                              |
| ------------------------------ | --------------------------------------------------------------------------------------------- |
| Not calling waitForTransaction | Always wait and check `committedTx.success`                                                   |
| Using number for large amounts | Use `bigint` for u64/u128/u256 in functionArguments                                           |
| Wrong signer for submit        | Use the Account whose address is the sender (or fee payer / additional signer as appropriate) |
| Assuming scriptComposer exists | Use separate transactions or batch; scriptComposer removed in v6                              |

---

## References

- SDK: `src/api/transaction.ts`, `src/internal/transactionSubmission.ts`, `src/internal/transaction.ts`
- Pattern: [TYPESCRIPT_SDK.md](../../../../patterns/fullstack/TYPESCRIPT_SDK.md)
- Related: [ts-sdk-account](../ts-sdk-account/SKILL.md), [ts-sdk-client](../ts-sdk-client/SKILL.md),
  [ts-sdk-wallet-adapter](../ts-sdk-wallet-adapter/SKILL.md), [use-ts-sdk](../use-ts-sdk/SKILL.md)
