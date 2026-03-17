---
name: compositional-acset-comparison
description: "Compare data structures (DuckDB, LanceDB) via ACSets with persistent homology coverage analysis and geometric morphism translation."
source: music-topos
license: MIT
xenomodern: true
ironic_detachment: 0.69
trit: 0
triangulated: 2025-12-22
---

# Compositional ACSet Comparison Skill

> *"The algorithm IS the data, the data IS the algorithm"*
> — Homoiconic Principle

**Trit**: 0 (ERGODIC - Coordinator)
**Color**: #26D826 (Green)
**Domain**: Compositional algorithm/data analysis via algebraic databases

---

## SYNOPSIS (Man Page)

```
compositional-acset-comparison - compare storage schemas via algebraic databases

USAGE:
    include("DuckDBACSet.jl")
    include("LanceDBACSet.jl")
    compare_schemas(SchDuckDB, SchLanceDB)

TOOLS:
    ComparisonUtils.jl     - 12-dimension golden spiral comparison
    GhristCoverage.jl      - Persistent homology coverage analysis
    ColoringFunctor.jl     - GF(3) coloring and 3-colorability
    GeometricMorphism.jl   - Presheaf topos translation analysis
    IrreversibleMorphisms.jl - Detect lossy morphisms
    SideBySideComparison.jl  - Visual diff tables

SEEDS:
    1000000 - Core schemas and comparison
    2000000 - Irreversibility analysis
    3000000 - Side-by-side streams
    4000000 - Ghrist/Coloring/Morphism analysis

SEE ALSO:
    acsets(7), gay-mcp(7), three-match(7), temporal-coalgebra(7)
```

---

## INFO (Quick Reference)

| Key | Value |
|-----|-------|
| **Type** | ERGODIC (0) - Coordinator |
| **Color** | #26D826 (Green) |
| **Seed** | 1000000 (core), 4000000 (analysis) |
| **Golden Angle** | 137.508° |
| **Dimensions** | 12 comparison axes |
| **Schemas** | DuckDB (10 Ob, 11 Hom), LanceDB (14 Ob, 18 Hom) |
| **Irreversible** | 0 (DuckDB), 2 (LanceDB) |
| **Coverage** | Table ↔ Table ✓, Column ↔ Column ✓ |
| **Dead Zones** | Segment, Manifest, VectorIndex |

### Quick Commands

```julia
# Full 12-dimension comparison
full_comparison()

# Coverage analysis (Ghrist)
run_coverage_analysis()

# Coloring functor with GF(3) verification
run_coloring_comparison()

# Geometric morphism (presheaf topos translation)
run_geometric_morphism_analysis()

# Reversibility statistics
reversibility_summary()
```

---

## Homoiconic Insight

In self-hosted Lisps, the boundary between data structures and algorithms dissolves:
- Code is data, data is code (homoiconicity)
- Evaluation time is phase-scoped (RED/BLUE/GREEN gadgets)
- Entanglement avoided by leaving phases open until explicitly closed
- Compositional structure preserved across algorithm ↔ data boundary

## Overview

Compare data structures and their properties (density/sparsity, dynamic/static, versioning strategies) using the richness afforded by ACSets. Uses Gay.jl-aided superrandom walks for deterministic exploration of comparison dimensions.

## Canonical Triads

```
schema-validation (-1) ⊗ compositional-acset-comparison (0) ⊗ gay-mcp (+1) = 0 ✓  [Property Analysis]
three-match (-1) ⊗ compositional-acset-comparison (0) ⊗ koopman-generator (+1) = 0 ✓  [Dynamic Traversal]
temporal-coalgebra (-1) ⊗ compositional-acset-comparison (0) ⊗ oapply-colimit (+1) = 0 ✓  [Versioning]
polyglot-spi (-1) ⊗ compositional-acset-comparison (0) ⊗ gay-mcp (+1) = 0 ✓  [Homoiconic Interop]
```

## Golden Thread Walk Dimensions

Each dimension is explored via φ-angle (137.508°) golden spiral for maximal dispersion:

