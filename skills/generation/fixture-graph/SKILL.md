---
name: fixture-graph
description: >
  Generate publication-quality figures from code analysis data.
  Multi-backend: Graphviz, Mermaid, NetworkX/D3, matplotlib, plotly, seaborn.
  Supports aerospace, nuclear, military, and mathematics visualization types.
  Integrates pydeps, pyreverse, python-control, and lean4-prove.
allowed-tools: Bash, Read
triggers:
  # General
  - generate figures
  - create diagram
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
  # Hierarchical
  - treemap
  - sunburst chart
  - fault tree
  - breakdown chart
  # Network & Graph
  - force directed graph
  - network diagram
  - system topology
  - PERT network
  - critical path
  # Control Systems (Aerospace/Nuclear)
  - bode plot
  - nyquist plot
  - root locus
  - frequency response
  - stability analysis
  - control system
  # Field Visualizations (Nuclear/Physics)
  - contour plot
  - flux distribution
  - temperature field
  - vector field
  - flow field
  - phase portrait
  - streamlines
  # Engineering
  - sankey diagram
  - energy flow
  - mass balance
  - parallel coordinates
  - DOE analysis
  - design space
  - radar chart
  - spider chart
  # Project Management (Military/Aerospace)
  - gantt chart
  - project schedule
  - timeline
  # Mathematics
  - polar plot
  - phase space
  - dynamical system
  - differential equations
  # GPU/Hardware Performance
  - roofline plot
  - roofline analysis
  - GPU performance
  - memory bandwidth
  - compute intensity
  - throughput latency
  - inference benchmark
  # LLM/ML Metrics
  - scaling law
  - scaling plot
  - training curves
  - loss curves
  - confusion matrix
  - ROC curve
  - AUC curve
  - precision recall
  - PR curve
  - attention heatmap
  - attention weights
  - embedding visualization
  - t-SNE plot
  - UMAP plot
  - embedding scatter
  - feature importance
  - calibration plot
  - reliability diagram
  # Biology/Bioinformatics
  - violin plot
  - gene expression
  - volcano plot
  - differential expression
  - survival curve
  - Kaplan-Meier
  - manhattan plot
  - GWAS
  - genome wide
  # Formal Methods
  - formal verification
  - lean4 theorem
  - requirement proof
metadata:
  short-description: Publication-quality figures for aerospace, nuclear, military, mathematics
---

# Fixture-Graph Skill

## ⚡ Quick Start for Agents

**Don't get overwhelmed by 50+ commands!** Use domain navigation:

