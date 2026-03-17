---
name: canvas
context: fork
skill: canvas
model: opus
description: Create and edit Obsidian Canvas files for architecture visualization
tags: [activity/architecture, domain/tooling, type/diagram]
---

# /canvas Skill

Create and edit Obsidian Canvas files (.canvas JSON format) for architecture visualization.

## When to Use This Skill

Use when creating or editing `.canvas` files (Obsidian Canvas format):
- Create architecture context diagrams (C4 Level 1)
- Design system landscape maps
- Visualize data flow architectures
- Show AWS infrastructure layouts
- Compare scenarios side-by-side
- Map system dependencies

## ⚠️ CRITICAL: Linter Configuration Warning

**The Obsidian linter will corrupt .canvas files if enabled.** If you have a linter active (prettier, eslint, etc.):
1. **DISABLE it for `.canvas` files**
2. Or **DISABLE it globally** during canvas editing
3. Canvas files use a specific JSON format that lingers may reformat incorrectly

The linter will delete nodes with empty `text` fields and reduce complex diagrams to 2 nodes.

## Canvas JSON Structure

### Correct Format

Every node MUST use `text` property for content (NOT `label`):

```json
{
  "nodes": [
    {
      "id": "unique-id",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 200,
      "height": 100,
      "color": "3",
      "text": "Node Content\nMultiline supported\nWith \\n character"
    }
  ],
  "edges": [
    {
      "id": "edge-id",
      "fromNode": "node-id-1",
      "toNode": "node-id-2",
      "fromSide": "right",
      "toSide": "left",
      "label": "Edge Label"
    }
  ],
  "metadata": {
    "version": "1.0-1.0",
    "frontmatter": {}
  }
}
```

### Property Reference

**Node Properties:**
| Property | Required | Type | Values | Notes |
|----------|----------|------|--------|-------|
| `id` | ✅ | string | Any unique ID | Use kebab-case |
| `type` | ✅ | string | `"text"` | Currently only text type supported |
| `x` | ✅ | number | Any integer | Canvas X coordinate |
| `y` | ✅ | number | Any integer | Canvas Y coordinate |
| `width` | ✅ | number | Any positive int | Node width in pixels |
| `height` | ✅ | number | Any positive int | Node height in pixels |
| `text` | ✅ | string | Any text | **USE THIS FOR NODE CONTENT** (not `label`) |
| `color` | ❌ | string | "1"-"6" | Color: 1=red, 2=orange, 3=yellow, 4=purple, 5=cyan, 6=green |

**Edge Properties:**
| Property | Required | Type | Values |
|----------|----------|------|--------|
| `id` | ✅ | string | Any unique ID |
| `fromNode` | ✅ | string | ID of source node |
| `toNode` | ✅ | string | ID of target node |
| `fromSide` | ✅ | string | "top", "right", "bottom", "left" |
| `toSide` | ✅ | string | "top", "right", "bottom", "left" |
| `label` | ❌ | string | Any text | **USE THIS FOR EDGE LABELS** (not node content) |

**Metadata:**
```json
"metadata": {
  "version": "1.0-1.0",
  "frontmatter": {}
}
```

## Common Mistakes

### ❌ WRONG: Using `label` for node content
```json
{"id":"node1","type":"text","x":0,"y":0,"width":100,"height":50,"label":"Node Text"}
```
Result: Text appears on edges, boxes are empty

### ✅ CORRECT: Using `text` for node content
```json
{"id":"node1","type":"text","x":0,"y":0,"width":100,"height":50,"text":"Node Text"}
```
Result: Text displays inside the box

### ❌ WRONG: Empty `text` field
```json
{"id":"node1","type":"text","x":0,"y":0,"width":100,"height":50,"text":""}
```
Result: Obsidian deletes the node on next edit

### ✅ CORRECT: No empty fields
Only include properties with values. Don't include `text` field if empty.

## Workflow

### Phase 1: Define Canvas Structure
Plan the canvas:
- **Sections/clusters** - Group related nodes (e.g., "SOURCE SYSTEMS", "KAFKA EVENT BUS")
- **Nodes** - Individual boxes with content
- **Edges** - Connections with labels

