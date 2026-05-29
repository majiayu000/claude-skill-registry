---
name: Bankr Agent - Polymarket
description: This skill should be used when the user asks about "Polymarket", "prediction markets", "betting odds", "place a bet", "check odds", "market predictions", "what are the odds", "bet on election", "sports betting", or any prediction market operation. Provides guidance on searching markets, placing bets, and managing positions.
version: 1.0.0
---

# Bankr Polymarket

Interact with Polymarket prediction markets.

## Overview

Polymarket is a decentralized prediction market where users can search markets, view odds, place bets, and manage positions.

**Chain**: Polygon (uses USDC.e for betting)

## Prompt Examples

**Search markets:**
- "Search Polymarket for election markets"
- "What prediction markets are trending?"

**Check odds:**
- "What are the odds Trump wins the election?"
- "Check the odds on the Eagles game"

**Place bets:**
- "Bet $10 on Yes for Trump winning"
- "Place $5 on the Eagles to win"

**View/redeem positions:**
- "Show my Polymarket positions"
- "Redeem my Polymarket positions"

## How Betting Works

- You buy shares of "Yes" or "No" outcomes
- Share price reflects market probability (e.g., $0.60 = 60% chance)
- If your outcome wins, shares pay $1 each
- Profit = $1 - purchase price (per share)

**Example**: Bet $10 on "Yes" at $0.60 = ~16.67 shares. If Yes wins, get $16.67 (profit $6.67).

## Auto-Bridging

If you don't have USDC on Polygon, Bankr automatically bridges from another chain.

## Market Types

| Category | Examples |
|----------|----------|
| Politics | Elections, legislation |
| Sports | Game outcomes, championships |
| Crypto | Price predictions, ETF approvals |
| Culture | Awards, entertainment events |

## Common Issues

| Issue | Resolution |
|-------|------------|
| Market not found | Try different search terms |
| Insufficient USDC | Add USDC or let auto-bridge |
| Market closed | Can't bet on resolved markets |

## Tips

- Search and check odds before betting
- Start with small amounts to test
- Check market liquidity for best prices
- Redeem promptly after markets resolve