```bash
# Step 1: Find your domain
fixture-graph domains

# Step 2: List commands for your domain
fixture-graph list --domain ml        # ML/LLM projects
fixture-graph list --domain control   # Aerospace/control systems
fixture-graph list --domain bio       # Bioinformatics

# Step 3: Or get recommendations by data type
fixture-graph recommend --data-type classification
fixture-graph recommend --data-type time_series
fixture-graph recommend --show-types  # See all data types
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

Generate publication-quality figures from code analysis data for academic papers.

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
| **lean4-prove** | Formal theorem verification | .lean files |

## D3-Style Scientific Visualizations

Advanced visualization types for scientific and engineering papers:

| Graph Type | Engineering Use | Backend |
|------------|-----------------|---------|
| **Sankey diagrams** | Energy/mass flow balances, reactor coolant | plotly/matplotlib |
| **Heatmaps** | Field distributions, neutron flux, temp | seaborn/matplotlib |
| **Treemaps** | Component breakdown, zone hierarchies | plotly/squarify |
| **Sunburst charts** | Fault hierarchies, module structure | plotly |
| **Force-directed** | System topology, P&ID, fault trees | NetworkX |
| **Parallel coordinates** | Multi-dimensional DOE analysis | pandas/plotly |
| **Chord diagrams** | Fuel cycle flows, interdependencies | NetworkX |

## Control Systems & Engineering Plots

Specialized visualizations for aerospace, nuclear, and control systems:

| Graph Type | Engineering Use | Backend |
|------------|-----------------|---------|
| **Bode plots** | Frequency response, stability margins | python-control/scipy |
| **Nyquist plots** | Stability analysis, gain/phase margins | python-control/scipy |
| **Root locus** | Pole placement, gain tuning | python-control/scipy |
| **Polar plots** | Antenna patterns, wind roses | matplotlib |
| **Contour plots** | Neutron flux, temperature fields, stress | matplotlib |
| **Vector fields** | Flow fields, gradients, velocity | matplotlib |
| **Phase portraits** | Dynamical systems, stability regions | matplotlib |
| **Radar charts** | Multi-attribute comparison | matplotlib |
| **Gantt charts** | Project scheduling, milestones | matplotlib |
| **PERT networks** | Critical path analysis | matplotlib/networkx |

## GPU/Hardware Performance Visualizations

Specialized visualizations for GPU, CUDA, and hardware performance papers:

| Graph Type | Use Case | Backend |
|------------|----------|---------|
| **Roofline plots** | Compute vs memory bound analysis, kernel optimization | matplotlib |
| **Throughput/Latency** | Inference benchmarks, batching analysis | matplotlib |
| **Scaling law plots** | Parameter/compute/data scaling (Chinchilla-style) | matplotlib |
| **Training curves** | Multi-run loss/accuracy with std shading | matplotlib |

## LLM/ML Visualization Types

Specialized visualizations for machine learning and LLM papers:

| Graph Type | Use Case | Backend |
|------------|----------|---------|
| **Confusion matrix** | Classification evaluation, error analysis | matplotlib |
| **ROC curves** | Binary classification, AUC comparison | matplotlib |
| **Attention heatmaps** | Transformer attention visualization | matplotlib |
| **Embedding scatter** | t-SNE/UMAP token/document embeddings | sklearn/umap |
| **Precision-Recall curves** | Multi-class classification metrics | matplotlib |
| **Feature importance** | Model interpretability, XGBoost/RF | matplotlib |
| **Calibration plots** | Probability calibration (reliability) | matplotlib |

## Biology/Bioinformatics Visualizations

Specialized visualizations for biological and medical research:

| Graph Type | Use Case | Backend |
|------------|----------|---------|
| **Violin plots** | Gene expression, distribution comparison | matplotlib |
| **Volcano plots** | Differential expression, fold change | matplotlib |
| **Survival curves** | Kaplan-Meier, clinical outcomes | matplotlib |
| **Manhattan plots** | GWAS, genome-wide association | matplotlib |

## Commands

### `deps` - Dependency Graph

Generate dependency graph from Python project.

```bash
./run.sh deps --project /path/to/package --output deps.pdf
./run.sh deps -p ./src -o deps.svg --backend mermaid --depth 3
./run.sh deps -p ./src -o deps.json --backend networkx --format json
```

Options:
- `--project, -p`: Path to Python package/module (required)
- `--output, -o`: Output file (default: dependencies.pdf)
- `--format, -f`: Output format (pdf, png, svg, dot, json)
- `--depth, -d`: Maximum dependency depth (default: 2)
- `--backend, -b`: graphviz, mermaid, networkx

### `uml` - UML Class Diagram

Generate UML class diagram using pyreverse.

```bash
./run.sh uml --project ./src --output classes.pdf
```

Requires: `pip install pylint`

### `architecture` - Architecture Diagram

Generate architecture diagram from project or /assess JSON.

```bash
./run.sh architecture --project ./assess_output.json --output arch.pdf
./run.sh architecture -p /path/to/project -o arch.svg --backend mermaid
```

### `metrics` - Metrics Chart

Generate publication-quality metrics chart with IEEE styling.

```bash
./run.sh metrics --input data.json --output metrics.pdf --type bar
./run.sh metrics -i data.json -o chart.pdf --type pie --title "Issue Distribution"
```

Chart types: `bar`, `hbar`, `pie`, `line`

Input formats:
```json
// Simple dict
{"Feature A": 42, "Feature B": 28}

// With "metrics" key
{"metrics": {"LOC": 1500, "Functions": 45}}

