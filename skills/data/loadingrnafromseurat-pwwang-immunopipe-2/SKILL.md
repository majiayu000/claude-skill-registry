---
name: loadingrnafromseurat
description: Load pre-existing Seurat objects into the immunopipe pipeline instead of starting from raw count matrices via SampleInfo. This enables analysis on already processed single-cell RNA-seq data stored in Seurat R objects.
---

# LoadingRNAFromSeurat Process Configuration

## Purpose
Load pre-existing Seurat objects into the immunopipe pipeline instead of starting from raw count matrices via SampleInfo. This enables analysis on already processed single-cell RNA-seq data stored in Seurat R objects.

## When to Use
- **Starting from pre-processed Seurat objects** (RDS or qs/qs2 format) instead of raw count matrices
- **Re-analyzing existing Seurat objects** with immunopipe's downstream analysis capabilities
- **Alternative entry point** when SampleInfo is not needed for RNA data input
- **When metadata is already embedded** in the Seurat object's meta.data slot
- **When combining with TCR/BCR data** - can use LoadingRNAFromSeurat for RNA + SampleInfo for VDJ data

## Configuration Structure

### Process Enablement
```toml
[LoadingRNAFromSeurat]
cache = true
```

### Input Specification
```toml
[LoadingRNAFromSeurat.in]
# Path to Seurat object file (RDS or qs/qs2 format)
# Can be single file or array of files for multiple samples
infile = ["path/to/seurat_object.rds"]

# Alternative: can use 'srtobj' alias (same as infile)
# srtobj = ["path/to/seurat_object.rds"]
```

### Environment Variables
```toml
[LoadingRNAFromSeurat.envs]
# Whether the Seurat object is well-prepared for the pipeline
# - If true: SeuratPreparing process will be skipped
# - If false: SeuratPreparing will run for QC, normalization, integration
prepared = false

# Whether the Seurat object is already clustered
# - If true: SeuratClustering (or SeuratClusteringOfAllCells) and SeuratMap2Ref will be skipped
# - Forces 'prepared' to be true if set to true
clustered = false

# Column name in Seurat object's meta.data that contains sample identifiers
# Used to create a "Sample" column in the output
# Default is "Sample" - if meta.data already has "Sample", no action is taken
# If column exists but named differently, specify here (e.g., "orig.ident", "sample_id")
sample = "Sample"
```

## Configuration Examples

### Minimal Configuration (Single Seurat Object)
```toml
[LoadingRNAFromSeurat]
[LoadingRNAFromSeurat.in]
infile = ["path/to/sample1.rds"]
```

### Pre-processed Seurat Object (Skip Preparation)
```toml
[LoadingRNAFromSeurat]
[LoadingRNAFromSeurat.in]
infile = ["data/preprocessed_seurat.rds"]

[LoadingRNAFromSeurat.envs]
# Object already normalized, QC'd, integrated - skip SeuratPreparing
prepared = true
```

### Fully Prepared Object with Clustering
```toml
[LoadingRNAFromSeurat]
[LoadingRNAFromSeurat.in]
infile = ["data/clustered_seurat.rds"]

[LoadingRNAFromSeurat.envs]
# Object is fully prepared and clustered
# Skip both SeuratPreparing and SeuratClustering
clustered = true
# 'prepared' automatically set to true when clustered = true
```

### Custom Sample Column Mapping
```toml
[LoadingRNAFromSeurat]
[LoadingRNAFromSeurat.in]
infile = ["data/seurat_objects/sample1.rds", "data/seurat_objects/sample2.rds"]

[LoadingRNAFromSeurat.envs]
# Seurat object uses "orig.ident" column for sample names
sample = "orig.ident"
```

### Loading Multiple Seurat Objects
```toml
[LoadingRNAFromSeurat]
[LoadingRNAFromSeurat.in]
infile = [
    "data/sample1.rds",
    "data/sample2.rds",
    "data/sample3.rds"
]

[LoadingRNAFromSeurat.envs]
# Each object must have the sample column specified
# Objects will be integrated by SeuratPreparing if prepared = false
sample = "Sample"
```

