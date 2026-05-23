---
name: nexus-elements-bridge-deposit
description: Install and use the Bridge Deposit widget (simple bridge deposit flow). Use when you want a lighter deposit UI without the full execute builder.
---

# Nexus Elements - Bridge Deposit

## Overview
Install the Bridge Deposit widget for a simple bridge-and-execute deposit flow. This is lighter than the full Deposit widget.

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
npx shadcn@latest add @nexus-elements/bridge-deposit
```
Alternative:
```bash
npx shadcn@latest add https://elements.nexus.availproject.org/r/bridge-deposit.json
```

## Manual install (no shadcn)
1) Download `https://elements.nexus.availproject.org/r/bridge-deposit.json`.
2) Create each file in `files[].target` with `files[].content`.
3) Install dependencies listed in `dependencies` and each `registryDependencies` item.

## Usage
```tsx
import NexusDeposit from "@/components/bridge-deposit/deposit";
import { SUPPORTED_CHAINS, TOKEN_METADATA } from "@avail-project/nexus-core";
import { parseUnits } from "viem";

<NexusDeposit
  address={address}
  chain={SUPPORTED_CHAINS.BASE}
  token="USDC"
  heading="Deposit USDC"
  destinationLabel="Deposit to Aave"
  embed={false}
  depositExecute={(token, amount, chainId, userAddress) => {
    const decimals = TOKEN_METADATA[token].decimals;
    const amountWei = parseUnits(amount, decimals);
    return {
      to: "0x...",
      data: "0x...",
      tokenApproval: {
        token,
        amount: amountWei,
        spender: "0x...",
      },
    };
  }}
/>
```

## SDK flow mapping
- Uses `sdk.bridgeAndExecute(...)` under the hood.
- Relies on intent + allowance hooks (`intent`, `allowance`) for confirmation UI.
- Progress updates come from `NEXUS_EVENTS.STEPS_LIST` and `NEXUS_EVENTS.STEP_COMPLETE`.

## Props (NexusDepositProps)
- `address` (required): connected wallet address
- `chain` (required): destination chain id
- `token` (optional, default "USDC")
- `chainOptions` (optional): customize source chains list
- `depositExecute` (required): returns `{ to, data, value?, tokenApproval? }`
- `heading`, `embed`, `destinationLabel`

## Notes
- Use `embed={true}` to render inline, otherwise a modal is shown.
- This is distinct from the full `deposit` widget which uses `swapAndExecute` and broader asset selection.
