---
name: patent-diagrams
description: Generate patent-style technical diagrams (flowcharts, block diagrams, system architectures) with automatic reference numbering.
---

# Patent Diagrams Skill

Generate professional patent-style technical diagrams using Graphviz.

**Capabilities:**
- Flowcharts (method steps, decision flows)
- Block diagrams (system architectures, data flows)
- Custom diagrams (arbitrary DOT code)
- Reference numbering (patent-style annotations)
- Templates (pre-built patterns)

Output: SVG (Scalable Vector Graphics) for USPTO submissions

## Core Operations

### 1. `create_flowchart`

**Inputs:**
- `steps` (List[str], required): Ordered list of step descriptions

**Outputs:**
```python
{
    "success": bool,
    "svg_path": str,         # Absolute path to SVG
    "filename": str,
    "message": str
}
```

**Example:**
```python
steps = [
    "Receive input data from sensor",
    "Validate data format",
    "Process data using algorithm",
    "Generate output signal",
    "Transmit result to display"
]
result = create_flowchart(steps)
```

### 2. `create_block_diagram`

**Inputs:**
- `blocks` (List[dict], required): Component definitions
  - `id` (str, required): Unique identifier
  - `label` (str, required): Display text (use `\n` for multiline)
  - `type` (str, optional): Block type (`"input"`, `"output"`, `"process"`, `"storage"`, `"decision"`, `"default"`)
- `connections` (List[dict], required): Connection definitions
  - `from_id` (str, required): Source block ID
  - `to_id` (str, required): Target block ID
  - `label` (str, optional): Connection label

**Example:**
```python
blocks = [
    {"id": "sensor", "label": "Input\nSensor", "type": "input"},
    {"id": "cpu", "label": "Processing\nUnit", "type": "process"},
    {"id": "memory", "label": "Memory\nStorage", "type": "storage"},
    {"id": "display", "label": "Output\nDisplay", "type": "output"}
]

connections = [
    {"from_id": "sensor", "to_id": "cpu", "label": "raw data"},
    {"from_id": "cpu", "to_id": "memory", "label": "store"},
    {"from_id": "memory", "to_id": "cpu", "label": "retrieve"},
    {"from_id": "cpu", "to_id": "display", "label": "results"}
]

result = create_block_diagram(blocks, connections)
```

### 3. `render_diagram`

Render arbitrary Graphviz DOT code.

**Inputs:**
- `dot` (str, required): Graphviz DOT code

**Example:**
```python
dot_code = """
digraph CustomDiagram {
    rankdir=TB;
    node [shape=box, style=filled, fillcolor=lightblue];

    A [label="Component A"];
    B [label="Component B"];
    C [label="Component C"];

    A -> B [label="signal"];
    B -> C [label="processed"];
    C -> A [label="feedback"];
}
"""

result = render_diagram(dot_code)
```

### 4. `add_diagram_references`

Add patent-style reference numbers to existing SVG.

**Inputs:**
- `svg_path` (str, required): Path to input SVG
- `reference_map` (dict, required): Element text -> reference number
  - Key: Text to match (case-insensitive substring)
  - Value: Reference number (integer)

**Outputs:**
```python
{
    "success": bool,
    "svg_path": str,         # NEW annotated SVG path
    "original_path": str,    # Original SVG preserved
    "filename": str,         # Ends with "_annotated.svg"
    "references_added": int,
    "message": str
}
```

**Example:**
```python
reference_map = {
    "Input Sensor": 10,
    "Processing Unit": 20,
    "Memory Storage": 30,
    "Output Display": 40
}

result = add_diagram_references(
    svg_path="C:/path/to/block_diagram.svg",
    reference_map=reference_map
)
# Creates: "block_diagram_annotated.svg"
```

### 5. `get_diagram_templates`

Retrieve pre-built templates.

**Outputs:**
```python
{
    "success": bool,
    "templates": {
        "template_name": {
            "name": str,
            "description": str,
            "dot_code": str
        }
    },
    "template_names": List[str]
}
```

**Available Templates:**
- `simple_flowchart`: Basic method flow
- `system_block`: System architecture
- `method_steps`: Patent method claims (101, 102, ...)
- `component_hierarchy`: Hierarchical tree

**Example:**
```python
result = get_diagram_templates()
template = result["templates"]["system_block"]
diagram = render_diagram(template["dot_code"])
```

## Graphviz Dependency

**Required:** Graphviz as Python package AND system executable.

**Check Installation:**
```python
check_graphviz_installed()
# Returns: {"ready": bool, "python_package": bool, "system_command": bool, "version": str, "message": str}
```

**Install if Missing:**
1. Python package: `pip install graphviz`
2. System executable:
   - Windows: `winget install graphviz`
   - macOS: `brew install graphviz`
   - Linux: `sudo apt install graphviz`

## Output Management

**Output Directory:** `PROJECT_ROOT/diagrams/` (auto-created)

**Filename Generation:**
- Flowcharts: `flowchart_YYYYMMDD_HHMMSS.svg`
- Block diagrams: `block_diagram_YYYYMMDD_HHMMSS.svg`
- Custom renders: `diagram_YYYYMMDD_HHMMSS.svg`
- Annotated: `{original_name}_annotated.svg`

**Format:** All paths are absolute (e.g., `C:/Users/<YOUR_USER>/Desktop/TEST1/diagrams/flowchart.svg`)

## Block Types and Styling

| Type | Shape | Color | Typical Use |
|------|-------|-------|-------------|
| `input` | invhouse | lightblue | Input devices, sensors |
| `output` | house | lightgreen | Output devices, displays |
| `process` | box | lightyellow | Processing units, algorithms |
| `storage` | cylinder | lightgray | Memory, databases |
| `decision` | diamond | lightcoral | Decision points, logic |
| `default` | box | white | Generic components |

## Common Use Cases

1. **Method Claims**: Use `simple_flowchart` or `method_steps` template
2. **System Architecture**: Use `system_block` template or custom `create_block_diagram`
3. **Component Relationships**: Use `component_hierarchy` template
4. **Custom Layouts**: Use `render_diagram` with full DOT control
5. **Final Publication**: Use `add_diagram_references` for patent-style numbering
