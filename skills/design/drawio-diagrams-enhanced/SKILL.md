---
name: drawio-diagrams-enhanced
description: Create professional draw.io (diagrams.net) diagrams in XML format (.drawio files) with integrated PMP/PMBOK methodologies, extensive visual asset libraries, and industry-standard professional templates. Use this skill when users ask to create flowcharts, swimlane diagrams, cross-functional flowcharts, org charts, network diagrams, UML diagrams, BPMN, project management diagrams (WBS, Gantt, PERT, RACI), risk matrices, stakeholder maps, or any other visual diagram in draw.io format. This skill includes access to custom shape libraries for icons, clipart, and professional symbols.
---

# Enhanced Draw.io Diagram Creation Skill
# with PMP/PMBOK Integration & Visual Asset Libraries

This skill enables Claude to create professional, pixel-perfect diagrams in draw.io's native XML format with enterprise-grade capabilities including project management methodologies, extensive icon libraries, and industry-standard templates.

## Core Capabilities

### 1. Standard Diagram Types
- **Flowcharts**: Basic flowcharts, decision trees, process flows
- **Cross-Functional Flowcharts (CFF)**: Swimlane diagrams showing processes across departments/roles
- **BPMN Diagrams**: Business Process Model and Notation diagrams
- **UML Diagrams**: Class diagrams, sequence diagrams, use case diagrams
- **Network Diagrams**: Infrastructure, cloud architecture, system design
- **Org Charts**: Organizational hierarchies and team structures
- **Mind Maps**: Conceptual mapping and brainstorming
- **Entity Relationship Diagrams**: Database schemas

### 2. PMP/PMBOK Project Management Diagrams
- **Work Breakdown Structure (WBS)**: Hierarchical decomposition of project deliverables
- **Project Network Diagrams**: PERT charts, CPM, activity dependencies
- **Gantt Charts**: Timeline-based project schedules
- **RACI Matrices**: Responsibility assignment matrices
- **Risk Register Diagrams**: Risk matrices, heat maps, probability-impact grids
- **Stakeholder Maps**: Power-interest grids, influence diagrams
- **Resource Histograms**: Resource allocation and capacity planning
- **Communication Plans**: Information flow diagrams
- **Process Group Diagrams**: Initiating, Planning, Executing, Monitoring & Controlling, Closing
- **Knowledge Area Maps**: Integration, Scope, Schedule, Cost, Quality, Resource, Communications, Risk, Procurement, Stakeholder Management

### 3. Visual Asset Libraries Available

Claude can reference and incorporate shapes from extensive custom libraries:

**Icon & Symbol Libraries**:
- Material Design Icons
- Font Awesome icons
- OSA (Open Security Architecture) Icons
- UN-OCHA Humanitarian Icons
- Flat Color Icons
- Chart & Infographic Icons
- Windows 10 Icons
- Gesture & Fingerprint Icons

**Technology & Infrastructure**:
- Kubernetes Icons
- Cloud Provider Icons (AWS, Azure, GCP, DigitalOcean)
- Network Device Libraries (Cisco, Arista, Fortinet, Commvault)
- DevOps & CI/CD Pipeline Shapes

**Business & General Purpose**:
- Wireframe Components
- Avatars & People Icons
- Form Elements
- Bioicons (Life Sciences)
- Genogram Symbols
- Templates & Building Blocks

**How to Use Custom Libraries**:
When generating diagrams that would benefit from specific icons, Claude can note which libraries to enable:
```
To use this diagram optimally, open it with these custom libraries:
https://app.diagrams.net/?clibs=Uhttps://jgraph.github.io/drawio-libs/libs/templates.xml
```

## Draw.io File Format

Draw.io files are XML-based with the `.drawio` extension (or `.xml`). The basic structure is:

```xml
<mxfile host="app.diagrams.net" modified="[timestamp]" agent="Claude" version="24.7.17">
  <diagram id="[unique-id]" name="Page-1">
    <mxGraphModel dx="1434" dy="759" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <!-- Shapes and connectors go here -->
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Core Concepts

### 1. Cells (mxCell)
Everything in draw.io is a cell - shapes, connectors, containers, and even the root elements.

**Basic Shape Cell:**
```xml
<mxCell id="2" value="Process Step" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>
```

**Connector Cell:**
```xml
<mxCell id="3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="2" target="4">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 2. ID Management
- Each cell must have a unique ID
- Use sequential integers: "2", "3", "4", etc.
- IDs "0" and "1" are reserved for the root cells
- When referencing shapes in connectors, use the same IDs

