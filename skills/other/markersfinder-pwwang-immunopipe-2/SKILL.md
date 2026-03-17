---
name: markersfinder
description: Flexible marker finding process that wraps Seurat's FindMarkers function for custom group comparisons beyond simple cluster-vs-all analysis. Unlike ClusterMarkers (all-vs-all cluster comparisons), MarkersFinder enables targeted differential expression analysis between specific groups, conditions within cell types, or any custom comparison defined by metadata columns. Automatically performs pathway enrichment analysis on significant markers and generates comprehensive visualizations.
---

# MarkersFinder Process Configuration

## Purpose
Flexible marker finding process that wraps Seurat's FindMarkers function for custom group comparisons beyond simple cluster-vs-all analysis. Unlike ClusterMarkers (all-vs-all cluster comparisons), MarkersFinder enables targeted differential expression analysis between specific groups, conditions within cell types, or any custom comparison defined by metadata columns. Automatically performs pathway enrichment analysis on significant markers and generates comprehensive visualizations.

## When to Use
- **Custom group comparisons**: Compare specific clusters (e.g., c1 vs c3)
- **Condition effects within cell types**: Treatment vs control in T cells
- **Targeted differential expression**: Focus on biologically meaningful comparisons
- **Multi-sample analysis**: Find markers across different samples/batches
- **Subset-based comparisons**: Compare cell states within defined populations
- **Complex experimental designs**: Multi-condition, multi-factor comparisons

**Note**: Use `ClusterMarkers` for standard all-vs-all cluster analysis. Use `MarkersFinder` for custom comparisons.

## Configuration Structure

### Process Enablement
```toml
[MarkersFinder]
cache = true
```

### Input Specification
```toml
[MarkersFinder.in]
srtobj = ["SeuratClustering"]
```

### Environment Variables

#### Core Group Specification
```toml
[MarkersFinder.envs]
group_by = "seurat_clusters"  # Column in metadata to group cells
ident_1 = ""  # First group (ident.1); if empty, all groups vs rest
ident_2 = ""  # Second group (ident.2); if empty, ident_1 vs rest
each = ""  # Column to create separate cases for each unique value
```

#### Statistical Test Selection (Seurat FindMarkers)
```toml
[MarkersFinder.envs]
test.use = "wilcox"  # Options: wilcox, MAST, DESeq2, roc, t, tobit, bimod, poisson, negbinom, LR
logfc.threshold = 0.25  # Minimum log2 fold change
min.pct = 0.1  # Minimum percentage of cells expressing gene
min.diff.pct = -Inf  # Minimum difference in detection
only.pos = false  # Only positive markers
min.cells.group = 3  # Minimum cells per group
min.cells.feature = 3  # Minimum cells expressing gene
```

#### Significant Markers Filter & Enrichment
```toml
[MarkersFinder.envs]
sigmarkers = "p_val_adj < 0.05"  # Filter for enrichment (vars: p_val, avg_log2FC, pct.1, pct.2, p_val_adj)
dbs = ["KEGG_2021_Human", "MSigDB_Hallmark_2020"]  # Pathway databases
enrich_style = "enrichr"  # Options: enrichr, clusterprofiler
```

#### Multiple Comparison Cases
```toml
[MarkersFinder.envs.cases."T_vs_B"]
group_by = "celltype"
ident_1 = "T cells"
ident_2 = "B cells"

[MarkersFinder.envs.cases."Treatment_vs_Control"]
group_by = "condition"
ident_1 = "treatment"
ident_2 = "control"
subset = "celltype == 'T cells'"
```

## External References

### Seurat FindMarkers Parameters
https://satijalab.org/seurat/reference/findmarkers

**Key Parameters:**
- `ident.1`, `ident.2`: Groups to compare
- `test.use`: Statistical test (wilcox, MAST, DESeq2, roc, etc.)
- `logfc.threshold`: Minimum fold change (log2 scale)
- `min.pct`: Minimum percentage of cells expressing gene
- `min.diff.pct`: Minimum difference in detection between groups
- `only.pos`: Return only positive markers (higher in ident.1)

### Enrichment Databases
- `"KEGG_2021_Human"`, `"KEGG"`: KEGG pathways
- `"MSigDB_Hallmark_2020"`, `"Hallmark"`: MSigDB Hallmark
- `"GO_Biological_Process_2025"`: GO Biological Process
- `"Reactome_Pathways_2024"`, `"Reactome"`: Reactome
- `"WikiPathways_2024_Human"`, `"WikiPathways"`: WikiPathways

**Full list**: https://maayanlab.cloud/Enrichr/#libraries

## Configuration Examples

### Minimal Configuration
```toml
[MarkersFinder]
[MarkersFinder.in]
srtobj = ["SeuratClustering"]
[MarkersFinder.envs]
group_by = "seurat_clusters"
```

### Cluster-to-Cluster Comparison
```toml
[MarkersFinder.envs]
group_by = "seurat_clusters"
ident_1 = "c1"
ident_2 = "c3"
logfc.threshold = 0.25
sigmarkers = "p_val_adj < 0.05 & avg_log2FC > 0"
```

