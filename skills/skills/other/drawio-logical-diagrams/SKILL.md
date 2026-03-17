---
name: drawio-logical-diagrams
description: 'Creates professional logical flow diagrams and logical system architecture diagrams using draw.io XML format (.drawio files). Use when creating: (1) logical flow diagrams showing data/process flow between system components, (2) logical architecture diagrams representing system structure without cloud provider specifics, (3) BPMN process diagrams, (4) UML diagrams (class, sequence, activity), (5) data flow diagrams (DFD), (6) decision flowcharts, or (7) system interaction diagrams. This skill focuses on generic/abstract representations, not AWS/Azure-specific architectures (use aws-drawio-architecture-diagrams for cloud diagrams).'
allowed-tools: Read, Write, Bash
---

# Draw.io Logical Diagrams Creation

## Overview

Create professional logical diagrams in draw.io's native XML format. This skill enables generation of production-ready `.drawio` files for logical flow diagrams, system architecture visualizations, and abstract process representations using generic shapes and symbols.

## When to Use

Use this skill when:
- Creating logical flow diagrams showing data flow between system components
- Designing logical architecture diagrams (abstract system structure)
- Building BPMN process diagrams for business processes
- Drawing UML diagrams (class, sequence, activity, state)
- Creating data flow diagrams (DFD) for system analysis
- Making decision flowcharts with branching logic
- Visualizing system interactions and sequences
- Documenting logical system design without cloud specifics

**Do NOT use for:**
- AWS/Azure/GCP architecture diagrams (use `aws-drawio-architecture-diagrams`)
- Infrastructure-specific diagrams

## Instructions

### Creating a Logical Diagram

1. **Analyze the request**: Understand the system/process to diagram
2. **Choose diagram type**: Flowchart, architecture, BPMN, UML, DFD, etc.
3. **Identify elements**: Determine actors, processes, data stores, connectors
4. **Draft XML structure**: Create the mxGraphModel with proper root cells
5. **Add shapes**: Create mxCell elements with appropriate styles
6. **Add connectors**: Link elements with edge elements
7. **Validate XML**: Ensure all tags are closed and IDs are unique
8. **Output**: Write the .drawio file for the user

### Key XML Components

- `mxfile`: Root element with host and version
- `diagram`: Contains the diagram definition
- `mxGraphModel`: Canvas settings (grid, page size)
- `root`: Container for all cells (must include id="0" and id="1")
- `mxCell`: Individual shapes (vertices) or connectors (edges)

## Draw.io XML Structure

Every `.drawio` file follows this XML structure:

```xml
<mxfile host="app.diagrams.net" agent="Claude" version="24.7.17">
  <diagram id="logical-flow-1" name="Logical Flow">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1"
      tooltips="1" connect="1" arrows="1" fold="1" page="1"
      pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- Shapes and connectors here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

**Key rules:**
- IDs "0" and "1" are reserved for root cells
- Use sequential integer IDs starting from "2"
- Use landscape orientation for architecture diagrams
- All coordinates must be positive and aligned to grid (multiples of 10)

## Generic Shapes and Styles

### Basic Shape Types

| Shape | Style |
|-------|-------|
| Rectangle | `rounded=0;whiteSpace=wrap;html=1;` |
| Rounded Rectangle | `rounded=1;whiteSpace=wrap;html=1;` |
| Ellipse/Circle | `ellipse;whiteSpace=wrap;html=1;` |
| Diamond | `rhombus;whiteSpace=wrap;html=1;` |
| Cylinder | `shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;` |
| Hexagon | `shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;` |
| Parallelogram | `shape=ext;double=1;rounded=0;whiteSpace=wrap;html=1;` |

### Standard Color Palette

| Element Type | Fill Color | Border Color | Usage |
|--------------|------------|--------------|-------|
| Process | `#dae8fc` (light blue) | `#6c8ebf` | Operations/actions |
| Decision | `#fff2cc` (light yellow) | `#d6b656` | Conditional branches |
| Start/End | `#d5e8d4` (light green) | `#82b366` | Terminal states |
| Data/Store | `#e1f5fe` (light cyan) | `#0277bd` | Databases/files |
| Entity | `#f3e5f5` (light purple) | `#7b1fa2` | External systems |
| Error/Stop | `#f8cecc` (light red) | `#b85450` | Error states |
| Actor/User | `#ffe0b2` (light orange) | `#f57c00` | Users/actors |
| Container | `#f5f5f5` (light gray) | `#666666` | Grouping areas |

