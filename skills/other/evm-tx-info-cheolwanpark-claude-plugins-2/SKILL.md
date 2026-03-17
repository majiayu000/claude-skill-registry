---
name: evm-tx-info
description: Use this skill when the user asks for "transaction details", "show me tx", "what happened in this transaction", "look up transaction", or mentions viewing transaction data on EVM chains (Ethereum, Polygon, Arbitrum, etc.). Requires a transaction hash and optional chain parameter.
allowed-tools: Bash
---

# EVM Transaction Info Fetcher

Gets transaction details by hash from an EVM blockchain network.

## Usage

Run the script with transaction hash and optional chain:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-evm-tx-info.sh <tx_hash> [chain]
```

## Arguments

- `tx_hash` (required): Transaction hash (0x + 64 hex characters)
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
# Get transaction on Ethereum
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-evm-tx-info.sh 0x1234...abcd

# Get transaction on Polygon
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-evm-tx-info.sh 0x5678...efgh polygon
```

## Note

For Solana transaction info, use the `sol-tx-info` skill instead.
