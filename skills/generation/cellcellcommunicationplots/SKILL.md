---
name: cellcellcommunicationplots
description: Visualize cell-cell communication inference results from CellCellCommunication process. Creates publication-ready network diagrams, heatmaps, and interaction plots to help interpret ligand-receptor interactions between cell types.
---

# CellCellCommunicationPlots Process Configuration

## Purpose
Visualize cell-cell communication inference results from CellCellCommunication process. Creates publication-ready network diagrams, heatmaps, and interaction plots to help interpret ligand-receptor interactions between cell types.

## When to Use
- After running CellCellCommunication to visualize inferred interactions
- To create publication-quality figures for cell communication analysis
- For exploring signaling pathways between cell populations
- When needing multiple visualization types (network, heatmap, box plots) for comprehensive analysis
- To subset and focus on specific pathways or cell type pairs of interest

## Configuration Structure

### Process Enablement
```toml
[CellCellCommunicationPlots]
cache = true  # Recommended to skip replotting when only adjusting parameters
```

### Input Specification
```toml
[CellCellCommunicationPlots.in]
# cccfile: Path to the output from CellCellCommunication process
# This is typically a text file with ligand-receptor interaction data
cccfile = ["CellCellCommunication"]
```

### Environment Variables

#### Data Filtering Options
```toml
[CellCellCommunicationPlots.envs]
# subset: dplyr filter expression to subset interactions
# Examples: subset = "source == 'T cells' & target == 'Macrophages'"
#          subset = "pathway == 'TNF signaling'"
subset = ""

# magnitude: Column name for interaction magnitude/strength
# Default: second last column in the data
# Common values: "magnitude", "score", "probability", "importance"
magnitude = "importance"

# specificity: Column name for interaction specificity
# Default: last column in the data
# Set to null (None) if method doesn't have specificity metric
specificity = "specificity"
```

#### Plot Rendering Parameters
```toml
[CellCellCommunicationPlots.envs.devpars]
# Plot resolution and dimensions
res = 100       # Resolution in DPI (default: 100)
height = 2000   # Plot height in pixels (optional)
width = 2000    # Plot width in pixels (optional)

[CellCellCommunicationPlots.envs]
# Additional output formats beyond PNG
more_formats = ["pdf", "svg"]  # Default: []

# Description shown in report
descr = "Cell-cell communication plot"
```

#### Cases Configuration (Multiple Plots)
```toml
[CellCellCommunicationPlots.envs.cases]
# Dictionary of plot configurations
# Keys = plot names (used in report filenames)
# Values = arguments passed to scplotter::CCCPlot

# Default case if none specified
[CellCellCommunicationPlots.envs.cases."Cell-Cell Communication"]
plot_type = "network"
```

## CellChat Plot Types

### Available Plot Types

#### network
**Description**: Network plot with cell types as nodes and interactions as edges. Best for overview of communication patterns.

**Use when**: You want to see the global communication network structure, identify major signaling hubs, or visualize cell type connectivity.

**Example**:
```toml
[CellCellCommunicationPlots.envs.cases."Cell-Cell Communication Network"]
plot_type = "network"
legend-position = "none"  # Remove legend for cleaner look
theme = "theme_blank"
theme_args = {add_coord = false}
```

#### chord / circos
**Description**: Circular chord diagram showing interaction flows between cell types. Equivalent to "circos" (alias).

**Use when**: You want to visualize bidirectional communication flows in a compact circular format, excellent for publication figures.

**Example**:
```toml
[CellCellCommunicationPlots.envs.cases."Cell-Cell Communication Circos Plot"]
plot_type = "circos"
```

#### heatmap
**Description**: Heatmap matrix with source cell types as rows and target cell types as columns. Color intensity represents interaction strength.

**Use when**: You want to identify strong/weak interactions at a glance, compare interaction patterns across many cell pairs, or find hotspots of communication.

**Example**:
```toml
[CellCellCommunicationPlots.envs.cases."Cell-Cell Communication Heatmap"]
plot_type = "heatmap"
```

#### sankey / alluvial
**Description**: Sankey/alluvial flow diagram showing communication as flows from senders to receivers. Equivalent to "alluvial" (alias).

**Use when**: You want to visualize communication as flows, highlight major pathways, or show directional emphasis.

**Example**:
```toml
[CellCellCommunicationPlots.envs.cases."Cell-Cell Communication Sankey"]
plot_type = "sankey"
```

#### dot
**Description**: Dot plot showing interaction strength with dot size/color. Compact alternative to network plots.

**Use when**: You have many cell types and network plot becomes too dense, or when you prefer a more compact visualization.

**Example**:
```toml
[CellCellCommunicationPlots.envs.cases."Cell-Cell Communication Dot"]
plot_type = "dot"
x_text_angle = 90  # Rotate x-axis labels for readability
```

#### box
**Description**: Box plots for source cell types, where each x is a target cell type and values are interaction strengths of ligand-receptor pairs. Requires `method = "interaction"`.

