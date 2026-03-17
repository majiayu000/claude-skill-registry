---
name: use-wallet
description: >-
  Integrate Algorand/AVM wallet connections using @txnlab/use-wallet v4.x.
  Use when building dApps that need wallet connectivity (Pera, Defly, Lute,
  Kibisis, Exodus, WalletConnect, etc.), transaction signing, data signing
  (ARC-60/SIWA), network switching, or wallet state management in vanilla
  JS/TS, React, Vue, SolidJS, or Svelte applications. Also covers the
  companion UI component library @txnlab/use-wallet-ui-react for drop-in
  wallet buttons and menus.
---

# @txnlab/use-wallet

A framework-agnostic Algorand wallet integration library (v4.x) with reactive adapters for React, Vue, SolidJS, and Svelte. Requires **algosdk v3**.

## Packages

| Package                       | Purpose                                       |
| ----------------------------- | --------------------------------------------- |
| `@txnlab/use-wallet`          | Core library (framework-agnostic)             |
| `@txnlab/use-wallet-react`    | React adapter (hooks + WalletProvider)        |
| `@txnlab/use-wallet-vue`      | Vue adapter (composables + plugin)            |
| `@txnlab/use-wallet-solid`    | SolidJS adapter (primitives + WalletProvider) |
| `@txnlab/use-wallet-svelte`   | Svelte adapter (primitives + context)         |
| `@txnlab/use-wallet-ui-react` | React UI components (WalletButton, menus)     |

## Routing Guide

Read the reference file that matches the developer's task:

### Setup & Configuration

- **Getting started (any framework)**: [references/getting-started.md](references/getting-started.md) — Installation, WalletManager config, supported wallets table, webpack fallbacks

### Framework-Specific Integration

- **Vanilla JS/TS (no framework)**: [references/vanilla.md](references/vanilla.md) — WalletManager direct usage, BaseWallet subscribe, no provider wrapper
- **React**: [references/react.md](references/react.md) — WalletProvider, useWallet, useNetwork hooks
- **Vue**: [references/vue.md](references/vue.md) — WalletManagerPlugin, useWallet/useNetwork composables
- **SolidJS**: [references/solid.md](references/solid.md) — WalletProvider, useWallet/useNetwork primitives (signals)
- **Svelte**: [references/svelte.md](references/svelte.md) — useWalletContext, useWallet/useNetwork primitives (.current)

### Features & Guides

- **Signing transactions**: [references/signing-transactions.md](references/signing-transactions.md) — signTransactions, transactionSigner with ATC, AlgoKit Utils
- **Signing data (ARC-60/SIWA)**: [references/signing-data.md](references/signing-data.md) — Sign In With Algorand, Lute wallet, verification
- **Network switching & custom networks**: [references/network-configuration.md](references/network-configuration.md) — NetworkConfigBuilder, custom AVM networks (Voi), runtime node config, useNetwork
- **Pre-built UI components**: [references/wallet-ui.md](references/wallet-ui.md) — @txnlab/use-wallet-ui-react: WalletButton, menus, theming, Tailwind setup
- **Testing**: [references/testing.md](references/testing.md) — Mnemonic wallet provider for dev/testing/E2E
- **Custom wallet provider**: [references/custom-provider.md](references/custom-provider.md) — Implementing CustomProvider interface

### Reference

- **Full API reference**: [references/api-reference.md](references/api-reference.md) — WalletManager, useWallet, useNetwork, enums, types
- **Migration from v3**: [references/migration-v3.md](references/migration-v3.md) — algosdk v3, network config changes, useNetwork extraction

## Quick Reference: Supported Wallets

| Wallet           | WalletId        | Required Package                                               |
| ---------------- | --------------- | -------------------------------------------------------------- |
| Pera             | `PERA`          | `@perawallet/connect`                                          |
| Defly            | `DEFLY`         | `@blockshake/defly-connect`                                    |
| Defly Web (beta) | `DEFLY_WEB`     | `@agoralabs-sh/avm-web-provider`                               |
| Exodus           | `EXODUS`        | —                                                              |
| Kibisis          | `KIBISIS`       | `@agoralabs-sh/avm-web-provider`                               |
| Lute             | `LUTE`          | `lute-connect`                                                 |
| WalletConnect    | `WALLETCONNECT` | `@walletconnect/sign-client`, `@walletconnect/modal`           |
| Magic            | `MAGIC`         | `magic-sdk`, `@magic-ext/algorand`                             |
| Web3Auth         | `WEB3AUTH`      | `@web3auth/modal`, `@web3auth/base`, `@web3auth/base-provider` |
| W3 Wallet        | `W3_WALLET`     | —                                                              |
| KMD              | `KMD`           | — (dev only)                                                   |
| Mnemonic         | `MNEMONIC`      | — (test only, never MainNet)                                   |
| Custom           | `CUSTOM`        | — (implement CustomProvider)                                   |

Wallets that require no extra package use built-in browser APIs or AVM web provider.

## Key Patterns

### Minimal Setup (React)

```tsx
import {
  WalletProvider,
  WalletManager,
  NetworkId,
  WalletId,
} from '@txnlab/use-wallet-react'

const manager = new WalletManager({
  wallets: [WalletId.PERA, WalletId.DEFLY, WalletId.LUTE],
  defaultNetwork: NetworkId.TESTNET,
})

function App() {
  return (
    <WalletProvider manager={manager}>
      <YourApp />
    </WalletProvider>
  )
}
```

### Accessing Wallet State

```tsx
const {
  wallets,
  activeAddress,
  isReady,
  signTransactions,
  transactionSigner,
  algodClient,
} = useWallet()
const {
  activeNetwork,
  setActiveNetwork,
  updateAlgodConfig,
  resetNetworkConfig,
} = useNetwork()
```

## Important Notes

- v4.x requires **algosdk v3** — see migration guide if upgrading from v3.x
- In v4.0.0, network features moved from `useWallet` to a separate `useNetwork` hook/composable/primitive
- Default networks (MainNet, TestNet, BetaNet, LocalNet) use Nodely's free API
- Some wallet providers require signature requests from direct user interaction (button clicks)
- Only Lute supports ARC-60 data signing (`signData`)
