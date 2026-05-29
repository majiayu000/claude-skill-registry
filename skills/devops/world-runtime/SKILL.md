---
name: world-runtime
description: Firecracker microVM + Morph Infinibranch WorldRuntime for parallel verse execution. Entities branch/snapshot in <250ms.
version: 1.0.0
---


# World Runtime Skill

> *"The age of linear computing is behind us."* -- Morph Labs
> *"Verses are parallel universes corresponding to probability events."* -- Dave White, Paradigm

## Overview

**WorldRuntime** provides the execution substrate for Multiverse Finance verses via:

1. **Firecracker microVMs**: Secure, fast isolation (~125ms boot)
2. **Morph Infinibranch**: Instant branching/snapshotting (<250ms)
3. **Paradigm Verses**: Financial parallel universes with push_down/pull_up

```
                    ┌─────────────────────────────────┐
                    │         WORLD RUNTIME           │
                    │   (Firecracker + Infinibranch)  │
                    └───────────────┬─────────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
    ┌───────▼───────┐       ┌───────▼───────┐       ┌───────▼───────┐
    │  verse-nash   │       │ verse-optimal │       │  verse-chaos  │
    │   trit: -1    │       │    trit: 0    │       │   trit: +1    │
    │  prob: 0.45   │       │   prob: 0.35  │       │  prob: 0.20   │
    └───────────────┘       └───────────────┘       └───────────────┘
            │                       │                       │
            └───────────────────────┼───────────────────────┘
                                    │
                            ┌───────▼───────┐
                            │   pull_up     │
                            │  (resolution) │
                            │   WEV = PoA-1 │
                            └───────────────┘
```

## Architecture

### Layer 1: Firecracker (Isolation)

```rust
// Firecracker provides:
// - KVM-based microVMs
// - 125ms boot time
// - 5MB memory overhead
// - Minimal attack surface
// - Rate limiters for I/O

struct MicroVM {
    vcpu_count: u8,      // 1-32 vCPUs
    mem_size_mib: u32,   // Memory in MiB
    boot_source: BootSource,
    drives: Vec<Drive>,
    network_interfaces: Vec<NetworkInterface>,
}
```

### Layer 2: Infinibranch (Branching)

```python
# Morph Cloud Infinibranch provides:
# - <250ms snapshot/restore
# - Zero-overhead branching
# - Complete state preservation (memory, disk, network)
# - Unlimited parallel branches

from morphcloud import MorphSandbox

# Create base world
world = await MorphSandbox.create()
await world.execute_code("import pandas as pd; data = load_universe()")

# Snapshot at decision point
snapshot_id = await world.snapshot("pre-event")

# Branch into parallel verses
verse_nash = await MorphSandbox.create(snapshot_id=snapshot_id)
verse_optimal = await MorphSandbox.create(snapshot_id=snapshot_id)
verse_chaos = await MorphSandbox.create(snapshot_id=snapshot_id)

# Execute in parallel with GF(3) conservation
results = await asyncio.gather(
    verse_nash.execute_code("strategy = 'selfish'; evolve()"),      # -1
    verse_optimal.execute_code("strategy = 'cooperative'; evolve()"), # 0
    verse_chaos.execute_code("strategy = 'random'; evolve()"),       # +1
)
```

### Layer 3: Verses (Financial)

```solidity
// Paradigm Multiverse Finance
// Verses partition the outcome space

struct Verse {
    bytes32 verseId;
    bytes32 parentId;
    bytes32[] children;
    uint256 probability;  // Fixed-point probability
    bool resolved;
    bool outcome;         // true = verse exists, false = verse collapsed
}

// Multiverse Map: verse -> owner -> balance
mapping(bytes32 => mapping(address => uint256)) public multiverseMap;

// Operations
function pushDown(bytes32 parent, bytes32[] calldata children) external;
function pullUp(bytes32[] calldata children, bytes32 parent) external;
```

## GF(3) Triads

```
ramanujan-expander (-1) ⊗ world-extractable-value (0) ⊗ world-runtime (+1) = 0 ✓  [Core]
three-match (-1) ⊗ world-hopping (0) ⊗ world-runtime (+1) = 0 ✓  [Branching]
polyglot-spi (-1) ⊗ mdm-cobordism (0) ⊗ world-runtime (+1) = 0 ✓  [Cobordism]
shadow-goblin (-1) ⊗ chromatic-walk (0) ⊗ world-runtime (+1) = 0 ✓  [Tracing]
temporal-coalgebra (-1) ⊗ acsets (0) ⊗ world-runtime (+1) = 0 ✓  [State]
```

