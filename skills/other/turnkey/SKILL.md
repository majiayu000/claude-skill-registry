---
name: turnkey
description: 'Thirdweb server wallets for server-side wallet creation and gasless transaction execution. Use when working with thirdweb server wallets, EIP-7702 gasless transactions, custodial wallets, or automated trading wallets. Triggers on: "thirdweb server wallet", "server wallet", "custodial wallet", "gasless", "sendSponsoredTransaction", "createServerWallet".'
---

## Overview

AutoClaw uses thirdweb server wallets (replacing Privy). Use for:
- Creating application-owned wallets via thirdweb API
- Gasless transaction execution (EIP-7702)
- EIP-712 signing for ERC-8004 agent linking

## Wallet Creation

```ts
import { createServerWallet } from '../lib/thirdweb-wallet';

// Idempotent for same identifier
const { address } = await createServerWallet(`agent-fx-${walletAddress.toLowerCase()}`);
```

## Transaction Execution (Gasless)

```ts
import { sendTransactionFromServerWallet } from '../lib/thirdweb-wallet';

const hash = await sendTransactionFromServerWallet(serverWalletAddress, {
  to: '0x...',
  data: '0x...',
  value: 0n, // optional
});
```

## Identifier Conventions

| Wallet | Identifier |
|--------|------------|
| ERC-8004 registrar | `erc8004-registrar` |
| FX agent (per user) | `agent-fx-{walletAddress}` |
| Yield agent (per user) | `agent-yield-{walletAddress}` |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `THIRDWEB_SECRET_KEY` | thirdweb API secret (wallet creation, sponsored txs) |
| `THIRDWEB_ADMIN_PRIVATE_KEY` | SIWE auth only (not for server wallets) |

## Important Notes

- Gas is sponsored by thirdweb — no fee buffer needed for Max button
- Server wallets are created via REST API at api.thirdweb.com
- `createServerWallet` is idempotent for the same identifier
