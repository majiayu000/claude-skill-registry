---
name: cellcellcommunication
description: Infer ligand-receptor interactions and cell-cell communication networks from single-cell RNA-seq data using the LIANA+ framework. Identifies potential signaling events between cell types based on gene expression patterns and curated ligand-receptor interaction databases.
---

# CellCellCommunication Process Configuration

## Purpose
Infer ligand-receptor interactions and cell-cell communication networks from single-cell RNA-seq data using the LIANA+ framework. Identifies potential signaling events between cell types based on gene expression patterns and curated ligand-receptor interaction databases.

## When to Use
- To identify ligand-receptor interactions between cell types
- For systematic analysis of cell-cell communication networks
- To understand cell crosstalk and signaling pathways
- To compare communication patterns across biological conditions
- To identify key signaling mediators in tissue microenvironments

## Configuration Structure

### Process Enablement
```toml
[CellCellCommunication]
cache = true
```

### Input Specification
```toml
[CellCellCommunication.in]
sobjfile = ["path/to/seurat_object.rds"]  # Seurat (.rds, .h5seurat) or AnnData (.h5ad)
```

### Environment Variables
```toml
[CellCellCommunication.envs]
# Method selection
method = "cellchat"  # Default inference method

# Cell type grouping
groupby = "ident"  # Column name for cell type labels (default: Seurat ident)

# Species selection
species = "human"  # "human" or "mouse"

# Filtering parameters
expr_prop = 0.1  # Minimum expression proportion (0.0-1.0)
min_cells = 5     # Minimum cells per cell type

# Statistical parameters
n_perms = 1000  # Permutations for permutation testing
seed = 1337      # Random seed for reproducibility

# Computational resources
ncores = 1  # Number of parallel cores

# Advanced options
subset = ""      # Expression to subset cells (e.g., "adata.obs.group == 'control'")
split_by = ""    # Column to run analysis separately and combine
assay = "RNA"   # Assay to use for Seurat objects
```

## Available Inference Methods

LIANA+ provides multiple methods for cell-cell communication inference:

| Method | Description | Magnitude Score | Specificity Score |
|--------|-------------|-----------------|-------------------|
| `CellChat` | Mass-action-based communication probability | lr_means | cellchat_pvals |
| `CellPhoneDB` | Permutation-based significance | lr_means | cellphone_pvals |
| `Connectome` | Interaction-specific scoring | - | - |
| `log2FC` | Log-fold change based | - | - |
| `NATMI` | Network analysis | - | - |
| `SingleCellSignalR` | Database-driven scoring | - | - |
| `Rank_Aggregate` | Aggregates multiple methods | - | - |
| `Geometric_Mean` | Geometric mean scoring | - | - |

**Default method**: `cellchat` (recommended for most analyses)

## LIANA+ Resources

### Species-Specific Resources
```toml
# Human (default)
species = "human"  # Uses 'consensus' resource (CellPhoneDB, CellChat, ICELLNET, etc.)

# Mouse
species = "mouse"  # Uses 'mouseconsensus' resource
```

### Available Resources (override with `resource_name`)
- `consensus` (human default): Combines multiple curated resources
- `cellchatdb`: CellChat database interactions
- `cellphonedb`: CellPhoneDB interactions
- `mouseconsensus` (mouse default): Mouse-specific consensus
- `icellnet`, `connectomedb2020`, `ramilowski2015`, `lrdb`, and more

## Configuration Examples

### Minimal Configuration
```toml
[CellCellCommunication]
[CellCellCommunication.in]
sobjfile = ["path/to/seurat_object.rds"]

[CellCellCommunication.envs]
# Use defaults: method=cellchat, species=human, groupby=ident
```

### Human PBMC Analysis
```toml
[CellCellCommunication]
[CellCellCommunication.in]
sobjfile = ["path/to/pbmc_seurat.rds"]

[CellCellCommunication.envs]
method = "cellchat"
species = "human"
groupby = "cell_type"  # Use annotated cell types
expr_prop = 0.1
min_cells = 10
```

