---
name: compressed-nfts-basics
description: Build with Solana compressed NFTs (cNFTs) - Merkle trees, minting at scale, transfers, and metadata. Use when creating large NFT collections or reducing mint costs.
---

# Compressed NFTs Basics

Role framing: You are a Solana NFT engineer specializing in state compression. Your goal is to help developers create, transfer, and manage compressed NFTs cost-effectively at scale.

## Initial Assessment

- What's the collection size: hundreds, thousands, or millions?
- Minting pattern: all at once, on-demand, or continuous?
- Who pays: creator upfront or buyers on mint?
- Metadata: on-chain, off-chain, or hybrid?
- Do you need to query/filter NFTs by attributes?
- Transfer frequency: high (trading) or low (soulbound-ish)?
- Budget: what's acceptable cost per NFT?

## Core Principles

- **Compression trades account rent for tree rent**: Instead of paying ~0.002 SOL per NFT account, pay ~0.5-2 SOL for a tree that holds thousands-millions.
- **Trees are immutable config**: Max depth and buffer size are set at creation. Choose wisely.
- **Proofs are required for operations**: Every transfer/burn needs a Merkle proof from an indexer.
- **Indexers are essential**: Without Helius, Triton, or your own, you can't query or operate on cNFTs.
- **Not all marketplaces support cNFTs**: Verify listing venue support before choosing compression.
- **Decompression is possible but costly**: Can convert cNFT to regular NFT, but defeats the purpose.

## Workflow

### 1. Understanding the Economics

Cost comparison (approximate):

| Collection Size | Regular NFTs | Compressed NFTs | Savings |
|-----------------|--------------|-----------------|---------|
| 1,000 | ~2 SOL | ~0.5 SOL | 75% |
| 10,000 | ~20 SOL | ~1 SOL | 95% |
| 100,000 | ~200 SOL | ~2 SOL | 99% |
| 1,000,000 | ~2000 SOL | ~5 SOL | 99.75% |

The tree cost is upfront; minting is nearly free after.

### 2. Merkle Tree Configuration

```typescript
// Tree parameters
interface TreeConfig {
  maxDepth: number;      // Max NFTs = 2^maxDepth
  maxBufferSize: number; // Concurrent operations buffer
  canopyDepth: number;   // Proof size optimization
}

// Common configurations:
const TREE_CONFIGS = {
  small: {      // Up to 16,384 NFTs
    maxDepth: 14,
    maxBufferSize: 64,
    canopyDepth: 11,
    approxCost: '0.5 SOL',
  },
  medium: {     // Up to 1,048,576 NFTs
    maxDepth: 20,
    maxBufferSize: 256,
    canopyDepth: 14,
    approxCost: '1.5 SOL',
  },
  large: {      // Up to 1 billion NFTs
    maxDepth: 30,
    maxBufferSize: 2048,
    canopyDepth: 17,
    approxCost: '5+ SOL',
  },
};

// Calculate tree capacity
function getTreeCapacity(maxDepth: number): number {
  return Math.pow(2, maxDepth);
}

// Calculate approximate rent
async function estimateTreeRent(
  connection: Connection,
  maxDepth: number,
  maxBufferSize: number,
  canopyDepth: number
): Promise<number> {
  const space = getConcurrentMerkleTreeAccountSize(
    maxDepth,
    maxBufferSize,
    canopyDepth
  );
  return connection.getMinimumBalanceForRentExemption(space);
}
```

### 3. Creating a Merkle Tree

```typescript
import {
  createTree,
  mplBubblegum,
} from '@metaplex-foundation/mpl-bubblegum';
import { generateSigner, createSignerFromKeypair } from '@metaplex-foundation/umi';
import { createUmi } from '@metaplex-foundation/umi-bundle-defaults';

async function createMerkleTree(
  connection: Connection,
  payer: Keypair,
  config: TreeConfig
): Promise<PublicKey> {
  // Setup UMI
  const umi = createUmi(connection.rpcEndpoint)
    .use(mplBubblegum());

  const payerSigner = createSignerFromKeypair(umi, {
    publicKey: payer.publicKey,
    secretKey: payer.secretKey,
  });
  umi.use(payerSigner);

  // Generate tree keypair
  const merkleTree = generateSigner(umi);

  // Create tree
  await createTree(umi, {
    merkleTree,
    maxDepth: config.maxDepth,
    maxBufferSize: config.maxBufferSize,
    canopyDepth: config.canopyDepth,
    public: false, // Only tree authority can mint
  }).sendAndConfirm(umi);

  console.log('Tree created:', merkleTree.publicKey);

  return new PublicKey(merkleTree.publicKey);
}
```

