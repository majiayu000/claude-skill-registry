---
name: scrnametaboliclandscape
description: Comprehensive metabolic landscape analysis pipeline for scRNA-seq data. This is an all-in-one process group performing complete metabolic pathway analysis including expression imputation, feature selection, pathway activity calculation, and heterogeneity analysis. Based on methodology from Xiao et al.
---

# ScrnaMetabolicLandscape Process Configuration

## Purpose
Comprehensive metabolic landscape analysis pipeline for scRNA-seq data. This is an all-in-one process group performing complete metabolic pathway analysis including expression imputation, feature selection, pathway activity calculation, and heterogeneity analysis. Based on methodology from Xiao et al. (2019) Nature Communications.

**Key difference from individual Metabolic* processes**: ScrnaMetabolicLandscape runs multiple related metabolic analysis steps as a coordinated workflow. Use this for complete metabolic analysis pipeline. Use individual processes (MetabolicInput, MetabolicExprImputation, MetabolicFeatures, MetabolicPathwayActivity, MetabolicPathwayHeterogeneity) for fine-grained control or specific steps only.

## When to Use
- **Complete metabolic analysis workflow**: Need all metabolic landscape analyses (imputation → activity → heterogeneity → features)
- **Comprehensive metabolic profiling**: Study metabolic heterogeneity across cell clusters or conditions
- **Pathway-centric analysis**: Have metabolic pathway gene sets (GMT files) and want to explore pathway activity
- **Comparative metabolic analysis**: Compare metabolic states across different cell types, treatments, or disease conditions
- **Alternative to individual Metabolic* processes**: Prefer this group for simplicity, individual processes for customization

## Configuration Structure

### Process Enablement
```toml
[ScrnaMetabolicLandscape]
cache = true
```

### Input Specification
```toml
[ScrnaMetabolicLandscape.in]
srtobj = ["SeuratClustering"]  # Input from upstream clustering process
```

**Note**: Input is automatically wired from `CombinedInput`. The `metafile` argument (used in standalone biopipen) is set via pipeline configuration.

### Environment Variables
```toml
[ScrnaMetabolicLandscape.envs]
# Core configuration
gmtfile = "path/to/metabolic_pathways.gmt"  # Required: GMT file with metabolic pathways
group_by = "seurat_clusters"                 # Required: Column to group cells (e.g., "cluster", "seurat_clusters")
subset_by = "treatment"                      # Optional: Subset data by metadata column

# Imputation settings
noimpute = false                            # Skip imputation if set to true

# Metadata transformations
mutaters = {}                               # dict - Add new columns using R expressions
# Example: {"timepoint": "if_else(treatment == 'control', 'pre', 'post')"}

# Performance
ncores = 1                                   # Number of cores for parallelization (inherited by all sub-processes)
```

**GMT file sources**:
- Bader Lab: https://download.baderlab.org/EM_Genesets/current_release/Human/symbol/
- Original repository: https://github.com/LocasaleLab/Single-Cell-Metabolic-Landscape/blob/master/Data/KEGG_metabolism.gmt
- Custom GMT files can be used - ensure gene symbols match your Seurat object

### Individual Process Configuration

#### MetabolicExprImputation (Dropout Imputation)
```toml
[ScrnaMetabolicLandscape.MetabolicExprImputation.envs]
tool = "alra"                                # Choice: "alra", "scimpute", "rmagic"
alra_args = {}                                # Additional RunALRA() parameters
```

**Imputation tools**: `alra` (fast, recommended), `scimpute` (accurate, slow), `rmagic` (diffusion-based).

#### MetabolicFeatures (Pathway Enrichment)
```toml
[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
prerank_method = "signal_to_noise"           # Gene ranking: signal_to_noise, abs_signal_to_noise, t_test, ratio_of_classes, diff_of_classes, log2_ratio_of_classes
comparisons = []                             # Specific group comparisons (empty = all pairwise)
fgsea_args = {}                              # Additional fgsea parameters: { "minSize": 15, "maxSize": 500 }
```

#### MetabolicPathwayActivity (Pathway Scores)
```toml
[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs]
ntimes = 5000                                # Number of permutations for p-value estimation
```

#### MetabolicPathwayHeterogeneity (Heterogeneity Analysis)
```toml
[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs]
select_pcs = 0.8                             # Proportion of variance to select PCs
pathway_pval_cutoff = 0.01                   # P-value cutoff for enriched pathways
fgsea_args = { scoreType = "std", nproc = 1 }
```

## Configuration Examples

### Minimal Configuration
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.in]
srtobj = ["SeuratClustering"]

[ScrnaMetabolicLandscape.envs]
gmtfile = "pathways/KEGG_metabolism.gmt"
group_by = "seurat_clusters"
```

### Complete Metabolic Analysis
```toml
[ScrnaMetabolicLandscape]
cache = true

[ScrnaMetabolicLandscape.in]
srtobj = ["SeuratClustering"]

[ScrnaMetabolicLandscape.envs]
gmtfile = "https://download.baderlab.org/EM_Genesets/current_release/Human/symbol/KEGG_2021_Human_symbol.gmt"
group_by = "seurat_clusters"
subset_by = "treatment"
mutaters = { "timepoint" = "if_else(treatment == 'control', 'pre', 'post')" }
ncores = 4
noimpute = false

