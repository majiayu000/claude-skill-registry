---
name: gdex-trading
description: Cross-chain DeFi trading skill for AI agents — spot trading, perpetual futures, portfolio management, and token discovery on Solana, Sui, and 12+ EVM chains via managed-custody wallets. Load gdex-onboarding to get started, or load a specific skill below for your task.
metadata:
  author: GemachDAO
  version: "1.0.0"
  argument-hint: <action> [params]
---

# GDEX Trading Skill

Cross-chain DeFi trading infrastructure for AI agents. All trading goes through encrypted `computedData` payloads (AES-256-CBC) with managed-custody wallets on the Gbot Trading Dashboard backend (`https://trade-api.gemach.io/v1`).

**Start here:** Load **gdex-onboarding** for a full overview and quickstart guide.

## Available Skills

| Category | Skill | Description | Auth Required? |
|----------|-------|-------------|----------------|
| **Getting Started** | `gdex-onboarding` | Platform overview, architecture, supported chains, quickstart | — |
| **Auth** | `gdex-authentication` | Managed-custody auth, encryption, session keys, API key login | — |
| **Trading** | `gdex-spot-trading` | Buy/sell tokens on any chain with DEX routing | Yes |
| | `gdex-perp-trading` | HyperLiquid perpetual futures — positions, orders, leverage, TP/SL | Yes |
| | `gdex-perp-funding` | Deposit/withdraw USDC to/from HyperLiquid | Yes |
| | `gdex-limit-orders` | Limit buy, limit sell, update/delete orders via encrypted payloads | Yes |
| **Data** | `gdex-portfolio` | Cross-chain portfolio, balances, trade history | Yes |
| | `gdex-token-discovery` | Token details, trending tokens, OHLCV, top traders | Yes |
| **Platform** | `gdex-copy-trading` | Copy trade wallets, create/delete configs, tx history, DEXes (Solana only for writes) | Discovery: No / Read+Write: Yes |
| | `gdex-perp-copy-trading` | HL perp copy trading — copy long/short futures positions, opposite copy, top traders, market data | Discovery: No / Read+Write: Yes |
| | `gdex-bridge` | Cross-chain bridging with quotes | Yes |
| | `gdex-wallet-setup` | Generate EVM wallets, session keys, wallet info | **No** |
| **Frontend** | `gdex-ui-install-setup` | React/Next.js project setup, SDK context providers, environment variables | — |
| | `gdex-ui-trading-components` | React component patterns for order forms, position tables, copy trade panels | — |
| | `gdex-ui-portfolio-dashboard` | Portfolio dashboard components — balances, trade history, chain selectors | — |
| | `gdex-ui-wallet-connection` | Wallet connection UI — connect buttons, auth state, chain switching | — |
| | `gdex-ui-theming` | CSS theming — dark/light mode, trading colors, responsive breakpoints, Tailwind | — |
| | `gdex-ui-page-layouts` | Full page compositions — trading, portfolio, copy trading, bridge pages | — |
| **Developer Tools** | `gdex-sdk-debugging` | Troubleshoot errors — error codes, encryption debugging, chain quirks, HL gotchas | — |

## Quick Decision Guide

- **"Buy/sell a token"** → Load `gdex-authentication` + `gdex-spot-trading`
- **"Open a perp position"** → Load `gdex-authentication` + `gdex-perp-funding` + `gdex-perp-trading`
- **"Check token price or trending"** → Load `gdex-authentication` + `gdex-token-discovery`
- **"Check portfolio/balances"** → Load `gdex-authentication` + `gdex-portfolio`
- **"User has no wallet"** → Load `gdex-wallet-setup` + `gdex-authentication`
- **"Copy a trader"** → Load `gdex-authentication` + `gdex-copy-trading` (sign-in must use `chainId: 622112261`)
- **"Copy a perp trader"** → Load `gdex-authentication` + `gdex-perp-copy-trading` (sign-in must use `chainId: 1`)
- **"Bridge tokens"** → Load `gdex-authentication` + `gdex-bridge`
- **"Create a limit order"** → Load `gdex-authentication` + `gdex-limit-orders`
- **"Set a limit buy"** → Load `gdex-authentication` + `gdex-limit-orders` (use `limitBuy()`)
- **"Set a take-profit/stop-loss sell"** → Load `gdex-authentication` + `gdex-limit-orders` (use `limitSell()`)
- **"Build a trading UI"** → Load `gdex-ui-install-setup` + `gdex-ui-trading-components` + `gdex-ui-theming`
- **"Create a portfolio dashboard"** → Load `gdex-ui-install-setup` + `gdex-ui-portfolio-dashboard`
- **"Build a complete trading app"** → Load `gdex-ui-install-setup` + `gdex-ui-page-layouts` + `gdex-ui-wallet-connection` + `gdex-ui-theming`
- **"Debug an error"** → Load `gdex-sdk-debugging`

