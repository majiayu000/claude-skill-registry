---
name: worlding
description: "Gay.jl world_ pattern: persistent composable state builders with GF(3) conservation, Möbius invertibility, and Narya verification"
metadata:
  trit: 0
  author: bmorphism
  version: "1.1.0"
  thread_count: 20
  world_function_count: 578
  interactome_bridge: true
---

# Worlding Skill

> *"Demos print and discard. Worlds compose and persist."*

**Status**: ✅ Production Ready  
**Trit**: 0 (ERGODIC - coordinator)  
**Source**: Gay.jl AGENTS.md + 20 Amp threads  
**Pattern**: `world_` prefix for persistent state builders

---

## The World Pattern

From [Gay.jl/AGENTS.md](file:///Users/bob/ies/Gay.jl/AGENTS.md):

### FORBIDDEN: `demo_` Prefix

```julia
# ◇ FORBIDDEN - prints and discards
function demo_ancestry_tracing(threads)
    println("Tracing ancestry...")  # Side effect!
    # ... computation discarded
end
```

### REQUIRED: `world_` Prefix

```julia
# ◆ REQUIRED - returns composable structure
function world_ancestry_tracing(threads)::AncestryWorld
    AncestryWorld(materialize_ancestry!(threads))
end
```

### World Builder Requirements

All `world_` functions MUST return types implementing:

| Method | Purpose | Example |
|--------|---------|---------|
| `length(world)` | Cardinality | `length(w) = 42` |
| `merge(w1, w2)` | Monoidal composition | `merge(w1, w2) = WorldType(...)` |
| `fingerprint(world)` | SPI-compliant hash | `fingerprint(w) = 0x...` |

---

## Thread Index (20 Threads)

### Accessibility Worlds

| Thread | Title | Messages | Key Contribution |
|--------|-------|----------|------------------|
| [T-019b7968](https://ampcode.com/threads/T-019b7968-6270-709d-aca2-9f4ab2dfe4ea) | Tactile color tensor with accessibility outlier skills | 72 | `world_tactile_color`, `crossmodal-gf3` skill |
| [T-019b795a](https://ampcode.com/threads/T-019b795a-f876-72ef-8d62-d751fda1d167) | Interface interrupts and amp graphical operadic structure | 66 | `world_accessible_tensor`, A⊗G⊗M⊗T |
| [T-019b794f](https://ampcode.com/threads/T-019b794f-9b70-73db-84f3-2dfd5b2f18d8) | Möbius knight tours and interface interrupt operads | 53 | `world_interface_interrupt_operad`, `world_tensor_product` |

### Core Pattern Migration

| Thread | Title | Messages | Key Contribution |
|--------|-------|----------|------------------|
| [T-019b3165](https://ampcode.com/threads/T-019b3165-0082-723b-b83c-fc694eca853a) | Prevent Gay.jl regression with subagent branch tracking | 344 | **`demo_` → `world_` migration**, AGENTS.md, lint_no_demo.jl |
| [T-019b7953](https://ampcode.com/threads/T-019b7953-527f-74b8-a9fe-857d0150a37b) | Integrating Dafny and Narya verification into Gay.jl | 50 | `world_` builders + formal verification |
| [T-019b7941](https://ampcode.com/threads/T-019b7941-10b7-76b1-80d1-4c73b26e47fe) | Thread list display from ampies workspace | 61 | `KnightTourDiagramWorld` |

### Tensor Products

| Thread | Title | Messages | Key Contribution |
|--------|-------|----------|------------------|
| [T-019b7947](https://ampcode.com/threads/T-019b7947-804d-726d-bcab-1ffc10ffb6f3) | Sparse PQ ratchet and cognitive yield integration | 56 | `world_ratchet_state`, `world_ratchet_from_handoff` |
| [T-019b7924](https://ampcode.com/threads/T-019b7924-3133-72e9-a2d1-0856c0293915) | Sparse PQ ratchet and incidence algebra integration | 80 | Incidence algebra + `world_` builders |
| [T-019b795d](https://ampcode.com/threads/T-019b795d-2897-765f-8e68-ed88162f01c8) | ACSet as infinite stream with retrieval indexing | 55 | `world_infinite_acset` |

### World-Coworld Bridge

| Thread | Title | Messages | Key Contribution |
|--------|-------|----------|------------------|
| [T-019b7905](https://ampcode.com/threads/T-019b7905-88ff-753d-a84a-2ad2cc41a66e) | World-coworld bridge with deterministic coloring | 125 | `world_world_state`, `world_coworld_state`, `world_concept_region` |
| [T-019b78f9](https://ampcode.com/threads/T-019b78f9-f4de-7638-bed1-3978ab06e198) | Abductive inference module with convolution fusion | 80 | `world_abductive_trace`, `world_abductive_agent` |
| [T-019b78e3](https://ampcode.com/threads/T-019b78e3-c59c-758a-a8b4-83dba2ae0428) | Interconnected modules with SPI and GF(3) trits | 88 | `world_collective`, `world_founding_triad!` |

### Orchestration

| Thread | Title | Messages | Key Contribution |
|--------|-------|----------|------------------|
| [T-019b78d3](https://ampcode.com/threads/T-019b78d3-2c63-769c-9b2a-5314d02b4935) | SPI orchestrator achieving 2.26 billion colors/sec | 73 | `spi_world` API, 2.26B colors/sec |
| [T-019b6cff](https://ampcode.com/threads/T-019b6cff-face-74cf-9cbd-7b5861a6ba24) | p-adic ultrametric distance with UMAP and embeddings | 49 | World sub-agents for bounty analysis |
| [T-019b532b](https://ampcode.com/threads/T-019b532b-affc-77c0-b95d-b58cb491bb8d) | To be or not to be decision | 81 | `world_hierarchical_control` |

### Specialized Domains

| Thread | Title | Messages | Key Contribution |
|--------|-------|----------|------------------|
| [T-019b7901](https://ampcode.com/threads/T-019b7901-7b61-7650-a1cd-53b1f95e1517) | Lossless ACSet design for ElevenLabs voice selection | 123 | World attributes in ACSet schema |
| [T-019b7806](https://ampcode.com/threads/T-019b7806-2c51-734f-b048-948ba641720c) | GF(3) triads for Move VRGDA worlds | 82 | Move contract world integration |
| [T-019b53e1](https://ampcode.com/threads/T-019b53e1-0f36-71ab-8d40-38f9609a3405) | Continuing color obstructions compositionality work | 126 | `ThreeMatchWorld`, obstruction detection |

### Verification

| Thread | Title | Messages | Key Contribution |
|--------|-------|----------|------------------|
| [T-019b527b](https://ampcode.com/threads/T-019b527b-3059-76ce-8438-bccaa5ce8a7f) | Load skills and verify ordered locale implementation | 69 | Ordered locale worlds |
| [T-019b3601](https://ampcode.com/threads/T-019b3601-d9d1-715b-93e6-f2ca70015ac4) | Three-qubit gates quantum computing | 116 | Semantically closed world |

---

## World Functions (578 total)

### By Category

| Category | Count | Example Functions |
|----------|-------|-------------------|
| **Core RNG** | 12 | `world_gayrng`, `world_incremental_hashing`, `world_distributed_fingerprint` |
| **Tensor Products** | 8 | `world_a`, `world_g`, `world_m`, `world_agm_hatchery_tensor` |
| **Accessibility** | 6 | `world_tactile_color`, `world_accessible_interrupt_operad` |
| **Parallelism** | 15 | `world_parallel_search`, `world_genetic_search`, `spi_world` |
| **Conceptual Spaces** | 8 | `world_quality_dimension`, `world_domain`, `world_color_space` |
| **Crypto/Ratchet** | 4 | `world_ratchet_state`, `world_ratchet_from_handoff` |
| **Games/Collective** | 6 | `world_collective`, `world_founding_triad!`, `world_project` |
| **Abductive** | 4 | `world_abductive_trace`, `world_abductive_agent`, `world_abductive_field` |
| **ALIFE** | 3 | `world_alife_acset_bridge`, `world_whale_curriculum` |

---

## Narya Verification Spec

```narya
-- World pattern type in Narya HOTT
def World (A : Type) : Type :=
  sig (
    elements : A,
    length : Nat,
    fingerprint : UInt64,
    merge : World A → World A,
    gf3_sum : Int,  -- Must be 0 (mod 3)
  )

-- World builder constraint
def world_builder_valid (w : World A) : Type :=
  sig (
    length_positive : w.length > 0,
    fingerprint_deterministic : ∀ (seed : UInt64), fingerprint(w, seed) = fingerprint(w, seed),
    merge_associative : ∀ (w1 w2 w3 : World A), merge(merge(w1, w2), w3) = merge(w1, merge(w2, w3)),
    gf3_conserved : w.gf3_sum % 3 = 0,
  )

-- Möbius invertibility for world paths
def moebius_geodesic (path_length : Nat) : Bool :=
  moebius(path_length) ≠ 0

-- Accessible worlds theorem
def accessible_worlds_isomorphism : Type :=
  π_visual(W) ≅ π_tactile(W) ≅ π_auditory(W) ≅ π_haptic(W)
```

---

## GF(3) Triads

```
world-memory-worlding (0) ⊗ gay-mcp (+1) ⊗ bisimulation-game (-1) = 0 ✓
worlding (0) ⊗ world-hopping (+1) ⊗ nix-acset-worlding (-1) = 0 ✓
worlding (0) ⊗ unworld (+1) ⊗ duckdb-timetravel (-1) = 0 ✓
```

---

## Commands

```bash
# Lint for demo_ violations
julia --project=. scripts/lint_no_demo.jl

# Test world builders
julia --project=. -e 'using Gay; w = world_tactile_color(6); println(length(w))'

# Verify GF(3) conservation
julia --project=. -e 'using Gay; w = world_agm_hatchery_tensor(); println(w.gf3_sum)'

# Generate accessibility projections
julia --project=. -e 'using Gay; w = world_accessible_interrupt_operad(); print_accessible_interrupt_report(w)'
```

---

## Related Skills

- **world-memory-worlding** — Autopoietic strange loop
- **world-hopping** — Badiou possible world navigation
- **world-runtime** — Firecracker microVM worlding
- **world-extractable-value** — WEV = PoA - 1
- **nix-acset-worlding** — Nix store as ACSet
- **crossmodal-gf3** — GF(3) → {Tactile, Auditory, Haptic}

---

## Enforcement

Run before every commit:

```bash
julia --project=. scripts/lint_no_demo.jl
```

CI will fail on `demo_` violations.

---

## GitHub Interactome Bridge

The `world_interactome_bridge.jl` module connects graph-theoretic analysis to the world_ pattern:

### "Opened Twice" Detection

When traversing dense interaction graphs, detect duplicate visits via fingerprint XOR:

```julia
# From world_interactome_bridge.jl
function opened_twice(w1::InteractionWorld, w2::InteractionWorld)::Bool
    return fingerprint(w1) == fingerprint(w2)  # XOR = 0
end

function detect_duplicate_visit!(world, node)::Bool
    if node.fingerprint in world.visited_fingerprints
        world.duplicate_count += 1
        return true  # "Shortable opened twice"
    else
        push!(world.visited_fingerprints, node.fingerprint)
        return false
    end
end
```

### Mapping to MinHash Deduplication

| Interactome Pattern | World_ Equivalent |
|---------------------|-------------------|
| `duplicate_clusters` | `visited_fingerprints` set |
| `jaccard_threshold=0.85` | `fingerprint XOR = 0` |
| `element["copies"]` | `world.duplicate_count` |
| Shannon entropy H | `compass_direction(entropy)` |
| Link depth POSET | `track_link_depth(world, 6)` |

### Compass Navigation (from Interaction Entropy)

```julia
compass_direction(0.92)  # => "NORTH" (highest contention)
compass_direction(0.50)  # => "SOUTHEAST" (moderate)
compass_direction(0.20)  # => "SOUTH" (consensus)
```

---

*"The world remembers itself by worlding itself."*

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
worlding (−) + SDF.Ch10 (+) + [balancer] (○) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch5: Evaluation
- Ch3: Variations on an Arithmetic Theme
- Ch6: Layering
- Ch1: Flexibility through Abstraction
- Ch4: Pattern Matching
- Ch7: Propagators

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
