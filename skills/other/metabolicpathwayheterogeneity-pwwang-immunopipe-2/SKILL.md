---
name: metabolicpathwayheterogeneity
description: Analyzes metabolic pathway heterogeneity within cell populations by calculating normalized enrichment scores (NES) for each pathway across different groups. Quantifies metabolic diversity and identifies pathways with variable activity patterns. Uses principal component analysis and GSEA to assess pathway heterogeneity, revealing subpopulation-specific metabolic states and transitions.
---

# MetabolicPathwayHeterogeneity Process Configuration

## Purpose
Analyzes metabolic pathway heterogeneity within cell populations by calculating normalized enrichment scores (NES) for each pathway across different groups. Quantifies metabolic diversity and identifies pathways with variable activity patterns. Uses principal component analysis and GSEA to assess pathway heterogeneity, revealing subpopulation-specific metabolic states and transitions.

## When to Use
- **Assess metabolic diversity**: When you need to quantify metabolic heterogeneity within clusters or conditions
- **Identify variable pathways**: To find which metabolic pathways show high vs low heterogeneity across groups
- **Compare metabolic variability**: To compare heterogeneity between treatments, timepoints, or cell types
- **After pathway activity analysis**: Complements MetabolicPathwayActivity by adding heterogeneity dimension
- **Final metabolic analysis step**: Typically the last process in the ScrnaMetabolicLandscape workflow
- **Subpopulation discovery**: When metabolic variability suggests hidden substructure

## Configuration Structure

### Process Enablement
MetabolicPathwayHeterogeneity is part of the ScrnaMetabolicLandscape group. Enable it by enabling the group:
```toml
[ScrnaMetabolicLandscape]
cache = true
```

### Input Specification
MetabolicPathwayHeterogeneity receives input automatically from MetabolicInput (or MetabolicExprImputation if imputation enabled):
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

#### MetabolicPathwayHeterogeneity-Specific Configuration
```toml
[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs]
# Principal component selection for heterogeneity analysis
select_pcs = 0.8                      # Fraction or number of PCs to use (0-1 = fraction, >1 = number)

# Pathway significance filtering
pathway_pval_cutoff = 0.01            # P-value cutoff to select enriched pathways

# Parallelization
ncores = 1                            # Cores for parallel processing (inherited from group if not set)

# fgsea parameters
[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs.fgsea_args]
scoreType = "std"                     # Options: "std", "pos", "neg"
nproc = 1                             # fgsea internal parallelization
minSize = 15                          # Minimum pathway size
maxSize = 500                         # Maximum pathway size

# Plots configuration
[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs.plots]
"Pathway Heterogeneity" = {
    plot_type = "dot",                 # Options: dot, heatmap
    devpars = { res = 100 }            # Plot resolution
}

# Multiple analysis cases (advanced)
[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs.cases]
"Treatment" = {
    subset_by = "treatment",
    group_by = "seurat_clusters",
    select_pcs = 0.8,
    pathway_pval_cutoff = 0.01
}
```

## Heterogeneity Analysis Method

### Algorithm Overview
1. **PCA on pathway scores**: Principal component analysis on pathway activity scores per group
2. **PC selection**: Select top PCs explaining variance (controlled by `select_pcs`)
3. **GSEA on PCs**: Run fgsea for each PC to identify pathways correlating with variance
4. **NES calculation**: Normalized Enrichment Score quantifies pathway-PC association
5. **Heterogeneity metric**: Pathways with high |NES| show high heterogeneity across groups

### PC Selection (`select_pcs`)

| Value | Interpretation | Use Case |
|-------|----------------|----------|
| **0.8** (default) | Use PCs explaining 80% variance | Balanced approach |
| **0.5** | Use PCs explaining 50% variance | Focus on major variation sources |
| **0.95** | Use PCs explaining 95% variance | Comprehensive analysis (slower) |
| **5** (integer) | Use exactly 5 PCs | Manual control |
| **10** | Use exactly 10 PCs | Fine-grained heterogeneity |

**Recommendation**: Start with `0.8` (default), increase to `0.9-0.95` if you suspect hidden heterogeneity.

### Pathway P-value Cutoff

```toml
pathway_pval_cutoff = 0.01  # Only pathways with p < 0.01 are analyzed
```

- **Purpose**: Filter to significantly enriched pathways before heterogeneity analysis
- **Lower values** (0.001): Strict, only highly significant pathways
- **Higher values** (0.05): Permissive, include more pathways
- **Default (0.01)**: Good balance for most analyses

### FGSEA Score Type

```toml
[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs.fgsea_args]
scoreType = "std"  # Options: "std", "pos", "neg"
```

