---
name: bitbadges-builder
description: Create BitBadges collections (tokens, NFTs, stablecoins) using MCP tools. Use when user wants to create collections, smart tokens, NFTs, or needs to generate BitBadges transaction JSON.
---

# BitBadges Collection Builder

Build BitBadges collections using the `bitbadges-builder-mcp` server tools.

## Quick Reference

### Available Tools

| Tool | Purpose |
|------|---------|
| `build_smart_token` | Create IBC-backed smart token (stablecoin, wrapped asset) |
| `build_fungible_token` | Create ERC-20 style fungible token |
| `build_nft_collection` | Create NFT collection with minting config |
| `generate_backing_address` | Compute backing address for IBC denom |
| `generate_approval` | Build approval structures |
| `generate_permissions` | Build permission presets |
| `generate_alias_path` | Build alias path for liquidity pools |
| `lookup_token_info` | Get token info by symbol or IBC denom |
| `validate_transaction` | Validate JSON against critical rules |
| `get_current_timestamp` | Get timestamp for time-dependent configs |
| `get_skill_instructions` | Get instructions for specific skill |
| `get_master_prompt` | Get complete critical rules |

### Supported Token Symbols

| Symbol | Decimals | Use For |
|--------|----------|---------|
| USDC | 6 | USD stablecoin |
| ATOM | 6 | Cosmos Hub |
| OSMO | 6 | Osmosis |
| BADGE | 9 | Native BitBadges |

## Example Workflows

### 1. USDC Stablecoin with Spend Limit

```
User: "Create a 1:1 backed USDC stablecoin with 100 USDC/day spend limit"

1. Call `lookup_token_info` with query "USDC"
   → Get IBC denom, decimals, backing address

2. Call `build_smart_token` with:
   - ibcDenom: "USDC"
   - creatorAddress: [user's address]
   - name: "Wrapped USDC"
   - symbol: "wUSDC"
   - dailyWithdrawLimit: "100000000" (100 USDC in 6 decimals)

3. Call `validate_transaction` to verify

4. Return JSON for user to broadcast
```

### 2. Simple NFT Collection

```
User: "Create an NFT collection of 1000 items at 5 BADGE each"

1. Call `build_nft_collection` with:
   - creatorAddress: [user's address]
   - name: "My NFT Collection"
   - totalSupply: "1000"
   - mintPrice: "5000000000" (5 BADGE in 9 decimals)
   - mintPriceDenom: "ubadge"
   - tradable: true

2. Call `validate_transaction` to verify

3. Return JSON for user to broadcast
```

### 3. Fungible Token with Liquidity Pool

```
User: "Create a swappable token called MYTOKEN"

1. Call `build_fungible_token` with:
   - creatorAddress: [user's address]
   - name: "My Token"
   - symbol: "MYTOKEN"
   - swappable: true
   - decimals: "9"

2. Call `validate_transaction` to verify

3. Return JSON for user to broadcast
```

## Critical Rules

### Number Format
- ALL numbers must be strings: `"1"` not `1`
- UintRange: `{ "start": "1", "end": "18446744073709551615" }`
- Forever time: `"18446744073709551615"`

### List IDs (Only These Allowed)
- `"All"` - Any address
- `"Mint"` - Mint address
- `"!Mint"` - Except Mint
- `"bb1..."` - Specific address
- `"!bb1..."` - Except address
- `"!Mint:bb1..."` - Smart Token unbacking format

### Smart Token Rules
- TWO approvals required: backing + unbacking
- NO `fromListId: "Mint"` approvals
- `allowBackedMinting: true` required
- `mustPrioritize: true` required
- `overridesFromOutgoingApprovals: false` for backing addresses

### Mint Approval Rules
- MUST have `overridesFromOutgoingApprovals: true`
- Only for `fromListId: "Mint"`

### Token Metadata
- MUST include `tokenIds` field

## Decimals Reference

When converting user amounts to base units:
- USDC: 6 decimals → 100 USDC = "100000000"
- ATOM: 6 decimals → 100 ATOM = "100000000"
- OSMO: 6 decimals → 100 OSMO = "100000000"
- BADGE: 9 decimals → 5 BADGE = "5000000000"

## Troubleshooting

If validation fails, common issues:
1. Numbers not strings → Use `"1"` not `1`
2. Missing tokenIds → Add to tokenMetadata entries
3. Invalid list ID → Use only reserved IDs
4. Missing override → Add `overridesFromOutgoingApprovals: true` for Mint

## Output Format

Always return:
1. Summary of what was created
2. Complete transaction JSON in code block
3. Instructions for broadcasting

```json
{
  "messages": [
    {
      "typeUrl": "/tokenization.MsgUniversalUpdateCollection",
      "value": { ... }
    }
  ]
}
```
