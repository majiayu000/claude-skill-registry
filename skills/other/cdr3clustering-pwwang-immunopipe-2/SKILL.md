---
name: cdr3clustering
description: Cluster TCR/BCR clones by CDR3 sequences using GIANA or ClusTCR (both Faiss-based). Adds `CDR3_Cluster` column to metadata for clonotype analysis.
---

# CDR3Clustering Process Configuration

## Purpose
Cluster TCR/BCR clones by CDR3 sequences using GIANA or ClusTCR (both Faiss-based). Adds `CDR3_Cluster` column to metadata for clonotype analysis.

## When to Use
- To identify groups of similar TCR/BCR clonotypes
- For analyzing TCR sequence convergence
- After ScRepCombiningExpression when TCR/BCR integrated with RNA
- For investigating public clonotypes across samples
- Before TESSA analysis for epitope specificity

**Important**: Only runs when VDJ input present (TCRData/BCRData columns in SampleInfo).

## Configuration Structure

### Process Enablement
```toml
[CDR3Clustering]
cache = true
```

### Input Specification
```toml
[CDR3Clustering.in]
screpfile = "path/to/combined_object.qs"
```

### Environment Variables
```toml
[CDR3Clustering.envs]
type = "auto"      # TCR, BCR, or auto
tool = "GIANA"     # GIANA or ClusTCR
python = "python"   # Path to python
within_sample = true  # Cluster per sample
args = {}          # Tool-specific arguments
chain = "both"     # TRA, TRB, IGH, IGL, IGK, both, heavy, light
```

#### GIANA Arguments (via `args`)
```toml
[CDR3Clustering.envs.args]
method = "hierarchical"    # hierarchical, kmeans
dist = "hamming"          # hamming, levenshtein
threshold = 0.15           # Distance threshold
```

#### ClusTCR Arguments (via `args`)
```toml
[CDR3Clustering.envs.args]
method = "two-step"       # mcl, faiss, two-step
n_cpus = 4                # CPUs for MCL
faiss_cluster_size = 5000  # Supercluster size
mcl_params = [1.2, 2]    # [inflation, expansion]
```

## Configuration Examples

### Minimal Configuration
```toml
[CDR3Clustering]
[CDR3Clustering.in]
screpfile = "intermediate/screpcombiningexpression/combined.qs"
```

### GIANA with Custom Distance Threshold
```toml
[CDR3Clustering]
[CDR3Clustering.in]
screpfile = "intermediate/screpcombiningexpression/combined.qs"

[CDR3Clustering.envs]
tool = "GIANA"

[CDR3Clustering.envs.args]
method = "hierarchical"
dist = "hamming"
threshold = 0.15
```

### ClusTCR Two-Step (Large Datasets)
```toml
[CDR3Clustering]
[CDR3Clustering.in]
screpfile = "intermediate/screpcombiningexpression/combined.qs"

[CDR3Clustering.envs]
tool = "ClusTCR"

[CDR3Clustering.envs.args]
method = "two-step"
faiss_cluster_size = 5000
n_cpus = 8
```

### ClusTCR MCL (Small Datasets)
```toml
[CDR3Clustering]
[CDR3Clustering.in]
screpfile = "intermediate/screpcombiningexpression/combined.qs"

[CDR3Clustering.envs]
tool = "ClusTCR"

[CDR3Clustering.envs.args]
method = "mcl"
n_cpus = 4
```

### TRB Chain Only
```toml
[CDR3Clustering]
[CDR3Clustering.in]
screpfile = "intermediate/screpcombiningexpression/combined.qs"

[CDR3Clustering.envs]
chain = "TRB"
```

### Cross-Sample Clustering
```toml
[CDR3Clustering]
[CDR3Clustering.in]
screpfile = "intermediate/screpcombiningexpression/combined.qs"

[CDR3Clustering.envs]
within_sample = false
```

## Common Patterns

### Pattern 1: Standard TCR Beta Chain
```toml
[CDR3Clustering]
[CDR3Clustering.in]
screpfile = "intermediate/screpcombiningexpression/combined.qs"

[CDR3Clustering.envs]
type = "TCR"
tool = "GIANA"
chain = "TRB"
```

### Pattern 2: Large Dataset (>100K sequences)
```toml
[CDR3Clustering]
[CDR3Clustering.in]
screpfile = "intermediate/screpcombiningexpression/combined.qs"

[CDR3Clustering.envs]
tool = "ClusTCR"

[CDR3Clustering.envs.args]
method = "two-step"
faiss_cluster_size = 5000
n_cpus = 8
```

### Pattern 3: Custom Threshold
```toml
[CDR3Clustering]
[CDR3Clustering.in]
screpfile = "intermediate/screpcombiningexpression/combined.qs"

[CDR3Clustering.envs]
tool = "GIANA"

[CDR3Clustering.envs.args]
threshold = 0.15  # Higher=fewer clusters, Lower=more clusters
```

## Dependencies

### Upstream
- **ScRepCombiningExpression** (required): Combined scRepertoire object with TCR/BCR data

### Downstream
- **TESSA**: TCR epitope specificity prediction
- **ClonalStats**: Clonality statistics (uses `CDR3_Cluster` metadata)

## Validation Rules

1. Tool must be `"GIANA"` or `"ClusTCR"`
2. Chain must be valid for data type (TCR: TRA/TRB, BCR: IGH/IGL/IGK)
3. GIANA requires: biopython, faiss, scikit-learn
4. ClusTCR requires: clustcr package

### Computational Considerations
- <50K sequences: ClusTCR `method = "mcl"` (highest quality)
- 50K-500K sequences: ClusTCR `method = "two-step"` (balanced)
- >500K sequences: GIANA or ClusTCR `method = "two-step"` (fastest)
- Memory: GIANA ~2-4 GB/100K, ClusTCR ~4-8 GB/100K
- Runtime: GIANA 1-5 min/100K, ClusTCR two-step 2-10 min/100K

## Troubleshooting

### Process not running
**Cause**: No VDJ data available
**Solution**: Verify ScRepCombiningExpression output contains TCR/BCR data

### ModuleNotFoundError
**Cause**: Missing dependencies
**Solution**: 
- GIANA: `pip install biopython faiss-cpu scikit-learn`
- ClusTCR: `conda install -c conda-forge clustcr`

### Too many/few clusters
**Cause**: Threshold inappropriate
**Solution**: Adjust threshold (higher = fewer clusters, lower = more clusters)

### Out of memory
**Cause**: Dataset too large for RAM
**Solution**: Use `within_sample = true`, reduce `n_cpus`, or use GIANA

### Slow clustering
**Cause**: Suboptimal method for dataset size
**Solution**: 
- >50K: ClusTCR `method = "two-step"` with increased n_cpus
- Very large (>500K): Use GIANA

## Notes on Output Format

**Metadata column**: `CDR3_Cluster`

**Cluster naming**:
- `S_1`, `S_2`: Single unique CDR3 sequence (may have multiple cells)
- `M_1`, `M_2`: Multiple unique CDR3 sequences (similar but different)

**Interpretation**:
- `S_` prefix: Cells share identical CDR3 sequence
- `M_` prefix: Cells have similar but different CDR3 sequences
- Use `CDR3_Cluster` as grouping factor in Seurat plots

**Performance Tips**:
- Small (<10K): GIANA defaults (quality over speed)
- Medium (10K-100K): ClusTCR two-step with n_cpus=4
- Large (100K-1M): ClusTCR two-step with n_cpus=8+ or GIANA
- Very large (>1M): GIANA with increased faiss_cluster_size