### RNA + TCR Combined Analysis
```toml
# Use LoadingRNAFromSeurat for RNA data
[LoadingRNAFromSeurat]
[LoadingRNAFromSeurat.in]
infile = ["data/rna_seurat.rds"]
[LoadingRNAFromSeurat.envs]
prepared = true

# Still use SampleInfo for TCR/BCR data paths
[SampleInfo.in]
infile = ["sample_info.txt"]
# sample_info.txt should contain TCRData/BCRData columns (not RNAData)
```

## Common Patterns

### Pattern 1: Load and Start Analysis (Standard Workflow)
```toml
[LoadingRNAFromSeurat]
[LoadingRNAFromSeurat.in]
infile = ["data/seurat.rds"]

# SeuratPreparing will run for QC, normalization, integration
# SeuratClustering will run for clustering
[SeuratClustering]
[SeuratClusterStats]
```

### Pattern 2: Load and Skip to Downstream Analysis
```toml
[LoadingRNAFromSeurat]
[LoadingRNAFromSeurat.in]
infile = ["data/prepared_seurat.rds"]
[LoadingRNAFromSeurat.envs]
prepared = true  # Skip SeuratPreparing

# Jump directly to clustering and marker analysis
[SeuratClustering]
[ClusterMarkers]
[SeuratClusterStats]
```

### Pattern 3: Fully Pre-processed (Skip Preparation + Clustering)
```toml
[LoadingRNAFromSeurat]
[LoadingRNAFromSeurat.in]
infile = ["data/final_seurat.rds"]
[LoadingRNAFromSeurat.envs]
clustered = true  # Skip SeuratPreparing AND SeuratClustering

# Jump directly to downstream analyses
[CellTypeAnnotation]
[ScFGSEA]
```

### Pattern 4: TCR Analysis with Pre-processed RNA
```toml
[LoadingRNAFromSeurat]
[LoadingRNAFromSeurat.in]
infile = ["data/rna_seurat.rds"]
[LoadingRNAFromSeurat.envs]
prepared = true

# Still load TCR/BCR data
[ScRepLoading]

# Continue with TCR-specific analyses
[TOrBCellSelection]
[CDR3Clustering]
[ClonalStats]
```

### Pattern 5: Multi-sample Integration
```toml
[LoadingRNAFromSeurat]
[LoadingRNAFromSeurat.in]
infile = [
    "data/patient1.rds",
    "data/patient2.rds",
    "data/patient3.rds"
]
[LoadingRNAFromSeurat.envs]
# Each object has a "patient_id" column for sample identification
sample = "patient_id"

# SeuratPreparing will integrate multiple samples
[SeuratPreparing]
[SeuratClustering]
```

## Dependencies

### Upstream
- **None** (Entry point process)
- Can optionally work with `SampleInfo` when TCR/BCR data is present (SampleInfo provides VDJ paths)

### Downstream
- **SeuratPreparing** (if `prepared = false`)
  - Performs QC, normalization, integration of loaded Seurat objects
  - Required for standard analysis workflow
- **SeuratClustering** or **SeuratClusteringOfAllCells** (if `clustered = false`)
  - Performs clustering analysis
- **All downstream RNA analysis processes**:
  - SeuratClusterStats, ClusterMarkers, CellTypeAnnotation, SeuratMap2Ref, etc.

## Validation Rules

### File Format Requirements
- **Supported formats**: RDS (`saveRDS()` / `readRDS()`) or qs/qs2 (`qs::qsave()` / `qs::qread()`)
- **Content**: Must contain a valid Seurat object
- **File existence**: Input files must exist at specified paths
- **Sample column**: If `sample` parameter is not "Sample", the specified column must exist in `object@meta.data`

### Metadata Handling
- If `meta.data` already contains a "Sample" column and `sample = "Sample"`:
  - No modification is made (symlink created to save space)
- If `sample` column doesn't exist:
  - **Error**: Process fails with message "Sample column 'X' not found in metadata"
- If `sample` column exists with custom name (not "Sample"):
  - A new "Sample" column is created by copying from the specified column
  - Modified object is saved to output

### SampleInfo Compatibility
- **Mutually exclusive with RNAData**: Cannot use both LoadingRNAFromSeurat and RNAData column in SampleInfo
- **Compatible with TCRData/BCRData**: Can use LoadingRNAFromSeurat for RNA + SampleInfo for VDJ data paths
- **Required when**: No SampleInfo section exists AND RNA data is needed

