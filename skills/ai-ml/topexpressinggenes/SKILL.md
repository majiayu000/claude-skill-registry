---
name: topexpressinggenesofallcells
description: Identifies and visualizes the top expressing genes per cluster across ALL cells (before T/B cell selection), followed by pathway enrichment analysis. Provides initial overview of all cell populations by highlighting the most highly expressed genes and their biological functions.
---

# TopExpressingGenesOfAllCells Process Configuration

## Purpose
Identifies and visualizes the top expressing genes per cluster across ALL cells (before T/B cell selection), followed by pathway enrichment analysis. Provides initial overview of all cell populations by highlighting the most highly expressed genes and their biological functions.

## When to Use
- **After**: `SeuratClusteringOfAllCells` process
- **Before**: `TOrBCellSelection` (this is a pre-selection analysis)
- **Use cases**:
  - Quick overview of ALL cell populations before separation
  - Initial assessment of broad cell type signatures
  - Understanding overall cell composition before T/B selection
  - Pathway enrichment on cell type markers before detailed analysis
  - Quality check for unexpected cell types
  - Complementary to `ClusterMarkersOfAllCells` for complete pre-selection profiling
- **Optional process**: Enable only when pre-selection analysis is needed

## Configuration Structure

### Process Enablement
```toml
[TopExpressingGenesOfAllCells]
cache = true
```

### Input Specification
```toml
[TopExpressingGenesOfAllCells.in]
srtobj = ["SeuratClusteringOfAllCells"]
```

**Note**: `srtobj` accepts the output from `SeuratClusteringOfAllCells`.

## Environment Variables

### Core Parameters
```toml
[TopExpressingGenesOfAllCells.envs]
# Number of top expressing genes to identify per cluster
n = 250

# Enrichment style
enrich_style = "enrichr"  # Options: "enrichr", "clusterprofiler"

# Enrichment databases
dbs = ["KEGG_2021_Human", "MSigDB_Hallmark_2020"]
```

### Enrichment Plot Settings
```toml
[TopExpressingGenesOfAllCells.envs.enrich_plots_defaults]
# Plot type for enrichment results
plot_type = "bar"  # Options: "bar", "dot", "lollipop", "network", "enrichmap", "wordcloud"

# Device parameters
devpars = {res = 100, width = 800, height = 600}

# Additional output formats
more_formats = []

# Save R code to reproduce plots
save_code = false

# Top terms to display
top_term = 10  # Number of top enriched pathways to show
ncol = 1  # Number of columns in multi-panel plots
```

### Cell Subsetting
```toml
[TopExpressingGenesOfAllCells.envs]
# Subset cells before analysis (optional)
subset = ""
```

### Cache Control
```toml
[TopExpressingGenesOfAllCells.envs]
# Cache intermediate results
cache = "/tmp"  # true, false, or directory path
```

## Configuration Examples

### Minimal Configuration
```toml
[TopExpressingGenesOfAllCells]

[TopExpressingGenesOfAllCells.in]
srtobj = ["SeuratClusteringOfAllCells"]
```

### Top 10 Genes for Broad Cell Type ID
```toml
[TopExpressingGenesOfAllCells]

[TopExpressingGenesOfAllCells.in]
srtobj = ["SeuratClusteringOfAllCells"]

[TopExpressingGenesOfAllCells.envs]
n = 10
dbs = ["MSigDB_Hallmark_2020"]
```

### Multiple Databases for Comprehensive Overview
```toml
[TopExpressingGenesOfAllCells]

[TopExpressingGenesOfAllCells.in]
srtobj = ["SeuratClusteringOfAllCells"]

[TopExpressingGenesOfAllCells.envs]
n = 100
dbs = [
  "KEGG_2021_Human",
  "MSigDB_Hallmark_2020",
  "GO_Biological_Process_2025"
]
```

## Common Patterns

### Pattern 1: Quick All-Cell Overview (Pre-Selection)
```toml
[TopExpressingGenesOfAllCells]

[TopExpressingGenesOfAllCells.in]
srtobj = ["SeuratClusteringOfAllCells"]

[TopExpressingGenesOfAllCells.envs]
n = 10
dbs = ["MSigDB_Hallmark_2020"]

[TopExpressingGenesOfAllCells.envs.enrich_plots_defaults]
plot_type = "bar"
top_term = 10
```

