---
name: brain-organizer
description: "[Utility] ⛔ MANDATORY skill for ANY Brain canvas operations. AI MUST invoke this skill BEFORE creating/modifying ANY files in Docs/Brain/. Failure to follow = broken canvas."
---

# Brain Organizer

**⛔ MANDATORY workflow for Archon Brain canvas system. AI MUST follow EXACTLY or canvas will NOT work.**

> 📄 **General Document Reference**: [Docs/Index/BRAIN_FORMAT.md](../../../Docs/Index/BRAIN_FORMAT.md)
> AI tools without skill system can also create Brain canvas by referencing the above document.

---

## 🚫 STOP! READ BEFORE ANY FILE OPERATIONS

**DO NOT CREATE ANY FILES until you have:**
1. ✅ Read and understood the Blocking Rules below
2. ✅ Calculated the exact `fileName` from canvas name
3. ✅ Verified ALL folder names will match `fileName`
4. ✅ Planned node positions using Grid Layout (no overlap!)

**If you skip these steps, the canvas WILL BE BROKEN and show "0 nodes" in Archon app.**

---

## ⛔ BLOCKING RULE #1: fileName (ZERO TOLERANCE)

**If canvas `name:` value and folder names don't match, Archon app CANNOT load nodes!**

### fileName Generation Algorithm (Archon App Internal Logic)

```swift
// This is EXACTLY how Archon app generates fileName from name
var fileName: String {
    name.replacingOccurrences(of: " ", with: "-")  // 1. Space → Hyphen
        .lowercased()                               // 2. Lowercase
        .filter { $0.isLetter || $0.isNumber || $0 == "-" }  // 3. Keep only letters/numbers/hyphens
}
```

**Transformation Examples:**

| `name:` value | Generated fileName |
|---------------|-------------------|
| `"My Canvas"` | `my-canvas` |
| `"Aesthetic Canvas: Minimal Diary"` | `aesthetic-canvas-minimal-diary` |
| `"UI Design (v2)"` | `ui-design-v2` |

### Folder Naming Rule (MUST MATCH fileName)

```
Canvas file:    {fileName}.md
Nodes folder:   {fileName}_Nodes/
Connections:    {fileName}_Connections/
Datasheet:      {fileName}_Datasheet/
```

### ✅ CORRECT Example

```yaml
# Canvas file: aesthetic-minimal-diary.md
name: "Aesthetic Minimal Diary"  # fileName = aesthetic-minimal-diary
```
```
Docs/Brain/
├── aesthetic-minimal-diary.md
├── aesthetic-minimal-diary_Nodes/      ✅ MATCH
├── aesthetic-minimal-diary_Connections/
└── aesthetic-minimal-diary_Datasheet/
```

### ❌ WRONG Example (App shows 0 nodes)

```yaml
# Canvas file: aesthetic-minimal-diary-brain.md
name: "Aesthetic Canvas: Minimal Diary Brain"
# fileName = aesthetic-canvas-minimal-diary-brain (colon removed!)
```
```
Docs/Brain/
├── aesthetic-minimal-diary-brain.md
├── aesthetic-minimal-diary-brain_Nodes/  ❌ MISMATCH!
│   # App looks for: aesthetic-canvas-minimal-diary-brain_Nodes
```

### Pre-Creation Checklist (MANDATORY)

**Before creating ANY files, verify:**

1. [ ] Calculate fileName from `name:` value using the algorithm above
2. [ ] Canvas file = `{fileName}.md`
3. [ ] Nodes folder = `{fileName}_Nodes/`
4. [ ] Connections folder = `{fileName}_Connections/`
5. [ ] Datasheet folder = `{fileName}_Datasheet/`
6. [ ] **ALL folder names EXACTLY match the calculated fileName**

---

## ⛔ BLOCKING RULE #2: Node Positioning (NO OVERLAP)

**Nodes MUST be placed on grid. Overlapping nodes = unusable canvas.**

```
Position X = COLUMN × 350
Position Y = ROW × 250
```

**Before creating nodes, assign grid positions:**
```
Node 1: Col 0, Row 0 → position: { x: 0, y: 0 }
Node 2: Col 1, Row 0 → position: { x: 350, y: 0 }
Node 3: Col 0, Row 1 → position: { x: 0, y: 250 }
Node 4: Col 1, Row 1 → position: { x: 350, y: 250 }
```