## Critical Notes (Live-Tested)

> **walletAddress = CONTROL address, NOT managed address.** All HL write operations (`hlCreateOrder`, `hlCloseAll`, `perpDeposit`, etc.) require `walletAddress` set to the **control wallet address** used during sign-in — NOT the managed-custody address returned by `/v1/user`. The backend verifies the session key signature against the sign-in `userId`. Passing the managed address causes `400 Unauthorized (code 103)`.

> **`hlCloseAll` / `/v1/hl/close_all_positions` is unreliable.** It frequently returns `TIMEOUT` or JSON parse errors. To close positions reliably, place a **reduce-only** `hl_create_order` sell/buy for the exact position size instead.

> **`hlUpdateLeverage` / `/v1/hl/update_leverage` is not implemented** on the backend (returns 404). Leverage is set automatically when placing orders — pass the desired leverage indirectly via position sizing.

> **Solana chainId is `622112261`, NOT `900`.** The correct Solana chain ID is `ChainId.SOLANA = 622112261`. Using `900` falls back to the EVM managed address with `balance: null`. The `/v1/user` endpoint returns a **different managed wallet** per `chainId`:
> - `chainId=1` → EVM managed: `0x9967...`
> - `chainId=622112261` → Solana managed: `CFSi4YimeCbfSNqH2WmHwJKwj1YYG1cWBtQyVPB4sCe1` (base58)
> Always use `ChainId.SOLANA` from the SDK's enum to avoid this mistake.

> **Solana Meteora swaps are broken (backend bug).** Tokens that route through Meteora DLMM (e.g. BONK) fail with `Program error: 1` because the backend doesn’t wrap SOL into WSOL before calling `Swap2`. **Raydium-routed tokens work correctly** (e.g. WIF). Check `token.dexId` — if it's `"meteora"`, the swap will fail. Prefer tokens with `isRaydium: true` or `dexId: "raydium"`.

> **Solana trades need ~0.01 SOL minimum.** ATA (Associated Token Account) creation costs ~0.002 SOL per new token, plus priority fees (default 0.0005 SOL) and base tx fees. First trade on a new token needs ~0.007 SOL overhead beyond the swap amount.

> **Bridge endpoints use different paths than expected.** The actual backend routes are `GET /v1/bridge/estimate_bridge`, `POST /v1/bridge/request_bridge`, and `GET /v1/bridge/bridge_orders`. The `request_bridge` endpoint requires ABI-encoded + signed + AES-encrypted `computedData` (same pattern as managed trades). Bridge is **native tokens only** and uses ChangeNow as provider. Amounts must be in **raw token units** (wei/lamports). See **gdex-bridge** skill for full details.

> **Copy trade write operations (create/delete) use `chainId: 622112261` for sign-in, NOT `chainId: 1`.** The chainId field in the ABI is `uint256` (not string). The update endpoint uses 16 ABI fields (not 15): `[traderWallet, copyTradeName, chainId(uint256), gasPrice, buyMode, copyBuyAmount, isBuyExistingToken, lossPercent, profitPercent, nonce, copySell, excludedDexNumbers, copyTradeId, isDelete, isChangeStatus, excludedProgramIds]`. Both `isDelete='1'` and `isChangeStatus='1'` permanently delete the trade — there is no toggle. Boolean fields use `''` (empty string) for false and `'1'` for true; string `'0'` is truthy and will trigger deletion.

