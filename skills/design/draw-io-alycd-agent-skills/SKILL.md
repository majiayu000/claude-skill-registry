---
name: draw-io
description: Create professional Draw.io (diagrams.net) XML diagrams for architecture, network flows, and system designs. Use when the user asks to create diagrams, architecture diagrams, flow charts, network diagrams, system diagrams, or mentions Draw.io/diagrams.net. Supports AWS/GCP icons, grouping, and custom styling.
---

# Draw.io Diagram Builder

Create professional, well-structured Draw.io XML diagrams with proper spacing, icons, grouping, and styling.

## Skill Structure

This skill is organized as follows:

- **SKILL.md** (this file) - Main instructions and workflow for creating diagrams
- **templates/** - Example diagrams and starter templates
  - `example-diagram.drawio.xml` - Complete working example with groups and styling
- **references/** - Detailed technical documentation
  - `api-reference.md` - XML structure, icon library, colors, and validation rules
- **assets/** - Static resources (reserved for future use)
- **scripts/** - Automation helpers (reserved for future use)

💡 **Quick tip**: Start here for the workflow, refer to `references/api-reference.md` for detailed XML syntax and icon codes.

## Quick Start

When the user requests a diagram:
1. Identify the components and their flow (A → B → C)
2. Determine if grouping is needed (e.g., [x, y, z] notation)
3. Create the XML structure with proper canvas size
4. Add styled boxes with icons for each component
5. Connect with arrows
6. Save as `.drawio.xml` file

## Core Components

### Canvas Structure

Every diagram needs:
- **Page dimensions**: 1400x900 minimum (adjust based on complexity)
- **Background color**: ALWAYS set `background="#ffffff"` in mxGraphModel (critical for visibility)
- **Title bar**: Blue header with diagram title
- **Platform container**: Gray background box (optional, for cloud diagrams)
- **Grid**: 10px grid for alignment

### Box Components

Each component box includes:
- **Container**: White rounded rectangle with shadow
- **Icon**: Hexagonal icon (AWS/GCP style)
- **Labels**: Category, service name, and description
- **Sizing**: Minimum 150x70, adjust for text length

### Arrows

Connect boxes with:
- **Style**: Orthogonal edges with blue (#4284F3) stroke
- **Width**: 2px stroke width
- **Arrow heads**: Block thin style
- **Spacing**: Ensure adequate space for routing

## Instructions

### Step 1: Parse the User Request

Extract the flow structure:
- **Linear flow**: A → B → C → D
- **Grouped components**: [server1, server2] means these should be in a container
- **Branching**: One component leading to multiple (fan-out)

Example parsing:
```
"MTA -> Direct Connect -> HAProxy -> [server1, server2] -> [box a, box b] -> database"

Components: 6 main boxes
Groups: 2 (servers and boxes)
Arrows: 5 connections
```

### Step 2: Determine Layout

Calculate positions:
- **Horizontal spacing**: 50-70px between boxes
- **Vertical spacing**: 110px for vertical flow
- **Group padding**: 20px inside containers, 30px for title
- **Start position**: x=140, y=250 for first component

Layout patterns:
- **Linear horizontal**: Place boxes left-to-right
- **Vertical with branches**: Main flow down center, branches to sides
- **Groups**: Container box with inner components

### Step 3: Choose Icons

Select appropriate icons based on component type:

**AWS Icons** (use `fillColor=#FF9900`):
- Network: `cloud_vpn`, `cloud_router`
- Compute: `compute_engine`, `app_engine`
- Storage: `cloud_storage`, `cloud_sql`
- Messaging: `cloud_pubsub`

**GCP Icons** (use `fillColor=#5184F3` or `#4285F4`):
- Processing: `cloud_dataflow`, `cloud_functions`
- Data: `bigquery`, `cloud_bigtable`
- Messaging: `cloud_pubsub`

**Generic Icons**:
- Load balancer: `#34A853` (green)
- Processing: `#FBBC04` (yellow)
- Database: `#EA4335` (red)

All icons use: `shape=mxgraph.gcp2.hexIcon`

### Step 4: Create Groups

When you see `[x, y, z]` notation:

1. **Create container box**:
   - Larger dimensions to hold inner boxes
   - Colored background (light tint)
   - Stroke color (darker shade)
   - Title at top
   - Shadow enabled

2. **Place inner components**:
   - Position inside container with padding
   - Smaller box sizes (90x60 typical)
   - Arrange horizontally or in grid
   - Leave space for title

3. **Single arrow into group**:
   - Connect to the container, not individual boxes
   - Arrow points to container edge

Group color schemes:
- **Servers/Compute**: Green tints (#E8F5E9 fill, #81C784 stroke)
- **Processing**: Orange tints (#FFF3E0 fill, #FFB74D stroke)
- **Storage**: Blue tints (#E3F2FD fill, #64B5F6 stroke)

### Step 5: Build XML Structure

Use this template structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" agent="Claude Code" version="28.1.2">
  <diagram id="unique-id" name="Page-1">
    <mxGraphModel dx="1554" dy="797" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1" page="1"
                  pageScale="1" pageWidth="1400" pageHeight="900"
                  background="#ffffff" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Title Bar -->
        <mxCell id="title-bar" value="Architecture: ..." />

        <!-- Optional Platform Container -->
        <mxCell id="platform-container" value="Cloud Platform" />

        <!-- Edges (arrows) -->
        <mxCell id="edge-1" style="..." source="box-1" target="box-2" />

        <!-- Boxes -->
        <mxCell id="box-1" value="" ... />
        <mxCell id="box-1-label" value="..." part="1" ... />

        <!-- Groups (if needed) -->
        <mxCell id="group-1" value="Group Title" ... />

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

**IMPORTANT**: The `background="#ffffff"` attribute in mxGraphModel is REQUIRED for proper rendering.

### Step 6: Size Boxes Appropriately

Ensure text fits properly:

**Standard sizes**:
- Simple name (< 15 chars): 150x70
- Medium name (15-30 chars): 170x80
- Long name (> 30 chars): 180x80 or 200x80

**Grouped boxes**:
- Inner boxes: 90x60 minimum
- Container: (number_of_boxes * 110 + 40) width

**Minimum dimensions**:
- Never smaller than 90x60
- Leave 10px padding around text
- Icon needs 44x39 space

### Step 7: Add Proper Spacing

Arrow routing needs space:
- **Horizontal gaps**: 50px minimum between boxes
- **Vertical gaps**: 110px for branching flows
- **Group boundaries**: 20px padding inside
- **Canvas margins**: 100px from edges

### Step 8: Apply Consistent Styling

Use these style patterns:

**Title Bar**:
```
fillColor=#4DA1F5;strokeColor=none;shadow=1;fontSize=14;
align=left;spacingLeft=50;fontColor=#ffffff
```

**Platform Container**:
```
fillColor=#F6F6F6;strokeColor=none;shadow=0;fontSize=14;
align=left;spacingLeft=40;fontColor=#717171
```

**Component Box**:
```
strokeColor=#dddddd;fillColor=#ffffff;shadow=1;strokeWidth=1;
rounded=1;absoluteArcSize=1;arcSize=2
```

**Arrow**:
```
edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#4284F3;
strokeWidth=2;startFill=1;endArrow=blockThin;endFill=1
```

**Group Container**:
```
fillColor=#E8F5E9;strokeColor=#81C784;strokeWidth=2;
rounded=1;arcSize=5;shadow=1
```

### Step 9: Validate the Diagram

Before finalizing:
- [ ] All boxes have minimum size and proper text spacing
- [ ] Arrows connect correctly and have routing space
- [ ] Groups contain components with single arrow in
- [ ] Icons use hexagon shape
- [ ] Colors are consistent with component types
- [ ] XML is valid (matching open/close tags)
- [ ] IDs are unique
- [ ] Canvas size accommodates all elements

### Step 10: Save and Inform User

Save the file as:
- `[descriptive-name].drawio.xml`
- In the current working directory or specified location

Inform the user:
- File path where saved
- How to open (app.diagrams.net)
- Key features of the diagram
- Any customizations made

## Examples

### Linear Flow

```
User: "Create a diagram: API -> Load Balancer -> App Server -> Database"

Result:
- 4 boxes horizontally aligned
- Blue arrows connecting left-to-right
- API (cloud icon), LB (network icon), Server (compute icon), DB (database icon)
- Total width: ~700px, positioned centered
```

### Grouped Components

```
User: "MTA -> Gateway -> [web1, web2, web3] -> Database"

Result:
- MTA box at x=140
- Gateway box at x=340
- Group container at x=540 containing:
  - web1, web2, web3 as smaller boxes
  - Green background with "Web Servers" title
- Database box at x=820
- Arrow into group (not into individual servers)
```

### Branching Flow

```
User: "Input -> Processor -> [Storage, Analytics, Notifications]"

Result:
- Linear flow to Processor
- Three arrows from Processor to separate endpoints
- Vertical spacing between endpoints (110px each)
- Processor at center, endpoints staggered vertically
```

## Best Practices

1. **Use descriptive IDs**: `box-mta`, `edge-1-2`, `group-servers`
2. **Consistent naming**: Match ID to component purpose
3. **Color coordination**: Group by function (compute, storage, network)
4. **Adequate spacing**: Never let boxes/arrows overlap
5. **Readable text**: Minimum 11px font, high contrast
6. **Group logically**: Related components in same container
7. **Single entry per group**: One arrow into grouped components
8. **Scale appropriately**: Larger diagrams need bigger canvas
9. **Test rendering**: Ensure XML is valid before saving
10. **Document customizations**: Note any special requirements

## Icon Reference

### Common Icon Types

| Component Type | Icon prIcon Value | Hex Color |
|---------------|------------------|-----------|
| API/Gateway | `cloud_vpn` | #FF9900 |
| Load Balancer | `compute_engine` | #34A853 |
| Server/Compute | `compute_engine` | #4285F4 |
| Processing | `cloud_dataflow` | #5184F3 |
| Functions | `cloud_functions` | #FBBC04 |
| Message Queue | `cloud_pubsub` | #5184F3 |
| Database | `cloud_sql` | #EA4335 |
| Storage | `cloud_storage` | #4285F4 |
| Analytics | `bigquery` | #5184F3 |
| Network | `cloud_router` | #FF9900 |

### Icon Template

```xml
<mxCell id="box-label"
  value="&lt;font color=&quot;#000000&quot;&gt;Category&lt;/font&gt;&lt;br&gt;Service Name&lt;hr&gt;&lt;font style=&quot;font-size: 11px&quot;&gt;Description&lt;/font&gt;"
  style="dashed=0;connectable=0;html=1;fillColor=#5184F3;strokeColor=none;shape=mxgraph.gcp2.hexIcon;prIcon=cloud_dataflow;part=1;labelPosition=right;verticalLabelPosition=middle;align=left;verticalAlign=top;spacingLeft=5;fontColor=#999999;fontSize=12;spacingTop=-8;"
  parent="box-id"
  vertex="1">
  <mxGeometry width="44" height="39" relative="1" as="geometry">
    <mxPoint x="5" y="10" as="offset" />
  </mxGeometry>
</mxCell>
```

## Troubleshooting

**Boxes overlap**:
- Increase horizontal/vertical spacing
- Reduce box sizes if too large
- Check canvas dimensions

**Text doesn't fit**:
- Increase box width (try +20px increments)
- Reduce font size for descriptions
- Use line breaks in labels

**Arrows route incorrectly**:
- Increase spacing between components
- Check source/target IDs match
- Ensure orthogonal routing has space

**Groups look wrong**:
- Add 20px padding inside container
- Ensure container is large enough
- Position title with spacingTop

**XML invalid**:
- Check all tags close properly
- Escape special chars (&lt; &gt; &amp; &quot;)
- Verify ID uniqueness
- Match parent references

## File Naming

Use descriptive names:
- `network-flow-diagram.drawio.xml`
- `aws-architecture.drawio.xml`
- `data-pipeline.drawio.xml`
- `microservices-diagram.drawio.xml`

## Testing

After creating a diagram:
1. Open in browser: https://app.diagrams.net
2. Import the XML file
3. Verify all components render correctly
4. Check text readability
5. Ensure arrows connect properly
6. Test grouping and layouts

## Files and Resources

### Templates
- `templates/example-diagram.drawio.xml` - Complete example of a data flow diagram with grouping

### References
- `references/api-reference.md` - Detailed XML structure documentation, icon library, and technical specifications

### External Resources
- Draw.io documentation: https://www.diagrams.net/doc/
- Icon library: https://github.com/jgraph/drawio/tree/dev/src/main/webapp/shapes