| Step | Dimension | Hex Color | Hue |
|------|-----------|-----------|-----|
| 1 | Storage Hierarchy | #EE2B2B | 0° |
| 2 | Density/Sparsity | #2BEE64 | 137.51° |
| 3 | Dynamic/Static | #9D2BEE | 275.02° |
| 4 | Versioning Strategy | #EED52B | 52.52° |
| 5 | Traversal Patterns | #2BCDEE | 190.03° |
| 6 | Index Structures | #EE2B94 | 327.54° |
| 7 | Compression | #5BEE2B | 105.05° |
| 8 | Query Model | #332BEE | 242.55° |
| 9 | Embedding Support | #EE6C2B | 20.06° |
| 10 | Interoperability | #2BEEA5 | 157.57° |
| 11 | Concurrency | #DE2BEE | 295.08° |
| 12 | Memory Model | #C5EE2B | 72.59° |

## Comparison Matrix: DuckDB vs LanceDB

### Dimension 1: Storage Hierarchy (#EE2B2B)

```
DuckDB                          LanceDB
──────                          ───────
Table                           Database
  └─RowGroup (122K rows)          └─Table
      └─Column                        └─Manifest (version)
          └─Segment                       └─Fragment
              └─Block                         └─Column
                                                  └─VectorColumn
```

**ACSet Morphism Depth**:
- DuckDB: 4 levels (Table→RowGroup→Column→Segment)
- LanceDB: 5 levels (Database→Table→Manifest→Fragment→Column)

### Dimension 2: Density/Sparsity (#2BEE64)

| Property | DuckDB | LanceDB |
|----------|--------|---------|
| **Default** | Dense columnar | Dense Arrow arrays |
| **Sparse Support** | Via NULL bitmask | Via Arrow validity bitmask |
| **Vector Sparsity** | N/A | Sparse via IVF partitioning |
| **Storage Efficiency** | ALP, ZSTD compression | Lance columnar format |
| **ACSet Rep** | `DenseFinColumn` | `DenseFinColumn` with `VectorColumn` extension |

**Density Formula**:
```julia
density(acset, obj) = nparts(acset, obj) / theoretical_max(acset, obj)
# DuckDB Segment: ~2048 rows per vector batch
# LanceDB Fragment: variable, optimized for vector search
```

### Dimension 3: Dynamic/Static (#9D2BEE)

| Property | DuckDB | LanceDB |
|----------|--------|---------|
| **Schema Evolution** | ALTER TABLE | Manifest versioning |
| **Row Updates** | In-place (TRANSIENT→PERSISTENT) | Append + compaction |
| **Index Updates** | Dynamic B-Tree/ART | Rebuild IVF partitions |
| **ACSet Mutation** | `set_subpart!`, `rem_part!` | Append-only, version chains |

**State Machine**:
```
DuckDB Segment: TRANSIENT ⟷ PERSISTENT (bidirectional)
LanceDB Manifest: V1 → V2 → V3 → ... (append-only chain)
```

### Dimension 4: Versioning Strategy (#EED52B) ⭐ Lance SDK 1.0.0

**Critical Update (December 15, 2025)**: Lance SDK adopts SemVer 1.0.0

| Component | Versioning | Strategy |
|-----------|------------|----------|
| **Lance SDK** | SemVer 1.0.0 | MAJOR.MINOR.PATCH |
| **Lance File Format** | 2.1 | Binary compatibility, independent |
| **Lance Table Format** | Feature flags | Full backward compat, no linear versions |
| **Lance Namespace Spec** | Per-operation | Iceberg REST Catalog style |

**Key Insight**: Breaking SDK changes will NOT invalidate existing Lance data.

```julia
# ACSet representation of versioning strategies
@present SchVersioning(FreeSchema) begin
  SDKVersion::Ob      # SemVer (1.0.0)
  FileFormat::Ob      # Binary compat (2.1)
  TableFormat::Ob     # Feature flags
  NamespaceSpec::Ob   # Per-operation
  
  # Morphisms: SDK ≠ Format
  sdk_file::Hom(SDKVersion, FileFormat)      # Many-to-one
  file_table::Hom(FileFormat, TableFormat)   # Independent
  table_ns::Hom(TableFormat, NamespaceSpec)  # Independent
end
```