## Implementation

### Babashka

```clojure
(ns world-runtime
  (:require [babashka.http-client :as http]
            [cheshire.core :as json]))

(def MORPH_API_KEY (System/getenv "MORPH_API_KEY"))

(defn create-world
  "Create a new world (Infinibranch sandbox)"
  [config]
  (let [resp (http/post "https://api.cloud.morph.so/v1/sandboxes"
               {:headers {"Authorization" (str "Bearer " MORPH_API_KEY)
                          "Content-Type" "application/json"}
                :body (json/generate-string config)})]
    (json/parse-string (:body resp) true)))

(defn snapshot-world
  "Snapshot current world state (<250ms)"
  [world-id name]
  (let [resp (http/post (str "https://api.cloud.morph.so/v1/sandboxes/" world-id "/snapshots")
               {:headers {"Authorization" (str "Bearer " MORPH_API_KEY)}
                :body (json/generate-string {:name name})})]
    (:snapshot_id (json/parse-string (:body resp) true))))

(defn branch-world
  "Branch from snapshot into new verse"
  [snapshot-id verse-name trit]
  (let [world (create-world {:snapshot_id snapshot-id
                              :metadata {:verse verse-name
                                         :trit trit}})]
    {:world-id (:id world)
     :verse verse-name
     :trit trit}))

(defn push-down
  "Split world into parallel verses (GF(3) balanced)"
  [world-id]
  (let [snapshot-id (snapshot-world world-id "pre-split")]
    {:verse-nash (branch-world snapshot-id "nash" -1)
     :verse-optimal (branch-world snapshot-id "optimal" 0)
     :verse-chaos (branch-world snapshot-id "chaos" +1)
     :gf3-sum 0}))

(defn execute-in-verse
  "Execute code in a verse"
  [world-id code]
  (let [resp (http/post (str "https://api.cloud.morph.so/v1/sandboxes/" world-id "/execute")
               {:headers {"Authorization" (str "Bearer " MORPH_API_KEY)}
                :body (json/generate-string {:code code})})]
    (json/parse-string (:body resp) true)))

(defn pull-up
  "Resolve verses and extract WEV"
  [verses oracle-result]
  (let [winning-verse (case oracle-result
                        :nash (:verse-nash verses)
                        :optimal (:verse-optimal verses)
                        :chaos (:verse-chaos verses))
        losing-verses (remove #(= % winning-verse) (vals verses))
        wev (reduce + (map :balance losing-verses))]
    {:winner winning-verse
     :wev wev
     :collapsed (map :verse losing-verses)}))
```

### DuckDB Schema

