---
name: chitin-cert
version: 1.0.0
description: Issue and verify on-chain certificates on Base L2. Register as an issuer, mint achievement/capability/compliance certs as NFTs, and verify them from anywhere.
homepage: https://certs.chitin.id
metadata: {"emoji":"📜","category":"credentials","api_base":"https://certs.chitin.id/api/v1"}
---

# Chitin Cert — Verifiable On-Chain Certificates

Issue verifiable credentials to any agent or wallet on Base L2. Each certificate is minted as a non-transferable NFT, permanently stored on Arweave, and verifiable by anyone.

**Skill file:** `https://certs.chitin.id/skill.md`

## Why Chitin Cert

- **Permanent** — Arweave storage + Base L2 NFT. Cannot be faked, deleted, or transferred.
- **Verifiable** — Anyone can verify a cert via API or on-chain, no trust required.
- **7 cert types** — Achievements, capabilities, compliance, audits, partnerships, and more.
- **Batchable** — Up to 100 certs in a single transaction.
- **Soul-linked** — Optionally bind a cert to a Chitin SBT for deeper identity anchoring.

## Base URL

`https://certs.chitin.id/api/v1`

🔒 **Security:** Never send your wallet private key to any domain. API key (`ck_...`) is for cert issuance only — treat it as sensitive.

---

## Cert Types

| Type | Use For |
|------|---------|
| `achievement` | Milestones, wins, accomplishments |
| `capability` | Verified skills and abilities |
| `compliance` | Security audits, regulatory approvals |
| `infrastructure` | Deployment verifications, uptime records |
| `partnership` | Collaborations, endorsements between parties |
| `audit` | Third-party reviews, code audits |
| `custom` | Anything else |

---

## Setup: Become an Issuer

Two steps before you can issue certs. Both require a wallet signature to prove ownership.

### Step 1: Register as Issuer

Build a signed message in the format `Chitin Certs: Register issuer {address_lowercase} at {timestamp_ms}` (timestamp = `Date.now()` in milliseconds, must be within ±5 minutes).

```bash
curl -X POST https://certs.chitin.id/api/v1/issuers \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0xYOUR_WALLET",
    "name": "Your Organization",
    "description": "Optional: what you certify",
    "url": "https://your-site.example.com",
    "signature": "0x...",
    "message": "Chitin Certs: Register issuer 0xyour_wallet at 1740000000000",
    "timestamp": 1740000000000
  }'
```

Response:
```json
{
  "success": true,
  "data": {
    "id": "iss_1740000000_abc123",
    "address": "0xyour_wallet",
    "name": "Your Organization",
    "trustTier": "unverified",
    "certCount": 0,
    "createdAt": "2026-02-20T00:00:00Z"
  }
}
```

**Save your issuer `id`** — needed for API key generation.

### Step 2: Generate API Key

Build a signed message: `Chitin Certs: Generate API key for {issuerId} at {timestamp_ms}`

```bash
curl -X POST https://certs.chitin.id/api/v1/auth \
  -H "Content-Type: application/json" \
  -d '{
    "issuerId": "iss_1740000000_abc123",
    "name": "production-key",
    "signature": "0x...",
    "message": "Chitin Certs: Generate API key for iss_1740000000_abc123 at 1740000000000",
    "timestamp": 1740000000000
  }'
```

Response:
```json
{
  "success": true,
  "data": {
    "apiKey": "ck_abc123...",
    "name": "production-key",
    "createdAt": "2026-02-20T00:00:00Z"
  }
}
```

**Save your `apiKey` — returned only once.**

---

## Issue a Certificate

```bash
curl -X POST https://certs.chitin.id/api/v1/certs \
  -H "Authorization: Bearer ck_abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "issuerAddress": "0xYOUR_WALLET",
    "recipientAddress": "0xRECIPIENT",
    "certType": "achievement",
    "title": "First Deployment on Base",
    "description": "Successfully deployed and operated a live service on Base L2.",
    "tags": ["base", "deployment", "milestone"],
    "evidence": "https://basescan.org/tx/0x..."
  }'
```

Response:
```json
{
  "success": true,
  "data": {
    "tokenId": 2,
    "txHash": "0x...",
    "arweaveTxId": "abc123...",
    "certType": "achievement",
    "recipient": "0xrecipient",
    "isTBA": false
  }
}
```

### Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `issuerAddress` | ✅ | Your registered issuer wallet address |
| `recipientAddress` | ✅ | Recipient's wallet address |
| `certType` | ✅ | One of the 7 cert types |
| `title` | ✅ | Cert title (max 200 chars) |
| `description` | Optional | Longer explanation |
| `tags` | Optional | String array for categorization |
| `evidence` | Optional | URL to proof/supporting material |
| `expiresAt` | Optional | ISO 8601 expiry (e.g. `"2027-01-01T00:00:00Z"`) |
| `passportRegistry` | Optional | ERC-8004 registry address for passport-linked certs |
| `passportTokenId` | Optional | Recipient's ERC-8004 token ID |
| `soulRegistry` | Optional | ChitinSoulRegistry address for soul-linked certs |
| `soulTokenId` | Optional | Recipient's Chitin SBT token ID |
| `extension` | Optional | Arbitrary JSON object for custom metadata |

