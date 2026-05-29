---
name: sol-account-info
description: Use this skill when the user asks "solana balance", "sol balance", "solana account", "is this a program", or mentions checking account info on Solana. Requires an address and optional chain parameter.
allowed-tools: Bash
---

# Solana Account Info

Gets account balance, type, and details from Solana network.

## Usage

Run the script with address and optional chain:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-sol-account-info.sh <address> [chain]
```

## Arguments

- `address` (required): Solana address (Base58, 32-44 characters)
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
# Check account on Solana mainnet
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-sol-account-info.sh vines1vzrYbzLMRdu58ou5XTby4qAqVRLmqo36NKPTg solana

# Check Token Program
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-sol-account-info.sh TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA solana
```

## Note

For EVM address info, use the `evm-address-info` skill instead.
