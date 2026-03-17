---
name: sol-program-idl
description: Use this skill when the user asks "fetch IDL", "program IDL", "anchor idl", "program interface", or mentions fetching Solana program IDL. Requires a program address and optional chain parameter.
allowed-tools: Bash
---

# Solana Program IDL

Fetches the IDL (Interface Definition Language) for Anchor programs on Solana.

## Usage

Run the script with program address and optional chain:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-sol-program-idl.sh <program_address> [chain]
```

## Arguments

- `program_address` (required): Program address (Base58)
- `chain` (optional): Chain name - solana (default), solana-devnet

## Supported Chains

| Chain | Aliases | Network |
|-------|---------|---------|
| solana | sol | mainnet-beta |
| solana-devnet | sol-devnet, devnet | devnet |

## Requirements

- `anchor` CLI must be installed
- Program must be an Anchor program with published IDL

## Examples

```bash
# Fetch IDL for Marinade Finance
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-sol-program-idl.sh MarBmsSgKXdrN1egZf5sqe1TMai9K1rChYNDJgjq7aD solana

# Fetch IDL on devnet
${CLAUDE_PLUGIN_ROOT}/scripts/crypto-sol-program-idl.sh <program_address> solana-devnet
```

## Note

For EVM contract source code, use the `evm-contract-source` skill instead.
