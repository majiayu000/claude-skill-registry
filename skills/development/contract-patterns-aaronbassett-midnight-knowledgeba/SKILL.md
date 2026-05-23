---
name: compact-core:contract-patterns
description: Use when implementing common Compact contract patterns such as voting systems, escrow, token transfers, access control, auctions, registries, or when looking for reusable contract templates and design patterns for Midnight blockchain development.
---

# Contract Patterns

> Reusable Compact contract patterns and best practices for Midnight development

## Overview

This skill provides a comprehensive catalog of Compact contract patterns for the Midnight blockchain. Patterns range from simple building blocks to comprehensive multi-contract systems.

### Pattern Categories

1. **Simple Patterns** (~10 focused examples)
   - Basic state management
   - Access control primitives
   - Time-based logic
   - Cryptographic commitments

2. **Deep-Dive Implementations** (3 comprehensive systems)
   - Private Voting System
   - Multi-Party Token Escrow
   - Role-Based Access Registry

## Quick Navigation

### Simple Patterns

| Pattern | File | Use Case |
|---------|------|----------|
| Counter | `examples/simple/counter.compact` | Basic state increments |
| Ownership | `examples/simple/ownership.compact` | Single-owner control |
| Time Lock | `examples/simple/time-lock.compact` | Delayed execution |
| Whitelist | `examples/simple/whitelist.compact` | Membership verification |
| Rate Limit | `examples/simple/rate-limit.compact` | Action throttling |
| Multi-Sig | `examples/simple/multi-sig.compact` | N-of-M approvals |
| Pausable | `examples/simple/pausable.compact` | Emergency stops |
| Upgradeable | `examples/simple/upgradeable.compact` | Logic migration |
| Fee Collector | `examples/simple/fee-collector.compact` | Payment handling |
| Random Selection | `examples/simple/random-selection.compact` | Commit-reveal randomness |

### Deep-Dive Systems

| System | Directory | Description |
|--------|-----------|-------------|
| Private Voting | `examples/deep-dives/private-voting/` | Complete anonymous voting with ZK proofs |
| Token Escrow | `examples/deep-dives/token-escrow/` | Multi-party custody with conditions |
| Access Registry | `examples/deep-dives/access-registry/` | Role-based access with Merkle proofs |

## References

- [Pattern Catalog](references/pattern-catalog.md) - Quick reference for all patterns
- [Private Voting Deep-Dive](references/private-voting.md) - Voting system architecture
- [Token Escrow Deep-Dive](references/token-escrow.md) - Escrow implementation guide
- [Access Registry Deep-Dive](references/access-registry.md) - Role-based access patterns

## Usage Examples

### Finding a Pattern

"Show me the counter pattern"
→ Read `examples/simple/counter.compact`

### Understanding Complex Systems

"How do I implement private voting?"
→ Read `references/private-voting.md` then explore `examples/deep-dives/private-voting/`

### Adapting Patterns

"I need time-locked multi-sig"
→ Combine `time-lock.compact` + `multi-sig.compact` patterns

## Best Practices

1. **Start Simple**: Use simple patterns as building blocks
2. **Understand Privacy**: Know what's public vs private in each pattern
3. **Test Thoroughly**: Each pattern includes test considerations
4. **Combine Carefully**: When mixing patterns, verify privacy guarantees
5. **Document Intent**: Add comments explaining business logic

## Dependencies

All patterns use standard library imports:
```compact
import CompactStandardLibrary;
```

Some advanced patterns may require additional imports:
```compact
import CompactStandardLibrary.Merkle;
import CompactStandardLibrary.Crypto;
```