### Condition Comparison within Cell Type
```toml
[MarkersFinder.envs]
group_by = "condition"
ident_1 = "treatment"
ident_2 = "control"
subset = "celltype == 'T cells'"
test.use = "MAST"
```

### Multiple Comparison Cases
```toml
[MarkersFinder.envs.cases."T_vs_B"]
group_by = "celltype"
ident_1 = "T cells"
ident_2 = "B cells"
[MarkersFinder.envs.cases."CD4_vs_CD8"]
group_by = "subtype"
ident_1 = "CD4+ T"
ident_2 = "CD8+ T"
subset = "celltype == 'T cells'"
```

### Cross-Sample Comparison (Using `each`)
```toml
[MarkersFinder.envs]
group_by = "seurat_clusters"
ident_1 = "c1"
ident_2 = "c2"
each = "Sample"
```

## Common Patterns

### Pattern 1: Specific Cluster Pair
```toml
[MarkersFinder.envs]
group_by = "seurat_clusters"
ident_1 = "c1"
ident_2 = "c3"
logfc.threshold = 0.25
sigmarkers = "p_val_adj < 0.05 & avg_log2FC > 0"
```

### Pattern 2: Treatment Effect per Cell Type
```toml
[MarkersFinder.envs.cases."Treatment_Tcells"]
group_by = "condition"
ident_1 = "treatment"
ident_2 = "control"
subset = "celltype == 'T cells'"
[MarkersFinder.envs.cases."Treatment_Bcells"]
group_by = "condition"
ident_1 = "treatment"
ident_2 = "control"
subset = "celltype == 'B cells'"
```

### Pattern 3: Multiple Contrasts
```toml
[MarkersFinder.envs.cases."T_vs_B"]
group_by = "celltype"
ident_1 = "T cells"
ident_2 = "B cells"
[MarkersFinder.envs.cases."CD4_vs_CD8"]
group_by = "subtype"
ident_1 = "CD4+ T"
ident_2 = "CD8+ T"
subset = "celltype == 'T cells'"
```

### Pattern 4: All Clusters vs Rest (Like ClusterMarkers)
```toml
[MarkersFinder.envs]
group_by = "seurat_clusters"
```

### Pattern 5: Cross-Batch Comparison with `each`
```toml
[MarkersFinder.envs]
group_by = "seurat_clusters"
ident_1 = "c1"
ident_2 = "c2"
each = "Batch"
overlaps = {"Batch_Overlap": {plot_type = "venn"}}
```

## Difference from ClusterMarkers

| Feature | ClusterMarkers | MarkersFinder |
|---------|---------------|---------------|
| **Default behavior** | All clusters vs all other clusters | Customizable comparisons |
| **Group specification** | Fixed to seurat_clusters | Any metadata column |
| **Comparisons** | All-vs-all matrix | Targeted pairs or groups vs rest |
| **Multiple cases** | Single comparison set | Multiple custom cases |
| **Use case** | Cluster annotation | Targeted differential expression |

**When to use which:**
- **ClusterMarkers**: Standard cluster identification, all-vs-all comparisons, quick cluster annotation
- **MarkersFinder**: Custom comparisons, condition effects, cell type-specific DE, multi-factor designs

## Dependencies
- **Upstream**: `SeuratClustering` (provides cluster assignments and metadata)
- **Downstream**: Custom differential expression analysis, cell type annotation
- **Related**: `ClusterMarkers` (simpler all-vs-all), `PseudoBulkDEG` (bulk-like DE)

## Validation Rules
- `group_by` must be valid column in Seurat object metadata
- `ident_1` and `ident_2` must exist in `group_by` column if specified
- Groups must have ≥ `min.cells.group` cells (default: 3)
- Genes must be expressed in ≥ `min.cells.feature` cells (default: 3)
- For `each`: creates separate case for each unique value in column
- `sigmarkers` must be valid R/dplyr expression with available variables: `p_val`, `avg_log2FC`, `pct.1`, `pct.2`, `p_val_adj`

## Troubleshooting

### Issue: Group Not Found
**Symptoms**: Error "ident.1 not found"
**Solution**: Verify `group_by` column name and `ident_1`/`ident_2` values match Seurat object metadata exactly (case-sensitive)

### Issue: Insufficient Cells in Groups
**Symptoms**: No markers found or cell count error
**Solution**: Reduce `min.cells.group` and `min.cells.feature` to 1, or combine similar groups via `mutaters`

### Issue: No Significant Markers Found
**Symptoms**: Empty marker tables
**Solution**: Loosen thresholds: `logfc.threshold = 0.1`, `min.pct = 0.05`, `sigmarkers = "p_val_adj < 0.1 & avg_log2FC > 0"`

### Issue: Too Many Markers Found
**Symptoms**: Thousands of markers, computationally expensive
**Solution**: Tighten thresholds: `logfc.threshold = 0.58` (1.5-fold), `min.pct = 0.25`, `sigmarkers = "p_val_adj < 0.01 & avg_log2FC > 1"`

### Issue: Enrichment Analysis Returns No Results
**Symptoms**: Empty enrichment tables
**Solution**: Loosen `sigmarkers` filter and add more databases: `dbs = ["KEGG_2021_Human", "MSigDB_Hallmark_2020", "Reactome_Pathways_2024"]`
