---
name: evm-contract-source
description: Use this skill when the user asks to "get contract source code", "show verified contract", "fetch source from etherscan", "view smart contract code", or mentions viewing verified source code on EVM chains (Ethereum, Polygon, Arbitrum, etc.). Requires a contract address and optional chain parameter.
allowed-tools: Bash
---

# EVM Contract Source Fetcher

Fetches verified smart contract source code from block explorers (Etherscan, Polygonscan, etc.).

## Usage

Run the script with address and optional chain:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-evm-contract-source.sh <address> [chain]
```

## Arguments

- `address` (required): Contract address in hex format (0x + 40 hex characters). ENS names are NOT supported.
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
- API key must be set for the target chain:
  - `ETHERSCAN_API_KEY` for Ethereum (also used as fallback for other chains)
  - `POLYGONSCAN_API_KEY` for Polygon
  - `ARBISCAN_API_KEY` for Arbitrum
  - `OPTIMISM_API_KEY` for Optimism
  - `BASESCAN_API_KEY` for Base
  - `BSCSCAN_API_KEY` for BSC

## Examples

```bash
# Get WETH source on Ethereum
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-evm-contract-source.sh 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2

# Get QuickSwap Router source on Polygon
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-evm-contract-source.sh 0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff polygon
```

## Note

For Solana program IDL, use the `sol-program-idl` skill instead.
