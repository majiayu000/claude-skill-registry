---
name: gate-dex-market
version: "2026.3.6-1"
updated: "2026-03-06"
description: "Gate Wallet market data and token info queries. K-line,
  transaction stats, liquidity, token details, rankings, security audit,
  new token discovery. Use when users ask about market data, prices, or
  token info. All queries require no authentication. Not for executing trades."
---

# Gate Wallet Market Skill

> Market / Token domain — K-line, transaction stats, liquidity, token details, rankings, security audit, new token discovery. 7 MCP tools, all require no authentication.

**Trigger scenarios**: User mentions "market", "K-line", "kline", "price", "token info", "ranking", "security", "audit", "risk", "chart", "new token", "liquidity", or when market data / security audit assistance is needed.

## Step 0: MCP Server Connection Check (Mandatory)

**Before executing any operation, the Gate Wallet MCP Server must be confirmed available. This step cannot be skipped.**

Connectivity probe:

```
CallMcpTool(server="gate-dex-mcp", toolName="chain.config", arguments={chain: "eth"})
```

| Result | Action |
|--------|--------|
| Success | MCP Server is available, proceed to next steps |
| `server not found` / `unknown server` | Cursor not configured → show config guide (see below) |
| `connection refused` / `timeout` | Unreachable → prompt to check URL and network |

### When Cursor Is Not Configured

```
❌ Gate Wallet MCP Server Not Configured

No MCP Server named "gate-dex-mcp" found in Cursor. Follow these steps to configure:

Option 1: Via Cursor Settings (recommended)
  1. Open Cursor → Settings → MCP
  2. Click "Add new MCP server"
  3. Fill in:
     - Name: gate-dex-mcp
     - Type: HTTP
     - URL: https://api.gatemcp.ai/mcp
  4. Save and retry

Option 2: Manually edit config file
  Edit ~/.cursor/mcp.json, add:
  {
    "mcpServers": {
      "gate-dex-mcp": {
        "url": "https://api.gatemcp.ai/mcp"
      }
    }
  }

If you don't have an MCP Server URL yet, contact your administrator.
```

### When Remote Service Is Unreachable

```
⚠️  Gate Wallet MCP Server Connection Failed

MCP Server configuration found, but unable to connect to the remote service. Please check:
1. Verify the service URL is correct (is the configured URL accessible?)
2. Check network connection (VPN / firewall interference?)
3. Confirm the remote service is running
```

### When API Key Authentication Fails

```
🔑 Gate Wallet MCP Server Authentication Failed

MCP Server connected but API Key validation failed. The service has AK/SK authentication enabled (x-api-key header).
Contact your administrator to obtain a valid API Key and verify the server-side configuration.
```

## Authentication

All tools in this Skill **require no authentication** — they are all public market data queries with no `mcp_token` needed.

## MCP Tool Specifications

### 1. `market_get_kline` — Get K-Line Data

Retrieve candlestick (K-line) data for a specified token over a given time interval.

| Field | Description |
|-------|-------------|
| **Tool name** | `market_get_kline` |
| **Parameters** | `{ chain: string, token_address: string, interval?: string, limit?: number }` |
| **Returns** | Array of K-line data, each containing `timestamp`, `open`, `high`, `low`, `close`, `volume` |

Parameters:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain identifier (e.g. `"eth"`, `"bsc"`) |
| `token_address` | Yes | Token contract address. Use `"native"` for native tokens |
| `interval` | No | K-line interval (e.g. `"1m"`, `"5m"`, `"1h"`, `"4h"`, `"1d"`). Default `"1h"` |
| `limit` | No | Number of records to return. Default 100 |

Call example:

```
CallMcpTool(
  server="gate-dex-mcp",
  toolName="market_get_kline",
  arguments={
    chain: "eth",
    token_address: "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    interval: "1h",
    limit: 24
  }
)
```

Response example:

```json
[
  {
    "timestamp": 1700000000,
    "open": "1.0001",
    "high": "1.0005",
    "low": "0.9998",
    "close": "1.0002",
    "volume": "15000000"
  }
]
```

Agent behavior: Present K-line trends as text tables or summaries (high/low prices, price change, volume changes, etc.).

---

### 2. `market_get_tx_stats` — Get Transaction Statistics

Retrieve on-chain transaction statistics for a specified token (buy/sell counts, volumes, etc.).

| Field | Description |
|-------|-------------|
| **Tool name** | `market_get_tx_stats` |
| **Parameters** | `{ chain: string, token_address: string, period?: string }` |
| **Returns** | `{ buy_count: number, sell_count: number, buy_volume: string, sell_volume: string, unique_buyers: number, unique_sellers: number }` |

Parameters:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain identifier |
| `token_address` | Yes | Token contract address |
| `period` | No | Statistics period (e.g. `"24h"`, `"7d"`, `"30d"`). Default `"24h"` |

