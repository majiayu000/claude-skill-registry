---
name: metabolicfeatures
description: Performs enrichment analysis (GSEA-based) for metabolic pathways across different cell groups to identify significantly enriched pathways. Uses fast gene set enrichment analysis (fgsea package) to rank pathways by their association with specific clusters, conditions, or cell states. Generates summary plots and enrichment visualizations for biological interpretation.
---

# MetabolicFeatures Process Configuration

## Purpose
Performs enrichment analysis (GSEA-based) for metabolic pathways across different cell groups to identify significantly enriched pathways. Uses fast gene set enrichment analysis (fgsea package) to rank pathways by their association with specific clusters, conditions, or cell states. Generates summary plots and enrichment visualizations for biological interpretation.

## When to Use
- **Identify differentially active pathways**: When you need to find which metabolic pathways are enriched in specific cell groups
- **Compare pathway enrichment**: To identify metabolic differences between clusters, treatments, or conditions
- **After pathway activity scoring**: Complements MetabolicPathwayActivity by providing statistical enrichment (p-values, FDR)
- **Part of ScrnaMetabolicLandscape**: Runs in parallel with MetabolicPathwayActivity and MetabolicPathwayHeterogeneity
- **GSEA-based analysis**: When you want enrichment scores based on ranked gene lists (signal-to-noise, t-test, fold change)

## Configuration Structure

### Process Enablement
MetabolicFeatures is part of the ScrnaMetabolicLandscape group. Enable it by enabling the group:
```toml
[ScrnaMetabolicLandscape]
cache = true
```

### Input Specification
MetabolicFeatures receives input automatically from MetabolicInput (or MetabolicExprImputation if imputation enabled):
```toml
[ScrnaMetabolicLandscape.in]
srtobj = ["SeuratClustering"]  # Input from upstream clustering process
```

### Environment Variables
All configuration is done at the ScrnaMetabolicLandscape group level:

```toml
[ScrnaMetabolicLandscape.envs]
# Core configuration (inherited by all metabolic processes)
gmtfile = "KEGG_2021_Human"           # Metabolic pathways database
group_by = "seurat_clusters"          # Column to group cells (e.g., "cluster")
subset_by = "treatment"               # Optional: Subset by metadata column
ncores = 1                            # Number of cores for parallelization
```

#### MetabolicFeatures-Specific Configuration
```toml
[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
# Gene ranking method for GSEA
prerank_method = "signal_to_noise"    # Options: signal_to_noise, abs_signal_to_noise, t_test, ratio_of_classes, diff_of_classes, log2_ratio_of_classes
ncores = 1                            # Cores for parallel fgsea execution

# Comparison groups (optional - defaults to all vs all)
comparisons = []                      # e.g., ["1", "2"] or ["1:2", "1:3"]

# fgsea parameters
[ScrnaMetabolicLandscape.MetabolicFeatures.envs.fgsea_args]
minSize = 15                          # Minimum pathway size
maxSize = 500                         # Maximum pathway size
nproc = 1                             # fgsea internal parallelization

# Plots configuration
[ScrnaMetabolicLandscape.MetabolicFeatures.envs.plots]
"Summary Plot" = {
    plot_type = "summary",             # Options: summary, gsea, dot
    top_term = 10,                     # Number of top pathways to show
    devpars = { res = 100 }            # Plot resolution
}
"Enrichment Plots" = {
    plot_type = "gsea",                # GSEA enrichment plot
    top_term = 10,
    devpars = { res = 100 }
}

# Multiple analysis cases (advanced)
[ScrnaMetabolicLandscape.MetabolicFeatures.envs.cases]
"Treatment" = {
    subset_by = "treatment",
    group_by = "seurat_clusters",
    prerank_method = "signal_to_noise",
    comparisons = []
}
```

## Gene Ranking Methods (prerank_method)

### Available Methods

| Method | Code | Description | Use Case |
|--------|------|-------------|----------|
| **Signal to Noise** | `signal_to_noise` or `s2n` | (mean1 - mean2) / (sd1 + sd2) | Default; balanced approach |
| **Absolute S2N** | `abs_signal_to_noise` or `abs_s2n` | abs(signal_to_noise) | Magnitude-focused ranking |
| **T-test** | `t_test` | (mean1 - mean2) / SE | Statistical significance focus |
| **Ratio of Classes** | `ratio_of_classes` | mean1 / mean2 | Fold change (natural scale) |
| **Diff of Classes** | `diff_of_classes` | mean1 - mean2 | Absolute difference |
| **Log2 Ratio** | `log2_ratio_of_classes` | log2(mean1 / mean2) | Fold change (log scale, recommended for log-normalized data) |

