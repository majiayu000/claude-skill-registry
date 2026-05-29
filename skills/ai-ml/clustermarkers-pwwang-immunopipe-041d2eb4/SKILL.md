---
name: clustermarkersofallcells
description: Finds marker genes for clusters of ALL cells before T/B cell selection. This process identifies differentially expressed genes across unsupervised clusters to help identify broad cell types (T cells, B cells, Myeloid cells, NK cells, etc.) in mixed immune cell populations.
---

# ClusterMarkersOfAllCells Process Configuration

## Purpose
Finds marker genes for clusters of ALL cells before T/B cell selection. This process identifies differentially expressed genes across unsupervised clusters to help identify broad cell types (T cells, B cells, Myeloid cells, NK cells, etc.) in mixed immune cell populations.

## When to Use
- **After `SeuratClusteringOfAllCells`**: Runs on all cells before T/B selection
- **Before `TOrBCellSelection`**: Provides markers to identify which clusters are T/B cells
- **Broad cell type identification**: Distinguish major immune cell types from mixed populations
- **Mixed cell populations**: When your data contains T, B, Myeloid, NK, and other cell types
- **Initial cell typing**: First-pass identification before detailed annotation
- **Data quality check**: Verify expected cell types are present in your data

## Configuration Structure

### Process Enablement

```toml
[ClusterMarkersOfAllCells]
cache = true
```

### Input Specification

```toml
[ClusterMarkersOfAllCells.in]
srtobj = ["SeuratClusteringOfAllCells"]
# Accepts output from SeuratClusteringOfAllCells process
```

### Environment Variables

All parameters are inherited from `ClusterMarkers` and `MarkersFinder`:

```toml
[ClusterMarkersOfAllCells.envs]
# Parallel computing
ncores = 1

# Grouping (uses seurat_clusters by default)
group_by = null  # null = use Seurat::Idents() (usually "seurat_clusters")

# Statistical test parameters (passed to Seurat::FindMarkers())
test.use = "wilcox"           # wilcox (Wilcoxon), bimod, roc, t, negbinom, poisson
min.pct = 0.1                  # Only test genes detected in >=10% of cells
logfc.threshold = 0.25         # Minimum log2 fold change

# Marker filtering
sigmarkers = "p_val_adj < 0.05 & avg_log2FC > 0"  # Filter for significant markers

# Enrichment analysis
dbs = ["KEGG_2021_Human", "MSigDB_Hallmark_2020"]
enrich_style = "enrichr"       # enrichr or clusterprofiler

# Error handling
error = false                  # Don't error out if no markers found

# Visualization
marker_plots_defaults = {"order_by": "desc(avg_log2FC)"}
allmarker_plots = {"Top 10 markers of all clusters": {"plot_type": "heatmap"}}
```

## External References

### Seurat FindMarkers Parameters
- **Full reference**: https://satijalab.org/seurat/reference/findmarkers
- **Statistical tests**: `test.use` parameter
  - `"wilcox"`: Wilcoxon Rank Sum test (default, recommended)
  - `"roc"`: Receiver Operating Characteristic
  - `"t"`: Student's t-test
  - `"negbinom"`: Negative binomial (requires DESeq2)
  - `"poisson"`: Poisson test
- **Common arguments** (use `-` instead of `.` in TOML):
  - `min-pct`: Minimum detection percentage in either group
  - `logfc-threshold`: Minimum log2 fold change threshold
  - `only-pos`: Only return positive markers
  - `min-diff-pct`: Minimum difference in detection percentage

### Enrichment Databases
- **MSigDB**: https://www.gsea-msigdb.org/gsea/msigdb/
- **KEGG**: https://www.genome.jp/kegg/
- **Reactome**: https://reactome.org/
- **GO**: http://geneontology.org/

## Configuration Examples

### Minimal Configuration

```toml
[SeuratClusteringOfAllCells]
[ClusterMarkersOfAllCells]

[ClusterMarkersOfAllCells.in]
srtobj = ["SeuratClusteringOfAllCells"]
```

### Standard Marker Finding

