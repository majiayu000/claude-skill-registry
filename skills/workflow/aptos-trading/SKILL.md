---
name: aptos-trading
description: Execute trades on Aptos mainnet with price-triggered profit-taking and dip-buying strategies. Includes wallet management, transaction signing, and DEX swaps via Liquidswap. Use when automating APT trading, checking balances, or executing swaps.
version: 1.0.0
---


# Aptos Trading Executor

Automated APT trading on Aptos mainnet with price-triggered strategies.

## Overview

- **Purpose**: Automated profit-taking and dip-buying (vulture) strategies
- **Network**: Aptos Mainnet via REST API
- **DEX**: Liquidswap for APT ↔ USDC swaps

## Quick Start

```bash
# Run the executor (requires confirmation)
python ~/.agents/skills/aptos-trading/scripts/alpha_executor.py
```

## Configuration

Wallet configuration in `/Users/alice/agent_scripts/wallets.yaml`:

- `apt_primary` - Main trading wallet
- `usdc_withdrawal` - USDC extraction wallet

## Strategy Parameters

### Profit Triggers (Bull Levels)
| Level | Price | Action |
|-------|-------|--------|
| B1 | $1.60 | Log only (adjust to take 20%) |
| B2 | $1.80 | Swap 30% to USDC |
| B3 | $2.00 | Swap 50% to USDC |
| MOON | $2.50 | Swap 75% to USDC |

### Dip Buying (Vulture Levels)
| Price | Amount |
|-------|--------|
| $1.40 | 15 APT |
| $1.30 | 15 APT |
| $1.20 | 15 APT |

## Architecture

### AptosClient Class
- `get_account_info()` - Fetch sequence number
- `get_balance()` - Read APT from fungible asset store
- `submit_transaction(payload)` - Sign and submit tx
- `swap_apt_to_usdc(amount, min_out)` - Execute Liquidswap swap

### Price Feeds
1. CoinGecko API (primary)
2. Binance API (fallback)
3. Default $1.50 (emergency)

## Security Notes

⚠️ **CRITICAL**: Private keys are in `wallets.yaml` - NEVER commit this file
⚠️ All transactions are signed locally and submitted to mainnet
⚠️ Script requires typing "EXECUTE" to confirm live trading

### Wallet Validation (MANDATORY)
Before funding ANY wallet, run:
```bash
just aptos-validate-all
```

**NEVER use `derive-resource-account-address` for wallet creation.**
Use `aptos init --private-key` to derive addresses correctly.

## Files

- `scripts/alpha_executor.py` - Main executor
- `references/system-docs.org` - Full system documentation
- `/Users/alice/agent_scripts/wallets.yaml` - Wallet config (external)
- `/Users/alice/agent_scripts/Holdings.md` - Live state tracker
- `/Users/alice/agent_scripts/alpha.log` - Execution log



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.