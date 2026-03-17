---
name: sol-slot-info
description: Use this skill when the user asks "solana slot", "current slot", "sol block", "latest slot", "epoch info", or mentions checking slot/block info on Solana. Optional slot number and chain parameter.
allowed-tools: Bash
---

# Solana Slot Info

Gets slot or block information from Solana network.

## Usage

Run the script with optional slot and chain:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-sol-slot-info.sh [slot] [chain]
```

## Arguments

- `slot` (optional): Slot number or "latest" (default)
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
# Get current slot on Solana mainnet
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-sol-slot-info.sh

# Get specific slot/block on Solana
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-sol-slot-info.sh 250000000 solana

# Get current slot on devnet
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-sol-slot-info.sh latest solana-devnet
```

## Note

For EVM block info, use the `evm-block-info` skill instead.