```toml
[SeuratClusteringOfAllCells]
[ClusterMarkersOfAllCells]

[ClusterMarkersOfAllCells.in]
srtobj = ["SeuratClusteringOfAllCells"]

[ClusterMarkersOfAllCells.envs]
# Find markers for broad cell type identification
dbs = ["MSigDB_Hallmark_2020", "KEGG_2021_Human"]
sigmarkers = "p_val_adj < 0.05 & avg_log2FC > 0.25"

# Generate key visualizations
[ClusterMarkersOfAllCells.envs.marker_plots."Volcano Plot (log2FC)"]
plot_type = "volcano_log2fc"

[ClusterMarkersOfAllCells.envs.allmarker_plots."Top 10 markers of all clusters"]
plot_type = "heatmap"

[ClusterMarkersOfAllCells.envs.enrich_plots."Bar Plot"]
plot_type = "bar"
top_term = 10
```

## Common Patterns

### Pattern 1: Broad Cell Type Markers

```toml
[ClusterMarkersOfAllCells.envs]
# Optimized for distinguishing T/B/Myeloid/NK cells
min-pct = 0.1              # Require detection in >=10% of cells
logfc-threshold = 0.25     # Minimum log2 fold change
test.use = "wilcox"        # Fast and robust
sigmarkers = "p_val_adj < 0.05 & avg_log2FC > 0"

# Visualize markers to identify cell types
[ClusterMarkersOfAllCells.envs.allmarker_plots."Top 20 markers per cluster"]
plot_type = "heatmap"

# Check for expected markers in outputs
# T cells: CD3D, CD3E, CD3G, CD4, CD8A
# B cells: CD19, MS4A1 (CD20), CD79A, CD79B
# Myeloid: CD14, LYZ, FCGR3A, CD68
# NK cells: NCAM1 (CD56), KLRD1 (CD94), NKG7
```

### Pattern 2: Quick Wilcoxon for Large Datasets

```toml
[ClusterMarkersOfAllCells.envs]
# Fast analysis for large datasets (>50k cells)
ncores = 8                  # Use multiple cores
test.use = "wilcox"
min-pct = 0.15              # More stringent to reduce noise
logfc-threshold = 0.3
sigmarkers = "p_val_adj < 0.01 & avg_log2FC > 0.5"

# Skip enrichment to save time
dbs = []

# Generate only essential plots
[ClusterMarkersOfAllCells.envs.allmarker_plots."Top markers heatmap"]
plot_type = "heatmap"
```

### Pattern 3: Identify T/B Cell Clusters

```toml
[ClusterMarkersOfAllCells.envs]
# Focus on finding T and B cell markers for selection
sigmarkers = "p_val_adj < 0.05 & avg_log2FC > 1"

# Will help identify which clusters express:
# T cell markers: CD3D, CD3E, CD3G
# B cell markers: CD19, MS4A1, CD79A

[ClusterMarkersOfAllCells.envs.allmarker_plots."All markers heatmap"]
plot_type = "heatmap"
```

## Difference from ClusterMarkers

| Aspect | ClusterMarkersOfAllCells | ClusterMarkers |
|--------|--------------------------|----------------|
| **Timing** | BEFORE `TOrBCellSelection` | AFTER `TOrBCellSelection` |
| **Data Scope** | ALL cells (mixed population) | SELECTED T/B cells only |
| **Purpose** | Identify broad cell types | Fine-grained sub-clusters |
| **Typical markers** | CD3, CD19, CD14, NK markers | Activation, differentiation markers |
| **Use case** | "Which clusters are T/B/Myeloid?" | "What subtypes exist within T cells?" |
| **Upstream** | `SeuratClusteringOfAllCells` | `SeuratClustering` (post-selection) |
| **Downstream** | `TOrBCellSelection` | Cell type annotation, downstream analysis |

**Key insight**: Use `ClusterMarkersOfAllCells` when you need to separate T/B cells from other cell types. Use `ClusterMarkers` when you want to analyze sub-clusters within already-purified T or B cell populations.

## Dependencies

### Upstream Processes
- **`SeuratClusteringOfAllCells`**: Required - provides clustered object with `seurat_clusters` metadata
- **`SeuratPreparing`**: Indirect - provides normalized Seurat object
- **`SampleInfo`** or **`LoadingRNAFromSeurat`**: Entry point for data

