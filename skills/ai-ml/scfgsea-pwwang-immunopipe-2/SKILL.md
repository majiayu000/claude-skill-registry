---
name: scfgsea
description: Performs fast Gene Set Enrichment Analysis (GSEA) on single-cell data using fgsea R package. Identifies enriched biological pathways by ranking genes based on differential expression between cell groups. Generates enrichment scores, significance metrics, and publication-ready visualizations.
---

# ScFGSEA Process Configuration

## Purpose
Performs fast Gene Set Enrichment Analysis (GSEA) on single-cell data using fgsea R package. Identifies enriched biological pathways by ranking genes based on differential expression between cell groups. Generates enrichment scores, significance metrics, and publication-ready visualizations.

## When to Use
- After clustering: Functional interpretation of cluster differences
- Pathway analysis: Identify biological processes driving cell type differentiation
- Comparative analysis: Compare gene expression patterns between groups (e.g., disease vs control)
- Subgroup analysis: Run GSEA on metadata subsets (diagnosis, treatment, etc.)
- TCR integration: Analyze pathway enrichment in TCR-selected clones/clusters

## Configuration Structure

### Process Enablement
```toml
[ScFGSEA]
cache = true
```

### Input Specification
```toml
[ScFGSEA.in]
srtobj = ["SeuratClustering"]  # or "ScRepCombiningExpression"
```

### Environment Variables
```toml
[ScFGSEA.envs]
# Core parameters
ncores = 1  # Parallel cores
assay = "RNA"  # Assay to use
subset = "seurat_clusters %in% c('c1', 'c2')"  # Subset cells

# Grouping parameters
group_by = "seurat_clusters"  # Column to compare
ident_1 = "c1"  # First group
ident_2 = "c2"  # Second group (optional: uses all others)
each = "seurat_clusters"  # Split into multiple cases

# Gene set database
gmtfile = "KEGG_2021_Human"  # Default

# Ranking method
method = "s2n"  # signal-to-noise (default)

# fgsea parameters
minsize = 10  # Min gene set size
maxsize = 100  # Max gene set size
top = 20  # Top pathways to plot (< 1 for padj threshold)
eps = 0.0  # P-value boundary

# Visualization
[ScFGSEA.envs.alleach_plots.Heatmap]
plot_type = "heatmap"
group_by = "Diagnosis"
```

## Gene Set Databases

### MSigDB Collections
- **H (Hallmark)**: 50 curated, non-redundant gene sets → `"MSigDB_Hallmark_2020"`
- **C2 (Curated)**: 7,411 gene sets from pathway databases
  - CP:KEGG → `"KEGG_2021_Human"`
  - CP:REACTOME → `"Reactome_Pathways_2024"`
  - CP:BIOCARTA → `"BioCarta_2016"`
  - CP:WIKIPATHWAYS → `"WikiPathways_2024_Human"`
- **C5 (GO)**: 18,807 Gene Ontology terms
  - BP → `"GO_Biological_Process_2025"`
  - CC → `"GO_Cellular_Component_2025"`
  - MF → `"GO_Molecular_Function_2025"`
- **C7 (Immunologic)**: 2,497 immune-specific signatures (use custom GMT)

### Custom GMT Files
```toml
gmtfile = "/path/to/custom.gmt"
```
Format: `name<tab>description<tab>gene1,gene2,...`

## Ranking Methods
- `"s2n"`/`"signal_to_noise"`: Signal-to-noise ratio (default)
- `"abs_s2n"`/`"abs_signal_to_noise"`: Absolute signal-to-noise
- `"t_test"`: Student's t-test
- `"ratio_of_classes"`: Fold change (natural scale)
- `"diff_of_classes"`: Difference of means
- `"log2_ratio_of_classes"`: Log2 fold change (recommended for log-scale RNA-seq)

## Configuration Examples

### Minimal Configuration
```toml
[ScFGSEA]
[ScFGSEA.in]
srtobj = ["SeuratClustering"]

[ScFGSEA.envs]
group_by = "seurat_clusters"
ident_1 = "c1"
ident_2 = "c2"
```

### Standard Hallmark Analysis
```toml
[ScFGSEA.envs]
gmtfile = "MSigDB_Hallmark_2020"
group_by = "Diagnosis"
ident_1 = "Disease"
ident_2 = "Control"
each = "seurat_clusters"
method = "s2n"
top = 20
```

### KEGG Pathways with Custom Thresholds
```toml
[ScFGSEA.envs]
gmtfile = "KEGG_2021_Human"
group_by = "Treatment"
ident_1 = "Treated"
ident_2 = "Untreated"
minsize = 15
maxsize = 200
method = "log2_ratio_of_classes"
```

### GO Biological Process
```toml
[ScFGSEA.envs]
gmtfile = "GO_Biological_Process_2025"
group_by = "Diagnosis"
ident_1 = "Colitis"
ident_2 = "Control"
minsize = 10
maxsize = 500
top = 0.05  # padj < 0.05
```

