---
name: ts-sdk-wallet-adapter
description:
  "How to integrate wallet connection in React frontends using @aptos-labs/wallet-adapter-react. Covers
  AptosWalletAdapterProvider setup, useWallet() hook, frontend transaction submission, and wallet connection UI.
  Triggers on: 'wallet adapter', 'connect wallet', 'useWallet', 'AptosWalletAdapterProvider', 'wallet-adapter-react',
  'wallet connection'."
license: MIT
metadata:
  author: aptos-labs
  version: "1.0"
  category: sdk
  tags: ["typescript", "sdk", "wallet", "react", "frontend", "adapter"]
  priority: high
---

# TypeScript SDK: Wallet Adapter (React)

## Purpose

Guide **wallet connection and frontend transaction submission** in React using `@aptos-labs/wallet-adapter-react`. End
users sign transactions via their browser wallet (Petra, Nightly, etc.) — never via raw private keys.

## ALWAYS

1. **Use `@aptos-labs/wallet-adapter-react` for frontend wallet integration** — this is the standard React adapter.
2. **Wrap your app root with `AptosWalletAdapterProvider`** — all `useWallet()` calls require this context.
3. **Use `useWallet()` hook** to access wallet functions in React components.
4. **Use the wallet adapter's `signAndSubmitTransaction`** (from `useWallet()`) in frontend — NOT the SDK's direct
   `aptos.signAndSubmitTransaction`.
5. **Always call `aptos.waitForTransaction({ transactionHash })` after submit** — the wallet returns when the tx is
   accepted, not committed.

## NEVER

1. **Do not use `Account.generate()` or raw private keys in browser/frontend** — use wallet adapter for end users.
2. **Do not use the SDK's `aptos.signAndSubmitTransaction` in React components** — use the wallet adapter's version from
   `useWallet()`.
3. **Do not hardcode wallet names** — use the `wallets` array from `useWallet()` for a dynamic list.

---

## Installation

```bash
npm install @aptos-labs/wallet-adapter-react
```

Modern AIP-62 standard wallets (Petra, Nightly, etc.) are autodetected and do NOT require additional packages. Legacy
wallets need their plugin package installed separately.

---

## Provider setup

Wrap your app root with `AptosWalletAdapterProvider`:

```tsx
// main.tsx or App.tsx
import { AptosWalletAdapterProvider } from "@aptos-labs/wallet-adapter-react";
import { Network } from "@aptos-labs/ts-sdk";

function App() {
  return (
    <AptosWalletAdapterProvider
      autoConnect={true}
      dappConfig={{
        network: Network.TESTNET
      }}
      onError={(error) => console.error("Wallet error:", error)}
    >
      <YourApp />
    </AptosWalletAdapterProvider>
  );
}
```

---

## useWallet() hook

```tsx
import { useWallet } from "@aptos-labs/wallet-adapter-react";

function MyComponent() {
  const {
    account, // Current connected account { address, publicKey }
    connected, // Boolean: is wallet connected?
    wallet, // Current wallet info { name, icon, url }
    wallets, // Array of available wallets
    connect, // (walletName) => Promise<void>
    disconnect, // () => Promise<void>
    signAndSubmitTransaction, // Submit entry function calls (use THIS in frontend)
    signTransaction, // Sign without submitting
    submitTransaction, // Submit a signed transaction
    signMessage, // Sign an arbitrary message
    signMessageAndVerify, // Sign and verify a message
    changeNetwork, // Switch networks (not all wallets support this)
    network // Current network info
  } = useWallet();
}
```

---

## Frontend transaction pattern

Use typed payloads with `InputTransactionData`:

```tsx
// entry-functions/increment.ts
import { InputTransactionData } from "@aptos-labs/wallet-adapter-react";
import { MODULE_ADDRESS } from "../lib/aptos";

export function buildIncrementPayload(): InputTransactionData {
  return {
    data: {
      function: `${MODULE_ADDRESS}::counter::increment`,
      functionArguments: []
    }
  };
}
```

```tsx
// components/IncrementButton.tsx
import { useWallet } from "@aptos-labs/wallet-adapter-react";
import { aptos } from "../lib/aptos";
import { buildIncrementPayload } from "../entry-functions/increment";

function IncrementButton() {
  const { signAndSubmitTransaction } = useWallet();

  const handleClick = async () => {
    try {
      const response = await signAndSubmitTransaction(buildIncrementPayload());
      await aptos.waitForTransaction({
        transactionHash: response.hash
      });
    } catch (error) {
      console.error("Transaction failed:", error);
    }
  };

  return <button onClick={handleClick}>Increment</button>;
}
```

---

## Wallet connection UI

```tsx
import { useWallet } from "@aptos-labs/wallet-adapter-react";

function WalletInfo() {
  const { account, connected, connect, disconnect, wallet, wallets } = useWallet();

  if (!connected) {
    return (
      <div>
        {wallets.map((w) => (
          <button key={w.name} onClick={() => connect(w.name)}>
            Connect {w.name}
          </button>
        ))}
      </div>
    );
  }

  return (
    <div>
      <p>Connected: {account?.address}</p>
      <p>Wallet: {wallet?.name}</p>
      <button onClick={disconnect}>Disconnect</button>
    </div>
  );
}
```

---

## Common mistakes

| Mistake                                             | Correct approach                                                       |
| --------------------------------------------------- | ---------------------------------------------------------------------- |
| Missing `AptosWalletAdapterProvider` wrapper        | Wrap app root with the provider                                        |
| Not waiting for transaction after submit            | Always call `aptos.waitForTransaction()`                               |
| Using SDK `aptos.signAndSubmitTransaction` in React | Use the wallet adapter's `signAndSubmitTransaction` from `useWallet()` |
| Using `Account.generate()` in frontend              | Use wallet adapter; generate only in server/scripts                    |
| Not handling user rejection                         | Catch and check for rejection-related error messages                   |
| Hardcoding wallet names                             | Use `wallets` array from `useWallet()` for dynamic list                |

---

## References

- Wallet Adapter: https://aptos.dev/build/sdks/wallet-adapter/dapp
- Pattern: [TYPESCRIPT_SDK.md](../../../../patterns/fullstack/TYPESCRIPT_SDK.md)
- Related: [ts-sdk-transactions](../ts-sdk-transactions/SKILL.md), [ts-sdk-client](../ts-sdk-client/SKILL.md),
  [use-ts-sdk](../use-ts-sdk/SKILL.md)
