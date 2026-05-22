---
name: topexpressinggenes
description: Identifies and visualizes the top expressing genes per cluster in T/B cells, followed by pathway enrichment analysis. Provides quick cluster characterization by highlighting the most highly expressed genes and their biological functions.
---

# TopExpressingGenes Process Configuration

## Purpose
Identifies and visualizes the top expressing genes per cluster in T/B cells, followed by pathway enrichment analysis. Provides quick cluster characterization by highlighting the most highly expressed genes and their biological functions.

## When to Use
- **After**: `SeuratClustering` and `TOrBCellSelection` processes
- **Use cases**: Quick cluster characterization, identifying dominant gene programs, pathway enrichment
- **Optional process**: Enable only when cluster-level expression profiling is needed

## Configuration Structure

### Process Enablement
```toml
[TopExpressingGenes]
cache = true
```

### Input Specification
```toml
[TopExpressingGenes.in]
srtobj = ["SeuratClustering"]
```

**Note**: `srtobj` accepts the output from `SeuratClustering` or `SeuratSubClustering`.

## Environment Variables

### Core Parameters
```toml
[TopExpressingGenes.envs]
# Number of top expressing genes to identify per cluster
n = 250

# Enrichment style
enrich_style = "enrichr"  # Options: "enrichr", "clusterprofiler"

# Enrichment databases
dbs = ["KEGG_2021_Human", "MSigDB_Hallmark_2020"]
```

### Enrichment Plot Settings
```toml
[TopExpressingGenes.envs.enrich_plots_defaults]
# Plot type: "bar", "dot", "lollipop", "network", "enrichmap", "wordcloud"
plot_type = "bar"
devpars = {res = 100, width = 800, height = 600}
top_term = 10  # Top enriched pathways to show
ncol = 1
```

## Configuration Examples

### Minimal Configuration
```toml
[TopExpressingGenes]

[TopExpressingGenes.in]
srtobj = ["SeuratClustering"]
```

### Top 10 Genes with Custom Databases
```toml
[TopExpressingGenes]

[TopExpressingGenes.in]
srtobj = ["SeuratClustering"]

[TopExpressingGenes.envs]
n = 10
dbs = ["GO_Biological_Process_2025", "Reactome_Pathways_2024"]
```

### Network Visualization
```toml
[TopExpressingGenes.envs.enrich_plots."Network"]
plot_type = "network"
top_term = 15

[TopExpressingGenes.envs.enrich_plots."Enrichmap"]
plot_type = "enrichmap"
```

## Common Patterns

### Pattern 1: Quick Cluster Overview
```toml
[TopExpressingGenes]

[TopExpressingGenes.in]
srtobj = ["SeuratClustering"]

[TopExpressingGenes.envs]
n = 10
dbs = ["MSigDB_Hallmark_2020"]
```

### Pattern 2: Detailed Profile
```toml
[TopExpressingGenes.envs]
n = 250
enrich_style = "clusterprofiler"

[TopExpressingGenes.envs.enrich_plots]
"KEGG" = {plot_type = "bar", dbs = ["KEGG_2021_Human"]}
"Reactome" = {plot_type = "network"}
```

### Pattern 3: Multiple Visualizations
```toml
[TopExpressingGenes.envs]
n = 50

[TopExpressingGenes.envs.enrich_plots."Bar"]
plot_type = "bar"

[TopExpressingGenes.envs.enrich_plots."Word Cloud"]
plot_type = "wordcloud"
```

## Difference from ClusterMarkers

| Aspect | TopExpressingGenes | ClusterMarkers |
|--------|-------------------|----------------|
| **Finds** | Highest expressed genes within clusters | Genes differentially expressed between clusters |
| **Meaning** | Basal/dominant expression | Distinguishing markers |
| **Stat test** | None (average expression) | Statistical (Wilcoxon, MAST) |
| **Use case** | Cluster identity/function | Marker discovery |
| **Output** | Top N genes | DEGs with p-values/FC |

**Recommendation**: Use both processes:
1. `TopExpressingGenes`: Quick overview of dominant programs
2. `ClusterMarkers`: Rigorous marker identification

## Dependencies
- **Upstream**: `SeuratClustering`, `TOrBCellSelection` (for TCR route)
- **Downstream**: None (terminal analysis process)

## Validation Rules
- `n`: Positive integer (typically 10-500)
- `dbs`: Valid enrichit/Enrichr database names or local GMT paths
- `enrich_style`: "enrichr" or "clusterprofiler"
- `plot_type`: Valid scplotter plot type

## Troubleshooting

### Ribosomal/Mitochondrial Gene Dominance
**Issue**: Housekeeping genes (RPS, RPL, MT-) dominate

**Solutions**: Increase `n`, use `ClusterMarkers`, filter genes in `SeuratPreparing`

### Empty Enrichment Results
**Issue**: No pathways enriched

**Solutions**: Increase `n` to 100-500, verify species (UPPERCASE=human, TitleCase=mouse)

### Plot Rendering Errors
**Issue**: Plots fail to render

**Solutions**: Reduce `top_term` (5-15), use simpler plots (`bar`, `dot`)

### Performance Issues
**Issue**: Process too slow

**Solutions**: Reduce `n`, use fewer databases, disable enrichment: `dbs = []`

## External References

### Databases (enrichit)
- `KEGG_2021_Human` - KEGG pathways
- `MSigDB_Hallmark_2020` - Hallmark gene sets
- `GO_Biological_Process_2025` - GO Biological Process
- `Reactome_Pathways_2024` - Reactome pathways
- See: https://pwwang.github.io/enrichit/reference/FetchGMT.html

### Plot Types (scplotter)
- `bar` - Bar chart
- `dot` - Dot plot
- `lollipop` - Lollipop plot
- `network` - Network visualization
- `enrichmap` - Enrichment map
- `wordcloud` - Word cloud

### Enrichment Styles
- `enrichr` - Fisher's exact test
- `clusterprofiler` - Hypergeometric test

## See Also
- `TopExpressingGenesOfAllCells` - Top genes before T/B selection
- `ClusterMarkers` - Differential expression analysis