| Score Type | Description | Use Case |
|------------|-------------|----------|
| **std** | Standard GSEA (both directions) | Default; detects heterogeneity in both high/low activity |
| **pos** | Only positive enrichment | Focus on pathways with increased activity variation |
| **neg** | Only negative enrichment | Focus on pathways with decreased activity variation |

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

### Comprehensive Heterogeneity Analysis
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
group_by = "seurat_clusters"
ncores = 8

[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs]
select_pcs = 0.95                      # Capture 95% of variance
pathway_pval_cutoff = 0.01             # Significant pathways only
ncores = 8

[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs.fgsea_args]
scoreType = "std"
nproc = 8
minSize = 10
maxSize = 500
```

### Treatment Comparison Heterogeneity
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "Reactome_Pathways_2024"
group_by = "seurat_clusters"
subset_by = "treatment"                # Compare heterogeneity between treatments

[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs]
select_pcs = 0.8
pathway_pval_cutoff = 0.05             # More permissive for exploratory analysis

[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs.plots]
"Treatment Heterogeneity" = {
    plot_type = "dot",
    devpars = { width = 1200, height = 800, res = 150 }
}
```

### High-Resolution Publication Plots
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
group_by = "seurat_clusters"

[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs]
select_pcs = 10                        # Use exactly 10 PCs
pathway_pval_cutoff = 0.01

[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs.plots]
"Pathway Heterogeneity" = {
    plot_type = "dot",
    devpars = { width = 1600, height = 1200, res = 300 }
}
```

### Multiple Analysis Cases
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
ncores = 8

# Case 1: Overall cluster heterogeneity
[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs.cases.Clusters]
group_by = "seurat_clusters"
select_pcs = 0.8
pathway_pval_cutoff = 0.01
plots = {
    "Cluster Heterogeneity" = { plot_type = "dot", devpars = { res = 150 } }
}

# Case 2: Treatment-specific heterogeneity
[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs.cases.Treatment]
subset_by = "treatment"
group_by = "seurat_clusters"
select_pcs = 0.9
pathway_pval_cutoff = 0.01
plots = {
    "Treatment Heterogeneity" = { plot_type = "dot", devpars = { res = 150 } }
}
```

### Conservative Analysis (Major Variance Only)
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
group_by = "seurat_clusters"

[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs]
select_pcs = 0.5                       # Only major variance (50%)
pathway_pval_cutoff = 0.001            # Very strict significance

[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs.fgsea_args]
scoreType = "std"
minSize = 20                           # Larger pathways only
maxSize = 300
```

## Common Patterns

### Pattern 1: Standard Heterogeneity Analysis
Assess metabolic variability across clusters:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
group_by = "seurat_clusters"

[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs]
select_pcs = 0.8
pathway_pval_cutoff = 0.01
```

### Pattern 2: Treatment Response Variability
Compare heterogeneity between responders and non-responders:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "Reactome_Pathways_2024"
subset_by = "response"                 # "responder" vs "nonresponder"
group_by = "seurat_clusters"

[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs]
select_pcs = 0.85
pathway_pval_cutoff = 0.01
```

### Pattern 3: Timepoint Progression
Analyze heterogeneity changes over time:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
subset_by = "timepoint"                # e.g., "day0", "day7", "day14"
group_by = "seurat_clusters"

[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs]
select_pcs = 0.9                       # Comprehensive to detect gradual changes
pathway_pval_cutoff = 0.01
```

### Pattern 4: Energy Metabolism Focus
Analyze heterogeneity in glycolysis and OXPHOS:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "/data/pathways/energy_metabolism.gmt"  # Custom GMT
group_by = "seurat_clusters"

[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs]
select_pcs = 0.8
pathway_pval_cutoff = 0.05             # More permissive for focused analysis

[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs.fgsea_args]
minSize = 5                            # Allow smaller custom pathways
```

### Pattern 5: High-Throughput Parallel Execution
Large dataset with many groups:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
group_by = "seurat_clusters"
ncores = 16

[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs]
select_pcs = 0.8
ncores = 16

[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs.fgsea_args]
nproc = 1  # Parallelize at group level, not within fgsea
```

## Dependencies

### Upstream Processes
- **Required**: `MetabolicInput` (part of ScrnaMetabolicLandscape group)
- **Optional**: `MetabolicExprImputation` (if imputation enabled with `noimpute = false`)
- **Root**: `CombinedInput` → requires `SeuratClustering` or similar clustering process

### Downstream Processes
- **Parallel**: Runs alongside `MetabolicPathwayActivity` and `MetabolicFeatures` (same group)
- **Typically final**: Usually the last metabolic analysis step
- **Optional**: Can feed into visualization or reporting processes

