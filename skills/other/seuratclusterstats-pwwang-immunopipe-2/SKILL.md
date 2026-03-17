---
name: seuratclusterstats
description: Generates comprehensive cluster statistics and visualizations for Seurat objects, including dimension reduction plots, gene expression visualizations, cluster quality metrics, and clustree diagrams. This process is essential for exploring and validating clustering results.
---

# SeuratClusterStats Process Configuration

## Purpose
Generates comprehensive cluster statistics and visualizations for Seurat objects, including dimension reduction plots, gene expression visualizations, cluster quality metrics, and clustree diagrams. This process is essential for exploring and validating clustering results.

## When to Use
- **After**: `SeuratClustering` or `SeuratSubClustering` processes
- **Use cases**:
  - Cluster quality assessment and validation
  - Visualizing cluster characteristics across dimensions
  - Comparing marker gene expression between clusters
  - Assessing cluster stability via clustree plots
  - Exploring metadata relationships with clusters
- **Always enabled** in immunopipe TCR and non-TCR workflows (order = -1, runs early)

## Configuration Structure

### Process Enablement
```toml
[SeuratClusterStats]
cache = true
```

### Input Specification
```toml
[SeuratClusterStats.in]
srtobj = ["SeuratClustering"]
```

**Note**: `srtobj` accepts the output name from `SeuratClustering` or `SeuratSubClustering`.

## Environment Variables

### Global Settings
```toml
[SeuratClusterStats.envs]
# Mutate metadata before plotting
mutaters = {}

# Cache feature plots (time-consuming)
cache = "/tmp"
```

### Clustree Plots
Visualize clustering resolution relationships.

```toml
[SeuratClusterStats.envs.clustrees_defaults]
prefix = true  # Auto-detect clustering columns
devpars = {res = 100, width = 800, height = 500}
more_formats = []
save_code = false
```

**Clustree cases**:
```toml
[SeuratClusterStats.envs.clustrees."Custom Clustree"]
prefix = "seurat_clusters"
devpars = {height = 600}
```

### Cluster Statistics (stats)
Cell count and fraction plots across clusters.

```toml
[SeuratClusterStats.envs.stats_defaults]
subset = ""
devpars = {res = 100, height = 600, width = 800}
descr = ""
more_formats = []
save_code = false
save_data = false
```

**Plot types for stats** (via `scplotter::CellStatPlot`):
- `bar` - Bar chart
- `circos` - Circos plot (chord diagram)
- `pie` - Single pie chart
- `ring`/`donut` - Ring/donut chart
- `trend` - Trend plot
- `area` - Area plot
- `sankey`/`alluvial` - Sankey/alluvial diagram
- `heatmap` - Heatmap
- `radar` - Radar plot
- `spider` - Spider plot
- `violin` - Violin plot
- `box` - Box plot

**Default cases**:
```toml
[SeuratClusterStats.envs.stats]
"Number of cells in each cluster (Bar Chart)" = {plot_type = "bar", x_text_angle = 90}
"Number of cells in each cluster by Sample (Bar Chart)" = {plot_type = "bar", group_by = "Sample", x_text_angle = 90}
```

**Custom stat example**:
```toml
[SeuratClusterStats.envs.stats."Cells by Diagnosis"]
plot_type = "bar"
group_by = "Diagnosis"
frac = "group"  # Options: "none", "group", "ident", "cluster", "all"
x_text_angle = 90
swap = true
position = "stack"
```

### Gene Count Visualization (ngenes)
Number of genes detected per cell.

```toml
[SeuratClusterStats.envs.ngenes_defaults]
more_formats = []
subset = ""
devpars = {res = 100, height = 800, width = 1000}
```

**Default case**:
```toml
[SeuratClusterStats.envs.ngenes]
"Number of genes detected in each cluster" = {}
```

### Feature Visualization (features)
Gene expression and metadata column plots.

```toml
[SeuratClusterStats.envs.features_defaults]
# Feature specification (multiple formats)
features = ["CD3D", "CD4", "CD8A"]  # OR
# features = "file://path/to/genes.txt"  # OR
# features = 10  # Top N variant features

# Cluster ordering
order_by = "desc(mean(Expression, na.rm = TRUE))"  # OR
# order_by = ["c1", "c2", "c3"]  # Literal order

subset = ""
devpars = {res = 100}
descr = ""
more_formats = []
save_code = false
save_data = false
```

**Feature plot types** (via `scplotter::FeatureStatPlot`):
- `violin` - Violin plot
- `box` - Box plot
- `bar` - Bar plot
- `ridge` - Ridge plot
- `dim` - Dimension reduction plot
- `cor` - Correlation plot
- `heatmap` - Heatmap
- `dot` - Dot plot (heatmap shortcut)

**Common feature parameters**:
- `plot_type` - Type of visualization
- `ident` - Identity column (e.g., "seurat_clusters", "Diagnosis")
- `group_by` - Group cells by metadata column
- `split_by` - Split into multiple plots
- `facet_by` - Facet plots by metadata
- `add_box` - Add box plot overlay (violin/ridge)
- `add_point` - Add jittered points
- `add_bg` - Add background reference
- `stack` - Stack multiple features
- `flip` - Flip plot orientation
- `comparisons` - Add statistical comparisons