### Downstream Processes
- **`TOrBCellSelection`**: Primary consumer - uses marker results to select T/B cells
- **`TopExpressingGenesOfAllCells`**: Optional complementary analysis

## Validation Rules

### Required Inputs
```toml
[ClusterMarkersOfAllCells.in]
srtobj = ["SeuratClusteringOfAllCells"]  # Must be specified
```

### Process Enablement
- Process automatically enabled when `SeuratClusteringOfAllCells` is in config
- No need to explicitly set `[ClusterMarkersOfAllCells]` if `SeuratClusteringOfAllCells` is enabled

### Parameter Constraints
- `test.use`: Must be one of `"wilcox"`, `"roc"`, `"t"`, `"negbinom"`, `"poisson"`
- `min-pct`: Should be between 0 and 1 (e.g., 0.1 = 10%)
- `logfc-threshold`: Numeric value (log2 scale)
- `sigmarkers`: Valid dplyr filter expression

### Common Errors
- **Missing clustering**: Ensure `SeuratClusteringOfAllCells` runs first
- **No markers found**: Adjust `sigmarkers` or `logfc-threshold` if too stringent
- **Memory issues**: Reduce `ncores` or subset data with large datasets

## Troubleshooting

### Issue: No significant markers found

**Symptoms**: Empty output directory or warning about no markers

**Solutions**:
```toml
[ClusterMarkersOfAllCells.envs]
# Less stringent thresholds
logfc-threshold = 0.1           # Lower fold change requirement
min-pct = 0.05                 # Lower detection percentage
sigmarkers = "p_val_adj < 0.1"  # More relaxed p-value

# Or check data quality
# - Are cells properly clustered?
# - Is expression matrix normalized?
# - Are there enough cells per cluster (>30 recommended)?
```

### Issue: Too many markers (slow enrichment)

**Symptoms**: Process takes very long, memory issues

**Solutions**:
```toml
[ClusterMarkersOfAllCells.envs]
# More stringent filtering
logfc-threshold = 0.5
min-pct = 0.2
sigmarkers = "p_val_adj < 0.01 & avg_log2FC > 1"

# Reduce enrichment databases
dbs = ["MSigDB_Hallmark_2020"]

# Or skip enrichment entirely
dbs = []
```

### Issue: Can't identify T/B cell clusters

**Symptoms**: Markers don't show clear T/B cell signatures

**Solutions**:
1. **Check marker gene presence**:
   ```toml
   # Verify expected markers are in your data
   # Use SeuratClusterStats to visualize:
   [SeuratClusterStats.envs.features_defaults]
   features = ["CD3D", "CD3E", "CD19", "MS4A1", "CD14", "LYZ"]
   ```

2. **Adjust clustering parameters**:
   ```toml
   [SeuratClusteringOfAllCells.envs]
   res = 0.5  # Try different resolutions (0.2-1.5)
   ```

3. **Check data quality**:
   - Are genes properly normalized?
   - Are there enough cells per cluster?
   - Is species correct (human vs mouse gene symbols)?

### Issue: Process not running

**Symptoms**: Process skipped in workflow

**Solutions**:
- Verify `SeuratClusteringOfAllCells` is in config
- Check dependencies are running correctly
- Ensure TCR data requires T/B selection (not all T cells already)

## Typical Marker Genes for Identification

| Cell Type | Positive Markers | Negative Markers |
|-----------|------------------|------------------|
| **T cells** | CD3D, CD3E, CD3G, CD4, CD8A | CD19, MS4A1, CD14 |
| **B cells** | CD19, MS4A1 (CD20), CD79A, CD79B | CD3E, CD3D, CD14 |
| **Monocytes** | CD14, LYZ, FCGR3A, S100A8 | CD3E, CD19 |
| **NK cells** | NCAM1 (CD56), KLRD1 (CD94), NKG7 | CD3E, CD19, CD14 |
| **Dendritic cells** | FCER1A, CST3 | CD3E, CD19, CD14 |
| **Megakaryocytes** | PPBP, PF4 | CD3E, CD19, CD14 |

Use these marker lists to identify which clusters correspond to which cell types in your `allmarker_plots` heatmaps.
