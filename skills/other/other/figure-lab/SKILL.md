---
name: figure-lab
description: >
  Iterative visualization development lab for /create-figure.
  Compose novel D3 visualizations from primitives (marks, scales, encodings),
  test rendering, evaluate against user intent, and promote successful
  compositions to /create-figure as first-class commands.
  Self-improving: tracks render success, visual fidelity, and user satisfaction.
allowed-tools: Bash, Read, Write
triggers:
  - figure lab
  - viz lab
  - visualization lab
  - create new chart type
  - develop visualization
  - prototype chart
  - test visualization
  - new d3 chart
  - promote visualization
  - figure experiments
  - iterate on chart
  - refine visualization
  - why does this chart look wrong
  - fix chart rendering
metadata:
  short-description: "Iterative D3 visualization composition, testing, and promotion"

provides:
  - figure-lab
composes:
  - create-figure
  - memory
  - d3_catalog
  - task-monitor
taxonomy:
  - creation
  - iteration
  - self-improvement
---

# figure-lab

Iterative visualization development lab. Composes novel D3 visualizations from
marks, scales, and encodings — tests rendering — evaluates against user intent —
promotes successful results to /create-figure as first-class commands.

## Key Difference from Other Labs

Unlike /table-lab (parameter tuning) or /prompt-lab (prompt iteration), /figure-lab
**composes new visualization types** from D3 primitives. The NOT_YET types in
d3_catalog.py are the backlog — figure-lab develops and tests them until they work,
then promotes them to implemented status.

## Self-Improvement Loop

```
User request ("show me a ridgeline plot of scores by domain")
  |
  v
1. COMPOSE — Generate D3/Plotly/matplotlib code from primitives
  |         (marks: area, line, rect; scales: linear, band, time;
  |          encodings: x, y, color, opacity)
  |
  v
2. RENDER — Execute in isolated sandbox, capture output
  |         Did it produce valid SVG/HTML without errors?
  |         Is the output non-empty and reasonable dimensions?
  |
  v
3. EVALUATE — Score the result:
  |   a) Render success (0/1) — did D3 throw?
  |   b) Visual fidelity — does it have axes, labels, data marks?
  |   c) Intent match — does it answer what the user asked?
  |   d) Distance-aware — are fonts 18px+, strokes 2px+?
  |
  v
4. ITERATE — If score < threshold:
  |   - Diagnose: missing scale? wrong mark type? data shape mismatch?
  |   - Adjust: swap marks, fix encodings, add missing axes
  |   - Re-render (max 3 iterations)
  |
  v
5. PROMOTE — If score >= 0.85 after iteration:
     - Save to gallery/ as reusable preset
     - Update d3_catalog.py: NOT_YET -> D3_INLINE (or appropriate backend)
     - Generate /create-figure CLI command registration
     - Learn to /memory for future recall
```

## Agent Workflow

### 1. Memory Recall (MANDATORY FIRST STEP)

```bash
/memory recall "visualization composition for <type>"
```

If memory has a prior successful composition, start from that baseline.

### 2. Compose a New Visualization

```bash
# From a user description
./run.sh compose "ridgeline plot of scores by domain" --data sample.json

# From a d3_catalog type name
./run.sh compose --type ridgeline --data sample.json

# Interactive iteration
./run.sh compose --type streamgraph --data sample.json --iterate --max-rounds 3
```

### 3. Evaluate a Composition

```bash
# Score an existing composition
./run.sh evaluate gallery/ridgeline_v1.html --intent "show distribution overlap"

# Batch evaluate all gallery items
./run.sh evaluate-all --gallery ./gallery/
```

### 4. Promote to /create-figure

```bash
# Promote a tested composition to a /create-figure command
./run.sh promote gallery/ridgeline_v1.html --name ridgeline --family distribution

# Dry-run to see what would change
./run.sh promote gallery/ridgeline_v1.html --name ridgeline --dry-run
```

### 5. Gallery Management

```bash
# List all compositions in the gallery
./run.sh gallery

# Show details of a composition
./run.sh gallery show ridgeline_v1

# Delete a failed experiment
./run.sh gallery delete ridgeline_v0
```

## Commands