Call example:

```
CallMcpTool(
  server="gate-dex-mcp",
  toolName="market_get_tx_stats",
  arguments={
    chain: "eth",
    token_address: "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    period: "24h"
  }
)
```

Response example:

```json
{
  "buy_count": 12500,
  "sell_count": 11800,
  "buy_volume": "45000000",
  "sell_volume": "42000000",
  "unique_buyers": 3200,
  "unique_sellers": 2900
}
```

---

### 3. `market_get_pair_liquidity` — Get Trading Pair Liquidity

Retrieve liquidity pool information for a specified token's trading pairs.

| Field | Description |
|-------|-------------|
| **Tool name** | `market_get_pair_liquidity` |
| **Parameters** | `{ chain: string, token_address: string }` |
| **Returns** | `{ total_liquidity_usd: string, pairs: [{ dex: string, pair: string, liquidity_usd: string, volume_24h: string }] }` |

Parameters:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain identifier |
| `token_address` | Yes | Token contract address |

Call example:

```
CallMcpTool(
  server="gate-dex-mcp",
  toolName="market_get_pair_liquidity",
  arguments={
    chain: "eth",
    token_address: "0xdAC17F958D2ee523a2206206994597C13D831ec7"
  }
)
```

Response example:

```json
{
  "total_liquidity_usd": "250000000",
  "pairs": [
    {
      "dex": "Uniswap V3",
      "pair": "USDT/ETH",
      "liquidity_usd": "120000000",
      "volume_24h": "35000000"
    },
    {
      "dex": "Uniswap V3",
      "pair": "USDT/USDC",
      "liquidity_usd": "80000000",
      "volume_24h": "22000000"
    }
  ]
}
```

---

### 4. `token_get_coin_info` — Get Token Details

Retrieve detailed information for a specified token (name, symbol, market cap, holders, etc.).

| Field | Description |
|-------|-------------|
| **Tool name** | `token_get_coin_info` |
| **Parameters** | `{ chain: string, token_address: string }` |
| **Returns** | `{ name: string, symbol: string, decimals: number, total_supply: string, market_cap: string, holders: number, price: string, price_change_24h: string, website: string, socials: object }` |

Parameters:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain identifier |
| `token_address` | Yes | Token contract address |

Call example:

```
CallMcpTool(
  server="gate-dex-mcp",
  toolName="token_get_coin_info",
  arguments={
    chain: "eth",
    token_address: "0xdAC17F958D2ee523a2206206994597C13D831ec7"
  }
)
```

Response example:

```json
{
  "name": "Tether USD",
  "symbol": "USDT",
  "decimals": 6,
  "total_supply": "40000000000",
  "market_cap": "40000000000",
  "holders": 5200000,
  "price": "1.0001",
  "price_change_24h": "0.01",
  "website": "https://tether.to",
  "socials": { "twitter": "@Tether_to" }
}
```

---

### 5. `token_ranking` — Token Rankings

Retrieve on-chain token rankings (by market cap, price change, volume, etc.).

| Field | Description |
|-------|-------------|
| **Tool name** | `token_ranking` |
| **Parameters** | `{ chain: string, sort_by?: string, order?: string, limit?: number }` |
| **Returns** | Array of ranked tokens, each containing `rank`, `name`, `symbol`, `price`, `market_cap`, `change_24h`, `volume_24h` |

Parameters:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain identifier |
| `sort_by` | No | Sort dimension: `"market_cap"`, `"volume_24h"`, `"change_24h"`, `"holders"`. Default `"market_cap"` |
| `order` | No | Sort direction: `"desc"` (descending), `"asc"` (ascending). Default `"desc"` |
| `limit` | No | Number of records to return. Default 20 |

Call example:

```
CallMcpTool(
  server="gate-dex-mcp",
  toolName="token_ranking",
  arguments={
    chain: "eth",
    sort_by: "volume_24h",
    order: "desc",
    limit: 10
  }
)
```

Response example:

```json
[
  {
    "rank": 1,
    "name": "Tether USD",
    "symbol": "USDT",
    "price": "1.0001",
    "market_cap": "40000000000",
    "change_24h": "0.01",
    "volume_24h": "5000000000"
  }
]
```

---

### 6. `token_get_coins_range_by_created_at` — New Token Discovery

Retrieve newly listed tokens within a specified creation time range.

| Field | Description |
|-------|-------------|
| **Tool name** | `token_get_coins_range_by_created_at` |
| **Parameters** | `{ chain: string, start_time?: number, end_time?: number, limit?: number }` |
| **Returns** | Array of tokens, each containing `name`, `symbol`, `token_address`, `created_at`, `price`, `market_cap`, `holders` |

