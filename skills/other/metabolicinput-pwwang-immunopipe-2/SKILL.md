---
name: metabolicinput
description: Pass-through process that prepares Seurat object for metabolic landscape analysis. Routes the processed Seurat object to downstream metabolic analysis processes (MetabolicExprImputation, MetabolicPathwayActivity, MetabolicFeatures, MetabolicPathwayHeterogeneity). **Note**: This process requires no direct configuration.
---

# MetabolicInput Process Configuration

## Purpose
Pass-through process that prepares Seurat object for metabolic landscape analysis. Routes the processed Seurat object to downstream metabolic analysis processes (MetabolicExprImputation, MetabolicPathwayActivity, MetabolicFeatures, MetabolicPathwayHeterogeneity).

**Note**: This process requires no direct configuration. All metabolic analysis parameters are configured at the ScrnaMetabolicLandscape group level.

## When to Use
- First step in modular metabolic analysis workflow
- When you want to perform metabolic pathway analysis on single-cell RNA-seq data
- Alternative to ScrnaMetabolicLandscape (same group, modular approach)
- After clustering is complete (SeuratClustering or related processes)
- When investigating metabolic heterogeneity across cell types or conditions

## Configuration Structure

### Process Enablement
```toml
[ScrnaMetabolicLandscape]
# This enables the entire metabolic analysis group
# MetabolicInput is automatically included as part of this group

[ScrnaMetabolicLandscape.envs]
# Configure metabolic analysis parameters here
```

### Input Specification
MetabolicInput automatically receives input from upstream processes:
- Requires: Seurat object from CombinedInput (includes RNA + optional VDJ data)
- Typically follows: `SeuratClustering`, `TESSA`, or other clustering/annotation processes

### Environment Variables (Group Level)
All metabolic analysis configuration is done at the ScrnaMetabolicLandscape group level:

```toml
[ScrnaMetabolicLandscape.envs]
# Metabolic pathway database file
gmtfile = "KEGG_2021_Human"

# Skip imputation (if data already complete)
noimpute = false

# Number of cores for parallelization
ncores = 4

# Optional: Subset data by metadata column
# subset_by = "Response"  # Remove NA values in this column

# Optional: Group data by metadata column
# group_by = "cluster"

# Optional: Add metadata columns for grouping/subsetting
# mutaters = {timepoint = "if_else(treatment == 'control', 'pre', 'post')"}
```

## Metabolic Pathway Databases

### Available Databases (via enrichit)

The `gmtfile` parameter accepts either:

1. **Built-in database names** (auto-downloaded):
   - `"KEGG_2021_Human"` - KEGG pathways (human, default)
   - `"KEGG"` - KEGG pathways (latest)
   - `"Reactome_Pathways_2024"` - Reactome pathways
   - `"Reactome"` - Reactome pathways (latest)
   - `"BioCarta_2016"` - BioCarta pathways
   - `"MSigDB_Hallmark_2020"` - MSigDB Hallmark gene sets
   - See full list: https://pwwang.github.io/enrichit/reference/FetchGMT.html

2. **Custom GMT files** (local paths or URLs):
   - Local file: `/path/to/custom.gmt`
   - URL: `https://example.com/pathways.gmt`

### Database Descriptions

- **KEGG**: Kyoto Encyclopedia of Genes and Genomes - manually curated metabolic pathways. Comprehensive coverage of metabolism, including carbohydrate, energy, lipid, nucleotide, amino acid, xenobiotics, and other pathways. Species-specific versions available.

- **Reactome**: Curated pathway database covering cellular processes, signal transduction, metabolic pathways, and more. More comprehensive than KEGG for signaling and regulatory pathways. Good for human/mouse.

- **BioCarta**: Curated pathways focusing on cell signaling, metabolic, and disease pathways. Older database but still useful for classic pathways.

- **Custom GMT**: Your own gene sets in GMT format (Gene Set Enrichment Format). Format: `name\tdescription\tgene1,gene2,gene3` (tab-separated).

### Species-Specific Considerations

- **Human data**: Use `"KEGG_2021_Human"`, `"Reactome_Pathways_2024"`, or species-specific GMT files
- **Mouse data**: Use KEGG with mouse gene IDs or download mouse-specific GMT from MSigDB
- **Other species**: Provide custom GMT file with appropriate gene identifiers matching your Seurat object
- **Gene name matching**: Ensure gene names in Seurat object match GMT file (case-sensitive, human: UPPERCASE, mouse: TitleCase)

## Configuration Examples

### Minimal Configuration (Default KEGG)
```toml
[ScrnaMetabolicLandscape]
```

### KEGG Human Pathways (Explicit)
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
ncores = 4
noimpute = false
```

### Reactome Pathways
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "Reactome_Pathways_2024"
ncores = 8
```

### Custom Metabolic Pathway GMT File
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "/data/pathways/custom_metabolism.gmt"
ncores = 4
```

### Subset Analysis by Response Group
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
subset_by = "Response"  # Analyze responders vs non-responders
group_by = "cluster"
ncores = 4
```

### Multiple Pathway Databases (Via Cases)
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
ncores = 4

# Analyze with KEGG
[ScrnaMetabolicLandscape.envs.cases.KEGG]
gmtfile = "KEGG_2021_Human"
group_by = "cluster"

