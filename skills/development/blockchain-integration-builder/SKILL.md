---
name: blockchain-integration-builder
description: Design and implement blockchain integrations across chains and frameworks with emphasis on patterns over specific technologies. Use when building Web3 applications, smart contract systems, token mechanics, decentralized identity, or blockchain-verified data. Triggers on blockchain architecture, smart contract design, Web3 integration, token systems, or decentralized application development. Framework-agnostic—applies to Ethereum, Solana, or emerging chains.
license: MIT
---

# Blockchain Integration Builder

Design blockchain systems using universal patterns applicable across chains.

## Core Abstractions

Blockchain-agnostic thinking: focus on *what* you're trying to achieve, then select chain/framework.

### Fundamental Primitives

| Primitive | What It Is | Chain Examples |
|-----------|------------|----------------|
| Account | Identity with balance | EOA (Eth), Wallet (Solana), Account (Near) |
| Transaction | State change request | Signed message + gas |
| Block | Batch of transactions | Time-ordered, immutable |
| Contract | On-chain program | Solidity, Rust, Move |
| Event/Log | Indexed side-effect | Emitted by contracts, queryable |
| State | Persistent data | Mappings, storage slots |

### Selection Criteria

| Need | Consider | Why |
|------|----------|-----|
| Programmability | Ethereum, Arbitrum, Base | Mature tooling, EVM ecosystem |
| Speed/Cost | Solana, Sui, Aptos | High throughput, low fees |
| Privacy | Aztec, Zcash | Zero-knowledge proofs |
| Interoperability | Cosmos, Polkadot | Cross-chain communication |
| Simplicity | Bitcoin, Litecoin | Limited scripting, proven security |

## Pattern Library

### Identity Patterns

**Wallet-Based Identity**
```
User → Wallet → Sign Message → Verify Signature → Authenticated
```
- No passwords stored
- User controls identity
- Works across applications

**Soul-Bound Tokens (SBTs)**
```
Issuer → Mint SBT → User Wallet (non-transferable)
```
- Credentials, achievements, reputation
- Cannot be sold or transferred
- Revocable by issuer (optionally)

**Decentralized Identifiers (DIDs)**
```
did:method:identifier → Resolve → DID Document → Public Keys, Services
```
- Self-sovereign identity
- Cross-chain portable
- W3C standard

### Token Patterns

**Fungible Tokens (ERC-20 pattern)**
```solidity
// Universal interface
balanceOf(address) → uint256
transfer(to, amount) → bool
approve(spender, amount) → bool
transferFrom(from, to, amount) → bool
```

**Non-Fungible Tokens (ERC-721 pattern)**
```solidity
// Universal interface
ownerOf(tokenId) → address
transferFrom(from, to, tokenId)
tokenURI(tokenId) → string (metadata)
```

**Semi-Fungible (ERC-1155 pattern)**
```solidity
// Batch operations, mixed fungible/non-fungible
balanceOf(account, id) → uint256
balanceOfBatch(accounts[], ids[]) → uint256[]
safeTransferFrom(from, to, id, amount, data)
```

### Governance Patterns

**Token Voting**
```
Proposal → Snapshot Balances → Vote Period → Tally → Execute (if passed)
```

**Quadratic Voting**
```
Cost of N votes = N² tokens
Reduces plutocratic dominance
```

**Optimistic Governance**
```
Proposal → Challenge Period → Execute if unchallenged
```

### Economic Patterns

**Bonding Curves**
```
Price = f(Supply)
Buy: Price increases with supply
Sell: Price decreases with supply
Creates automatic market making
```

**Staking/Slashing**
```
Stake tokens → Perform duties → Earn rewards
Misbehave → Lose stake (slashing)
```

**Streaming Payments**
```
Deposit → Linear unlock over time → Recipient claims
```

## Architecture Patterns

### On-Chain vs Off-Chain

| Aspect | On-Chain | Off-Chain |
|--------|----------|-----------|
| Cost | High (gas fees) | Low/free |
| Speed | Slow (block time) | Fast |
| Trust | Trustless | Requires trust |
| Privacy | Public | Can be private |
| Storage | Expensive | Cheap |

**Hybrid approach:**
```
Off-chain: Computation, storage, user experience
On-chain: Verification, settlement, ownership
Bridge: Oracles, merkle proofs, signatures
```

### Indexing Pattern

Blockchain data is hard to query directly. Use indexers:

```
Blockchain → Events → Indexer → Database → API → Frontend
```

Tools: The Graph, Goldsky, custom indexers

### Oracle Pattern

Bring external data on-chain:

```
External Data → Oracle Network → Consensus → On-chain Value
```

Use cases: Price feeds, random numbers, API data

## Security Principles

### Smart Contract Security

1. **Check-Effects-Interactions**: Update state before external calls
2. **Reentrancy Guards**: Prevent recursive calls
3. **Access Control**: Verify caller permissions
4. **Input Validation**: Never trust user input
5. **Upgrade Patterns**: Plan for bug fixes (proxies, migrations)

### Common Vulnerabilities

| Vulnerability | Description | Prevention |
|---------------|-------------|------------|
| Reentrancy | Recursive calls drain funds | Checks-effects-interactions |
| Integer overflow | Math wraps around | SafeMath or Solidity 0.8+ |
| Front-running | Miners/validators see pending txs | Commit-reveal, flashbots |
| Oracle manipulation | Fake price data | Multiple oracles, TWAP |
| Access control | Missing permission checks | Role-based access |

## Integration Workflow

### 1. Define Requirements

- What needs to be trustless?
- What can stay off-chain?
- Who are the actors?
- What are the assets?

### 2. Select Chain

Based on: throughput needs, cost constraints, ecosystem fit, team expertise

### 3. Design Contracts

- Keep contracts simple and focused
- Separate concerns into multiple contracts
- Plan upgrade path

### 4. Build Indexing

- Determine query patterns
- Index relevant events
- Build API layer

### 5. Create Frontend

- Wallet connection
- Transaction signing
- State display
- Error handling

### 6. Test & Audit

- Unit tests
- Integration tests
- Formal verification (for critical contracts)
- Third-party audit

## References

- `references/contract-patterns.md` - Common smart contract patterns
- `references/chain-comparison.md` - Chain-specific considerations
