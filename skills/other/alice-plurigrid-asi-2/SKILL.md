---
name: alice
description: Primary Aptos testnet wallet for transaction origination. Use when initiating test transactions.
metadata:
  trit: -1
---

# World ALICE Skill

**Trit**: -1 (MINUS (validator/constrainer))
**Color Range**: Cold hues (180-300°)
**Index**: 26
**Wallet**: alice_aptos
**MCP Server**: `mcp__alice_aptos__*`

## GF(3) Role

This world operates as **MINUS (validator/constrainer)** in the triadic system.

Conservation law: `Σ trits ≡ 0 (mod 3)` across all parallel operations.

## Usage

Access blockchain operations via MCP tools:

```
mcp__alice_aptos__aptos_balance      # Check APT balance
mcp__alice_aptos__aptos_transfer     # Transfer APT (requires approval)
mcp__alice_aptos__aptos_swap         # Swap tokens on DEX
mcp__alice_aptos__aptos_stake        # Stake with validator
mcp__alice_aptos__aptos_view         # Call view function (read-only)
mcp__alice_aptos__aptos_intent       # Natural language intent
mcp__alice_aptos__aptos_pending      # List pending decisions
mcp__alice_aptos__aptos_approve      # Approve/reject decision
```

## World Description

Primary testnet account for transaction origination

## Triadic Coordination

When operating in parallel with other worlds:

| Your Role | Partner Roles | Combined |
|-----------|--------------|----------|
| -1 | Need +1, 0 | Σ = 0 ✓ |

## Related Skills

- `aptos-agent` - Core Aptos interaction patterns
- `aptos-society` - World Extractable Value (WEV) contracts
- `gay-mcp` - Deterministic color generation from seed
- `plurigrid-asi-integrated` - Unified skill orchestration

## Customization

Add world-specific configurations below this line:

---

<!-- World ALICE custom content -->



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.