Example structure:
```
SECTION HEADERS (120px high, wide)
  ↓
MAIN NODES (100+ px high, sized to fit content)
  ↓
EDGES with labels connecting them
```

### Phase 2: Calculate Coordinates
- **X axis**: Left to right (0 → +)
- **Y axis**: Top to bottom (0 → +)
- Group related items with consistent spacing
- Use 20-30px padding between nodes

Example grid:
```
(0,0)    (300,0)    (600,0)    (900,0)
  A        B          C          D

(0,100)  (300,100)  (600,100)  (900,100)
  E        F          G          H
```

### Phase 3: Determine Node Heights
Size nodes based on content:
- **Section headers**: 40px height
- **Simple labels**: 50px height
- **Multi-line (2-3 lines)**: 70px height
- **Multi-line (4+ lines)**: 80-100px height
- **Large info boxes**: 100px+ height

Add ~10-15px padding for text overflow.

### Phase 4: Create JSON
Use `text` property for all node content. Use `label` property for edge labels only.

### Phase 5: Validate & Test
1. Save `.canvas` file
2. Verify JSON syntax: `node -e "JSON.parse(require('fs').readFileSync('file.canvas'))"`
3. Open in Obsidian and verify:
   - All boxes display with text inside (not on edges)
   - Edge labels appear on connections
   - Layout matches intended design
   - Colours display correctly

## Examples from This Vault

All of these use correct JSON Canvas format:

- `Canvas - C4 Context Diagram` - 9 nodes, 9 edges
- `Canvas - System Landscape` - 18 nodes, 14 edges
- `Canvas - Data Flow Diagram` - 22 nodes, 18 edges
- `Canvas - AWS Architecture` - 24 nodes, 11 edges
- `Canvas - Scenario Comparison` - 19 nodes, 2 edges
- `Canvas - Data Platform Data Flow` - 38 nodes, 68 edges

All use `text` property for node content and `label` property for edge labels.

## Color Reference

Canvas supports 6 colors:
- **"1"** - Red (Critical, Production)
- **"2"** - Orange (High Priority, Warning)
- **"3"** - Yellow (Source Systems, Starting Point)
- **"4"** - Purple (Access/Gateway, Tools)
- **"5"** - Cyan (Transformation, Processing)
- **"6"** - Green (Analytics, Destination, Data Lake)

## Size Guidelines

**Width:**
- Section headers: 160-200px (full width of section)
- Small nodes: 100-120px
- Medium nodes: 150-160px
- Large nodes: 200-260px
- Full-width containers: 240-300px+

**Height:**
- Thin header: 40px
- Simple label: 50px
- 2-3 lines: 70px
- 4-5 lines: 80px
- 5+ lines or containers: 100px+

## Testing Checklist

Before considering a canvas file "done":

- [ ] JSON syntax is valid
- [ ] All node content uses `text` property
- [ ] All edge labels use `label` property
- [ ] No empty `text` fields exist
- [ ] File opens in Obsidian without errors
- [ ] All boxes display text inside (not on edges)
- [ ] All edge labels appear on connections
- [ ] Colours display correctly
- [ ] Layout matches intended design
- [ ] Spacing and alignment looks good

## Related Skills

- `/diagram` - Generate diagrams programmatically using Python
- `/scenario-compare` - Create side-by-side scenario comparison canvases
- `/impact-analysis` - Visualize system impact on canvas

## File Naming Convention

```
Canvas - {{Diagram Name}}.canvas
Canvas - C4 Context Diagram.canvas
Canvas - System Landscape.canvas
Canvas - Data Flow Diagram.canvas
Canvas - AWS Architecture.canvas
```

## JSON Validation

Quick validation command:
```bash
node -e "try { JSON.parse(require('fs').readFileSync('file.canvas', 'utf8')); console.log('✓ Valid JSON'); } catch(e) { console.log('✗ Error:', e.message); }"
```

---

**Key Principle:** `text` = node content, `label` = edge labels. Never use `label` for node content.

**Key Warning:** Disable linters before editing `.canvas` files - they corrupt the JSON structure.
