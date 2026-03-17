---
name: torbcellselection
description: Separates T and non-T cells or B and non-B cells from a mixed cell population. Uses either clonotype percentage from VDJ data, indicator gene expression (CD3 markers for T cells, CD19/CD20 for B cells), custom selector expressions, or k-means clustering for automatic selection.
---

# TOrBCellSelection Process Configuration

## Purpose
Separates T and non-T cells or B and non-B cells from a mixed cell population. Uses either clonotype percentage from VDJ data, indicator gene expression (CD3 markers for T cells, CD19/CD20 for B cells), custom selector expressions, or k-means clustering for automatic selection.

## When to Use
- When dataset contains mixed cell types (T cells + other cell types, or B cells + other cell types)
- Before TCR-specific or BCR-specific analysis to isolate relevant cells
- After `SeuratClusteringOfAllCells` to identify which clusters are T/B cells
- When scRNA-seq data includes scTCR-seq or scBCR-seq data
- **DO NOT use** if all cells in your dataset are already T/B cells

## Configuration Structure

### Process Enablement
```toml
[TOrBCellSelection]
cache = true  # Enable caching for this process
```

### Input Specification
```toml
[TOrBCellSelection.in]
# Seurat object file (RDS/qs2 format) from SeuratClusteringOfAllCells
srtobj = ["SeuratClusteringOfAllCells"]

# Optional: Immune repertoire data file (RDS/qs2 format) from ScRepLoading
# Required unless ignore_vdj is set to true
immdata = ["ScRepLoading"]
```

### Environment Variables
```toml
[TOrBCellSelection.envs]
# Whether to ignore VDJ information and use only marker gene expression
ignore_vdj = false

# Custom R expression to identify T/B cells
# Example: "Clonotype_Pct > 0.25" selects cells with >25% clonotype percentage
# Can use indicator genes: "Clonotype_Pct > 0.25 & CD3E > 0"
# If not provided, k-means clustering will be used
selector = null

# List of indicator genes for T/B cell identification
# For T cells: ["CD3E", "CD3D", "CD3G"] (positive markers)
#             or include negative markers: ["CD3E", "CD19", "CD14"]
# For B cells: ["CD19", "MS4A1", "CD79A", "CD79B"]
indicator_genes = ["CD3E"]

# Parameters for k-means clustering (if selector not provided)
# Reference: https://rdrr.io/r/stats/kmeans.html
# Note: dots in argument names should be replaced with hyphens
kmeans = {"nstart": 25}
```

## Configuration Examples

### Minimal Configuration (Default T Cell Markers)
```toml
[TOrBCellSelection]
[TOrBCellSelection.in]
srtobj = ["SeuratClusteringOfAllCells"]
```
**What this does**: Uses default CD3E marker + k-means clustering with VDJ data to automatically select T cell clusters.

### T Cell Selection with Multiple CD3 Markers
```toml
[TOrBCellSelection]
[TOrBCellSelection.in]
srtobj = ["SeuratClusteringOfAllCells"]
immdata = ["ScRepLoading"]

[TOrBCellSelection.envs]
# Use all three CD3 markers for robust T cell identification
indicator_genes = ["CD3E", "CD3D", "CD3G"]
```

### B Cell Selection (Default Markers)
```toml
[TOrBCellSelection]
[TOrBCellSelection.in]
srtobj = ["SeuratClusteringOfAllCells"]
immdata = ["ScRepLoading"]

[TOrBCellSelection.envs]
# Select B cells using CD19 and CD20 (MS4A1) markers
indicator_genes = ["CD19", "MS4A1"]
```

### Selection by Clonotype Percentage Threshold
```toml
[TOrBCellSelection]
[TOrBCellSelection.in]
srtobj = ["SeuratClusteringOfAllCells"]
immdata = ["ScRepLoading"]

[TOrBCellSelection.envs]
# Select cells/clusters with >25% clonotype percentage as T/B cells
selector = "Clonotype_Pct > 0.25"
```

### Selection Combined with Marker Expression
```toml
[TOrBCellSelection]
[TOrBCellSelection.in]
srtobj = ["SeuratClusteringOfAllCells"]
immdata = ["ScRepLoading"]

[TOrBCellSelection.envs]
# Select cells with high clonotype percentage AND CD3E expression
indicator_genes = ["CD3E"]
selector = "Clonotype_Pct > 0.25 & CD3E > 0"
```

