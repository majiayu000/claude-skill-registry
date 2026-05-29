---
name: ducklake-walk
description: Ergodic random walks over DuckLake lakehouses with GF(3) triadic concurrent walkers. Society-of-mind coordination for schema exploration.
version: 1.0.0
license: MIT
metadata:
  trit: 0
  bundle: database
  agent: ergodic
---

# DuckLake Random Walk

Ergodic random walk exploration of DuckDB/DuckLake schemas with concurrent Society-of-Mind walkers. Implements PageRank-style teleportation for irreducibility and GF(3)-balanced walker coordination.

## Triadic Structure

| Stream | Trit | Role | Implementation |
|--------|------|------|----------------|
| MINUS (-1) | Validator | Constraint verification, DuckLake semantics | `duckdb-validator.sql` |
| ERGODIC (0) | Coordinator | Random walk orchestration | `ducklake-walk.clj` |
| PLUS (+1) | Generator | Concurrent walker execution | `mensi_walker.py` |

**Conservation**: Σ trits = -1 + 0 + 1 = 0 (mod 3) ✓

## Lojban Gismu Mapping

| Gismu | Meaning | Component |
|-------|---------|-----------|
| pensi | think | `PensiWalker` - individual cognition |
| jimpe | understand | `Jimpe` - shared understanding |
| djuno | know | `Djuno` - knowledge units |
| mensi | sibling | Walker siblings in society |
| gunma | group | `GunmaSociety` - collective |

## Algorithm: Ergodic Random Walk

The walk follows a Markov chain with teleportation (PageRank-style):

```
P(teleport) = 0.15  # Random restart for ergodicity
P(follow_edge) = 0.85 × (has_neighbors ? 1 : 0)
P(forced_teleport) = 1 - P(teleport) - P(follow_edge)
```

**Guarantees**:
- **Irreducibility**: All tables reachable via teleportation
- **Aperiodicity**: Random restarts break cycles
- **Ergodicity**: Unique stationary distribution exists

## Usage

### Babashka Ergodic Walker (ERGODIC stream)

```bash
# Demo mode with in-memory schema
bb ducklake-walk.clj

# With existing DuckDB file
bb ducklake-walk.clj /path/to/lakehouse.duckdb
```

### Python Society-of-Mind (PLUS stream)

```bash
# Run concurrent walkers
python mensi_walker.py

# Interactive REPL
python jimpe_repl.py
```

### DuckLake Validation (MINUS stream)

```sql
LOAD ducklake;
ATTACH 'ducklake:metadata.duckdb' AS lake (DATA_PATH './data');

-- Create walk history table
CREATE TABLE lake.main.walk_history (
    step_id INTEGER,
    from_state VARCHAR,
    to_state VARCHAR,
    trit INTEGER,
    walk_time TIMESTAMPTZ
);

-- Verify GF(3) conservation
SELECT SUM(trit) % 3 AS conservation FROM lake.main.walk_history;
-- Should return 0
```

## Output Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Coverage | >80% | Unique tables visited / total tables |
| Entropy | ~ln(N) | Shannon entropy of visit distribution |
| Edge ratio | ~38% | FK-following vs teleportation |
| GF(3) sum | 0 mod 3 | Conservation across all trits |

## Integration Points

- **duckdb-timetravel**: Snapshot versioning for walk history
- **random-walk-fusion**: Seed chaining for deterministic walks
- **gay-mcp**: Color assignment for walker visualization
- **acsets**: Algebraic database schema navigation

## Files

```
skills/ducklake-walk/
├── SKILL.md                 # This file
├── ducklake-walk.clj        # Babashka ergodic walker
├── mensi_walker.py          # Python concurrent walkers
├── jimpe_repl.py            # Interactive REPL
└── demo_interleaving.py     # Thread visualization
```

## Example Output

```
=== DuckLake Random Walk ===
GF(3) Color: ERGODIC (0) - Neutral Coordinator
Tables found: 8
Random restart probability: 0.15
Starting at: ducklake.products

Step   0: ducklake.products        (rows: 4) -> ducklake.categories [edge]
Step   1: ducklake.categories      (rows: 4) -> ducklake.products [edge]
Step   2: ducklake.products        (rows: 4) -> ducklake.users [teleport]
...

=== Ergodicity Analysis ===
Coverage: 100.0%
Edge transitions: 38.0%
Teleportations: 62.0%
Entropy: 1.994 / 2.079 (max)
Ergodic: YES
```

## GF(3) Walker Roles

```python
class GF3Trit(IntEnum):
    MINUS = -1     # Validator (cold hue 270°)
    ERGODIC = 0    # Coordinator (neutral hue 180°)
    PLUS = 1       # Generator (warm hue 30°)

# Role-specific behavior weights
PLUS:    explore=0.7, validate=0.1, synthesize=0.2
MINUS:   explore=0.2, validate=0.6, synthesize=0.2
ERGODIC: explore=0.3, validate=0.2, synthesize=0.5
```

## Related Skills

- `duckdb-timetravel` (trit: 0) - Temporal versioning
- `duckdb-ies` (trit: +1) - Interactome analytics
- `random-walk-fusion` (trit: +1) - Skill graph navigation
- `acsets` (trit: 0) - Algebraic databases



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `graph-theory`: 38 citations in bib.duckdb

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


## Forward Reference

- unified-reafference (canonical cross-agent DuckDB schema)