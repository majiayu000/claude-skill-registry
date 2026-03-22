---
name: hyperliquid
description: >
  Hyperliquid L1 reference for Dwellir endpoints: HyperEVM JSON-RPC, Info API proxy,
  gRPC L1 streaming, order book WebSocket, dedicated nodes, and trading patterns.
  Covers HyperCore trading layer, HyperEVM smart contracts (chain ID 999),
  market data queries, perpetuals metadata, spot markets, and best practices.
  Use when working with Hyperliquid, HYPE, HyperEVM, HyperCore,
  perpetual futures, order books, funding rates, or Hyperliquid trading through Dwellir.
  Triggers on mentions of hyperliquid, HYPE, HyperEVM, HyperCore,
  order book, perpetuals, funding rate, l2Book, l4Book, gRPC streaming,
  nanoreth, or hyperliquid trading.
---

# Hyperliquid via Dwellir

Hyperliquid is a purpose-built L1 blockchain optimized for trading. Dwellir runs its own Hyperliquid nodes and offers infrastructure beyond standard RPC: a custom gRPC gateway for Hypercore data, a real-time order book server, and a filtering Info API proxy, with edge servers in Singapore and Tokyo.

## How Hyperliquid Works

Hyperliquid has two layers:

**HyperCore** is the native trading layer. Fully on-chain perpetual futures and spot order books. Every order, cancellation, trade, and liquidation settles within one block. Handles ~200,000 orders/second with sub-second finality via HyperBFT consensus.

**HyperEVM** is a general-purpose EVM smart contract layer that runs alongside HyperCore. Developers can deploy Solidity contracts that interact with HyperCore's liquidity. Chain ID: **999**. Native gas token: **HYPE**.

Key properties:
- All order books are fully on-chain (no off-chain matching)
- Sub-second block times with one-block finality
- Perpetuals support up to 40x leverage (BTC); most assets 3-10x
- Native spot trading with HIP-3 DEX deployment

## What Dwellir Provides

Dwellir runs full Hyperliquid infrastructure: the official HL node, plus custom software built by Dwellir and the community for serving specific data channels.