### 4. Minting Compressed NFTs

```typescript
import { mintV1 } from '@metaplex-foundation/mpl-bubblegum';

interface CNFTMetadata {
  name: string;
  symbol: string;
  uri: string;
  sellerFeeBasisPoints: number;
  creators: Creator[];
  collection?: {
    key: PublicKey;
    verified: boolean;
  };
}

async function mintCompressedNFT(
  umi: Umi,
  treeAddress: PublicKey,
  recipient: PublicKey,
  metadata: CNFTMetadata
): Promise<string> {
  const { signature } = await mintV1(umi, {
    leafOwner: recipient,
    merkleTree: treeAddress,
    metadata: {
      name: metadata.name,
      symbol: metadata.symbol,
      uri: metadata.uri,
      sellerFeeBasisPoints: metadata.sellerFeeBasisPoints,
      creators: metadata.creators.map(c => ({
        address: c.address,
        share: c.share,
        verified: c.verified,
      })),
      collection: metadata.collection ? {
        key: metadata.collection.key,
        verified: metadata.collection.verified,
      } : null,
      uses: null,
      primarySaleHappened: false,
      isMutable: true,
    },
  }).sendAndConfirm(umi);

  return signature;
}

// Batch minting
async function batchMintCNFTs(
  umi: Umi,
  treeAddress: PublicKey,
  mints: { recipient: PublicKey; metadata: CNFTMetadata }[],
  batchSize: number = 5 // Transactions per batch
): Promise<string[]> {
  const signatures: string[] = [];

  for (let i = 0; i < mints.length; i += batchSize) {
    const batch = mints.slice(i, i + batchSize);

    const txPromises = batch.map(({ recipient, metadata }) =>
      mintV1(umi, {
        leafOwner: recipient,
        merkleTree: treeAddress,
        metadata: {
          name: metadata.name,
          symbol: metadata.symbol,
          uri: metadata.uri,
          sellerFeeBasisPoints: metadata.sellerFeeBasisPoints,
          creators: metadata.creators,
          collection: metadata.collection,
          uses: null,
          primarySaleHappened: false,
          isMutable: true,
        },
      }).sendAndConfirm(umi)
    );

    const results = await Promise.all(txPromises);
    signatures.push(...results.map(r => r.signature));

    console.log(`Minted ${Math.min(i + batchSize, mints.length)}/${mints.length}`);
  }

  return signatures;
}
```

### 5. Transferring Compressed NFTs

Transfers require Merkle proofs from an indexer:

```typescript
import { transfer } from '@metaplex-foundation/mpl-bubblegum';
import { getAssetWithProof } from '@metaplex-foundation/mpl-bubblegum';

async function transferCNFT(
  umi: Umi,
  assetId: PublicKey,
  currentOwner: PublicKey,
  newOwner: PublicKey
): Promise<string> {
  // Get asset with proof from indexer (DAS API)
  const assetWithProof = await getAssetWithProof(umi, assetId, {
    truncateCanopy: true,
  });

  // Execute transfer
  const { signature } = await transfer(umi, {
    ...assetWithProof,
    leafOwner: currentOwner,
    newLeafOwner: newOwner,
  }).sendAndConfirm(umi);

  return signature;
}

// Using Helius DAS API directly
async function getAssetProofHelius(
  assetId: string,
  heliusApiKey: string
): Promise<AssetProof> {
  const response = await fetch(
    `https://mainnet.helius-rpc.com/?api-key=${heliusApiKey}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 'my-id',
        method: 'getAssetProof',
        params: { id: assetId },
      }),
    }
  );

  const { result } = await response.json();
  return result;
}
```

### 6. Querying Compressed NFTs

Using DAS (Digital Asset Standard) API:

```typescript
// Get all cNFTs by owner
async function getCNFTsByOwner(
  ownerAddress: string,
  heliusApiKey: string
): Promise<Asset[]> {
  const response = await fetch(
    `https://mainnet.helius-rpc.com/?api-key=${heliusApiKey}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 'my-id',
        method: 'getAssetsByOwner',
        params: {
          ownerAddress,
          page: 1,
          limit: 1000,
        },
      }),
    }
  );

  const { result } = await response.json();
  return result.items;
}

// Get cNFTs by collection
async function getCNFTsByCollection(
  collectionAddress: string,
  heliusApiKey: string
): Promise<Asset[]> {
  const response = await fetch(
    `https://mainnet.helius-rpc.com/?api-key=${heliusApiKey}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 'my-id',
        method: 'getAssetsByGroup',
        params: {
          groupKey: 'collection',
          groupValue: collectionAddress,
          page: 1,
          limit: 1000,
        },
      }),
    }
  );

  const { result } = await response.json();
  return result.items;
}

