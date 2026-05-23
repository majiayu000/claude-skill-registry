---
name: clustermarkers
description: Finds differentially expressed genes (markers) for clusters of T/B cells using Seurat's FindMarkers function. Performs statistical testing between clusters, identifies cluster-defining genes, and automatically runs pathway enrichment analysis (via Enrichr) on significant markers. Generates publication-ready visualizations including volcano plots, dot plots, heatmaps, and enrichment plots.
---

# ClusterMarkers Process Configuration

## Purpose
Finds differentially expressed genes (markers) for clusters of T/B cells using Seurat's FindMarkers function. Performs statistical testing between clusters, identifies cluster-defining genes, and automatically runs pathway enrichment analysis (via Enrichr) on significant markers. Generates publication-ready visualizations including volcano plots, dot plots, heatmaps, and enrichment plots.

## When to Use
- **After SeuratClustering**: Essential for cluster interpretation and annotation
- **Cluster annotation**: Identify marker genes to assign biological meaning to clusters
- **Publication preparation**: Generate marker tables, volcano plots, and enrichment figures
- **Cell type characterization**: Understand functional differences between cell populations
- **Comparative analysis**: Compare clusters to find unique gene expression signatures

## Configuration Structure

### Process Enablement
```toml
[ClusterMarkers]
cache = true  # Cache results for faster re-runs with different visualizations
```

### Input Specification
```toml
[ClusterMarkers.in]
srtobj = ["SeuratClustering"]  # Seurat object with cluster assignments
```

### Environment Variables

#### Core Parameters
```toml
[ClusterMarkers.envs]
# Number of cores for parallel computation
ncores = 1  # int; Parallelize Seurat procedures

# Subset cells before marker finding (R expression)
subset = "seurat_clusters %in% c('c1', 'c2', 'c3')"  # Optional

# Cache location for intermediate results
cache = "/tmp"  # Path; Set to false to disable caching

# Assay to use for marker finding
assay = "RNA"  # Default: uses active assay

# Error on no markers found
error = false  # bool; If true, fail if no markers found
```

#### Statistical Test Selection
```toml
[ClusterMarkers.envs]
# Statistical test for differential expression
test.use = "wilcox"  # Default
```

**Available tests:**
- `"wilcox"`: Wilcoxon rank sum test (default, fast)
- `"wilcox_limma"`: Limma implementation (Seurat v4 compatibility)
- `"MAST"`: GLM with cellular detection rate covariate (recommended)
- `"DESeq2"`: Negative binomial model (robust, requires counts)
- `"roc"`: ROC analysis (AUC-based classification)
- `"t"`: Student's t-test
- `"tobit"`: Tobit test for censored data
- `"bimod"`: Likelihood-ratio test for bimodal expression
- `"poisson"`: Poisson distribution (UMI datasets only)
- `"negbinom"`: Negative binomial (UMI datasets only)
- `"LR"`: Logistic regression (latent.vars supported)

**Test selection guidelines:**
- Default: `"wilcox"` for speed and reliability
- Publication-quality: `"MAST"` for single-cell-specific modeling
- Bulk-like DE: `"DESeq2"` for rigorous statistical testing
- UMI data: `"negbinom"` or `"poisson"` for count-based models
- Classification: `"roc"` for AUC-based marker ranking

#### Threshold Parameters (Seurat FindMarkers)
```toml
[ClusterMarkers.envs]
# Minimum log2 fold change threshold
logfc.threshold = 0.25  # float; Default: 0.25

# Minimum percentage of cells expressing gene
min.pct = 0.1  # float; Range: 0.0-1.0

# Minimum difference in detection percentage
min.diff.pct = -Inf  # float; Default: no limit

# Only positive markers (higher in ident.1 group)
only.pos = false  # bool; Default: false (both directions)

# Maximum cells per identity (downsampling)
max.cells.per.ident = Inf  # int; No downsampling by default

# Minimum cells expressing gene (poisson/negbinom tests)
min.cells.feature = 3  # int

# Minimum cells per group
min.cells.group = 3  # int
```

**Note:** Use `-` to replace `.` in parameter names (e.g., `logfc.threshold`, not `logfc.threshold`)

#### Significant Markers Filter (for Enrichment)
```toml
[ClusterMarkers.envs]
# Filter markers for enrichment analysis (R expression)
sigmarkers = "p_val_adj < 0.05 & avg_log2FC > 0"  # Default

# Variables available: p_val, avg_log2FC, pct.1, pct.2, p_val_adj
# Example: "p_val_adj < 0.05 & abs(avg_log2FC) > 1" (both directions)
```

