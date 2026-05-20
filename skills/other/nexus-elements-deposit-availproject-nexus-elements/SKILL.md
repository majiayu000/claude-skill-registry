---
name: nexus-elements-deposit
description: Install and use the Nexus Deposit widget (swap + execute via swapAndExecute). Use when integrating the full deposit flow with destination config and custom execute builder.
---

# Nexus Elements - Deposit

## Overview
Install the NexusDeposit widget for a full swap-and-execute deposit flow with unified balances, fee preview, and progress UI.

## Prerequisites
- NexusProvider installed and initialized on wallet connect.
- Wallet connection configured.
- You can build an execute call (contract address + encoded data) for the target protocol.

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
npx shadcn@latest add @nexus-elements/deposit
```
Alternative:
```bash
npx shadcn@latest add https://elements.nexus.availproject.org/r/deposit.json
```

## Manual install (no shadcn)
1) Download `https://elements.nexus.availproject.org/r/deposit.json`.
2) Create each file in `files[].target` with `files[].content`.
3) Install dependencies listed in `dependencies` and each `registryDependencies` item.

## Usage
```tsx
import NexusDeposit from "@/components/deposit/nexus-deposit";
import {
  SUPPORTED_CHAINS,
  TOKEN_CONTRACT_ADDRESSES,
  TOKEN_METADATA,
  CHAIN_METADATA,
} from "@avail-project/nexus-core";
import { encodeFunctionData, type Abi } from "viem";

<NexusDeposit
  destination={{
    chainId: SUPPORTED_CHAINS.BASE,
    tokenAddress: TOKEN_CONTRACT_ADDRESSES["USDC"][SUPPORTED_CHAINS.BASE],
    tokenSymbol: "USDC",
    tokenDecimals: TOKEN_METADATA["USDC"].decimals,
    tokenLogo: TOKEN_METADATA["USDC"].icon,
    label: "Deposit USDC on Aave Base",
    gasTokenSymbol: CHAIN_METADATA[SUPPORTED_CHAINS.BASE].nativeCurrency.symbol,
    explorerUrl: CHAIN_METADATA[SUPPORTED_CHAINS.BASE].blockExplorerUrls[0],
    estimatedTime: "~= 30s",
  }}
  executeDeposit={(tokenSymbol, tokenAddress, amount, _chainId, user) => {
    const contractAddress = "0x..." as const;
    const abi: Abi = [
      {
        inputs: [
          { internalType: "address", name: "asset", type: "address" },
          { internalType: "uint256", name: "amount", type: "uint256" },
          { internalType: "address", name: "onBehalfOf", type: "address" },
          { internalType: "uint16", name: "referralCode", type: "uint16" },
        ],
        name: "supply",
        outputs: [],
        stateMutability: "nonpayable",
        type: "function",
      },
    ];

    const data = encodeFunctionData({
      abi,
      functionName: "supply",
      args: [tokenAddress, amount, user, 0],
    });

    return {
      to: contractAddress,
      data,
      tokenApproval: {
        token: tokenSymbol,
        amount,
        spender: contractAddress,
      },
    };
  }}
/>
```

## SDK flow mapping
- Uses `sdk.swapAndExecute(...)` under the hood.
- Relies on the swap intent hook (`swapIntent`) for confirmation UI.
- Progress updates come from `NEXUS_EVENTS.SWAP_STEP_COMPLETE`.

## Props (DepositWidgetProps)
- `destination` (required): chainId, tokenAddress, tokenSymbol, tokenDecimals, tokenLogo?, label?, estimatedTime?, gasTokenSymbol?, explorerUrl?, depositTargetLogo?
- `executeDeposit` (required): returns `{ to, data, value?, tokenApproval? }`
- `embed`, `heading`, `className` for layout
- `open`, `onOpenChange`, `defaultOpen` for modal control
- `onSuccess`, `onError`, `onClose`

## Notes
- Use `embed={true}` for inline rendering; default renders a modal.
- `executeDeposit` receives `amount` in smallest units (`bigint`); return calldata + optional `tokenApproval`.