### Dimension Reduction Plots (dimplots)
UMAP/tSNE/PCA visualizations.

```toml
[SeuratClusterStats.envs.dimplots_defaults]
group_by = null
split_by = null
subset = ""
devpars = {res = 100}
reduction = "dim"  # Options: "dim", "auto", "umap", "tsne", "pca"
```

**Reduction options**:
- `dim` - Auto-detect: UMAP → tSNE → PCA (uses sub_umap for subclusters)
- `auto` - Same as `dim`
- `umap` - Force UMAP
- `tsne` - Force tSNE
- `pca` - Force PCA

**Common dimplot parameters**:
- `label` - Add cluster labels
- `label_size` - Label font size
- `label_repel` - Repel overlapping labels
- `add_mark` - Add cluster boundaries (options: hull, ellipse, rect, circle)
- `mark_alpha` - Mark transparency
- `mark_linetype` - Mark line type
- `hex` - Use hexagonal binning
- `hex_bins` - Number of hex bins
- `stat_by` - Add statistics by metadata
- `stat_plot_type` - pie, ring, bar, line
- `stat_plot_size` - Size of stat plot
- `facet_by` - Facet by metadata
- `highlight` - Highlight specific cells

**Default cases**:
```toml
[SeuratClusterStats.envs.dimplots]
"Dimensional reduction plot" = {label = true}
"VDJ Presence" = {group_by = "VDJ_Presence"}  # Only if TCR data present
```

## External References

