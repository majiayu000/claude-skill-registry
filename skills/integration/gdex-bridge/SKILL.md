---
name: gdex-bridge
description: Cross-chain bridging — get estimates and execute native token transfers between EVM chains, Solana, and Sui via ChangeNow
---

# GDEX: Cross-Chain Bridge

Bridge **native tokens** between supported chains with quote previews and time estimates.
Uses ChangeNow as the bridge provider (StarGate support exists but is currently disabled).

## When to Use

- Moving native tokens from one chain to another (e.g., ETH on Ethereum → ETH on Base)
- Getting a bridge estimate before executing
- Checking bridge order history

## Prerequisites

- `@gdexsdk/gdex-skill` installed
- Authenticated via managed-custody sign-in — see **gdex-authentication**
- Session keypair (sessionPrivateKey + sessionKey) from sign-in flow

## Backend Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/v1/bridge/estimate_bridge` | Get a bridge quote |
| `POST` | `/v1/bridge/request_bridge` | Execute a bridge (encrypted) |
| `GET` | `/v1/bridge/bridge_orders` | List bridge order history |

## 1. Get a Bridge Estimate (Quote)

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY } from '@gdexsdk/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);

const estimate = await skill.estimateBridge({
  fromChainId: 1,        // Ethereum
  toChainId: 8453,       // Base
  amount: '1000000000000000000',  // 1 ETH in wei
});
```

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `fromChainId` | `number` | Yes | Source chain ID |
| `toChainId` | `number` | Yes | Destination chain ID |
| `amount` | `string` | Yes | Amount in **raw token units** (wei for EVM, lamports for Solana) |

### Estimate Response

```typescript
interface BridgeEstimate {
  tool: string;              // "ChangeNow"
  fromChainId: number;
  fromAmount: string;        // input amount (raw units)
  toChainId: number;
  estimateAmount: string;    // estimated output (raw units)
  minEstimateTime: number;   // seconds
  maxEstimateTime: number;   // seconds
}
```

### Error Codes
| Code | Meaning |
|------|---------|
| 101 | Missing params / same chain / unsupported chain |
| 106 | ChangeNow API error |
| 107 | Unsupported chain (e.g., Fraxtal 252) or catch-all |

## 2. Execute a Bridge

The bridge endpoint requires an **AES-encrypted `computedData` payload** containing ABI-encoded parameters and a secp256k1 signature — the same pattern as managed spot trades.

```typescript
import {
  GdexSkill,
  GDEX_API_KEY_PRIMARY,
  generateGdexSessionKeyPair,
  buildGdexSignInMessage,
  buildGdexSignInComputedData,
} from '@gdexsdk/gdex-skill';
import { ethers } from 'ethers';

// After sign-in (you have sessionPrivateKey from the auth flow):
const result = await skill.requestBridge({
  fromChainId: 1,          // Ethereum
  toChainId: 8453,         // Base
  amount: '1000000000000000000',  // 1 ETH in wei
  userId: controlAddress,
  sessionPrivateKey,
  apiKey: GDEX_API_KEY_PRIMARY,
});

if (result.isSuccess) {
  console.log('TX hash:', result.hash);
  console.log(`ETA: ${result.minTime}-${result.maxTime}s`);
}
```

### Encryption Protocol

The SDK handles this automatically, but for reference:

1. **ABI-encode data**: `['string', 'uint64', 'uint64', 'string']` → `[amount, fromChainId, toChainId, nonce]`
2. **Sign message**: `"request_bridge-{userId.toLowerCase()}-{dataHex}"` using secp256k1 session key
3. **Encrypt JSON**: `{ userId, data, signature }` → AES-256-CBC with key/IV derived from SHA256(apiKey)
4. **POST body**: `{ computedData: "<hex>" }`

### Bridge Result

```typescript
interface BridgeResult {
  isSuccess: boolean;
  hash: string | null;       // source chain tx hash
  message: string;
  minTime?: number;          // seconds
  maxTime?: number;          // seconds
  error?: string;            // on failure
}
```

### Error Codes
| Code | Meaning |
|------|---------|
| 101 | Missing params / same chain / unsupported chain |
| 102 | Invalid or reused nonce |
| 103 | User wallet not found on chain |
| 104 | Unauthorized (signature verification failed) |
| 105 | Below minimum bridge amount / insufficient balance |

## 3. Get Bridge Order History

```typescript
import { buildGdexUserSessionData, GDEX_API_KEY_PRIMARY } from '@gdexsdk/gdex-skill';

const data = buildGdexUserSessionData(sessionKey, GDEX_API_KEY_PRIMARY);
const orders = await skill.getBridgeOrders({
  userId: controlAddress,
  data,
});
console.log(`${orders.count} bridge orders`);
orders.bridgeOrders.forEach(o => {
  console.log(`${o.fromChainId} → ${o.toChainId}: ${o.fromAmount} (tx: ${o.txHash})`);
});
```

### Response

```typescript
interface BridgeOrdersResponse {
  count: number;
  bridgeOrders: BridgeOrder[];
}

interface BridgeOrder {
  userId: string;
  fromChainId: number;
  toChainId: number;
  fromAmount: string;
  estimateToAmount: string;
  fromWallet: string;
  toWallet: string;
  txHash: string;
  requestTime: number;
}
```

## Supported Chains for Bridging

Controlled by backend `config.bridgeSupportedChainIds`. Known supported:

| Chain | ChainId |
|-------|---------|
| Ethereum | `1` |
| Optimism | `10` |
| BSC | `56` |
| Sonic | `146` |
| Base | `8453` |
| Arbitrum | `42161` |
| Berachain | `80094` |
| Solana | `622112261` |
| Sui | `1313131213` |

> **Fraxtal (252) is explicitly blocked** by the backend and will return error code 107.

## Key Points

- **Native tokens only** — the bridge transfers the chain's native token (ETH, SOL, BNB, etc.), not arbitrary ERC-20s.
- **Amounts in raw units** — use wei for EVM (1 ETH = `"1000000000000000000"`), lamports for Solana (1 SOL = `"1000000000"`).
- **Minimum bridge amount** — each chain has a `minBridge` config (default 1 in native decimals). Below this triggers error 105.
- **Nonce required** — each `requestBridge` call uses a unique nonce verified server-side. The SDK generates this automatically.
- **ChangeNow provider** — all bridges currently go through ChangeNow (StarGate code exists but is disabled).

## Autonomous Agent Notes (Live-Tested)

1. **`estimateBridge` works with API key only (E2E verified).** No session key or full sign-in needed for quotes.
2. **`requestBridge` requires full managed-custody auth** (session key + ABI encoding + AES encryption).
3. **Bridge paths are non-obvious:** `GET /v1/bridge/estimate_bridge`, `POST /v1/bridge/request_bridge`, `GET /v1/bridge/bridge_orders`. Do NOT use `/v1/bridge/estimate` or `/v1/bridge/execute`.
4. **Fraxtal (252) is explicitly blocked** and returns error 107.
5. **Bridge times vary:** ETH→ARB is ~5-15 min, Solana→EVM can take longer.
6. **For autonomous pre-trade funding:** Use `estimateBridge` to check feasibility before committing. If `estimateAmount` is too low (high fee), consider alternative routes.

## Related Skills

- **gdex-authentication** — Auth setup required for bridging
- **gdex-portfolio** — Check balances on target chain after bridging
- **gdex-spot-trading** — Trade on the destination chain after bridging
