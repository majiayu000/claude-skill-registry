---
name: renzo
description: Query Renzo crypto liquid restaking protocol — DeFi vault yields, TVL, ezETH exchange rates, EigenLayer operators, supported blockchain networks, user token balances, and withdrawal status.
homepage: https://github.com/Renzo-Protocol/openclaw-skill
metadata:
  clawdbot:
    emoji: "\U0001F7E2"
    requires:
      bins: ["curl", "jq"]
    files: ["renzo-mcp.sh"]
---

# Renzo Protocol

Query live data from the Renzo liquid restaking protocol: ezETH metrics, vault information, protocol stats, supported chains, and operator details.

## When to Use

Activate this skill when the user asks about:
- Renzo protocol, ezETH, pzETH, ezSOL, or any Renzo vault token
- Liquid restaking yields, APRs, or staking returns on Renzo
- Renzo TVL (total value locked) or protocol statistics
- Renzo vault details, performance, or comparisons
- Chains or networks Renzo supports
- EigenLayer operators delegated through Renzo
- Institutional vault management on Renzo
- Their Renzo token balances or portfolio (given an Ethereum address)
- ezETH withdrawal requests, unstaking status, or cooldown timers
- Vault strategies, AVS allocations, or where vault capital is deployed
- LTV ratios, leverage, or risk parameters for reserve vaults (ezCompETH1, ezUSCC1)

## Available Tools

