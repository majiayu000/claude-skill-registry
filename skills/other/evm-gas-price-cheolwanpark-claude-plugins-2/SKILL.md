---
name: evm-gas-price
description: Use this skill when the user asks "gas price", "how much is gas", "current gas", "check gas fees", or mentions checking gas costs on EVM chains (Ethereum, Polygon, Arbitrum, etc.). Optional chain parameter.
allowed-tools: Bash
---

# EVM Gas Price Fetcher

Gets current gas price for an EVM blockchain network.

## Usage

Run the script with optional chain:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-evm-gas-price.sh [chain]
```

## Arguments

- `chain` (optional): Chain name - ethereum (default), polygon, arbitrum, optimism, base, bsc

## Supported Chains

| Chain | Aliases | Explorer |
|-------|---------|----------|
| ethereum | eth, mainnet | Etherscan |
| polygon | matic | Polygonscan |
| arbitrum | arb | Arbiscan |
| optimism | op | Optimism Etherscan |
| base | - | Basescan |
| bsc | binance | BSCScan |

## Requirements

- `cast` (Foundry) must be installed
- RPC URL is optional (uses PublicNode fallback)

## Examples

```bash
# Get gas price on Ethereum
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-evm-gas-price.sh

# Get gas price on Polygon
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-evm-gas-price.sh polygon
```

## Note

For Solana fees, use the `sol-fees` skill instead.
