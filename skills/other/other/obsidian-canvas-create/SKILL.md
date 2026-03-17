---
name: obsidian-canvas-create
description: |
  Generates Obsidian .canvas files from intent. Takes a description of what you
  want to visualise and produces valid JSON Canvas — mind maps, flowcharts,
  kanban boards, research canvases, project overviews. Activates on "create
  canvas", "make a board", "visualise", "map out", "mind map", or when spatial
  organisation of ideas is needed.
allowed-tools: |
  bash: ls, find, cat
  file: read, write
---

# Obsidian Canvas Create

<purpose>
Canvas files are JSON. Writing them by hand is painful — you're juggling node
coordinates, edge connections, hex IDs, and layout math. But the format is dead
simple once you know the spec. This skill translates intent ("make a kanban for
my project tasks") into valid .canvas files that open perfectly in Obsidian.
</purpose>

## When To Activate

<triggers>
- User says "create canvas", "make a canvas", "new canvas"
- User says "mind map", "flowchart", "kanban", "board"
- User says "visualise this", "map this out", "diagram this"
- User wants to spatially organise notes, ideas, or processes
- After research or planning that would benefit from visual layout
</triggers>

Do NOT trigger for:
- Mermaid diagrams in markdown (those go in notes, not canvas)
- Editing existing canvas files (read and modify directly)
- Simple lists that don't need spatial layout

## Instructions

### Step 1: Understand the Intent

<intent>
Before generating, clarify what kind of canvas:

| Intent | Canvas Type | Layout |
|--------|-------------|--------|
| Organise ideas | Mind map | Radial from centre |
| Track tasks | Kanban board | Columns left to right |
| Show a process | Flowchart | Top to bottom |
| Gather research | Research canvas | Clusters with links |
| Project overview | Project board | Grouped sections |
| Compare options | Decision canvas | Side by side |

Ask if not obvious: "What kind of layout — mind map, kanban, flowchart, or something else?"
</intent>

### Step 2: Gather Content

<content>
Collect what goes on the canvas:

- **Text nodes:** Ideas, descriptions, notes to write directly on the canvas
- **File nodes:** Existing vault notes to reference (`[[Note Name]]`)
- **Link nodes:** External URLs
- **Groups:** Categories or clusters to visually group nodes

```bash
# If referencing vault notes, verify they exist
find "$VAULT_PATH" -name "note-name.md" 2>/dev/null
```
</content>

### Step 3: Generate the Canvas JSON

<generate>
The JSON Canvas spec (1.0):

```json
{
  "nodes": [],
  "edges": []
}
```

**Node types:**

Text node (content written directly on canvas):
```json
{
  "id": "a1b2c3d4e5f6a7b8",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 250,
  "height": 120,
  "text": "# Heading\n\nContent here with **markdown**"
}
```

File node (reference to a vault note):
```json
{
  "id": "b2c3d4e5f6a7b8c9",
  "type": "file",
  "x": 300,
  "y": 0,
  "width": 250,
  "height": 120,
  "file": "Notes/note-name.md"
}
```

Link node (external URL):
```json
{
  "id": "c3d4e5f6a7b8c9d0",
  "type": "link",
  "x": 600,
  "y": 0,
  "width": 250,
  "height": 120,
  "url": "https://example.com"
}
```

Group node (visual container):
```json
{
  "id": "d4e5f6a7b8c9d0e1",
  "type": "group",
  "x": -20,
  "y": -40,
  "width": 580,
  "height": 200,
  "label": "Group Name"
}
```

**Edges (connections between nodes):**
```json
{
  "id": "e5f6a7b8c9d0e1f2",
  "fromNode": "a1b2c3d4e5f6a7b8",
  "toNode": "b2c3d4e5f6a7b8c9",
  "fromSide": "right",
  "toSide": "left",
  "label": "leads to"
}
```

**ID generation:** 16 lowercase hex characters. Use random generation:
```python
import secrets
node_id = secrets.token_hex(8)  # "a1b2c3d4e5f6a7b8"
```

**Color options:**
- Preset: `"1"` (red), `"2"` (orange), `"3"` (yellow), `"4"` (green), `"5"` (cyan), `"6"` (purple)
- Hex: `"#FF0000"`
</generate>

### Step 4: Layout the Nodes

<layout>
Layout depends on canvas type:

**Mind map (radial):**
```
         [Topic A]
              |
[Topic B] - [Centre] - [Topic C]
              |
         [Topic D]
```
- Centre node at (0, 0)
- Branches radiate: right (400, 0), left (-400, 0), top (0, -250), bottom (0, 250)
- Sub-branches offset further (+400/+250 from parent)

**Kanban (columns):**
```
| Todo (x:0)   | In Progress (x:300) | Done (x:600) |
| Task 1       | Task 3              | Task 5       |
| Task 2       | Task 4              | Task 6       |
```
- Group columns: width 280, spacing 300
- Cards inside: width 240, height 80, y-offset 60 between cards
- First card y offset: 40 below group top

**Flowchart (vertical):**
```
    [Start]        y: 0
       |
    [Step 1]       y: 200
       |
   /      \
[Yes]    [No]      y: 400
```
- Nodes centred on x: 0, spacing y: 200
- Branches: left x: -200, right x: 200
- Edges with fromSide: "bottom", toSide: "top"

**Research canvas (clusters):**
```
[Source Group]     [Notes Group]     [Synthesis Group]
  [Source 1]         [Note 1]          [Summary]
  [Source 2]         [Note 2]
  [Source 3]
```
- Groups spaced 400 apart horizontally
- Nodes inside groups spaced 140 apart vertically

**Recommended node sizes:**
- Standard text/file: 250 x 120
- Small card: 200 x 80
- Large note: 400 x 250
- Group padding: 20px on each side, 40px top (for label)
</layout>

### Step 5: Write the File

<write>
```bash
# Write to vault root or a Canvas/ folder
CANVAS_PATH="$VAULT_PATH/canvas-name.canvas"
```

Write the JSON with proper formatting (2-space indent).

Verify:
```bash
# Validate JSON
python3 -c "import json; json.load(open('$CANVAS_PATH'))" && echo "Valid JSON"
```

Confirm:
```markdown
Canvas created: canvas-name.canvas

Nodes: X text, Y file, Z link
Edges: N connections
Layout: [mind map / kanban / flowchart / research]

Open in Obsidian to view.
```
</write>

## Output Format

```markdown
## Canvas Created

**File:** canvas-name.canvas
**Type:** [mind map / kanban / flowchart / research]
**Nodes:** X (Y text, Z file, W link)
**Edges:** N connections
**Groups:** G groups

Open in Obsidian to view and rearrange.
```

## NEVER

- Generate invalid JSON (always validate)
- Use newline characters literally in text fields (use `\n`)
- Create nodes with overlapping positions
- Skip the layout step (random positions look terrible)
- Use IDs shorter than 16 hex chars
- Reference vault files that don't exist without noting it
- Create canvases with a single node (just use a note)

## ALWAYS

- Generate valid 16-char hex IDs for every node and edge
- Use consistent spacing in layout
- Validate the JSON before confirming
- Use groups to organise related nodes
- Add edge labels where the relationship isn't obvious
- Tell the user to open in Obsidian to view (canvas is visual)

## Example

**User:** "Create a kanban board for my current project tasks"

```json
{
  "nodes": [
    {
      "id": "g001000000000001",
      "type": "group",
      "x": 0, "y": 0,
      "width": 280, "height": 400,
      "label": "Todo",
      "color": "1"
    },
    {
      "id": "g002000000000002",
      "type": "group",
      "x": 300, "y": 0,
      "width": 280, "height": 400,
      "label": "In Progress",
      "color": "3"
    },
    {
      "id": "g003000000000003",
      "type": "group",
      "x": 600, "y": 0,
      "width": 280, "height": 400,
      "label": "Done",
      "color": "4"
    },
    {
      "id": "n001000000000004",
      "type": "text",
      "x": 20, "y": 50,
      "width": 240, "height": 80,
      "text": "# Set up rate limiting\n\nImplement token bucket on API gateway"
    },
    {
      "id": "n002000000000005",
      "type": "text",
      "x": 20, "y": 150,
      "width": 240, "height": 80,
      "text": "# Write integration tests\n\nCover all payment flows"
    },
    {
      "id": "n003000000000006",
      "type": "text",
      "x": 320, "y": 50,
      "width": 240, "height": 80,
      "text": "# API design doc\n\nDocument endpoint contracts"
    },
    {
      "id": "n004000000000007",
      "type": "text",
      "x": 620, "y": 50,
      "width": 240, "height": 80,
      "text": "# Auth middleware\n\nJWT validation complete"
    }
  ],
  "edges": []
}
```

```
Canvas created: project-kanban.canvas

Nodes: 4 task cards in 3 groups
Layout: Kanban (Todo → In Progress → Done)

Open in Obsidian to drag tasks between columns.
```

<failed-attempts>
What DOESN'T work:
- Using literal newlines in JSON text fields — breaks the JSON parser, must use `\n`
- Overlapping node positions — canvas renders but nodes stack on top of each other
- Skipping groups in kanban — cards float without visual columns
- Not validating JSON — one missing comma and the whole canvas won't open
</failed-attempts>