| Command | Description |
|---------|-------------|
| `compose` | Generate a new D3 visualization from description or type name |
| `evaluate` | Score a composition (render success, visual fidelity, intent match) |
| `evaluate-all` | Batch evaluate gallery |
| `iterate` | Run the self-improvement loop on a composition |
| `promote` | Move successful composition to /create-figure |
| `gallery` | List/show/delete gallery items |
| `catalog-status` | Show d3_catalog coverage (implemented vs NOT_YET) |
| `backlog` | List NOT_YET types ranked by user demand |

## Composition Primitives

### D3 Marks
- `rect` (bars, heatmap cells, treemap tiles)
- `circle` (scatter, bubble, beeswarm)
- `line` (line charts, sparklines, slopes)
- `area` (area charts, streamgraphs, ridgelines)
- `arc` (pie, donut, sunburst, radial bar)
- `path` (Sankey links, chord ribbons, contours)
- `text` (annotations, labels, word clouds)

### D3 Scales
- `scaleLinear`, `scaleLog`, `scaleSqrt`, `scalePow`
- `scaleBand`, `scalePoint`, `scaleOrdinal`
- `scaleTime`, `scaleUtc`
- `scaleSequential`, `scaleDiverging`

### Encodings
- `x`, `y` — position
- `color`, `opacity` — visual
- `size`, `strokeWidth` — magnitude
- `shape`, `angle` — categorical

## Evaluation Rubric

| Dimension | Weight | 0.0 | 0.5 | 1.0 |
|-----------|--------|-----|-----|-----|
| Render success | 0.30 | JS error or empty | Partial render | Clean SVG/HTML |
| Data marks present | 0.25 | No marks | Some marks, wrong count | All data points rendered |
| Axes & labels | 0.15 | Missing | Present but wrong | Correct and readable |
| Intent match | 0.20 | Wrong chart type | Right type, poor mapping | Clearly answers the question |
| Distance-aware | 0.10 | <14px text | Mixed sizes | All text 18px+, strokes 2px+ |

**Threshold**: >= 0.85 to promote. < 0.50 triggers re-composition from scratch.

## Preset Format (gallery/*.json)

```json
{
  "name": "ridgeline",
  "version": 1,
  "family": "distribution",
  "description": "Overlapping density plots showing distribution differences across groups",
  "data_shapes": ["distribution", "categorical"],
  "min_data_points": 20,
  "max_data_points": 10000,
  "min_dimensions": 2,
  "max_dimensions": 3,
  "keywords": ["ridgeline", "joy plot", "density", "distribution", "overlap"],
  "backend": "d3_inline",
  "d3_modules": ["d3-shape", "d3-scale", "d3-axis"],
  "canvas_compatible": true,
  "composition": {
    "marks": ["area"],
    "scales": {"x": "scaleLinear", "y": "scaleBand", "color": "scaleSequential"},
    "encodings": {"x": "value", "y": "group", "opacity": 0.7}
  },
  "template_html": "<!-- self-contained D3 code -->",
  "test_data": [{"group": "A", "value": 42}, {"group": "B", "value": 37}],
  "scores": {
    "render_success": 1.0,
    "data_marks": 1.0,
    "axes_labels": 0.9,
    "intent_match": 0.95,
    "distance_aware": 1.0,
    "overall": 0.97
  },
  "promoted": true,
  "promoted_at": "2026-02-25T12:00:00Z",
  "iterations": 2,
  "created_at": "2026-02-25T11:30:00Z"
}
```

## Gallery Structure

```
gallery/
├── ridgeline_v1.json       # Metadata + scores
├── ridgeline_v1.html       # Self-contained D3 output
├── streamgraph_v1.json
├── streamgraph_v1.html
├── beeswarm_v2.json        # v2 = iterated improvement
├── beeswarm_v2.html
└── _failed/                # Failed experiments (for learning)
    ├── ridgeline_v0.json
    └── ridgeline_v0.html
```

## Dependencies

- Python 3.10+
- typer, rich
- Node.js (for D3 SSR via jsdom — optional, falls back to browser)
- d3_catalog.py (from /create-figure)

## Integration

- **/create-figure**: Promoted presets become CLI commands
- **/memory**: Successful compositions stored for future recall
- **d3_catalog.py**: NOT_YET types graduate to implemented
- **AnswerCanvas**: Gallery items can be served directly to the 5ft canvas
- **Shadow-LEGO**: Failed compositions become negative training data
