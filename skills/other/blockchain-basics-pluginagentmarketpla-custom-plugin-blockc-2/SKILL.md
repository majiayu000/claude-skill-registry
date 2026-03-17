---
name: blockchain-basics
description: Master blockchain fundamentals including consensus, cryptography, and distributed systems
sasmp_version: "1.3.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 01-blockchain-fundamentals
bond_type: PRIMARY_BOND

# Skill Configuration
atomic: true
single_responsibility: blockchain_education

# Parameter Validation
parameters:
  topic:
    type: string
    required: true
    enum: [consensus, cryptography, networks, transactions, blocks]
  depth:
    type: string
    default: intermediate
    enum: [basic, intermediate, advanced, expert]

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

# Blockchain Basics Skill

> Master blockchain fundamentals including consensus mechanisms, cryptographic primitives, and distributed systems architecture.

## Quick Start

```python
# Invoke this skill for blockchain fundamentals
Skill("blockchain-basics", topic="consensus", depth="intermediate")
```

## Topics Covered

### 1. Consensus Mechanisms
Learn how distributed networks achieve agreement:
- **Proof of Work**: Mining, hashrate, difficulty adjustment
- **Proof of Stake**: Validators, slashing, finality
- **Byzantine Fault Tolerance**: Leader election, view changes

### 2. Cryptographic Foundations
Understand the security primitives:
- **Hash Functions**: SHA-256, Keccak-256, properties
- **Digital Signatures**: ECDSA, Ed25519, verification
- **Merkle Trees**: Proof construction, verification

### 3. Network Architecture
Explore distributed systems:
- **P2P Networks**: Gossip protocols, peer discovery
- **Node Types**: Full nodes, light clients, archives
- **Block Propagation**: Compact blocks, relay networks

### 4. Transaction Lifecycle
Follow data through the chain:
- **Transaction Structure**: Inputs, outputs, signatures
- **Mempool**: Fee markets, ordering, priority
- **Confirmation**: Finality, reorganization

## Code Examples

### Verify Merkle Proof
```python
import hashlib

def verify_merkle_proof(leaf: bytes, proof: list, root: bytes) -> bool:
    """Verify a Merkle proof for inclusion"""
    current = leaf
    for sibling, is_left in proof:
        if is_left:
            current = hashlib.sha256(sibling + current).digest()
        else:
            current = hashlib.sha256(current + sibling).digest()
    return current == root
```

### Calculate Block Hash
```python
import hashlib
import struct

def calculate_block_hash(header: dict) -> bytes:
    """Calculate Bitcoin-style block hash"""
    data = struct.pack(
        '<I32s32sIII',
        header['version'],
        bytes.fromhex(header['prev_block']),
        bytes.fromhex(header['merkle_root']),
        header['timestamp'],
        header['bits'],
        header['nonce']
    )
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()[::-1]
```

## Common Pitfalls

| Pitfall | Issue | Solution |
|---------|-------|----------|
| Finality confusion | PoW is probabilistic | Wait for 6+ confirmations |
| Hash vs encryption | Hashes are one-way | Use proper encryption for secrets |
| Timestamp trust | Miners can manipulate | Use block height for precision |

## Troubleshooting

### "Why is my transaction not confirming?"
1. Check transaction fee vs current mempool
2. Verify nonce is sequential (no gaps)
3. Ensure sufficient balance for amount + gas

### "How do I verify a signature?"
```python
from eth_account import Account
from eth_account.messages import encode_defunct

message = encode_defunct(text="Hello")
address = Account.recover_message(message, signature=sig)
```

## Learning Path

```
[Beginner] → Hash Functions → Digital Signatures → Transactions
    ↓
[Intermediate] → Merkle Trees → Consensus → Network Layer
    ↓
[Advanced] → BFT Protocols → Sharding → Cross-chain
```

## Test Yourself

```python
# Unit test template
def test_merkle_root():
    txs = [b"tx1", b"tx2", b"tx3", b"tx4"]
    root = build_merkle_root(txs)
    assert len(root) == 32
    assert verify_merkle_proof(txs[0], get_proof(0), root)
```

## Cross-References

- **Bonded Agent**: `01-blockchain-fundamentals`
- **Related Skills**: `ethereum-development`, `smart-contract-security`

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01 | Production-grade with validation, examples |
| 1.0.0 | 2024-12 | Initial release |