> **Limit order endpoints are `limit_buy` / `limit_sell` / `update_order` — NOT `orders/create` / `orders/cancel`.** Use `limitBuy()` for buy orders, `limitSell()` for sell orders (auto-classifies TP vs SL), and `updateOrder({ isDelete: true })` to cancel. Listing uses `GET /v1/orders` with `userId` + encrypted `data` + `chainId`. All write endpoints use ABI-encoded + signed + AES-encrypted `computedData` (same managed-custody pattern). Minimum order is ~0.01 native token. See **gdex-limit-orders** skill for full details.

> **HL perp copy trading is completely separate from Solana copy trading.** Uses `chainId: 1` (EVM), ABI methods `hl_create`/`hl_update` (8 and 11 string fields), and goes through `buildHlComputedData()`. Both `isDelete` and `isChangeStatus` permanently **DELETE** the trade (same as Solana — there is no toggle). Both TP and SL are **mandatory** (> 0). Max 3 copy trades per user. Supports opposite-direction copying via `oppositeCopy`. Backend stores ABI byte-offsets for `copyMode` and `oppositeCopy` (e.g., `copyMode=416`), not the actual values. `user_stats` requires the managed wallet address, not the control wallet. See **gdex-perp-copy-trading** skill for full details.

## Autonomous Agent Playbook

> **This section contains everything an autonomous AI agent needs to trade without human help.**

### Portfolio / Balances — Backend Param Mismatch (Live-Tested)

The high-level `getPortfolio()` and `getBalances()` methods send `walletAddress` + `chain`, but the backend expects `userId` + `chainId` + `data` (encrypted session key). **Workaround — use the raw client directly:**

```typescript
import { buildGdexUserSessionData } from '@gdexsdk/gdex-skill';
const data = buildGdexUserSessionData(sessionKey, apiKey);

// Portfolio
const portfolio = await skill.client.get('/v1/portfolio', {
  params: { userId: controlAddress, chainId: 622112261, data }
});

// Balances
const balances = await skill.client.get('/v1/balances', {
  params: { userId: controlAddress, chainId: 622112261, data }
});
```

### Trade History — Different Param Names (Live-Tested)

Backend expects `user` (not `userId`), and the managed Solana chainId for trade history is `900` (not `622112261`):

```typescript
const history = await skill.client.get('/v1/user_trade_history', {
  params: { user: controlAddress, chainId: 900, data, page: 1, limit: 20 }
});
```

### OHLCV / TopTraders — Numeric chainId Required (Live-Tested)

Backend needs numeric `chainId`, not string `chain`. These work:
```typescript
await skill.getOHLCV({ tokenAddress, chain: 622112261, resolution: '60', from, to });
await skill.getTopTraders({ chain: 622112261, period: '7d', limit: 5 });
```

### Spot Trading (Managed Custody) — Raw Units Required (Live-Tested)

For managed-custody trades, amounts must be in **raw units** (lamports for Solana, wei for EVM), NOT float:
```typescript
// ❌ WRONG: amount: '0.01'
// ✅ CORRECT: amount: '10000000' (0.01 SOL = 10000000 lamports)
```

### Limit Orders — profitPercent/lossPercent MUST Be uint256 (Live-Tested)

The `limit_buy` and `update_order` ABI schemas use `uint256` for `profitPercent` and `lossPercent` — NOT `string`. The backend decodes them as uint256 and validates 0-100 range. Using `string` type produces ABI byte-offsets (e.g. 192) that always fail. The SDK handles this correctly.

### Endpoints That Don't Work (Live-Tested)

| Endpoint | Status | Alternative |
|----------|--------|-------------|
| `hlCloseAll` / `/v1/hl/close_all_positions` | Returns TIMEOUT/400 | Use `hlCreateOrder` with `reduceOnly: true, isMarket: true` |
| `hlUpdateLeverage` / `/v1/hl/update_leverage` | Returns 404 | Leverage is set automatically by the backend per order |
| `getGbotUsdcBalance` | Returns 404 | Use `getHlAccountState()` to check USDC balance |
| `getHlUserStats(controlAddress)` | Returns 400 | Must pass the **managed** wallet address, not control |

