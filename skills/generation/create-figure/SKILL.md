---
name: create-figure
description: >
  Create publication-quality figures, charts, and diagrams.
  Multi-backend: Graphviz, Mermaid, NetworkX/D3, matplotlib, plotly, seaborn.
  50+ visualization types for any domain.
allowed-tools: Bash, Read
triggers:
  # General
  - create figure
  - create chart
  - create diagram
  - create plot
  - generate figure
  - make chart
  - publication figure
  - IEEE figure
  # Architecture & Code
  - architecture diagram
  - dependency graph
  - class diagram
  - UML diagram
  - module dependencies
  - workflow diagram
  - pipeline diagram
  # Metrics & Data
  - metrics visualization
  - bar chart
  - pie chart
  - line chart
  - heatmap
  - correlation matrix
  # Control Systems
  - bode plot
  - nyquist plot
  - root locus
  # ML/LLM
  - confusion matrix
  - ROC curve
  - training curves
  - scaling law
  - attention heatmap
  # Biology
  - violin plot
  - volcano plot
  - survival curve
metadata:
  short-description: "Create figures, charts, diagrams (50+ types)"
---

# create-figure

Generate publication-quality figures from code analysis data for academic papers.

## Quick Start for Agents

**Don't get overwhelmed by 50+ commands!** Use domain navigation:

```bash
# Step 1: Find your domain
create-figure domains

# Step 2: List commands for your domain
create-figure list --domain ml        # ML/LLM projects
create-figure list --domain control   # Aerospace/control systems
create-figure list --domain bio       # Bioinformatics

# Step 3: Or get recommendations by data type
create-figure recommend --data-type classification
create-figure recommend --data-type time_series
create-figure recommend --show-types  # See all data types
```

### Domain Quick Reference

| Domain | Use For | Key Commands |
|--------|---------|--------------|
| **core** | Any project | `metrics`, `workflow`, `architecture`, `deps` |
| **ml** | ML/LLM evaluation | `confusion-matrix`, `roc-curve`, `training-curves`, `scaling-law` |
| **control** | Aerospace, control systems | `bode`, `nyquist`, `rootlocus`, `state-space` |
| **field** | Nuclear, thermal, physics | `contour`, `vector-field`, `heatmap` |
| **project** | Scheduling, requirements | `gantt`, `pert`, `radar`, `sankey` |
| **math** | Pure mathematics | `3d-surface`, `complex-plane`, `phase-portrait` |
| **bio** | Bioinformatics, medical | `violin`, `volcano`, `survival-curve`, `manhattan` |
| **hierarchy** | Breakdowns, fault trees | `treemap`, `sunburst`, `force-graph` |

---

## Architecture

Multi-backend design for maximum compatibility:

| Backend | Use Case | Output Formats |
|---------|----------|----------------|
| **Graphviz** | Deterministic layouts, CI-friendly | PDF, PNG, SVG, DOT |
| **Mermaid** | Quick documentation, GitHub-compatible | PDF, PNG, SVG, MMD |
| **NetworkX** | Graph manipulation, D3 export | JSON, PDF, PNG |
| **matplotlib/seaborn** | Publication charts (IEEE settings) | PDF, PNG, SVG |
| **plotly** | Interactive Sankey, sunburst, treemap | PDF, PNG, HTML |
| **pydeps** | Python module dependencies | via Graphviz |
| **pyreverse** | UML class diagrams | via Graphviz |

## Common Commands

### `deps` - Dependency Graph

```bash
./run.sh deps --project /path/to/package --output deps.pdf
./run.sh deps -p ./src -o deps.svg --backend mermaid --depth 3
```

### `architecture` - Architecture Diagram

```bash
./run.sh architecture --project ./assess_output.json --output arch.pdf
```

### `metrics` - Metrics Chart

```bash
./run.sh metrics --input data.json --output metrics.pdf --type bar
./run.sh metrics -i data.json -o chart.pdf --type pie --title "Issue Distribution"
```

Chart types: `bar`, `hbar`, `pie`, `line`

### `workflow` - Workflow Diagram

```bash
./run.sh workflow --stages "Scope,Analysis,Search,Learn,Draft" --output workflow.pdf
```

### `confusion-matrix` - Confusion Matrix

```bash
./run.sh confusion-matrix --input results.json --output confusion.pdf --normalize
```

### `roc-curve` - ROC Curve

```bash
./run.sh roc-curve --input roc_data.json --output roc.pdf
```

### `bode` - Bode Plot

```bash
./run.sh bode --num 1,2 --den 1,3,2 --output bode.pdf
```

### `heatmap` - Heatmap

```bash
./run.sh heatmap --input matrix.json --output flux.pdf --cmap plasma
```

### `sankey` - Sankey Diagram

```bash
./run.sh sankey --input flows.json --output sankey.pdf
```

### `from-assess` - Generate All Figures

Generate all figures from /assess output in one command:

```bash
./run.sh from-assess --input assess_output.json --output-dir ./figures/
```

Generates:
- `architecture.pdf` - System architecture diagram
- `dependencies.pdf` - Module dependency graph
- `features.pdf` - Feature distribution chart
- `issues.pdf` - Issue severity pie chart

## Publication Quality Settings

matplotlib figures use IEEE publication settings:
- Font: 8pt Times New Roman (serif)
- DPI: 600 for saving, 300 for display
- Column widths: Single (3.5"), Double (7.16")
- TrueType fonts for Illustrator compatibility

## Dependencies

**Required:**
- Python 3.10+
- typer
- numpy

**Optional (enables features):**

| Package | Features Enabled |
|---------|------------------|
| matplotlib | All charts, plots, diagrams |
| seaborn | Heatmaps, publication styling |
| plotly | Sankey, sunburst, treemap, interactive |
| networkx | Force-directed graphs, PERT |
| scipy | Bode/Nyquist fallback, contours |
| control | Bode, Nyquist, root locus |
| graphviz | Dependency/architecture diagrams |

## Installation

```bash
# Core
pip install typer numpy matplotlib

# Full installation (all features)
pip install typer numpy matplotlib seaborn plotly networkx pandas squarify scipy control pydeps pylint

# System dependencies
apt install graphviz  # Debian/Ubuntu
npm install -g @mermaid-js/mermaid-cli
```