---

## ⛔ BLOCKING RULE #3: Mandatory Validation

**After creating ALL files, AI MUST verify:**

```
✓ VALIDATION CHECKLIST (AI must print this)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Canvas name:     "{name value}"
Calculated fileName: "{result}"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Canvas file:   {fileName}.md
✓ Nodes folder:  {fileName}_Nodes/ (contains {N} files)
✓ Connections:   {fileName}_Connections/ (if applicable)
✓ Datasheet:     {fileName}_Datasheet/ (if applicable)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Node positions verified: No overlaps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If validation fails, FIX IMMEDIATELY before reporting completion.**

---

## Directory Structure

**⚠️ All folder names MUST use `{fileName}` calculated from canvas `name:` value!**

```
Docs/Brain/
├── {fileName}.md                      # Main canvas file
├── {fileName}_Nodes/                  # Node files directory
│   ├── Node_Heading-Text_{UUID}.md
│   ├── Node_Body-Text_{UUID}.md
│   ├── Node_Post-It_{UUID}.md
│   ├── Node_Image_{UUID}.md
│   ├── Node_Memo_{UUID}.md
│   └── Node_Data-Sheet_{UUID}.md
├── {fileName}_Connections/            # Connection files directory
│   ├── Connection_Arrow_{UUID}.md
│   └── Connection_Normal_{UUID}.md
└── {fileName}_Datasheet/              # Datasheet files directory
    ├── Datasheet_{UUID}.csv
    └── {UUID}.styles.json
```

## Canvas File Format

**File**: `Docs/Brain/{fileName}.md`

```yaml
---
id: "{UUID-UPPERCASE}"
name: "{Human Readable Name}"
viewport_offset: { x: 0, y: 0 }
zoom_level: 1.0
created_at: "{ISO8601 with Z suffix}"
updated_at: "{ISO8601 with Z suffix}"

node_ids:
  - "{node-uuid-1}"

connections:
  - id: "{connection-uuid}"
    start_node_id: "{node-uuid}"
    start_point_id: "{point-uuid}"
    start_point_position: "right"
    start_target_type: "node"
    destination_node_id: "{node-uuid}"
    destination_point_id: "{point-uuid}"
    destination_point_position: "left"
    destination_target_type: "node"
    line_type: "arrow"

groups:
  - id: "{group-uuid}"
    name: "{Group Name}"
    color: "#FF6B6B"
    created_at: "{ISO8601}"
    updated_at: "{ISO8601}"
    node_ids:
      - "{node-uuid}"
---

# {Canvas Name}
```

## Node File Format

**Directory**: `Docs/Brain/{fileName}_Nodes/`

| Node Type | File Prefix | Key Fields |
|-----------|-------------|------------|
| Heading-Text | `Node_Heading-Text_` | type: "heading-text", title, position |
| Body-Text | `Node_Body-Text_` | type: "body-text", title, content, position, size |
| Post-It | `Node_Post-It_` | type: "post-it", title, content, position, size |
| Image | `Node_Image_` | type: "image", title, image_url, position, size |
| Memo | `Node_Memo_` | type: "memo", title, content, position, size |
| Data-Sheet | `Node_Data-Sheet_` | type: "data-sheet", title, datasheet_file, position, size |

### Node Structure

```yaml
---
id: "{UUID}"
type: "{node-type}"
title: "{Title}"
content: "{content}" # if applicable
position: { x: -1000, y: -500 }
size: { width: 260, height: 130 } # if applicable
group_id: "{group-uuid}" # if in group

# Connection Points
connection_points:
  - id: "{point-uuid}"
    position: "top"
    index: 0
  - id: "{point-uuid}"
    position: "right"
    index: 0
    connected_to: "{other-point-uuid}" # if connected
    connection_id: "{connection-uuid}" # if connected
  - id: "{point-uuid}"
    position: "bottom"
    index: 0
  - id: "{point-uuid}"
    position: "left"
    index: 0

# Connections (if any)
connections:
  - connection_id: "{uuid}"
    point_id: "{point-uuid}"
    point_position: "right"
    connected_node_id: "{other-node-uuid}"
    connected_point_id: "{other-point-uuid}"
    role: "start" # or "destination"
    line_type: "arrow" # or "normal"

created_at: "{ISO8601}"
updated_at: "{ISO8601}"
---