### 3. Geometry (mxGeometry)
- `x`, `y`: Position (top-left corner)
- `width`, `height`: Dimensions
- `relative="1"`: For connectors (relative positioning)

### 4. Styling
Styles are semicolon-separated key-value pairs:
- **Shape type**: `rounded=1`, `ellipse`, `rhombus`
- **Colors**: `fillColor=#dae8fc`, `strokeColor=#6c8ebf`, `fontColor=#000000`
- **Text**: `fontSize=12`, `fontStyle=1` (bold=1, italic=2, underline=4)
- **Alignment**: `align=center`, `verticalAlign=middle`
- **Spacing**: `spacingLeft=10`, `spacingTop=5`

## PMP/PMBOK Specific Shapes & Styles

### Work Breakdown Structure (WBS)
WBS uses hierarchical tree structure with boxes connected by lines.

**WBS Package Box:**
```
shape=rectangle;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;fontSize=10;
```

**WBS Levels:**
- Level 0 (Project): Large box, 200x80, bold, dark green
- Level 1 (Deliverables): Medium box, 160x60, medium green
- Level 2 (Sub-deliverables): Small box, 140x50, light green
- Level 3 (Work Packages): Smallest box, 120x40, lightest green

### Project Network Diagram (PERT/CPM)

**Activity Node (AON - Activity on Node):**
```
shape=rectangle;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=0;
```

**Node Structure** (divided into sections):
```
┌─────────────────┐
│  Early Start ES │ Duration
├─────────────────┤
│  Activity Name  │
├─────────────────┤
│  Late Start LS  │ Late Finish LF
└─────────────────┘
```

**Critical Path Highlighting:**
```
fillColor=#f8cecc;strokeColor=#b85450;strokeWidth=3;
```

### RACI Matrix

**Matrix Container:**
```
swimlane;html=1;startSize=40;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;
```

**RACI Cells:**
- R (Responsible): `fillColor=#d5e8d4;strokeColor=#82b366;`
- A (Accountable): `fillColor=#dae8fc;strokeColor=#6c8ebf;`
- C (Consulted): `fillColor=#fff2cc;strokeColor=#d6b656;`
- I (Informed): `fillColor=#e1d5e7;strokeColor=#9673a6;`

### Gantt Chart Elements

**Timeline Bar:**
```
rounded=0;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;fontColor=#ffffff;
```

**Milestone Diamond:**
```
rhombus;whiteSpace=wrap;html=1;fillColor=#fa6800;strokeColor=#C73500;fontColor=#000000;
```

**Dependency Arrow:**
```
edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;strokeWidth=2;
```

### Risk Matrix (Probability-Impact Grid)

**Risk Matrix Structure:**
```
5x5 grid with:
- X-axis: Impact (Very Low, Low, Medium, High, Very High)
- Y-axis: Probability (Very Low, Low, Medium, High, Very High)
```

**Risk Level Colors:**
- **Low Risk**: `fillColor=#d5e8d4;strokeColor=#82b366;` (Green)
- **Medium Risk**: `fillColor=#fff2cc;strokeColor=#d6b656;` (Yellow)
- **High Risk**: `fillColor=#ffe6cc;strokeColor=#d79b00;` (Orange)
- **Critical Risk**: `fillColor=#f8cecc;strokeColor=#b85450;` (Red)

### Stakeholder Power-Interest Grid

**Quadrant Structure:**
```
┌─────────────────┬─────────────────┐
│   Manage        │    Partner      │
│   Closely       │    Closely      │
│ (High Power,    │ (High Power,    │
│  High Interest) │  High Interest) │
├─────────────────┼─────────────────┤
│   Keep          │    Keep         │
│   Satisfied     │    Informed     │
│ (High Power,    │ (Low Power,     │
│  Low Interest)  │  High Interest) │
└─────────────────┴─────────────────┘
```

## Common Shape Styles

