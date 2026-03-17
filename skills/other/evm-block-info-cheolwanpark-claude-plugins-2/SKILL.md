---
name: evm-block-info
description: Use this skill when the user asks "block info", "what's in block", "latest block", "get block details", or mentions viewing block data on EVM chains (Ethereum, Polygon, Arbitrum, etc.). Optional block number/tag and chain parameter.
allowed-tools: Bash
---

# EVM Block Info Fetcher

Gets block information from an EVM blockchain network.

## Usage

Run the script with optional block and chain:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-evm-block-info.sh [block] [chain]
```

## Arguments

- `block` (optional): Block number, hex, or tag (latest, pending, earliest, finalized, safe). Default: latest
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
# Get latest block on Ethereum
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-evm-block-info.sh

# Get specific block on Polygon
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-evm-block-info.sh 50000000 polygon
```

## Note

For Solana slot/block info, use the `sol-slot-info` skill instead.