#### Enrichment Analysis
```toml
[ClusterMarkers.envs]
# Databases for pathway enrichment
dbs = ["KEGG_2021_Human", "MSigDB_Hallmark_2020"]  # Default

# Enrichment style
enrich_style = "enrichr"  # Options: "enrichr", "clusterprofiler", "clusterProfiler"
```

**Available databases (enrichit):**
- `"KEGG_2021_Human"`, `"KEGG"`: KEGG pathways
- `"MSigDB_Hallmark_2020"`, `"Hallmark"`: MSigDB Hallmark gene sets
- `"GO_Biological_Process_2025"`: Gene Ontology Biological Process
- `"GO_Cellular_Component_2025"`: Gene Ontology Cellular Component
- `"GO_Molecular_Function_2025"`: Gene Ontology Molecular Function
- `"Reactome_Pathways_2024"`, `"Reactome"`: Reactome pathways
- `"WikiPathways_2024_Human"`, `"WikiPathways"`: WikiPathways
- `"BioCarta_2016"`: BioCarta pathways

**More databases:** https://maayanlab.cloud/Enrichr/#libraries

#### Visualization Parameters
```toml
[ClusterMarkers.envs]
# Marker plots configuration
marker_plots_defaults = {order_by = "desc(avg_log2FC)"}

# All markers plots (across clusters)
allmarker_plots = {"Top 10 markers of all clusters": {plot_type = "heatmap"}}

# Enrichment plots (all clusters)
allenrich_plots = {}  # Empty by default

# Marker plots (per cluster)
marker_plots = {}  # Default: volcano plots and dot plots

# Enrichment plots (per cluster)
enrich_plots = {}  # Default: bar plot

# Overlap analysis (venn/upset)
overlaps = {}  # Empty by default
```

## External References

### Seurat FindMarkers
https://satijalab.org/seurat/reference/findmarkers
- Core differential expression function
- Statistical tests: wilcox, MAST, DESeq2, ROC, t-test, etc.
- Threshold parameters control sensitivity and speed

### Enrichr Databases
https://maayanlab.cloud/Enrichr/#libraries
- Comprehensive gene set enrichment collection
- KEGG, GO, Reactome, MSigDB, WikiPathways

### biopipen MarkersFinder
https://pwwang.github.io/biopipen/api/biopipen.ns.scrna/#biopipen.ns.scrna.MarkersFinder
- Parent process with extended functionality
- Visualization: biopipen.utils::VizDEGs, scplotter::EnrichmentPlot

## Configuration Examples

### Minimal Configuration
```toml
[ClusterMarkers]
[ClusterMarkers.in]
srtobj = ["SeuratClustering"]
```
**Result**: Default wilcox test, standard thresholds, hallmark + KEGG enrichment

### Standard Marker Finding (Wilcoxon)
```toml
[ClusterMarkers]
[ClusterMarkers.in]
srtobj = ["SeuratClustering"]

[ClusterMarkers.envs]
test.use = "wilcox"
logfc.threshold = 0.25
min.pct = 0.1
sigmarkers = "p_val_adj < 0.05 & avg_log2FC > 0"
```

### Publication-Ready MAST Analysis
```toml
[ClusterMarkers]
[ClusterMarkers.in]
srtobj = ["SeuratClustering"]

[ClusterMarkers.envs]
test.use = "MAST"
logfc.threshold = 0.25
min.pct = 0.1
sigmarkers = "p_val_adj < 0.01 & abs(avg_log2FC) > 1"
ncores = 4
```

### DESeq2 for Robust Analysis
```toml
[ClusterMarkers]
[ClusterMarkers.in]
srtobj = ["SeuratClustering"]

[ClusterMarkers.envs]
test.use = "DESeq2"
logfc.threshold = 0.5  # More stringent
min.pct = 0.15
sigmarkers = "p_val_adj < 0.05 & avg_log2FC > 0.5"
```
**Note**: DESeq2 requires count data in the Seurat object

### Stringent Thresholds for High-Confidence Markers
```toml
[ClusterMarkers.envs]
logfc.threshold = 0.58  # 1.5-fold change (2^0.58)
min.pct = 0.25  # Expressed in >25% cells
min.diff.pct = 0.1  # 10% difference in detection
only.pos = true  # Positive markers only
sigmarkers = "p_val_adj < 0.01 & avg_log2FC > 1"
```