### Selection Without VDJ Data (Markers Only)
```toml
[TOrBCellSelection]
[TOrBCellSelection.in]
srtobj = ["SeuratClusteringOfAllCells"]

[TOrBCellSelection.envs]
# Ignore VDJ data, use only marker gene expression
ignore_vdj = true

# Need at least 2 markers for k-means when VDJ is ignored
indicator_genes = ["CD3E", "CD3D", "CD3G"]

# First gene must be a positive marker for selection
# (CD3E is positive for T cells)
```

### B Cell Selection Without VDJ Data
```toml
[TOrBCellSelection]
[TOrBCellSelection.in]
srtobj = ["SeuratClusteringOfAllCells"]

[TOrBCellSelection.envs]
# Select B cells using markers only (no VDJ data)
ignore_vdj = true
indicator_genes = ["CD19", "MS4A1", "CD79A"]
```

### Custom K-means Parameters
```toml
[TOrBCellSelection]
[TOrBCellSelection.in]
srtobj = ["SeuratClusteringOfAllCells"]
immdata = ["ScRepLoading"]

[TOrBCellSelection.envs]
indicator_genes = ["CD3E", "CD3D", "CD3G"]

# Custom k-means parameters
# nstart: number of random starts for stability (default: 25)
# iter.max: maximum iterations (default: 10 in R)
# Note: hyphens instead of dots in key names
kmeans = {"nstart": 50, "iter-max": 20}
```

## Common Patterns

### Pattern 1: Standard T Cell Selection (with VDJ)
```toml
[TOrBCellSelection]
[TOrBCellSelection.in]
srtobj = ["SeuratClusteringOfAllCells"]
immdata = ["ScRepLoading"]

[TOrBCellSelection.envs]
# Robust T cell selection using all three CD3 markers
indicator_genes = ["CD3E", "CD3D", "CD3G"]
```
**When to use**: Typical TCR-seq analysis where T cells need to be separated from other cell types.

### Pattern 2: Standard B Cell Selection (with VDJ)
```toml
[TOrBCellSelection]
[TOrBCellSelection.in]
srtobj = ["SeuratClusteringOfAllCells"]
immdata = ["ScRepLoading"]

[TOrBCellSelection.envs]
# B cell selection using CD19 and CD20 markers
indicator_genes = ["CD19", "MS4A1"]
```
**When to use**: BCR-seq analysis where B cells need to be separated from other cell types.

### Pattern 3: High-Sensitivity T Cell Selection
```toml
[TOrBCellSelection]
[TOrBCellSelection.in]
srtobj = ["SeuratClusteringOfAllCells"]
immdata = ["ScRepLoading"]

[TOrBCellSelection.envs]
# Lower threshold to capture more T cells
selector = "Clonotype_Pct > 0.10 & CD3E > 0"
```
**When to use**: When you suspect low-quality VDJ data or want to capture borderline T cells.

### Pattern 4: High-Specificity T Cell Selection
```toml
[TOrBCellSelection]
[TOrBCellSelection.in]
srtobj = ["SeuratClusteringOfAllCells"]
immdata = ["ScRepLoading"]

[TOrBCellSelection.envs]
# Higher threshold for clean T cell population
selector = "Clonotype_Pct > 0.50 & CD3E > 1"
```
**When to use**: When you want only the highest-confidence T cells (e.g., for clonal expansion analysis).

### Pattern 5: Auto-Selection (K-means) with Multiple Markers
```toml
[TOrBCellSelection]
[TOrBCellSelection.in]
srtobj = ["SeuratClusteringOfAllCells"]
immdata = ["ScRepLoading"]

[TOrBCellSelection.envs]
# Let k-means determine T cell clusters automatically
# No selector = automatic selection
indicator_genes = ["CD3E", "CD3D", "CD3G"]
kmeans = {"nstart": 50}
```
**When to use**: When you don't have a specific threshold in mind and want automatic unsupervised selection.

## Dependencies

### Upstream Processes
- **SeuratClusteringOfAllCells**: Provides clustered Seurat object with `seurat_clusters` metadata
- **ScRepLoading**: Provides VDJ data with clonotype information (unless `ignore_vdj = true`)

### Downstream Processes
- **SeuratClustering**: Clusters the selected T/B cells for downstream analysis
- **ScRepCombiningExpression**: Combines selected cells with VDJ data
- **ModuleScoreCalculator**: Calculates module scores on selected cells
- Other TCR/BCR-specific processes (CDR3Clustering, TESSA, ClonalStats, etc.)

