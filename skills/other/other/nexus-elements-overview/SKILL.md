---
name: nexus-elements-overview
description: Overview and selection guide for Nexus Elements skills and prerequisites. Use when someone asks how to set up Nexus Elements, configure the registry, or choose which element (fast bridge, transfer, deposit, swaps, unified balance, view history, provider, common) to install.
---

# Nexus Elements Overview

## Overview
Select the right Nexus Elements sub-skill and ensure prerequisites (shadcn registry + NexusProvider + wallet connection) are in place.

## Prerequisites checklist
- Ensure shadcn/ui is initialized (a `components.json` exists) or be ready to manual copy files from `/r` JSON.
- Ensure wallet connection is configured (wagmi or any EIP-1193 provider).
- Install and wrap the app with `NexusProvider`; call `handleInit` on wallet connect.

### Provider setup (minimal)
```tsx
"use client";
import NexusProvider from "@/components/nexus/NexusProvider";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <NexusProvider>{children}</NexusProvider>;
}
```

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

## Registry info
- Base registry URL: `https://elements.nexus.availproject.org/r/{name}.json`
- If `components.json` exists, ensure this registry mapping exists:
```json
"registries": {
  "@nexus-elements/": "https://elements.nexus.availproject.org/r/{name}.json"
}
```

## Pick the right sub-skill
- Fast bridge UI: `nexus-elements-fast-bridge`
- Transfer UI: `nexus-elements-transfer` (registry name is `transfer`, docs sometimes say `fast-transfer`)
- Deposit widget (swap + execute via `swapAndExecute`): `nexus-elements-deposit`
- Bridge deposit (bridge + execute via `bridgeAndExecute`): `nexus-elements-bridge-deposit`
- Swaps widget: `nexus-elements-swaps`
- Unified balance display: `nexus-elements-unified-balance`
- View history (intent history): `nexus-elements-view-history` (no `view-intent` component exists)
- Provider setup: `nexus-elements-nexus-provider`
- Shared hooks/utils: `nexus-elements-common`

## SDK flow mapping (for answering questions)
- Fast bridge → `sdk.bridge` + intent/allowance hooks + `NEXUS_EVENTS.STEPS_LIST`/`STEP_COMPLETE`.
- Transfer → `sdk.bridgeAndTransfer` + intent/allowance hooks.
- Deposit → `sdk.swapAndExecute` + swap intent hook (`swapIntent`).
- Bridge deposit → `sdk.bridgeAndExecute` + intent/allowance hooks.
- Swaps → `sdk.swapWithExactIn` / `sdk.swapWithExactOut` + swap intent hook + `NEXUS_EVENTS.SWAP_STEP_COMPLETE`.
- Unified balance → `sdk.getBalancesForBridge` / `sdk.getBalancesForSwap` (via `NexusProvider`).
- View history → `sdk.getMyIntents()`.

## Manual install fallback
If shadcn is not initialized, use the `/r` JSON for a component and create each file in `files[].target` with `files[].content`. Repeat for all `registryDependencies` listed in that JSON and install the `dependencies` array.
