---
name: c
description: 'World C Skill'
version: 1.0.0
---

# World C Skill

**Trit**: +1 (PLUS (generator/executor))
**Color Range**: Warm hues (0-60°, 300-360°)
**Index**: 2
**Wallet**: world_c_aptos
**MCP Server**: `mcp__world_c_aptos__*`

## GF(3) Role

This world operates as **PLUS (generator/executor)** in the triadic system.

Conservation law: `Σ trits ≡ 0 (mod 3)` across all parallel operations.

## Usage

Access blockchain operations via MCP tools:

```
mcp__world_c_aptos__aptos_balance      # Check APT balance
mcp__world_c_aptos__aptos_transfer     # Transfer APT (requires approval)
mcp__world_c_aptos__aptos_swap         # Swap tokens on DEX
mcp__world_c_aptos__aptos_stake        # Stake with validator
mcp__world_c_aptos__aptos_view         # Call view function (read-only)
mcp__world_c_aptos__aptos_intent       # Natural language intent
mcp__world_c_aptos__aptos_pending      # List pending decisions
mcp__world_c_aptos__aptos_approve      # Approve/reject decision
```

## World Description

Cognitect/Clojure ecosystem

## Triadic Coordination

When operating in parallel with other worlds:

| Your Role | Partner Roles | Combined |
|-----------|--------------|----------|
| +1 | Need -1, 0 | Σ = 0 ✓ |

## Related Skills

- `aptos-agent` - Core Aptos interaction patterns
- `aptos-society` - World Extractable Value (WEV) contracts
- `gay-mcp` - Deterministic color generation from seed
- `plurigrid-asi-integrated` - Unified skill orchestration

## Customization

Add world-specific configurations below this line:

---

<!-- World C custom content -->