### Connector Styles

**Standard flow:**
```
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;endFill=1;strokeColor=#666666;strokeWidth=2;
```

**Dashed (alternative/optional):**
```
edgeStyle=orthogonalEdgeStyle;dashed=1;dashPattern=5 5;strokeColor=#666666;
```

**Arrow head styles:**
- `endArrow=classic;endFill=1` - Filled triangle
- `endArrow=open;endFill=0` - Open arrow
- `endArrow=blockThin;endFill=1` - Block arrow

## Diagram Types

### 1. Logical Flow Diagram

Shows the logical flow of data or processes through system components:

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  User   │────▶│ Service │────▶│  Data   │
└─────────┘     └─────────┘     └─────────┘
```

**Key elements:**
- Actors/Users (orange)
- Services/Processes (blue)
- Data Stores (cyan)
- External Systems (purple)
- Data flows (solid arrows)

### 2. Logical Architecture Diagram

Abstract representation of system components:

```
┌─────────────────────────────────────────┐
│            Presentation Layer            │
│  ┌─────────────┐  ┌─────────────┐       │
│  │  Web UI     │  │  Mobile    │       │
│  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│            Application Layer             │
│  ┌─────────────┐  ┌─────────────┐       │
│  │   API       │  │  Business   │       │
│  │   Gateway   │  │   Logic     │       │
│  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│              Data Layer                  │
│  ┌─────────────┐  ┌─────────────┐       │
│  │  Database   │  │    Cache    │       │
│  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────┘
```

### 3. BPMN Process Diagram

Business process modeling:

| Symbol | Meaning |
|--------|---------|
| Circle | Start/End Event |
| Rounded Rectangle | Activity/Task |
| Diamond | Gateway/Decision |
| Arrow | Sequence Flow |

### 4. UML Sequence Diagram

Interaction between components:

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  Actor  │     │Service A│     │Service B│
└────┬────┘     └────┬────┘     └────┬────┘
     │              │              │
     │─────────────▶│              │
     │              │─────────────▶│
     │              │◀─────────────│
     │◀─────────────│              │
```

### 5. Data Flow Diagram (DFD)

System data movement:

- **External Entity** (square) - Sources/destinations
- **Process** (circle/rounded) - Transformations
- **Data Store** (open rectangle) - Storage
- **Data Flow** (arrow) - Data movement

## Shape Examples

### Simple Process Box
```xml
<mxCell id="2" value="Process Name"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;"
  vertex="1" parent="1">
  <mxGeometry x="200" y="100" width="120" height="60" as="geometry" />
</mxCell>
```

### Decision Diamond
```xml
<mxCell id="3" value="Decision?"
  style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;"
  vertex="1" parent="1">
  <mxGeometry x="280" y="200" width="80" height="80" as="geometry" />
</mxCell>
```

### Start/End Oval
```xml
<mxCell id="4" value="Start"
  style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=12;"
  vertex="1" parent="1">
  <mxGeometry x="200" y="300" width="80" height="40" as="geometry" />
</mxCell>
```

### Data Store (Cylinder)
```xml
<mxCell id="5" value="Database"
  style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#e1f5fe;strokeColor=#0277bd;fontSize=12;"
  vertex="1" parent="1">
  <mxGeometry x="400" y="100" width="60" height="80" as="geometry" />
</mxCell>
```

### Connector/Arrow
```xml
<mxCell id="10"
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;endFill=1;strokeColor=#666666;strokeWidth=2;"
  edge="1" parent="1" source="2" target="3">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Label on Connector
```xml
<mxCell id="11" value="Data"
  style="text;html=1;align=center;verticalAlign=middle;fontSize=11;fontColor=#333333;labelBackgroundColor=#ffffff;"
  vertex="1" parent="1">
  <mxGeometry x="250" y="160" width="40" height="20" as="geometry" />