### Workflow Integration
```
SeuratPreparing → SeuratClusteringOfAllCells → TOrBCellSelection → SeuratClustering → (downstream TCR/BCR analysis)
                                                       ↑
                                                ScRepLoading
```

## Selection Methods Explained

### Method 1: K-means Clustering (Default)
When `selector` is not provided, TOrBCellSelection performs:
1. Calculates average expression of indicator genes per cluster
2. If VDJ data available: calculates clonotype percentage per cluster
3. Performs k-means clustering (K=2) on [gene expressions + clonotype_pct]
4. Selects cluster with higher clonotype percentage (or higher expression of first indicator gene if no VDJ)

**Pros**: Automatic, unsupervised, adapts to data
**Cons**: May select unexpected clusters if data is noisy

### Method 2: Custom Selector Expression
Provide a custom R expression via `selector`:
- Can use any metadata column: `Clonotype_Pct > 0.25`
- Can combine with gene expression: `Clonotype_Pct > 0.25 & CD3E > 0`
- Can use complex logic: `(Clonotype_Pct > 0.25 | CD3E > 1) & CD19 < 0.1`

**Pros**: Full control, transparent selection criteria
**Cons**: Requires domain knowledge, need to test thresholds

### Method 3: Marker-Only Selection (ignore_vdj)
Set `ignore_vdj = true` to use only marker genes:
- Useful when VDJ data is poor or missing
- Requires at least 2 indicator genes for k-means
- First gene in list must be positive marker for the target cell type

**Pros**: Works without VDJ data, robust marker-based selection
**Cons**: Requires good marker genes, may include non-clonal cells

## Marker Gene Recommendations

### T Cell Markers
**Positive markers** (expressed in T cells):
- `CD3E`: Core CD3 epsilon chain (most reliable)
- `CD3D`: Core CD3 delta chain
- `CD3G`: Core CD3 gamma chain

**Negative markers** (excluded from T cells):
- `CD19`: B cell marker
- `MS4A1` (CD20): B cell marker
- `CD14`: Monocyte marker
- `CD68`: Macrophage marker

**Recommended for T cells**:
```toml
indicator_genes = ["CD3E", "CD3D", "CD3G"]
```

### B Cell Markers
**Positive markers** (expressed in B cells):
- `CD19`: Pan-B cell marker (most reliable)
- `MS4A1` (CD20): Mature B cell marker
- `CD79A`: B cell receptor component
- `CD79B`: B cell receptor component

**Recommended for B cells**:
```toml
indicator_genes = ["CD19", "MS4A1"]
```

### Subtype-Specific Markers
For selecting specific T/B cell subtypes:
- T helper cells: `CD4`
- Cytotoxic T cells: `CD8A`, `CD8B`
- Regulatory T cells: `FOXP3`, `IL2RA`
- Memory B cells: `CD27`
- Plasma cells: `CD38`, `SDC1` (CD138)

## Validation Rules

### Required Inputs
- `srtobj` must be specified (from SeuratClusteringOfAllCells)
- `immdata` required unless `ignore_vdj = true`

### Marker Gene Validation
- Must provide at least 1 indicator gene
- If `ignore_vdj = true`, must provide at least 2 indicator genes
- First gene in `indicator_genes` must be a positive marker when using k-means without VDJ data

### Selector Expression Validation
- `selector` must be a valid R expression
- Can reference: metadata columns (e.g., `Clonotype_Pct`), indicator genes (e.g., `CD3E`)
- Use R logical operators: `&` (and), `|` (or), `!` (not)

### K-means Parameter Validation
- `kmeans` must be a valid JSON object
- Valid keys: `nstart`, `iter-max`, `algorithm`, etc. (see `stats::kmeans` documentation)
- Dots in R argument names replaced with hyphens (e.g., `iter.max` → `iter-max`)

## Troubleshooting

### Issue: "No clonotype information found"
**Cause**: Barcode mismatch between scRNA-seq and VDJ data
**Solution**:
1. Check barcode formats match in both datasets
2. Verify `ScRepLoading` processed VDJ data correctly
3. Try `ignore_vdj = true` to use marker genes only

