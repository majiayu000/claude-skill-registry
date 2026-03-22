---
name: binance-token-info
description: Binance Web3 official skill — search tokens, retrieve metadata, real-time market data, and candlestick charts across BSC, Base, and Solana. Sourced from github.com/binance/binance-skills-hub.
metadata: { "cryptoclaw": { "emoji": "🔍", "always": false } }
---

# Binance Token Info

Official Binance Web3 skill for querying token details, market data, and price charts.

> Source: [binance/binance-skills-hub](https://github.com/binance/binance-skills-hub/tree/main/skills/binance-web3/query-token-info)

## Supported Chains

| Chain  | chainId | K-Line platform |
| ------ | ------- | --------------- |
| BSC    | 56      | bsc             |
| Base   | 8453    | base            |
| Solana | CT_501  | solana          |

## API 1 — Token Search

Search tokens by name, symbol, or contract address.

```
GET https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/token/search
  ?keyword=<name|symbol|address>
  &chainId=<chainId>          # optional, omit for all chains
  &sortBy=volume              # optional
  &page=1
  &pageSize=20
```

Response: token list with name, symbol, contract address, chain, price, volume.

## API 2 — Token Metadata

Static token information.

```
GET https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/token/metadata
  ?contractAddress=<address>
  &chainId=<chainId>
```

Response includes:

- Name, symbol, logo URL
- Social links (website, Twitter, Telegram)
- Creator address
- Audit status
- Project description

## API 3 — Token Dynamic Data

Real-time market metrics.

```
GET https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/token/dynamic
  ?contractAddress=<address>
  &chainId=<chainId>
```

Response includes:

- Current price (USD)
- 24h / 6h / 1h volume
- Market cap, fully diluted valuation
- Liquidity
- Holder count and distribution
- Transaction counts (buys/sells)
- Price change percentages across timeframes

## API 4 — K-Line Candlestick Data

OHLCV price chart data.

```
GET https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/token/kline
  ?contractAddress=<address>
  &platform=<bsc|solana|base|eth>
  &interval=<interval>
  &limit=<count>
  &from=<timestamp_ms>        # optional, limit takes precedence
```

Supported intervals: `1s`, `1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `1d`, `1w`, `1M`

Response is a 2D array per candle:

```
[open, high, low, close, volume, timestamp_ms, transaction_count]
```

## Notes

- All numeric values are returned as strings — convert before calculations
- Logo URLs require prefix: `https://bin.bnbstatic.com`
- `limit` parameter takes precedence over `from` in K-Line requests

## Usage Examples

```
User: Find the token PEPE on BSC
→ GET Token Search, keyword:PEPE, chainId:56

User: What is the current price and market cap of <contract>?
→ GET Token Dynamic Data

User: Show me the 4h chart for <contract> on Solana
→ GET K-Line, platform:solana, interval:4h, limit:100

User: Who created this token and does it have social links?
→ GET Token Metadata
```