</mxCell>
```

## Layout Best Practices

1. **Flow direction**: Left-to-right or top-to-bottom consistently
2. **Spacing**: 40-60px between elements, 20px inside containers
3. **Grid alignment**: All coordinates in multiples of 10
4. **Label placement**: Above horizontal arrows, right of vertical arrows
5. **Container grouping**: Use rounded rectangles for logical groupings
6. **Balance**: Keep diagrams centered, avoid extreme whitespace

## Reference Files

For detailed templates and shape references, see:
- [shape-styles.md](references/shape-styles.md) - Complete shape and style reference
- [diagram-templates.md](references/diagram-templates.md) - Ready-to-use templates

## Examples

### Example 1: Simple Order Processing Flow

**User Request:**
"Create a logical flow diagram showing order processing: customer submits order, system validates, if valid then processes payment and ships, if invalid notifies customer."

**Generated XML:**
```xml
<mxfile host="app.diagrams.net" agent="Claude" version="24.7.17">
  <diagram id="order-flow-1" name="Order Processing">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- Start -->
        <mxCell id="2" value="Start"
          style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=12;"
          vertex="1" parent="1">
          <mxGeometry x="80" y="50" width="80" height="40" as="geometry" />
        </mxCell>
        <!-- Submit Order -->
        <mxCell id="3" value="Submit Order"
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;"
          vertex="1" parent="1">
          <mxGeometry x="60" y="130" width="120" height="60" as="geometry" />
        </mxCell>
        <!-- Validate -->
        <mxCell id="4" value="Validate&#xa;Order?"
          style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;"
          vertex="1" parent="1">
          <mxGeometry x="80" y="230" width="80" height="80" as="geometry" />
        </mxCell>
        <!-- Invalid: Notify -->
        <mxCell id="5" value="Notify&#xa;Customer"
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=12;"
          vertex="1" parent="1">
          <mxGeometry x="220" y="240" width="100" height="50" as="geometry" />
        </mxCell>
        <!-- Valid: Process Payment -->
        <mxCell id="6" value="Process&#xa;Payment"
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;"
          vertex="1" parent="1">
          <mxGeometry x="60" y="350" width="120" height="60" as="geometry" />
        </mxCell>
        <!-- Ship -->
        <mxCell id="7" value="Ship Order"
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;"
          vertex="1" parent="1">
          <mxGeometry x="60" y="450" width="120" height="60" as="geometry" />
        </mxCell>
        <!-- End -->
        <mxCell id="8" value="End"
          style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=12;"
          vertex="1" parent="1">
          <mxGeometry x="80" y="550" width="80" height="40" as="geometry" />
        </mxCell>
        <!-- Connectors -->
        <mxCell id="10" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;endFill=1;strokeColor=#666666;strokeWidth=2;" edge="1" parent="1" source="2" target="3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="11" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;endFill=1;strokeColor=#666666;strokeWidth=2;" edge="1" parent="1" source="3" target="4">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="12" value="No" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;endFill=1;strokeColor=#b85450;strokeWidth=2;fontSize=11;" edge="1" parent="1" source="4" target="5">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="13" value="Yes" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;endFill=1;strokeColor=#82b366;strokeWidth=2;fontSize=11;" edge="1" parent="1" source="4" target="6">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="14" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;endFill=1;strokeColor=#666666;strokeWidth=2;" edge="1" parent="1" source="6" target="7">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="15" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;endFill=1;strokeColor=#666666;strokeWidth=2;" edge="1" parent="1" source="7" target="8">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="16" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;endFill=1;strokeColor=#b85450;strokeWidth=2;" edge="1" parent="1" source="5" target="8">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

### Example 2: Three-Tier Logical Architecture

**User Request:**
"Create a logical architecture diagram for a web application with presentation, business logic, and data tiers."

