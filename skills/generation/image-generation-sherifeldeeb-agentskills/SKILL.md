---
name: image-generation
description: |
  Create diagrams, charts, and visual assets for security documentation.
  Generate network diagrams, architecture visuals, and data visualizations.
  Use when creating visual content for reports or presentations.
license: Apache-2.0
compatibility: |
  - Python 3.9+
  - Required packages: pillow, matplotlib, graphviz
metadata:
  author: SherifEldeeb
  version: "1.0.0"
  category: baseline
---

# Image Generation Skill

Create diagrams, charts, and visual assets for security documentation with support for network diagrams, data visualizations, and flowcharts.

## Capabilities

- **Diagrams**: Generate network topology and architecture diagrams
- **Charts**: Create data visualizations (bar, pie, line, heatmaps)
- **Flowcharts**: Build process and workflow diagrams
- **Risk Matrices**: Generate risk assessment visualizations
- **Timelines**: Create incident and event timelines
- **Export**: Save to PNG, SVG, and PDF formats

## Quick Start

```python
import matplotlib.pyplot as plt

# Create a simple bar chart
severities = ['Critical', 'High', 'Medium', 'Low']
counts = [3, 8, 15, 22]

plt.figure(figsize=(10, 6))
plt.bar(severities, counts, color=['#e74c3c', '#e67e22', '#f1c40f', '#3498db'])
plt.title('Findings by Severity')
plt.savefig('severity_chart.png', dpi=150)
```

## Usage

### Bar Charts

Create bar charts for comparisons.

**Example**:
```python
import matplotlib.pyplot as plt
from typing import Dict

def create_severity_chart(data: Dict[str, int], output_path: str = 'chart.png'):
    """Create a severity distribution bar chart."""
    colors = {
        'Critical': '#e74c3c', 'High': '#e67e22',
        'Medium': '#f1c40f', 'Low': '#3498db'
    }

    severities = list(data.keys())
    counts = list(data.values())
    bar_colors = [colors.get(s, '#333') for s in severities]

    plt.figure(figsize=(10, 6))
    plt.bar(severities, counts, color=bar_colors)
    plt.title('Findings by Severity', fontsize=14, fontweight='bold')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

# Usage
create_severity_chart({'Critical': 3, 'High': 8, 'Medium': 15, 'Low': 22})
```

### Network Diagrams

Create network topology diagrams using Graphviz.

**Example**:
```python
from graphviz import Digraph

def create_network_diagram(nodes: list, edges: list, output_path: str = 'network'):
    """Create a network topology diagram."""
    dot = Digraph()
    dot.attr(rankdir='TB')

    shapes = {'firewall': 'box3d', 'server': 'box', 'database': 'cylinder'}

    for node in nodes:
        dot.node(node['id'], node['label'],
                shape=shapes.get(node.get('type', 'server'), 'box'),
                style='filled', fillcolor=node.get('color', 'lightblue'))

    for edge in edges:
        dot.edge(edge['from'], edge['to'], label=edge.get('label', ''))

    dot.render(output_path, format='png', cleanup=True)

# Usage
nodes = [
    {'id': 'fw', 'label': 'Firewall', 'type': 'firewall', 'color': 'lightcoral'},
    {'id': 'web', 'label': 'Web Server', 'type': 'server'},
    {'id': 'db', 'label': 'Database', 'type': 'database'}
]
edges = [{'from': 'fw', 'to': 'web'}, {'from': 'web', 'to': 'db'}]
create_network_diagram(nodes, edges)
```

### Flowcharts

Create process flowcharts.

**Example**:
```python
from graphviz import Digraph

def create_flowchart(steps: list, output_path: str = 'flowchart'):
    """Create a process flowchart."""
    dot = Digraph()
    dot.attr(rankdir='TB')

    shapes = {'start': 'ellipse', 'end': 'ellipse',
              'process': 'box', 'decision': 'diamond'}
    colors = {'start': 'lightgreen', 'end': 'lightcoral',
              'process': 'lightblue', 'decision': 'lightyellow'}

    for step in steps:
        dot.node(step['id'], step['label'],
                shape=shapes.get(step.get('type', 'process'), 'box'),
                style='filled',
                fillcolor=colors.get(step.get('type', 'process'), 'white'))

        if 'next' in step:
            for n in (step['next'] if isinstance(step['next'], list) else [step['next']]):
                if isinstance(n, dict):
                    dot.edge(step['id'], n['to'], label=n.get('label', ''))
                else:
                    dot.edge(step['id'], n)

    dot.render(output_path, format='png', cleanup=True)
```

### Risk Heatmaps

Create risk assessment heatmaps.

**Example**:
```python
import matplotlib.pyplot as plt
import numpy as np

def create_risk_heatmap(data: list, x_labels: list, y_labels: list, output_path: str):
    """Create a risk assessment heatmap."""
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(data, cmap='RdYlGn_r')

    ax.set_xticks(np.arange(len(x_labels)))
    ax.set_yticks(np.arange(len(y_labels)))
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)

    for i in range(len(y_labels)):
        for j in range(len(x_labels)):
            ax.text(j, i, data[i][j], ha='center', va='center',
                   color='white' if data[i][j] > 5 else 'black')

    ax.set_title('Risk Matrix')
    plt.colorbar(im)
    plt.savefig(output_path, dpi=150)
    plt.close()
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `IMAGE_OUTPUT_DIR` | Output directory | No | `./output` |
| `IMAGE_DPI` | Default DPI | No | `150` |

## Limitations

- **Interactive**: Static images only
- **3D**: Limited 3D support
- **Graphviz**: Required for diagrams

## Troubleshooting

### Graphviz Not Found

Install the system package:
```bash
apt-get install graphviz  # Ubuntu
brew install graphviz      # macOS
```

## Related Skills

- [pptx](../pptx/): Embed images in presentations
- [docx](../docx/): Include visuals in reports
- [pdf](../pdf/): Add charts to PDF reports

## References

- [Detailed API Reference](references/REFERENCE.md)
- [Matplotlib Documentation](https://matplotlib.org/)
- [Graphviz Documentation](https://graphviz.org/)
