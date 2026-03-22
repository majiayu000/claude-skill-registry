---
name: gas-tracker
description: Monitor gas prices across blockchain networks.
metadata: { "cryptoclaw": { "emoji": "⛽", "always": true } }
---

# Gas Tracker Skill

Monitor gas prices across blockchain networks.

## Overview

Provide real-time gas price information to help users time their transactions for optimal costs.

## Capabilities

- **Current gas price**: Show gas price in Gwei for any network
- **Multi-chain comparison**: Compare gas costs across networks
- **Gas estimation**: Estimate cost for specific transaction types
- **Network congestion**: Report on current network load

## Tools Used

- `get_network_info` - Fetch current gas price per network
- `estimate_gas` - Estimate specific transaction costs
- `get_block_info` - Check block utilization

## Example Interactions

User: "What's gas on Ethereum right now?"
Action: Query ETH mainnet gas price, report in Gwei and USD

User: "Compare gas across chains"
Action: Query gas price on ETH, BSC, Polygon, Arbitrum, format comparison

User: "How much would a token transfer cost on BSC?"
Action: Estimate gas for ERC20 transfer on BSC, show in BNB and USD

## Notes

- Gas prices fluctuate rapidly; always note the timestamp
- For L2s (Arbitrum, Optimism, Base), note that gas is typically much cheaper
- BSC gas is typically 3-5 Gwei; Ethereum varies widely
