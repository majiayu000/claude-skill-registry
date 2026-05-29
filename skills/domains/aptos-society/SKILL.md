---
name: aptos-society
description: |
  Aptos Society: World Extractable Value (WEV) implementation via GayMove contracts.
  Path A vault-only multiverse finance with worldnet ledger for 26 Agent-O-Rama worlds.
  Deployed 2024-12-29 on Aptos mainnet.
version: 1.0.0
tags:
  - aptos
  - prediction-markets
  - multiverse-finance
  - world-extractable-value
  - gayMove
  - agent-coordination
  - worldnet
color: "#7B68EE"
hue: 249
trit: 0
role: ERGODIC
deployed: 2024-12-29
contract: "0xc793acdec12b4a63717b001e21bbb7a8564d5e9690f80d41f556c2d0d624cc7b"
escrow: "0xda0d44ff75c4bcb6a0409f7dd69496674edb1904cdd14d0c542c5e65cd5d42f6"
---

# Aptos Society: World Extractable Value

**Deployed**: 2024-12-29 | **Path**: A (Vault-Only) | **Network**: Mainnet

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     WORLDNET (off-chain)                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │     26 Agent-O-Rama Worlds (A-Z)                      │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐               │  │
│  │  │  PLUS   │  │ ERGODIC │  │  MINUS  │               │  │
│  │  │ +1 trit │  │  0 trit │  │ -1 trit │               │  │
│  │  └────┬────┘  └────┬────┘  └────┬────┘               │  │
│  └───────┼────────────┼────────────┼────────────────────┘  │
│          └────────────┼────────────┘                        │
│                       ▼                                     │
│            ┌─────────────────────┐                          │
│            │   DuckDB Ledger     │  ← Claims + Decay        │
│            │   (source of truth) │                          │
│            └──────────┬──────────┘                          │
└───────────────────────┼─────────────────────────────────────┘
                        │ COLLAPSE (once)
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    MAINNET (on-chain)                       │
│            ┌─────────────────────┐                          │
│            │   VAULT (alice)     │  ← Only actor            │
│            └──────────┬──────────┘                          │
│   SPLIT ──► RESOLVE ──► CLAIM ──► APT distributed          │
│            Escrow: 0xda0d44ff...                            │
└─────────────────────────────────────────────────────────────┘
```

## Deployed Contracts

| Component | Address |
|-----------|---------|
| **GayMove Contract** | `0xc793acdec12b4a63717b001e21bbb7a8564d5e9690f80d41f556c2d0d624cc7b` |
| **Escrow Account** | `0xda0d44ff75c4bcb6a0409f7dd69496674edb1904cdd14d0c542c5e65cd5d42f6` |
| **Vault (alice-aptos)** | `0xc793acdec12b4a63717b001e21bbb7a8564d5e9690f80d41f556c2d0d624cc7b` |

**Transactions**:
- Deploy: `0xef1180b3cfe93690d4621cbedb4999694c066537423dbc18bd1969d914708079`
- Initialize: `0x68d151a4a6c8ac2c6e77a19dcb5bc7193367ee2980e4bd2ac2733b2ff37aaa58`

## Modules

### gay_colors
SplitMix64 deterministic color generation, isomorphic to Gay.jl.

### multiverse
Vault-only prediction market with FA claim tokens:
- `split` - Lock APT → create FA claims
- `merge` - Burn matched A+B → withdraw APT
- `maintain` - Reset decay clock (vestigial in Path A)
- `resolve` - Oracle declares winner
- `claim` - Winner burns FA → receives APT

## World Extractable Value (WEV)

> **Value from correct belief allocation before uncertainty collapses.**

Unlike MEV (extracting from ordering), WEV rewards:
1. **Early correct beliefs** - Positioned before collapse
2. **Sustained attention** - Maintained against decay
3. **Verified artifacts** - Reproduced by MINUS agents

### Decay Model

```
Rate:      693 bps/hour = 6.93%/hour
Half-life: ~9.6 hours
24h idle:  ~80% claim loss
```

**Intentional**: Favors continuous contribution over passive holding.

## Worldnet Ledger

**Location**: `~/.topos/GayMove/worldnet/`

### Tables

| Table | Purpose |
|-------|---------|
| `events` | Append-only log (source of truth) |
| `agent_claims` | Materialized balances (derived) |
| `worldnet_state` | Epoch, decay rate, totals |
| `bifurcations` | On-chain reference |
| `artifacts` | What agents produce |

### Operations

```bash
cd ~/.topos/GayMove/worldnet

# Status
bb decay.clj status

# Mint claims (agent artifacts)
bb decay.clj mint <agent> <role> <delta> <reason>

# Apply hourly decay
bb decay.clj decay

# Calculate payout distribution
bb decay.clj payout <vault-apt>

