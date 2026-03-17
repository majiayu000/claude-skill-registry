---
name: arweave-bridge
version: "1.0.0"
description: ZigZag Exchange Arweave Bridge - Pay with zkSync stablecoins (USDC/USDT/DAI) for permanent Arweave storage. Use for building dApps needing decentralized file storage, NFT metadata permanence, or Layer 2 storage solutions.
---

# ZigZag Arweave Bridge Skill

The Arweave Bridge is a service built by ZigZag Exchange that enables zkSync transactions to access permanent storage on Arweave. It provides a seamless way for Layer 2 users to store data permanently without needing to acquire AR tokens directly.

**Core Value Proposition**: Access Arweave permanent storage at $1/MB by paying directly on zkSync with stablecoins.

## When to Use This Skill

This skill should be triggered when:
- Building dApps that need permanent, decentralized file storage
- Storing NFT metadata permanently from Layer 2 networks
- Creating permissionless listing systems that need public metadata storage
- Integrating Arweave storage into zkSync applications
- Needing a bridge between L2 payments and permanent storage
- Implementing file upload systems with cryptographic authentication
- Building applications that require immutable data storage guarantees

## Quick Reference

### Base URL
```
https://zigzag-arweave-bridge.herokuapp.com/
```

### Payment Address (zkSync)
```
0xcb7aca0cdea76c5bd5946714083c559e34627607
```

### Supported Tokens
- USDC
- USDT
- DAI

### Conversion Rate
**1 MB per $1** of stablecoin deposited

## API Endpoints

### 1. Check Allocation

Query remaining storage bytes for an address.

**Endpoint:**
```
GET /allocation/zksync?address={wallet_address}
```

**Response:**
```json
{
  "remaining_bytes": 1048576
}
```

**Example:**
```bash
curl "https://zigzag-arweave-bridge.herokuapp.com/allocation/zksync?address=0xYourWalletAddress"
```

### 2. Get Server Time

Get current server timestamp for signature generation.

**Endpoint:**
```
GET /time
```

**Response:**
```json
{
  "timestamp": 1640000000000
}
```

**Example:**
```bash
curl "https://zigzag-arweave-bridge.herokuapp.com/time"
```

### 3. Upload File

Upload a file to Arweave permanent storage.

**Endpoint:**
```
POST /arweave/upload
```

**Content-Type:** `multipart/form-data`

**Required Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `sender` | string | Ethereum wallet address |
| `file` | file | The file to upload |
| `timestamp` | number | Current server timestamp (ms) |
| `signature` | string | ECDSA signature of `{sender}:{timestamp}` |

**Response:**
```json
{
  "arweave_tx_id": "abc123...",
  "remaining_bytes": 1000000
}
```

## Authentication

All uploads require cryptographic signature verification:

1. Get current server timestamp from `/time`
2. Create message: `{sender_address}:{timestamp}`
3. Sign message with your Ethereum private key (ECDSA)
4. Include signature in upload request

**Message Format:**
```
0xYourAddress:1640000000000
```

## Complete Upload Example (Node.js)

```javascript
import { FormData, fileFromPath } from "formdata-node";
import fetch from "node-fetch";
import { ethers } from "ethers";
import dotenv from "dotenv";

dotenv.config();

const BASE_URL = "https://zigzag-arweave-bridge.herokuapp.com";

async function uploadToArweave(filePath) {
  // 1. Get current server time
  const timeResponse = await fetch(`${BASE_URL}/time`);
  const { timestamp } = await timeResponse.json();

  // 2. Create wallet and sign message
  const wallet = new ethers.Wallet(process.env.ETH_PRIVKEY);
  const sender = wallet.address;
  const message = `${sender}:${timestamp}`;
  const signature = await wallet.signMessage(message);

  // 3. Prepare form data
  const formData = new FormData();
  formData.append("sender", sender);
  formData.append("timestamp", timestamp.toString());
  formData.append("signature", signature);
  formData.append("file", await fileFromPath(filePath));

  // 4. Upload file
  const response = await fetch(`${BASE_URL}/arweave/upload`, {
    method: "POST",
    body: formData,
  });

  const result = await response.json();
  console.log("Arweave TX ID:", result.arweave_tx_id);
  console.log("Remaining bytes:", result.remaining_bytes);

  return result;
}

// Usage
uploadToArweave("./my-file.json");
```

## Dependencies

```json
{
  "dependencies": {
    "formdata-node": "^4.0.0",
    "node-fetch": "^3.0.0",
    "ethers": "^5.0.0",
    "dotenv": "^10.0.0"
  }
}
```

## Environment Variables

```bash
# Required for signing uploads
ETH_PRIVKEY=your_private_key_here
```

## Workflow

### Step 1: Fund Your Allocation

Send stablecoins on zkSync to the bridge address:

```
Address: 0xcb7aca0cdea76c5bd5946714083c559e34627607
Network: zkSync
Tokens: USDC, USDT, or DAI
Rate: $1 = 1 MB storage
```