### Environment Variable Validation
- `clustered = true` → automatically sets `prepared = true` (forced dependency)
- `sample` column must exist in Seurat object metadata
- Boolean flags accept `true`/`false` (case-insensitive in TOML)

## Troubleshooting

### Issue: "Sample column not found in metadata"
**Cause**: The specified `sample` column name doesn't exist in `object@meta.data`
**Solution**:
```toml
[LoadingRNAFromSeurat.envs]
# Check your Seurat object's metadata:
# colnames(seurat_obj@meta.data)
sample = "actual_column_name"  # Use the exact column name
```

### Issue: SeuratPreparing still running despite `prepared = true`
**Cause**: Configuration syntax error or caching issue
**Solution**:
1. Check TOML syntax (no quotes around boolean values)
2. Clear cache: `[LoadingRNAFromSeurat] cache = "force"`
3. Verify config is being loaded: `python -m immunopipe.validate_config config.toml`

### Issue: Multiple samples not being integrated
**Cause**: Sample column mapping incorrect or objects don't have the specified column
**Solution**:
```toml
[LoadingRNAFromSeurat.in]
infile = ["sample1.rds", "sample2.rds"]
[LoadingRNAFromSeurat.envs]
# Verify each object has this column before running
sample = "orig.ident"  # Common alternative to "Sample"
```

### Issue: Want to use LoadingRNAFromSeurat but also have TCR data
**Cause**: Unclear how to specify TCR data paths
**Solution**: Use both processes:
```toml
[LoadingRNAFromSeurat.in]
infile = ["rna_seurat.rds"]

[SampleInfo.in]
infile = ["sample_info.txt"]
# sample_info.txt only needs TCRData/BCRData columns (not RNAData)
```

### Issue: Symlink error when Sample column already exists
**Cause**: Trying to create symlink when file exists
**Solution**: This is handled automatically by the script - it removes existing file before creating symlink

### Issue: Want to combine LoadingRNAFromSeurat with SampleInfo metadata
**Cause**: Need additional metadata columns
**Solution**: Use `SeuratPreparing.envs.mutaters` to add columns:
```toml
[SeuratPreparing.envs]
mutaters = {
    "Condition" = "metadata$Condition",
    "Batch" = "metadata$Batch"
}
```

## Best Practices

1. **Always specify sample column**: Even if default is "Sample", explicitly set it to avoid issues
2. **Check metadata before running**: Use R to verify column names exist in `object@meta.data`
3. **Use `prepared = true` for re-analysis**: Skip unnecessary preprocessing when objects are already prepared
4. **Use `clustered = true` cautiously**: Only skip clustering if you're satisfied with existing clustering
5. **Validate configuration**: Run `python -m immunopipe.validate_config config.toml` before executing pipeline
6. **Consider file size**: Large RDS files can be slow to copy; use qs/qs2 format for better performance

## Difference from SampleInfo

| Feature | SampleInfo | LoadingRNAFromSeurat |
|---------|-----------|----------------------|
| Input format | Raw count matrices (10X, loom) | Pre-processed Seurat objects |
| Data preparation | Always requires SeuratPreparing | Optional (can skip with `prepared = true`) |
| Metadata source | Sample info text file | Embedded in Seurat object |
| Multi-sample handling | Specified in text file | Multiple input files or single multi-sample object |
| TCR/BCR data support | Provides paths for RNA + VDJ | Only RNA (use SampleInfo for VDJ) |
| Integration | Required step | Depends on `prepared` setting |

## Workflow Integration

LoadingRNAFromSeurat replaces the standard `SampleInfo → SeuratPreparing` entry point:

**Standard workflow** (raw data):
```
SampleInfo → SeuratPreparing → SeuratClustering → downstream analyses
```

**With LoadingRNAFromSeurat** (prepared data):
```
LoadingRNAFromSeurat → SeuratClustering → downstream analyses
```

**With LoadingRNAFromSeurat** (fully processed):
```
LoadingRNAFromSeurat → downstream analyses (skip SeuratClustering)
```

**With TCR data**:
```
LoadingRNAFromSeurat (RNA) + SampleInfo (VDJ paths) → ScRepLoading → TCR analyses
```