```sql
-- WorldRuntime entities
CREATE TABLE IF NOT EXISTS world_runtime_entities (
  entity_id VARCHAR PRIMARY KEY,
  entity_type VARCHAR NOT NULL,  -- 'microvm', 'sandbox', 'verse'
  parent_id VARCHAR,
  snapshot_id VARCHAR,
  trit INT CHECK (trit IN (-1, 0, 1)),
  state VARCHAR DEFAULT 'running',  -- 'running', 'snapshotted', 'collapsed'
  memory_mib INT,
  vcpu_count INT,
  boot_time_ms FLOAT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  resolved_at TIMESTAMP
);

-- Branching events
CREATE TABLE IF NOT EXISTS world_branches (
  branch_id VARCHAR PRIMARY KEY,
  parent_entity_id VARCHAR REFERENCES world_runtime_entities(entity_id),
  child_entity_ids VARCHAR[],  -- Array of child entity IDs
  branch_type VARCHAR,  -- 'push_down', 'fork', 'snapshot'
  snapshot_time_ms FLOAT,
  gf3_sum INT,
  branched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Verse resolutions
CREATE TABLE IF NOT EXISTS verse_resolutions (
  resolution_id VARCHAR PRIMARY KEY,
  verses VARCHAR[],  -- Participating verse IDs
  winning_verse VARCHAR,
  oracle_source VARCHAR,
  wev_extracted FLOAT,
  pull_up_time_ms FLOAT,
  resolved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance metrics
CREATE TABLE IF NOT EXISTS runtime_metrics (
  metric_id VARCHAR PRIMARY KEY,
  entity_id VARCHAR REFERENCES world_runtime_entities(entity_id),
  boot_time_ms FLOAT,
  snapshot_time_ms FLOAT,
  branch_time_ms FLOAT,
  memory_overhead_mb FLOAT,
  measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Performance Characteristics

| Operation | Firecracker | Infinibranch | Combined |
|-----------|-------------|--------------|----------|
| Boot/Create | ~125ms | ~250ms | ~250ms* |
| Snapshot | N/A | <250ms | <250ms |
| Branch | Clone (~seconds) | <250ms | <250ms |
| Memory Overhead | ~5MB | Variable | ~5MB base |
| Isolation | KVM + seccomp | Full VM | Hardware + VM |

*Infinibranch uses pre-warmed Firecracker pools

## Comparison: Traditional vs WorldRuntime

| Aspect | Traditional VMs | WorldRuntime |
|--------|-----------------|--------------|
| Boot Time | 2-3 minutes | <250ms |
| Branching | Full clone | Zero-overhead |
| State Preservation | Manual snapshots | Instant any-point |
| Parallel Exploration | Resource duplication | Native support |
| Financial Primitives | None | Verses + WEV |

## Integration with Existing Skills

### With world-extractable-value (trit: 0)

```clojure
;; WEV extraction via WorldRuntime
(defn extract-wev [seed]
  (let [worlds (push-down (create-world {:seed seed}))
        ;; Execute different strategies in parallel
        _ (execute-in-verse (:world-id (:verse-nash worlds))
                            "strategy = 'selfish'")
        _ (execute-in-verse (:world-id (:verse-optimal worlds))
                            "strategy = 'cooperative'")
        ;; Oracle determines outcome
        oracle-result :optimal
        ;; Pull up and extract
        result (pull-up worlds oracle-result)]
    {:wev (:wev result)
     :winner (:winner result)}))
```

### With chromatic-walk (trit: 0)

```clojure
;; 3-agent chromatic walk across verses
(defn chromatic-verse-walk [seed]
  (let [worlds (push-down (create-world {:seed seed}))]
    ;; Generator (+1) in chaos verse
    (execute-in-verse (:world-id (:verse-chaos worlds))
                      "generate_proposals()")
    ;; Coordinator (0) in optimal verse
    (execute-in-verse (:world-id (:verse-optimal worlds))
                      "coordinate_proposals()")
    ;; Validator (-1) in nash verse
    (execute-in-verse (:world-id (:verse-nash worlds))
                      "validate_proposals()")))
```

## Commands

```bash
# WorldRuntime operations
just world-runtime-create     # Create new world
just world-runtime-snapshot   # Snapshot current state
just world-runtime-branch     # Branch into 3 verses
just world-runtime-push-down  # push_down operation
just world-runtime-pull-up    # pull_up with oracle
just world-runtime-metrics    # Performance metrics

# Query runtime entities
just world-runtime-entities   # List all entities
just world-runtime-branches   # Branch history
just world-runtime-resolutions # Resolution history
```

## Future: Monad Parallel Execution

For on-chain verse execution, Monad's optimistic parallel execution provides:

- Identical block semantics to Ethereum
- Parallel transaction execution
- Automatic re-execution on conflicts
- Perfect for verse state transitions

```
Monad Block = [Tx1, Tx2, Tx3, ...]
             = verse_nash || verse_optimal || verse_chaos
             = GF(3) balanced execution
```

## References

1. **AWS Firecracker (2018)** -- "Lightweight virtualization for serverless"
2. **Morph Labs (2025)** -- "Infinibranch Sandboxes"
3. **Paradigm/Dave White (2025)** -- "Multiverse Finance"
4. **Monad (2025)** -- "Parallel Execution Documentation"
5. **KVM** -- Linux Kernel-based Virtual Machine

## See Also

- [world-extractable-value](../world-extractable-value/SKILL.md) - WEV calculation
- [world-hopping](../world-hopping/SKILL.md) - Badiou triangle traversal
- [chromatic-walk](../chromatic-walk/SKILL.md) - 3-agent exploration
- [mdm-cobordism](../mdm-cobordism/SKILL.md) - State cobordisms



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