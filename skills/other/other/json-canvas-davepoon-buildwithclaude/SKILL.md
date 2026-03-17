---
name: json-canvas
category: document-processing
description: Create and edit JSON Canvas files (.canvas) with nodes, edges, groups, and connections. Use when working with .canvas files, creating visual canvases, mind maps, flowcharts, or when the user mentions Canvas files in Obsidian.
---

# JSON Canvas

This skill enables Claude Code to create and edit valid JSON Canvas files (`.canvas`) used in Obsidian and other applications.

## Overview

JSON Canvas is an open file format for infinite canvas data. Canvas files use the `.canvas` extension and contain valid JSON following the JSON Canvas Spec 1.0.

## When to Use This Skill

- Creating or editing .canvas files in Obsidian
- Building visual mind maps or flowcharts
- Creating project boards or planning documents
- Organizing notes visually with connections
- Building diagrams with linked content

## File Structure

A canvas file contains two top-level arrays:

```json
{
  "nodes": [],
  "edges": []
}
```

- `nodes` (optional): Array of node objects
- `edges` (optional): Array of edge objects connecting nodes

## Nodes

Nodes are objects placed on the canvas. There are four node types:
- `text` - Text content with Markdown
- `file` - Reference to files/attachments
- `link` - External URL
- `group` - Visual container for other nodes

### Z-Index Ordering

First node = bottom layer (displayed below others)
Last node = top layer (displayed above others)

### Generic Node Attributes

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `id` | Yes | string | Unique identifier for the node |
| `type` | Yes | string | Node type: `text`, `file`, `link`, or `group` |
| `x` | Yes | integer | X position in pixels |
| `y` | Yes | integer | Y position in pixels |
| `width` | Yes | integer | Width in pixels |
| `height` | Yes | integer | Height in pixels |
| `color` | No | canvasColor | Node color (see Color section) |

### Text Nodes

Text nodes contain Markdown content.

```json
{
  "id": "text1",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 300,
  "height": 150,
  "text": "# Heading\n\nThis is **markdown** content."
}
```

### File Nodes

File nodes reference files or attachments (images, videos, PDFs, notes, etc.)

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `file` | Yes | string | Path to file within the system |
| `subpath` | No | string | Link to heading or block (starts with `#`) |

```json
{
  "id": "file1",
  "type": "file",
  "x": 350,
  "y": 0,
  "width": 400,
  "height": 300,
  "file": "Notes/My Note.md",
  "subpath": "#Heading"
}
```

### Link Nodes

Link nodes display external URLs.

```json
{
  "id": "link1",
  "type": "link",
  "x": 0,
  "y": 200,
  "width": 300,
  "height": 150,
  "url": "https://example.com"
}
```

### Group Nodes

Group nodes are visual containers for organizing other nodes.

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `label` | No | string | Text label for the group |
| `background` | No | string | Path to background image |
| `backgroundStyle` | No | string | Background rendering style |

#### Background Styles

| Value | Description |
|-------|-------------|
| `cover` | Fills entire width and height of node |
| `ratio` | Maintains aspect ratio of background image |
| `repeat` | Repeats image as pattern in both directions |

```json
{
  "id": "group1",
  "type": "group",
  "x": -50,
  "y": -50,
  "width": 800,
  "height": 500,
  "label": "Project Ideas",
  "color": "4"
}
```

## Edges

Edges are lines connecting nodes.

| Attribute | Required | Type | Default | Description |
|-----------|----------|------|---------|-------------|
| `id` | Yes | string | - | Unique identifier for the edge |
| `fromNode` | Yes | string | - | Node ID where connection starts |
| `fromSide` | No | string | - | Side where edge starts |
| `fromEnd` | No | string | `none` | Shape at edge start |
| `toNode` | Yes | string | - | Node ID where connection ends |
| `toSide` | No | string | - | Side where edge ends |
| `toEnd` | No | string | `arrow` | Shape at edge end |
| `color` | No | canvasColor | - | Line color |
| `label` | No | string | - | Text label for the edge |

### Side Values

| Value | Description |
|-------|-------------|
| `top` | Top edge of node |
| `right` | Right edge of node |
| `bottom` | Bottom edge of node |
| `left` | Left edge of node |