Parameters:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain identifier |
| `start_time` | No | Start timestamp (seconds). Default 24 hours ago |
| `end_time` | No | End timestamp (seconds). Default current time |
| `limit` | No | Number of records to return. Default 20 |

Call example:

```
CallMcpTool(
  server="gate-dex-mcp",
  toolName="token_get_coins_range_by_created_at",
  arguments={
    chain: "eth",
    limit: 10
  }
)
```

---

### 7. `token_get_risk_info` — Token / Contract Security Audit

Retrieve security risk assessment for a token or contract, including audit status and risk tags.

| Field | Description |
|-------|-------------|
| **Tool name** | `token_get_risk_info` |
| **Parameters** | `{ chain: string, address: string }` |
| **Returns** | `{ risk_level: string, is_audited: boolean, risk_items: [{ type: string, description: string, severity: string }], contract_verified: boolean, owner_renounced: boolean }` |

Parameters:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain identifier |
| `address` | Yes | Token contract address or any contract address |

Call example:

```
CallMcpTool(
  server="gate-dex-mcp",
  toolName="token_get_risk_info",
  arguments={
    chain: "eth",
    address: "0xdAC17F958D2ee523a2206206994597C13D831ec7"
  }
)
```

Response example:

```json
{
  "risk_level": "low",
  "is_audited": true,
  "risk_items": [],
  "contract_verified": true,
  "owner_renounced": false
}
```

`risk_level` values:

| risk_level | Meaning | Agent Behavior |
|------------|---------|----------------|
| `low` | Low risk | Proceed normally |
| `medium` | Medium risk | Alert user, list risk items |
| `high` | High risk | Strong warning, advise against interaction. If user insists, show security warning confirmation |
| `unknown` | No audit data | Inform that no security info was found, advise user to investigate independently |

Agent behavior: This tool is used for pre-trade contract security audits, helping users assess token risk.

## Skill Routing

After viewing market data, guide subsequent actions based on user intent:

| User Intent | Suggested Action |
|-------------|-----------------|
| View other token market data | Continue using this Skill's `market_get_kline` and other tools |
| View token security info | Use `token_get_risk_info` |
| View more token rankings | Use `token_ranking` |
| View token details | Use `token_get_coin_info` |

## Workflows

> All workflows below require passing the Step 0 MCP Server connection check first. If the check fails, abort — this will not be repeated.

### Flow A: View Token Market Data (K-Line + Stats)

```
Step 1: Intent recognition + parameter collection
  Extract query intent from user input:
  - Token name/symbol or contract address
  - Chain (optional, can infer from context)
  - K-line interval (optional, default 1h)
  - Stats period (optional, default 24h)

  If user provides token symbol without contract address:
  - First call token_get_coin_info or infer from context
  ↓

Step 2: Fetch market data
  Parallel calls (when applicable):
  - market_get_kline({ chain, token_address, interval, limit })
  - market_get_tx_stats({ chain, token_address, period })
  - market_get_pair_liquidity({ chain, token_address })
  ↓

Step 3: Format and display

  ────────────────────────────
  📈 {token_name} ({symbol}) Market Data

  Current Price: ${price}
  24h Change: {change_24h}%
  24h High: ${high_24h}
  24h Low: ${low_24h}

  ── Transaction Stats (24h) ──
  Buys: {buy_count} txns / ${buy_volume}
  Sells: {sell_count} txns / ${sell_volume}
  Unique Buyers: {unique_buyers}
  Unique Sellers: {unique_sellers}

  ── Liquidity ──
  Total Liquidity: ${total_liquidity_usd}
  Main Pairs:
  | DEX | Pair | Liquidity | 24h Volume |
  |-----|------|-----------|------------|
  | {dex} | {pair} | ${liquidity} | ${volume} |
  ────────────────────────────

  ↓

Step 4: Suggest next actions
  - View security info → token_get_risk_info
  - View more tokens → token_ranking
  - View token details → token_get_coin_info
```

### Flow B: View Token Details

```
Step 1: Execute query
  Call token_get_coin_info({ chain, token_address })
  ↓

Step 2: Format and display

  ────────────────────────────
  🪙 Token Details

  Name: {name} ({symbol})
  Contract: {token_address}
  Chain: {chain_name}
  Decimals: {decimals}
  Total Supply: {total_supply}
  Market Cap: ${market_cap}
  Holders: {holders}
  Current Price: ${price}
  24h Change: {price_change_24h}%
  Website: {website}
  ────────────────────────────

  ↓

Step 3: Suggest next actions
  - View K-line data → market_get_kline
  - View security audit → token_get_risk_info
  - View token rankings → token_ranking
```

### Flow C: Token Rankings