### Flowchart Shapes

**Process (Rectangle):**
```
rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;
```

**Decision (Diamond):**
```
rhombus;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;
```

**Start/End (Rounded Rectangle):**
```
ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;
```

**Document:**
```
shape=document;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;
```

**Data (Parallelogram):**
```
shape=parallelogram;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;
```

### Swimlane Shapes

**Swimlane Container:**
```
swimlane;html=1;startSize=20;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;
```

**Vertical Swimlane:**
```
swimlane;html=1;startSize=20;fillColor=#f5f5f5;strokeColor=#666666;horizontal=0;fontStyle=1;
```

## Creating PMP/PMBOK Diagrams

### Work Breakdown Structure (WBS) Example

```xml
<mxfile host="app.diagrams.net">
  <diagram id="WBS-1" name="Project WBS">
    <mxGraphModel dx="1434" dy="759" grid="1" gridSize="10" guides="1">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <!-- Level 0: Project -->
        <mxCell id="2" value="Project Name" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;fontColor=#ffffff;fontStyle=1;fontSize=14;" vertex="1" parent="1">
          <mxGeometry x="280" y="40" width="200" height="80" as="geometry"/>
        </mxCell>
        
        <!-- Level 1: Major Deliverables -->
        <mxCell id="3" value="Deliverable 1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;fontColor=#ffffff;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="160" width="160" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="4" value="Deliverable 2" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;fontColor=#ffffff;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="240" y="160" width="160" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="5" value="Deliverable 3" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#60a917;strokeColor=#2D7600;fontColor=#ffffff;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="440" y="160" width="160" height="60" as="geometry"/>
        </mxCell>
        
        <!-- Connectors -->
        <mxCell id="6" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.25;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="2" target="3">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="7" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="2" target="4">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="8" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.75;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="2" target="5">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### RACI Matrix Example

```xml
<mxfile host="app.diagrams.net">
  <diagram id="RACI-1" name="RACI Matrix">
    <mxGraphModel dx="1434" dy="759" grid="1" gridSize="10" guides="1">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <!-- Matrix Container -->
        <mxCell id="2" value="RACI Matrix" style="swimlane;html=1;startSize=40;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;fontSize=14;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="720" height="400" as="geometry"/>
        </mxCell>
        
        <!-- Header Row -->
        <mxCell id="3" value="Activities / Tasks" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontStyle=1;" vertex="1" parent="2">
          <mxGeometry x="10" y="50" width="180" height="40" as="geometry"/>
        </mxCell>
        
        <mxCell id="4" value="Role A" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontStyle=1;" vertex="1" parent="2">
          <mxGeometry x="200" y="50" width="120" height="40" as="geometry"/>
        </mxCell>
        
        <mxCell id="5" value="Role B" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontStyle=1;" vertex="1" parent="2">
          <mxGeometry x="330" y="50" width="120" height="40" as="geometry"/>
        </mxCell>
        
        <!-- Task Rows with RACI Assignments -->
        <mxCell id="6" value="Task 1: Define Requirements" style="rounded=0;whiteSpace=wrap;html=1;align=left;spacingLeft=10;" vertex="1" parent="2">
          <mxGeometry x="10" y="100" width="180" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="7" value="R" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;fontSize=16;" vertex="1" parent="2">
          <mxGeometry x="200" y="100" width="120" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="8" value="A" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=16;" vertex="1" parent="2">
          <mxGeometry x="330" y="100" width="120" height="50" as="geometry"/>
        </mxCell>
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Stakeholder Power-Interest Grid Example