### End Shapes

| Value | Description |
|-------|-------------|
| `none` | No endpoint shape |
| `arrow` | Arrow endpoint |

```json
{
  "id": "edge1",
  "fromNode": "text1",
  "fromSide": "right",
  "toNode": "file1",
  "toSide": "left",
  "toEnd": "arrow",
  "label": "references"
}
```

## Colors

The `canvasColor` type supports both hex colors and preset options.

### Hex Colors

```json
{
  "color": "#FF0000"
}
```

### Preset Colors

| Preset | Color |
|--------|-------|
| `"1"` | Red |
| `"2"` | Orange |
| `"3"` | Yellow |
| `"4"` | Green |
| `"5"` | Cyan |
| `"6"` | Purple |

Specific color values for presets are intentionally undefined, allowing applications to use their own brand colors.

## Complete Examples

### Simple Canvas with Text and Connections

```json
{
  "nodes": [
    {
      "id": "idea1",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 250,
      "height": 100,
      "text": "# Main Idea\n\nCore concept goes here"
    },
    {
      "id": "idea2",
      "type": "text",
      "x": 350,
      "y": -50,
      "width": 200,
      "height": 80,
      "text": "## Supporting Point 1\n\nDetails..."
    },
    {
      "id": "idea3",
      "type": "text",
      "x": 350,
      "y": 100,
      "width": 200,
      "height": 80,
      "text": "## Supporting Point 2\n\nMore details..."
    }
  ],
  "edges": [
    {
      "id": "e1",
      "fromNode": "idea1",
      "fromSide": "right",
      "toNode": "idea2",
      "toSide": "left",
      "toEnd": "arrow"
    },
    {
      "id": "e2",
      "fromNode": "idea1",
      "fromSide": "right",
      "toNode": "idea3",
      "toSide": "left",
      "toEnd": "arrow"
    }
  ]
}
```

### Project Board with Groups

```json
{
  "nodes": [
    {
      "id": "todo-group",
      "type": "group",
      "x": 0,
      "y": 0,
      "width": 300,
      "height": 400,
      "label": "To Do",
      "color": "1"
    },
    {
      "id": "progress-group",
      "type": "group",
      "x": 350,
      "y": 0,
      "width": 300,
      "height": 400,
      "label": "In Progress",
      "color": "3"
    },
    {
      "id": "done-group",
      "type": "group",
      "x": 700,
      "y": 0,
      "width": 300,
      "height": 400,
      "label": "Done",
      "color": "4"
    },
    {
      "id": "task1",
      "type": "text",
      "x": 20,
      "y": 50,
      "width": 260,
      "height": 80,
      "text": "## Task 1\n\nDescription of first task"
    },
    {
      "id": "task2",
      "type": "text",
      "x": 370,
      "y": 50,
      "width": 260,
      "height": 80,
      "text": "## Task 2\n\nCurrently working on this"
    },
    {
      "id": "task3",
      "type": "text",
      "x": 720,
      "y": 50,
      "width": 260,
      "height": 80,
      "text": "## Task 3\n\n~~Completed task~~"
    }
  ],
  "edges": []
}
```

### Research Canvas with Files and Links

```json
{
  "nodes": [
    {
      "id": "central",
      "type": "text",
      "x": 200,
      "y": 200,
      "width": 200,
      "height": 100,
      "text": "# Research Topic\n\nMain research question",
      "color": "6"
    },
    {
      "id": "notes1",
      "type": "file",
      "x": 0,
      "y": 0,
      "width": 180,
      "height": 150,
      "file": "Research/Literature Review.md"
    },
    {
      "id": "notes2",
      "type": "file",
      "x": 450,
      "y": 0,
      "width": 180,
      "height": 150,
      "file": "Research/Methodology.md"
    },
    {
      "id": "source1",
      "type": "link",
      "x": 0,
      "y": 350,
      "width": 180,
      "height": 100,
      "url": "https://scholar.google.com"
    },
    {
      "id": "source2",
      "type": "link",
      "x": 450,
      "y": 350,
      "width": 180,
      "height": 100,
      "url": "https://arxiv.org"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "fromNode": "central",
      "toNode": "notes1",
      "toEnd": "arrow",
      "label": "literature"
    },
    {
      "id": "e2",
      "fromNode": "central",
      "toNode": "notes2",
      "toEnd": "arrow",
      "label": "methods"
    },
    {
      "id": "e3",
      "fromNode": "central",
      "toNode": "source1",
      "toEnd": "arrow"
    },
    {
      "id": "e4",
      "fromNode": "central",
      "toNode": "source2",
      "toEnd": "arrow"
    }
  ]
}
```

