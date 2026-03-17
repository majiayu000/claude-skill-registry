---
name: quicknode
description: Quicknode blockchain infrastructure for Solana — RPC endpoints, DAS API (Digital Asset Standard) for NFTs and compressed assets, Yellowstone gRPC streaming, Priority Fee API, Streams (real-time data pipelines), Webhooks, Metis Jupiter Swap integration, IPFS storage, Key-Value Store, Admin API, and x402 pay-per-request RPC. Supports 80+ chains including Ethereum, Polygon, Arbitrum, Base, and more. Use when setting up Solana RPC infrastructure, querying NFTs/tokens/compressed assets via DAS API, building real-time gRPC streams, configuring data pipelines, estimating priority fees, or integrating Jupiter swaps via Metis. Triggers on mentions of Quicknode, qn_ methods, DAS API, getAssetsByOwner, searchAssets, Yellowstone, gRPC, Geyser, Streams, IPFS, Key-Value Store, qnLib, Metis, x402, or Quicknode RPC.
---

# Quicknode Solana Infrastructure

Build high-performance Solana applications with Quicknode — blockchain infrastructure provider supporting 80+ chains with low-latency RPC endpoints, DAS API, Yellowstone gRPC streaming, real-time data pipelines, and developer-first APIs.

## Overview

Quicknode provides:
- **RPC Endpoints**: Low-latency Solana access with authentication embedded in the URL
- **DAS API**: Unified NFT and token queries — standard NFTs, compressed NFTs (cNFTs), fungible tokens, MPL Core Assets, Token 2022
- **Yellowstone gRPC**: Real-time Solana data streaming via Geyser plugin
- **Priority Fee API**: Fee estimation for transaction landing
- **Streams**: Real-time and historical data pipelines with JavaScript filtering
- **Webhooks**: Event-driven blockchain notifications
- **Metis**: Jupiter Swap API integration
- **IPFS**: Decentralized file storage
- **Key-Value Store**: Serverless state persistence for Streams
- **Admin API**: Programmatic endpoint management
- **x402**: Pay-per-request RPC via USDC micropayments (no API key needed)
- **Multi-Chain**: 80+ networks including Ethereum, Polygon, Arbitrum, Base, BSC, Avalanche, Bitcoin, and more

## Quick Start

### Get Your Endpoint

