---
name: metabolicpathwayactivity
description: Calculates pathway activity scores for metabolic pathways across different cell groups and subsets. This process quantifies the metabolic activity of each pathway per group, generating visualizations (heatmaps and violin plots) to compare metabolic states between clusters or conditions. Based on the methodology from Xiao et al.
---

# MetabolicPathwayActivity Process Configuration

## Purpose
Calculates pathway activity scores for metabolic pathways across different cell groups and subsets. This process quantifies the metabolic activity of each pathway per group, generating visualizations (heatmaps and violin plots) to compare metabolic states between clusters or conditions. Based on the methodology from Xiao et al. (2019) Nature Communications.

## When to Use
- **Third step in metabolic workflow**: After MetabolicInput and MetabolicExprImputation (optional)
- **To quantify pathway-level metabolism**: When you need scores for each metabolic pathway per group
- **Compare metabolic states**: To identify differences in pathway activity between clusters, treatments, or conditions
- **Metabolic profiling visualization**: When you need heatmaps showing pathway activity across groups and violin plots showing distribution
- **Comprehensive metabolic analysis**: As part of the ScrnaMetabolicLandscape group for complete metabolic landscape analysis

## Configuration Structure

### Process Enablement
MetabolicPathwayActivity is part of the ScrnaMetabolicLandscape group. Enable it by enabling the group:
```toml
[ScrnaMetabolicLandscape]
cache = true
```

### Input Specification
MetabolicPathwayActivity receives input automatically from MetabolicInput:
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
group_by = "seurat_clusters"            # Column to group cells (e.g., "cluster")
subset_by = "treatment"                 # Optional: Subset by metadata column
ncores = 1                              # Number of cores for parallelization
```

#### MetabolicPathwayActivity-Specific Configuration
```toml
[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs]
# Statistical analysis
ntimes = 5000                          # Number of permutations for p-value estimation

# Plot customization (default plots)
[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs.plots]
"Pathway Activity (violin plot)" = {
    plot_type = "violin",               # Options: "heatmap", "violin", "merged_heatmap"
    add_box = true,                     # Add box plot inside violin
    devpars = { res = 100 }             # Plot resolution
}
"Pathway Activity (heatmap)" = {
    plot_type = "heatmap",
    devpars = { res = 100 }
}
"All Subsets (merged)" = {
    plot_type = "merged_heatmap",       # All subsets in one plot
    devpars = { res = 100 }
}

# Multiple analysis cases (advanced)
[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs.cases]
"Treatment" = {
    subset_by = "treatment",            # Analyze by treatment groups
    group_by = "seurat_clusters",
    plots = { "Treatment Activity" = { plot_type = "violin", add_box = true } }
}
"Response" = {
    subset_by = "response",             # Analyze by response groups
    group_by = "seurat_clusters",
    plots = { "Response Activity" = { plot_type = "heatmap" } }
}
```

## Pathway Activity Scoring

### Scoring Method
MetabolicPathwayActivity uses **AUCell-like scoring** to calculate pathway activity:
- **AUCell-like**: Area Under the Curve calculation - ranks gene expression for each cell, then calculates area under the curve for genes in each pathway
- **Permutation-based p-values**: Uses `ntimes` permutations to estimate statistical significance
- **Normalized scores**: Scores are normalized to enable comparison across pathways and groups

### Scoring Process
1. **Gene ranking**: For each cell, genes are ranked by expression level
2. **Pathway AUC calculation**: For each pathway, calculate AUC using the ranking and pathway gene list
3. **Permutation testing**: Randomly permute gene rankings `ntimes` times to estimate null distribution
4. **P-value estimation**: Compare observed AUC to null distribution to calculate significance
5. **Score aggregation**: Aggregate cell-level scores to group-level scores for visualization

### GMT File Sources
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

### Custom Plots with High Resolution
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
group_by = "seurat_clusters"

[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs]
ntimes = 10000  # More permutations for robust p-values

[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs.plots]
"Activity Violin" = {
    plot_type = "violin",
    add_box = true,
    devpars = { width = 1200, height = 800, res = 150 }
}
"Activity Heatmap" = {
    plot_type = "heatmap",
    devpars = { width = 1400, height = 1000, res = 150 }
}
"Merged Heatmap" = {
    plot_type = "merged_heatmap",
    devpars = { width = 1600, height = 1200, res = 150 }
}
```

### Treatment Comparison Analysis
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
group_by = "seurat_clusters"
subset_by = "treatment"  # Compare between treatment groups