### Flowchart

```json
{
  "nodes": [
    {
      "id": "start",
      "type": "text",
      "x": 100,
      "y": 0,
      "width": 150,
      "height": 60,
      "text": "**Start**",
      "color": "4"
    },
    {
      "id": "decision",
      "type": "text",
      "x": 75,
      "y": 120,
      "width": 200,
      "height": 80,
      "text": "## Decision\n\nIs condition true?",
      "color": "3"
    },
    {
      "id": "yes-path",
      "type": "text",
      "x": -100,
      "y": 280,
      "width": 150,
      "height": 60,
      "text": "**Yes Path**\n\nDo action A"
    },
    {
      "id": "no-path",
      "type": "text",
      "x": 300,
      "y": 280,
      "width": 150,
      "height": 60,
      "text": "**No Path**\n\nDo action B"
    },
    {
      "id": "end",
      "type": "text",
      "x": 100,
      "y": 420,
      "width": 150,
      "height": 60,
      "text": "**End**",
      "color": "1"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "fromNode": "start",
      "fromSide": "bottom",
      "toNode": "decision",
      "toSide": "top",
      "toEnd": "arrow"
    },
    {
      "id": "e2",
      "fromNode": "decision",
      "fromSide": "left",
      "toNode": "yes-path",
      "toSide": "top",
      "toEnd": "arrow",
      "label": "Yes"
    },
    {
      "id": "e3",
      "fromNode": "decision",
      "fromSide": "right",
      "toNode": "no-path",
      "toSide": "top",
      "toEnd": "arrow",
      "label": "No"
    },
    {
      "id": "e4",
      "fromNode": "yes-path",
      "fromSide": "bottom",
      "toNode": "end",
      "toSide": "left",
      "toEnd": "arrow"
    },
    {
      "id": "e5",
      "fromNode": "no-path",
      "fromSide": "bottom",
      "toNode": "end",
      "toSide": "right",
      "toEnd": "arrow"
    }
  ]
}
```

## ID Generation

Node and edge IDs must be unique strings. Obsidian generates 16-character hexadecimal IDs.

Example format: `a1b2c3d4e5f67890`

## Layout Guidelines

### Positioning

- Coordinates can be negative (canvas extends infinitely)
- `x` increases to the right
- `y` increases downward
- Position refers to top-left corner of node

### Recommended Sizes

| Node Type | Suggested Width | Suggested Height |
|-----------|-----------------|------------------|
| Small text | 200-300 | 80-150 |
| Medium text | 300-450 | 150-300 |
| Large text | 400-600 | 300-500 |
| File preview | 300-500 | 200-400 |
| Link preview | 250-400 | 100-200 |
| Group | Varies | Varies |

### Spacing

- Leave 20-50px padding inside groups
- Space nodes 50-100px apart for readability
- Align nodes to grid (multiples of 10 or 20) for cleaner layouts

## Validation Rules

1. All `id` values must be unique across nodes and edges
2. `fromNode` and `toNode` must reference existing node IDs
3. Required fields must be present for each node type
4. `type` must be one of: `text`, `file`, `link`, `group`
5. `backgroundStyle` must be one of: `cover`, `ratio`, `repeat`
6. `fromSide`, `toSide` must be one of: `top`, `right`, `bottom`, `left`
7. `fromEnd`, `toEnd` must be one of: `none`, `arrow`
8. Color presets must be `"1"` through `"6"` or valid hex color

## References

- [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/)
- [JSON Canvas GitHub](https://github.com/obsidianmd/jsoncanvas)