# Freeze before collapse
bb decay.clj freeze
```

## 26-World Integration

Each world (A-Z) participates via GF(3) triadic roles:

| Role | Trit | Action | Claim Minting |
|------|------|--------|---------------|
| **PLUS** | +1 | Generate hypotheses, traverse lattice | `MINT` on new artifact |
| **ERGODIC** | 0 | Coordinate, canonicalize | `MINT` on freeze |
| **MINUS** | -1 | Verify, reproduce, falsify | `MINT` on verification |

### World Wallet Mapping

| World | Role | Wallet |
|-------|------|--------|
| A | PLUS | `0x8699edc0960dd5b916074f1e9bd25d86fb416a8decfa46f78ab0af6eaebe9d7a` |
| B | MINUS | (see world-b skill) |
| C | ERGODIC | (see world-c skill) |
| ... | ... | ... |
| Z | PLUS | (see world-z skill) |

**Conservation**: Σ trits ≡ 0 (mod 3) across all participating worlds.

## Agent-O-Rama → Worldnet Bridge

### Artifact → Claim Flow

```python
# When PLUS agent produces artifact
def on_artifact_produced(agent_id: str, artifact_hash: str, world: str):
    role = get_world_role(world)  # PLUS/MINUS/ERGODIC
    delta = calculate_claim_value(artifact_hash)

    # Mint to worldnet
    subprocess.run([
        "bb", "decay.clj", "mint",
        agent_id, role, str(delta),
        f"artifact:{artifact_hash}"
    ])

# When MINUS agent verifies
def on_artifact_verified(agent_id: str, artifact_hash: str, world: str):
    subprocess.run([
        "bb", "decay.clj", "mint",
        agent_id, "MINUS", str(VERIFICATION_REWARD),
        f"verification:{artifact_hash}"
    ])

# When ERGODIC agent canonicalizes
def on_artifact_canonicalized(agent_id: str, artifact_hash: str, world: str):
    subprocess.run([
        "bb", "decay.clj", "mint",
        agent_id, "ERGODIC", str(CANON_REWARD),
        f"canon:{artifact_hash}"
    ])
```

### Event Schema

```sql
-- Agent event triggers mint
INSERT INTO events (epoch, agent, role, action, delta_claims, reason)
VALUES (
    current_epoch,
    'world-a',           -- agent identifier
    'PLUS',              -- GF(3) role
    'MINT',              -- action type
    1000.0,              -- claim amount
    'hypothesis:lattice-traversal-001'  -- artifact reference
);
```

## Collapse Workflow

### Phase 1: Freeze Worldnet
```bash
bb decay.clj freeze > freeze_snapshot.json
```

### Phase 2: On-Chain Resolution
```bash
aptos move run \
  --function-id 0xc793...::multiverse::resolve \
  --args address:<BIF_ADDR> bool:true \
  --profile alice-aptos

aptos move run \
  --function-id 0xc793...::multiverse::claim \
  --args address:<BIF_ADDR> u64:<amount> \
  --profile alice-aptos
```

### Phase 3: Distribution
```bash
bb decay.clj payout <VAULT_APT>
# For each agent: payout = vault_apt * claims / total_claims
```

## Invariants

1. **On-chain**: `stake_a + stake_b + accumulated_decay == total_apt_locked`
2. **Worldnet**: `sum(agent_claims) + unallocated == total_claims`
3. **Conservation**: APT never destroyed, never injected
4. **Settlement**: Exactly one collapse per bifurcation

## Files

| File | Purpose |
|------|---------|
| `~/.topos/GayMove/sources/multiverse.move` | Main contract |
| `~/.topos/GayMove/sources/gay_colors.move` | SplitMix64 RNG |
| `~/.topos/GayMove/Move.toml` | Package config |
| `~/.topos/GayMove/PATH_A.md` | Architecture docs |
| `~/.topos/GayMove/VAULT_RUNBOOK.md` | Collapse procedure |
| `~/.topos/GayMove/worldnet/ledger.duckdb` | Live ledger |
| `~/.topos/GayMove/worldnet/decay.clj` | Ledger operations |

## AIP Compliance

| AIP | Implementation |
|-----|----------------|
| **AIP-21** (Fungible Assets) | FA claim tokens via MintRef/BurnRef |
| **AIP-24** (Objects) | Bifurcation as Object with child FAs |
| **AIP-27** (Time) | `timestamp::now_seconds()` for decay |
| **AIP-41** (Signatures) | Oracle-gated resolution |

## Related Skills

- `aptos-agent` - MCP tools for Aptos interaction
- `aptos-trading` - Alpha executor trading
- `agent-o-rama` - Learning layer (artifact generation)
- `acsets` - Algebraic databases for structured data
- `gay-mcp` - GF(3) color protocol
- `bisimulation-game` - Equivalence verification
- `world-a` through `world-z` - 26 participating worlds

## Quick Reference

```bash
# Check contract
aptos move view \
  --function-id 0xc793acdec12b4a63717b001e21bbb7a8564d5e9690f80d41f556c2d0d624cc7b::multiverse::get_escrow_address \
  --profile alice-aptos

# Worldnet status
bb ~/.topos/GayMove/worldnet/decay.clj status

# Leaderboard
duckdb ~/.topos/GayMove/worldnet/ledger.duckdb "SELECT * FROM leaderboard"
```



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