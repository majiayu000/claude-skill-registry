---
name: drawio
description: Generate draw.io diagrams programmatically using Python. Creates flowcharts, architecture diagrams, tree structures, network diagrams, and more. Use when the user requests a .drawio file, diagram, flowchart, or visual documentation.
license: MIT
metadata:
  author: example
  version: "1.1"
  dependency-management: uv (PEP 723 inline script metadata)
---

# Draw.io Diagram Generation

## Overview

This skill generates `.drawio` files using the **drawpyo** Python library. Draw.io diagrams are XML-based and can be opened in:
- draw.io desktop app
- diagrams.net (web)
- VS Code draw.io extension

## Quick Start

All scripts include inline dependency metadata (PEP 723). Use `uv run` to execute them — dependencies are handled automatically in an isolated environment:

```bash
# No installation needed — uv handles dependencies automatically
uv run scripts/create_flowchart.py steps.json /mnt/user-data/outputs/flow.drawio
```

For custom code, you can also use `uv run` with inline dependencies:

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["drawpyo>=0.2.0"]
# ///
import drawpyo

# Create a file and page
file = drawpyo.File()
file.file_path = "/home/claude"
file.file_name = "diagram.drawio"
page = drawpyo.Page(file=file)

# Add a shape
box = drawpyo.diagram.Object(page=page, value="Hello World")
box.position = (100, 100)

# Save
file.write()
```

Then run with: `uv run my_script.py`

## Decision Tree

```
What type of diagram?
├── Tree/Hierarchy (org chart, decision tree, file structure)
│   └── Use TreeDiagram class (auto-layout) — see references/REFERENCE.md
│
├── Flowchart (sequential steps with decisions)
│   └── Use helper script: scripts/create_flowchart.py
│   └── Or write custom code with Object + Edge classes
│
├── Architecture/Network (boxes with connections)
│   └── Write custom code using Object + Edge classes
│   └── See references/REFERENCE.md
│
├── From structured data (CSV, JSON, dict)
│   └── Use helper script: scripts/from_data.py
│
└── Complex/Custom
    └── Write custom drawpyo code — see references/REFERENCE.md
```

## Key Concepts

### Objects (Shapes)
```python
# Basic rectangle
obj = drawpyo.diagram.Object(page=page, value="Label")
obj.position = (x, y)        # Coordinates in pixels
obj.width = 120              # Default: 120
obj.height = 60              # Default: 60

# From draw.io shape library
obj = drawpyo.diagram.object_from_library(
    page=page,
    library="general",       # or "flowchart", "basic", etc.
    obj_name="process",      # shape name from library
    value="Process Step"
)
```

### Edges (Connections)
```python
edge = drawpyo.diagram.Edge(
    page=page,
    source=obj1,
    target=obj2,
    label="connects to"
)
```

### Styling
```python
# Apply a style string (same format as draw.io)
obj.apply_style_string(
    "rounded=1;whiteSpace=wrap;html=1;"
    "fillColor=#dae8fc;strokeColor=#6c8ebf;"
)
```

## Helper Scripts

Run with `uv run` — dependencies are handled automatically:

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/create_flowchart.py` | Create flowcharts from step definitions | `uv run scripts/create_flowchart.py input.json output.drawio` |
| `scripts/create_tree.py` | Create tree diagrams with auto-layout | `uv run scripts/create_tree.py input.json output.drawio` |
| `scripts/from_data.py` | Create diagrams from JSON/dict data | `uv run scripts/from_data.py input.json output.drawio` |

## Common Shape Libraries

Use with `object_from_library(library=..., obj_name=...)`:

- **general**: `rectangle`, `ellipse`, `process`, `diamond`, `parallelogram`, `hexagon`, `triangle`, `cylinder`, `cloud`, `document`, `note`, `actor`
- **flowchart**: `terminator`, `process`, `decision`, `data`, `document`, `predefined_process`, `stored_data`, `internal_storage`, `manual_input`, `manual_operation`
- **basic**: `rectangle`, `ellipse`, `rhombus`, `triangle`, `pentagon`, `hexagon`, `octagon`

## Output

Always save generated `.drawio` files to `/mnt/user-data/outputs/` and use the `present_files` tool to share with the user.

## Next Steps

- **references/REFERENCE.md**: Complete API documentation, styling options, all shape libraries
- **references/examples.md**: Example code for common diagram types
- **scripts/**: Ready-to-use helper scripts