### Method Selection Guide

**Signal to Noise (Default)**: Best for most analyses
- Accounts for both mean difference and variance
- Robust to outliers
- Recommended starting point

**T-test**: When statistical significance is priority
- Incorporates sample size
- Good for unbalanced groups

**Log2 Ratio**: For log-normalized data (Seurat default)
- Recommended for interpreting fold changes
- Standard in RNA-seq analysis

**Ratio/Diff of Classes**: For natural scale data
- Use if data is NOT log-normalized
- Direct fold change interpretation

## FGSEA Parameters

### Core Parameters

```toml
[ScrnaMetabolicLandscape.MetabolicFeatures.envs.fgsea_args]
minSize = 15           # Minimum genes in pathway (filter small pathways)
maxSize = 500          # Maximum genes in pathway (filter very broad pathways)
nproc = 1              # Internal fgsea parallelization (set to ncores for speedup)
eps = 1e-50            # Epsilon for p-value calculation (lower = more precise)
```

### FGSEA Algorithm
MetabolicFeatures uses the **fgsea** R package for fast GSEA:
- **Kolmogorov-Smirnov-like test**: Tests if pathway genes are enriched at top/bottom of ranked list
- **Permutation-based**: Generates null distribution by permuting gene labels
- **Normalized Enrichment Score (NES)**: Accounts for pathway size differences
- **FDR correction**: Multiple testing correction for significance

### Reference
fgsea documentation: https://rdrr.io/bioc/fgsea/man/fgsea.html

## Comparison Groups

### Automatic Comparisons (Default)
```toml
# Empty comparisons = all groups vs all groups
[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
comparisons = []  # Each group compared to all other groups
```

If `group_by = "seurat_clusters"` has clusters 1, 2, 3:
- Cluster 1 vs (2+3)
- Cluster 2 vs (1+3)
- Cluster 3 vs (1+2)

### Specific Groups
```toml
# Only analyze specific groups
comparisons = ["1", "2"]  # Only clusters 1 and 2 vs rest
```
Results:
- Cluster 1 vs (2+3+...)
- Cluster 2 vs (1+3+...)

### Pairwise Comparisons
```toml
# Explicit pairwise comparisons
comparisons = ["1:2", "1:3", "2:3"]
```
Results:
- Cluster 1 vs Cluster 2
- Cluster 1 vs Cluster 3
- Cluster 2 vs Cluster 3

## GMT File Sources

The `gmtfile` parameter accepts:
- **Built-in databases**: `"KEGG_2021_Human"`, `"Reactome_Pathways_2024"`, `"BioCarta_2016"`, `"MSigDB_Hallmark_2020"`
- **Custom files**: Local paths or URLs to GMT format files
- See `/skills/processes/metabolicinput.md` for detailed database options

## Configuration Examples

### Minimal Configuration (Default Settings)
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.in]
srtobj = ["SeuratClustering"]

