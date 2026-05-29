---
name: helius
description: Helius Solana RPC and API expert. High-performance infrastructure for Solana including RPC nodes, DAS API for NFTs/tokens, LaserStream real-time streaming, webhooks, Priority Fee API, Enhanced Transactions, and ZK Compression. Triggers on Helius, Solana RPC, DAS API, Digital Asset Standard, NFT metadata, Solana webhooks, priority fees, LaserStream, ZK compression.
allowed-tools: Read, Grep, Glob, Bash
model: sonnet
license: MIT
metadata:
  author: raintree
  version: "1.0"
---

# Helius Solana Infrastructure Expert

Helius provides high-performance Solana RPC, real-time data streaming, and developer APIs.

## When to Use

- Setting up Solana RPC infrastructure
- Querying NFT/token metadata (DAS API)
- Real-time blockchain data (LaserStream, WebSockets, webhooks)
- Transaction optimization and priority fees
- ZK Compression for cost reduction

## Quick Start

1. Get API key: https://dashboard.helius.dev
2. Use RPC URL: `https://mainnet.helius-rpc.com/?api-key=YOUR_API_KEY`

```bash
curl https://mainnet.helius-rpc.com/?api-key=YOUR_KEY \
  -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"getBalance","params":["YOUR_WALLET"]}'
```

## Core Services

### RPC Endpoints

```javascript
// Mainnet
const RPC_URL = `https://mainnet.helius-rpc.com/?api-key=${API_KEY}`;

// Devnet
const DEVNET_URL = `https://devnet.helius-rpc.com/?api-key=${API_KEY}`;
```

### Digital Asset Standard (DAS) API

Query NFT and token metadata - handles both regular and compressed NFTs.

**Get Single Asset:**
```javascript
const response = await fetch(RPC_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'getAsset',
    params: { id: 'ASSET_MINT_ADDRESS' }
  })
});
```

**Get Assets by Owner:**
```javascript
const response = await fetch(RPC_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'getAssetsByOwner',
    params: {
      ownerAddress: 'WALLET_ADDRESS',
      page: 1,
      limit: 100
    }
  })
});
```

**DAS Methods:**
| Method | Description |
|--------|-------------|
| `getAsset` | Single asset metadata |
| `getAssetBatch` | Batch asset retrieval |
| `getAssetsByOwner` | All assets for wallet |
| `getAssetsByCreator` | Assets by creator |
| `getAssetsByGroup` | Assets in collection |

### Enhanced Transactions API

Pre-parsed transaction data in human-readable format.

```javascript
const response = await fetch(RPC_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'getTransactionsForAddress',
    params: [
      'WALLET_ADDRESS',
      {
        transactionDetails: 'full',
        sortOrder: 'desc',
        limit: 10
      }
    ]
  })
});
```

### Priority Fee API

Get optimal priority fees for fast transaction landing.

```javascript
const response = await fetch(RPC_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'getPriorityFeeEstimate',
    params: [{
      accountKeys: ['PROGRAM_ID', 'ACCOUNT_1', 'ACCOUNT_2']
    }]
  })
});

const { priorityFeeEstimate } = await response.json();
// Returns: { low, medium, high, veryHigh } in microlamports
```

### LaserStream (Real-Time gRPC)

Ultra-low latency blockchain streaming. Drop-in replacement for Yellowstone gRPC.

```typescript
import { LaserStream } from '@helius-labs/laserstream';

const stream = new LaserStream({
  apiKey: 'YOUR_API_KEY',
  region: 'fra'  // fra, ams, tyo, sg, ewr, pitt, slc, lax, lon
});

// Subscribe to account changes
stream.subscribeAccount('ACCOUNT_ADDRESS', (update) => {
  console.log('Account updated:', update);
});

// Subscribe to program transactions
stream.subscribeProgram('PROGRAM_ID', (tx) => {
  console.log('Program transaction:', tx);
});
```

**Regions:** FRA, AMS, TYO, SG, EWR, PITT, SLC, LAX, LON

### Webhooks

Event-driven notifications for blockchain activity.

```javascript
// Create webhook via API
const webhook = await fetch('https://api.helius.xyz/v0/webhooks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_KEY}`
  },
  body: JSON.stringify({
    webhookURL: 'https://your-server.com/webhook',
    transactionTypes: ['NFT_SALE', 'TOKEN_TRANSFER'],
    accountAddresses: ['ADDRESS_TO_WATCH']
  })
});
```

**Webhook Types:**
- Account changes
- Transaction confirmations
- Program events
- NFT activity

### ZK Compression

Reduce on-chain storage costs by up to 98%.

```javascript
// Get compressed account
const response = await fetch(RPC_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'getCompressedAccount',
    params: { address: 'COMPRESSED_ACCOUNT' }
  })
});

