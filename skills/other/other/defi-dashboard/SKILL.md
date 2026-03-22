---
name: defi-dashboard
description: Monitor yield farming, staking positions, and liquidity pool status.
metadata: { "cryptoclaw": { "emoji": "🏦", "always": true } }
---

# DeFi Dashboard Skill

Monitor yield farming, staking positions, and liquidity pool status.

## Overview

Provide a comprehensive view of DeFi positions including yield farming, staking, and LP positions across protocols.

## Capabilities

- **Staking overview**: Check staking positions and rewards
- **LP positions**: View liquidity pool positions and impermanent loss
- **Yield farming**: Monitor farming rewards across protocols
- **Protocol TVL**: Check total value locked in DeFi protocols

## Tools Used

- `read_contract` - Query DeFi protocol contracts
- `get_erc20_balance` - Check LP token and reward balances
- `get_native_balance` - Check staked native currency

## Data Sources

- On-chain contract queries for individual positions
- DeFiLlama API for protocol-level TVL and APY data

## Example Interactions

User: "Show my DeFi positions"
Action: Scan known DeFi protocols on active chain for wallet positions

User: "What's the APY on PancakeSwap BNB-USDT?"
Action: Query PancakeSwap farm contract for pool info and calculate APY

User: "How much have I earned staking?"
Action: Query staking contract for pending rewards

## Notes

- DeFi protocols have diverse contract interfaces; focus on major protocols
- PancakeSwap (BSC), Uniswap (ETH), Aave, Compound are priority
- Always show both token amounts and USD values
- Warn about impermanent loss for LP positions
