---
name: nft-development
description: Master NFT development with token standards, metadata, marketplaces, and on-chain art
sasmp_version: "1.3.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 07-nft-development
bond_type: PRIMARY_BOND

# Skill Configuration
atomic: true
single_responsibility: nft_development

# Parameter Validation
parameters:
  topic:
    type: string
    required: true
    enum: [standards, metadata, marketplace, onchain]
  standard:
    type: string
    default: ERC721
    enum: [ERC721, ERC721A, ERC1155, DN404]

# Retry & Error Handling
retry_config:
  max_attempts: 3
  backoff: exponential
  initial_delay_ms: 1000

# Logging & Observability
logging:
  level: info
  include_timestamps: true
  track_usage: true
---

# NFT Development Skill

> Master NFT development with token standards, metadata design, marketplace integration, and on-chain generative art.

## Quick Start

```python
# Invoke this skill for NFT development
Skill("nft-development", topic="standards", standard="ERC721A")
```

## Topics Covered

### 1. Token Standards
Choose the right standard:
- **ERC-721**: Standard NFTs, one token per ID
- **ERC-721A**: Gas-optimized batch minting
- **ERC-1155**: Multi-token, semi-fungible
- **DN404**: Divisible NFT hybrid

### 2. Metadata Design
Structure your NFT data:
- **On-chain**: Base64 JSON, SVG
- **IPFS**: Content-addressed storage
- **Arweave**: Permanent storage
- **Dynamic**: Evolving traits

### 3. Marketplace Integration
List and sell NFTs:
- **OpenSea**: Seaport protocol
- **Royalties**: EIP-2981
- **Operator Filter**: Royalty enforcement
- **Collection Verification**: Metadata standards

### 4. On-Chain Art
Generate art in Solidity:
- **SVG Generation**: Dynamic shapes
- **Seed-based**: Deterministic randomness
- **Traits**: Rarity distribution
- **Base64**: Data URI encoding

## Code Examples

### ERC-721A Mint
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "erc721a/contracts/ERC721A.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyNFT is ERC721A, Ownable {
    uint256 public constant MAX_SUPPLY = 10000;
    uint256 public constant PRICE = 0.08 ether;

    error MaxSupplyReached();
    error InsufficientPayment();

    constructor() ERC721A("MyNFT", "MNFT") Ownable(msg.sender) {}

    function mint(uint256 quantity) external payable {
        if (_totalMinted() + quantity > MAX_SUPPLY) revert MaxSupplyReached();
        if (msg.value < PRICE * quantity) revert InsufficientPayment();

        _mint(msg.sender, quantity);
    }

    function _startTokenId() internal pure override returns (uint256) {
        return 1;
    }
}
```

### On-Chain SVG
```solidity
function tokenURI(uint256 tokenId) public view returns (string memory) {
    uint256 seed = seeds[tokenId];

    string memory svg = string(abi.encodePacked(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">',
        '<rect width="400" height="400" fill="#', _getColor(seed), '"/>',
        '<circle cx="200" cy="200" r="80" fill="#', _getColor(seed >> 24), '"/>',
        '</svg>'
    ));

    string memory json = string(abi.encodePacked(
        '{"name":"Art #', tokenId.toString(),
        '","image":"data:image/svg+xml;base64,', Base64.encode(bytes(svg)), '"}'
    ));

    return string(abi.encodePacked(
        "data:application/json;base64,",
        Base64.encode(bytes(json))
    ));
}
```

### EIP-2981 Royalties
```solidity
import "@openzeppelin/contracts/token/common/ERC2981.sol";

contract NFTWithRoyalty is ERC721A, ERC2981 {
    constructor() {
        _setDefaultRoyalty(msg.sender, 500); // 5%
    }

    function supportsInterface(bytes4 interfaceId)
        public view override(ERC721A, ERC2981)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
```

## Metadata Schema

### ERC-721 Standard
```json
{
  "name": "Cool NFT #1",
  "description": "A very cool NFT",
  "image": "ipfs://QmXxx.../1.png",
  "animation_url": "ipfs://QmXxx.../1.mp4",
  "external_url": "https://example.com/1",
  "attributes": [
    { "trait_type": "Background", "value": "Blue" },
    { "trait_type": "Rarity", "value": "Legendary" },
    { "display_type": "number", "trait_type": "Power", "value": 100 }
  ]
}
```

## Standard Comparison

| Standard | Best For | Gas (1 mint) | Gas (5 mints) |
|----------|----------|--------------|---------------|
| ERC-721 | Simple NFTs | ~100k | ~500k |
| ERC-721A | PFP collections | ~100k | ~120k |
| ERC-1155 | Game items | ~50k | ~80k |

## Common Pitfalls

| Pitfall | Issue | Solution |
|---------|-------|----------|
| Metadata not showing | Bad tokenURI | Validate JSON, check CORS |
| Gas too high | Standard ERC-721 | Use ERC-721A for batches |
| Royalties not paid | Marketplaces ignore | Use operator filter |
| Reveal broken | Wrong base URI | Test on testnet first |

## Troubleshooting

### "Metadata not showing on OpenSea"
1. Verify tokenURI returns valid JSON
2. Check IPFS gateway accessibility
3. Refresh metadata via API:
```bash
curl "https://api.opensea.io/api/v2/chain/ethereum/contract/{addr}/nfts/{id}/refresh"
```

### "Batch mint out of gas"
- Use ERC-721A instead of ERC-721
- Limit batch size to 10-20 per tx

### "Royalties not enforced"
Implement operator filter:
```solidity
import "operator-filter-registry/src/DefaultOperatorFilterer.sol";

function setApprovalForAll(address op, bool approved)
    public override onlyAllowedOperatorApproval(op)
{
    super.setApprovalForAll(op, approved);
}
```

## Gas Optimization

| Technique | Savings |
|-----------|---------|
| ERC721A batching | ~80% for batches |
| Merkle whitelist | ~50% vs mapping |
| Packed storage | ~20k per slot |
| Custom errors | ~200 per error |

## Cross-References

- **Bonded Agent**: `07-nft-development`
- **Related Skills**: `solidity-development`, `web3-frontend`

## Resources

- ERC-721: eips.ethereum.org/EIPS/eip-721
- ERC-721A: erc721a.org
- OpenSea Metadata: docs.opensea.io/docs/metadata-standards

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01 | Production-grade with standards, on-chain |
| 1.0.0 | 2024-12 | Initial release |