**What to expect**: Top 10 genes per cluster showing broad cell type markers (CD3 for T cells, CD19 for B cells, CD14 for monocytes, etc.)

### Pattern 2: Broad Cell Type Signature Identification
```toml
[TopExpressingGenesOfAllCells]

[TopExpressingGenesOfAllCells.in]
srtobj = ["SeuratClusteringOfAllCells"]

[TopExpressingGenesOfAllCells.envs]
n = 50

[TopExpressingGenesOfAllCells.envs.enrich_plots]
"T Cell Pathways" = {plot_type = "bar", dbs = ["KEGG_2021_Human"]}
"B Cell Pathways" = {plot_type = "bar", dbs = ["KEGG_2021_Human"]}
"Myeloid Pathways" = {plot_type = "bar", dbs = ["KEGG_2021_Human"]}
```

**What to expect**: Identification of T cell (CD3E, CD3D), B cell (CD19, MS4A1), and myeloid (CD14, LYZ) signatures across clusters

### Pattern 3: Quality Check for Unexpected Cell Types
```toml
[TopExpressingGenesOfAllCells]

[TopExpressingGenesOfAllCells.in]
srtobj = ["SeuratClusteringOfAllCells"]

[TopExpressingGenesOfAllCells.envs]
n = 20
dbs = [
  "GO_Biological_Process_2025",
  "GO_Cellular_Component_2025"
]

[TopExpressingGenesOfAllCells.envs.enrich_plots_defaults]
plot_type = "dot"
top_term = 15
```

**What to expect**: Detection of contamination (e.g., EPCAM for epithelial, COL1A1 for fibroblasts, RBC markers)

## Difference from TopExpressingGenes

**TopExpressingGenesOfAllCells** vs **TopExpressingGenes**:

| Aspect | TopExpressingGenesOfAllCells | TopExpressingGenes |
|--------|-----------------------------|-------------------|
| **When it runs** | BEFORE `TOrBCellSelection` | AFTER `TOrBCellSelection` |
| **Input data** | All cells (unfiltered) | Only selected T or B cells |
| **Upstream process** | `SeuratClusteringOfAllCells` | `SeuratClustering` + `TOrBCellSelection` |
| **Use case** | Initial assessment, quality check | Detailed T/B cell analysis |
| **Cell types** | ALL cell types present | Only T OR B cells |
| **Typical markers** | CD3, CD19, CD14, etc. | Specific T/B cell subtypes |
| **Position in workflow** | Pre-selection overview | Post-selection deep dive |

**Workflow context**:
```
RNA Input → SeuratPreparing → SeuratClusteringOfAllCells
                                              ↓
                                      TopExpressingGenesOfAllCells  ← Runs here
                                              ↓
                                      TOrBCellSelection (separates T/B)
                                              ↓
                                      SeuratClustering (on selected cells)
                                              ↓
                                      TopExpressingGenes  ← Runs here
```

**Recommendation**:
- Use `TopExpressingGenesOfAllCells` to assess overall data quality and cell type composition
- Use `TopExpressingGenes` for detailed analysis of T or B cell subtypes
- Enable both for comprehensive analysis: pre-selection overview + post-selection deep dive

## Dependencies
- **Upstream**: `SeuratClusteringOfAllCells`
- **Downstream**: `TOrBCellSelection` (optional - this process provides pre-selection context)
- **Data**: Seurat object with cluster assignments for ALL cells

## Validation Rules
- **`n` parameter**: Must be positive integer (typically 10-500)
- **`dbs`**: Must be valid enrichit/Enrichr database names or local GMT file paths
- **`enrich_style`**: Must be "enrichr" or "clusterprofiler"
- **`plot_type`**: Must be valid scplotter plot type
- **Workflow requirement**: Only runs when `SeuratClusteringOfAllCells` is enabled

## Troubleshooting

### Process Not Running
**Issue**: TopExpressingGenesOfAllCells not executed despite being in config

**Causes**:
- `SeuratClusteringOfAllCells` not enabled
- Missing dependency in workflow
- Process disabled via validation warning

**Solutions**:
1. Ensure `SeuratClusteringOfAllCells` is enabled in config
2. Check validation warnings: `python -m immunopipe.validate_config config.toml`
3. Verify both processes in config:
   ```toml
   [SeuratClusteringOfAllCells]
   [TopExpressingGenesOfAllCells]
   ```

