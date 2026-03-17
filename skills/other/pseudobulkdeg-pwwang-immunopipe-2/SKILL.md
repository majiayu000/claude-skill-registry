---
name: pseudobulkdeg
description: Performs pseudo-bulk differential gene expression analysis using DESeq2 or edgeR. Aggregates single-cell counts to sample-level pseudo-bulk data, then identifies differentially expressed genes between conditions while accounting for biological replicates. Supports complex experimental designs including batch effects, paired samples, and interaction terms.
---

# PseudoBulkDEG Process Configuration

## Purpose
Performs pseudo-bulk differential gene expression analysis using DESeq2 or edgeR. Aggregates single-cell counts to sample-level pseudo-bulk data, then identifies differentially expressed genes between conditions while accounting for biological replicates. Supports complex experimental designs including batch effects, paired samples, and interaction terms. Automatically runs pathway enrichment analysis on significant markers.

## When to Use
- **Robust differential expression**: When you need statistical rigor with biological replicates
- **Sample-level variation**: To account for sample-to-sample variability (not just cell-level)
- **Multiple comparisons**: Compare conditions across multiple samples, time points, or treatments
- **Batch correction**: Model and adjust for batch effects in differential expression
- **Paired samples**: When samples have natural pairing (e.g., same subject across time points)
- **Per-cell-type analysis**: Perform DEG separately for each cell type
- **Publication-quality results**: DESeq2 is the gold standard for bulk RNA-seq analysis

**Contrast with ClusterMarkers**:
- `ClusterMarkers`: Cell-level comparison (cluster vs cluster), no biological replicates
- `PseudoBulkDEG`: Sample-level comparison (condition vs condition), requires biological replicates

## Configuration Structure

### Process Enablement
```toml
[PseudoBulkDEG]
cache = true  # Cache intermediate results for faster re-runs

[PseudoBulkDEG.in]
srtobj = ["SeuratClustering"]  # Input Seurat object
```

### Environment Variables - Core Parameters

```toml
[PseudoBulkDEG.envs]
# Number of cores for parallel computation
ncores = 1  # int; Parallelize DESeq2/edgeR procedures

# Metadata mutators - add new columns for grouping
mutaters = {}  # json; Keys = new column names, Values = R expressions
# Example:
# mutaters = {Treatment = "ifelse(Timepoint > 2, 'Late', 'Early')"}

# Expand cases for each value in a column
each = ""  # str; Column name to create multiple DEG cases
# Example: each = "cell_type" creates one DEG case per cell type

# Cache location for intermediate steps
cache = "/tmp"  # str; Path, true (outdir), or false (no caching)

# Subset cells before pseudo-bulk aggregation
subset = ""  # str; R expression to filter cells
# Example: subset = "seurat_clusters %in% c('0', '1', '2')"

# How to aggregate cells into pseudo-bulk
aggregate_by = ""  # str; Column name(s) defining sample units
# Common: aggregate_by = "SampleID" or aggregate_by = "orig.ident"

# Data layer to aggregate
layer = "counts"  # str; Default: "counts"

# Assay to use (alternative to layer)
assay = ""  # str; Default: uses active assay

# Error on no markers/enrichment found
error = false  # bool; If true, fail when no significant results

# Column to group cells (defines comparison groups)
group_by = ""  # str; Metadata column for conditions
# Example: group_by = "Condition" or group_by = "Treatment"

# First group identity (reference level)
ident_1 = ""  # str; Value from group_by column

# Second group identity (comparison level)
ident_2 = ""  # str; Value from group_by column
# If not specified, compares ident_1 against all other groups

# Paired sample column (for paired tests)
paired_by = ""  # str; Column marking paired samples (e.g., "SubjectID")

# Differential expression tool
tool = "DESeq2"  # str; "DESeq2" or "edgeR"

# Enrichment analysis databases
dbs = ["KEGG_2021_Human", "MSigDB_Hallmark_2020"]  # list; Built-in or GMT paths

# Filter for significant markers (for enrichment)
sigmarkers = "p_val_adj < 0.05"  # str; dplyr filter expression

# Enrichment analysis style
enrich_style = "enrichr"  # str; "enrichr" or "clusterProfiler"
```

## DESeq2 Design Formulas

### Formula Syntax

DESeq2 uses R's formula syntax with the tilde (`~`) operator:

```
~ [main effects] [+ interactions]
```

**Key concepts:**
- `+`: Add main effects (terms modeled independently)
- `*`: Full factorial (main effects + interaction)
- `:`: Interaction term only
- Term order matters (last term is the primary comparison)

