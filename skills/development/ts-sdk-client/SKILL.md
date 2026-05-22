---
name: ts-sdk-client
description:
  "How to create and configure the Aptos client (Aptos, AptosConfig) in @aptos-labs/ts-sdk. Covers Network,
  fullnode/indexer/faucet URLs, singleton pattern, and Bun compatibility. Triggers on: 'Aptos client', 'AptosConfig',
  'SDK client', 'client setup', 'new Aptos(', 'Network.TESTNET', 'Network.MAINNET'."
license: MIT
metadata:
  author: aptos-labs
  version: "1.0"
  category: sdk
  tags: ["typescript", "sdk", "client", "aptos", "config", "network"]
  priority: high
---

# TypeScript SDK: Aptos Client

## Purpose

Guide creation and configuration of the **Aptos** client and **AptosConfig** in `@aptos-labs/ts-sdk`. One client
instance is used for all read/write and account/transaction APIs.

## ALWAYS

1. **Create one Aptos instance per app** (singleton) and reuse it – avoid multiple `new Aptos(config)` for the same
   network.
2. **Configure network via `AptosConfig`** – use `Network.TESTNET` or `Network.MAINNET` (or custom endpoints).
3. **Use environment variables for network/URLs** in production – e.g. `process.env.APTOS_NETWORK` or
   `import.meta.env.VITE_APP_NETWORK`.
4. **Use `Network.TESTNET` as default for development** – devnet resets frequently.

## NEVER

1. **Do not create a new Aptos client per request** – reuse the singleton.
2. **Do not hardcode fullnode/indexer URLs** in source when using public networks – use `Network` enum.
3. **Do not omit `network` when using custom endpoints** – in v5.2+ use `Network.CUSTOM` with custom URLs.

---

## Basic setup

```typescript
import { Aptos, AptosConfig, Network } from "@aptos-labs/ts-sdk";

const config = new AptosConfig({ network: Network.TESTNET });
const aptos = new Aptos(config);
```

---

## Network options

```typescript
// Predefined networks
const devnet = new AptosConfig({ network: Network.DEVNET });
const testnet = new AptosConfig({ network: Network.TESTNET });
const mainnet = new AptosConfig({ network: Network.MAINNET });

// Custom endpoints (network is REQUIRED in v5.2+)
const custom = new AptosConfig({
  network: Network.CUSTOM,
  fullnode: "https://your-fullnode.example.com/v1",
  indexer: "https://your-indexer.example.com/v1/graphql",
  faucet: "https://your-faucet.example.com"
});
```

---

## Singleton pattern (recommended)

```typescript
// lib/aptos.ts or similar
import { Aptos, AptosConfig, Network } from "@aptos-labs/ts-sdk";

function getNetwork(): Network {
  const raw = typeof process !== "undefined" ? process.env.APTOS_NETWORK : import.meta.env?.VITE_APP_NETWORK;
  switch (raw) {
    case "mainnet":
      return Network.MAINNET;
    case "devnet":
      return Network.DEVNET;
    default:
      return Network.TESTNET;
  }
}

const config = new AptosConfig({ network: getNetwork() });
export const aptos = new Aptos(config);
```

---

## Optional endpoints (override per service)

```typescript
const config = new AptosConfig({
  network: Network.TESTNET,
  fullnode: "https://fullnode.testnet.aptoslabs.com/v1", // override default
  indexer: "https://indexer.testnet.aptoslabs.com/v1/graphql",
  faucet: "https://faucet.testnet.aptoslabs.com",
  pepper: "https://...", // keyless pepper service
  prover: "https://..." // keyless prover
});
const aptos = new Aptos(config);
```

---

## Client config (HTTP, timeouts, Bun)

```typescript
// Disable HTTP/2 when using Bun (recommended)
const config = new AptosConfig({
  network: Network.TESTNET,
  clientConfig: { http2: false }
});
const aptos = new Aptos(config);
```

---

## Using the client

After construction, use the same `aptos` instance for:

- **Account / balance:** `aptos.getAccountInfo()`, `aptos.getBalance()`, `aptos.getAccountResources()`, etc.
- **Transactions:** `aptos.transaction.build.simple()`, `aptos.signAndSubmitTransaction()`,
  `aptos.waitForTransaction()`.
- **View:** `aptos.view()`.
- **Faucet:** `aptos.fundAccount()` (devnet/testnet).
- **Coin / token / object / ANS / staking:** `aptos.coin.*`, `aptos.digitalAsset.*`, `aptos.fungibleAsset.*`,
  `aptos.object.*`, `aptos.ans.*`, `aptos.staking.*`.

---

## Common mistakes

| Mistake                            | Correct approach                                                     |
| ---------------------------------- | -------------------------------------------------------------------- |
| Creating Aptos in every function   | One singleton; pass `aptos` or import from shared module             |
| Using devnet for persistent dev    | Prefer testnet; devnet resets                                        |
| Custom URLs without Network.CUSTOM | Set `network: Network.CUSTOM` when providing fullnode/indexer/faucet |
| Forgetting http2: false on Bun     | Set `clientConfig: { http2: false }` for Bun                         |

---

## References

- SDK: `src/api/aptos.ts`, `src/api/aptosConfig.ts`
- Pattern: [TYPESCRIPT_SDK.md](../../../../patterns/fullstack/TYPESCRIPT_SDK.md)
- Related: [ts-sdk-account](../ts-sdk-account/SKILL.md), [ts-sdk-transactions](../ts-sdk-transactions/SKILL.md),
  [ts-sdk-wallet-adapter](../ts-sdk-wallet-adapter/SKILL.md), [use-ts-sdk](../use-ts-sdk/SKILL.md)
