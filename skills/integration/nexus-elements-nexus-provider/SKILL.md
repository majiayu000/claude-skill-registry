---
name: nexus-elements-nexus-provider
description: Install and configure the NexusProvider for Nexus Elements. Use when setting up provider context, handleInit on wallet connect, or when any element needs useNexus.
---

# Nexus Elements - NexusProvider

## Overview
Install `NexusProvider`, initialize the SDK once on wallet connect, and access Nexus context via `useNexus`. All Nexus Elements widgets depend on this provider.

## What NexusProvider does
- Creates a single `NexusSDK` instance (configurable `network` and `debug`).
- Initializes the SDK with an EIP-1193 provider (`handleInit`).
- Preloads:
  - supported chains/tokens (bridge + swap)
  - bridgeable and swappable balances
  - exchange rates (Coinbase) for fiat display
- Attaches SDK hooks for intent, allowance, and swap intent previews.
- Exposes all of the above to components via `useNexus()`.

## Install (shadcn registry)
1) Ensure shadcn/ui is initialized (`components.json` exists).
2) Ensure registry mapping exists:
```json
"registries": {
  "@nexus-elements/": "https://elements.nexus.availproject.org/r/{name}.json"
}
```
3) Install:
```bash
npx shadcn@latest add @nexus-elements/nexus-provider
```
Alternative:
```bash
npx shadcn@latest add https://elements.nexus.availproject.org/r/nexus-provider.json
```

## Manual install (no shadcn)
1) Download `https://elements.nexus.availproject.org/r/nexus-provider.json`.
2) Create each file in `files[].target` with `files[].content`.
3) Install dependencies: `@avail-project/nexus-core@1.0.0-beta.64` and `wagmi`.

## Usage
Wrap your app:
```tsx
"use client";
import NexusProvider from "@/components/nexus/NexusProvider";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <NexusProvider>{children}</NexusProvider>;
}
```

Initialize on wallet connect (wagmi example):
```tsx
"use client";
import { useEffect } from "react";
import { useAccount } from "wagmi";
import type { EthereumProvider } from "@avail-project/nexus-core";
import { useNexus } from "@/components/nexus/NexusProvider";

export function InitNexusOnConnect() {
  const { status, connector } = useAccount();
  const { handleInit } = useNexus();

  useEffect(() => {
    if (status === "connected") {
      connector?.getProvider().then((p) => handleInit(p as EthereumProvider));
    }
  }, [status, connector, handleInit]);

  return null;
}
```

## What `useNexus()` provides
- `nexusSDK`: initialized SDK instance (or `null` before init)
- `handleInit(provider)`: init + preload + attach hooks
- `initializeNexus(provider)` / `deinitializeNexus()`: manual lifecycle control
- `intent`, `allowance`, `swapIntent`: refs for SDK hooks (must call `allow()`/`deny()`)
- `supportedChainsAndTokens`, `swapSupportedChainsAndTokens`
- `bridgableBalance`, `swapBalance`
- `exchangeRate`, `getFiatValue(amount, symbol)`
- `fetchBridgableBalance()`, `fetchSwapBalance()`
- `loading`, `network`

## Notes
- `handleInit` expects an EIP-1193 provider with `request()`.
- Optional `config` supports `network` (`"mainnet"`/`"testnet"` or custom) and `debug`.
- Hooks are attached in `handleInit`; if you override hooks elsewhere, always call `allow()`/`deny()` or flows will stall.
- Provider auto-deinitializes on wallet disconnect via wagmi `useAccountEffect`; if not using wagmi, call `deinitializeNexus()` manually.