[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
group_by = "seurat_clusters"
```

### Custom GSEA Parameters
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
group_by = "seurat_clusters"

[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
prerank_method = "log2_ratio_of_classes"  # Fold change for log-normalized data
ncores = 4

[ScrnaMetabolicLandscape.MetabolicFeatures.envs.fgsea_args]
minSize = 10     # Allow smaller pathways
maxSize = 300    # Restrict to core pathways
nproc = 4        # Parallel fgsea
```

### Pairwise Treatment Comparison
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "Reactome_Pathways_2024"
group_by = "treatment"
ncores = 8

[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
prerank_method = "t_test"
comparisons = ["control:treated", "control:resistant"]

[ScrnaMetabolicLandscape.MetabolicFeatures.envs.fgsea_args]
minSize = 15
maxSize = 500
nproc = 8
```

### High-Resolution Publication Plots
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
group_by = "seurat_clusters"

[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
prerank_method = "signal_to_noise"

[ScrnaMetabolicLandscape.MetabolicFeatures.envs.plots]
"Top Enriched Pathways" = {
    plot_type = "summary",
    top_term = 20,
    devpars = { width = 1600, height = 1200, res = 300 }
}
"GSEA Enrichment Curves" = {
    plot_type = "gsea",
    top_term = 10,
    devpars = { width = 1400, height = 1000, res = 300 }
}
```

### Multiple Analysis Cases
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
ncores = 8

# Case 1: Cluster-based enrichment
[ScrnaMetabolicLandscape.MetabolicFeatures.envs.cases.Clusters]
group_by = "seurat_clusters"
prerank_method = "signal_to_noise"
comparisons = []
plots = {
    "Cluster Enrichment" = { plot_type = "summary", top_term = 15, devpars = { res = 150 } }
}

# Case 2: Treatment response
[ScrnaMetabolicLandscape.MetabolicFeatures.envs.cases.Treatment]
subset_by = "response"
group_by = "treatment"
prerank_method = "log2_ratio_of_classes"
comparisons = ["responder:nonresponder"]
plots = {
    "Response Enrichment" = { plot_type = "gsea", top_term = 10, devpars = { res = 150 } }
}
```

## Common Patterns

### Pattern 1: Standard Pathway Enrichment
Identify enriched pathways per cluster:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
group_by = "seurat_clusters"

[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
prerank_method = "signal_to_noise"
```

### Pattern 2: Treatment vs Control
Compare metabolic enrichment between conditions:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "Reactome_Pathways_2024"
group_by = "treatment"

[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
prerank_method = "log2_ratio_of_classes"
comparisons = ["control:treated"]
```

### Pattern 3: Specific Pathway Focus
Analyze only glycolysis and OXPHOS:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "/data/pathways/glycolysis_oxphos.gmt"
group_by = "seurat_clusters"

[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
prerank_method = "signal_to_noise"

[ScrnaMetabolicLandscape.MetabolicFeatures.envs.fgsea_args]
minSize = 5   # Allow smaller custom pathways
```

### Pattern 4: Subset-Specific Analysis
Compare enrichment within T cell subsets only:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
subset_by = "celltype"  # Metadata column to subset by
group_by = "activation_state"

[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
prerank_method = "t_test"
# Will analyze only cells where celltype == "T cell"
```

### Pattern 5: High-Throughput Parallel Execution
Large dataset with many comparisons:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
group_by = "seurat_clusters"
ncores = 16

[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
prerank_method = "signal_to_noise"
ncores = 16

[ScrnaMetabolicLandscape.MetabolicFeatures.envs.fgsea_args]
nproc = 1  # Parallelize at comparison level, not within fgsea
```

## Dependencies

### Upstream Processes
- **Required**: `MetabolicInput` (part of ScrnaMetabolicLandscape group)
- **Optional**: `MetabolicExprImputation` (if imputation enabled with `noimpute = false`)
- **Root**: `CombinedInput` → requires `SeuratClustering` or similar clustering process

### Downstream Processes
- **Parallel**: Runs alongside `MetabolicPathwayActivity` and `MetabolicPathwayHeterogeneity` (same group)
- **Optional**: Can feed into visualization or reporting processes

### Data Requirements
- Seurat object with normalized expression data
- Metadata column specified in `group_by` (e.g., cluster assignments)
- Optional metadata column in `subset_by` for subset analysis
- GMT file with metabolic pathway gene sets matching Seurat object gene names

## Output Format

### Output Files
MetabolicFeatures generates the following outputs in the `outdir` directory (default: `{{in.sobjfile | stem}}.pathwayfeatures`):

- **GSEA results tables**: TSV files with pathway enrichment statistics (NES, p-value, FDR)
  - Columns: pathway, NES, pval, padj, ES, leading_edge, size
- **Summary plots**: Bar/dot plots showing top enriched pathways per comparison
- **GSEA enrichment plots**: Classic GSEA running enrichment score plots for top pathways
- **Dot plots**: Multi-comparison overviews (case/subset level)

### Result Interpretation
- **NES (Normalized Enrichment Score)**: Direction and magnitude of enrichment
  - Positive NES: Pathway enriched in group 1 (upregulated)
  - Negative NES: Pathway enriched in group 2 (downregulated)
  - Magnitude: Strength of enrichment (|NES| > 1.5 typically significant)
- **P-value**: Statistical significance (raw)
- **FDR (padj)**: Multiple testing corrected p-value (use this for significance)
- **Leading edge**: Core genes driving enrichment

## Validation Rules

### Input Validation
- `gmtfile` must be a valid enrichit database name OR accessible GMT file
- Gene names in GMT file must match Seurat object (case-sensitive)
- `group_by` column must exist in Seurat object metadata
- If `subset_by` specified, column must exist and NA values will be removed

### Parameter Validation
- `prerank_method` must be one of: signal_to_noise, s2n, abs_signal_to_noise, abs_s2n, t_test, ratio_of_classes, diff_of_classes, log2_ratio_of_classes
- `ncores` must be positive integer
- `comparisons` must be valid group names from `group_by` column

### FGSEA Validation
- `minSize` < `maxSize`
- `minSize` >= 1
- At least one pathway must meet size criteria after filtering

## Troubleshooting

### Issue: No significant pathways found
**Cause**: Weak biological signal or stringent filtering
**Solution**:
```toml
# Relax pathway size filters
[ScrnaMetabolicLandscape.MetabolicFeatures.envs.fgsea_args]
minSize = 5
maxSize = 1000

# Try different ranking method
[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
prerank_method = "log2_ratio_of_classes"
```

### Issue: Process too slow
**Cause**: Many comparisons or insufficient parallelization
**Solution**:
```toml
# Increase parallelization
[ScrnaMetabolicLandscape.envs]
ncores = 8

[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
ncores = 8

[ScrnaMetabolicLandscape.MetabolicFeatures.envs.fgsea_args]
nproc = 8  # Parallelize fgsea internally

# Or reduce comparison scope
comparisons = ["1:2", "1:3"]  # Only specific comparisons
```

### Issue: Gene name mismatch errors
**Cause**: GMT file gene names don't match Seurat object
**Solution**:
- Check gene format: Human (UPPERCASE), Mouse (TitleCase)
- Verify GMT file format: `name\tdescription\tgene1\tgene2\tgene3`
- Ensure gene IDs match (e.g., both ENSEMBL or both symbols)

### Issue: Empty or NA results for some comparisons
**Cause**: Insufficient cells in comparison groups
**Solution**:
```toml
# Check group sizes first
# Ensure each group has >30 cells for reliable statistics

# Or remove small groups
[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
comparisons = ["1", "2"]  # Exclude small cluster 3
```

### Issue: Plots are unreadable (too many pathways)
**Cause**: `top_term` too high or too many significant pathways
**Solution**:
```toml
# Reduce number of pathways shown
[ScrnaMetabolicLandscape.MetabolicFeatures.envs.plots]
"Summary Plot" = {
    plot_type = "summary",
    top_term = 5,  # Show only top 5 pathways
    devpars = { width = 1200, height = 600, res = 150 }
}
```

### Issue: Enrichment scores don't match expectations
**Cause**: Wrong ranking method for data type
**Solution**:
```toml
# For log-normalized Seurat data (default), use:
[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
prerank_method = "log2_ratio_of_classes"

# For raw/natural scale data, use:
prerank_method = "ratio_of_classes"
```

### Issue: Memory errors during fgsea
**Cause**: Too many pathways or parallel processes
**Solution**:
```toml
# Reduce parallelization
[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
ncores = 2

[ScrnaMetabolicLandscape.MetabolicFeatures.envs.fgsea_args]
nproc = 1

# Or filter pathways more aggressively
minSize = 20
maxSize = 300
```

## External References

### Original Papers
**fgsea algorithm**:
- Korotkevich, G. et al. (2021). Fast gene set enrichment analysis. bioRxiv. https://www.biorxiv.org/content/10.1101/060012v3

**GSEA methodology**:
- Subramanian, A. et al. (2005). Gene set enrichment analysis: A knowledge-based approach for interpreting genome-wide expression profiles. PNAS, 102(43), 15545-15550. https://www.pnas.org/doi/10.1073/pnas.0506580102

### Tool Documentation
- **fgsea package**: https://rdrr.io/bioc/fgsea/man/fgsea.html
- **biopipen VizGSEA**: https://pwwang.github.io/biopipen.utils.R/reference/VizGSEA.html
- **biopipen metabolic pipeline**: https://pwwang.github.io/biopipen/pipelines/scrna_metabolic/

### GMT Databases
- **MSigDB**: http://www.gsea-msigdb.org/gsea/msigdb/
- **KEGG**: https://www.genome.jp/kegg/pathway.html
- **Reactome**: https://reactome.org/
- **enrichit database list**: See `/skills/processes/metabolicinput.md`

### Related Skills
- **ScrnaMetabolicLandscape**: `/skills/processes/scrnametaboliclandscape.md` - Full metabolic analysis group
- **MetabolicInput**: `/skills/processes/metabolicinput.md` - Input preparation and GMT databases
- **MetabolicPathwayActivity**: `/skills/processes/metabolicpathwayactivity.md` - Pathway activity scoring (AUCell-based)
- **MetabolicPathwayHeterogeneity**: `/skills/processes/metabolicpathwayheterogeneity.md` - Heterogeneity analysis