### Mixed Cell Types in Results
**Issue**: Clusters show multiple cell type markers (CD3 + CD19)

**Causes**:
- Overlapping clusters (resolution too low)
- Doublets/multiplets not filtered
- Contamination in data

**Solutions**:
1. Adjust clustering resolution in `SeuratClusteringOfAllCells`
2. Filter doublets in `SeuratPreparing` step
3. Use `TOrBCellSelection` after assessment to clean data

### No Clear Cell Type Signatures
**Issue**: Top genes list lacks expected markers (CD3, CD19, CD14)

**Causes**:
- Data quality issues (low counts, high mitochondrial)
- Wrong organism (human vs mouse gene symbols)
- Incomplete clustering

**Solutions**:
1. Check QC metrics in `SeuratClusterStatsOfAllCells`
2. Verify organism (uppercase=human, titlecase=mouse)
3. Review clustering results from `SeuratClusteringOfAllCells`

### Ribosomal/Mitochondrial Gene Dominance
**Issue**: Top genes list dominated by housekeeping genes (RPS, RPL, MT-)

**Solutions**:
1. Increase `n` parameter to see beyond housekeeping genes
2. Filter out ribosomal/mitochondrial genes in `SeuratPreparing` step
3. Use `ClusterMarkersOfAllCells` for differential expression

### Empty Enrichment Results
**Issue**: No pathways enriched despite top genes identified

**Causes**:
- Gene identifiers don't match database
- `n` too small for meaningful enrichment
- Database not appropriate for cell type

**Solutions**:
1. Increase `n` to 100-500 genes
2. Verify species match (check gene symbols)
3. Try different databases (e.g., `GO_Biological_Process_2025`)

### Plot Rendering Errors
**Issue**: Enrichment plots fail to render

**Causes**:
- Network plots with too many terms
- Missing dependencies in R environment

**Solutions**:
1. Reduce `top_term` parameter
2. Use simpler plot types (`bar`, `dot`)
3. Verify R packages installed: `enrichit`, `scplotter`

## Output Structure
```
<srtobj_stem>.top_expressing_genes/
├── <cluster_name>/              # One subdirectory per cluster (ALL cells)
│   ├── top_genes.tsv            # Top N genes with expression metrics
│   └── enrich/                 # Enrichment results
│       ├── <db_name>/          # One subdirectory per database
│       │   ├── *.Bar-Plot.png  # Enrichment plots
│       │   ├── *.enrich.tsv    # Enrichment tables
│       │   └── ...
```

## External References

### Enrichment Databases (enrichit)
[Full reference](https://pwwang.github.io/enrichit/reference/FetchGMT.html)

**Built-in databases**:
- `KEGG_2021_Human` - KEGG pathways (human)
- `MSigDB_Hallmark_2020` - MSigDB Hallmark gene sets
- `GO_Biological_Process_2025` - GO Biological Process terms
- `GO_Cellular_Component_2025` - GO Cellular Component terms
- `GO_Molecular_Function_2025` - GO Molecular Function terms
- `Reactome_Pathways_2024` - Reactome pathways
- `WikiPathways_2024_Human` - WikiPathways (human)

**Enrichr libraries**: See https://maayanlab.cloud/Enrichr/#libraries

### Enrichment Plot Types (scplotter)
[Full reference](https://pwwang.github.io/scplotter/reference/EnrichmentPlot.html)

- `bar` - Bar chart of enriched terms
- `dot` - Dot plot (bubble chart)
- `lollipop` - Lollipop plot
- `network` - Network visualization of term relationships
- `enrichmap` - Enrichment map (similar to Cytoscape)
- `wordcloud` - Word cloud visualization

### Enrichment Styles
- `enrichr` - Fisher's exact test (Enrichr-style)
- `clusterprofiler` - Hypergeometric test (clusterProfiler-style)

## See Also
- `TopExpressingGenes` - Top genes for selected T/B cells after selection
- `ClusterMarkersOfAllCells` - Differential expression for all cells before selection
- `SeuratClusteringOfAllCells` - Clustering on all cells before T/B selection
- `TOrBCellSelection` - T/B cell separation process
