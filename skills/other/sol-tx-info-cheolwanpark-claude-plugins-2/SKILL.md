---
name: sol-tx-info
description: Use this skill when the user asks for "solana transaction", "sol tx", "signature details", "confirm signature", or mentions viewing transaction data on Solana. Requires a transaction signature and optional chain parameter.
allowed-tools: Bash
---

# Solana Transaction Info

Gets transaction details by signature from Solana network.

## Usage

Run the script with transaction signature and optional chain:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-sol-tx-info.sh <signature> [chain]
```

## Arguments

- `signature` (required): Transaction signature (Base58, 86-90 characters)
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
# Get transaction on Solana mainnet
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-sol-tx-info.sh 5UfDuX...signature...here solana

# Get transaction on devnet
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-sol-tx-info.sh 5UfDuX...signature...here solana-devnet
```

## Note

For EVM transaction info, use the `evm-tx-info` skill instead.
