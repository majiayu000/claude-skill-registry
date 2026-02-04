---
name: nexus-elements-unified-balance
description: Install and use the Unified Balance component for cross-chain balance aggregation. Use when you need a balance panel with per-chain breakdown.
---

# Nexus Elements - Unified Balance

## Overview
Install the UnifiedBalance component to display aggregated token balances across chains with per-chain breakdown.

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
npx shadcn@latest add @nexus-elements/unified-balance
```
Alternative:
```bash
npx shadcn@latest add https://elements.nexus.availproject.org/r/unified-balance.json
```

## Manual install (no shadcn)
1) Download `https://elements.nexus.availproject.org/r/unified-balance.json`.
2) Create each file in `files[].target` with `files[].content`.
3) Install dependencies listed in `dependencies` and each `registryDependencies` item.

## Usage
```tsx
import UnifiedBalance from "@/components/unified-balance/unified-balance";

<UnifiedBalance className="max-w-lg" />
```

## SDK flow mapping
- Displays `bridgableBalance` and `swapBalance` from `NexusProvider` (from `sdk.getBalancesForBridge()` / `sdk.getBalancesForSwap()`).
- Uses `nexusSDK.utils.formatTokenBalance(...)` for display formatting.

## Props (UnifiedBalanceProps)
- `className?`: optional container className