**DuckDB Versioning**:
- Temporal tables via `VERSION AT`
- Extension versioning separate from core

### Dimension 5: Traversal Patterns (#2BCDEE)

| Pattern | DuckDB | LanceDB |
|---------|--------|---------|
| **Sequential Scan** | RowGroup→Column→Segment | Fragment→Column |
| **Index Scan** | ART/B-Tree navigation | IVF partition probe |
| **Vector Search** | N/A (extension) | Centroid→Partition→Rows |
| **Time Travel** | `FOR SYSTEM_TIME AS OF` | `checkout(version)` |

**ACSet Incident Queries**:
```julia
# DuckDB: Find all segments in a column
incident(duckdb_acset, col_id, :column)

# LanceDB: Find all centroids for an index
incident(lancedb_acset, idx_id, :partition_index) |>
  flatmap(p -> incident(lancedb_acset, p, :centroid_partition))
```

### Dimension 6: Index Structures (#EE2B94)

| Index Type | DuckDB | LanceDB |
|------------|--------|---------|
| **Primary** | None (heap) | None (Lance format) |
| **Secondary** | ART (Radix Tree) | Scalar indexes |
| **Vector** | Extension (vss) | IVF_PQ, IVF_HNSW_SQ, IVF_HNSW_PQ |
| **Full-Text** | Extension (fts) | N/A |

**ACSet Index Representation**:
```julia
# LanceDB vector index hierarchy
VectorIndex → Partition → Centroid
    ↓
index_column → VectorColumn → Column
```

### Dimension 7: Compression (#5BEE2B)

| Algorithm | DuckDB | LanceDB |
|-----------|--------|---------|
| **Numeric** | ALP (Adaptive Lossless) | Arrow encoding |
| **String** | Dictionary, FSST | Dictionary |
| **General** | ZSTD, LZ4 | ZSTD |
| **Vector** | N/A | PQ (Product Quantization) |

### Dimension 8: Query Model (#332BEE)

| Aspect | DuckDB | LanceDB |
|--------|--------|---------|
| **Language** | SQL | Python/Rust API + SQL filter |
| **Optimization** | Volcano/push-based | Vector-first + filter |
| **Execution** | Vectorized (2048 batch) | Arrow RecordBatch |
| **Parallelism** | Morsel-driven | Partition-parallel |

### Dimension 9: Embedding Support (#EE6C2B)

| Feature | DuckDB | LanceDB |
|---------|--------|---------|
| **Native** | No | Yes (FixedSizeList<Float>) |
| **Generation** | UDF/Extension | EmbeddingFunction registry |
| **Storage** | ARRAY type | VectorColumn |
| **Search** | Extension (vss) | Native (IVF, HNSW) |

### Dimension 10: Interoperability (#2BEEA5)

| Format | DuckDB | LanceDB |
|--------|--------|---------|
| **Arrow** | Full support | Native (Lance = Arrow extension) |
| **Parquet** | Read/Write | Read (convert to Lance) |
| **CSV/JSON** | Read/Write | Via Arrow |
| **ACSets** | Via Tables.jl | Via Arrow → Tables.jl |

**Cross-Language (from ACSets Intertypes)**:
```julia
# Generate interoperable types
generate_module(DuckDBACSet, [PydanticTarget, JacksonTarget])
generate_module(LanceDBACSet, [PydanticTarget, JacksonTarget])
```

### Dimension 11: Concurrency (#DE2BEE)

| Aspect | DuckDB | LanceDB |
|--------|--------|---------|
| **Model** | MVCC | Optimistic (manifest-based) |
| **Writers** | Single (or WAL) | Single (append) |
| **Readers** | Unlimited concurrent | Unlimited concurrent |
| **Isolation** | Snapshot | Version snapshot |