```xml
<mxfile host="app.diagrams.net">
  <diagram id="Stakeholder-1" name="Stakeholder Map">
    <mxGraphModel dx="1434" dy="759" grid="1" gridSize="10" guides="1">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <!-- Grid Background -->
        <!-- High Power, High Interest -->
        <mxCell id="2" value="Manage Closely&lt;br&gt;&lt;b&gt;(Key Players)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;verticalAlign=top;fontSize=12;fontStyle=0;" vertex="1" parent="1">
          <mxGeometry x="400" y="80" width="320" height="280" as="geometry"/>
        </mxCell>
        
        <!-- High Power, Low Interest -->
        <mxCell id="3" value="Keep Satisfied&lt;br&gt;&lt;b&gt;(Keep Informed)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;verticalAlign=top;fontSize=12;fontStyle=0;" vertex="1" parent="1">
          <mxGeometry x="400" y="360" width="320" height="280" as="geometry"/>
        </mxCell>
        
        <!-- Low Power, High Interest -->
        <mxCell id="4" value="Keep Informed&lt;br&gt;&lt;b&gt;(Show Consideration)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;verticalAlign=top;fontSize=12;fontStyle=0;" vertex="1" parent="1">
          <mxGeometry x="80" y="80" width="320" height="280" as="geometry"/>
        </mxCell>
        
        <!-- Low Power, Low Interest -->
        <mxCell id="5" value="Monitor&lt;br&gt;&lt;b&gt;(Minimal Effort)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;verticalAlign=top;fontSize=12;fontStyle=0;" vertex="1" parent="1">
          <mxGeometry x="80" y="360" width="320" height="280" as="geometry"/>
        </mxCell>
        
        <!-- Axis Labels -->
        <mxCell id="6" value="Interest" style="text;html=1;align=center;verticalAlign=middle;fontSize=14;fontStyle=1;rotation=90;" vertex="1" parent="1">
          <mxGeometry x="20" y="320" width="100" height="40" as="geometry"/>
        </mxCell>
        
        <mxCell id="7" value="Power / Influence" style="text;html=1;align=center;verticalAlign=middle;fontSize=14;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="350" y="660" width="200" height="40" as="geometry"/>
        </mxCell>
        
        <!-- Sample Stakeholders -->
        <mxCell id="8" value="CEO" style="ellipse;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;fontColor=#ffffff;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="520" y="150" width="80" height="60" as="geometry"/>
        </mxCell>
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Color Schemes

### Professional Blue Theme (Default)
- **Primary**: `fillColor=#dae8fc;strokeColor=#6c8ebf;`
- **Secondary**: `fillColor=#b1ddf0;strokeColor=#10739e;`
- **Accent**: `fillColor=#f8cecc;strokeColor=#b85450;`

### Green/Natural Theme
- **Primary**: `fillColor=#d5e8d4;strokeColor=#82b366;`
- **Secondary**: `fillColor=#fff2cc;strokeColor=#d6b656;`
- **Accent**: `fillColor=#e1d5e7;strokeColor=#9673a6;`

### Corporate/Neutral Theme
- **Primary**: `fillColor=#f5f5f5;strokeColor=#666666;`
- **Secondary**: `fillColor=#e1d5e7;strokeColor=#9673a6;`
- **Highlight**: `fillColor=#ffe6cc;strokeColor=#d79b00;`

### PMP Risk Matrix Colors
- **Critical**: `fillColor=#8B0000;strokeColor=#600000;fontColor=#ffffff;` (Dark Red)
- **High**: `fillColor=#FF0000;strokeColor=#CC0000;fontColor=#ffffff;` (Red)
- **Medium**: `fillColor=#FFA500;strokeColor=#CC8400;fontColor=#000000;` (Orange)
- **Low**: `fillColor=#FFFF00;strokeColor=#CCCC00;fontColor=#000000;` (Yellow)
- **Very Low**: `fillColor=#90EE90;strokeColor=#66AA66;fontColor=#000000;` (Light Green)

## Connector Styles

### Basic Connector
```
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;
```

### Straight Connector
```
rounded=0;html=1;jettySize=auto;orthogonalLoop=1;
```

### Curved Connector
```
curved=1;rounded=1;html=1;jettySize=auto;orthogonalLoop=1;
```

### With Arrow
```
edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=classic;endFill=1;
```

### Dashed Line (for dependencies)
```
edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;dashed=1;dashPattern=5 5;
```

### Thick Line (for critical path)
```
edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=3;strokeColor=#b85450;
```

## Best Practices

### 1. Layout Guidelines
- **Grid alignment**: Use x/y coordinates in multiples of 10 for clean alignment
- **Standard spacing**: 20-30px between shapes, 40-50px between rows
- **Shape sizes**: 
  - Small: 80x40
  - Medium: 120x60
  - Large: 160x80
  - Extra Large (Project boxes): 200x80
