---
name: gdex-onboarding
description: Start here — GDEX overview, architecture, supported chains, available skills, and quickstart for cross-chain DeFi trading via managed-custody wallets
---

# GDEX: Agent Onboarding

GDEX is a cross-chain DeFi trading infrastructure for AI agents. It provides spot trading, perpetual futures (HyperLiquid), portfolio management, token discovery, copy trading, and bridging across Solana, Sui, and 12+ EVM chains — all through a single SDK with managed-custody wallets.

## When to Use

- You're new to GDEX and need to understand the platform
- You need to decide which skill to load for a specific task
- You want a quick overview of supported chains and capabilities

## Architecture

```
Agent → @gdexsdk/gdex-skill SDK → GDEX Backend (trade-api.gemach.io/v1) → On-chain Execution
```

**Key concepts:**
- **Managed custody** — GDEX provisions and manages all on-chain trading wallets server-side. Your control wallet only signs in once.
- **Encrypted payloads** — All trades use AES-256-CBC encrypted `computedData` payloads. The API key derives the AES key deterministically via SHA256 hash chain.
- **Session keypairs** — A secp256k1 session key signs trade payloads after initial control-wallet sign-in.
- **Shared API keys** — Pre-configured keys let agents authenticate instantly without wallet signing.

## Quick Start

```bash
npm install @gdexsdk/gdex-skill
```

```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY } from '@gdexsdk/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);

// No-auth: check trending tokens
const trending = await skill.getTrendingTokens({ chain: 'solana', period: '24h', limit: 5 });

// Auth required: buy a token
const trade = await skill.buyToken({
  chain: 'solana',
  tokenAddress: 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
  amount: '0.1',
  slippage: 1,
});
```

**Shared API Keys (pre-configured for all agents):**
- Primary: `9b4e1c73-6a2f-4d88-b5c9-3e7a2f1d6c54`
- Secondary: `2c8f0a91-5d34-4e7b-9a62-f1c3d8e4b705`

## Supported Chains

| Chain | ChainId | DEXes | Perps | Bridge |
|-------|---------|-------|-------|--------|
| Ethereum | `1` | Uniswap v2/v3, Odos | — | Yes |
| Optimism | `10` | Uniswap v3, Odos | — | Yes |
| BSC | `56` | PancakeSwap, Odos | — | Yes |
| Sonic | `146` | — | — | Yes |
| Fraxtal | `252` | Uniswap v3 | — | Yes |
| Nibiru | `6900` | — | — | Yes |
| Base | `8453` | Uniswap v3, Odos, Arcadia | — | Yes |
| Arbitrum | `42161` | Uniswap v3, Odos | — | Yes |
| Berachain | `80094` | — | — | Yes |
| Solana | `622112261` / `'solana'` | Raydium, Raydium v2, Orca | — | Yes |
| Sui | `1313131213` / `'sui'` | Cetus, Bluefin | — | Yes |
| HyperLiquid | — | — | Native perp engine | — |

**Chain IDs for managed-custody:** 900 = Solana, 101 = Sui, or standard EVM chain IDs.

## Available Skills

| Category | Skill | Description |
|----------|-------|-------------|
| **Getting Started** | `gdex-onboarding` | **You are here** — Overview, architecture, quickstart |
| **Auth** | `gdex-authentication` | Managed-custody auth, encryption, session key flow |
| **Trading** | `gdex-spot-trading` | Buy/sell tokens on any supported chain |
| | `gdex-perp-trading` | HyperLiquid perpetual futures — positions, orders, leverage |
| | `gdex-perp-funding` | Deposit/withdraw USDC to/from HyperLiquid |
| | `gdex-limit-orders` | Create, cancel, and list limit orders |
| **Data** | `gdex-portfolio` | Cross-chain portfolio, balances, trade history |
| | `gdex-token-discovery` | Token details, trending tokens, OHLCV charts (no auth) |
| **Platform** | `gdex-copy-trading` | Copy trade wallets, create/manage configs, tx history, DEXes (Solana writes only) |
| | `gdex-perp-copy-trading` | HL perp copy trading — top traders, create/manage configs, market data |
| | `gdex-bridge` | Cross-chain bridging with quotes |
| | `gdex-wallet-setup` | Generate EVM wallets, session keys, get wallet info |
| **Frontend** | `gdex-ui-install-setup` | React/Next.js project setup, SDK context providers |
| | `gdex-ui-trading-components` | React component patterns for trading UIs |
| | `gdex-ui-portfolio-dashboard` | Portfolio dashboard components |
| | `gdex-ui-wallet-connection` | Wallet connection UI and auth flows |
| | `gdex-ui-theming` | CSS theming — dark/light mode, trading colors |
| | `gdex-ui-page-layouts` | Full page compositions for trading apps |
| **Developer Tools** | `gdex-sdk-debugging` | Troubleshoot errors, chain quirks, common pitfalls |

## Recommended Next Steps

**If you want to trade tokens (spot):**
1. Load **gdex-authentication** for auth setup
2. Load **gdex-spot-trading** for buy/sell operations

**If you want perpetual futures:**
1. Load **gdex-authentication** for auth setup
2. Load **gdex-perp-funding** to deposit USDC to HyperLiquid
3. Load **gdex-perp-trading** for positions and orders