### Error Recovery for Autonomous Agents

| Error | What to Do |
|-------|------------|
| `400 Unauthorized (103)` | Check: (1) using control address not managed, (2) ABI types match exactly, (3) session key is from the same sign-in |
| `Insufficient balance` | Check managed wallet balance on the correct chain. For HL, check USDC deposit amount. |
| `TIMEOUT` on hlCloseAll | Use reduce-only order instead (see above) |
| `Program error: 1` on Solana | Token routes through Meteora DLMM. Swap to a Raydium-routed token instead. |
| `lossPercent must be between 0 and 100` | ABI encoding bug — profitPercent/lossPercent must be uint256, not string |
| `404` on leverage | Expected — leverage is auto-set. Control via position sizing. |
| `Reused nonce` | Always generate fresh: `String(Math.floor(Date.now() / 1000) + Math.floor(Math.random() * 1000))` |
| Rate limited (429) | SDK auto-retries with exponential backoff. If manual, wait `retryAfter` seconds. |

### Live-Tested E2E Results (39/42 Pass)

| Section | Tests | Pass | Notes |
|---------|-------|------|-------|
| Auth & Portfolio | 7 | 7/7 | Sign-in, resolve user, portfolio (raw client), balances, trade history |
| Token Discovery | 3 | 3/3 | Token details, trending, OHLCV |
| Top Traders | 1 | 1/1 | Top traders by PnL |
| Spot Trading | 3 | 3/3 | Buy WIF (Solana), sell WIF, poll status |
| HL Perp Trading | 10 | 8/10 | Deposit, create order, positions, close (reduce-only). `getGbotUsdcBalance` 404, `hlCloseAll` 400 |
| Limit Orders | 4 | 4/4 | List, create (limit buy), verify, cancel |
| Copy Trading Reads | 4 | 4/4 | Wallets, custom wallets, gems, DEXes |
| HL Copy Trading Reads | 8 | 7/8 | Top traders, top by PnL, assets, DEXes, deposit tokens. `getHlUserStats` needs managed addr |
| Bridge Estimate | 1 | 1/1 | ETH→ARB estimate |
| Wallet Generation | 1 | 1/1 | Offline EVM wallet |

## Quick Start

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY } from '@gdexsdk/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);

// No-auth endpoints work immediately
const trending = await skill.getTrendingTokens({ chain: 'solana', period: '24h', limit: 5 });

// Auth-required endpoints
const trade = await skill.buyToken({
  chain: 'solana',
  tokenAddress: 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
  amount: '0.1',
  slippage: 1,
});
```

**Shared API Keys:** `9b4e1c73-6a2f-4d88-b5c9-3e7a2f1d6c54` (primary), `2c8f0a91-5d34-4e7b-9a62-f1c3d8e4b705` (secondary)

## Installation

```bash
# Install all skills
npx skills add GemachDAO/gdex-skill --all --agent '*' -g

# Install SDK
npm install @gdexsdk/gdex-skill
```
| userId | Control wallet address (from sign-in), NOT managed wallet |
| Bridge receiver | `0x2Df1c51E09aECF9cacB7bc98cB1742757f163dF7` |

### HL Signature Format

All HL write operations sign with the **session private key** (registered during sign-in):
```
message = "{action}-{userId.toLowerCase()}-{dataHex}" // e.g. "hl_deposit-0x53d0...-0000..."
digest  = keccak256(utf8Bytes(message))
output  = r(64hex) + s(64hex) + v(2hex)  // 130 chars, v=00/01, no 0x prefix
```

### HL Error Codes

| Code | Error | Common Cause |
|---|---|---|
| 103 | Unauthorized | Wrong ABI type (uint256 instead of uint64), wrong userId, or signing with wrong key |
| 102 | Invalid chainId | chainId is not 42161 |
| 102 | Invalid params | Reused nonce or unsupported token |
| — | Insufficient balance | Managed wallet needs more USDC + fee on Arbitrum |
| — | Too low amount | Amount < 10 USDC (10000000 smallest unit) |