### Formula Patterns

#### 1. Simple Two-Group Comparison
```toml
[PseudoBulkDEG.envs]
# Compare Treatment vs Control
group_by = "Condition"
ident_1 = "Control"
ident_2 = "Treatment"
```
**Internal design formula**: `~ Condition`
**Interpretation**: Direct comparison between Control and Treatment

#### 2. Batch Correction
```toml
[PseudoBulkDEG.envs]
# Compare treatment groups while accounting for batch
group_by = "Treatment"
ident_1 = "Vehicle"
ident_2 = "Drug"
# Batch column must exist in metadata
# batch info automatically added if 'batch' column present
```
**Internal design formula**: `~ batch + Treatment`
**Interpretation**: Treatment effect adjusted for batch differences

#### 3. Paired Samples
```toml
[PseudoBulkDEG.envs]
# Compare time points within same subjects
group_by = "Timepoint"
ident_1 = "Day0"
ident_2 = "Day7"
paired_by = "SubjectID"
```
**Internal design formula**: `~ SubjectID + Timepoint`
**Interpretation**: Timepoint effect adjusted for subject-specific baseline

#### 4. Interaction Design (Treatment × Cell Type)
```toml
[PseudoBulkDEG.envs]
# Test if treatment effect differs between cell types
group_by = "Treatment_CellType"  # Requires combined column
ident_1 = "Control_Tcell"
ident_2 = "Treatment_Tcell"
```
**Using mutaters to create interaction**:
```toml
[PseudoBulkDEG.envs]
mutaters = {
  Treatment_CellType = "paste(Treatment, CellType, sep = '_')"
}
group_by = "Treatment_CellType"
```

#### 5. Multi-Factor Design (Batch + Condition)
```toml
[PseudoBulkDEG.envs]
# Complex design with multiple covariates
# Requires metadata columns: Batch, Gender, Condition
group_by = "Condition"
ident_1 = "WildType"
ident_2 = "Mutant"
```
**Internal design**: `~ Batch + Gender + Condition`
**Interpretation**: Condition effect adjusted for batch and gender

### Contrast Specification

DESeq2 compares specific group combinations via `ident_1` and `ident_2`:

```toml
# Simple comparison
ident_1 = "Control"    # Reference level
ident_2 = "Treatment"  # Comparison level

# One-vs-many comparison
ident_1 = "Control"
ident_2 = ""  # Empty = compare against all other groups combined
```

## Configuration Examples

### Example 1: Minimal Configuration

**Scenario**: Simple treatment vs control with biological replicates

```toml
[PseudoBulkDEG]
cache = true

[PseudoBulkDEG.in]
srtobj = ["SeuratClustering"]

[PseudoBulkDEG.envs]
# Basic two-group comparison
group_by = "Treatment"
ident_1 = "Vehicle"
ident_2 = "Drug"
```

### Example 2: Disease vs Healthy with Batch Correction

**Scenario**: Compare disease samples to healthy controls from multiple batches

```toml
[PseudoBulkDEG]
cache = true

[PseudoBulkDEG.in]
srtobj = ["SeuratClustering"]

[PseudoBulkDEG.envs]
# Ensure metadata has "Batch" column
group_by = "Diagnosis"
ident_1 = "Healthy"
ident_2 = "Disease"

# Batch correction (if Batch column exists)
# No explicit config needed - DESeq2 automatically includes batch if column present

# Use DESeq2 (default) for robust analysis
tool = "DESeq2"

# More stringent significance threshold
sigmarkers = "p_val_adj < 0.01 & abs(log2FC) > 1"
```

### Example 3: Per Cell Type Analysis

**Scenario**: Find DEGs separately for each major cell type

```toml
[PseudoBulkDEG]
cache = true

[PseudoBulkDEG.in]
srtobj = ["SeuratClustering"]

[PseudoBulkDEG.envs]
# Create one DEG case per cell type
each = "CellType"

# Define comparison for each case
group_by = "Condition"
ident_1 = "Control"
ident_2 = "Disease"

# Tool configuration
tool = "DESeq2"
sigmarkers = "p_val_adj < 0.05"

# Separate enrichment per cell type
enrich_style = "clusterProfiler"
dbs = ["KEGG_2021_Human", "MSigDB_Hallmark_2020"]
```

### Example 4: Time Course with Paired Samples

**Scenario**: Same subjects measured at multiple time points