The helper script `renzo-mcp.sh` (located in this skill's directory) calls the Renzo MCP server and returns clean JSON.

| Tool | Purpose | Arguments |
|------|---------|-----------|
| `get_ezeth_info` | ezETH metrics: APR, supply, TVL, price, exchange rate | None |
| `get_protocol_stats` | Aggregate protocol stats: total TVL, APRs, chain count | None |
| `get_supported_chains` | List of blockchain networks Renzo operates on | None |
| `get_vaults` | List vaults with TVL and APR | Optional: `{"ecosystem":"eigenlayer"}` (eigenlayer, symbiotic, jito, generic) |
| `get_vault_details` | Detailed info for one vault, including live LTV for reserve vaults | Required: `{"vaultId":"<symbol_or_address>"}` |
| `get_vault_strategy` | AVS allocations, staking %, and operators for EigenLayer vaults | Required: `{"vaultId":"<symbol>"}` (ezETH, ezEIGEN, ezREZ) |
| `get_operators` | List protocol operators | Optional: `{"product":"ezETH"}` (ezETH, pzETH, ezSOL, etc.) |
| `get_token_balances` | User's Renzo token balances (ezETH, pzETH, vault LPs) with ETH/USD values | Required: `{"address":"0x..."}` (Ethereum address) |
| `get_withdrawal_requests` | User's pending ezETH withdrawal requests with claimability and time remaining | Required: `{"address":"0x..."}` (Ethereum address) |

## How to Call

Run the helper script via the Bash tool. The script path is relative to this skill's directory.

```bash
# No arguments
./skills/renzo/renzo-mcp.sh get_ezeth_info
./skills/renzo/renzo-mcp.sh get_protocol_stats
./skills/renzo/renzo-mcp.sh get_supported_chains

# With optional filter
./skills/renzo/renzo-mcp.sh get_vaults '{"ecosystem":"jito"}'
./skills/renzo/renzo-mcp.sh get_operators '{"product":"pzETH"}'

# With required argument
./skills/renzo/renzo-mcp.sh get_vault_details '{"vaultId":"ezREZ"}'
./skills/renzo/renzo-mcp.sh get_vault_details '{"vaultId":"ezCompETH1"}'
./skills/renzo/renzo-mcp.sh get_vault_strategy '{"vaultId":"ezETH"}'

# User-specific queries (require an Ethereum address)
./skills/renzo/renzo-mcp.sh get_token_balances '{"address":"0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"}'
./skills/renzo/renzo-mcp.sh get_withdrawal_requests '{"address":"0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"}'
```

## Presenting Results

Format data for readability. Follow these rules:

- **APR/APY**: Display as percentages with 2 decimal places (e.g., "2.84%")
- **TVL**: Format in USD with commas and 2 decimal places (e.g., "$430,813,580.01"). For values over $1M, also show shorthand (e.g., "$430.8M")
- **Exchange rates**: Show 4-6 decimal places (e.g., "1.0721 ETH per ezETH")
- **Token amounts**: Show 2-4 decimal places with the token symbol
- **Tables**: Use markdown tables when comparing vaults or listing multiple items
- **Context**: Briefly explain what the numbers mean for users unfamiliar with liquid restaking

### Example: ezETH Info Response

The `get_ezeth_info` tool returns:
```json
{
  "token": "ezETH",
  "aprPercent": 2.83,
  "aprAvgPeriodDays": 30,
  "totalSupplyEth": 215986.82,
  "lpTotalSupply": 201461.43,
  "tvlUsd": 430813580.00,
  "ethPriceUsd": 2138.44,
  "exchangeRate": 1.0721
}
```

Present this as:
> **ezETH** is currently earning **2.83% APR** (30-day average). The exchange rate is **1.0721 ETH per ezETH**, with a total TVL of **$430.8M**. Total supply is **215,987 ETH**.

### Example: Vault Comparison

When listing vaults, use a table:

| Vault | Underlying | APR | TVL | Ecosystem |
|-------|-----------|-----|-----|-----------|
| ezSOL | SOL | 6.41% | $6.4M | Jito |
| ezEIGEN | EIGEN | 18.23% | $329.6K | EigenLayer |
| ezREZ | REZ | 1.64% | $2.5M | EigenLayer |

### Example: Protocol Overview

For general "tell me about Renzo" questions, call `get_protocol_stats` and `get_ezeth_info` together, then summarize:

> Renzo is a liquid restaking protocol with **$469.5M total TVL** across **8 chains**. The flagship product ezETH earns **2.84% APR** with pzETH at **2.34% APR**. The protocol spans both EVM chains (Ethereum, Arbitrum, Base, Linea, BNB Chain, Mode, Blast) and Solana.

### Example: Reserve Vault with Live LTV

The `get_vault_details` tool now returns a `strategy` block for reserve vaults (ezCompETH1, ezUSCC1) with live on-chain LTV data:
```json
{
  "symbol": "ezCompETH1",
  "tvlUsd": 965393.86,
  "aprPercent": 3.78,
  "strategy": {
    "protocols": ["Renzo", "Compound V3"],
    "description": "Automates leveraged looping on Compound Finance to amplify ezETH staking and restaking rewards.",
    "parameters": [
      { "label": "Current LTV", "value": "80.00%" },
      { "label": "Target LTV", "value": "80%" },
      { "label": "Maximum LTV", "value": "89.90%" }
    ]
  }
}
```

Present this as:
> **ezCompETH1** earns **3.78% APR** ($965.4K TVL) via leveraged looping on Compound V3.
>
> | Parameter | Value |
> |-----------|-------|
> | Current LTV | 80.00% |
> | Target LTV | 80% |
> | Maximum LTV (liquidation) | 89.90% |
>
> The vault is operating at its target LTV with a 9.9% buffer before liquidation.

For ezUSCC1 (Aave Horizon), similar strategy data is returned with additional fields: Effective Vault LTV, Position LTV, Market Target LTV, and Max Asset Utilization.

### Example: Vault Strategy (AVS Allocations)

The `get_vault_strategy` tool returns where an EigenLayer vault's capital is deployed:
```json
{
  "vault": { "symbol": "ezETH", "ecosystem": "eigenlayer" },
  "underlyingTvl": 212785.80,
  "allocations": [
    {
      "avs": "EigenDA",
      "description": "EigenDA is a data availability store...",
      "stakedAmount": 128772.95,
      "percentOfTvl": 60.52,
      "operators": ["0xdfcb...", "0x5cd6...", "0x5dcd..."]
    },
    {
      "avs": "Aligned",
      "stakedAmount": 181405.06,
      "percentOfTvl": 85.25,
      "operators": ["0xdfcb...", "0x3f98...", "0x5cd6...", "0x5dcd..."]
    }
  ],
  "operators": [
    { "id": "luganodes", "name": "Luganodes", "link": "https://www.luganodes.com/" },
    { "id": "figment", "name": "Figment", "link": "https://figment.io/" }
  ]
}
```

Present this as:
> **ezETH Strategy** — EigenLayer vault with **212,786 ETH** staked across 16 AVS services.
>
> Top AVS allocations:
>
> | AVS | Staked (ETH) | % of TVL |
> |-----|-------------|----------|
> | Aligned | 181,405 | 85.25% |
> | EigenDA | 128,773 | 60.52% |
> | AltLayer | 74,516 | 35.02% |
> | Witness Chain | 54,591 | 25.66% |
>
> Operators: Figment, Luganodes, Pier Two, HashKey Cloud
>
> Note: Percentages sum to more than 100% because capital is restaked across multiple AVS services simultaneously.

### Example: Token Balances Response

The `get_token_balances` tool returns:
```json
{
  "address": "0xABC...123",
  "network": "Ethereum Mainnet",
  "tokens": [
    {
      "symbol": "ezETH",
      "balance": "12.5432",
      "balanceEth": "13.4476",
      "balanceUsd": 28751.23
    },
    {
      "symbol": "pzETH",
      "balance": "5.0000",
      "balanceEth": "5.2100",
      "balanceUsd": 11134.02
    }
  ],
  "totalValueUsd": 39885.25
}
```

Present this as:
> **Renzo Portfolio** for `0xABC...123` on Ethereum Mainnet:
>
> | Token | Balance | Value (ETH) | Value (USD) |
> |-------|---------|-------------|-------------|
> | ezETH | 12.5432 | 13.4476 | $28,751.23 |
> | pzETH | 5.0000 | 5.2100 | $11,134.02 |
>
> **Total value: $39,885.25**

If `tokens` is empty, tell the user the address holds no Renzo tokens on Ethereum mainnet.

### Example: Withdrawal Requests Response

The `get_withdrawal_requests` tool returns:
```json
{
  "address": "0xABC...123",
  "requests": [
    {
      "withdrawRequestId": 42,
      "ezEthAmount": "2.5000",
      "ethAmount": "2.6803",
      "claimable": false,
      "createdAt": "2025-02-10T14:30:00Z",
      "claimableAt": "2025-02-17T14:30:00Z",
      "timeRemainingSeconds": 172800
    }
  ],
  "totalRequests": 1,
  "cooldownPeriodSeconds": 604800
}
```

Present this as:
> **Pending Withdrawals** for `0xABC...123`:
>
> | # | ezETH | ETH to Receive | Status | Claimable At |
> |---|-------|---------------|--------|-------------|
> | 42 | 2.5000 | 2.6803 | Pending (~2 days left) | Feb 17, 2025 |
>
> The cooldown period is **7 days** from the time of request. Once claimable, the ETH can be claimed from the WithdrawQueue contract.

If `requests` is empty, tell the user they have no pending ezETH withdrawals.

## Choosing the Right Tool

| User asks about... | Call |
|-------------------|------|
| ezETH price, rate, yield, APR, TVL | `get_ezeth_info` |
| Overall Renzo stats, total TVL | `get_protocol_stats` |
| Which chains/networks Renzo supports | `get_supported_chains` |
| Available vaults, vault yields, vault comparison | `get_vaults` |
| Specific vault details (by name or symbol) | `get_vault_details` with the vault symbol |
| EigenLayer operators, validators, delegation | `get_operators` |
| AVS allocations, where capital is staked, restaking strategy | `get_vault_strategy` with the vault symbol |
| Vault LTV, leverage, risk parameters (reserve vaults) | `get_vault_details` with the vault symbol |
| General Renzo overview | `get_protocol_stats` + `get_ezeth_info` |
| "What yield can I get?" | `get_vaults` (shows all vault APRs) |
| "What are my Renzo balances?" (given an address) | `get_token_balances` with the address |
| "Check my withdrawal status" (given an address) | `get_withdrawal_requests` with the address |
| Full portfolio overview (given an address) | `get_token_balances` + `get_withdrawal_requests` |

When the user asks about a specific vault by name, first call `get_vaults` to find the symbol, then call `get_vault_details` with that symbol.

When the user provides an Ethereum address (0x..., 42 hex characters), use it directly with `get_token_balances` or `get_withdrawal_requests`. If the user asks about "my position" or "my balance" without providing an address, ask them for their Ethereum address first.

## External Endpoints

| Endpoint | Method | Data Sent | Purpose |
|----------|--------|-----------|---------|
| `https://mcp.renzoprotocol.com/mcp` | POST | JSON-RPC tool name and arguments (e.g., vault ID, ecosystem filter, Ethereum address) | All Renzo MCP queries |

No other endpoints are contacted. The helper script calls only the Renzo MCP server listed above.

## Security & Privacy

- **No credentials required**: The Renzo MCP endpoint is public and requires no API keys or authentication tokens.
- **No local file access**: The script does not read or write any files on your machine.
- **No persistent state**: Nothing is stored between invocations.
- **Input validation**: Tool names are validated against a hardcoded allowlist. JSON arguments are validated with `jq` before being sent. User-provided values are passed safely via `jq --argjson` (no shell interpolation of user input into URLs or commands).
- **Data sent externally**: When querying user-specific tools (`get_token_balances`, `get_withdrawal_requests`), the Ethereum address you provide is sent to the Renzo MCP server. No other personal data is transmitted.
- **Data received**: All responses are read-only protocol data (token balances, APRs, TVL figures). No executable content is returned or evaluated.

## Trust Statement

By using this skill, queries are sent to the Renzo Protocol MCP server at `https://mcp.renzoprotocol.com/mcp`. For user-specific tools, your Ethereum address is shared with this server. Only install this skill if you trust Renzo Protocol with this information. Source code is available at https://github.com/Renzo-Protocol/openclaw-skill.

## Error Handling

If the script exits with an error:
- **Network failure**: Tell the user the Renzo MCP server is unreachable and suggest trying again later
- **Unknown tool**: This is a bug in the skill — report the tool name attempted
- **Invalid JSON arguments**: Check the argument format matches what the tool expects
- **Server error**: Report the error message from the server response

Never show raw JSON error output to the user. Summarize the issue in plain language.