Credits typically appear within 1-2 minutes.

### Step 2: Check Your Allocation

```javascript
const response = await fetch(
  `${BASE_URL}/allocation/zksync?address=${yourAddress}`
);
const { remaining_bytes } = await response.json();
console.log(`Available storage: ${remaining_bytes / 1024 / 1024} MB`);
```

### Step 3: Upload Files

Use the complete upload example above, ensuring:
- Timestamp is current (stale timestamps are rejected)
- Signature is valid for your address
- File size doesn't exceed your allocation

### Step 4: Access Your Data

Once uploaded, your file is permanently stored on Arweave:

```
https://arweave.net/{arweave_tx_id}
```

## Use Cases

### NFT Metadata Storage

```javascript
// Store NFT metadata permanently
const metadata = {
  name: "My NFT",
  description: "A permanent NFT",
  image: "https://arweave.net/previous_image_tx_id",
  attributes: [...]
};

// Write to temp file and upload
fs.writeFileSync("/tmp/metadata.json", JSON.stringify(metadata));
const result = await uploadToArweave("/tmp/metadata.json");

// Use Arweave URL as NFT tokenURI
const tokenURI = `https://arweave.net/${result.arweave_tx_id}`;
```

### Permissionless Token Listing

```javascript
// Store token pair metadata for DEX listing
const pairMetadata = {
  baseToken: "0x...",
  quoteToken: "0x...",
  icon: "base64_image_data",
  description: "Trading pair info"
};

const result = await uploadToArweave(pairMetadataPath);
// Metadata now permanently accessible and verifiable
```

### Document Archival

```javascript
// Archive important documents permanently
const documents = ["contract.pdf", "agreement.pdf", "records.json"];

for (const doc of documents) {
  const result = await uploadToArweave(doc);
  console.log(`${doc} archived: https://arweave.net/${result.arweave_tx_id}`);
}
```

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid signature | Wrong private key or message format | Verify `{sender}:{timestamp}` format |
| Timestamp expired | Request took too long | Get fresh timestamp and retry |
| Insufficient allocation | Not enough storage credits | Send more stablecoins to bridge |
| Invalid sender | Address doesn't match signature | Ensure sender matches signing wallet |

### Error Response Format

```json
{
  "error": "Invalid signature",
  "message": "The provided signature does not match the sender address"
}
```

## Security Considerations

- **Private Key Security**: Never expose your `ETH_PRIVKEY` in client-side code
- **Timestamp Validation**: Always fetch fresh timestamps; stale ones are rejected
- **Replay Protection**: Timestamp in signature prevents replay attacks
- **HTTPS**: Always use HTTPS for API calls

## Why Arweave Bridge?

### The Problem
- Ethereum's original vision included Swarm for decentralized storage, but it was never implemented
- Users on L2s can't easily access permanent storage
- Requiring users to acquire AR tokens creates friction
- Filecoin exists but Arweave has better architecture for permanence

### The Solution
- Pay with familiar stablecoins on zkSync
- No need to acquire or manage AR tokens
- Simple REST API with cryptographic authentication
- Permanent, immutable storage guarantees

## Architecture

```
┌─────────────┐     ┌─────────────────────┐     ┌─────────────┐
│   User      │────▶│  Arweave Bridge     │────▶│   Arweave   │
│  (zkSync)   │     │  (Heroku Server)    │     │  (Storage)  │
└─────────────┘     └─────────────────────┘     └─────────────┘
      │                      │
      │ USDC/USDT/DAI       │ Manages allocations
      ▼                      │ Validates signatures
┌─────────────┐              │ Uploads to Arweave
│   Bridge    │◀─────────────┘
│   Address   │
└─────────────┘
```

## Related Technologies

- **Arweave**: Permanent decentralized storage network
- **zkSync**: Ethereum Layer 2 scaling solution
- **ZigZag Exchange**: Native DEX on ZK Rollups
- **ethers.js**: Ethereum library for signing

## Resources

- [GitHub Repository](https://github.com/ZigZagExchange/arweave-bridge)
- [ZigZag Exchange](https://www.zigzag.exchange/)
- [Arweave Network](https://www.arweave.org/)
- [zkSync](https://zksync.io/)

## Limitations

- Currently supports zkSync only (other L2s planned)
- Requires Node.js environment for the example code
- Server-side signing required (can't sign in browser without exposing private key)
- Hosted on Heroku (consider self-hosting for production)

## Notes

- Allocation credits appear within 1-2 minutes of zkSync transaction
- Files are stored permanently on Arweave once uploaded
- The bridge is open source and can be self-hosted
- Timestamps must be current; the API rejects stale requests
- All uploads are verified via ECDSA signatures

## Version History

- **1.0.0** (2026-01-10): Initial skill release
  - Complete API documentation
  - Node.js upload example
  - Authentication workflow
  - Use case examples
  - Error handling guide