```toml
[PseudoBulkDEG]
cache = true

[PseudoBulkDEG.in]
srtobj = ["SeuratClustering"]

[PseudoBulkDEG.envs]
# Paired design accounts for subject-specific effects
group_by = "Timepoint"
ident_1 = "Baseline"
ident_2 = "PostTreatment"
paired_by = "SubjectID"

# More sensitive threshold for time course
sigmarkers = "p_val_adj < 0.1"

# Add time-course specific enrichment
dbs = ["MSigDB_Hallmark_2020", "Reactome_2024_Human"]
```

### Example 5: Multiple Cases with Custom Grouping

**Scenario**: Compare multiple disease subtypes to healthy controls

```toml
[PseudoBulkDEG]
cache = true

[PseudoBulkDEG.in]
srtobj = ["SeuratClustering"]

[PseudoBulkDEG.envs]
# Define multiple comparison cases

[PseudoBulkDEG.envs.cases."Disease vs Healthy"]
group_by = "Diagnosis"
ident_1 = "Healthy"
ident_2 = "Disease"

[PseudoBulkDEG.envs.cases."Subtype A vs Healthy"]
group_by = "Diagnosis"
ident_1 = "Healthy"
ident_2 = "SubtypeA"

[PseudoBulkDEG.envs.cases."Subtype B vs Healthy"]
group_by = "Diagnosis"
ident_1 = "Healthy"
ident_2 = "SubtypeB"

[PseudoBulkDEG.envs.cases."Subtype A vs B"]
group_by = "Diagnosis"
ident_1 = "SubtypeA"
ident_2 = "SubtypeB"

# Each case can override defaults
[PseudoBulkDEG.envs.cases."Subtype A vs Healthy"]
sigmarkers = "p_val_adj < 0.01"  # More stringent for subtype A

[PseudoBulkDEG.envs.cases."Subtype B vs Healthy"]
sigmarkers = "p_val_adj < 0.05"  # Standard threshold for subtype B
```

## Common Patterns

### Pattern 1: Disease vs Healthy with Age Adjustment

```toml
[PseudoBulkDEG.envs]
# Metadata columns needed: Diagnosis, Age
mutaters = {
  AgeGroup = "ifelse(Age > 65, 'Elderly', 'Adult')"
}
group_by = "Diagnosis"
ident_1 = "Healthy"
ident_2 = "Disease"
# DESeq2 automatically includes AgeGroup as covariate if column exists
```

### Pattern 2: Time Series Analysis

```toml
[PseudoBulkDEG.envs]
# Compare consecutive time points
[PseudoBulkDEG.envs.cases."Day0 vs Day3"]
group_by = "Timepoint"
ident_1 = "Day0"
ident_2 = "Day3"

[PseudoBulkDEG.envs.cases."Day3 vs Day7"]
group_by = "Timepoint"
ident_1 = "Day3"
ident_2 = "Day7"

[PseudoBulkDEG.envs.cases."Day0 vs Day7"]
group_by = "Timepoint"
ident_1 = "Day0"
ident_2 = "Day7"
```

### Pattern 3: Multi-Factor Design (Genotype × Treatment)

```toml
[PseudoBulkDEG.envs]
# Create combined groups for interaction analysis
mutaters = {
  Combined = "paste(Genotype, Treatment, sep = '_')"
}

[PseudoBulkDEG.envs.cases."WT_Vehicle vs WT_Drug"]
group_by = "Combined"
ident_1 = "WT_Vehicle"
ident_2 = "WT_Drug"

[PseudoBulkDEG.envs.cases."KO_Vehicle vs KO_Drug"]
group_by = "Combined"
ident_1 = "KO_Vehicle"
ident_2 = "KO_Drug"

# Interaction: Treatment effect different between WT and KO?
[PseudoBulkDEG.envs.cases."WT_Drug vs KO_Drug"]
group_by = "Combined"
ident_1 = "WT_Drug"
ident_2 = "KO_Drug"
```

### Pattern 4: Subset to Specific Cell Types

```toml
[PseudoBulkDEG.envs]
# Only analyze T cells and B cells
subset = "CellType %in% c('T_cell', 'B_cell')"

# Create per-cell-type DEG
each = "CellType"

group_by = "Condition"
ident_1 = "Control"
ident_2 = "Disease"
```

## Plotting Configuration

### Marker Plots (Volcano, Dot, Heatmap)

```toml
[PseudoBulkDEG.envs.marker_plots."Volcano Plot"]
plot_type = "volcano"

[PseudoBulkDEG.envs.marker_plots."Dot Plot of Top Genes"]
plot_type = "dot"
genes = 20  # Show top 20 genes

[PseudoBulkDEG.envs.marker_plots."Heatmap of Top Markers"]
plot_type = "heatmap"
order_by = "desc(abs(log2FC))"
devpars = {width = 800, height = 1000}

[PseudoBulkDEG.envs.marker_plots."Volcano with Percent Difference"]
plot_type = "volcano_pct"
```

