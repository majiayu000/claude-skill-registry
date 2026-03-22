---
name: visual-mockup
version: 2.1
description: "This skill should be used when the user asks to 'mockup the layout', 'sketch the diagram', 'show me the layout before coding', 'draft the positions', 'quick visual of the layout', 'matplotlib mockup', 'interactive mockup', 'drag and drop layout', 'draw a rough layout', 'prototype the diagram', 'let me arrange the nodes', 'mockup the chart before CeTZ', or when you're about to write a diagram with 4+ nodes or a CeTZ chart and want to confirm the visual with the user first."
user-invocable: false
---

**Announce:** "I'll create a mockup so you can see the layout before I code the real diagram."

## Why This Exists

Diagram code (CeTZ, Fletcher, TikZ) is slow to iterate on — you write coordinates, compile, discover the layout is wrong, rewrite. A 30-second sketch lets the user see and approve the spatial layout *before* any real code gets written. This saves 3-5 compile-fix cycles on complex diagrams.

## When to Use

- Before coding a new diagram with 4+ nodes, regions, or non-trivial arrow routing
- Before coding a CeTZ chart where the data shape matters (stock prices, timelines)
- When the user describes a layout change and you want to confirm before implementing
- When an ASCII sketch isn't enough to convey spatial relationships (overlapping regions, diagonal arrows, nested containers)
- When you and the user are iterating on where things should go

You don't need this for simple diagrams (2-3 nodes in a line). Use your judgment — if the layout is obvious, skip the mockup and go straight to code.

## Choosing a Mode

| Mode | When | Output |
|------|------|--------|
| **Interactive** (default for node diagrams) | Fletcher diagrams, 4+ nodes, precise positioning | Drag-and-drop HTML → Fletcher JSON |
| **Matplotlib** (for charts/plots) | CeTZ charts, stock prices, timelines, data series | Static PNG → iterate data → translate to CeTZ |

**Default to interactive** for node-edge diagrams. Use matplotlib for anything with axes, data series, or time-based plots.

---

## Interactive Mockup (Fletcher Diagrams)

### 1. Gather the Layout

From conversation context or the user's request, identify:
- **Nodes**: labeled boxes with approximate positions
- **Edges**: arrows between nodes, with labels and directionality
- **Regions**: background containers grouping nodes (dashed borders, light fills)
- **Constraints**: "X must be above Y", "no crossing arrows", "these two side by side"

### 2. Generate the Interactive HTML

Write the layout as JSON and run the generator:

```bash
cat > /tmp/layout.json << 'LAYOUT'
{
  "title": "Diagram Name",
  "nodes": [
    {"id": "n1", "label": "Issuer", "x": 200, "y": 100, "color": "#89b4fa"},
    {"id": "n2", "label": "Buyer", "x": 200, "y": 300, "color": "#a6e3a1"}
  ],
  "edges": [
    {"from": "n1", "to": "n2", "label": "§11 claim"}
  ],
  "regions": [
    {"id": "r1", "label": "Primary Market", "x": 140, "y": 60, "w": 250, "h": 280, "color": "#89b4fa"}
  ]
}
LAYOUT
python3 ${SKILL_DIR}/scripts/interactive_mockup.py /tmp/layout.json --open
```

`${SKILL_DIR}` resolves to this skill's base directory (e.g., `skills/visual-mockup`).

The browser opens with a Catppuccin-themed drag-and-drop canvas:
- **Drag** nodes and regions to reposition
- **Drag edge labels** to offset from midpoint; **R / Shift+R** to rotate 15 degrees
- **Double-click** any element to rename its label
- **"+ Node" / "+ Edge" / "+ Region"** buttons to add elements
- **Delete/Backspace** to remove selected element
- **Bottom-right handle** on regions to resize
- **"Export as"** dropdown: Fletcher (grid coords, y-down) or Raw pixels
- **"Copy Layout JSON"** button copies transformed positions to clipboard