### Data Requirements
- Seurat object with normalized expression data
- Metadata column specified in `group_by` (e.g., cluster assignments)
- Optional metadata column in `subset_by` for subset analysis
- GMT file with metabolic pathway gene sets matching Seurat object gene names
- Multiple groups required (>2) for meaningful heterogeneity analysis

## Output Format

### Output Files
MetabolicPathwayHeterogeneity generates the following outputs in the `outdir` directory (default: `{{in.sobjfile | stem}}.pathwayhetero`):

- **Heterogeneity scores**: TSV files with NES per pathway and PC
  - Columns: pathway, PC1_NES, PC1_pval, PC2_NES, PC2_pval, ...
- **Dot plots**: Visualization of pathway heterogeneity across groups and subsets
- **PCA results**: PC variance explained, loadings
- **Pathway rankings**: Pathways ranked by heterogeneity magnitude

### Result Interpretation
- **High |NES|**: Pathway shows high heterogeneity (variable activity across groups)
- **Low |NES|**: Pathway shows low heterogeneity (uniform activity across groups)
- **Positive NES**: Pathway correlated with PC (increases along PC axis)
- **Negative NES**: Pathway anti-correlated with PC (decreases along PC axis)
- **P-value**: Statistical significance of pathway-PC association

### Biological Interpretation
- **High heterogeneity pathways**: Indicate metabolic subpopulations or transitions
- **Low heterogeneity pathways**: Indicate core/constitutive metabolism
- **Group-specific patterns**: Suggest differential metabolic regulation
- **PC loadings**: Reveal metabolic axes of variation

## Validation Rules

### Input Validation
- `gmtfile` must be a valid enrichit database name OR accessible GMT file
- Gene names in GMT file must match Seurat object (case-sensitive)
- `group_by` column must exist in Seurat object metadata
- If `subset_by` specified, column must exist and NA values will be removed

### Parameter Validation
- `select_pcs`: If 0 < value <= 1, interpreted as fraction; if > 1, interpreted as number
- `pathway_pval_cutoff`: Must be between 0 and 1 (typically 0.001-0.1)
- `ncores`: Must be positive integer
- At least 2 groups required in `group_by` for heterogeneity analysis

### FGSEA Validation
- `scoreType` must be one of: "std", "pos", "neg"
- `minSize` < `maxSize`
- `minSize` >= 1
- At least one pathway must meet size and significance criteria

## Troubleshooting

### Issue: All heterogeneity scores are zero or very low
**Cause**: Groups have similar metabolic profiles or insufficient variance
**Solution**:
```toml
# Increase PC capture
[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs]
select_pcs = 0.95  # Capture more variance

# Relax pathway significance
pathway_pval_cutoff = 0.05

# Check if groups are truly different
# May need to refine group_by or subset_by columns
```

### Issue: Process too slow
**Cause**: High `select_pcs` or insufficient parallelization
**Solution**:
```toml
# Reduce PCs
[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs]
select_pcs = 0.7  # Use fewer PCs

# Increase parallelization
ncores = 8

[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs.fgsea_args]
nproc = 8
```

### Issue: No significant pathways after filtering
**Cause**: `pathway_pval_cutoff` too strict or weak biological signal
**Solution**:
```toml
# Relax cutoff
[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs]
pathway_pval_cutoff = 0.05  # Increase from 0.01

# Or reduce pathway size filters
[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs.fgsea_args]
minSize = 10
maxSize = 800
```

### Issue: Memory errors during PCA
**Cause**: Too many pathways or groups
**Solution**:
```toml
# Reduce number of PCs
[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs]
select_pcs = 5  # Use fixed small number

# Or filter pathways more aggressively
pathway_pval_cutoff = 0.001

# Reduce parallelization
ncores = 2
```

### Issue: Results don't make biological sense
**Cause**: Inappropriate PC selection or wrong grouping variable
**Solution**:
```toml
# Try different PC thresholds
select_pcs = 0.8  # Default
# vs
select_pcs = 10    # Fixed number

# Verify grouping variable is biologically meaningful
group_by = "refined_clusters"  # More biologically relevant than raw seurat_clusters

# Check if subset_by is creating meaningful comparisons
subset_by = "cell_type"  # More specific than "treatment"
```