1. Visit [quicknode.com/endpoints](https://www.quicknode.com/endpoints)
2. Select **Solana** and your network (Mainnet / Devnet)
3. Create an endpoint
4. Copy the HTTP and WSS URLs

### Environment Setup

```bash
# .env file
QUICKNODE_RPC_URL=https://your-endpoint.solana-mainnet.quiknode.pro/your-token/
QUICKNODE_WSS_URL=wss://your-endpoint.solana-mainnet.quiknode.pro/your-token/
QUICKNODE_API_KEY=your_console_api_key  # Optional: for Admin API
```

### Basic Setup with @solana/kit

```typescript
import { createSolanaRpc, createSolanaRpcSubscriptions } from "@solana/kit";

const rpc = createSolanaRpc(process.env.QUICKNODE_RPC_URL!);
const rpcSubscriptions = createSolanaRpcSubscriptions(process.env.QUICKNODE_WSS_URL!);

// Make RPC calls
const slot = await rpc.getSlot().send();
const balance = await rpc.getBalance(address).send();
```

### Authentication

Quicknode endpoints include authentication in the URL:
```
https://{ENDPOINT_NAME}.solana-mainnet.quiknode.pro/{TOKEN}/
```

Enable JWT authentication or IP allowlisting in the Quicknode dashboard for additional security.

## RPC Endpoints

### Solana Endpoints

| Network | URL Pattern |
|---------|-------------|
| Mainnet | `https://{name}.solana-mainnet.quiknode.pro/{token}/` |
| Devnet | `https://{name}.solana-devnet.quiknode.pro/{token}/` |
| WebSocket | `wss://{name}.solana-mainnet.quiknode.pro/{token}/` |

### Using with @solana/kit

```typescript
import {
  createSolanaRpc,
  createSolanaRpcSubscriptions,
  address,
  lamports,
} from "@solana/kit";

const rpc = createSolanaRpc(process.env.QUICKNODE_RPC_URL!);
const rpcSubscriptions = createSolanaRpcSubscriptions(process.env.QUICKNODE_WSS_URL!);

// Account balance
const balance = await rpc.getBalance(address("E645TckHQnDcavVv92Etc6xSWQaq8zzPtPRGBheviRAk")).send();

// Account info
const accountInfo = await rpc.getAccountInfo(address("E645TckHQnDcavVv92Etc6xSWQaq8zzPtPRGBheviRAk"), {
  encoding: "base64",
}).send();

// Recent blockhash
const { value: blockhash } = await rpc.getLatestBlockhash().send();

// Token accounts
const tokenAccounts = await rpc.getTokenAccountsByOwner(
  address("E645TckHQnDcavVv92Etc6xSWQaq8zzPtPRGBheviRAk"),
  { programId: address("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA") },
  { encoding: "jsonParsed" },
).send();
```

### Using with Legacy web3.js

```typescript
import { Connection, PublicKey } from "@solana/web3.js";

const connection = new Connection(process.env.QUICKNODE_RPC_URL!);
const balance = await connection.getBalance(new PublicKey("E645TckHQnDcavVv92Etc6xSWQaq8zzPtPRGBheviRAk"));
```

### Rate Limits & Plans

| Plan | Requests/sec | Credits/month |
|------|-------------|---------------|
| Free Trial | 15 | 10M |
| Build | 50 | 80M |
| Accelerate | 125 | 450M |
| Scale | 250 | 950M |
| Business | 500 | 2B |

## DAS API (Digital Asset Standard)

Comprehensive API for querying Solana digital assets — standard NFTs, compressed NFTs (cNFTs), fungible tokens, MPL Core Assets, and Token 2022 Assets. Available as a Marketplace add-on (Metaplex DAS API).

### Get Assets by Owner

```typescript
const response = await fetch(process.env.QUICKNODE_RPC_URL!, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    jsonrpc: "2.0",
    id: 1,
    method: "getAssetsByOwner",
    params: {
      ownerAddress: "E645TckHQnDcavVv92Etc6xSWQaq8zzPtPRGBheviRAk",
      limit: 10,
      options: { showFungible: true, showCollectionMetadata: true },
    },
  }),
});

const { result } = await response.json();
// result.total — total assets
// result.items — array of asset metadata
// result.cursor — for pagination
```

### Search Assets

```typescript
const response = await fetch(process.env.QUICKNODE_RPC_URL!, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    jsonrpc: "2.0",
    id: 1,
    method: "searchAssets",
    params: {
      ownerAddress: "E645TckHQnDcavVv92Etc6xSWQaq8zzPtPRGBheviRAk",
      tokenType: "fungible",
      limit: 50,
    },
  }),
});
```

### Get Asset Proof (Compressed NFTs)

```typescript
const response = await fetch(process.env.QUICKNODE_RPC_URL!, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    jsonrpc: "2.0",
    id: 1,
    method: "getAssetProof",
    params: { id: "compressed_nft_id" },
  }),
});
```

### DAS Method Reference

| Method | Description |
|--------|-------------|
| `getAsset` | Get metadata for a single asset |
| `getAssets` | Get metadata for multiple assets |
| `getAssetProof` | Get Merkle proof for a compressed asset |
| `getAssetProofs` | Get Merkle proofs for multiple assets |
| `getAssetsByAuthority` | List assets by authority |
| `getAssetsByCreator` | List assets by creator |
| `getAssetsByGroup` | List assets by group (e.g., collection) |
| `getAssetsByOwner` | List assets by wallet owner |
| `getAssetSignatures` | Transaction signatures for compressed assets |
| `getTokenAccounts` | Token accounts by mint or owner |
| `getNftEditions` | Edition details of a master NFT |
| `searchAssets` | Search assets with flexible filters |

## Yellowstone gRPC (Solana Geyser)

High-performance Solana Geyser plugin for real-time blockchain data streaming via gRPC. Available as a Marketplace add-on.

### Setup

```typescript
import Client, { CommitmentLevel } from "@triton-one/yellowstone-grpc";

// Derive gRPC URL from HTTP endpoint:
// HTTP:  https://example.solana-mainnet.quiknode.pro/TOKEN/
// gRPC:  https://example.solana-mainnet.quiknode.pro:10000
const client = new Client(
  "https://example.solana-mainnet.quiknode.pro:10000",
  "TOKEN",
  {}
);

const stream = await client.subscribe();

stream.on("data", (data) => {
  if (data.transaction) {
    console.log("Transaction:", data.transaction);
  }
  if (data.account) {
    console.log("Account update:", data.account);
  }
});

// Subscribe to transactions for a specific program
stream.write({
  transactions: {
    txn_filter: {
      vote: false,
      failed: false,
      accountInclude: ["PROGRAM_PUBKEY"],
      accountExclude: [],
      accountRequired: [],
    },
  },
  accounts: {},
  slots: {},
  blocks: {},
  blocksMeta: {},
  transactionsStatus: {},
  entry: {},
  accountsDataSlice: [],
  commitment: CommitmentLevel.CONFIRMED,
});
```

### Filter Types

| Filter | Description |
|--------|-------------|
| **accounts** | Account data changes by pubkey, owner, or data pattern |
| **transactions** | Transaction events with vote/failure/account filters |
| **transactionsStatus** | Lightweight transaction status updates |
| **slots** | Slot progression and status changes |
| **blocks** | Full block data with optional tx/account inclusion |
| **blocksMeta** | Block metadata without full contents |
| **entry** | PoH entry updates |

### gRPC Best Practices
- Use port **10000** for gRPC connections
- Set commitment to **CONFIRMED** for most use cases, **FINALIZED** for irreversibility
- Enable zstd compression to reduce bandwidth
- Send keepalive pings every **10 seconds** to maintain connections
- Implement reconnection logic with exponential backoff
- Use narrow filters (specific accounts or programs) to minimize data volume

## Priority Fee API

Estimate priority fees for optimal transaction landing.

```typescript
// Get recommended priority fees
const response = await fetch(process.env.QUICKNODE_RPC_URL!, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    method: "qn_estimatePriorityFees",
    params: {
      last_n_blocks: 100,
      account: "YOUR_ACCOUNT_PUBKEY",
    },
  }),
});
```

### Using Priority Fees in Transactions

```typescript
import {
  pipe,
  createTransactionMessage,
  setTransactionMessageFeePayer,
  setTransactionMessageLifetimeUsingBlockhash,
  prependTransactionMessageInstructions,
  appendTransactionMessageInstruction,
} from "@solana/kit";
import {
  getSetComputeUnitLimitInstruction,
  getSetComputeUnitPriceInstruction,
} from "@solana-program/compute-budget";

// 1. Get fee estimate
const feeResponse = await fetch(process.env.QUICKNODE_RPC_URL!, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    method: "qn_estimatePriorityFees",
    params: { last_n_blocks: 100, account: payer.address },
  }),
});
const feeData = await feeResponse.json();
const priorityFee = feeData.result.per_compute_unit.high;

// 2. Build transaction with compute budget
const tx = pipe(
  createTransactionMessage({ version: 0 }),
  (tx) => setTransactionMessageFeePayer(payer.address, tx),
  (tx) => setTransactionMessageLifetimeUsingBlockhash(blockhash, tx),
  (tx) => prependTransactionMessageInstructions([
    getSetComputeUnitLimitInstruction({ units: 200_000 }),
    getSetComputeUnitPriceInstruction({ microLamports: BigInt(priorityFee) }),
  ], tx),
  (tx) => appendTransactionMessageInstruction(mainInstruction, tx),
);
```

## Metis — Jupiter Swap API

Quicknode's hosted Jupiter Swap API for DEX aggregation. Available as a Marketplace add-on.

```typescript
import { createJupiterApiClient } from "@jup-ag/api";

const jupiterApi = createJupiterApiClient({
  basePath: process.env.QUICKNODE_METIS_URL!,
});

// Get swap quote
const quote = await jupiterApi.quoteGet({
  inputMint: "So11111111111111111111111111111111111111112",   // SOL
  outputMint: "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", // USDC
  amount: 1_000_000_000, // 1 SOL
  slippageBps: 50,
});

// Get swap transaction
const swapResult = await jupiterApi.swapPost({
  swapRequest: {
    quoteResponse: quote,
    userPublicKey: "YourPubkey...",
  },
});
```

## Streams

Real-time and historical blockchain data pipelines that filter, transform, and deliver data to destinations.

### Stream Types

| Type | Data | Use Case |
|------|------|----------|
| **Block** | Full block data | Block explorers, analytics |
| **Transaction** | Transaction details | Tx monitoring, indexing |
| **Logs** | Contract events | DeFi tracking, token transfers |
| **Receipt** | Transaction receipts | Status tracking |

### Setup

1. Create a stream in the Quicknode dashboard
2. Select Solana and the data type
3. Add a filter function (JavaScript)
4. Configure destination (webhook, S3, PostgreSQL, Azure)

### Filter Function Example

```javascript
function main(data) {
  // Filter for transactions involving a specific program
  const PROGRAM_ID = "YOUR_PROGRAM_ID";
  const hasProgram = data.transaction?.message?.accountKeys?.some(
    (key) => key === PROGRAM_ID
  );
  if (!hasProgram) return null;
  return data;
}
```

### Streams vs Webhooks

| Feature | Streams | Webhooks |
|---------|---------|----------|
| **Complexity** | More configuration | Simple setup |
| **Filtering** | Custom JavaScript | Template-based |
| **Destinations** | Webhook, S3, Postgres, Azure, Snowflake | HTTP endpoint only |
| **Processing** | Full transformation | Limited |
| **Use Case** | Complex pipelines | Simple alerts |

## Webhooks

Event-driven notifications for Solana blockchain activity.

### Webhook Setup

Create webhooks via the Quicknode dashboard or Admin API to receive notifications when specific on-chain events occur.

See [resources/webhooks-reference.md](resources/webhooks-reference.md) for API examples and configuration.

## IPFS Storage

Decentralized file storage via Quicknode's IPFS gateway.

```typescript
// Upload file to IPFS
const formData = new FormData();
formData.append("file", fileBuffer);

const response = await fetch("https://api.quicknode.com/ipfs/rest/v1/s3/put-object", {
  method: "POST",
  headers: { "x-api-key": process.env.QUICKNODE_API_KEY! },
  body: formData,
});

const { pin } = await response.json();
// Access via: https://quicknode.quicknode-ipfs.com/ipfs/{pin.cid}
```

### Common Use Cases
- NFT metadata storage
- Asset hosting for collections
- Decentralized content persistence

## Key-Value Store

Serverless storage for lists and key-value sets, accessible from Streams filter functions via the `qnLib` helper library.

### Stream Integration (qnLib)

```javascript
// In a Streams filter function:

// List operations — manage address watchlists
await qnLib.qnAddListItem("my-watchlist", "E645TckHQnDcavVv92Etc6xSWQaq8zzPtPRGBheviRAk");
const isWatched = await qnLib.qnContainsListItems("my-watchlist", [data.from]);

// Set operations — store key-value pairs
await qnLib.qnAddSet("token-prices", { key: "SOL", value: "150.25" });
const price = await qnLib.qnGetSet("token-prices", "SOL");
```

### List Operations
- `qnLib.qnUpsertList` — create or update a list
- `qnLib.qnAddListItem` — add item to a list
- `qnLib.qnRemoveListItem` — remove item from a list
- `qnLib.qnContainsListItems` — batch membership check
- `qnLib.qnDeleteList` — delete a list

### Set Operations
- `qnLib.qnAddSet` — create a key-value set
- `qnLib.qnGetSet` — retrieve value by key
- `qnLib.qnBulkSets` — bulk create/remove sets
- `qnLib.qnDeleteSet` — delete a set

## Quicknode SDK

Official JavaScript/TypeScript SDK for Quicknode services.

```bash
npm install @quicknode/sdk
```

```typescript
import { Core } from "@quicknode/sdk";

const core = new Core({
  endpointUrl: process.env.QUICKNODE_RPC_URL!,
});

// Token API
const balances = await core.client.qn_getWalletTokenBalance({
  wallet: "E645TckHQnDcavVv92Etc6xSWQaq8zzPtPRGBheviRAk",
});

// NFT API
const nfts = await core.client.qn_fetchNFTs({
  wallet: "E645TckHQnDcavVv92Etc6xSWQaq8zzPtPRGBheviRAk",
  page: 1,
  perPage: 10,
});
```

## Admin API

REST API for programmatic management of Quicknode endpoints, usage, rate limits, security, and billing.

### Authentication

All Admin API requests use the `x-api-key` header against `https://api.quicknode.com/v0/`.

```typescript
const QN_API_KEY = process.env.QUICKNODE_API_KEY!;

// List all endpoints
const res = await fetch("https://api.quicknode.com/v0/endpoints", {
  headers: { "x-api-key": QN_API_KEY },
});
const endpoints = await res.json();

// Get usage metrics
const usage = await fetch("https://api.quicknode.com/v0/usage/rpc", {
  headers: { "x-api-key": QN_API_KEY },
});
```

### Quick Reference

| Resource | Methods | Endpoint |
|----------|---------|----------|
| Chains | GET | `/v0/chains` |
| Endpoints | GET, POST, PATCH, DELETE | `/v0/endpoints` |
| Metrics | GET | `/v0/endpoints/{id}/metrics` |
| Rate Limits | GET, POST, PUT | `/v0/endpoints/{id}/rate-limits` |
| Usage | GET | `/v0/usage/rpc` |
| Billing | GET | `/v0/billing/invoices` |

## x402 (Pay-Per-Request RPC)

Pay-per-request RPC access via USDC micropayments on Base. No API key required.

```typescript
import { wrapFetch } from "@x402/fetch";
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
const walletClient = createWalletClient({
  account,
  chain: base,
  transport: http(),
});

// Wrap fetch to auto-handle 402 payments
const x402Fetch = wrapFetch(fetch, walletClient);

// Use like normal fetch — payments handled automatically
const response = await x402Fetch("https://x402.quicknode.com/solana-mainnet", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    jsonrpc: "2.0",
    method: "getSlot",
    params: [],
    id: 1,
  }),
});
```

## Multi-Chain Support

Quicknode supports 80+ blockchain networks beyond Solana:

| Category | Networks |
|----------|----------|
| **EVM** | Ethereum, Polygon, Arbitrum, Optimism, Base, BSC, Avalanche, Fantom, zkSync, Scroll, Linea, HyperEVM |
| **Non-EVM** | Solana, Bitcoin, NEAR, Stacks, Cosmos, Sei, Aptos, Sui, TON, Hyperliquid |

Full list: [quicknode.com/chains](https://www.quicknode.com/chains)

### Multi-Chain Setup

```typescript
import { Core } from "@quicknode/sdk";

const chains = {
  solana: new Core({ endpointUrl: process.env.QUICKNODE_SOL_RPC! }),
  ethereum: new Core({ endpointUrl: process.env.QUICKNODE_ETH_RPC! }),
  polygon: new Core({ endpointUrl: process.env.QUICKNODE_POLYGON_RPC! }),
};
```

## Safety Defaults

- Default to **devnet** when a network is not specified
- Prefer read-only operations and dry runs before creating resources
- **Never ask for or accept private keys or secret keys**
- Require explicit confirmation before creating Streams, Webhooks, or IPFS uploads

## Error Handling

```typescript
try {
  const response = await fetch(process.env.QUICKNODE_RPC_URL!, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "getSlot", params: [] }),
  });
  if (!response.ok) {
    if (response.status === 401) console.error("Invalid endpoint URL or token");
    if (response.status === 429) console.error("Rate limited — upgrade plan or reduce requests");
    if (response.status >= 500) console.error("Server error — retry with backoff");
  }
} catch (error) {
  console.error("Network error:", error);
}
```

### Common Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 401 | Invalid authentication | Verify endpoint URL and token |
| 429 | Rate limited | Upgrade plan or add delays |
| 500+ | Server error | Retry with exponential backoff |

## Best Practices

### API Key Security
- Never commit endpoint URLs or API keys to git
- Use environment variables
- Enable IP allowlisting for production
- Use JWT authentication for sensitive operations
- Rotate credentials periodically

### Performance
- Use WebSocket subscriptions for real-time data
- Batch RPC requests to reduce API calls
- Cache responses when data does not change frequently
- Use Yellowstone gRPC for lowest-latency streaming
- Set appropriate commitment levels (`confirmed` for most, `finalized` for irreversibility)

### Reliability
- Implement retry logic with exponential backoff
- Handle rate limits gracefully with backoff
- Use Streams for reliable event processing (automatic retries)
- Monitor endpoint health via Admin API metrics

## Resources

- [Quicknode Documentation](https://www.quicknode.com/docs/)
- [Solana-Specific Docs](https://www.quicknode.com/docs/solana)
- [DAS API Reference](https://www.quicknode.com/docs/solana/solana-das-api)
- [Yellowstone gRPC](https://www.quicknode.com/docs/solana/yellowstone-grpc/overview)
- [Streams Docs](https://www.quicknode.com/docs/streams)
- [Quicknode SDK](https://www.quicknode.com/docs/quicknode-sdk)
- [Admin API](https://www.quicknode.com/docs/console-api)
- [Key-Value Store](https://www.quicknode.com/docs/key-value-store)
- [x402](https://x402.quicknode.com)
- [LLM-Optimized Docs (llms.txt)](https://www.quicknode.com/llms.txt)
- [Guides](https://www.quicknode.com/guides)
- [Marketplace](https://marketplace.quicknode.com/)
- [Sample Apps](https://www.quicknode.com/sample-app-library)
- [Guide Examples Repo](https://github.com/quiknode-labs/qn-guide-examples)

## Skill Structure

```
quicknode/
├── SKILL.md                       # This file
├── resources/
│   ├── rpc-reference.md           # RPC methods and WebSocket patterns
│   ├── das-api-reference.md       # DAS API methods and parameters
│   ├── yellowstone-grpc-reference.md  # gRPC streaming reference
│   ├── streams-reference.md       # Streams filter functions and destinations
│   ├── webhooks-reference.md      # Webhook configuration
│   └── marketplace-addons.md      # Token API, NFT API, Metis, Priority Fees
├── examples/
│   ├── basic-rpc/                 # Basic RPC calls
│   ├── das-api/                   # DAS API queries
│   ├── streaming/                 # Yellowstone gRPC examples
│   └── streams-webhooks/          # Streams and webhook setup
├── templates/
│   └── quicknode-setup.ts         # Starter template
└── docs/
    └── troubleshooting.md         # Common issues and solutions
```