### Immunologic Signatures (Custom GMT)
```toml
[ScFGSEA.envs]
gmtfile = "/data/gmt/MSigDB_C7_Immunologic_Signatures.gmt"
group_by = "tissue_type"
ident_1 = "Inflamed"
ident_2 = "Normal"
minsize = 5
maxsize = 150
```

### Multiple Database Comparison
```toml
[ScFGSEA.envs.cases.Hallmark]
gmtfile = "MSigDB_Hallmark_2020"
ident_1 = "Disease"
ident_2 = "Control"

[ScFGSEA.envs.cases.KEGG]
gmtfile = "KEGG_2021_Human"
ident_1 = "Disease"
ident_2 = "Control"
```

### TCR Clonotype Analysis
```toml
[ScFGSEA.in]
srtobj = ["ScRepCombiningExpression"]

[ScFGSEA.envs]
group_by = "cdr3_clonotype_cluster"
ident_1 = "expanded_clone"
ident_2 = "rest"
gmtfile = "MSigDB_Hallmark_2020"
subset = "CD4"
```

## Common Patterns

### Pattern 1: Standard Cluster Comparison
```toml
[ScFGSEA.envs]
gmtfile = "MSigDB_Hallmark_2020"
group_by = "seurat_clusters"
ident_1 = "c1"
ident_2 = "c2"
```

### Pattern 2: Disease vs Control with Multiple Clusters
```toml
[ScFGSEA.envs]
group_by = "Diagnosis"
ident_1 = "Disease"
ident_2 = "Control"
each = "seurat_clusters"
gmtfile = "KEGG_2021_Human"
```

### Pattern 3: Log2 Fold Change Ranking
```toml
[ScFGSEA.envs]
method = "log2_ratio_of_classes"
gmtfile = "MSigDB_Hallmark_2020"
```

### Pattern 4: Stringent Pathway Size Filter
```toml
[ScFGSEA.envs]
minsize = 20
maxsize = 150
gmtfile = "Reactome_Pathways_2024"
```

### Pattern 5: P-Value Threshold for Plots
```toml
[ScFGSEA.envs]
top = 0.01  # padj < 0.01 only
gmtfile = "MSigDB_Hallmark_2020"
```

### Pattern 6: Custom Metabolic Pathways
```toml
[ScFGSEA.envs]
gmtfile = "/data/gmt/KEGG_Metabolism.gmt"
group_by = "Metabolic_State"
ident_1 = "High"
ident_2 = "Low"
```

## Dependencies
- **Upstream**: `SeuratClustering` or `ScRepCombiningExpression`
- **Downstream**: `CellTypeAnnotation`, pathway visualization

## Validation Rules
- `gmtfile`: Valid enrichit name or GMT path
- `group_by`: Valid metadata column
- `ident_1`/`ident_2`: Values must exist in `group_by`
- `minsize`: ≥ 1, `maxsize`: > minsize
- `top`: > 0 or < 1 (padj threshold)
- `method`: Valid fgsea ranking method

## Troubleshooting

### Too Few Pathways Enriched
```toml
[ScFGSEA.envs]
minsize = 5  # Smaller pathways
maxsize = 500  # Larger pathways
top = 0.1  # Looser threshold
gmtfile = "GO_Biological_Process_2025"  # More gene sets
```

### No Enrichment Results
**Causes**: Insufficient cells, gene name mismatch, restrictive thresholds
**Solutions**:
```toml
[ScFGSEA.envs]
minsize = 10
maxsize = 200
subset = "group_by_count > 10"
```

### Long Computation Time
```toml
[ScFGSEA.envs]
minsize = 20
maxsize = 100
gmtfile = "MSigDB_Hallmark_2020"
ncores = 8
subset = "seurat_clusters %in% c('c1', 'c2')"
```

### Gene Name Mismatch
**Cause**: Human (GENE) vs mouse (Gene), different ID types
**Solutions**:
- Download species-specific GMT from MSigDB
- Check `rownames(seurat_object)`
- Ensure consistent formatting (uppercase for human)

## Best Practices
1. Start with Hallmark for quick, interpretable results
2. Use `log2_ratio_of_classes` for log-scale RNA-seq data
3. Adjust `minsize`/`maxsize` based on database and research question
4. Use multiple databases for comprehensive coverage
5. Verify gene names match between Seurat and GMT files
6. Use `each` parameter for multiple subgroup comparisons
7. Set `top < 1` for p-value-based filtering
8. Validate cell counts before running GSEA
9. Parallelize with `ncores` for large datasets
10. Cache results when testing visualization parameters

## External References
- **fgsea**: https://bioconductor.org/packages/release/bioc/html/fgsea.html
- **MSigDB**: https://www.gsea-msigdb.org/gsea/msigdb/
- **enrichit**: https://pwwang.github.io/enrichit/reference/FetchGMT.html
- **GSEA paper**: Subramanian et al. 2005, PNAS

## Related Processes
- **ClusterMarkers**: Differential expression (provides ranked genes)
- **MarkersFinder**: Flexible marker finding with GSEA
- **PseudoBulkDEG**: Bulk-like DE with GSEA
- **ModuleScoreCalculator**: Score pathway genes across cells
