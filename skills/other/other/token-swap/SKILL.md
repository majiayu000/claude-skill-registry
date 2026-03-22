---
name: token-swap
description: Execute token swaps on Uniswap/PancakeSwap across multiple EVM chains.
metadata: { "cryptoclaw": { "emoji": "🔄", "always": true } }
---

# Token Swap Skill

Execute token swaps on Uniswap (V2/V3) and PancakeSwap (V2/V3) across multiple EVM chains.

## Overview

Swap tokens using dedicated DEX tools that automatically compare V2 and V3 quotes to find the best price. Uses the active wallet for signing transactions.

## Supported DEXes

- **BSC**: PancakeSwap V2 + V3
- **Ethereum**: Uniswap V2 + V3
- **Polygon**: QuickSwap V2 + Uniswap V3
- **Arbitrum**: Uniswap V2 + V3
- **Optimism**: Uniswap V3
- **Base**: Uniswap V3

## Tools Used

- `swap_get_quote` - Get best swap quote across V2/V3 with estimated output and price impact
- `swap_execute` - Execute the swap (auto-approves token spending if needed)
- `swap_check_allowance` - Check if token is already approved for the router
- `swap_supported_dexes` - List available DEXes and fee tiers for a network
- `get_erc20_token_info` - Look up token name, symbol, decimals by contract address

## Workflow

1. User requests a swap → call `swap_get_quote` with tokenIn, tokenOut, amountIn
2. Present quote: input amount, estimated output, minimum output, slippage, DEX name, version
3. If price impact is high or slippage > 1%, warn the user
4. Ask user for explicit confirmation before proceeding
5. Call `swap_execute` with same parameters

## Security Rules

- ALWAYS show the swap quote before executing
- ALWAYS warn if estimated output seems low (possible low liquidity)
- NEVER execute swaps without explicit user confirmation
- Default slippage: 0.5% — warn if user sets above 3%
- For large swaps, suggest splitting into multiple smaller trades
- Run `security-check` on the target token before executing a swap to detect honeypots and high taxes

## V3 Fee Tiers

When using V3, the fee tier affects which liquidity pool is used:

- 0.01% (100) — stablecoin pairs
- 0.05% (500) — stable/common pairs
- 0.3% (3000) — most common, default
- 1% (10000) — exotic pairs

The tool auto-selects the best fee tier by default.

## Example Interactions

User: "Swap 1 BNB for USDT on BSC"
→ Call `swap_get_quote` with tokenIn="native", tokenOut="0x55d398326f99059fF775485246999027B3197955", amountIn="1"
→ Show: "PancakeSwap V3: 1 BNB → ~590.23 USDT (min: 587.28 USDT, 0.5% slippage)"
→ After confirmation: call `swap_execute`

User: "What would I get for swapping 100 USDT to ETH on Ethereum?"
→ Call `swap_get_quote` only, display result without executing

User: "What DEXes work on Arbitrum?"
→ Call `swap_supported_dexes` with network="arbitrum"