### Enrichment Plots (Bar, Dot, Network, Word Cloud)

```toml
[PseudoBulkDEG.envs.enrich_plots."Bar Plot"]
plot_type = "bar"
ncol = 1
top_term = 10

[PseudoBulkDEG.envs.enrich_plots."Dot Plot"]
plot_type = "dot"
top_term = 15

[PseudoBulkDEG.envs.enrich_plots."Network"]
plot_type = "network"
top_term = 20

[PseudoBulkDEG.envs.enrich_plots."Word Cloud"]
plot_type = "wordcloud"

[PseudoBulkDEG.envs.enrich_plots."Enrichmap"]
plot_type = "enrichmap"
```

### Overlap Analysis (Venn/UpSet Plots)

```toml
# Only works when ident_1 is not specified (multiple comparisons)
[PseudoBulkDEG.envs.overlaps."Overlapping DEGs"]
plot_type = "venn"
sigmarkers = "p_val_adj < 0.01"

[PseudoBulkDEG.envs.overlaps."UpSet of DEGs"]
plot_type = "upset"
sigmarkers = "p_val_adj < 0.01 & abs(log2FC) > 1"
```

## Dependencies

### Upstream Processes
- **Required**: `CombinedInput` (requires `SeuratClustering` or similar)
- **SeuratClustering**: Provides clustered Seurat object with metadata

### Downstream Uses
- **Pathway analysis**: Results feed into ScFGSEA (additional enrichment)
- **Visualization**: Volcano plots, heatmaps, enrichment plots
- **Publication**: Tables of significant genes, pathways

## Validation Rules

### Design Formula Validation
- **Replicates required**: Minimum 2-3 biological replicates per condition
- **Degrees of freedom**: Must have more samples than coefficients in model
- **Factor levels**: Cannot have single-factor level for all samples

### Metadata Requirements
- **`group_by` column**: Must exist in Seurat metadata
- **`ident_1`/`ident_2` values**: Must be levels in `group_by` column
- **`aggregate_by` column**: Must uniquely identify samples
- **`paired_by` column**: If specified, each subject must have measurements for all conditions

### Sample Size Guidelines
- **Simple comparison**: ≥ 3 replicates per condition (minimum)
- **Batch correction**: ≥ 3 replicates per batch per condition
- **Paired design**: ≥ 5 subject pairs recommended
- **Multi-factor**: Increase replicates to maintain power

## Troubleshooting

### Issue: "Coefficients equal to number of samples"
**Cause**: Model matrix has same number of coefficients as samples
**Solution**: Add more samples or simplify design formula
```toml
# Too complex for sample size
# Fix: Remove unnecessary covariates
```

### Issue: No significant markers found
**Cause**: Low effect size, high variance, or insufficient replicates
**Solutions**:
```toml
# Relax thresholds for discovery
sigmarkers = "p_val_adj < 0.1"  # Less stringent

# Check log2FC filter
sigmarkers = "p_val_adj < 0.05 & abs(log2FC) > 0.5"  # Lower fold-change threshold

# Use edgeR (more sensitive for small sample sizes)
tool = "edgeR"
```

### Issue: Batch effects not corrected
**Cause**: Batch column not in metadata or improperly named
**Solution**: Ensure `Batch` column exists in Seurat metadata
```toml
# Verify batch column exists in metadata
# Check with: colnames(seurat_obj@meta.data)
```

### Issue: Paired design not working
**Cause**: Subjects don't have all time points or unbalanced design
**Solution**: Ensure each subject has data for all conditions
```toml
# Verify paired structure
# Each SubjectID should have entries for all Timepoint values
```

### Issue: Interaction effects not interpretable
**Cause**: Missing main effects or wrong formula syntax
**Solution**: Use full factorial syntax or create combined groups
```toml
# Wrong: group_by = "Treatment" with cell type interaction
# Right: Create combined column
mutaters = {
  Combined = "paste(Treatment, CellType, sep = '_')"
}
group_by = "Combined"
```

## Best Practices

### 1. Always Check Metadata
Before running PseudoBulkDEG, verify metadata columns:
```r
# In R before running immunopipe
colnames(seurat_obj@meta.data)
table(seurat_obj$Condition)  # Check group sizes
table(seurat_obj$Batch)       # Check batch distribution
```

