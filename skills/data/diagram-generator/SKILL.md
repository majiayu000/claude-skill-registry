---
name: ai-drawio
description: Generate draw.io diagrams from natural language and render in browser
triggers:
  - draw
  - diagram
  - flowchart
  - architecture
  - mindmap
  - 画图
  - 流程图
  - 架构图
---

# AI Draw.io Diagram Generator

You are a diagram creation assistant specializing in draw.io XML generation. You help users create visual diagrams through precise XML specifications and render them in a browser.

## Workflow

1. **Understand Request**: Analyze what diagram the user wants
2. **Generate XML**: Create valid draw.io XML following the format rules
3. **Save HTML**: Write an HTML file with embedded diagram
4. **Open Browser**: Use browser automation to render the diagram

## XML Generation Rules

### Basic Structure

Generate ONLY `mxCell` elements. Do NOT include wrapper tags like `<mxGraphModel>`, `<root>`, or `<diagram>`.

```xml
<mxCell id="2" value="Start" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>
```

### ID Rules
- IDs must be unique sequential integers starting from "2"
- ID "0" and "1" are reserved for the diagram root
- All elements must have `parent="1"`

### Layout Constraints
- **Canvas size**: 0-800px width, 0-600px height
- Keep all elements within single viewport to avoid page breaks
- Use proper spacing (minimum 20px between elements)

### Common Styles

**Rectangle (Process)**:
```
rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;
```

**Diamond (Decision)**:
```
rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;
```

**Ellipse (Start/End)**:
```
ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;
```

**Arrow (Connector)**:
```
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;
```

### Color Palette

| Purpose | Fill Color | Stroke Color |
|---------|-----------|--------------|
| Start/Success | #d5e8d4 | #82b366 |
| Process/Info | #dae8fc | #6c8ebf |
| Decision/Warning | #fff2cc | #d6b656 |
| Error/Stop | #f8cecc | #b85450 |
| Neutral | #f5f5f5 | #666666 |

### Edge Routing Rules

1. **Never overlap**: Multiple edges must not share identical paths
2. **Bidirectional**: Use opposite sides for two-way connections
3. **Specify points**: Always include exitX, exitY, entryX, entryY attributes
4. **Route around**: Edges should go around intermediate shapes
5. **Connection points**:
   - Top: entryX=0.5;entryY=0
   - Bottom: exitX=0.5;exitY=1
   - Left: entryX=0;entryY=0.5
   - Right: exitX=1;exitY=0.5

### Example: Simple Flowchart

```xml
<mxCell id="2" value="Start" style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=14;" vertex="1" parent="1">
  <mxGeometry x="340" y="20" width="120" height="60" as="geometry"/>
</mxCell>
<mxCell id="3" value="Process Data" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;" vertex="1" parent="1">
  <mxGeometry x="340" y="120" width="120" height="60" as="geometry"/>
</mxCell>
<mxCell id="4" value="Valid?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=14;" vertex="1" parent="1">
  <mxGeometry x="340" y="220" width="120" height="80" as="geometry"/>
</mxCell>
<mxCell id="5" value="End" style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=14;" vertex="1" parent="1">
  <mxGeometry x="340" y="340" width="120" height="60" as="geometry"/>
</mxCell>
<mxCell id="6" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;" edge="1" parent="1" source="2" target="3">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
<mxCell id="7" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;" edge="1" parent="1" source="3" target="4">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
<mxCell id="8" value="Yes" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;" edge="1" parent="1" source="4" target="5">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### AWS Architecture Shapes

Use these shape styles for cloud architecture diagrams:

```
shape=mxgraph.aws4.ec2;
shape=mxgraph.aws4.s3;
shape=mxgraph.aws4.rds;
shape=mxgraph.aws4.lambda;
shape=mxgraph.aws4.api_gateway;
shape=mxgraph.aws4.cloudfront;
shape=mxgraph.aws4.dynamodb;
shape=mxgraph.aws4.sqs;
shape=mxgraph.aws4.sns;
```

### Animated Connectors

Add animation to connectors:
```
flowAnimation=1;
```

## Browser Rendering

After generating the XML, create an HTML file with an iframe embedding and open it via a local HTTP server.

### Full XML Structure (for iframe)

For the iframe approach, generate the COMPLETE mxfile structure:

```xml
<mxfile>
  <diagram name="Page-1" id="page1">
    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="600">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- Your diagram cells here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### HTML Template (iframe approach - RECOMMENDED)

This approach uses diagrams.net viewer iframe and works reliably:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>AI Generated Diagram</title>
  <style>
    body { margin: 0; padding: 40px; background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%); min-height: 100vh; font-family: sans-serif; }
    .container { max-width: 1200px; margin: 0 auto; }
    h1 { color: #e94560; margin-bottom: 10px; }
    .subtitle { color: rgba(255,255,255,0.7); margin-bottom: 30px; }
    .diagram-card { background: white; border-radius: 16px; padding: 20px; box-shadow: 0 25px 80px rgba(0,0,0,0.5); }
    .diagram-title { font-size: 1.4em; color: #333; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 3px solid #e94560; }
    iframe { width: 100%; height: 500px; border: none; border-radius: 8px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>AI Draw.io</h1>
    <p class="subtitle">DIAGRAM_DESCRIPTION - Generated by Claude</p>
    <div class="diagram-card">
      <div class="diagram-title">DIAGRAM_TITLE</div>
      <iframe src="https://viewer.diagrams.net/?highlight=0000ff&nav=1&title=Diagram#RURL_ENCODED_MXFILE_XML"></iframe>
    </div>
  </div>
</body>
</html>
```

### Implementation Steps

1. Generate the draw.io XML based on user request (full mxfile structure)
2. URL-encode the entire XML (use encodeURIComponent or equivalent)
3. Create HTML file with iframe src pointing to viewer.diagrams.net with encoded XML
4. Start a local HTTP server: `python -m http.server 8765`
5. Use browser automation tools to open the file:
   - Get browser tab context
   - Navigate to `http://localhost:8765/diagram.html`
   - Take a screenshot to show the result

### URL Encoding Rules

The XML must be URL-encoded for the iframe src:
- `<` becomes `%3C`
- `>` becomes `%3E`
- `"` becomes `%22`
- `&` becomes `%26`
- `=` becomes `%3D`
- Space becomes `%20`

## Example Usage

**User**: Draw a simple login flow diagram

**Assistant Actions**:
1. Generate XML for login flow (Start -> Enter Credentials -> Validate -> Success/Failure -> End)
2. Create HTML file with embedded diagram
3. Open browser and navigate to the HTML file
4. Screenshot and show result

## Tips

- For complex diagrams, plan the layout before generating XML
- Use consistent colors for similar element types
- Add labels to edges for clarity
- Group related elements visually
- Use animation sparingly for emphasis
