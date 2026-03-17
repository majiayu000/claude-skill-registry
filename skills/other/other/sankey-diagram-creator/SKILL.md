---
name: sankey-diagram-creator
description: Create interactive Sankey diagrams for flow visualization from CSV, DataFrame, or dict data. Supports node/link styling and HTML/PNG/SVG export.
---

# Sankey Diagram Creator

Create interactive Sankey diagrams to visualize flows, transfers, and relationships between categories. Perfect for budget flows, energy transfers, user journeys, and data pipelines.

## Quick Start

```python
from scripts.sankey_creator import SankeyCreator

# From dictionary
sankey = SankeyCreator()
sankey.from_dict({
    'source': ['A', 'A', 'B', 'B'],
    'target': ['C', 'D', 'C', 'D'],
    'value': [10, 20, 15, 25]
})
sankey.generate().save_html("flow.html")

# From CSV
sankey = SankeyCreator()
sankey.from_csv("flows.csv", source="from", target="to", value="amount")
sankey.title("Budget Flow").generate().save_html("budget.html")
```

## Features

- **Multiple Input Sources**: Dict, DataFrame, or CSV files
- **Interactive Output**: Hover tooltips with flow details
- **Node Customization**: Colors, labels, positions
- **Link Styling**: Colors, opacity, labels
- **Export Formats**: HTML (interactive), PNG, SVG
- **Auto-Coloring**: Automatic color assignment or custom schemes

## API Reference

### Initialization

```python
sankey = SankeyCreator()
```

### Data Input Methods

```python
# From dictionary
sankey.from_dict({
    'source': ['A', 'A', 'B'],
    'target': ['X', 'Y', 'X'],
    'value': [10, 20, 15]
})

# From CSV file
sankey.from_csv(
    filepath="data.csv",
    source="source_col",
    target="target_col",
    value="value_col",
    label=None  # Optional: column for link labels
)

# From pandas DataFrame
import pandas as pd
df = pd.DataFrame({
    'from': ['A', 'B'],
    'to': ['C', 'C'],
    'amount': [100, 200]
})
sankey.from_dataframe(df, source="from", target="to", value="amount")

# Add individual flows
sankey.add_flow("Source", "Target", 50)
sankey.add_flow("Source", "Other", 30, label="30 units")
```

### Styling Methods

All methods return `self` for chaining.

```python
# Node colors
sankey.node_colors({
    'Income': '#2ecc71',
    'Expenses': '#e74c3c',
    'Savings': '#3498db'
})

# Use colormap for automatic colors
sankey.node_colors(colormap='Pastel1')

# Link colors (by source, target, or custom)
sankey.link_colors(by='source')  # Color by source node
sankey.link_colors(by='target')  # Color by target node
sankey.link_colors(opacity=0.6)  # Set link opacity

# Custom link colors
sankey.link_colors(colors={
    ('Income', 'Expenses'): '#ff6b6b',
    ('Income', 'Savings'): '#4ecdc4'
})

# Title
sankey.title("My Flow Diagram")
sankey.title("Budget Overview", font_size=20)

# Layout
sankey.layout(orientation='h')  # Horizontal (default)
sankey.layout(orientation='v')  # Vertical
sankey.layout(pad=20)  # Node padding
```

### Generation and Export

```python
# Generate the diagram
sankey.generate()

# Save as interactive HTML
sankey.save_html("diagram.html")
sankey.save_html("diagram.html", auto_open=True)  # Open in browser

# Save as static image
sankey.save_image("diagram.png")
sankey.save_image("diagram.svg", format='svg')
sankey.save_image("diagram.png", width=1200, height=800)

# Get Plotly figure object for customization
fig = sankey.get_figure()
fig.update_layout(...)

# Show in notebook/browser
sankey.show()
```

## Data Format

### CSV Format

```csv
source,target,value,label
Income,Housing,1500,Rent
Income,Food,600,Groceries
Income,Transport,400,Car
Income,Savings,500,Emergency Fund
Savings,Investments,300,Stocks
```

### Dictionary Format

```python
data = {
    'source': ['Income', 'Income', 'Income', 'Expenses'],
    'target': ['Rent', 'Food', 'Savings', 'Tax'],
    'value': [1500, 600, 500, 400],
    'label': ['Housing', 'Groceries', 'Emergency', 'Federal']  # Optional
}
```

### DataFrame Format

```python
import pandas as pd
df = pd.DataFrame({
    'from_node': ['A', 'A', 'B', 'C'],
    'to_node': ['B', 'C', 'D', 'D'],
    'flow_value': [100, 200, 150, 180]
})
```

## Color Schemes

### Available Colormaps