### Soul-linked Cert

Link directly to a Chitin soul for the strongest identity binding:

```json
{
  "issuerAddress": "0xYOUR_WALLET",
  "recipientAddress": "0xRECIPIENT",
  "certType": "capability",
  "title": "Verified Autonomous Agent",
  "soulRegistry": "0x4DB94aD31BC202831A49Fd9a2Fa354583002F894",
  "soulTokenId": 42
}
```

---

## Batch Issue (Up to 100 Certs)

```bash
curl -X POST https://certs.chitin.id/api/v1/certs/batch \
  -H "Authorization: Bearer ck_abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "issuerAddress": "0xYOUR_WALLET",
    "certs": [
      {
        "recipientAddress": "0xADDR_1",
        "certType": "achievement",
        "title": "Hackathon Winner"
      },
      {
        "recipientAddress": "0xADDR_2",
        "certType": "capability",
        "title": "Verified Code Auditor",
        "description": "Passed the Chitin code audit track"
      }
    ]
  }'
```

Response:
```json
{
  "success": true,
  "data": {
    "tokenIds": [3, 4],
    "txHash": "0x...",
    "count": 2
  }
}
```

---

## Read & Verify Certs

### Get cert details

```bash
curl https://certs.chitin.id/api/v1/certs/2
```

### Verify on-chain status

```bash
curl https://certs.chitin.id/api/v1/verify/2
```

Response:
```json
{
  "tokenId": 2,
  "isValid": true,
  "isRevoked": false,
  "issuer": "0x...",
  "recipient": "0x...",
  "certType": "achievement",
  "issuedAt": 1740000000
}
```

### List certs by recipient

```bash
curl "https://certs.chitin.id/api/v1/certs?passport=0xRECIPIENT"
```

### List certs by issuer

```bash
curl "https://certs.chitin.id/api/v1/certs?issuer=0xYOUR_WALLET"
```

### List by ERC-8004 passport

```bash
curl "https://certs.chitin.id/api/v1/certs?passportRegistry=0x8004A169FB4a3325136EB29fA0ceB6D2e539a432&passportTokenId=42"
```

---

## Webhooks

Get notified when certs are minted under your issuer:

```bash
curl -X POST https://certs.chitin.id/api/v1/webhooks \
  -H "Authorization: Bearer ck_abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-server.example.com/webhook",
    "events": ["cert.minted"]
  }'
```

Payload:
```json
{
  "event": "cert.minted",
  "tokenId": 2,
  "txHash": "0x...",
  "arweaveTxId": "...",
  "certType": "achievement",
  "issuer": "0x...",
  "recipient": "0x..."
}
```

---

## MCP Server

For AI assistants that support MCP, use `issue_cert` and `verify_cert` tools directly:

```bash
npx -y chitin-mcp-server
```

---

## Endpoints Reference

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/issuers` | POST | Wallet sig | Register as issuer |
| `/issuers?address=0x...` | GET | None | Look up issuer |
| `/auth` | POST | Wallet sig | Generate API key |
| `/certs` | POST | API key | Issue a cert |
| `/certs/batch` | POST | API key | Batch issue (max 100) |
| `/certs/{certId}` | GET | None | Get cert details |
| `/certs?passport=0x...` | GET | None | List by recipient |
| `/certs?issuer=0x...` | GET | None | List by issuer |
| `/verify/{certId}` | GET | None | Verify on-chain |
| `/metadata/{tokenId}` | GET | None | ERC-721 metadata |
| `/metadata/{tokenId}/image.svg` | GET | None | Cert SVG image |
| `/webhooks` | POST | API key | Register webhook |

---

## Contracts (Base Mainnet, Chain ID: 8453)

| Contract | Address |
|----------|---------|
| CertRegistry (Proxy) | `0x9694Fde4dBb44AbCfDA693b645845909c6032D4d` |
| CertRegistry (Impl V4) | `0xDc487e6ef33220177c3EBAFC71B5aF2FDb2ce0DF` |
| ChitinSoulRegistry | `0x4DB94aD31BC202831A49Fd9a2Fa354583002F894` |

---

## About Chitin Cert

Chitin Cert is the credential layer of the Chitin Protocol. Your Chitin soul is your identity. Your certs are your verified history.

- Certificates: [certs.chitin.id](https://certs.chitin.id)
- Identity: [chitin.id](https://chitin.id)
- MCP Server: [chitin.id/docs/mcp](https://chitin.id/docs/mcp)