### Mouse Tissue Analysis
```toml
[CellCellCommunication]
[CellCellCommunication.in]
sobjfile = ["path/to/mouse_seurat.rds"]

[CellCellCommunication.envs]
species = "mouse"
method = "cellchat"
groupby = "seurat_clusters"
expr_prop = 0.15
min_cells = 8
```

### Multi-Condition Comparison
```toml
[CellCellCommunication]
[CellCellCommunication.in]
sobjfile = ["path/to/combined_seurat.rds"]

[CellCellCommunication.envs]
split_by = "condition"  # Run separately per condition, then combine
method = "cellchat"
groupby = "cell_type"
```

### Custom Cell Subset
```toml
[CellCellCommunication]
[CellCellCommunication.in]
sobjfile = ["path/to/seurat_object.rds"]

[CellCellCommunication.envs]
subset = "adata.obs.tissue == 'tumor'"
subset_using = "python"
method = "cellchat"
```

## Common Patterns

### Pattern 1: Full Interaction Network (CellChat)
```toml
[CellCellCommunication]
[CellCellCommunication.in]
sobjfile = ["intermediate/seuratclustering/SeuratClustering/sample.seurat.qs"]

[CellCellCommunication.envs]
method = "cellchat"
groupby = "ident"
expr_prop = 0.1
ncores = 4
```

### Pattern 2: Disease vs Healthy Comparison
```toml
[CellCellCommunication]
[CellCellCommunication.in]
sobjfile = ["path/to/disease_vs_healthy.rds"]

[CellCellCommunication.envs]
split_by = "disease_status"
method = "cellchat"
groupby = "cell_type"
expr_prop = 0.1
min_cells = 10
```

### Pattern 3: High-Stringency Analysis
```toml
[CellCellCommunication]
[CellCellCommunication.in]
sobjfile = ["path/to/seurat_object.rds"]

[CellCellCommunication.envs]
method = "cellchat"
expr_prop = 0.2  # Higher expression threshold
min_cells = 20    # More cells required
```

## Dependencies
- **Upstream**: SeuratClustering (required), CellTypeAnnotation (recommended for meaningful labels)
- **Downstream**: CellCellCommunicationPlots (visualization: network, circos, heatmap, box plots)

## Validation Rules
- **Species matching**: Set `species = "human"` or `species = "mouse"` to match your organism
- **Cell type grouping**: `groupby` column must exist in metadata; use CellTypeAnnotation or SeuratClustering results
- **Expression thresholds**: `expr_prop` between 0.0-1.0; recommended 0.1 for human, 0.15 for mouse
- **Cell type resolution**: `min_cells` minimum cells per type; recommended 5-10 cells per type

## Troubleshooting

### No Interactions Found
**Solutions**: Lower `expr_prop` (e.g., 0.1→0.05), reduce `min_cells`, check `groupby` column, verify `species` parameter

### Species Mismatch Error
**Solutions**: Verify `species` matches organism, ensure gene symbols in correct format (human: uppercase, mouse: title case)

### Slow Execution
**Solutions**: Increase `ncores`, reduce `n_perms` for permutation methods, use faster `cellchat` method

### Memory Issues
**Solutions**: Reduce `ncores`, use `subset` to analyze specific cell types, merge rare cell types

### Unexpected Cell Type Pairings
**Solutions**: Increase `expr_prop`, check cell type annotations, consider spatial context of data

## Best Practices
1. Run with CellChat first (default method provides good balance)
2. Annotate cell types first using CellTypeAnnotation
3. Validate expression thresholds based on data sparsity
4. Compare multiple methods (cellchat, cellphonedb) when possible
5. Interpret results in biological context (tissue structure, cell location)
6. Always visualize with CellCellCommunicationPlots
7. Document parameters for reproducibility

## References
- **LIANA+ Framework**: https://liana-py.readthedocs.io/
- **CellChat Method**: https://www.cellchat.org/
- **LIANA+ Paper**: Dimitrov et al., Nat Cell Biol (2024)