**Use when**: You want to see the distribution of interaction strengths, identify outliers, or compare variability across interactions.

**Example**:
```toml
[CellCellCommunicationPlots.envs.cases."Cell-Cell Communication Interaction (Box Plot)"]
plot_type = "box"
method = "interaction"
x_text_angle = 90
```

#### violin
**Description**: Violin plots similar to box plots but showing full distribution shape. Requires `method = "interaction"`.

**Use when**: You want to see the full distribution of interaction strengths, identify multi-modal patterns, or compare distribution shapes.

**Example**:
```toml
[CellCellCommunicationPlots.envs.cases."Cell-Cell Communication Violin"]
plot_type = "violin"
method = "interaction"
add_box = true  # Add box plot overlay
```

#### ridge
**Description**: Ridge (joy) plots for source cell types, each row is a target cell type. Requires `method = "interaction"`.

**Use when**: You want to compare distributions across many target cell types, or when you prefer a compact density visualization.

**Example**:
```toml
[CellCellCommunicationPlots.envs.cases."Cell-Cell Communication Ridge"]
plot_type = "ridge"
method = "interaction"
```

### Method Parameter

Two methods control what data is plotted:

**method = "aggregation"** (default)
- Aggregates ligand-receptor pairs for each source-target pair
- Shows only source/target cell type pairs
- Best for overview visualization

**method = "interaction"**
- Plots individual ligand-receptor pair interactions
- Shows specific ligand-receptor pairs driving communication
- Required for box, violin, and ridge plot types
- Best for detailed pathway analysis

## Configuration Examples

### Minimal Configuration (Default Plot)
```toml
[CellCellCommunicationPlots.in]
cccfile = ["CellCellCommunication"]
```

### Overview Plots (Quick Exploration)
```toml
[CellCellCommunicationPlots.in]
cccfile = ["CellCellCommunication"]

[CellCellCommunicationPlots.envs.cases."Network Overview"]
plot_type = "network"
legend-position = "right"

[CellCellCommunicationPlots.envs.cases."Heatmap Overview"]
plot_type = "heatmap"
```

### Pathway-Specific Plots (Deep Dive)
```toml
[CellCellCommunicationPlots.in]
cccfile = ["CellCellCommunication"]

# Focus on specific pathways (uses subset filter)
[CellCellCommunicationPlots.envs.cases."TNF Signaling"]
plot_type = "network"
subset = "pathway == 'TNF signaling'"
legend-position = "none"

[CellCellCommunicationPlots.envs.cases."IL6 Pathway"]
plot_type = "heatmap"
subset = "pathway == 'IL-6 signaling'"
```

### Cell Type Pair Focus
```toml
[CellCellCommunicationPlots.in]
cccfile = ["CellCellCommunication"]

# Focus on specific sender-receiver pairs
[CellCellCommunicationPlots.envs.cases."T cell to Macrophage"]
plot_type = "box"
method = "interaction"
subset = "source == 'T cell' & target == 'Macrophage'"

[CellCellCommunicationPlots.envs.cases."T cell to B cell"]
plot_type = "dot"
subset = "source == 'T cell' & target == 'B cell'"
```

### Publication Figure Set (Comprehensive)
```toml
[CellCellCommunicationPlots.in]
cccfile = ["CellCellCommunication"]

[CellCellCommunicationPlots.envs.devpars]
res = 300  # High resolution for publication

[CellCellCommunicationPlots.envs]
more_formats = ["pdf", "svg"]

[CellCellCommunicationPlots.envs.cases."Figure 1A: Network"]
plot_type = "network"
legend-position = "none"
theme = "theme_blank"
theme_args = {add_coord = false}

[CellCellCommunicationPlots.envs.cases."Figure 1B: Heatmap"]
plot_type = "heatmap"

[CellCellCommunicationPlots.envs.cases."Figure 1C: Circos"]
plot_type = "circos"

[CellCellCommunicationPlots.envs.cases."Supplementary: Interaction Distribution"]
plot_type = "box"
method = "interaction"
x_text_angle = 90
```

### Table Output (Data Export)
```toml
[CellCellCommunicationPlots.in]
cccfile = ["CellCellCommunication"]

[CellCellCommunicationPlots.envs.cases."Interaction Table"]
plot_type = "table"  # Special type to export data as text file
```

## Common Patterns

### Pattern 1: Overview + Detail
```toml
# First, get a global overview with network and heatmap
[CellCellCommunicationPlots.envs.cases."Global Network"]
plot_type = "network"

[CellCellCommunicationPlots.envs.cases."Global Heatmap"]
plot_type = "heatmap"

# Then, explore top pathways in detail
[CellCellCommunicationPlots.envs.cases."Top Pathway Interactions"]
plot_type = "box"
method = "interaction"
subset = "pathway == 'CXCL' | pathway == 'CCL'"
```

