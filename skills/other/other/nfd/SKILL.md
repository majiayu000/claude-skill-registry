---
name: nfd
description: >-
  Work with NFDomains (NFDs), the Algorand Name Service (.algo domains), using
  the @txnlab/nfd-sdk TypeScript SDK. Use when building features that involve
  resolving .algo domain names to addresses (or reverse), displaying NFD avatars
  and metadata, searching for NFDs, minting new NFDs, purchasing NFDs from the
  marketplace, managing NFD metadata and linked addresses, working with NFD
  segments (subdomains), interacting with NFD vaults, or integrating NFD name
  resolution into Algorand applications.
---

# NFDomains (NFD)

NFDomains are human-readable names (e.g., `alice.algo`) on the Algorand blockchain. Each NFD is a smart contract that maps a `.algo` name to wallet addresses, metadata, and a vault account.

## Package

`@txnlab/nfd-sdk` — TypeScript SDK for on-chain NFD operations. Requires `algosdk` as a peer dependency.

```bash
npm install @txnlab/nfd-sdk algosdk
```

The SDK uses AlgoKit typed clients to interact with NFD contracts directly on-chain. It also exposes `nfd.api` for search operations that require off-chain indexing.

A REST API exists at `https://api.nf.domains` (TestNet: `https://api.testnet.nf.domains`), but the SDK is preferred for all operations it supports.

## NfdClient Initialization

```typescript
import { NfdClient } from '@txnlab/nfd-sdk'

const nfd = new NfdClient() // MainNet (default)
const nfd = NfdClient.mainNet() // MainNet (explicit)
const nfd = NfdClient.testNet() // TestNet
```

Custom configuration:

```typescript
import { NfdClient, NfdRegistryId } from '@txnlab/nfd-sdk'
import { AlgorandClient } from '@algorandfoundation/algokit-utils'

const nfd = new NfdClient({
  algorand: AlgorandClient.mainNet(),
  registryId: NfdRegistryId.MAINNET, // 760937186
})
```

For write operations (mint, buy, manage), set a signer:

```typescript
const signedClient = nfd.setSigner(activeAddress, transactionSigner)
```

## Key Concepts

- **Forward resolution**: Name → address (`nfd.resolve('alice.algo')`)
- **Reverse lookup**: Address → name (`nfd.resolveAddress(address)`)
- **Views**: `tiny` (minimal), `brief` (default), `full` (all properties)
- **depositAccount**: The safe address to send assets to (resolves verified → unverified → owner)
- **caAlgo**: Array of verified linked Algorand addresses
- **unverifiedCaAlgo**: Array of unverified linked addresses
- **nfdAccount**: The NFD's vault (contract-controlled Algorand account)
- **Segments**: Subdomains like `sub.root.algo`, minted from a root NFD

## Reference Files

Read the appropriate file based on the task:

| Task                                                | Reference                                           |
| --------------------------------------------------- | --------------------------------------------------- |
| Install SDK, initialize client                      | [getting-started.md](references/getting-started.md) |
| Resolve name → address, reverse lookup              | [resolve.md](references/resolve.md)                 |
| Get avatar/banner images                            | [images.md](references/images.md)                   |
| Search for NFDs                                     | [search.md](references/search.md)                   |
| Mint a new NFD                                      | [minting.md](references/minting.md)                 |
| Buy or claim an NFD                                 | [purchasing.md](references/purchasing.md)           |
| Link addresses, set metadata                        | [managing.md](references/managing.md)               |
| Work with segments (subdomains)                     | [segments.md](references/segments.md)               |
| Send assets to/from vaults                          | [vaults.md](references/vaults.md)                   |
| Integrate NFDs into an app (display names, avatars) | [integration.md](references/integration.md)         |
| Full API surface and types                          | [api-reference.md](references/api-reference.md)     |

## SDK vs REST API

The SDK handles: resolve, reverse lookup, images, mint, claim, buy, manage (link address, set metadata, set primary), search.

The REST API is needed for: vault send-to/send-from operations, batch address lookups (20+ addresses), analytics/activity queries, consensus leaders, contract upgrades.

When both can do it, use the SDK.