### Issue: Dot plot unreadable (too many pathways)
**Cause**: Too many significant pathways
**Solution**:
```toml
# Stricter filtering
[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs]
pathway_pval_cutoff = 0.001  # Very strict

# Or use custom GMT with fewer pathways
[ScrnaMetabolicLandscape.envs]
gmtfile = "/data/pathways/core_metabolism.gmt"

# Increase plot size
[ScrnaMetabolicLandscape.MetabolicPathwayHeterogeneity.envs.plots]
"Pathway Heterogeneity" = {
    plot_type = "dot",
    devpars = { width = 2000, height = 1500, res = 150 }
}
```

### Issue: Gene name mismatch errors
**Cause**: GMT file gene names don't match Seurat object
**Solution**:
- Check gene format: Human (UPPERCASE), Mouse (TitleCase)
- Verify GMT file format: `name\tdescription\tgene1\tgene2\tgene3`
- Ensure gene IDs match (e.g., both ENSEMBL or both symbols)

### Issue: Insufficient groups for heterogeneity analysis
**Cause**: Only 1-2 groups in `group_by` column
**Solution**:
```toml
# Use different grouping variable with more groups
[ScrnaMetabolicLandscape.envs]
group_by = "seurat_clusters"  # Should have >2 clusters

# Or add subset_by to create comparisons
subset_by = "treatment"  # Creates multiple group sets
```

### Issue: PCA explains very little variance
**Cause**: Pathways have little variation across groups
**Solution**:
- Verify upstream pathway activity analysis completed successfully
- Check if groups are truly metabolically distinct
- Try different pathway database (e.g., KEGG → Reactome)
- Consider different `group_by` variable

## External References

### Original Paper
**Metabolic landscape methodology**:
- Xiao, Z. et al. (2019). Metabolic landscape of the tumor microenvironment at single cell resolution. Nature Communications, 10, 3763. https://www.nature.com/articles/s41467-019-11738-0

### Analytical Methods
**PCA (Principal Component Analysis)**:
- Standard dimensionality reduction technique for identifying axes of variation
- https://en.wikipedia.org/wiki/Principal_component_analysis

**GSEA (Gene Set Enrichment Analysis)**:
- Subramanian, A. et al. (2005). Gene set enrichment analysis. PNAS, 102(43), 15545-15550. https://www.pnas.org/doi/10.1073/pnas.0506580102

**fgsea (Fast GSEA)**:
- Korotkevich, G. et al. (2021). Fast gene set enrichment analysis. bioRxiv. https://www.biorxiv.org/content/10.1101/060012v3

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
- **MetabolicFeatures**: `/skills/processes/metabolicfeatures.md` - Pathway enrichment analysis (FGSEA-based)

## Decision Tree for Heterogeneity Analysis

```
Start: MetabolicPathwayHeterogeneity
│
├─ Do groups show obvious metabolic differences?
│  ├─ YES → Use default settings (select_pcs = 0.8)
│  └─ NO → Increase PC capture (select_pcs = 0.95)
│
├─ How many groups in analysis?
│  ├─ 2-5 groups → Use select_pcs = 0.8 (major variance)
│  ├─ 6-10 groups → Use select_pcs = 0.85 (balanced)
│  └─ >10 groups → Use select_pcs = 0.9 (comprehensive)
│
├─ Exploratory vs confirmatory analysis?
│  ├─ Exploratory → pathway_pval_cutoff = 0.05 (permissive)
│  └─ Confirmatory → pathway_pval_cutoff = 0.01 (default)
│
└─ Computational resources available?
   ├─ Limited → select_pcs = 0.7, ncores = 2
   ├─ Moderate → select_pcs = 0.8, ncores = 4
   └─ Abundant → select_pcs = 0.95, ncores = 16
```

## Interpretation Guide

### High Heterogeneity Pathways (|NES| > 2)
- **Biological significance**: Indicates metabolic subpopulations or transitional states
- **Follow-up**: Investigate which groups drive heterogeneity (check PC loadings)
- **Examples**: Glycolysis (Warburg effect heterogeneity), fatty acid oxidation (metabolic flexibility)

### Low Heterogeneity Pathways (|NES| < 1)
- **Biological significance**: Core/constitutive metabolism shared across groups
- **Follow-up**: May serve as normalizing factors or housekeeping metabolism
- **Examples**: Basic nucleotide metabolism, core TCA cycle

### PC Interpretation
- **PC1**: Usually captures major metabolic axis (e.g., proliferative vs quiescent)
- **PC2-3**: Secondary axes (e.g., treatment response, differentiation state)
- **Higher PCs**: Fine-grained variation or technical noise

### Comparing Cases
When using multiple cases (e.g., treatment vs control):
- **Similar heterogeneity**: Pathway variability intrinsic to cell populations
- **Differential heterogeneity**: Treatment-induced metabolic plasticity or restriction