**If you just need market data (no auth):**
1. Load **gdex-token-discovery** — works immediately, no authentication needed

**If the user has no wallet:**
1. Load **gdex-wallet-setup** to generate an EVM control wallet
2. Load **gdex-authentication** to sign in via managed custody

**If you want to copy successful traders:**
1. Load **gdex-authentication** for auth setup
2. Load **gdex-copy-trading** for tracking wallets and settings

**If you want to bridge assets cross-chain:**
1. Load **gdex-authentication** for auth setup
2. Load **gdex-bridge** for bridging operations

**If you want to build a trading frontend:**
1. Load **gdex-ui-install-setup** for React/Next.js project setup
2. Load **gdex-ui-trading-components** for order forms and position tables
3. Load **gdex-ui-theming** for dark/light mode and trading colors
4. Load **gdex-ui-page-layouts** for full page compositions

**If you're debugging an issue:**
1. Load **gdex-sdk-debugging** for error codes, chain quirks, and common pitfalls

## Key Links

| Resource | URL |
|----------|-----|
| SDK (npm) | https://www.npmjs.com/package/@gdexsdk/gdex-skill |
| Repository | https://github.com/GemachDAO/gdex-skill |
| Trading Dashboard | https://gdex.pro |
| Backend API | https://trade-api.gemach.io/v1 |

## Installation

```bash
# Install all skills globally (recommended)
npx skills add GemachDAO/gdex-skill --all --agent '*' -g

# Install specific skill
npx skills add GemachDAO/gdex-skill --skill gdex-spot-trading

# Install SDK
npm install @gdexsdk/gdex-skill
```

## MCP Server

For AI clients that support [Model Context Protocol](https://modelcontextprotocol.io), the GDEX MCP server exposes 8 tools for searching docs, getting code patterns, and exploring workflows:

```bash
npx @gdexsdk/mcp-server init --client claude   # Claude Code
npx @gdexsdk/mcp-server init --client cursor   # Cursor
npx @gdexsdk/mcp-server init --client vscode   # VS Code Copilot
npx @gdexsdk/mcp-server init --client codex    # Codex
npx @gdexsdk/mcp-server init --client opencode  # OpenCode
```

Tools: `search_gdex_docs`, `get_sdk_pattern`, `get_api_info`, `explain_workflow`, `get_chain_info`, `get_trading_guide`, `get_copy_trade_guide`, `get_component_guide`.

## Autonomous Agent Quickstart

If you're an AI agent operating autonomously (no human to ask), here's the minimum viable flow:

### 1. Initialize
```typescript
import { GdexSkill, GDEX_API_KEY_PRIMARY } from '@gdexsdk/gdex-skill';
const skill = new GdexSkill();
skill.loginWithApiKey(GDEX_API_KEY_PRIMARY);
```

### 2. Research Before Trading
```typescript
// Check what's trending
const trending = await skill.getTrendingTokens({ chain: 622112261, period: '1h', limit: 10 });

// Get details on a token — CHECK dexId BEFORE buying
const token = await skill.getTokenDetails({ tokenAddress: trending[0].address, chain: 622112261 });
if (token.dexId === 'meteora') {
  // ❌ Meteora tokens FAIL on Solana — skip this token
}
if (token.dexId === 'raydium') {
  // ✅ Safe to buy
}
```

### 3. Full Managed-Custody Setup (for actual trading)
```typescript
import { ethers } from 'ethers';
import {
  generateGdexSessionKeyPair, buildGdexSignInMessage,
  buildGdexSignInComputedData, buildGdexUserSessionData,
} from '@gdexsdk/gdex-skill';

const wallet = ethers.Wallet.fromPhrase('your mnemonic...');
const { sessionPrivateKey, sessionKey } = generateGdexSessionKeyPair();
const nonce = String(Date.now());
const msg = buildGdexSignInMessage(wallet.address, nonce, sessionKey);
const sig = await wallet.signMessage(msg);
const payload = buildGdexSignInComputedData({
  apiKey: GDEX_API_KEY_PRIMARY, userId: wallet.address, sessionKey, nonce, signature: sig,
});
await skill.signInWithComputedData({ computedData: payload.computedData, chainId: 1 });
```

### 4. Key Rules for Autonomous Operation
- **Always use control wallet address** (the one that signed in) for `userId`/`walletAddress` in API calls
- **Never use managed wallet address** in API calls (except `getHlUserStats()`)
- **Amounts in raw units** for managed trades (lamports for Solana, wei for EVM)
- **Check `dexId`** before buying on Solana — skip Meteora tokens
- **Generate fresh nonce** for every operation
- **Portfolio/balances use raw client** — high-level methods send wrong params
- **If `hlCloseAll` fails**, use reduce-only order instead

## Related Skills

- **gdex-authentication** — Managed-custody auth flow and encryption details
- **gdex-spot-trading** — Buy/sell tokens on any chain
- **gdex-perp-trading** — HyperLiquid perpetual futures
- **gdex-token-discovery** — Token info without authentication
- **gdex-wallet-setup** — Wallet generation for new users
- **gdex-ui-install-setup** — Frontend project setup with React/Next.js
- **gdex-sdk-debugging** — Error troubleshooting and debugging guide
