---
name: nft-manager
description: View, transfer, and manage NFTs (ERC721 and ERC1155).
metadata: { "cryptoclaw": { "emoji": "🖼️", "always": true } }
---

# NFT Manager Skill

View, transfer, and manage NFTs (ERC721 and ERC1155).

## Overview

Manage NFT collections and individual tokens across EVM chains. View metadata, transfer ownership, and check NFT holdings.

## Capabilities

- **View NFT**: Get metadata, image URI, owner for any NFT
- **Transfer NFT**: Send an NFT to another address
- **List owned NFTs**: Check NFT holdings for a wallet
- **Collection info**: Get collection name, symbol, floor data

## Tools Used

- `get_nft_info` - Fetch NFT metadata (ERC721)
- `transfer_nft` - Transfer ERC721 NFT
- `transfer_erc1155` - Transfer ERC1155 tokens
- `get_erc20_balance` - Check ERC1155 balances
- `read_contract` - Query custom NFT contract functions

## Security Rules

- ALWAYS confirm NFT transfers with token ID and recipient
- Show the NFT name/image before transfer to prevent mistakes
- Warn about sending NFTs to contracts that may not support them
- Use safeTransferFrom when possible

## Example Interactions

User: "Show me NFT #42 from Bored Apes"
Action: Query `get_nft_info` with BAYC contract and token ID 42

User: "Send my NFT to 0x..."
Action: Confirm which NFT, show details, then use `transfer_nft`

User: "What NFTs do I own on Polygon?"
Action: Query known NFT contracts on Polygon for active wallet balance