### 2. Start Simple
Begin with simple comparison, then add complexity:
```toml
# Step 1: Simple comparison
[PseudoBulkDEG.envs]
group_by = "Condition"
ident_1 = "Control"
ident_2 = "Treatment"

# Step 2: Add batch if needed
# Ensure Batch column exists in metadata

# Step 3: Add interactions via combined groups
mutaters = {Combined = "paste(Var1, Var2, sep = '_')"}
```

### 3. Use Appropriate Thresholds
Choose thresholds based on biological question:
- **Stringent**: `p_val_adj < 0.01 & abs(log2FC) > 1` (high-confidence genes)
- **Standard**: `p_val_adj < 0.05 & abs(log2FC) > 0.5` (balanced)
- **Exploratory**: `p_val_adj < 0.1` (sensitive, more false positives)

### 4. Validate Results
Check DEG results for sanity:
```toml
# Look at top genes
[PseudoBulkDEG.envs.marker_plots."Top 20 Genes"]
plot_type = "dot"
genes = 20

# Check enrichment quality
[PseudoBulkDEG.envs.enrich_plots."Pathway Bar"]
plot_type = "bar"
top_term = 15
```

### 5. Cache Strategy
Use caching for efficient iteration:
```toml
[PseudoBulkDEG]
cache = true  # Cache pseudo-bulk aggregation

[PseudoBulkDEG.envs]
cache = "/tmp"  # Cache intermediate DESeq2 results
```

## External References

### DESeq2 Documentation
- **Official vignette**: https://bioconductor.org/packages/release/bioc/html/DESeq2.html
- **Design formulas**: https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html#design-formulas
- **Contrasts**: https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html#results

### edgeR Documentation
- **User guide**: https://bioconductor.org/packages/release/bioc/html/edgeR.html
- **GLM framework**: https://bioconductor.org/packages/release/bioc/vignettes/edgeR/inst/doc/edgeRUsersGuide.pdf

### Enrichment Databases
- **MSigDB**: https://www.gsea-msigdb.org/gsea/msigdb/
- **KEGG**: https://www.genome.jp/kegg/
- **Reactome**: https://reactome.org/

### Plotthis/scplotter Documentation
- **FeatureStatPlot**: https://pwwang.github.io/scplotter/reference/FeatureStatPlot.html
- **EnrichmentPlot**: https://pwwang.github.io/scplotter/reference/EnrichmentPlot.html
- **VolcanoPlot**: https://pwwang.github.io/plotthis/reference/VolcanoPlot.html

## Quick Reference: Tool Comparison

| Feature | DESeq2 | edgeR |
|---------|--------|-------|
| **Default tool** | ✅ | ❌ |
| **Statistical model** | Negative binomial GLM | Negative binomial GLM |
| **Shrinkage estimators** | apeglm, ashr, lfcShrink | cpm, aveLogCPM |
| **Recommended for** | Publication-quality, robust results | Small sample sizes, exploratory |
| **Batch correction** | Built-in via design formula | Built-in via design formula |
| **Paired designs** | Supported | Supported |
| **Computation speed** | Moderate | Fast |
| **Output columns** | `baseMean`, `log2FC`, `lfcSE`, `stat`, `p_val`, `p_val_adj` | `logCPM`, `log2FC`, `LR`, `p_val`, `p_val_adj` |

## Workflow Integration

### Typical Pipeline Position
```
SampleInfo → SeuratPreparing → SeuratClustering → PseudoBulkDEG → [Visualization/Downstream]
```

### Input Requirements
- Seurat object with:
  - Count data (`"counts"` layer)
  - Metadata columns for grouping (`group_by`, `aggregate_by`)
  - Clustering results (optional, for subset analysis)

### Output Structure
```
outdir/
├── pseudo_bulk_counts/       # Aggregated counts per sample
├── deseq2_results/           # DESeq2/edgeR results
│   ├── case1/
│   │   ├── markers.tsv        # Full DEG table
│   │   ├── significant.tsv   # Filtered by sigmarkers
│   │   ├── volcano/          # Volcano plots
│   │   ├── marker_plots/      # Gene expression plots
│   │   └── enrichment/        # Pathway enrichment results
│   └── case2/
└── overlaps/                  # Overlap analysis (if applicable)
```

---

**Documentation**: `/docs/processes/PseudoBulkDEG.md`  
**Biopipen Reference**: [biopipen.ns.scrna.PseudoBulkDEG](https://pwwang.github.io/biopipen/api/biopipen.ns.scrna/#biopipen.ns.scrna.PseudoBulkDEG)
