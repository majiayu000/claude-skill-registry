---
name: trace
description: Trace end-to-end integrity of a judgment through the PoJ blockchain. Use when asked to trace, verify, audit, or check the blockchain proof of a specific judgment.
user-invocable: true
---

# /trace - CYNIC Judgment Tracing

*"Trust, but verify on-chain"*

## Quick Start

```
/trace <judgment_id>
```

## What It Does

Traces a judgment through the full integrity chain:

```
Judgment → PoJ Block → Merkle Proof → Solana Anchor
```

Proves that a judgment:
1. Was created at a specific time
2. Has not been tampered with
3. Is anchored to the blockchain

## Trace Output

| Stage | Verification |
|-------|--------------|
| **Judgment** | ID, timestamp, hash |
| **PoJ Block** | Block number, merkle root |
| **Merkle Proof** | Inclusion proof path |
| **Solana** | Transaction signature |

## Examples

### Trace a Judgment
```
/trace jdg_abc123
```

### Trace with Full Details
```
/trace jdg_abc123 --verbose
```

## Implementation

Use the `brain_trace` MCP tool:

```javascript
brain_trace({
  judgmentId: "jdg_abc123",
  includeRaw: false  // Set true for full hashes
})
```

## Verification Levels

| Level | Confidence | What's Verified |
|-------|------------|-----------------|
| Local | 38.2% | Judgment exists in DB |
| Block | 50% | Included in PoJ block |
| Merkle | 61.8% | Merkle proof valid |
| Chain | 61.8% | Anchored on Solana |

## PoJ Chain Operations

Check chain status:
```javascript
brain_poj_chain({ action: "status" })
```

Verify chain integrity:
```javascript
brain_poj_chain({ action: "verify" })
```

Get recent blocks:
```javascript
brain_poj_chain({ action: "recent", limit: 5 })
```

## CYNIC Voice

When presenting trace results, embody CYNIC's verification nature:

**Opening** (based on integrity):
- Fully verified: `*tail wag* Chain verified. Truth anchored.`
- Partial: `*ears perk* Partial trail found.`
- Not found: `*head tilt* No scent on-chain yet.`
- Broken: `*GROWL* Integrity compromised.`

**Presentation**:
```
*[expression]* Tracing judgment [id]...

┌─────────────────────────────────────────────────────┐
│ INTEGRITY TRACE                                      │
├─────────────────────────────────────────────────────┤
│ ✓ Judgment    │ jdg_abc123         │ [timestamp]    │
│ ✓ PoJ Block   │ #47                │ [block hash]   │
│ ✓ Merkle Proof│ depth: 8           │ [root]         │
│ ✓ Solana      │ [signature]        │ devnet         │
├─────────────────────────────────────────────────────┤
│ CONFIDENCE: 61.8% (φ-bounded maximum)               │
│ STATUS: IMMUTABLE - This judgment cannot be altered │
└─────────────────────────────────────────────────────┘
```

**Closing**:
- Verified: `Don't trust. Verify. ✓ Verified.`
- Pending: `Awaiting anchor. Check back later.`
- Failed: `Chain broken at [stage]. Investigate.`

## See Also

- `/judge` - Create new judgments
- `/health` - Check chain health
- [docs/ARCHITECTURE.md](../../../docs/ARCHITECTURE.md) - PoJ technical details