**Best for Fletcher diagrams.** The exported grid coords drop directly into `node((x, y), ...)` calls. CeTZ diagrams require manual arrow routing that the mockup can't capture — use matplotlib mode for CeTZ instead.

### 3. Get the Layout Back

Tell the user: "Drag nodes where you want them, select **Fletcher** in the Export dropdown, then click **Copy Layout JSON** and paste it here."

The user pastes JSON with Fletcher grid coordinates. Use these positions directly in `node((x, y), ...)` calls — no coordinate transform needed.

### 4. Iterate if Needed

If the user wants further changes, regenerate with updated JSON and `--open` again. When approved, proceed to real diagram code.

---

## Matplotlib Mockup (CeTZ Charts & Simple Layouts)

### 1. Gather the Data

Identify the chart's data series, axes, annotations, and shaded regions. For node diagrams, identify nodes, edges, regions.

### 2. Generate the Mockup

Write a Python script that uses matplotlib/seaborn to sketch the visual:

**For charts/plots:**
- Plot data series with appropriate line styles
- Add shaded regions (class periods, lookback windows, etc.)
- Add annotations (damage brackets, labels, axis markers)
- Match the target palette if known

**For node diagrams:**
- `matplotlib.patches.FancyBboxPatch` with rounded corners for nodes
- `ax.annotate` with `arrowprops` for edges
- Low-alpha patches with dashed borders for regions

Output to `/tmp/visual-mockup.png` at 150 DPI, then open it:

```python
plt.savefig('/tmp/visual-mockup.png', dpi=150, bbox_inches='tight')
```

```bash
open /tmp/visual-mockup.png
```

### 3. Iterate with the User

Show the mockup and ask if the data shape / layout is right. This is where the value lives — catching problems like "the stock price doesn't bounce back" or "the damage bracket is in the wrong place" takes seconds in matplotlib vs. minutes in CeTZ compile cycles.

When approved, translate to CeTZ. For charts, the data arrays transfer directly — matplotlib and CeTZ use the same coordinate space, just different syntax.

## Style Guide (Matplotlib Mode)

- `figsize=(12, 6)` for side-by-side, `(8, 6)` for single diagrams
- `boxstyle="round,pad=0.1"` for nodes
- Use color to distinguish categories (red for danger/fraud, blue for normal flow)
- `ax.set_aspect('equal')` and `ax.axis('off')` for node diagrams

---

## Red Flags — STOP If You Catch Yourself:

| Action | Why Wrong | Do Instead |
|--------|-----------|------------|
| Spending 10+ minutes polishing the mockup | The user is waiting for a sketch, not a deliverable. Polishing a mockup is anti-helpful — it delays the real diagram. | Get it "good enough to discuss" and open it. 2 minutes max. |
| Adding data, formulas, or precise styling | You're building the real diagram in the wrong tool. The mockup exists to be thrown away. | Boxes, arrows, labels, data shape. That's it. |
| Skipping the mockup because "I know the layout" | You thought that about Morrison too. The user saw crossing arrows you didn't. Skipping creates 3+ failed compile-fix cycles — that's not faster, it's slower. | If 4+ nodes, sketch it. 30 seconds vs. 3 failed compiles. |
| Going straight to CeTZ for a chart | You can't see data shape problems until you compile. Editing CeTZ data arrays blind wastes the user's time on compile-squint-edit cycles. | Mockup in matplotlib first — iterate on data with the user, then translate. |
| Editing CeTZ data arrays "real quick" without mockup | You're gambling that you'll guess the right data shape. The value-line incident: "just shift the prices down" produced a chart that told the wrong story for weeks. | 30-second matplotlib plot catches data shape errors the user can see instantly. |

## What This Skill is NOT

- Not a render-verify loop (use `visual-verify` for that)
- Not a replacement for the actual diagram code
- Not for standalone data visualization (use `ds` workflow for charts/plots)
- Not for pixel-perfect output — it's a spatial sketch for layout approval
