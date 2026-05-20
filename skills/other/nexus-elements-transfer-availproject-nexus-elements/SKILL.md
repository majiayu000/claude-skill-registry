---
name: nexus-elements-transfer
description: Install and use the Fast Transfer widget (registry name: transfer) from Nexus Elements. Use for intent-based cross-chain transfers to a recipient.
---

# Nexus Elements - Transfer

## Overview
Install the FastTransfer component (registry item name is `transfer`) for intent-based cross-chain transfers with allowance flow and progress UI.

## Prerequisites
- NexusProvider installed and initialized on wallet connect.
- Wallet connection configured.

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
npx shadcn@latest add @nexus-elements/transfer
```
Alternative:
```bash
npx shadcn@latest add https://elements.nexus.availproject.org/r/transfer.json
```

## Manual install (no shadcn)
1) Download `https://elements.nexus.availproject.org/r/transfer.json`.
2) Create each file in `files[].target` with `files[].content`.
3) Install dependencies listed in `dependencies` and each `registryDependencies` item.

## Usage
```tsx
import FastTransfer from "@/components/transfer/transfer";
import { SUPPORTED_CHAINS } from "@avail-project/nexus-core";

<FastTransfer
  prefill={{
    token: "USDC",
    chainId: SUPPORTED_CHAINS.BASE,
  }}
  onStart={() => {}}
  onComplete={() => {}}
  onError={(message) => console.error(message)}
/>
```

## SDK flow mapping
- Uses `sdk.bridgeAndTransfer(...)` under the hood.
- Relies on intent + allowance hooks (`intent`, `allowance`) for confirmation UI.
- Progress updates come from `NEXUS_EVENTS.STEPS_LIST` and `NEXUS_EVENTS.STEP_COMPLETE`.

## Props (FastTransferProps)
- `prefill`: `{ token, chainId, amount?, recipient? }`
- `onStart`, `onComplete`, `onError`

## Notes
- Docs refer to this as `fast-transfer`, but the registry item is `transfer`.
- FastTransfer renders `ViewHistory` if installed.
