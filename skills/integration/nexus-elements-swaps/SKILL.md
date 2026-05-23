---
name: nexus-elements-swaps
description: Install and use the Swaps widget (SwapWidget) from Nexus Elements. Use for cross-chain exact-in or exact-out swaps with intent progress UI.
---

# Nexus Elements - Swaps

## Overview
Install the SwapWidget component for cross-chain swaps with exact-in/out modes, progress UI, and optional callbacks.

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
npx shadcn@latest add @nexus-elements/swaps
```
Alternative:
```bash
npx shadcn@latest add https://elements.nexus.availproject.org/r/swaps.json
```

## Manual install (no shadcn)
1) Download `https://elements.nexus.availproject.org/r/swaps.json`.
2) Create each file in `files[].target` with `files[].content`.
3) Install dependencies listed in `dependencies` and each `registryDependencies` item.

## Usage
```tsx
import SwapWidget from "@/components/swaps/swap-widget";

<SwapWidget
  onStart={() => {}}
  onComplete={(amount) => console.log(amount)}
  onError={() => console.error("Swap failed")}
/>
```

## SDK flow mapping
- Uses `sdk.swapWithExactIn(...)` and `sdk.swapWithExactOut(...)`.
- Relies on the swap intent hook (`swapIntent`) for confirmation UI.
- Progress updates come from `NEXUS_EVENTS.SWAP_STEP_COMPLETE`.

## Props (SwapsProps)
- `onStart`, `onComplete`, `onError`

## Notes
- The widget handles exact-in and exact-out modes internally.
- If you need an error message, you can widen the `onError` signature in `swap-widget.tsx` to accept `(message?: string)`.