// List format
[{"name": "A", "value": 10}, {"name": "B", "value": 20}]
```

### `table` - LaTeX Table

Generate LaTeX table with proper escaping.

```bash
./run.sh table --input features.json --output table.tex --caption "Feature Comparison"
```

### `workflow` - Workflow Diagram

Generate workflow/pipeline diagram with quality gates.

```bash
./run.sh workflow --stages "Scope,Analysis,Search,Learn,Draft" --output workflow.pdf
./run.sh workflow -s "A,B,C,D" -o flow.svg --no-gates --backend graphviz
```

### `theorem` - Formal Verification

Generate formally verified theorem from requirement (uses lean4-prove).

```bash
./run.sh theorem --requirement "All inputs must be validated" --name input_validation --output theorem.lean
```

### `sankey` - Sankey Diagram

Generate Sankey diagram for energy/mass flow balances.

```bash
./run.sh sankey --input flows.json --output sankey.pdf --title "Reactor Coolant Flow"
```

Input format:
```json
[{"source": "Primary", "target": "Heat Exchanger", "value": 1000}]
```

### `heatmap` - Heatmap

Generate heatmap for field distributions or correlation matrices.

```bash
./run.sh heatmap --input matrix.json --output flux.pdf --cmap plasma --title "Neutron Flux"
```

### `treemap` - Treemap

Generate treemap for hierarchical size data.

```bash
./run.sh treemap --input sizes.json --output breakdown.pdf
```

### `sunburst` - Sunburst Chart

Generate sunburst chart for hierarchical fault trees.

```bash
./run.sh sunburst --input hierarchy.json --output faults.pdf
```

### `force-graph` - Force-Directed Graph

Generate force-directed graph for system topology.

```bash
./run.sh force-graph --input network.json --output topology.pdf
```

### `parallel-coords` - Parallel Coordinates

Generate parallel coordinates for multi-dimensional DOE analysis.

```bash
./run.sh parallel-coords --input experiments.json --output doe.pdf --color-by efficiency
```

### `radar` - Radar Chart

Generate radar/spider chart for multi-attribute comparison.

```bash
./run.sh radar --input attributes.json --output comparison.pdf
```

Input format:
```json
{"Design A": {"Safety": 8, "Cost": 6, "Efficiency": 9}, "Design B": {"Safety": 9, "Cost": 4, "Efficiency": 7}}
```

### `bode` - Bode Plot

Generate Bode plot for control systems frequency response.

```bash
./run.sh bode --num 1,2 --den 1,3,2 --output bode.pdf --freq-min 0.01 --freq-max 100
```

### `nyquist` - Nyquist Plot

Generate Nyquist plot for stability analysis.

```bash
./run.sh nyquist --num 1,2 --den 1,3,2,0 --output nyquist.pdf
```

### `rootlocus` - Root Locus

Generate root locus for control system gain analysis.

```bash
./run.sh rootlocus --num 1 --den 1,5,6 --output rootlocus.pdf
```

### `polar` - Polar Plot

Generate polar plot for directional data (antenna patterns, wind roses).

```bash
./run.sh polar --input pattern.json --output antenna.pdf
```

### `contour` - Contour Plot

Generate contour plot for field distributions (flux, temperature, stress).

```bash
./run.sh contour --input field.json --output flux.pdf --cmap plasma --levels 30
```

Input format:
```json
{"x": [0, 1, 2], "y": [0, 1, 2], "z": [[0,1,2],[1,2,3],[2,3,4]]}
```

### `gantt` - Gantt Chart

Generate Gantt chart for project scheduling.

```bash
./run.sh gantt --input schedule.json --output timeline.pdf
```

Input format:
```json
[{"task": "Design", "start": 0, "end": 5, "progress": 100}]
```

### `pert` - PERT Network

Generate PERT network diagram for critical path analysis.

```bash
./run.sh pert --input network.json --output cpm.pdf
```

### `vector-field` - Vector Field

Generate vector field for flow visualization.

```bash
./run.sh vector-field --input flow.json --output velocity.pdf --streamlines
```

### `phase-portrait` - Phase Portrait

Generate phase portrait for dynamical systems.

```bash
./run.sh phase-portrait --equations "dx = y; dy = -x - 0.5*y" --output damped.pdf
```

### `roofline` - Roofline Plot

Generate roofline plot for GPU/hardware performance analysis.

```bash
./run.sh roofline --input kernels.json --output roofline.pdf
```

Input format:
```json
{"peak_flops": 19.5e12, "peak_bandwidth": 900e9, "kernels": [{"name": "GEMM", "flops": 1e12, "bytes": 1e9}]}
```

### `scaling-law` - Scaling Law Plot

Generate log-log scaling law plot (common in LLM papers).

```bash
./run.sh scaling-law --input params_vs_loss.json --output scaling.pdf --fit
```

### `confusion-matrix` - Confusion Matrix

Generate confusion matrix for classification results.

```bash
./run.sh confusion-matrix --input results.json --output confusion.pdf --normalize
```

### `roc-curve` - ROC Curve

Generate ROC curve with AUC for binary classification.

```bash
./run.sh roc-curve --input roc_data.json --output roc.pdf
```

### `training-curves` - Training Curves

Generate multi-run training curves with std shading.

```bash
./run.sh training-curves --input runs.json --output loss.pdf --log-y
```

### `attention-heatmap` - Attention Heatmap

Generate transformer attention visualization.

```bash
./run.sh attention-heatmap --input attention.json --output attn.pdf
```

### `embedding-scatter` - Embedding Scatter

Generate t-SNE or UMAP visualization of embeddings.

```bash
./run.sh embedding-scatter --input embeddings.json --output tsne.pdf --method tsne
```

### `throughput-latency` - Throughput vs Latency

Generate throughput vs latency plot for inference benchmarks.

```bash
./run.sh throughput-latency --input benchmarks.json --output perf.pdf
```

### `pr-curve` - Precision-Recall Curve

Generate Precision-Recall curve for classification.

```bash
./run.sh pr-curve --input pr_data.json --output pr.pdf
```

### `violin` - Violin Plot

Generate violin plot for distribution comparison.

```bash
./run.sh violin --input expression.json --output violin.pdf --y-label "Expression"
```

### `volcano` - Volcano Plot

Generate volcano plot for differential expression analysis.

```bash
./run.sh volcano --input deseq.json --output volcano.pdf --fc 1.5 --pval 0.01
```

### `survival-curve` - Kaplan-Meier Survival Curve

Generate Kaplan-Meier survival curve.

```bash
./run.sh survival-curve --input survival.json --output km.pdf
```

### `manhattan` - Manhattan Plot

Generate Manhattan plot for GWAS results.

```bash
./run.sh manhattan --input gwas.json --output manhattan.pdf
```

### `feature-importance` - Feature Importance

Generate feature importance bar chart.

```bash
./run.sh feature-importance --input importance.json --output features.pdf --top-n 15
```

### `calibration` - Calibration Plot

Generate calibration plot (reliability diagram).

```bash
./run.sh calibration --input calibration.json --output calib.pdf
```

### `from-assess` - Generate All Figures

Generate all figures from /assess output in one command.

```bash
./run.sh from-assess --input assess_output.json --output-dir ./figures/
```

Generates:
- `architecture.pdf` - System architecture diagram
- `dependencies.pdf` - Module dependency graph
- `features.pdf` - Feature distribution chart
- `issues.pdf` - Issue severity pie chart
- `comparison.tex` - Feature comparison table
- `test_coverage.tex` - Test coverage table

### `check` - Backend Status

Check which backends are available.

```bash
./run.sh check
```

## Publication Quality Settings

matplotlib figures use IEEE publication settings:
- Font: 8pt Times New Roman (serif)
- DPI: 600 for saving, 300 for display
- Column widths: Single (3.5"), Double (7.16")
- TrueType fonts for Illustrator compatibility

## Integration with paper-writer

```python
from pathlib import Path
import subprocess

