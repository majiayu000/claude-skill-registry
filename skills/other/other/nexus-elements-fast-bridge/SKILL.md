---
name: nexus-elements-fast-bridge
description: Install and use the Fast Bridge widget from Nexus Elements. Use when someone wants an intent-based cross-chain bridge UI with allowance flow and progress steps.
---

# Nexus Elements - Fast Bridge

## Overview
Install the FastBridge component and wire it to NexusProvider for intent-based bridging with allowance handling and progress steps.

## Prerequisites
- NexusProvider installed and initialized on wallet connect.
- Wallet connection configured; you have the connected wallet address.

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
npx shadcn@latest add @nexus-elements/fast-bridge
```
Alternative:
```bash
npx shadcn@latest add https://elements.nexus.availproject.org/r/fast-bridge.json
```

## Manual install (no shadcn)
1) Download `https://elements.nexus.availproject.org/r/fast-bridge.json`.
2) Create each file in `files[].target` with `files[].content`.
3) Install dependencies listed in `dependencies` and each `registryDependencies` item.

## Usage
```tsx
import FastBridge from "@/components/fast-bridge/fast-bridge";
import { SUPPORTED_CHAINS } from "@avail-project/nexus-core";

<FastBridge
  connectedAddress={address}
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
- Uses `sdk.bridge(...)` under the hood (intent-based bridge).
- Relies on intent + allowance hooks (`intent`, `allowance`) for confirmation UI.
- Progress updates come from `NEXUS_EVENTS.STEPS_LIST` and `NEXUS_EVENTS.STEP_COMPLETE`.

## Props (FastBridgeProps)
- `connectedAddress`: connected wallet address (required)
- `prefill`: `{ token, chainId, amount?, recipient? }`
- `onStart`, `onComplete`, `onError`

## Notes
- FastBridge renders `ViewHistory` if installed; keep it if you want intent history.
- If the wallet disconnects, ensure you re-run `handleInit` on reconnect.