### Plotthis Plot Types
[Full reference](https://pwwang.github.io/plotthis/reference/)

**Dimension Reduction**:
- `DimPlot`: UMAP/tSNE/PCA visualization
  - `dims` - Dimensions to plot (default: 1:2)
  - `pt_size` - Point size
  - `alpha` - Point transparency
  - `label` - Add cluster labels
  - `highlight` - Highlight cells
  - `add_density` - Add density layer
  - `hex` - Hexagonal binning

**Statistical Plots**:
- `ViolinPlot`: Distribution with density
  - `add_box` - Add box overlay
  - `add_point` - Add points
  - `add_trend` - Add trend line
  - `flip` - Horizontal orientation

- `BoxPlot`: Box and whisker plots
  - `add_jitter` - Add jittered points
  - `add_violin` - Add violin overlay

- `BarPlot`: Bar charts
  - `position` - "stack", "dodge", "fill"
  - `x_text_angle` - X-axis text rotation
  - `swap` - Swap x and fill aesthetics

- `RidgePlot`: Ridge (joy) plots
  - `flip` - Horizontal orientation

**Heatmaps**:
- `Heatmap`: Gene expression heatmaps
  - `cell_type` - "tile", "dot", "violin", "boxplot", "bar", "pie"
  - `cluster_rows` - Cluster rows
  - `cluster_columns` - Cluster columns
  - `rows_split_by` - Split rows by metadata
  - `columns_split_by` - Split columns by metadata
  - `flip` - Transpose heatmap
  - `palette` - Color palette (e.g., "viridis", "YlOrRd", "Spectral")
  - `column_annotation` - Add column annotations (list of column names)
  - `column_annotation_type` - Annotation types (simple, violin, pie, ring, bar)
  - `dot_size` - Function for dot size (e.g., function(x) sum(x > 0) / length(x))
  - `dot_size_name` - Legend name for dot size
  - `add_reticle` - Add grid lines
  - `add_bg` - Add background

**Advanced Visualizations**:
- `CircosPlot`: Chord/circos diagram
- `SankeyPlot`: Sankey/alluvial diagram
  - `links_alpha` - Link transparency
  - `group_by` - Node columns (list for multiple nodes)

### Device Parameters
Common to all plot types:
```toml
devpars = {
  res = 100,      # Resolution in DPI
  width = 800,     # Width in pixels
  height = 600     # Height in pixels
}
```

## Configuration Examples

### Minimal Configuration
```toml
[SeuratClusterStats]
cache = true

[SeuratClusterStats.in]
srtobj = ["SeuratClustering"]
```

### Standard QC Plots
```toml
[SeuratClusterStats.envs.stats."Number of cells per cluster"]
plot_type = "bar"
x_text_angle = 90

[SeuratClusterStats.envs.stats."Cells by Sample"]
plot_type = "bar"
group_by = "Sample"
x_text_angle = 90
```

### Gene Expression Visualization
```toml
[SeuratClusterStats.envs.features_defaults]
features = ["CD3D", "CD4", "CD8A", "MS4A1", "CD14", "LYZ", "FCGR3A", "NCAM1", "KLRD1"]

[SeuratClusterStats.envs.features."T cell markers (violin)"]
plot_type = "violin"
ident = "seurat_clusters"
add_box = true

[SeuratClusterStats.envs.features."T cell markers (ridge)"]
plot_type = "ridge"
ident = "seurat_clusters"
flip = true

[SeuratClusterStats.envs.features."Marker on UMAP"]
plot_type = "dim"
feature = "CD4"
highlight = "seurat_clusters == 'c1'"
```

### Heatmap with Annotations
```toml
[SeuratClusterStats.envs.features."Marker heatmap"]
features = {
  "T cell markers" = ["CD3D", "CD4", "CD8A"],
  "B cell markers" = ["MS4A1"],
  "Monocyte markers" = ["CD14", "LYZ", "FCGR3A"],
  "NK cell markers" = ["NCAM1", "KLRD1"]
}
plot_type = "heatmap"
ident = "Diagnosis"
columns_split_by = "seurat_clusters"
name = "Expression"
devpars = {height = 560}
cell_type = "dot"
dot_size = "nanmean"
dot_size_name = "Percent Expressed"
column_annotation = ["percent.mt", "VDJ_Presence"]
column_annotation_type = {percent.mt = "violin", VDJ_Presence = "pie"}
devpars = {width = 1400, height = 900}
```

### Advanced Dimplot
```toml
[SeuratClusterStats.envs.dimplots."UMAP with labels"]
label = true

[SeuratClusterStats.envs.dimplots."UMAP with marks"]
add_mark = true
mark_linetype = 2

[SeuratClusterStats.envs.dimplots."UMAP by Diagnosis"]
facet_by = "Diagnosis"
highlight = true
theme = "theme_blank"

[SeuratClusterStats.envs.dimplots."UMAP with hex bins"]
hex = true
hex_bins = 50

[SeuratClusterStats.envs.dimplots."UMAP with stat"]
stat_by = "Diagnosis"
stat_plot_type = "ring"
stat_plot_size = 0.15
```

## Common Patterns

### Pattern 1: Basic UMAP Visualization
```toml
[SeuratClusterStats.envs.dimplots."Basic UMAP"]
label = true
reduction = "umap"
```

### Pattern 2: QC Metrics per Cluster
```toml
[SeuratClusterStats.envs.ngenes."Genes per cluster"]
plot_type = "violin"
add_box = true
add_point = true

[SeuratClusterStats.envs.stats."QC stats"]
plot_type = "bar"
group_by = "percent.mt_bin"
x_text_angle = 90
```

### Pattern 3: Custom Feature Plots
```toml
# From file
[SeuratClusterStats.envs.features_defaults]
features = "file://path/to/custom_markers.txt"

[SeuratClusterStats.envs.features."Custom markers"]
plot_type = "violin"
ident = "seurat_clusters"
comparisons = true
sig_label = "p.signif"
```

### Pattern 4: Cluster Comparison Sankey
```toml
[SeuratClusterStats.envs.stats."Cluster flow by condition"]
plot_type = "sankey"
group_by = ["seurat_clusters", "Diagnosis"]
links_alpha = 0.6
devpars = {width = 800}
```

### Pattern 5: Subclustering Visualization
```toml
[SeuratClusterStats.envs.dimplots."Subcluster UMAP"]
group_by = "sub_clusters"
reduction = "umap"  # Uses sub_umap_<ident> automatically
label = true
```

## Dependencies
- **Upstream**: `SeuratClustering`, `SeuratSubClustering` (via `CombinedInput`)
- **Downstream**: None (terminal visualization process)
- **Data**: Seurat object with cluster assignments and optional subclustering

## Validation Rules
- **Feature names**: Must match gene symbols or metadata columns in Seurat object
- **Reduction names**: Must exist in Seurat object (umap, tsne, pca, or sub_umap_<ident>)
- **Plot types**: Must be valid plotthis plot types
- **Metadata columns**: Must exist in `@meta.data` slot
- **Device parameters**: Positive integers required for width/height/res

## Troubleshooting

### Plot generation errors
- **"Feature not found"**: Check gene symbols match case sensitivity (human: UPPERCASE, mouse: TitleCase)
- **"Reduction not found"**: Verify reduction name in `Reducuctions(srtobj)` object
- **Empty plots**: Check if `subset` expression filters out all cells
- **Slow rendering**: Use `cache = true` for feature plots, reduce `hex_bins` or downsample

### Visual quality issues
- **Overcrowded labels**: Use `label_repel = true` or reduce number of clusters
- **Poor color contrast**: Set custom `palette` parameter
- **Incorrect orientation**: Use `flip = true` to transpose plot
- **Missing annotations**: Verify `column_annotation` columns exist in metadata

### Missing subcluster UMAP
- If subclustering exists but `sub_umap_<ident>` not found, process uses standard UMAP
- To force subcluster visualization: Run `RunUMAP()` on subcluster level or specify `reduction = "umap"`

### Large dataset performance
- Enable `hex = true` for dimplots with >10,000 cells
- Use `downsample` parameter in feature plots
- Set `cache = true` to avoid re-rendering expensive plots

## Output Structure
```
<srtobj_stem>.cluster_stats/
├── clustrees/          # Clustree plots (png + pdf)
├── stats/              # Cell count/statistics plots
├── ngenes/             # Gene count plots
├── features/           # Gene expression visualizations
└── dimplots/           # Dimension reduction plots
```

Each subdirectory contains plots for each configured case in the process environment.
