---
name: flowchart-generator
description: Generate flowcharts from YAML/JSON definitions or Python DSL. Supports standard flowchart shapes, swimlanes, and PNG/SVG/PDF export.
---

# Flowchart Generator

Create professional flowcharts from structured process definitions. Supports standard flowchart symbols (start/end, process, decision, I/O), swimlanes for multi-actor processes, and multiple export formats.

## Quick Start

```python
from scripts.flowchart_gen import FlowchartGenerator

# Using Python DSL
flow = FlowchartGenerator()
flow.start("Start")
flow.process("Step 1", id="s1")
flow.decision("Check?", id="d1")
flow.process("Yes Path", id="yes")
flow.process("No Path", id="no")
flow.end("End")

flow.connect("Start", "s1")
flow.connect("s1", "d1")
flow.connect("d1", "yes", label="Yes")
flow.connect("d1", "no", label="No")
flow.connect("yes", "End")
flow.connect("no", "End")

flow.generate().save("flowchart.png")

# From YAML file
flow = FlowchartGenerator()
flow.from_yaml("process.yaml")
flow.generate().save("process.png")
```

## Features

- **Multiple Input Sources**: Python DSL, YAML, or JSON
- **Standard Shapes**: Start/End, Process, Decision, Input/Output, Connector
- **Swimlanes**: Multi-actor/department process diagrams
- **Styling Presets**: Business, technical, minimal themes
- **Layout Options**: Top-bottom, left-right, and more
- **Export Formats**: PNG, SVG, PDF, DOT

## API Reference

### Initialization

```python
flow = FlowchartGenerator()
```

### Node Creation (DSL)

```python
# Start node (oval/ellipse)
flow.start("Start")
flow.start("Begin Process", id="start1")

# End node (oval/ellipse)
flow.end("End")
flow.end("Process Complete", id="end1")

# Process node (rectangle)
flow.process("Process Data")
flow.process("Calculate Total", id="calc")

# Decision node (diamond)
flow.decision("Valid?", id="check")
flow.decision("Amount > 100?", id="d1")

# Input/Output node (parallelogram)
flow.input_output("User Input", id="input1")
flow.input_output("Display Result", id="output1")

# Connector (circle) - for complex flows
flow.connector("A", id="conn_a")
```

### Connections

```python
# Basic connection
flow.connect("start", "process1")

# With label
flow.connect("decision1", "yes_path", label="Yes")
flow.connect("decision1", "no_path", label="No")

# Multiple connections from decision
flow.decision("Approved?", id="d1")
flow.connect("d1", "approve_path", label="Yes")
flow.connect("d1", "reject_path", label="No")
```

### Loading from Files

```python
# From YAML
flow.from_yaml("process.yaml")

# From JSON
flow.from_json("process.json")
```

### Swimlanes

```python
# Define swimlanes
flow.swimlanes([
    "Customer",
    "Sales Team",
    "Fulfillment"
])

# Add nodes to specific lanes
flow.process("Place Order", id="order", lane="Customer")
flow.process("Review Order", id="review", lane="Sales Team")
flow.process("Ship Order", id="ship", lane="Fulfillment")
```

### Styling

```python
# Style presets
flow.style("business")   # Professional blue theme
flow.style("technical")  # Gray technical theme
flow.style("minimal")    # Clean minimal theme
flow.style("colorful")   # Vibrant colors

# Layout direction
flow.layout("TB")  # Top to Bottom (default)
flow.layout("LR")  # Left to Right
flow.layout("BT")  # Bottom to Top
flow.layout("RL")  # Right to Left

# Custom colors
flow.node_colors({
    'start': '#2ecc71',
    'end': '#e74c3c',
    'process': '#3498db',
    'decision': '#f39c12',
    'io': '#9b59b6'
})
```

### Generation and Export

```python
# Generate
flow.generate()

# Save
flow.save("chart.png")
flow.save("chart.svg")
flow.save("chart.pdf")
flow.save("chart.dot")  # GraphViz source

# Get DOT source
dot_source = flow.to_dot()

# Show in viewer
flow.show()
```

## Data Formats

### YAML Format

```yaml
# process.yaml
title: Order Processing
layout: TB
style: business

nodes:
  - id: start
    type: start
    label: Start

  - id: receive
    type: process
    label: Receive Order

  - id: check_stock
    type: decision
    label: In Stock?

  - id: fulfill
    type: process
    label: Fulfill Order

  - id: backorder
    type: process
    label: Create Backorder

  - id: notify
    type: io
    label: Notify Customer

  - id: end
    type: end
    label: End

connections:
  - from: start
    to: receive

  - from: receive
    to: check_stock

  - from: check_stock
    to: fulfill
    label: "Yes"

  - from: check_stock
    to: backorder
    label: "No"

  - from: fulfill
    to: notify

  - from: backorder
    to: notify

  - from: notify
    to: end
```

### JSON Format

```json
{
  "title": "Order Processing",
  "layout": "TB",
  "style": "business",
  "nodes": [
    {"id": "start", "type": "start", "label": "Start"},
    {"id": "process1", "type": "process", "label": "Process Data"},
    {"id": "decision1", "type": "decision", "label": "Valid?"},
    {"id": "end", "type": "end", "label": "End"}
  ],
  "connections": [
    {"from": "start", "to": "process1"},
    {"from": "process1", "to": "decision1"},
    {"from": "decision1", "to": "end", "label": "Yes"}
  ]
}
```

### Swimlane YAML Format

