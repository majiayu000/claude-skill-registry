---
name: org-chart-generator
description: Generate organizational hierarchy charts from CSV, JSON, or nested data. Supports multiple layouts, department coloring, and PNG/SVG/PDF export.
---

# Org Chart Generator

Create professional organizational hierarchy charts from structured data. Perfect for company org charts, team structures, reporting relationships, and any hierarchical data visualization.

## Quick Start

```python
from scripts.orgchart_gen import OrgChartGenerator

# From CSV (employee name + manager)
org = OrgChartGenerator()
org.from_csv("employees.csv", name="name", manager="reports_to")
org.generate().save("org_chart.png")

# From nested dictionary
org = OrgChartGenerator()
org.from_dict({
    'name': 'CEO',
    'children': [
        {'name': 'CTO', 'children': [{'name': 'Dev Lead'}, {'name': 'QA Lead'}]},
        {'name': 'CFO', 'children': [{'name': 'Controller'}]}
    ]
})
org.layout("top-down").generate().save("hierarchy.png")
```

## Features

- **Multiple Input Sources**: CSV, JSON, nested dict, or programmatic
- **Layout Options**: Top-down, left-right, bottom-up, right-left
- **Node Styling**: Colors by level, department, or custom
- **Additional Data**: Titles, departments, photos
- **Edge Styles**: Straight, orthogonal, curved
- **Export Formats**: PNG, SVG, PDF, DOT

## API Reference

### Initialization

```python
org = OrgChartGenerator()
```

### Data Input Methods

```python
# From CSV with name and manager columns
org.from_csv(
    filepath="employees.csv",
    name="employee_name",
    manager="reports_to",
    title="job_title",        # Optional
    department="dept",        # Optional
)

# From JSON file (nested structure)
org.from_json("structure.json")

# From nested dictionary
org.from_dict({
    'name': 'Root',
    'title': 'CEO',
    'department': 'Executive',
    'children': [
        {'name': 'Child 1', 'children': [...]},
        {'name': 'Child 2'}
    ]
})

# Programmatic: add nodes and relationships
org.add_node("Alice", title="CEO", department="Executive")
org.add_node("Bob", title="CTO", department="Engineering")
org.add_node("Carol", title="CFO", department="Finance")
org.add_relationship("Bob", "Alice")  # Bob reports to Alice
org.add_relationship("Carol", "Alice")
```

### Layout Configuration

```python
# Layout direction
org.layout("top-down")    # TB - Default, root at top
org.layout("bottom-up")   # BT - Root at bottom
org.layout("left-right")  # LR - Root on left
org.layout("right-left")  # RL - Root on right

# Spacing
org.spacing(rank=1.0, node=0.5)  # Vertical and horizontal spacing
```

### Node Styling

```python
# Colors by department
org.colors_by_department({
    'Engineering': '#3498db',
    'Finance': '#2ecc71',
    'Marketing': '#e74c3c',
    'Executive': '#9b59b6'
})

# Colors by level (depth in tree)
org.colors_by_level({
    0: '#e74c3c',  # Root (CEO)
    1: '#f39c12',  # Level 1 (C-suite)
    2: '#3498db',  # Level 2 (Directors)
    3: '#2ecc71'   # Level 3+ (Managers/Staff)
})

# Uniform color
org.node_color('#3498db')

# Node shape
org.node_style(
    shape='box',           # box, ellipse, diamond, record
    font='Arial',
    font_size=12,
    border_width=1
)
```

### Edge Styling

```python
# Edge style
org.edge_style(
    style='orthogonal',    # orthogonal, straight, curved
    color='#666666',
    width=1.0
)
```

### Generation and Export

```python
# Generate the chart
org.generate()

# Save to file
org.save("chart.png")       # PNG
org.save("chart.svg")       # SVG
org.save("chart.pdf")       # PDF
org.save("chart.dot")       # DOT source

# Save with custom size
org.save("chart.png", dpi=150)

# Get DOT source code
dot_code = org.to_dot()

# Show (opens in viewer)
org.show()
```

## Data Formats

### CSV Format

**Flat structure with manager references:**

```csv
name,reports_to,title,department
Alice,,"CEO","Executive"
Bob,"Alice","CTO","Engineering"
Carol,"Alice","CFO","Finance"
Dave,"Bob","Dev Lead","Engineering"
Eve,"Bob","QA Lead","Engineering"
Frank,"Carol","Controller","Finance"
```

Note: Empty `reports_to` indicates root node(s).

### JSON Format

**Nested structure:**

```json
{
  "name": "Alice",
  "title": "CEO",
  "department": "Executive",
  "children": [
    {
      "name": "Bob",
      "title": "CTO",
      "department": "Engineering",
      "children": [
        {"name": "Dave", "title": "Dev Lead"},
        {"name": "Eve", "title": "QA Lead"}
      ]
    },
    {
      "name": "Carol",
      "title": "CFO",
      "department": "Finance",
      "children": [
        {"name": "Frank", "title": "Controller"}
      ]
    }
  ]
}
```