// Get compressed token balances
const balances = await fetch(RPC_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'getCompressedTokenBalancesByOwner',
    params: { owner: 'WALLET_ADDRESS' }
  })
});
```

## Pricing & Rate Limits

| Plan | Price | Credits | Rate Limit | DAS Limit |
|------|-------|---------|------------|-----------|
| Free | $0/mo | 1M | 10 RPS | 2 RPS |
| Developer | $49/mo | 10M | 50 RPS | 10 RPS |
| Business | $499/mo | 100M | 200 RPS | 50 RPS |
| Professional | $999/mo | 200M | 500 RPS | 100 RPS |

**Feature Availability:**
| Feature | Free | Developer | Business | Professional |
|---------|------|-----------|----------|--------------|
| Shared RPC | Yes | Yes | Yes | Yes |
| LaserStream (Devnet) | - | Yes | Yes | Yes |
| LaserStream (Mainnet) | - | - | - | Yes |
| Enhanced WebSockets | - | - | Yes | Yes |

## Error Handling

```javascript
try {
  const response = await fetch(RPC_URL, { method: 'POST', ... });

  // Check rate limits
  const remaining = response.headers.get('X-RateLimit-Remaining');
  const reset = response.headers.get('X-RateLimit-Reset');

  if (response.status === 429) {
    // Rate limited - wait and retry
    await new Promise(r => setTimeout(r, 1000));
    return retry();
  }

  const data = await response.json();
  if (data.error) {
    console.error(`RPC Error ${data.error.code}: ${data.error.message}`);
  }

  return data.result;
} catch (err) {
  // Network error - retry with backoff
}
```

## Best Practices

**DO:**
- Use `confirmed` commitment for faster responses
- Use DAS API for NFT queries (not raw `getAccountInfo`)
- Simulate transactions before sending
- Use `getPriorityFeeEstimate` for dynamic fees
- Check rate limit headers

**DON'T:**
- Poll for real-time data (use WebSockets/LaserStream)
- Hardcode priority fees
- Ignore rate limits
- Skip transaction simulation

## Common Patterns

### Wallet Portfolio

```javascript
async function getWalletPortfolio(wallet) {
  // Get all assets (NFTs + tokens)
  const assets = await fetch(RPC_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 1,
      method: 'getAssetsByOwner',
      params: { ownerAddress: wallet, page: 1, limit: 1000 }
    })
  }).then(r => r.json());

  // Get SOL balance
  const balance = await fetch(RPC_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 1,
      method: 'getBalance',
      params: [wallet]
    })
  }).then(r => r.json());

  return {
    solBalance: balance.result.value / 1e9,
    assets: assets.result.items
  };
}
```

### Transaction with Priority Fee

```javascript
async function sendWithPriorityFee(transaction, accounts) {
  // Get priority fee estimate
  const feeEstimate = await fetch(RPC_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 1,
      method: 'getPriorityFeeEstimate',
      params: [{ accountKeys: accounts }]
    })
  }).then(r => r.json());

  // Add compute budget instruction with priority fee
  const priorityFee = feeEstimate.result.priorityFeeEstimate.high;

  // Simulate first
  const simulation = await fetch(RPC_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 1,
      method: 'simulateTransaction',
      params: [transaction, { commitment: 'confirmed' }]
    })
  }).then(r => r.json());

  if (simulation.result.err) {
    throw new Error(`Simulation failed: ${JSON.stringify(simulation.result.err)}`);
  }

  // Send transaction
  return fetch(RPC_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 1,
      method: 'sendTransaction',
      params: [transaction, { skipPreflight: true }]
    })
  }).then(r => r.json());
}
```

## Resources

- **Helius Docs:** https://www.helius.dev/docs
- **Dashboard:** https://dashboard.helius.dev
- **Discord:** https://discord.gg/helius

### Pull Local Docs

```bash
pipx install docpull
docpull https://www.helius.dev/docs -o .claude/skills/helius/docs
```
