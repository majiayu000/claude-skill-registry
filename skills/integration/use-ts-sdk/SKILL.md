---
name: use-ts-sdk
description:
  "Orchestrates TypeScript SDK integration for Aptos dApps. Routes to granular skills for specific tasks (client setup,
  accounts, transactions, view functions, types, wallet adapter). Use this skill for fullstack dApp integration or when
  multiple SDK concerns are involved. Triggers on: 'typescript sdk', 'ts-sdk', 'aptos sdk', 'SDK setup', 'interact with
  contract', 'call aptos', 'aptos javascript', 'frontend integration', 'fullstack'."
license: MIT
metadata:
  author: aptos-labs
  version: "1.0"
  category: sdk
  tags: ["typescript", "sdk", "frontend", "orchestrator", "fullstack"]
  priority: high
---

# Use TypeScript SDK (Orchestrator)

## Purpose

Orchestrates `@aptos-labs/ts-sdk` integration for Aptos dApps. For specific tasks, route to the appropriate granular
skill. For composite tasks (e.g., "build me a fullstack dApp"), follow the workflow below.

## Core Rules

1. **ALWAYS use `@aptos-labs/ts-sdk`** (the current official SDK, NOT the deprecated `aptos` package)
2. **NEVER hardcode private keys** in source code or frontend bundles
3. **NEVER expose private keys** in client-side code or logs
4. **NEVER store private keys** in environment variables accessible to the browser (use `VITE_` prefix only for public
   config)
5. **ALWAYS load private keys from environment variables** in server-side scripts only, using `process.env`

## Important: Boilerplate Template

If the project was scaffolded with `npx create-aptos-dapp` (boilerplate template), **wallet adapter and SDK setup are
already done.** Before writing new code, check what already exists:

- `frontend/components/WalletProvider.tsx` — wallet adapter setup with auto-connect
- `frontend/constants.ts` — `NETWORK`, `MODULE_ADDRESS`, `APTOS_API_KEY` from env vars
- `frontend/entry-functions/` — existing entry function patterns (follow these for new ones)
- `frontend/view-functions/` — existing view function patterns (follow these for new ones)

**Do NOT recreate** wallet provider, client setup, or constants if they already exist. Instead, **follow the existing
patterns** to add new entry/view functions for your Move contracts.

## Skill Routing

Route to the appropriate granular skill based on the task:

| Task                                           | Skill                                                      |
| ---------------------------------------------- | ---------------------------------------------------------- |
| Set up Aptos client / configure network        | [ts-sdk-client](../ts-sdk-client/SKILL.md)                 |
| Create accounts/signers (server-side)          | [ts-sdk-account](../ts-sdk-account/SKILL.md)               |
| Parse, format, or derive addresses             | [ts-sdk-address](../ts-sdk-address/SKILL.md)               |
| Build, sign, submit, simulate transactions     | [ts-sdk-transactions](../ts-sdk-transactions/SKILL.md)     |
| Read on-chain data (view, balances, resources) | [ts-sdk-view-and-query](../ts-sdk-view-and-query/SKILL.md) |
| Map Move types to TypeScript types             | [ts-sdk-types](../ts-sdk-types/SKILL.md)                   |
| Connect wallet in React frontend               | [ts-sdk-wallet-adapter](../ts-sdk-wallet-adapter/SKILL.md) |

## Fullstack dApp Workflow

When building a complete frontend integration:

1. **Set up client** → read [ts-sdk-client](../ts-sdk-client/SKILL.md)
2. **Create view function wrappers** → read [ts-sdk-view-and-query](../ts-sdk-view-and-query/SKILL.md)
3. **Create entry function payloads** → read [ts-sdk-transactions](../ts-sdk-transactions/SKILL.md)
4. **Wire up wallet connection** → read [ts-sdk-wallet-adapter](../ts-sdk-wallet-adapter/SKILL.md)
5. **Handle types correctly** → read [ts-sdk-types](../ts-sdk-types/SKILL.md) (as needed)

## File Organization Pattern

```
src/
  lib/
    aptos.ts                    # Singleton Aptos client + MODULE_ADDRESS
  view-functions/
    getCount.ts                 # One file per view function
    getListing.ts
  entry-functions/
    increment.ts                # One file per entry function
    createListing.ts
  hooks/
    useCounter.ts               # React hooks wrapping view functions
    useListing.ts
  components/
    WalletProvider.tsx           # AptosWalletAdapterProvider wrapper
    IncrementButton.tsx          # Components calling entry functions
```

## Error Handling Pattern

```typescript
async function submitTransaction(
  aptos: Aptos,
  signer: Account,
  payload: InputGenerateTransactionPayloadData
): Promise<string> {
  try {
    const transaction = await aptos.transaction.build.simple({
      sender: signer.accountAddress,
      data: payload
    });

    const pendingTx = await aptos.signAndSubmitTransaction({
      signer,
      transaction
    });

    const committed = await aptos.waitForTransaction({
      transactionHash: pendingTx.hash
    });

    if (!committed.success) {
      throw new Error(`Transaction failed: ${committed.vm_status}`);
    }

    return pendingTx.hash;
  } catch (error) {
    if (error instanceof Error) {
      if (error.message.includes("RESOURCE_NOT_FOUND")) {
        throw new Error("Resource does not exist at the specified address");
      }
      if (error.message.includes("MODULE_NOT_FOUND")) {
        throw new Error("Contract is not deployed at the specified address");
      }
      if (error.message.includes("ABORTED")) {
        const match = error.message.match(/code: (\d+)/);
        const code = match ? match[1] : "unknown";
        throw new Error(`Contract error (code ${code})`);
      }
    }
    throw error;
  }
}
```