### Dictionary Format

**Same nested structure as JSON:**

```python
data = {
    'name': 'Alice',
    'title': 'CEO',
    'children': [
        {'name': 'Bob', 'title': 'CTO'},
        {'name': 'Carol', 'title': 'CFO'}
    ]
}
```

## CLI Usage

```bash
# From CSV
python orgchart_gen.py --input employees.csv \
    --name name --manager reports_to \
    --output org.png

# With title and department
python orgchart_gen.py --input team.csv \
    --name employee --manager boss \
    --title job_title --department dept \
    --layout left-right \
    --output team_chart.png

# From JSON
python orgchart_gen.py --input structure.json --output org.svg

# High resolution
python orgchart_gen.py --input data.csv --name n --manager m \
    --output chart.png --dpi 300
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input` | Input CSV or JSON file | Required |
| `--name` | Name column (CSV) | - |
| `--manager` | Manager column (CSV) | - |
| `--title` | Title column (CSV) | - |
| `--department` | Department column (CSV) | - |
| `--output` | Output file path | `orgchart.png` |
| `--layout` | Layout direction | `top-down` |
| `--dpi` | Image resolution | 96 |

## Examples

### Basic Company Org Chart

```python
org = OrgChartGenerator()
org.from_csv("company.csv", name="employee", manager="manager")
org.layout("top-down")
org.node_style(shape='box')
org.generate().save("company_org.png")
```

### Colored by Department

```python
org = OrgChartGenerator()
org.from_csv("team.csv", name="name", manager="reports_to", department="dept")
org.colors_by_department({
    'Executive': '#8e44ad',
    'Engineering': '#2980b9',
    'Sales': '#27ae60',
    'Marketing': '#e67e22',
    'HR': '#c0392b'
})
org.layout("left-right")
org.generate().save("dept_org.png")
```

### With Titles

```python
org = OrgChartGenerator()
org.from_dict({
    'name': 'Sarah Johnson',
    'title': 'CEO',
    'children': [
        {
            'name': 'Mike Chen',
            'title': 'VP Engineering',
            'children': [
                {'name': 'Lisa Park', 'title': 'Engineering Manager'},
                {'name': 'Tom Brown', 'title': 'Tech Lead'}
            ]
        },
        {
            'name': 'Emma Wilson',
            'title': 'VP Sales',
            'children': [
                {'name': 'John Davis', 'title': 'Sales Manager'}
            ]
        }
    ]
})
org.layout("top-down")
org.generate().save("executive_org.png")
```

### Project Team Structure

```python
org = OrgChartGenerator()

# Add nodes
org.add_node("Project Manager", department="PMO")
org.add_node("Tech Lead", department="Engineering")
org.add_node("Designer", department="Design")
org.add_node("Dev 1", department="Engineering")
org.add_node("Dev 2", department="Engineering")
org.add_node("QA", department="Quality")

# Add relationships
org.add_relationship("Tech Lead", "Project Manager")
org.add_relationship("Designer", "Project Manager")
org.add_relationship("QA", "Project Manager")
org.add_relationship("Dev 1", "Tech Lead")
org.add_relationship("Dev 2", "Tech Lead")

org.colors_by_department({
    'PMO': '#9b59b6',
    'Engineering': '#3498db',
    'Design': '#e74c3c',
    'Quality': '#2ecc71'
})
org.generate().save("project_team.png")
```

### Multiple Root Nodes

```python
# Board of Directors structure
org = OrgChartGenerator()
org.from_dict({
    'name': 'Board of Directors',
    'children': [
        {
            'name': 'CEO',
            'children': [
                {'name': 'COO'},
                {'name': 'CFO'},
                {'name': 'CTO'}
            ]
        },
        {
            'name': 'Audit Committee',
            'children': [
                {'name': 'Internal Audit'},
                {'name': 'External Audit'}
            ]
        }
    ]
})
org.generate().save("board_structure.png")
```

## Node Display Format

By default, nodes display:
- Name (required)
- Title (if provided)

Example node appearance:
```
┌─────────────┐
│  John Smith │
│    CEO      │
└─────────────┘
```

## Dependencies

```
graphviz>=0.20.0
pandas>=2.0.0
```

**System Requirement**: Graphviz must be installed on the system.
- macOS: `brew install graphviz`
- Ubuntu: `apt-get install graphviz`
- Windows: Download from graphviz.org

## Limitations

- Very large org charts (100+ nodes) may be hard to read
- Photo support requires external image files
- Node positions are auto-calculated (limited manual control)
- Complex reporting relationships (matrix orgs) not well supported