# Analyze with Reactome
[ScrnaMetabolicLandscape.envs.cases.Reactome]
gmtfile = "Reactome_Pathways_2024"
group_by = "cluster"
```

### Adding Custom Metadata for Grouping
```toml
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
ncores = 4
# Create timepoint column based on treatment
mutaters = {timepoint = "if_else(treatment == 'control', 'pre', 'post')"}
subset_by = "timepoint"
group_by = "cluster"
```

## Common Patterns

### Pattern 1: Standard Metabolic Analysis
```toml
# Basic setup with KEGG pathways
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
ncores = 4
```

### Pattern 2: Skip Imputation (Clean Data)
```toml
# If data is already complete, skip imputation step
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
noimpute = true
ncores = 4
```

### Pattern 3: Disease vs Control Comparison
```toml
# Compare metabolic pathways between conditions
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "KEGG_2021_Human"
subset_by = "diagnosis"  # e.g., "disease", "control"
group_by = "cluster"
ncores = 4
```

### Pattern 4: Time Series Analysis
```toml
# Analyze metabolic changes across timepoints
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "Reactome_Pathways_2024"
subset_by = "timepoint"  # e.g., "day0", "day7", "day14"
group_by = "cluster"
ncores = 8
```

### Pattern 5: Species-Specific Analysis
```toml
# Non-human data with custom pathways
[ScrnaMetabolicLandscape]
[ScrnaMetabolicLandscape.envs]
gmtfile = "/data/pathways/mouse_metabolism.gmt"
ncores = 4
```

## Dependencies

### Upstream Processes
- **Required**: Seurat object from `CombinedInput`
  - CombinedInput can be: `ScRepCombiningExpression` (RNA + VDJ) or `RNAInput` (RNA only)
  - RNAInput typically: `SeuratClustering`, `SeuratMap2Ref`, `CellTypeAnnotation`, or `TESSA`
- **Preceding**: Clustering must be complete before metabolic analysis

### Downstream Processes (In ScrnaMetabolicLandscape Group)
- **MetabolicExprImputation** (optional): Impute missing expression values (ALRA, scImpute, or MAGIC)
- **MetabolicPathwayActivity**: Calculate pathway activity scores per group
- **MetabolicFeatures**: Enrichment analysis of metabolic pathways per group
- **MetabolicPathwayHeterogeneity**: Calculate metabolic heterogeneity across groups

## Validation Rules

### Database Validation
- `gmtfile` must be a valid enrichit database name OR accessible GMT file path/URL
- For custom GMT files:
  - File must exist (absolute path or relative to config file)
  - Format must be GMT: `name\tdescription\tgene1,gene2,gene3`
  - Gene identifiers must match Seurat object (case-sensitive)

### Species Validation
- Gene names in Seurat object must match GMT file:
  - Human: UPPERCASE (e.g., `CD3D`, `IFNG`)
  - Mouse: TitleCase (e.g., `Cd3d`, `Ifng`)
  - Verify with: `sobj@assays$RNA@features` (Seurat R command)

### Metadata Validation
- If `subset_by` specified: column must exist in Seurat object metadata
- If `group_by` specified: column must exist in Seurat object metadata
- NA values in `subset_by` column are automatically removed

## Troubleshooting

### Common Pathway Loading Issues

#### Issue: "GMT file not found"
**Cause**: Invalid path to custom GMT file
**Solution**:
```toml
# Use absolute path
gmtfile = "/full/path/to/pathways.gmt"

# Or path relative to config file location
gmtfile = "./data/pathways.gmt"
```

#### Issue: "Gene names not found in Seurat object"
**Cause**: Gene identifier mismatch between GMT and Seurat object
**Solution**:
- Check gene format in Seurat: `sobj@assays$RNA@features[1:10,]`
- Ensure case matches: Human (UPPERCASE) vs Mouse (TitleCase)
- Consider using gene symbol conversion tools if needed

#### Issue: "Empty pathway results"
**Cause**: Too few genes matching between pathways and data
**Solution**:
- Verify species compatibility (human GMT with mouse data won't work)
- Try different database: Switch from KEGG to Reactome or vice versa
- Use custom GMT with species-specific pathways

#### Issue: "No enriched pathways found"
**Cause**: Statistical thresholds too strict or no biological differences
**Solution**:
- Relax p-value cutoff in downstream processes (e.g., `pathway_pval_cutoff`)
- Check grouping: Ensure groups have distinct biological differences
- Use more comprehensive database (Reactome often has more pathways than KEGG)

### Performance Issues

#### Issue: Metabolic analysis too slow
**Cause**: Insufficient cores for parallelization
**Solution**:
```toml
# Increase cores for metabolic analysis
[ScrnaMetabolicLandscape.envs]
ncores = 8  # Increase based on available CPU
```

#### Issue: Memory errors during imputation
**Cause**: Large dataset with imputation enabled
**Solution**:
```toml
# Skip imputation if data is complete
[ScrnaMetabolicLandscape.envs]
noimpute = true
```

### Integration Issues

#### Issue: Process not running
**Cause**: ScrnaMetabolicLandscape not enabled in config
**Solution**:
```toml
# Ensure the group is enabled
[ScrnaMetabolicLandscape]
```

#### Issue: Wrong input data
**Cause**: Clustering not complete or incorrect upstream process
**Solution**:
- Ensure `SeuratClustering` or similar process runs before metabolic analysis
- Check that Seurat object has cluster assignments: `sobj@meta.data$seurat_clusters`
- Verify no missing values in metadata columns used for grouping

## Reference

- **Original Paper**: Xiao, Z. et al. "Metabolic landscape of the tumor microenvironment at single cell resolution." Nature Communications 10, 1-12 (2019)
- **Pipeline**: https://github.com/LocasaleLab/Single-Cell-Metabolic-Landscape
- **KEGG**: https://www.genome.jp/kegg/pathway.html
- **Reactome**: https://reactome.org/
- **enrichit Databases**: https://pwwang.github.io/enrichit/reference/FetchGMT.html
- **GMT Format**: http://www.broadinstitute.org/gsea/msigdb/file_formats.jsp