## Edge Cases

| Scenario                | Check                                            | Action                                       |
| ----------------------- | ------------------------------------------------ | -------------------------------------------- |
| Resource not found      | `error.message.includes("RESOURCE_NOT_FOUND")`   | Return default value or null                 |
| Module not deployed     | `error.message.includes("MODULE_NOT_FOUND")`     | Show "contract not deployed" message         |
| Function not found      | `error.message.includes("FUNCTION_NOT_FOUND")`   | Check function name and module address       |
| Move abort              | `error.message.includes("ABORTED")`              | Parse abort code, map to user-friendly error |
| Out of gas              | `error.message.includes("OUT_OF_GAS")`           | Increase `maxGasAmount` and retry            |
| Sequence number error   | `error.message.includes("SEQUENCE_NUMBER")`      | Retry after fetching fresh sequence number   |
| Network timeout         | `error.message.includes("timeout")`              | Retry with exponential backoff               |
| Account does not exist  | `error.message.includes("ACCOUNT_NOT_FOUND")`    | Fund account or prompt user to create one    |
| Insufficient balance    | `error.message.includes("INSUFFICIENT_BALANCE")` | Show balance and required amount             |
| User rejected in wallet | Wallet-specific rejection error                  | Show "transaction cancelled" message         |

## Anti-patterns

1. **NEVER use the deprecated `aptos` npm package** — use `@aptos-labs/ts-sdk`
2. **NEVER skip `waitForTransaction`** after submitting — transaction may not be committed yet
3. **NEVER hardcode module addresses** — use environment variables (`VITE_MODULE_ADDRESS`)
4. **NEVER create multiple `Aptos` client instances** — create one singleton and share it
5. **NEVER use `Account.generate()` in frontend code** for real users — use wallet adapter
6. **NEVER use `scriptComposer`** — removed in v6.0; use separate transactions instead
7. **NEVER use `getAccountCoinAmount` or `getAccountAPTAmount`** — deprecated; use `getBalance()`

## SDK Version Notes

### AIP-80 Private Key Format (v2.0+)

Ed25519 and Secp256k1 private keys now use an AIP-80 prefixed format when serialized with `toString()`:

```typescript
const key = new Ed25519PrivateKey("0x...");
key.toString(); // Returns AIP-80 prefixed format, NOT raw hex
```

### Fungible Asset Transfers (v1.39+)

```typescript
await aptos.transferFungibleAssetBetweenStores({
  sender: account,
  fungibleAssetMetadataAddress: metadataAddr,
  senderStoreAddress: fromStore,
  recipientStoreAddress: toStore,
  amount: 1000n
});
```

### Account Abstraction (v1.34+, AIP-104)

```typescript
// Check if AA is enabled for an account
const isEnabled = await aptos.abstraction.isAccountAbstractionEnabled({
  accountAddress: "0x...",
  authenticationFunction: `${MODULE_ADDRESS}::auth::authenticate`
});

// Enable AA on an account
const enableTxn = await aptos.abstraction.enableAccountAbstractionTransaction({
  accountAddress: account.accountAddress,
  authenticationFunction: `${MODULE_ADDRESS}::auth::authenticate`
});

// Use AbstractedAccount for signing with custom auth logic
import { AbstractedAccount } from "@aptos-labs/ts-sdk";
```

## References

**Pattern Documentation:**

- [TYPESCRIPT_SDK.md](../../../../patterns/fullstack/TYPESCRIPT_SDK.md) — Complete SDK API reference

**Official Documentation:**

- TypeScript SDK: https://aptos.dev/build/sdks/ts-sdk
- API Reference: https://aptos-labs.github.io/aptos-ts-sdk/
- Wallet Adapter: https://aptos.dev/build/sdks/wallet-adapter/dapp
- GitHub: https://github.com/aptos-labs/aptos-ts-sdk

**Granular Skills:**

- [ts-sdk-client](../ts-sdk-client/SKILL.md) — Client setup and configuration
- [ts-sdk-account](../ts-sdk-account/SKILL.md) — Account/signer creation
- [ts-sdk-address](../ts-sdk-address/SKILL.md) — Address parsing and derivation
- [ts-sdk-transactions](../ts-sdk-transactions/SKILL.md) — Build, sign, submit transactions
- [ts-sdk-view-and-query](../ts-sdk-view-and-query/SKILL.md) — View functions and queries
- [ts-sdk-types](../ts-sdk-types/SKILL.md) — Move-to-TypeScript type mapping
- [ts-sdk-wallet-adapter](../ts-sdk-wallet-adapter/SKILL.md) — React wallet integration

**Related Skills:**

- `write-contracts` — Write the Move contracts that this SDK interacts with
- `deploy-contracts` — Deploy contracts before calling them from TypeScript