### Pattern 2: Comparing Specific Cell Types
```toml
# All communications from T cells
[CellCellCommunicationPlots.envs.cases."T cell as Sender"]
plot_type = "chord"
subset = "source == 'T cell'"

# All communications to T cells
[CellCellCommunicationPlots.envs.cases."T cell as Receiver"]
plot_type = "chord"
subset = "target == 'T cell'"

# Specific interaction pair with full detail
[CellCellCommunicationPlots.envs.cases."T cell <-> Macrophage Details"]
plot_type = "violin"
method = "interaction"
subset = "(source == 'T cell' & target == 'Macrophage') | (source == 'Macrophage' & target == 'T cell')"
```

### Pattern 3: Publication-Ready Workflow
```toml
# Set high resolution for all plots
[CellCellCommunicationPlots.envs.devpars]
res = 300
height = 2500
width = 2500

[CellCellCommunicationPlots.envs]
more_formats = ["pdf"]  # Export as PDF for publication

# Main figure: clean network
[CellCellCommunicationPlots.envs.cases."Main Figure"]
plot_type = "network"
legend-position = "none"
theme = "theme_blank"
theme_args = {add_coord = false}

# Supplementary: detailed heatmap
[CellCellCommunicationPlots.envs.cases."Supplementary Heatmap"]
plot_type = "heatmap"

# Supplementary: interaction distribution
[CellCellCommunicationPlots.envs.cases."Supplementary Distribution"]
plot_type = "ridge"
method = "interaction"
```

## Dependencies

### Upstream Processes
- **CellCellCommunication**: Required. Provides the ligand-receptor interaction data file (cccfile). This process must complete successfully with interaction inference.

### Downstream Processes
- **None**: CellCellCommunicationPlots is a terminal visualization process. No downstream processes depend on its output.

## Validation Rules

### Input Validation
- `cccfile` must point to a valid output file from CellCellCommunication
- File must contain columns: `source`, `target`, `ligand`, `receptor`, plus magnitude/specificity columns

### Plot Type Validation
- Valid `plot_type` values: "dot", "network", "chord", "circos", "heatmap", "sankey", "alluvial", "box", "violin", "ridge"
- "box", "violin", and "ridge" require `method = "interaction"`

### Subset Expression Validation
- `subset` must be valid dplyr::filter() expression
- Column names in expression must exist in the input data

### Method Validation
- Valid `method` values: "aggregation", "interaction"

## Troubleshooting

### Issue: Too many edges in network plot
**Problem**: Network plot becomes unreadable with many interactions

**Solutions**:
- Use `subset` to filter to specific pathways or cell types:
  ```toml
  subset = "pathway %in% c('TNF', 'CXCL', 'CCL')"
  subset = "importance > 0.5"  # Filter by strength
  ```
- Use `heatmap` instead for better overview with many cell types
- Use `circos` for more compact visualization

### Issue: Unreadable axis labels
**Problem**: Cell type labels overlap or are too small

**Solutions**:
```toml
# Rotate x-axis labels
x_text_angle = 90

# For network plots, adjust legend position
legend-position = "bottom"

# For heatmap, toggle row/column name display
show_row_names = true
show_column_names = true
```

### Issue: Box/violin plots show nothing
**Problem**: Box, violin, or ridge plots are empty

**Cause**: These plot types require `method = "interaction"`

**Solution**:
```toml
[CellCellCommunicationPlots.envs.cases."My Plot"]
plot_type = "box"  # or "violin", "ridge"
method = "interaction"  # Required!
```

### Issue: Specificity column not found
**Problem**: Error about missing specificity column

**Cause**: Some inference methods don't provide specificity scores

**Solution**:
```toml
[CellCellCommunicationPlots.envs]
specificity = null  # Set to null if not available
# OR specify a different column:
specificity = "pvalue"
```

### Issue: Plot file too large
**Problem**: High-resolution plots consume too much disk space

**Solutions**:
```toml
[CellCellCommunicationPlots.envs.devpars]
res = 100  # Reduce from 300 to 100 DPI

[CellCellCommunicationPlots.envs]
more_formats = []  # Remove PDF/SVG exports, keep only PNG
```

### Issue: Incorrect magnitude/specificity columns
**Problem**: Plots show unexpected values or are blank

**Cause**: Default column selection (second last / last) doesn't match your data

**Solution**: Explicitly specify correct column names
```toml
[CellCellCommunicationPlots.envs]
# Check your cccfile headers and match these:
magnitude = "score"  # or "probability", "importance", etc.
specificity = "pvalue"  # or "specificity", "fdr", etc.
```

## External References

- **scplotter::CCCPlot**: https://pwwang.github.io/scplotter/reference/CCCPlot.html
- **LIANA methods**: https://liana-py.readthedocs.io/en/latest/notebooks/basic_usage.html#Tileplot
- **CellChat**: http://www.cellchat.org/
- **CCPlotR**: https://bioconductor.org/packages/CCPlotR/
- **Cell-cell communication best practices**: https://www.sc-best-practices.org/mechanisms/cell_cell_communication.html