```
Step 1: Collect parameters
  Determine ranking dimension (market cap / volume / price change), chain, count
  ↓

Step 2: Execute query
  Call token_ranking({ chain, sort_by, order, limit })
  ↓

Step 3: Format and display

  ────────────────────────────
  🏆 {chain_name} Token Rankings (by {sort_by})

  | # | Token | Price | 24h Change | Market Cap | 24h Volume |
  |---|-------|-------|------------|------------|------------|
  | 1 | {symbol} | ${price} | {change}% | ${mcap} | ${vol} |
  | 2 | ... | ... | ... | ... | ... |
  ────────────────────────────
```

### Flow D: Security Audit

```
Step 1: Execute query
  Call token_get_risk_info({ chain, address })
  ↓

Step 2: Format and display

  When risk_level == "low":

  ────────────────────────────
  🛡️ Security Audit Results

  Contract: {address}
  Chain: {chain_name}
  Risk Level: Low ✅
  Contract Verified: Yes
  Audited: Yes
  Owner Renounced: {Yes/No}
  Risk Items: None
  ────────────────────────────

  When risk_level == "high":

  ────────────────────────────
  ⚠️ Security Audit Results

  Contract: {address}
  Chain: {chain_name}
  Risk Level: High ⚠️
  Contract Verified: {Yes/No}
  Audited: {Yes/No}

  Risk Items:
  - [{severity}] {description}
  - [{severity}] {description}

  Warning: Exercise caution when interacting with this contract — risk of asset loss.
  ────────────────────────────
```

### Flow E: New Token Discovery

```
Step 1: Collect parameters
  Determine chain and time range
  ↓

Step 2: Execute query
  Call token_get_coins_range_by_created_at({ chain, start_time?, end_time?, limit })
  ↓

Step 3: Format and display

  ────────────────────────────
  🆕 {chain_name} Newly Listed Tokens

  | Token | Contract | Created At | Price | Market Cap | Holders |
  |-------|----------|------------|-------|------------|---------|
  | {symbol} | {addr_short} | {time} | ${price} | ${mcap} | {holders} |

  Note: New tokens carry higher risk. Check the security audit before making any trading decisions.
  ────────────────────────────

  ↓

Step 4: Suggest next actions
  - View a token's security info → token_get_risk_info
  - View a token's details → token_get_coin_info
```

## Typical Workflow

### Query → Audit Workflow

```
token_get_coin_info (query token info)
  → token_get_risk_info (security audit)
    → market_get_kline + market_get_tx_stats (market analysis)
```

## Display Standards

### Price Display Rules

- **Greater than $1**: 2 decimal places (e.g. `$1,920.50`)
- **$0.01 ~ $1**: 4 decimal places (e.g. `$0.0521`)
- **Less than $0.01**: 6–8 significant digits (e.g. `$0.00000142`)
- **Percentages**: 2 decimal places (e.g. `+2.15%`, `-0.32%`)
- **Large values**: Thousand separators; very large values use abbreviations (e.g. `$1.2B`, `$350M`)

### Address Display Rules

- Show full contract address with chain info when displaying completely
- Use truncated format for brief references: `0xdAC1...1ec7`
- Provide block explorer links for user verification

### Time Display Rules

- Use the user's local timezone
- Format: `YYYY-MM-DD HH:mm:ss`
- Relative time: within 24h, use "X minutes ago", "X hours ago"

## Edge Cases and Error Handling

| Scenario | Handling |
|----------|---------|
| MCP Server not configured | Abort all operations, show Cursor config guide |
| MCP Server unreachable | Abort all operations, show network check prompt |
| Invalid token contract address | Prompt address format error, ask user to confirm |
| Token not found on specified chain | Inform token not found, suggest verifying chain and address |
| `market_get_kline` returns empty data | Inform no K-line data available — may be a new or very low volume token |
| `token_get_risk_info` returns `unknown` | Inform no security audit info found, advise user to investigate independently |
| `token_ranking` returns empty list | Inform no ranking data available for this chain |
| Query timeout | Suggest network issue, recommend retrying later |
| MCP Server returns unknown error | Display the error message as-is |
| User provides token symbol instead of address | First attempt to resolve via `token_get_coin_info` or context |
| Unsupported chain identifier | Display the list of supported chains |

## Security Rules

1. **Read-only operations**: This Skill only involves public data queries — no on-chain writes, no authentication needed, no transaction confirmation gates.
2. **Objective security audit display**: Present `token_get_risk_info` results as-is without subjective commentary. Clearly flag high risk but do not make decisions for the user.
3. **New token risk warnings**: Append risk reminders when displaying new token lists — new tokens generally carry higher risk.
4. **No operations when MCP Server is unavailable**: If Step 0 check fails, abort all subsequent steps.
5. **Transparent MCP Server errors**: Display all MCP Server error messages to the user as-is — do not hide or alter them.
6. **No investment advice**: Market data is provided for reference only — the Agent must not make any recommendations or judgments on token investment value.