### Subset Specific Clusters
```toml
[ClusterMarkers.envs]
# Only analyze clusters c1, c2, c3 to save computation
subset = "seurat_clusters %in% c('c1', 'c2', 'c3')"
```

### Custom Enrichment Databases
```toml
[ClusterMarkers.envs]
# Use different pathway databases
dbs = ["Reactome_Pathways_2024", "GO_Biological_Process_2025"]
enrich_style = "clusterprofiler"
```

### Positive Markers Only (Cluster-Specific)
```toml
[ClusterMarkers.envs]
only.pos = true
sigmarkers = "p_val_adj < 0.05 & avg_log2FC > 0"
```

### Downsample Large Clusters
```toml
[ClusterMarkers.envs]
max.cells.per.ident = 5000  # Limit to 5000 cells per cluster
random.seed = 42  # Reproducible downsampling
```

## Common Patterns

### Pattern 1: Quick Wilcoxon Test (Default)
```toml
[ClusterMarkers]
[ClusterMarkers.in]
srtobj = ["SeuratClustering"]
```
**Use case**: Initial exploration, speed priority

### Pattern 2: Publication-Quality MAST
```toml
[ClusterMarkers]
[ClusterMarkers.in]
srtobj = ["SeuratClustering"]

[ClusterMarkers.envs]
test.use = "MAST"
logfc.threshold = 0.25
min.pct = 0.1
ncores = 8
```
**Use case**: Single-cell publication, accounts for detection rate

### Pattern 3: Both Positive and Negative Markers
```toml
[ClusterMarkers.envs]
only.pos = false
sigmarkers = "p_val_adj < 0.05 & abs(avg_log2FC) > 0.5"
```
**Use case**: Find genes upregulated and downregulated in each cluster

### Pattern 4: Stringent Top Markers
```toml
[ClusterMarkers.envs]
logfc.threshold = 1.0  # 2-fold change
min.pct = 0.3
sigmarkers = "p_val_adj < 0.001 & avg_log2FC > 1"
only.pos = true
```
**Use case**: High-confidence cluster markers for annotation

### Pattern 5: Custom Enrichment with Multiple DBs
```toml
[ClusterMarkers.envs]
dbs = [
  "KEGG_2021_Human",
  "MSigDB_Hallmark_2020",
  "GO_Biological_Process_2025",
  "Reactome_Pathways_2024"
]
enrich_style = "enrichr"
```

### Pattern 6: ROC Analysis for Classification
```toml
[ClusterMarkers.envs]
test.use = "roc"
logfc.threshold = 0.1
sigmarkers = "p_val_adj < 0.05 & avg_log2FC > 0"
```
**Use case**: Find markers with highest AUC for classification

## Dependencies

### Upstream Processes
- **Required**: `SeuratClustering` (provides cluster assignments)
- **Alternative**: `SeuratSubClustering` (if sub-clustering analysis)
- **Context**: Runs after `TOrBCellSelection` if T/B cell selection is enabled

### Downstream Processes
- **CellTypeAnnotation**: Uses markers for automated cell type assignment
- **SeuratMap2Ref**: Reference-based annotation may use marker profiles
- **ScFGSEA**: Gene set enrichment on identified markers
- **ModuleScoreCalculator**: Score marker genes across cells

## Validation Rules

### Statistical Test Constraints
- `test.use` must be one of: wilcox, wilcox_limma, MAST, DESeq2, roc, t, tobit, bimod, poisson, negbinom, LR
- DESeq2 requires count data (automatically uses counts slot)
- MAST, poisson, negbinom support `latent.vars` for additional covariates

### Threshold Validation
- `logfc.threshold`: ≥ 0 (typical range: 0.1-1.0)
- `min.pct`: 0.0-1.0 (typical: 0.1-0.3)
- `min.diff.pct`: ≥ -Inf (typical: 0.05-0.2)
- `min.cells.feature`: ≥ 1 (default: 3)
- `min.cells.group`: ≥ 1 (default: 3)

### sigmarkers Expression
- Must be valid R/dplyr expression
- Available variables: p_val, avg_log2FC, pct.1, pct.2, p_val_adj
- Use `&` for AND, `|` for OR, `!` for NOT

