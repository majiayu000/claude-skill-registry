---
name: goldrush-api
description: "Query blockchain data across 100+ chains: wallet balances, token prices, transactions, DEX pairs, and real-time OHLCV streams via the GoldRush API by Covalent."
category: blockchain
risk: safe
source: community
date_added: "2026-03-17"
author: covalenthq
tags: [blockchain, crypto, web3, api, defi, wallet, multi-chain]
tools: [claude, cursor, gemini, codex, copilot]
---

# GoldRush API

## Overview
GoldRush by Covalent provides blockchain data across 100+ chains through a unified REST API, real-time WebSocket streams, a CLI, and an x402 pay-per-request proxy. This skill enables AI agents to query wallet balances, token prices, transaction history, NFT holdings, and DEX pair data without building chain-specific integrations.

## When to Use This Skill
- Retrieving wallet token balances or total portfolio value across any chain
- Fetching transaction history or decoded event logs for an address
- Getting current or historical token prices (USD or native)
- Monitoring DEX pairs, liquidity events, and real-time OHLCV candles via WebSocket
- Building block explorers, portfolio dashboards, tax tools, or DeFi analytics
- Accessing on-chain data with no signup via x402 pay-per-request

## How It Works

### Step 1: Get credentials
Sign up at https://goldrush.dev for a free API key. For agent-native no-signup access, use the x402 proxy instead.

### Step 2: Set your API key
```bash
export GOLDRUSH_API_KEY="your_api_key_here"
```

### Step 3: Query data

**REST API (most endpoints):**
```bash
# Wallet token balances on Ethereum
curl -H "Authorization: Bearer $GOLDRUSH_API_KEY"   "https://api.covalenthq.com/v1/eth-mainnet/address/0xADDRESS/balances_v2/"
```

**CLI (quick terminal queries):**
```bash
npx @covalenthq/goldrush-cli balances --chain eth-mainnet --address 0xADDRESS
```

**SDK (in code):**
```javascript
import GoldRushClient from "@covalenthq/client-sdk";
const client = new GoldRushClient(process.env.GOLDRUSH_API_KEY);
const resp = await client.BalanceService.getTokenBalancesForWalletAddress(
  "eth-mainnet", "0xADDRESS"
);
```

## Examples

### Example 1: Token Balances
```bash
curl -H "Authorization: Bearer $GOLDRUSH_API_KEY"   "https://api.covalenthq.com/v1/eth-mainnet/address/0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045/balances_v2/"
```

### Example 2: Token Price History
```bash
curl -H "Authorization: Bearer $GOLDRUSH_API_KEY"   "https://api.covalenthq.com/v1/pricing/historical_by_addresses_v2/eth-mainnet/USD/0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48/"
```

### Example 3: Transaction History
```bash
curl -H "Authorization: Bearer $GOLDRUSH_API_KEY"   "https://api.covalenthq.com/v1/eth-mainnet/address/0xADDRESS/transactions_v3/"
```

### Example 4: Real-time OHLCV via WebSocket
```javascript
// Stream live price candles for a token pair
const ws = new WebSocket("wss://streaming.covalenthq.com/v1/eth-mainnet/ohlcv");
ws.on("message", (data) => console.log(JSON.parse(data)));
```

## Best Practices
✅ Use chain slugs: `eth-mainnet`, `matic-mainnet`, `base-mainnet`, `bsc-mainnet` — full list at https://goldrush.dev/docs/networks
✅ Store API key in `GOLDRUSH_API_KEY` env var — never hardcode
✅ Use WebSocket streams for real-time data rather than polling REST
✅ Use SDK cursor pagination for large result sets
❌ Don't use x402 for high-volume use cases — get a standard API key instead
❌ Don't use chain IDs (e.g., `1`) — use chain slugs (e.g., `eth-mainnet`)

## Security & Safety Notes
- API key in `GOLDRUSH_API_KEY` environment variable only
- x402 payments use USDC on Base — set spending limits before autonomous agent use
- Read-only data API — no write operations, no transaction signing

## Common Pitfalls

**Problem:** 401 Unauthorized  
**Solution:** Ensure API key is in `Authorization: Bearer` header, not query string

**Problem:** `chain_name not found`  
**Solution:** Use chain slug format — see https://goldrush.dev/docs/networks

**Problem:** Empty results for new wallet  
**Solution:** Some endpoints require on-chain activity; new wallets with no transactions return empty arrays, not errors

## Related Skills
- @goldrush-streaming-api — real-time WebSocket DEX pair and OHLCV streams
- @goldrush-x402 — pay-per-request blockchain data without API key
- @goldrush-cli — terminal-first blockchain data queries