[ScrnaMetabolicLandscape.MetabolicExprImputation.envs]
tool = "alra"

[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs]
ntimes = 10000

[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
prerank_method = "log2_ratio_of_classes"
fgsea_args = { minSize = 15, maxSize = 500 }
comparisons = ["0", "1"]
```

### Multiple Analysis Cases
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "pathways/KEGG_metabolism.gmt"
group_by = "seurat_clusters"

# Case 1: Treatment comparison
[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs.cases.Treatment]
subset_by = "treatment"
group_by = "seurat_clusters"

# Case 2: Response comparison
[ScrnaMetabolicLandscape.MetabolicFeatures.envs.cases.Response]
subset_by = "response"
group_by = "seurat_clusters"
prerank_method = "signal_to_noise"
```

## Common Patterns

### Pattern 1: Standard Metabolic Workflow
All metabolic analysis steps with minimal customization:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.in]
srtobj = ["SeuratClustering"]

[ScrnaMetabolicLandscape.envs]
gmtfile = "pathways/KEGG_metabolism.gmt"
group_by = "seurat_clusters"
ncores = 4
```

### Pattern 2: Focused Pathway Analysis
Compare only specific groups:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "pathways/KEGG_metabolism.gmt"
group_by = "seurat_clusters"

[ScrnaMetabolicLandscape.MetabolicFeatures.envs]
comparisons = ["0", "1"]  # Compare cluster 0 and 1 against others
```

### Pattern 3: Skip Imputation
When you don't want to impute dropout values:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "pathways/KEGG_metabolism.gmt"
group_by = "seurat_clusters"
noimpute = true
```

## Metabolic Analysis Pipeline Steps

1. **MetabolicInput**: Passes Seurat object to downstream processes
2. **MetabolicExprImputation**: Imputes missing expression values (ALRA/scImpute/MAGIC)
3. **MetabolicPathwayActivity**: Calculates pathway activity scores with heatmaps and violin plots
4. **MetabolicPathwayHeterogeneity**: Analyzes pathway heterogeneity using permutation-based NES
5. **MetabolicFeatures**: Detailed GSEA enrichment analysis with summary and enrichment plots

## Dependencies
- **Upstream**: `CombinedInput` (requires `SeuratClustering` or equivalent)
- **Downstream**: None (terminal analysis group)
- **Data requirements**: Seurat object with normalized expression and metadata columns

## Validation Rules
- **GMT file**: Must be valid GMT format with gene symbols matching Seurat object gene names
- **group_by column**: Must exist in Seurat object metadata
- **subset_by column** (if specified): Must exist in Seurat object metadata, NA values will be removed
- **Expression data**: Seurat object must have normalized expression data (typically after SeuratClustering)

## Troubleshooting

### Issue: Gene name mismatch in GMT file
**Symptom**: No pathways enriched or warning about missing genes
**Solution**: Ensure GMT file uses same gene identifier type as your Seurat object (e.g., HGNC symbols for human, MGI symbols for mouse).

### Issue: Imputation takes too long
**Symptom**: MetabolicExprImputation process runs for hours
**Solution**: Use `tool = "alra"` (fastest) or skip imputation with `noimpute = true`.

### Issue: No significant pathways
**Symptom**: All pathways have high p-values or no enrichment
**Solution**: Check `fgsea_args` (adjust minSize/maxSize), try different `prerank_method`, verify group_by column has sufficient differences.

### Issue: Out of memory errors
**Symptom**: Process fails during permutation or GSEA
**Solution**: Reduce `ntimes` (default 5000 → 1000) or reduce `ncores` to limit parallel memory usage.

### Issue: Subset has no cells after filtering
**Symptom**: Warning about empty subsets or missing groups
**Solution**: Check `subset_by` column for NA values or mismatched categories. Use `mutaters` to clean metadata.

## External References

### Original Paper
Xiao, Zhengtao, Ziwei Dai, and Jason W. Locasale. "Metabolic landscape of tumor microenvironment at single cell resolution." Nature communications 10.1 (2019): 1-12. https://www.nature.com/articles/s41467-019-11738-0

### GMT File Sources
- Bader Lab: https://download.baderlab.org/EM_Genesets/current_release/Human/symbol/
- KEGG pathways: https://www.genome.jp/kegg/
- Reactome: https://reactome.org/
- GSEA MSigDB: https://www.gsea-msigdb.org/gsea/msigdb/

### Tools
- **fgsea**: https://rdrr.io/bioc/fgsea/man/fgsea.html - Fast preranked GSEA
- **Seurat ALRA**: https://satijalab.org/seurat/reference/runalra - Low-rank approximation imputation
- **scImpute**: https://github.com/vvnathan/scImpute - Cell-specific imputation
- **MAGIC**: https://github.com/KrishnaswamyLab/MAGIC - Diffusion-based imputation

### biopipen Documentation
- Scrna metabolic pipeline: https://pwwang.github.io/biopipen/pipelines/scrna_metabolic/
- Process API: https://pwwang.github.io/biopipen/api/biopipen.ns.scrna_metabolic_landscape/
- Plotthis: https://pwwang.github.io/plotthis/reference/
