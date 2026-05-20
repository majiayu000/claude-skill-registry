---
name: whale-watcher
description: Monitor large transactions and whale movements on-chain.
metadata: { "cryptoclaw": { "emoji": "🐋", "always": true } }
---

# Whale Watcher Skill

Monitor large transactions and whale movements on-chain.

## Overview

Track large token transfers and notable wallet activity using on-chain data and block explorer APIs.

## Capabilities

- **Large transfer alerts**: Detect transfers above a threshold
- **Wallet tracking**: Monitor specific addresses for activity
- **Recent blocks scan**: Scan recent blocks for notable transactions
- **Token flow analysis**: Track inflows/outflows for specific tokens

## Tools Used

- `get_block_info` - Fetch block data with transactions
- `get_transaction` - Get transaction details
- `get_native_balance` - Check whale wallet balances
- `get_erc20_balance` - Check token holdings

## Data Sources

- On-chain block/transaction data via RPC
- Block explorer APIs (Etherscan, BSCScan) for indexed data

## Example Interactions

User: "Any big BNB transfers in the last hour?"
Action: Scan recent blocks on BSC, filter transactions above 100 BNB

User: "Watch this address: 0x..."
Action: Check recent transactions for the address, report notable activity

User: "What are whales doing with PEPE?"
Action: Check large PEPE transfers on Ethereum, summarize trends