def generate_figures(assess_json: Path, output_dir: Path):
    subprocess.run([
        str(FIXTURE_GRAPH_SCRIPT), "from-assess",
        "--input", str(assess_json),
        "--output-dir", str(output_dir),
    ])
```

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
| pandas | Parallel coordinates |
| squarify | Treemaps (matplotlib fallback) |
| scipy | Bode/Nyquist fallback, contours |
| control | Bode, Nyquist, root locus |
| sklearn | t-SNE for embedding scatter |
| umap-learn | UMAP for embedding scatter |
| graphviz | Dependency/architecture diagrams |
| pydeps | Python module dependencies |
| pylint | UML via pyreverse |

**System dependencies:**
- graphviz (`apt install graphviz`) - Graphviz rendering
- mermaid-cli (`npm install -g @mermaid-js/mermaid-cli`) - Mermaid backend
- lean4-prove skill - Formal theorem verification

## Installation

```bash
# Core
pip install typer numpy matplotlib

# Full installation (all features)
pip install typer numpy matplotlib seaborn plotly networkx pandas squarify scipy control pydeps pylint

# Control systems only
pip install typer numpy matplotlib scipy control

# System dependencies
apt install graphviz  # Debian/Ubuntu
npm install -g @mermaid-js/mermaid-cli
```

## Sanity Check

```bash
./sanity.sh
```

Verifies:
- Python dependencies available
- CLI loads correctly
- Basic diagram generation works
- Tests pass

## Research Sources

This skill's design is informed by:
- [pydeps](https://github.com/thebjorn/pydeps) - Python module dependency visualization
- [matplotlib for papers](https://github.com/jbmouret/matplotlib_for_papers) - Publication-quality figures
- [Mermaid vs Graphviz](https://www.unidiagram.com/blog/mermaid-vs-graphviz-comparison) - Diagram-as-code comparison
- [NetworkX + D3](https://github.com/simonlindgren/nXd3) - Interactive graph visualization
- [OverViz](https://www.overviz.com/) - AI architecture diagram generation