# {Title}

{Content}
```

## Connection File Format

**Directory**: `Docs/Brain/{fileName}_Connections/`

```yaml
---
id: "{UUID}"
line_type: "arrow" # or "normal"

# Start Point
start_node_id: "{node-uuid}"
start_point_id: "{point-uuid}"
start_point_position: "right"

# Destination Point
destination_node_id: "{node-uuid}"
destination_point_id: "{point-uuid}"
destination_point_position: "left"

created_at: "{ISO8601}"
updated_at: "{ISO8601}"
---

# Connection: 화살표

Direction: start → destination
```

## Datasheet Format

**Directory**: `Docs/Brain/{fileName}_Datasheet/`

**CSV**: Row 1 = headers, Row 2 = types (Int, Double, String), Row 3+ = data

**Styles JSON**: `"row_col"` format for backgroundColors, formulas, alignments

## Group Colors

| Color | Hex | Use Case |
|-------|-----|----------|
| Red | `#FF6B6B` | Primary category |
| Yellow | `#F7DC6F` | Highlights |
| Green | `#98D8C8` | Completed |
| Teal | `#4ECDC4` | Secondary |
| Purple | `#9B59B6` | Special |
| Blue | `#5DADE2` | References |

## Positioning Strategy (⚠️ Prevent Node Overlap)

**Grid-Based Layout - Use this formula:**

```
Position X = COLUMN × 350
Position Y = ROW × 250
```

**Example for 6 nodes (2 rows × 3 columns):**
```yaml
# Row 0 (Headers)
Node 1: position: { x: 0, y: 0 }
Node 2: position: { x: 350, y: 0 }
Node 3: position: { x: 700, y: 0 }
# Row 1 (Content)
Node 4: position: { x: 0, y: 250 }
Node 5: position: { x: 350, y: 250 }
Node 6: position: { x: 700, y: 250 }
```

**Minimum Spacing:** 300px horizontal, 200px vertical

## Node Size Reference

| Node Type | Width | Height | Note |
|-----------|-------|--------|------|
| Heading-Text | 200 | 40 | - |
| Body-Text | 260 | 130 | - |
| Post-It | 190 | 140 | - |
| Image | 250 | 300 | - |
| Memo | 165 | **40 (minimize)** | ⚠️ Always use minimum height |
| Data-Sheet | 265 | **40 (minimize)** | ⚠️ Always use minimum height |

**⚠️ Memo & Data-Sheet Height Rule:**
Memo and Data-Sheet nodes MUST use minimum height (40). These node types auto-expand when opened in Archon app.

## Best Practices

- UUID: UPPERCASE format (e.g., `E9991F5F-C691-4042-827B-8D76BDF2A5A3`)
- Timestamp: ISO8601 with Z suffix (e.g., `2025-12-15T07:28:18Z`)
- Max 50 nodes per canvas
- Each node has 4 connection points (top, right, bottom, left)

## When to Invoke (AUTOMATIC)

**⚠️ This skill MUST be invoked automatically when:**
- ANY file operation in `Docs/Brain/` directory
- User mentions "Brain", "canvas", "nodes", "캔버스", "브레인"
- Creating visual research output
- Organizing aesthetic references
- Any task that requires structured information visualization

**Trigger Phrases:**
- "Create a Brain canvas for {topic}"
- "Organize {info} in Brain"
- "Add nodes to Brain canvas"
- "Brain-organize {research results}"

## Integration with Aesthetic Skills

| Aesthetic Skill | Brain Output |
|-----------------|--------------|
| `aesthetic-cultural-research` | Image nodes + Memo nodes (analysis) |
| `aesthetic-critic-historian` | Memo nodes (critical notes) |
| `aesthetic-form-composition` | Memo nodes (composition rules) |
| `aesthetic-motion-temporal` | Memo nodes (motion bible) |
| `aesthetic-pattern-miner` | Data-Sheet nodes (pattern library) |

---

## 🚨 FINAL REMINDER: 3 BLOCKING RULES

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ RULE #1: fileName MUST match folder names                   ┃
┃ RULE #2: Nodes MUST use grid positions (X=COL×350, Y=ROW×250)┃
┃ RULE #3: MUST print validation checklist after completion   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

VIOLATION = BROKEN CANVAS (0 nodes, overlapping nodes, unusable)
```