**Generated XML:**
```xml
<mxfile host="app.diagrams.net" agent="Claude" version="24.7.17">
  <diagram id="three-tier-1" name="Three-Tier Architecture">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- User -->
        <mxCell id="2" value="User"
          style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffe0b2;strokeColor=#f57c00;fontSize=12;"
          vertex="1" parent="1">
          <mxGeometry x="40" y="340" width="60" height="40" as="geometry" />
        </mxCell>
        <!-- Presentation Layer -->
        <mxCell id="3" value="Presentation Layer"
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=14;fontStyle=1;"
          vertex="1" parent="1">
          <mxGeometry x="160" y="40" width="300" height="180" as="geometry" />
        </mxCell>
        <mxCell id="4" value="Web&#xa;Browser"
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;"
          vertex="1" parent="3">
          <mxGeometry x="20" y="30" width="80" height="50" as="geometry" />
        </mxCell>
        <mxCell id="5" value="Mobile&#xa;App"
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;"
          vertex="1" parent="3">
          <mxGeometry x="120" y="30" width="80" height="50" as="geometry" />
        </mxCell>
        <mxCell id="6" value="API&#xa;Client"
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;"
          vertex="1" parent="3">
          <mxGeometry x="200" y="30" width="80" height="50" as="geometry" />
        </mxCell>
        <!-- Application Layer -->
        <mxCell id="7" value="Application Layer"
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=14;fontStyle=1;"
          vertex="1" parent="1">
          <mxGeometry x="160" y="260" width="300" height="180" as="geometry" />
        </mxCell>
        <mxCell id="8" value="API&#xa;Gateway"
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;"
          vertex="1" parent="7">
          <mxGeometry x="20" y="30" width="80" height="50" as="geometry" />
        </mxCell>
        <mxCell id="9" value="Business&#xa;Logic"
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;"
          vertex="1" parent="7">
          <mxGeometry x="110" y="30" width="80" height="50" as="geometry" />
        </mxCell>
        <mxCell id="10" value="Auth&#xa;Service"
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;"
          vertex="1" parent="7">
          <mxGeometry x="200" y="30" width="80" height="50" as="geometry" />
        </mxCell>
        <!-- Data Layer -->
        <mxCell id="11" value="Data Layer"
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=14;fontStyle=1;"
          vertex="1" parent="1">
          <mxGeometry x="160" y="480" width="300" height="180" as="geometry" />
        </mxCell>
        <mxCell id="12" value="Primary&#xa;Database"
          style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#e1f5fe;strokeColor=#0277bd;fontSize=12;"
          vertex="1" parent="11">
          <mxGeometry x="20" y="30" width="60" height="80" as="geometry" />
        </mxCell>
        <mxCell id="13" value="Read&#xa;Replica"
          style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#e1f5fe;strokeColor=#0277bd;fontSize=12;"
          vertex="1" parent="11">
          <mxGeometry x="100" y="30" width="60" height="80" as="geometry" />
        </mxCell>
        <mxCell id="14" value="Cache&#xa;(Redis)"
          style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#fff3e0;strokeColor=#e65100;fontSize=12;"
          vertex="1" parent="11">
          <mxGeometry x="180" y="30" width="60" height="80" as="geometry" />
        </mxCell>
        <!-- Connectors -->
        <mxCell id="20" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;endFill=1;strokeColor=#666666;strokeWidth=2;" edge="1" parent="1" source="2" target="4">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="21" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;endFill=1;strokeColor=#666666;strokeWidth=2;" edge="1" parent="1" source="4" target="8">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="22" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;endFill=1;strokeColor=#666666;strokeWidth=2;" edge="1" parent="1" source="8" target="9">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="23" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;endFill=1;strokeColor=#666666;strokeWidth=2;" edge="1" parent="1" source="9" target="12">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="24" value="query" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=open;endFill=0;strokeColor=#666666;strokeWidth=1;fontSize=10;dashed=1;" edge="1" parent="1" source="9" target="14">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="25" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;endFill=1;strokeColor=#666666;strokeWidth=2;" edge="1" parent="1" source="9" target="13">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

### Example 3: Microservice Communication Flow

**User Request:**
"Create a logical diagram showing microservice architecture with API gateway, multiple services, and message queue for async communication."

**Reference:** See [diagram-templates.md](references/diagram-templates.md) for complete microservice template.

## Constraints and Warnings

### Critical Constraints

1. **XML validity**: Always close tags properly and escape special characters
2. **Unique IDs**: All cell IDs must be unique (except parent "0" and "1")
3. **Valid references**: Source/target must reference existing cell IDs
4. **Positive coordinates**: All x, y values must be >= 0

### Warnings

- XML files must be well-formed or will fail to open in draw.io
- Invalid parent references cause elements to disappear
- Negative coordinates place elements outside visible canvas

## Best Practices

### Visual Guidelines

1. Use consistent colors per element type
2. Keep arrows straight with minimal bends
3. Place labels at least 20px from arrow lines
4. Group related elements in containers
5. Use 12-14px font for labels, 10-11px for annotations

### Accessibility

1. Use high contrast colors
2. Don't rely solely on color to convey meaning
3. Include text labels for all shapes
4. Add annotations for complex flows