For current pricing, features, and service details, see [Dwellir Hyperliquid docs](https://www.dwellir.com/docs/hyperliquid) and [Pricing](https://www.dwellir.com/docs/hyperliquid/pricing).

| Endpoint | What It Serves | Protocol | Reference |
|----------|---------------|----------|-----------|
| **HyperEVM JSON-RPC** | EVM state, smart contracts, blocks | HTTPS + WSS | [hyperevm-json-rpc.md](references/hyperevm-json-rpc.md) |
| **Info API proxy** | Market data, user state, metadata | HTTPS (POST) | [info-api.md](references/info-api.md) |
| **L1 gRPC Gateway** | Hypercore block/fill/orderbook streaming | gRPC | [grpc-gateway.md](references/grpc-gateway.md) |
| **Orderbook WebSocket** | Real-time L2/L4 order book data | WSS only | [orderbook-websocket.md](references/orderbook-websocket.md) |
| **Dedicated Node** | Full stack, uncapped throughput | All | See below |

### Dwellir CLI

The [Dwellir CLI](https://www.dwellir.com/docs/cli) (`dwellir`) provides terminal access to endpoint discovery, API key management, usage monitoring, and documentation. Useful for quickly finding Hyperliquid endpoint URLs, reading docs without leaving the terminal, and managing keys in CI pipelines. See [dwellir-cli.md](references/dwellir-cli.md).

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/dwellir-public/cli/main/scripts/install.sh | sh

# Find all Hyperliquid endpoints
dwellir endpoints search hyperliquid

# Read Hyperliquid docs as markdown
dwellir docs search hyperliquid
dwellir docs get hyperliquid/info-endpoint

# Manage API keys and check usage
dwellir keys list
dwellir usage summary
```

### What Dwellir Does NOT Proxy

**Exchange API**: Order placement, cancellation, transfers, and other write operations require EIP-712 signatures and go directly to `api.hyperliquid.xyz/exchange`. See [native-api.md](references/native-api.md).

**Native WebSocket**: Hyperliquid's subscription WebSocket (`wss://api.hyperliquid.xyz/ws`) for user events, trades, and candles is separate from Dwellir's Orderbook WebSocket. See [native-api.md](references/native-api.md).

### Read vs Write Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Your Application                                        │
├──────────────────┬──────────────────────────────────────┤
│  READ (Dwellir)  │  WRITE (Hyperliquid native)          │
│                  │                                       │
│  EVM state ──────┤  Place orders ─── api.hyperliquid.xyz │
│  Info queries ───┤  Cancel orders    /exchange           │
│  gRPC streams ───┤  Transfers        (requires sig)      │
│  Order book ─────┤  Set leverage                         │
└──────────────────┴──────────────────────────────────────┘
```

## When to Use Which Reference

| You want to... | Use this reference |
|----------------|-------------------|
| Deploy or interact with Solidity contracts on HyperEVM | [hyperevm-json-rpc.md](references/hyperevm-json-rpc.md) |
| Query EVM state (balances, logs, blocks) | [hyperevm-json-rpc.md](references/hyperevm-json-rpc.md) |
| Get market data (prices, order books, candles, funding rates) | [info-api.md](references/info-api.md) |
| Query user positions, orders, fills, or balances | [info-api.md](references/info-api.md) |
| Get perpetuals/spot metadata (universe, leverage, assets) | [info-api.md](references/info-api.md) |
| Stream real-time order book updates with deep levels | [orderbook-websocket.md](references/orderbook-websocket.md) |
| Build market-making or arbitrage systems | [orderbook-websocket.md](references/orderbook-websocket.md) |
| Stream L1 block data or fill executions | [grpc-gateway.md](references/grpc-gateway.md) |
| Build indexers or data pipelines from Hypercore | [grpc-gateway.md](references/grpc-gateway.md) |
| Place, cancel, or modify orders | [native-api.md](references/native-api.md) |
| Subscribe to user events, trades, or candle updates | [native-api.md](references/native-api.md) |
| Access historical trade/fill data | [historical-data.md](references/historical-data.md) |
| Discover endpoint URLs, manage API keys, or read docs from the terminal | [dwellir-cli.md](references/dwellir-cli.md) |

## Dedicated Nodes

Full Hyperliquid stack on single-tenant infrastructure. No shared rate limits, uncapped throughput. Available in Tokyo (mainnet) and testnet configurations.

A dedicated node includes all Dwellir services (EVM JSON-RPC, Info API, gRPC Gateway, Orderbook Server) on isolated infrastructure.

For current pricing and configuration options, see [Dwellir Hyperliquid Pricing](https://www.dwellir.com/docs/hyperliquid/pricing).

Contact sales or subscribe via [dashboard.dwellir.com](https://dashboard.dwellir.com).

## Best Practices

1. **Use Dwellir for reads, Hyperliquid native for writes.** Dwellir provides the data infrastructure; order placement requires signatures and goes through `api.hyperliquid.xyz/exchange`.

2. **Use the gRPC gateway for latency-sensitive streaming.** The gRPC endpoint reads from disk and has lower latency than HTTP polling the Info API.

3. **Use Dwellir's Orderbook WebSocket for book data.** It's optimized for order book delivery with edge servers in Singapore and Tokyo.

4. **Batch Info API queries.** Fetch combined endpoints like `metaAndAssetCtxs` (via public API) rather than per-asset queries. Check [Info API docs](https://www.dwellir.com/docs/hyperliquid/info-endpoint) for which types are available on the Dwellir proxy vs public endpoint.

5. **Cache metadata.** `meta`, `spotMeta`, and `perpDexs` are semi-static. Cache for 1-5 minutes.

6. **Use `l2Book` via Info API for snapshots, Orderbook WS for streaming.** The Info API gives point-in-time snapshots; the Orderbook WebSocket gives continuous updates.

## Documentation Links

- Dwellir Hyperliquid docs: [dwellir.com/docs/hyperliquid](https://www.dwellir.com/docs/hyperliquid)
- Dwellir L1 gRPC Gateway: contact support@dwellir.com for source access
- Dwellir Orderbook Server: contact support@dwellir.com for source access
- Dwellir REST Server: contact support@dwellir.com for source access
- Hyperliquid API docs: [hyperliquid.gitbook.io](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api)
- Hyperliquid Python SDK: [github.com/hyperliquid-dex/hyperliquid-python-sdk](https://github.com/hyperliquid-dex/hyperliquid-python-sdk)
- Dwellir dashboard: [dashboard.dwellir.com](https://dashboard.dwellir.com)
- Dwellir support: support@dwellir.com
