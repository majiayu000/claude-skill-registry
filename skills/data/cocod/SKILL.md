---
name: cocod
description: A Cashu ecash wallet CLI for Bitcoin and Lightning payments. Use when managing Cashu tokens, sending/receiving payments via Lightning (bolt11) or ecash, or viewing wallet history.
compatibility: Requires cocod CLI to be installed. Supports Cashu ecash protocol and Lightning Network payments.
metadata:
  project: cocod
  type: cashu-wallet
  networks:
    - cashu
    - bitcoin
    - lightning
---

# Cocod - Cashu Wallet CLI

Cocod is a Cashu wallet for managing ecash tokens and making Bitcoin/Lightning payments. It uses the Cashu protocol for privacy-preserving ecash transactions.

## What is Cashu?

Cashu is a Chaumian ecash protocol that lets you hold and transfer Bitcoin-backed tokens privately. It enables unlinkable transactions using blind signatures.

## Installation

```bash
# Install cocod CLI
bun install -g cocod
```

## Quick Start

```bash
# Initialize your wallet (generates mnemonic automatically)
cocod init

# Or with a custom mint
cocod init --mint-url https://mint.example.com

# Check balance
cocod balance
```

## Commands

### Core Wallet

```bash
# Check daemon and wallet status
cocod status

# Initialize wallet with optional mnemonic
cocod init [mnemonic] [--passphrase <passphrase>] [--mint-url <url>]

# Unlock encrypted wallet (only required when initialised with passphrase)
cocod unlock <passphrase>

# Get wallet balance
cocod balance

# Test daemon connection
cocod ping
```

### Receiving Payments

```bash
# Receive Cashu token
cocod receive cashu <token>

# Create Lightning invoice to receive
cocod receive bolt11 <amount> [--mint-url <url>]
```

### Sending Payments

```bash
# Create Cashu token to send to someone
cocod send cashu <amount> [--mint-url <url>]

# Pay a Lightning invoice
cocod send bolt11 <invoice> [--mint-url <url>]
```

### Mints

```bash
# Add a mint URL
cocod mints add <url>

# List configured mints
cocod mints list

# Get mint information
cocod mints info <url>
```

### Lightning Address (NPC)

Lightning Addresses are email-style identifiers (like `name@npubx.cash`) that let others pay you over Lightning. If you have not purchased a username, NPC provides a free address from your Nostr npub; purchasing a username gives you a human-readable handle. Buying a username is a two-step flow so you can review the required sats before confirming payment.

```bash
# Get your NPC Lightning Address
cocod npc address

# Reserve/buy an NPC username (two-step)
cocod npc username <name>
cocod npc username <name> --confirm
```

### History

```bash
# View wallet history
cocod history

# With pagination
cocod history --offset 0 --limit 20

# Watch for real-time updates
cocod history --watch

# Limit with watch
cocod history --limit 50 --watch
```

### Daemon Control

```bash
# Start the background daemon (started automatically when not running when required)
cocod daemon

# Stop the daemon
cocod stop
```

## Examples

**Initialize with encryption:**

```bash
cocod init --passphrase "my-secret"
```

**Receive via Lightning:**

```bash
cocod receive bolt11 5000
# Returns: lnbc50u1... (share this invoice to receive)
```

**Pay a Lightning invoice:**

```bash
cocod send bolt11 lnbc100u1p3w7j3...
```

**Send Cashu to a friend:**

```bash
cocod send cashu 1000
# Returns: cashuAeyJ0b2tlbiI6...
# Friend receives with: cocod receive cashu cashuAeyJ0b2tlbiI6...
```

**Check status and balance:**

```bash
cocod status
cocod balance
```

**View recent history:**

```bash
cocod history --limit 10
```

## Concepts

- **Cashu**: Privacy-preserving ecash protocol using blind signatures
- **Mint**: Server that issues and redeems Cashu tokens
- **Token**: Transferable Cashu string representing satoshi value
- **Bolt11**: Lightning Network invoice format
- **NPC**: Lightning Address service for receiving payments
- **Mnemonic**: Seed phrase for wallet recovery