- **Swimlane heights**: 120-150px for single row, add 100px per additional row
- **WBS spacing**: 40px vertical, 20px horizontal between levels

### 2. Naming Conventions
- Use sequential IDs: "2", "3", "4"...
- Keep shape labels concise (1-5 words)
- Use Title Case for important labels
- Use sentence case for descriptions
- Add ID numbers to WBS packages (e.g., "1.2.3 Task Name")

### 3. Visual Hierarchy
- **Start shapes**: Use green/light colors
- **End shapes**: Use red/dark colors
- **Decision points**: Use orange/yellow
- **Regular processes**: Use blue/neutral
- **Important processes**: Use bolder colors or thicker borders
- **Critical path**: Use red with thick borders (strokeWidth=3)

### 4. PMP/PMBOK Specific
- **WBS Levels**: Use progressively lighter shades for deeper levels
- **RACI Matrix**: Consistently use R=Green, A=Blue, C=Yellow, I=Purple
- **Risk Matrix**: Follow standard risk color coding (Green to Red)
- **Critical Path**: Always highlight in red with strokeWidth=3
- **Milestones**: Use diamond shapes with distinct colors

### 5. Readability
- Keep diagrams under 20-25 shapes when possible
- Group related processes in the same swimlane
- Use consistent shape sizes within the same category
- Label all connectors for complex flows
- Add whitespace between dense sections
- Include legends for symbols/colors in complex diagrams

## PMBOK Process Groups & Knowledge Areas Quick Reference

### 5 Process Groups
1. **Initiating**: Green colors (`#d5e8d4`)
2. **Planning**: Blue colors (`#dae8fc`)
3. **Executing**: Orange colors (`#ffe6cc`)
4. **Monitoring & Controlling**: Yellow colors (`#fff2cc`)
5. **Closing**: Purple colors (`#e1d5e7`)

### 10 Knowledge Areas
1. **Integration Management**: Gray (`#f5f5f5`)
2. **Scope Management**: Blue (`#dae8fc`)
3. **Schedule Management**: Green (`#d5e8d4`)
4. **Cost Management**: Orange (`#ffe6cc`)
5. **Quality Management**: Red (`#f8cecc`)
6. **Resource Management**: Purple (`#e1d5e7`)
7. **Communications Management**: Teal (`#b1ddf0`)
8. **Risk Management**: Yellow (`#fff2cc`)
9. **Procurement Management**: Pink (`#f8cecc`)
10. **Stakeholder Management**: Light Purple (`#e1d5e7`)

## Professional Diagram Templates

### Template 1: Cross-Functional Flowchart (Swimlane)
**Use Case**: Business process across departments
**Structure**: Horizontal swimlanes, one per department
**Key Features**: Clear handoffs, decision points, subprocess indicators

### Template 2: Work Breakdown Structure (WBS)
**Use Case**: Project scope decomposition
**Structure**: Hierarchical tree, 3-4 levels deep
**Key Features**: Numbered packages (1.1, 1.2, etc.), deliverable-oriented

### Template 3: Project Network Diagram (PERT/CPM)
**Use Case**: Activity sequencing and critical path analysis
**Structure**: Activity nodes with duration, early/late start/finish
**Key Features**: Critical path highlighted, float calculations

### Template 4: RACI Matrix
**Use Case**: Role and responsibility assignment
**Structure**: Grid with tasks (rows) and roles (columns)
**Key Features**: R, A, C, I assignments with color coding

### Template 5: Risk Register Heat Map
**Use Case**: Visual risk assessment
**Structure**: 5x5 grid (Probability vs Impact)
**Key Features**: Color-coded zones, risk items plotted on grid

### Template 6: Stakeholder Power-Interest Grid
**Use Case**: Stakeholder analysis and engagement strategy
**Structure**: 2x2 or 3x3 grid
**Key Features**: Quadrant labels, stakeholder names plotted

### Template 7: Organizational Breakdown Structure (OBS)
**Use Case**: Project team hierarchy
**Structure**: Hierarchical tree similar to org chart
**Key Features**: Names, roles, reporting relationships

### Template 8: Resource Histogram
**Use Case**: Resource allocation over time
**Structure**: Bar chart with time on X-axis, resources on Y-axis
**Key Features**: Color-coded resource types, over-allocation indicators