[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs]
ntimes = 5000
ncores = 4

[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs.plots]
"Treatment Violin" = { plot_type = "violin", add_box = true }
"Treatment Heatmap" = { plot_type = "heatmap" }
```

### Multiple Analysis Cases (Advanced)
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
group_by = "seurat_clusters"
ncores = 8

# Case 1: Treatment analysis
[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs.cases.Treatment]
subset_by = "treatment"
group_by = "seurat_clusters"
ntimes = 5000
plots = {
    "Treatment Activity" = { plot_type = "violin", add_box = true, devpars = { res = 150 } }
}

# Case 2: Response analysis
[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs.cases.Response]
subset_by = "response"
group_by = "seurat_clusters"
ntimes = 10000
plots = {
    "Response Heatmap" = { plot_type = "heatmap", devpars = { res = 150 } }
}
```

### Energy Metabolism Focus
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
# Use custom GMT focused on energy pathways
gmtfile = "/data/pathways/energy_metabolism.gmt"
group_by = "seurat_clusters"
ncores = 4

[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs]
ntimes = 10000

[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs.plots]
"Energy Pathways" = { plot_type = "heatmap", devpars = { res = 150 } }
```

## Common Patterns

### Pattern 1: All Pathways with Default Settings
Standard analysis with KEGG pathways:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
group_by = "seurat_clusters"
```

### Pattern 2: Energy Metabolism Focus (Glycolysis + OXPHOS)
Focus on specific energy pathways using custom GMT:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "/path/to/energy_pathways.gmt"
group_by = "seurat_clusters"

[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs]
ntimes = 5000

[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs.plots]
"Energy Activity" = { plot_type = "violin", add_box = true }
```

### Pattern 3: Multiple Condition Comparison
Compare metabolic activity across different conditions:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "Reactome_Pathways_2024"
group_by = "seurat_clusters"
subset_by = "condition"  # e.g., "control", "treatment_A", "treatment_B"

[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs]
ntimes = 10000

[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs.plots]
"Condition Comparison" = { plot_type = "heatmap" }
"Condition Distribution" = { plot_type = "violin", add_box = true }
"All Conditions" = { plot_type = "merged_heatmap" }
```

### Pattern 4: High-Throughput Screening
For large datasets requiring parallel processing:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
group_by = "seurat_clusters"
ncores = 16

[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs]
ntimes = 2000  # Fewer permutations for speed
```

### Pattern 5: Publication-Quality Plots
High-resolution plots for manuscripts:
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
group_by = "seurat_clusters"

[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs]
ntimes = 10000

[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs.plots]
"Pathway Activity Heatmap" = {
    plot_type = "heatmap",
    devpars = { width = 1600, height = 1200, res = 300 }
}
"Pathway Activity Violin" = {
    plot_type = "violin",
    add_box = true,
    devpars = { width = 1200, height = 800, res = 300 }
}
```

## Dependencies

### Upstream Processes
- **Required**: `MetabolicInput` (part of ScrnaMetabolicLandscape group)
- **Optional**: `MetabolicExprImputation` (if imputation enabled with `noimpute = false`)
- **Root**: `CombinedInput` → requires `SeuratClustering` or similar clustering process

### Downstream Processes
- **Parallel**: Runs alongside `MetabolicFeatures` and `MetabolicPathwayHeterogeneity` (same group)
- **Optional**: Can feed into visualization or reporting processes

### Data Requirements
- Seurat object with normalized expression data
- Metadata column specified in `group_by` (e.g., cluster assignments)
- Optional metadata column in `subset_by` for subset analysis
- GMT file with metabolic pathway gene sets matching Seurat object gene names

## Output Format

### Output Files
MetabolicPathwayActivity generates the following outputs in the `outdir` directory (default: `{{in.sobjfile | stem}}.pathwayactivity`):

- **Pathway activity scores**: Tab-delimited files with pathway activity scores per group
- **Heatmap plots**: PNG/PDF images showing pathway activity heatmaps
- **Violin plots**: PNG/PDF images showing pathway activity distribution
- **Merged heatmaps**: Combined heatmaps for all subsets (if configured)

### Score Interpretation
- **Higher scores**: Greater pathway activity in the group
- **Lower scores**: Lower pathway activity in the group
- **P-values**: Statistical significance (based on permutation testing)
- **Normalization**: Scores are normalized to enable cross-pathway comparison

## Validation Rules