| Name | Description |
|------|-------------|
| `Pastel1` | Soft pastel colors |
| `Pastel2` | Muted pastels |
| `Set1` | Bold distinct colors |
| `Set2` | Muted distinct colors |
| `Set3` | Light distinct colors |
| `Paired` | Paired color scheme |
| `viridis` | Blue-green-yellow |
| `plasma` | Purple-orange-yellow |

### Custom Colors

```python
# Hex colors
sankey.node_colors({
    'Category A': '#1abc9c',
    'Category B': '#3498db',
    'Category C': '#9b59b6'
})

# Named colors
sankey.node_colors({
    'Revenue': 'green',
    'Costs': 'red',
    'Profit': 'blue'
})
```

## CLI Usage

```bash
# Basic usage
python sankey_creator.py --input flows.csv \
    --source from --target to --value amount \
    --output flow.html

# With title and colors
python sankey_creator.py --input budget.csv \
    --source category --target subcategory --value amount \
    --title "Budget Breakdown" \
    --colormap Pastel1 \
    --output budget.html

# PNG output
python sankey_creator.py --input data.csv \
    --source src --target dst --value val \
    --output diagram.png \
    --width 1200 --height 800
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input` | Input CSV file | Required |
| `--source` | Source column name | Required |
| `--target` | Target column name | Required |
| `--value` | Value column name | Required |
| `--output` | Output file path | `sankey.html` |
| `--title` | Diagram title | None |
| `--colormap` | Color scheme | `Pastel1` |
| `--link-opacity` | Link opacity (0-1) | 0.5 |
| `--orientation` | 'h' or 'v' | `h` |
| `--width` | Image width (PNG/SVG) | 1000 |
| `--height` | Image height (PNG/SVG) | 600 |

## Examples

### Budget Flow

```python
sankey = SankeyCreator()
sankey.from_dict({
    'source': ['Salary', 'Salary', 'Salary', 'Salary', 'Savings', 'Investments'],
    'target': ['Housing', 'Food', 'Transport', 'Savings', 'Investments', 'Stocks'],
    'value': [2000, 800, 500, 1000, 700, 700]
})
sankey.title("Monthly Budget Flow")
sankey.node_colors({
    'Salary': '#27ae60',
    'Housing': '#e74c3c',
    'Food': '#f39c12',
    'Transport': '#3498db',
    'Savings': '#9b59b6',
    'Investments': '#1abc9c',
    'Stocks': '#34495e'
})
sankey.generate().save_html("budget_flow.html")
```

### Energy Flow

```python
sankey = SankeyCreator()
sankey.add_flow("Coal", "Electricity", 100)
sankey.add_flow("Gas", "Electricity", 80)
sankey.add_flow("Solar", "Electricity", 30)
sankey.add_flow("Electricity", "Industry", 120)
sankey.add_flow("Electricity", "Residential", 60)
sankey.add_flow("Electricity", "Commercial", 30)

sankey.title("Energy Flow")
sankey.node_colors(colormap='Set2')
sankey.link_colors(by='source', opacity=0.4)
sankey.generate().save_html("energy.html")
```

### User Journey

```python
sankey = SankeyCreator()
sankey.from_dict({
    'source': ['Landing', 'Landing', 'Product', 'Product', 'Cart', 'Cart'],
    'target': ['Product', 'Exit', 'Cart', 'Exit', 'Checkout', 'Exit'],
    'value': [1000, 200, 600, 200, 400, 100]
})
sankey.title("User Journey")
sankey.node_colors({
    'Landing': '#3498db',
    'Product': '#2ecc71',
    'Cart': '#f1c40f',
    'Checkout': '#27ae60',
    'Exit': '#e74c3c'
})
sankey.generate().save_html("journey.html")
```

### Multi-Level Flow

```python
# Three-level hierarchy
data = {
    'source': [
        # Level 1 -> Level 2
        'Revenue', 'Revenue', 'Revenue',
        # Level 2 -> Level 3
        'Products', 'Products', 'Services', 'Services'
    ],
    'target': [
        'Products', 'Services', 'Other',
        'Electronics', 'Software', 'Consulting', 'Support'
    ],
    'value': [500, 300, 50, 300, 200, 200, 100]
}

sankey = SankeyCreator()
sankey.from_dict(data)
sankey.title("Revenue Breakdown")
sankey.generate().save_html("revenue.html")
```

## Dependencies

```
plotly>=5.15.0
pandas>=2.0.0
kaleido>=0.2.0
```

## Limitations

- Static image export (PNG/SVG) requires `kaleido` package
- Very complex diagrams with many nodes may be hard to read
- Node positions are auto-calculated (limited manual control)
- Link colors can only be uniform or by source/target