```yaml
title: Customer Service Process
layout: LR
swimlanes:
  - Customer
  - Support Agent
  - Technical Team

nodes:
  - id: submit
    type: start
    label: Submit Ticket
    lane: Customer

  - id: review
    type: process
    label: Review Ticket
    lane: Support Agent

  - id: technical
    type: decision
    label: Technical Issue?
    lane: Support Agent

  - id: escalate
    type: process
    label: Escalate
    lane: Technical Team

  - id: resolve
    type: process
    label: Resolve
    lane: Support Agent

  - id: close
    type: end
    label: Close Ticket
    lane: Customer

connections:
  - from: submit
    to: review
  - from: review
    to: technical
  - from: technical
    to: escalate
    label: "Yes"
  - from: technical
    to: resolve
    label: "No"
  - from: escalate
    to: resolve
  - from: resolve
    to: close
```

## CLI Usage

```bash
# From YAML
python flowchart_gen.py --input process.yaml --output flowchart.png

# From JSON with custom layout
python flowchart_gen.py --input process.json --layout LR --output flow.png

# With style preset
python flowchart_gen.py --input workflow.yaml --style business --output workflow.svg

# High resolution
python flowchart_gen.py --input process.yaml --output chart.png --dpi 300
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input` | Input YAML or JSON file | Required |
| `--output` | Output file path | `flowchart.png` |
| `--layout` | Layout direction (TB, LR, BT, RL) | `TB` |
| `--style` | Style preset | `business` |
| `--dpi` | Image resolution | 96 |

## Examples

### Simple Linear Flow

```python
flow = FlowchartGenerator()
flow.start("Start")
flow.process("Step 1", id="s1")
flow.process("Step 2", id="s2")
flow.process("Step 3", id="s3")
flow.end("End")

flow.connect("Start", "s1")
flow.connect("s1", "s2")
flow.connect("s2", "s3")
flow.connect("s3", "End")

flow.generate().save("linear.png")
```

### Decision Flow

```python
flow = FlowchartGenerator()

flow.start("Start")
flow.input_output("Get Input", id="input")
flow.decision("Valid?", id="check")
flow.process("Process", id="proc")
flow.input_output("Show Error", id="error")
flow.end("End")

flow.connect("Start", "input")
flow.connect("input", "check")
flow.connect("check", "proc", label="Yes")
flow.connect("check", "error", label="No")
flow.connect("proc", "End")
flow.connect("error", "input")  # Loop back

flow.style("business")
flow.generate().save("decision_flow.png")
```

### Login Process

```python
flow = FlowchartGenerator()

flow.start("Start")
flow.input_output("Enter Credentials", id="creds")
flow.process("Validate", id="validate")
flow.decision("Valid?", id="check")
flow.decision("Attempts < 3?", id="attempts")
flow.process("Login Success", id="success")
flow.input_output("Show Error", id="error")
flow.process("Lock Account", id="lock")
flow.end("End")

flow.connect("Start", "creds")
flow.connect("creds", "validate")
flow.connect("validate", "check")
flow.connect("check", "success", label="Yes")
flow.connect("check", "attempts", label="No")
flow.connect("attempts", "creds", label="Yes")
flow.connect("attempts", "lock", label="No")
flow.connect("success", "End")
flow.connect("lock", "End")

flow.layout("TB")
flow.style("technical")
flow.generate().save("login_flow.png")
```

### Order Processing with Swimlanes

```python
flow = FlowchartGenerator()

flow.swimlanes(["Customer", "System", "Warehouse"])

flow.start("Order Placed", id="start", lane="Customer")
flow.process("Validate Order", id="validate", lane="System")
flow.decision("In Stock?", id="stock", lane="System")
flow.process("Reserve Items", id="reserve", lane="Warehouse")
flow.process("Backorder", id="backorder", lane="Warehouse")
flow.process("Process Payment", id="payment", lane="System")
flow.process("Ship Order", id="ship", lane="Warehouse")
flow.end("Complete", id="end", lane="Customer")

flow.connect("start", "validate")
flow.connect("validate", "stock")
flow.connect("stock", "reserve", label="Yes")
flow.connect("stock", "backorder", label="No")
flow.connect("reserve", "payment")
flow.connect("backorder", "payment")
flow.connect("payment", "ship")
flow.connect("ship", "end")

flow.layout("TB")
flow.generate().save("order_swimlane.png")
```

## Node Shapes

| Type | Shape | Usage |
|------|-------|-------|
| `start` | Oval/Ellipse | Beginning of flow |
| `end` | Oval/Ellipse | End of flow |
| `process` | Rectangle | Action or step |
| `decision` | Diamond | Yes/No branch |
| `io` | Parallelogram | Input/Output |
| `connector` | Circle | Page/flow connector |

## Style Presets

| Preset | Description |
|--------|-------------|
| `business` | Professional blue tones |
| `technical` | Gray/silver technical look |
| `minimal` | Black and white, clean |
| `colorful` | Vibrant multi-color |

## Dependencies

```
graphviz>=0.20.0
PyYAML>=6.0
```

**System Requirement**: Graphviz must be installed on the system.
- macOS: `brew install graphviz`
- Ubuntu: `apt-get install graphviz`
- Windows: Download from graphviz.org

## Limitations

- Complex nested decisions may require manual layout adjustments
- Swimlane rendering depends on graphviz subgraph support
- Very large flowcharts (50+ nodes) may be hard to read
- Limited control over exact node positioning