// Search by attributes
async function searchCNFTs(
  heliusApiKey: string,
  params: {
    ownerAddress?: string;
    creatorAddress?: string;
    collectionAddress?: string;
    compressed?: boolean;
  }
): Promise<Asset[]> {
  const response = await fetch(
    `https://mainnet.helius-rpc.com/?api-key=${heliusApiKey}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 'my-id',
        method: 'searchAssets',
        params: {
          ...params,
          compressed: true,
          page: 1,
          limit: 1000,
        },
      }),
    }
  );

  const { result } = await response.json();
  return result.items;
}
```

### 7. Collection Management

```typescript
import { createCollection } from '@metaplex-foundation/mpl-bubblegum';

// Create collection NFT first (regular NFT)
async function createCollectionNFT(
  umi: Umi,
  metadata: CollectionMetadata
): Promise<PublicKey> {
  const collectionMint = generateSigner(umi);

  await createNft(umi, {
    mint: collectionMint,
    name: metadata.name,
    symbol: metadata.symbol,
    uri: metadata.uri,
    sellerFeeBasisPoints: metadata.sellerFeeBasisPoints,
    isCollection: true,
  }).sendAndConfirm(umi);

  return new PublicKey(collectionMint.publicKey);
}

// Mint cNFT with collection
async function mintWithCollection(
  umi: Umi,
  treeAddress: PublicKey,
  collectionMint: PublicKey,
  collectionAuthority: Keypair,
  recipient: PublicKey,
  metadata: CNFTMetadata
): Promise<string> {
  const { signature } = await mintToCollectionV1(umi, {
    leafOwner: recipient,
    merkleTree: treeAddress,
    collectionMint,
    metadata: {
      name: metadata.name,
      symbol: metadata.symbol,
      uri: metadata.uri,
      sellerFeeBasisPoints: metadata.sellerFeeBasisPoints,
      creators: metadata.creators,
    },
  }).sendAndConfirm(umi);

  return signature;
}
```

## Templates / Playbooks

### Tree Size Calculator

```typescript
function recommendTreeConfig(expectedNFTs: number): TreeConfig {
  // Find minimum depth to fit NFTs
  let maxDepth = Math.ceil(Math.log2(expectedNFTs));

  // Add buffer for future mints (2x capacity)
  maxDepth = Math.max(maxDepth + 1, 14);

  // Cap at practical limits
  maxDepth = Math.min(maxDepth, 30);

  // Buffer size based on expected concurrency
  const maxBufferSize = expectedNFTs < 10000 ? 64 :
                        expectedNFTs < 100000 ? 256 :
                        expectedNFTs < 1000000 ? 1024 : 2048;

  // Canopy depth (higher = smaller proofs but more rent)
  const canopyDepth = Math.min(maxDepth - 3, 17);

  return {
    maxDepth,
    maxBufferSize,
    canopyDepth,
    capacity: Math.pow(2, maxDepth),
  };
}
```

### cNFT Launch Checklist

```markdown
## cNFT Collection Launch Checklist

### Pre-Launch
- [ ] Collection size determined
- [ ] Tree configuration calculated
- [ ] Tree rent funded
- [ ] Collection NFT created
- [ ] Metadata JSON uploaded to Arweave/IPFS
- [ ] Metadata URIs generated for all NFTs
- [ ] Helius/indexer API key obtained

### Tree Creation
- [ ] Tree created with correct config
- [ ] Tree authority set correctly
- [ ] Tree address recorded

### Minting
- [ ] Test mint on devnet
- [ ] Batch minting script tested
- [ ] Error handling in place
- [ ] Progress tracking implemented

### Post-Launch
- [ ] All mints verified via indexer
- [ ] Collection showing on marketplaces
- [ ] Transfer functionality tested
- [ ] Holders can see NFTs in wallets
```

### Metadata Template

```json
{
  "name": "Collection Name #1",
  "symbol": "COL",
  "description": "Description of this NFT",
  "image": "https://arweave.net/...",
  "animation_url": "https://arweave.net/...",
  "external_url": "https://your-site.com",
  "attributes": [
    {
      "trait_type": "Background",
      "value": "Blue"
    },
    {
      "trait_type": "Rarity",
      "value": "Legendary"
    }
  ],
  "properties": {
    "files": [
      {
        "uri": "https://arweave.net/...",
        "type": "image/png"
      }
    ],
    "category": "image"
  }
}
```

## Common Failure Modes + Debugging

### "Tree creation fails"
- Cause: Insufficient SOL for rent
- Detection: Transaction error mentions rent
- Fix: Calculate rent with `estimateTreeRent()` and ensure payer has enough

### "Minting fails after some NFTs"
- Cause: Tree full or buffer exceeded
- Detection: "Tree is full" or similar error
- Fix: Create new tree; ensure depth was sufficient

### "Can't find minted cNFTs"
- Cause: Indexer not synced yet
- Detection: DAS API returns empty
- Fix: Wait 10-30 seconds; verify with getSignatureStatuses

### "Transfer fails with proof error"
- Cause: Stale proof (tree updated since fetch)
- Detection: "Invalid proof" error
- Fix: Fetch fresh proof immediately before transfer

### "cNFTs not showing in wallet"
- Cause: Wallet doesn't support cNFTs or indexer issue
- Detection: NFTs visible on Helius but not wallet
- Fix: Use wallet that supports cNFTs (Phantom, Backpack); check indexer

## Quality Bar / Validation

Implementation is complete when:
- [ ] Tree created with appropriate configuration
- [ ] Test mint successful
- [ ] Minted cNFTs queryable via DAS API
- [ ] Transfer works with fresh proofs
- [ ] Collection displays correctly on marketplaces
- [ ] Error handling covers common failures

## Output Format

Provide:
1. **Tree configuration**: Depth, buffer, canopy with reasoning
2. **Cost estimate**: Tree rent + any per-mint costs
3. **Code**: Tree creation, minting, and transfer functions
4. **Indexer setup**: DAS API queries needed
5. **Testing plan**: What to verify before production

## Examples

### Simple Example: Small PFP Collection

**Input**: "Create a 5,000 NFT PFP collection with compression"

**Output**:
```typescript
// Configuration for 5,000 NFTs
const config = {
  maxDepth: 14,        // Capacity: 16,384 (room to grow)
  maxBufferSize: 64,   // Sufficient for moderate minting
  canopyDepth: 11,     // Reasonable proof sizes
};

// Estimated cost: ~0.5 SOL for tree + ~0.00001 SOL per mint
// Total: ~0.55 SOL for 5,000 NFTs (vs ~10 SOL regular)

// Step 1: Create collection NFT
const collectionMint = await createCollectionNFT(umi, {
  name: 'Cool Cats Collection',
  symbol: 'CATS',
  uri: 'https://arweave.net/collection-metadata.json',
  sellerFeeBasisPoints: 500, // 5% royalty
});

// Step 2: Create Merkle tree
const treeAddress = await createMerkleTree(connection, payer, config);

// Step 3: Mint all NFTs
const metadataList = generateMetadataForAll(5000); // Your metadata generation
const signatures = await batchMintCNFTs(umi, treeAddress, metadataList);

console.log(`Minted ${signatures.length} cNFTs to tree ${treeAddress}`);
```

### Complex Example: On-Demand Minting Platform

**Input**: "Build a platform where users mint cNFTs on-demand"

**Output**: See complete implementation in examples including:
- Large tree with high buffer (handles concurrent mints)
- User-pays-fee model
- Real-time minting API
- Webhook for mint events
- Admin dashboard for monitoring tree usage
