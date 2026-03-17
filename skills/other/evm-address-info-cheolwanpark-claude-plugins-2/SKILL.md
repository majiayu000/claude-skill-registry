---
name: evm-address-info
description: Use this skill when the user asks to "check balance", "what's the balance of", "is this a contract or EOA", "get address info", or mentions checking wallet balance or account type on EVM chains (Ethereum, Polygon, Arbitrum, etc.). Requires an address and optional chain parameter.
allowed-tools: Bash
---

# EVM Address Info Fetcher

Gets address balance and account type (EOA vs Contract) from an EVM blockchain network.

## Usage

Run the script with address and optional chain:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-evm-address-info.sh <address> [chain]
```

## Arguments

- `address` (required): Ethereum address (0x + 40 hex) or ENS name
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
# Check ENS name balance on Ethereum
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-evm-address-info.sh vitalik.eth

# Check address on Polygon
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-evm-address-info.sh 0x1234...abcd polygon
```

## Note

For Solana account info, use the `sol-account-info` skill instead.