### Dimension 12: Memory Model (#C5EE2B)

| Aspect | DuckDB | LanceDB |
|--------|--------|---------|
| **Buffer Pool** | BufferManager | Memory-mapped Arrow |
| **Eviction** | LRU | OS page cache |
| **Allocation** | Unified allocator | Arrow allocator |
| **Out-of-Core** | Automatic spill | Lazy loading |

## Interleaved 3-Stream Comparison

Using GF(3) conservation for balanced parallel analysis:

```
Stream 1 (Blue, -1): Validation/Constraints
  #31945E → #B3DA86 → #8810F2 → #2F5194 → #2452AA → #245FB4

Stream 2 (Green, 0): Coordination/Transport
  #6D59D2 → #9E2981 → #72E24F → #31C5B4 → #C04DDD → #1C8EEE

Stream 3 (Red, +1): Generation/Composition
  #E22FA7 → #E812C8 → #6F68E6 → #25D840 → #DA387F → #A82358
```

## Crystal Family Analogy

Data structures map to crystal symmetry:

| Crystal Family | Symmetry | DuckDB Analog | LanceDB Analog |
|----------------|----------|---------------|----------------|
| Cubic (#9E94DD) | Order 48 | RowGroup uniformity | Fragment uniformity |
| Hexagonal (#65F475) | Order 24 | Column types | Vector dimensions |
| Tetragonal (#E764F1) | Order 16 | Segment blocking | Partition structure |
| Orthorhombic (#2ADC56) | Order 8 | Type system | Index types |
| Monoclinic (#CD7B61) | Order 4 | Compression | Quantization |
| Triclinic (#E4338F) | Order 2 | Raw storage | Raw Arrow |

## Hierarchical Control Palette

Powers PCT cascade for harmonious comparison:

```
Level 5 (Program): "Compare DuckDB vs LanceDB"
    ↓ sets reference for
Level 4 (Transition): Dimension sequence [30° steps]
    ↓ sets reference for
Level 3 (Configuration): Property relationships
    ↓ sets reference for
Level 2 (Sensation): Individual metrics
    ↓ sets reference for
Level 1 (Intensity): Numeric values
```

Colors: #B322C0 → #D5268C → #DC3946 → #DF884A → #E0D551 → #A3E04E

## XY Model Phenomenology

At τ=0.5 (ordered phase, τ < τ_c=0.893):
- Smooth field, defects bound in pairs
- High valence, disentangled
- Antivortex at (4,3): #C33567

**Interpretation**: Both DuckDB and LanceDB are in "ordered phase" - mature, production-ready systems with well-defined structures.

## Usage

```julia
using ACSets, Catlab

# Load both schemas
include("DuckDBACSet.jl")
include("LanceDBACSet.jl")

# Compare morphism structures
compare_schemas(SchDuckDB, SchLanceDB)

# Analyze density
density_analysis = map([SchDuckDB, SchLanceDB]) do sch
  Dict(ob => sparsity_metric(sch, ob) for ob in obs(sch))
end

# Traverse with Gay.jl colors
for (i, dimension) in enumerate(DIMENSIONS)
  color = gay_color_at(1000000, i)
  analyze_dimension(dimension, color)
end
```

## Skill Files

| File | Purpose | Gay.jl Seed |
|------|---------|-------------|
| `DuckDBACSet.jl` | Schema for DuckDB storage layer | 1000000 |
| `LanceDBACSet.jl` | Schema for LanceDB vector store | 1000000 |
| `IrreversibleMorphisms.jl` | Analysis of lossy morphisms | 2000000 |
| `SideBySideComparison.jl` | Visual comparison tables | 3000000 |
| `ComparisonUtils.jl` | 12-dimension comparison utilities | 1000000 |
| `GhristCoverage.jl` | Persistent homology coverage analysis | 4000000 |
| `ColoringFunctor.jl` | Schema coloring + GF(3) verification | 4000000 |
| `GeometricMorphism.jl` | Presheaf topos translation analysis | 4000000 |

## Ghrist Persistent Homology Integration

Based on de Silva & Ghrist "Coverage in Sensor Networks via Persistent Homology":

**AM Radio Coverage Analogy**:
- Radio stations = Schema objects (Table, Column, etc.)
- Coverage radius = Morphism composability range
- Signal overlap = Translatable concepts between schemas
- Dead zones = Irreversible information loss

**Betti Numbers for Schemas**:
- β₀: Connected components (isolated subsystems)
- β₁: Coverage holes (information flow gaps)
- β₂: Enclosed voids (unreachable regions)

**Persistent Holes (never die)**:
- 🔴 `parent_manifest`: Temporal irreversibility (version chain)
- 🔴 `source_column`: Semantic irreversibility (embedding loss)

## Geometric Morphism Analysis

For presheaf topoi PSh(SchDuckDB) and PSh(SchLanceDB):

**Essential Image** (lossless translation):
- Table ↔ Table ✓
- Column ↔ Column ✓

**Partial Coverage** (lossy translation):
- RowGroup ~ Fragment
- VectorColumn → Column (loses vector semantics)

**Dead Zones** (no translation):
- Segment → ??? (DuckDB-only)
- Manifest ← ??? (LanceDB-only)
- VectorIndex ← ??? (LanceDB-only)

## DeepWiki Integration (Verified 2025-12-22)

Query repository documentation via MCP for up-to-date schema information:

```julia
# DuckDB architecture via DeepWiki
mcp__deepwiki__ask_question("duckdb/duckdb", 
    "How does RowGroup partitioning work with ColumnData?")

# LanceDB versioning via DeepWiki
mcp__deepwiki__ask_question("lancedb/lancedb", 
    "How does manifest versioning enable time travel?")

# ACSets internals via DeepWiki
mcp__deepwiki__ask_question("AlgebraicJulia/ACSets.jl", 
    "How does StructACSet implement columnar storage?")
```

### Cross-Skill Synergy

| Source Skill | Comparison Application |
|--------------|------------------------|
| **gay-mcp** (+1) | Golden thread colors for 12 dimensions |
| **three-match** (-1) | 3-colorability validation of schemas |
| **temporal-coalgebra** (-1) | Version chain analysis (Manifest→Manifest) |
| **koopman-generator** (+1) | Dynamic traversal patterns |
| **oapply-colimit** (+1) | Schema composition via colimits |
| **polyglot-spi** (-1) | Cross-language type generation |
| **sheaf-cohomology** (-1) | Local-to-global consistency |
| **persistent-homology** (-1) | Coverage hole detection |
| **acsets** (0) | Core algebraic database primitives |
| **deepwiki-mcp** (0) | Live repository documentation |

---

## Related Skills

- **acsets**: Core ACSets primitives, StructACSet internals
- **gay-mcp**: Deterministic color generation via SplitMix64
- **three-match**: Colored subgraph isomorphism for 3-SAT
- **temporal-coalgebra**: Coalgebraic observation of streams
- **persistent-homology**: Topological data analysis
- **sheaf-cohomology**: Čech cohomology for consistency
- **deepwiki-mcp**: Repository documentation via MCP
- **structured-decomp**: StructuredDecompositions.jl integration

---

## References

- [de Silva & Ghrist, Coverage via Persistent Homology](https://www2.math.upenn.edu/~ghrist/preprints/persistent.pdf)
- [Lance SDK 1.0.0 Announcement](https://lancedb.github.io/lancedb/blog/announcing-lance-sdk-1.0.0/) (December 15, 2025)
- [DuckDB Architecture](https://duckdb.org/internals/overview)
- [ACSets.jl Documentation](https://algebraicjulia.github.io/ACSets.jl/)
- [StructuredDecompositions.jl](https://github.com/AlgebraicJulia/StructuredDecompositions.jl)
- [Gay.jl Deterministic Colors](https://github.com/bmorphism/Gay.jl)
- [Bumpus, Deciding Sheaves on Presheaves](https://arxiv.org/abs/2302.00952)
