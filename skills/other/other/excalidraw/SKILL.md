---
name: excalidraw
description: Create and design Excalidraw diagrams, especially architecture diagrams for software, cloud (AWS, Azure, GCP), databases, AI/ML, analytics, and infrastructure. Generates valid .excalidraw JSON files. Works with VS Code, VS Code Insiders, Obsidian. Triggers on excalidraw, architecture diagram, system design, cloud diagram, infrastructure diagram, flowchart, whiteboard, software architecture, database diagram, network diagram, data flow, microservices diagram.
---

# Excalidraw Diagrams

Create hand-drawn style diagrams for architecture, flowcharts, and technical documentation.

## JSON File Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [/* ExcalidrawElement[] */],
  "appState": {
    "gridSize": 20,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## Element Types

### Common Properties (All Elements)

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier |
| `type` | string | Element type |
| `x` | number | X coordinate |
| `y` | number | Y coordinate |
| `width` | number | Width in pixels |
| `height` | number | Height in pixels |
| `strokeColor` | string | Border color (hex) |
| `backgroundColor` | string | Fill color or "transparent" |
| `fillStyle` | string | "solid", "hachure", "cross-hatch" |
| `strokeWidth` | number | Border width (1, 2, 4) |
| `roughness` | number | Hand-drawn effect (0-2) |
| `opacity` | number | 0-100 |

### Rectangle

```json
{
  "id": "rect-1",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 100,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roundness": { "type": 3 }
}
```

### Text

```json
{
  "id": "text-1",
  "type": "text",
  "x": 100,
  "y": 100,
  "text": "API Gateway",
  "fontSize": 20,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": null
}
```

Font families: 1=Virgil (hand-drawn), 2=Helvetica, 3=Cascadia (monospace)

### Arrow

```json
{
  "id": "arrow-1",
  "type": "arrow",
  "x": 200,
  "y": 130,
  "width": 100,
  "height": 0,
  "points": [[0, 0], [100, 0]],
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "startBinding": {
    "elementId": "rect-1",
    "focus": 0,
    "gap": 5
  },
  "endBinding": {
    "elementId": "rect-2",
    "focus": 0,
    "gap": 5
  }
}
```

### Ellipse

Same properties as rectangle. Use for circles (equal width/height).

### Diamond

Same properties as rectangle. Renders as a rotated square (rhombus).

## Element Bindings

### Connecting Arrow to Shape

1. Add `boundElements` to the shape:
```json
{
  "id": "rect-1",
  "boundElements": [
    { "id": "arrow-1", "type": "arrow" }
  ]
}
```

2. Add `startBinding` or `endBinding` to the arrow.

### Text Inside Shape

1. Add `boundElements` to container
2. Set `containerId` on the text element

## Grouping Elements

Assign the same `groupIds` array to related elements:

```json
{
  "id": "rect-1",
  "groupIds": ["group-1"]
},
{
  "id": "text-1",
  "groupIds": ["group-1"]
}
```

## Color Reference

### Default Palette

| Color | Hex | Use |
|-------|-----|-----|
| Black | `#1e1e1e` | Strokes, text |
| White | `#ffffff` | Backgrounds |
| Light Blue | `#a5d8ff` | Compute services |
| Light Green | `#b2f2bb` | Databases, storage |
| Light Orange | `#ffd8a8` | Networking |
| Light Red | `#ffc9c9` | Security, errors |
| Light Purple | `#d0bfff` | Integration |
| Light Yellow | `#fff3bf` | Highlights |
| Gray | `#dee2e6` | External, users |

## Service Box with Label

```json
[
  {
    "id": "service-1",
    "type": "rectangle",
    "x": 100,
    "y": 100,
    "width": 120,
    "height": 60,
    "backgroundColor": "#a5d8ff",
    "strokeColor": "#1e1e1e",
    "strokeWidth": 2,
    "roundness": { "type": 3 },
    "boundElements": [
      { "id": "service-1-text", "type": "text" }
    ]
  },
  {
    "id": "service-1-text",
    "type": "text",
    "x": 105,
    "y": 115,
    "text": "API Gateway",
    "fontSize": 16,
    "fontFamily": 2,
    "textAlign": "center",
    "containerId": "service-1"
  }
]
```

## Coordinate System

- Origin (0, 0) is at canvas center
- X increases to the right
- Y increases downward
- All measurements in pixels
- Grid snapping: 20px default

## Recommended Spacing

| Element | Spacing |
|---------|---------|
| Between components | 40-80px |
| Arrow gap from shape | 5-10px |
| Text padding in container | 10-20px |
| Group margin | 20px |
| Frame padding | 40px |

## VS Code Settings

```json
{
  "excalidraw.workspaceLibraryPath": ".excalidraw/library.excalidrawlib",
  "excalidraw.theme": "light"
}
```

## When to Use This Skill

- Creating architecture diagrams
- Designing system flowcharts
- Cloud infrastructure diagrams
- Database relationship diagrams
- Network topology diagrams
- Microservices architecture
- Data flow diagrams
- Whiteboard-style documentation

## Best Practices

1. Use consistent colors for element types
2. Maintain grid alignment (20px increments)
3. Group related elements together
4. Use frames to organize sections
5. Keep text readable (16-20px font size)
6. Connect elements with arrows for flow
7. Add labels to all major components
