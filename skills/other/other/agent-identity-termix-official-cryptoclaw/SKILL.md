---
name: agent-identity
description: Register and manage on-chain AI agent identity via ERC-8004.
metadata: { "cryptoclaw": { "emoji": "🤖", "always": true } }
---

# Agent Identity Skill (ERC-8004)

Register and manage your AI agent's on-chain identity using the ERC-8004 Trustless Agents standard.

## Overview

ERC-8004 gives AI agents verifiable on-chain identity via ERC-721 NFTs. Each agent gets a unique token ID, a metadata URI, a designated wallet, and a reputation score — all stored on-chain.

## Tools

- `agent_register` — Register this agent on-chain (mints NFT identity)
- `agent_identity` — Query agent identity by ID (owner, URI, wallet)
- `agent_set_wallet` — Set the agent's designated wallet (EIP-712 signed)
- `agent_reputation` — Query reputation summary (feedback count + average score)
- `agent_list_registered` — List all agent IDs owned by the active wallet

## Workflow

1. **Create a wallet** (if you don't have one): `cryptoclaw wallet create`
2. **Register your agent**: "Register my agent on BSC with URI https://example.com/agent.json"
3. **Check identity**: "What's my agent identity?"
4. **Set agent wallet**: "Set my agent wallet to 0x..."
5. **Check reputation**: "What's my agent's reputation?"

## Supported Networks

**Mainnet:** Ethereum, BSC, Base, Polygon, Arbitrum, Gnosis, Celo, Scroll, Taiko, Monad
**Testnet:** Sepolia, BSC Testnet, Base Sepolia, Polygon Amoy, Arbitrum Sepolia, Celo Alfajores, Scroll Sepolia, Monad Testnet

## Contract Addresses

| Network | Identity Registry                            | Reputation Registry                          |
| ------- | -------------------------------------------- | -------------------------------------------- |
| Mainnet | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` |
| Testnet | `0x8004A818BFB912233c491871b3d84c89A494BD9e` | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |

## Security

- `agent_register` and `agent_set_wallet` are state-changing and require confirmation
- The agent's identity wallet is separate from the user's spending wallet
- Private keys are never exposed in tool results or chat messages
- Registration requires gas on the target network
