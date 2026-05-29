---
name: sol-fees
description: Use this skill when the user asks "solana fees", "sol fees", "priority fees", "lamports per signature", or mentions checking transaction fees on Solana. Optional chain parameter (solana or solana-devnet).
allowed-tools: Bash
---

# Solana Network Fees

Gets current fee structure for Solana network.

## Usage

Run the script with optional chain:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-sol-fees.sh [chain]
```

## Arguments

- `chain` (optional): Chain name - solana (default), solana-devnet

## Supported Chains

| Chain | Aliases | Network |
|-------|---------|---------|
| solana | sol | mainnet-beta |
| solana-devnet | sol-devnet, devnet | devnet |

## Requirements

- `solana` CLI must be installed

## Examples

```bash
# Get fees on Solana mainnet
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-sol-fees.sh

# Get fees on Solana devnet
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-sol-fees.sh solana-devnet
```

## Note

For EVM chain gas prices, use the `evm-gas-price` skill instead.