## Error Prevention

### Common Issues
1. **Overlapping shapes**: Ensure x/y coordinates don't overlap
2. **Missing parents**: Swimlane children must reference parent ID
3. **Invalid IDs**: Don't reuse IDs, keep them sequential
4. **Malformed style strings**: Always end with semicolon
5. **Incorrect connector references**: `source` and `target` must match existing shape IDs
6. **WBS numbering**: Ensure hierarchical numbering is consistent (1.0, 1.1, 1.1.1)

### Validation Checklist
- [ ] All IDs are unique
- [ ] Root cells (0, 1) exist
- [ ] All connectors have valid source/target
- [ ] Swimlane children have correct parent references
- [ ] Coordinates are positive numbers
- [ ] Style strings are properly formatted
- [ ] XML is well-formed (properly nested tags)
- [ ] WBS packages have proper hierarchical numbering
- [ ] RACI matrix has all cells filled (no blanks)
- [ ] Risk matrix uses standard color coding

## Custom Library Integration

When creating diagrams that benefit from specific icon libraries, include instructions like:

```markdown
## How to Open with Custom Libraries

To access additional icons and shapes for this diagram, open it with:

https://app.diagrams.net/?clibs=Uhttps://jgraph.github.io/drawio-libs/libs/templates.xml;Uhttps://jgraph.github.io/drawio-libs/libs/un-ocha-icons.xml

Or manually in draw.io:
1. Open the diagram in app.diagrams.net
2. File → Open Library from → URL
3. Enter: https://jgraph.github.io/drawio-libs/libs/[library-name].xml
```

## Output Format

Always output the complete `.drawio` file with:
1. Proper XML declaration (optional but recommended)
2. Complete mxfile structure
3. All necessary root cells
4. Properly formatted and indented for readability
5. Save with `.drawio` or `.xml` extension
6. Include usage instructions if custom libraries are beneficial

## Tips for Excellence

1. **Ask clarifying questions** if the process/project isn't clear
2. **Suggest improvements** to workflows if you spot issues
3. **Use appropriate shapes** for different process types and PM artifacts
4. **Maintain consistency** in sizing, spacing, and color schemes
5. **Consider the audience** - executives need less detail than implementers
6. **Test the flow logic** - ensure all paths lead somewhere
7. **Add legends** if using multiple shape types or colors
8. **Include PMBOK process group** identifiers when relevant
9. **Reference custom libraries** that would enhance the diagram
10. **Provide opening instructions** if special libraries are needed

## Professional Templates Library

The following template patterns can be adapted for various use cases:

1. **Agile/Scrum Diagrams**: Sprint planning, retrospectives, burndown charts
2. **DevOps Pipelines**: CI/CD flows with stages, gates, and tools
3. **Business Model Canvas**: 9-box strategic planning tool
4. **Value Stream Mapping**: Lean process analysis with cycle times
5. **SIPOC Diagrams**: Supplier-Input-Process-Output-Customer
6. **Fishbone/Ishikawa**: Root cause analysis
7. **Affinity Diagrams**: Idea clustering and organization
8. **Decision Trees**: Multi-level decision analysis
9. **Use Case Diagrams**: UML user-system interactions
10. **Data Flow Diagrams**: Information flow analysis

## Resources

- Official draw.io documentation: https://www.drawio.com/doc/
- Example diagrams: https://www.drawio.com/example-diagrams
- Custom libraries repository: https://github.com/jgraph/drawio-libs
- Template library: Available in draw.io via Arrange > Insert > Template
- Shape libraries: Enable via "More Shapes" in draw.io
- PMBOK Guide (6th & 7th Edition): PMI official documentation
- Project Management Institute: https://www.pmi.org/

## Limitations

- Complex custom shapes may require manual adjustment
- Some advanced features (layers, pages) may need manual setup
- 3D shapes and advanced styling might not be fully represented
- Custom library icons require internet connection to load
- Very large WBS structures may need to be split across pages
- Always recommend testing the generated file in draw.io

Remember: The goal is to create diagrams that are immediately usable, professional-looking, accurately represent the user's process or system, and follow PMP/PMBOK best practices when applicable!