### Issue: "You need at least 2 markers to perform k-means clustering with VDJ data being ignored"
**Cause**: Using `ignore_vdj = true` with only 1 indicator gene
**Solution**: Add more indicator genes or use a custom `selector`

### Issue: Selected cells are not what I expected
**Cause**: K-means selected wrong cluster
**Solution**:
1. Check the k-means plot in `details/kmeans.png`
2. Adjust `indicator_genes` to include more robust markers
3. Use custom `selector` instead of automatic selection
4. Adjust `kmeans.nstart` for more stable clustering (e.g., `{"nstart": 50}`)

### Issue: Too few or too many cells selected
**Cause**: Threshold too high or too low
**Solution**:
1. Adjust `selector` threshold (e.g., `Clonotype_Pct > 0.20` vs `0.30`)
2. Review the selection table in `details/data.txt`
3. Check scatter plots in `details/` directory for gene vs clonotype relationships

### Issue: All cells selected as T cells (or none selected)
**Cause**: Poor VDJ data or incorrect marker genes
**Solution**:
1. Verify VDJ data quality in `ScRepLoading` output
2. Check if `CD3E` is actually expressed in your data
3. Use `ignore_vdj = true` with robust marker genes
4. Manually inspect expression plots before running selection

## Output Files

### Primary Output
- `outfile`: Seurat object (qs2 format) containing only selected T/B cells
  - Located at: `{{in.srtobj | stem}}.qs`
  - Contains all original metadata + subset of cells

### Detailed Output Directory (`details/`)
- `data.txt`: Table of indicator gene expression and clonotype percentage per cluster
  - Shows: Cluster, indicator gene expression, Clonotype_Pct, Cluster_Size, is_selected
- `kmeans.png`: K-means clustering visualization (if k-means used)
- `selected_cells_per_sample.png`: Bar plot of selected cells per sample
- `selected_cells_pie.png`: Pie chart of selected vs other cells
- `selected-cells.png`: Dimension plots showing VDJ data and selected cells
- `feature-plots.png`: Feature plots of indicator genes

### Report
Interactive HTML report with visualization of selection results and cell composition.

## Common Use Cases

### Use Case 1: TCR-seq Analysis of PBMC Data
```toml
# Standard TCR-seq workflow
[SeuratClusteringOfAllCells]

[TOrBCellSelection]
[TOrBCellSelection.in]
srtobj = ["SeuratClusteringOfAllCells"]
immdata = ["ScRepLoading"]

[TOrBCellSelection.envs]
indicator_genes = ["CD3E", "CD3D", "CD3G"]

[SeuratClustering]
# Clustering of selected T cells
[CDR3Clustering]
[TESSA]
[ClonalStats]
```

### Use Case 2: BCR-seq Analysis of Tumor-Infiltrating Lymphocytes
```toml
[SeuratClusteringOfAllCells]

[TOrBCellSelection]
[TOrBCellSelection.in]
srtobj = ["SeuratClusteringOfAllCells"]
immdata = ["ScRepLoading"]

[TOrBCellSelection.envs]
# Select B cells from TILs
indicator_genes = ["CD19", "MS4A1", "CD79A"]
selector = "CD19 > 0.5"

[SeuratClustering]
[CDR3Clustering]
[CellCellCommunication]
```

### Use Case 3: RNA-only Data with T/B Cell Separation
```toml
[SeuratClusteringOfAllCells]

[TOrBCellSelection]
[TOrBCellSelection.in]
srtobj = ["SeuratClusteringOfAllCells"]

[TOrBCellSelection.envs]
# No VDJ data, use markers only
ignore_vdj = true
indicator_genes = ["CD3E", "CD3D", "CD3G"]

[SeuratClustering]
[ScFGSEA]
[CellCellCommunication]
```

## Key Notes

1. **Not for Pure T/B Cell Populations**: If all cells are already T or B cells, skip this process and use `SeuratClustering` directly.

2. **Cluster-Level Selection**: Selection happens at the cluster level, not single-cell level. All cells in selected clusters are kept.

3. **Normalization**: Gene expression values are normalized (mean=0, SD=1) before k-means clustering.

4. **Marker First**: When using k-means without VDJ data, the first indicator gene must be a positive marker for your target cell type.

5. **Report Review**: Always review the HTML report and plots in `details/` to verify selection quality.

6. **Threshold Tuning**: Start with default k-means, then adjust to custom `selector` if automatic selection is not satisfactory.
