---
name: og
description: '## Overview'
---

# og - Observational Bridge Time Travel Skill

## Overview

The `og` skill maintains plurigrid fork synchronization while cherry-picking from the original (og) remote. It implements time-travel exercises through an observational bridge pattern for DuckDB buffers tracking ersatz Emacs interactions.

## Core Concepts

### Observational Bridge Type
```
OG Remote ────[cherry-pick]────→ Plurigrid Fork
     ↑                                  │
     │                                  │
  [time-travel]              [DuckDB buffer]
     │                                  │
     └──── CRDT.el sexp state ←────────┘
```

### 3-MATCH Chromatic Identity for Git Operations
- **SEED-WORLD**: Git commit SHA
- **COLOR-WORLD**: Gay.jl color from commit timestamp
- **FINGERPRINT-WORLD**: DuckDB buffer hash

### Tracked Interactions
1. **crdt.el sexp state** - Intermediate collaborative editing state
2. **Gay.jl invocations** - Color generation calls with seed/index
3. **GayMCP rewriting** - Self-modifying protocol operations

## Usage

### Cherry-Pick with Time Travel
```bash
# Fetch from og remote with color tracking
og fetch --track-colors

# Cherry-pick specific commit with DuckDB buffer
og cherry-pick <sha> --buffer-to-duckdb

# Time travel to previous state
og time-travel --to-round <drand_round>
```

### DuckDB Buffer Operations
```sql
-- Query crdt.el interaction history
SELECT * FROM crdt_sexp_buffer
WHERE session_id = current_session()
ORDER BY timestamp DESC;

-- Gay.jl color tracking
SELECT seed, index, hex_color, girard_polarity
FROM gay_color_invocations
WHERE timestamp > now() - interval '1 hour';
```

### Self-Rewriting Protocol
The skill tracks when GayMCP rewrites itself by monitoring:
- Seed state changes
- Color palette mutations
- 3-MATCH triangle verification failures

## Configuration

```json
{
  "og": {
    "remote": "og",
    "branch": "asi-skillz",
    "duckdb_path": "~/.og/time_travel.duckdb",
    "track_gay_jl": true,
    "track_crdt_el": true,
    "drand_beacon": "quicknet"
  }
}
```

## Integration with music-topos

The skill connects to the Blume-Capel ergodic random walk:
- +1 cherry-pick: Accept commit (ferromagnetic)
- -1 cherry-pick: Reject commit (antiferromagnetic)
- 0 cherry-pick: BEAVER - defer decision (vacancy)

Möbius inversion tracks the cumulative cherry-pick decisions.



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 4. Pattern Matching

**Concepts**: unification, match, segment variables, pattern

### GF(3) Balanced Triad

```
og (○) + SDF.Ch4 (+) + [balancer] (−) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch10: Adventure Game Example

### Connection Pattern

Pattern matching extracts structure. This skill recognizes and transforms patterns.
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