### Database Constraints
- `dbs` must be valid enrichit database names or GMT file paths
- Custom GMT files: use absolute paths or paths relative to config file

## Troubleshooting

### Issue: Too Many Markers Found
**Symptoms**: Thousands of markers, low statistical power

**Solutions**:
```toml
[ClusterMarkers.envs]
logfc.threshold = 0.5  # Increase fold change threshold
min.pct = 0.25  # Increase expression percentage
min.diff.pct = 0.15  # Increase detection difference
sigmarkers = "p_val_adj < 0.01 & avg_log2FC > 1"  # Stricter filter
```

### Issue: No Markers Found
**Symptoms**: Empty marker tables, no enrichment results

**Solutions**:
```toml
[ClusterMarkers.envs]
logfc.threshold = 0.1  # Lower threshold
min.pct = 0.05  # Lower expression requirement
min.diff.pct = -Inf  # Remove detection difference
sigmarkers = "p_val_adj < 0.1 & avg_log2FC > 0.1"  # Looser filter
```

### Issue: Slow Performance
**Symptoms**: Marker finding takes hours

**Solutions**:
```toml
[ClusterMarkers.envs]
ncores = 8  # Use more cores
logfc.threshold = 0.5  # Higher threshold reduces genes tested
max.cells.per.ident = 5000  # Downsample large clusters
```

### Issue: DESeq2 Fails with Integrated Data
**Symptoms**: DESeq2 error on integrated Seurat object

**Cause**: DESeq2 requires count data, integrated objects have empty counts slot

**Solution**:
```toml
# Use SCTransform counts instead of integrated data
[SeuratPreparing.envs]
method = "SCTransform"
integration_method = null  # Skip integration for DESeq2

[ClusterMarkers.envs]
test.use = "DESeq2"
```
**Alternative**: Use MAST or wilcox on integrated data

### Issue: Enrichment Analysis Returns No Results
**Symptoms**: Empty enrichment tables/plots

**Solutions**:
```toml
[ClusterMarkers.envs]
# Check sigmarkers filter is too strict
sigmarkers = "p_val_adj < 0.1 & avg_log2FC > 0"

# Add more databases
dbs = ["KEGG_2021_Human", "MSigDB_Hallmark_2020", "Reactome_Pathways_2024"]
```

### Issue: NA p-values in Results
**Symptoms**: Some markers have NA p-values

**Cause**: Insufficient cells per group or low expression variance

**Solutions**:
```toml
[ClusterMarkers.envs]
min.cells.group = 10  # Increase minimum cells
min.cells.feature = 5  # Increase minimum expressing cells
```

### Issue: Different Test Methods Return Similar Results
**Symptoms**: wilcox and MAST return nearly identical gene lists

**Cause**: Strong markers are robust across methods

**Solution**: Use ROC analysis for alternative ranking:
```toml
[ClusterMarkers.envs]
test.use = "roc"
```

### Issue: Computationally Expensive Enrichment
**Symptoms**: Enrichment step takes very long

**Solutions**:
```toml
[ClusterMarkers.envs]
# Limit markers for enrichment
sigmarkers = "p_val_adj < 0.01 & avg_log2FC > 1"

# Use fewer databases
dbs = ["MSigDB_Hallmark_2020"]

# Subset clusters for analysis
subset = "seurat_clusters %in% c('c1', 'c2')"
```

## Best Practices

1. **Start with default wilcox test** for initial exploration
2. **Use MAST for publications** (single-cell-specific modeling)
3. **Set appropriate thresholds**: logfc.threshold = 0.25-0.5, min.pct = 0.1-0.2
4. **Filter for enrichment**: Use sigmarkers to limit to high-confidence markers
5. **Customize enrichment databases**: Choose databases relevant to your study
6. **Use both.pos = false** to see upregulated and downregulated genes
7. **Parallelize with ncores** for large datasets
8. **Subset clusters** when analyzing many clusters to save computation
9. **Validate markers**: Check expression patterns in visualization
10. **Reproducibility**: Set random.seed for downsampling

## Related Processes

- **ClusterMarkersOfAllCells**: Marker finding before T/B cell selection
- **MarkersFinder**: Extended parent process with more flexibility
- **TopExpressingGenes**: Top expressed genes per cluster (non-DE)
- **SeuratClustering**: Required upstream process for cluster assignments
- **CellTypeAnnotation**: Uses markers for automated annotation