### Input Validation
- `gmtfile` must be a valid enrichit database name OR accessible GMT file
- Gene names in GMT file must match Seurat object (case-sensitive)
- `group_by` column must exist in Seurat object metadata
- If `subset_by` specified, column must exist and NA values will be removed

### Parameter Validation
- `ntimes` must be positive integer (recommended: 1000-10000)
- `ncores` must be positive integer (adjust based on available CPU)
- Plot types must be valid: `heatmap`, `violin`, `merged_heatmap`

### Data Quality Validation
- Sufficient cells per group for meaningful score calculation (recommended: >10 cells)
- Gene overlap between GMT file and Seurat object (warning if too low)

## Troubleshooting

### Issue: Empty or all-zero pathway scores
**Cause**: Gene name mismatch between GMT file and Seurat object
**Solution**:
- Check gene format in Seurat: `sobj@assays$RNA@features[1:10,]` (R)
- Ensure case matches: Human (UPPERCASE) vs Mouse (TitleCase)
- Verify GMT file format: `name\tdescription\tgene1,gene2,gene3`

### Issue: Process too slow
**Cause**: High `ntimes` or insufficient `ncores`
**Solution**:
```toml
# Reduce permutations for faster analysis
[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs]
ntimes = 2000  # Default is 5000

# Increase cores for parallelization
[ScrnaMetabolicLandscape.envs]
ncores = 8  # Increase based on available CPU
```

### Issue: Out of memory errors
**Cause**: Large dataset with high `ncores`
**Solution**:
```toml
# Reduce cores to limit parallel memory usage
[ScrnaMetabolicLandscape.envs]
ncores = 2  # Reduce from default 1 if memory issues

# Reduce permutations
[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs]
ntimes = 1000
```

### Issue: No significant differences between groups
**Cause**: Groups have similar metabolic profiles or insufficient statistical power
**Solution**:
- Increase `ntimes` for more robust p-value estimation
- Verify `group_by` column captures meaningful biological differences
- Try different pathway database (e.g., KEGG → Reactome)
- Check subset groupings if using `subset_by`

### Issue: Subset has no cells after filtering
**Cause**: NA values in `subset_by` column or mismatched categories
**Solution**:
```toml
# Clean metadata before analysis
[ScrnaMetabolicLandscape.envs]
mutaters = {treatment_clean = "if_else(is.na(treatment), 'unknown', treatment)"}
subset_by = "treatment_clean"
```

### Issue: Heatmap not readable (too many pathways)
**Cause**: GMT file contains too many pathways for visualization
**Solution**:
```toml
# Use smaller pathway database or custom GMT with selected pathways
gmtfile = "/path/to/core_metabolism.gmt"  # Custom curated pathways
```

### Issue: Violin plots too crowded
**Cause**: Too many groups or pathways
**Solution**:
```toml
# Generate multiple plots with subsets
[ScrnaMetabolicLandscape.MetabolicPathwayActivity.envs.plots]
"Part 1" = {
    plot_type = "violin",
    add_box = true,
    # Additional filtering options via plotthis
}
# Or use merged_heatmap for overview
"Overview" = { plot_type = "merged_heatmap" }
```

## External References

### Original Paper
Xiao, Zhengtao, Ziwei Dai, and Jason W. Locasale. "Metabolic landscape of the tumor microenvironment at single cell resolution." Nature communications 10.1 (2019): 1-12. https://www.nature.com/articles/s41467-019-11738-0

### AUCell Method
AUCell: https://github.com/aertslab/AUCell - Area Under the Curve for gene set enrichment in single-cell data

### Plotthis Functions
- Heatmap: https://pwwang.github.io/plotthis/reference/Heatmap.html
- ViolinPlot: https://pwwang.github.io/plotthis/reference/ViolinPlot.html

### biopipen Documentation
- Metabolic pipeline: https://pwwang.github.io/biopipen/pipelines/scrna_metabolic/
- Process API: https://pwwang.github.io/biopipen/api/biopipen.ns.scrna_metabolic_landscape/

### Related Skills
- **ScrnaMetabolicLandscape**: `/skills/processes/scrnametaboliclandscape.md` - Full metabolic analysis group
- **MetabolicInput**: `/skills/processes/metabolicinput.md` - Input preparation and GMT databases
- **MetabolicFeatures**: Pathway enrichment analysis (FGSEA-based)
- **MetabolicPathwayHeterogeneity**: Pathway heterogeneity analysis
