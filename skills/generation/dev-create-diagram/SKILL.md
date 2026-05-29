---
name: dev-create-diagram
description: Create a matplotlib diagram for a forge-gpu lesson using the project's dark theme and visual identity
disable-model-invocation: false
---

Create a diagram or visualization for a forge-gpu lesson using the project's
matplotlib diagram infrastructure. Diagrams increase reader engagement and help
learners understand the topics being taught.

**When to use this skill:**

- A lesson would benefit from a visual explanation of a concept
- You need to show geometric relationships, data flow, memory layout, or
  mathematical concepts visually
- A concept is hard to explain with text alone — a diagram makes it click
- You're writing a lesson with `/dev-math-lesson`, `/dev-engine-lesson`, or
  `/dev-gpu-lesson` and want to add visual aids

**When NOT to use this skill:**

- The concept is a sequential flow better suited to a Mermaid diagram
- The concept is a formula better expressed with KaTeX math notation
- A screenshot of the running program already shows the concept clearly

## Arguments

The user (or you) provides:

- **Lesson key**: e.g. `math/01`, `gpu/04`, `engine/04`
- **Diagram name**: e.g. `vector_addition.png`, `stack_vs_heap.png`
- **Description**: what the diagram should show

If any are missing, infer from context or ask.

## Steps

### 1. Determine the diagram module

Diagram functions are organized by track and lesson number under
`scripts/forge_diagrams/<track>/lesson_NN.py`:

- `scripts/forge_diagrams/math/lesson_NN.py` — math lessons
- `scripts/forge_diagrams/gpu/lesson_NN.py` — GPU lessons
- `scripts/forge_diagrams/engine/lesson_NN.py` — engine lessons
- `scripts/forge_diagrams/ui/lesson_NN.py` — UI lessons
- `scripts/forge_diagrams/assets/lesson_NN.py` — asset pipeline lessons
- `scripts/forge_diagrams/physics/lesson_NN.py` — physics lessons
- `scripts/forge_diagrams/audio/lesson_NN.py` — audio lessons

If a `lesson_NN.py` file does not exist yet for the lesson, create one.

### 2. Write the diagram function

Add a new function to the appropriate per-lesson module following the existing
patterns.

**Required imports and helpers:**

```python
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np

from .._common import FORGE_CMAP, STYLE, draw_vector, save, setup_axes
```

`pe` is needed for the text readability stroke (`path_effects=[pe.withStroke(...)]`)
used throughout diagram code. `FORGE_CMAP` is a custom colormap for heatmaps and
gradient visualizations — import it when using `imshow()` or `pcolormesh()`.

**Theme colors — always use `STYLE` dict values, never hardcoded colors:**

| Key          | Hex       | Use for                                    |
| ------------ | --------- | ------------------------------------------ |
| `bg`         | `#1a1a2e` | Figure and axes background                 |
| `grid`       | `#2a2a4a` | Grid lines, subtle dividers                |
| `axis`       | `#8888aa` | Axis labels, tick labels                   |
| `text`       | `#e0e0f0` | Primary text, titles                       |
| `text_dim`   | `#8888aa` | Secondary text, annotations                |
| `accent1`    | `#4fc3f7` | Cyan — primary vectors, highlights         |
| `accent2`    | `#ff7043` | Orange — secondary vectors, results        |
| `accent3`    | `#66bb6a` | Green — tertiary elements, normals         |
| `accent4`    | `#ab47bc` | Purple — special elements                  |
| `warn`       | `#ffd54f` | Yellow — annotations, important highlights |
| `surface`    | `#252545` | Filled regions, box backgrounds            |

**Function template:**

```python
# ---------------------------------------------------------------------------
# category/NN-lesson-name — diagram_name.png
# ---------------------------------------------------------------------------


def diagram_diagram_name():
    """Brief description of what the diagram shows."""
    fig = plt.figure(figsize=(W, H), facecolor=STYLE["bg"])
    ax = fig.add_subplot(111)
    setup_axes(ax, xlim=(...), ylim=(...))

    # --- Draw content here ---

    # Title with vertical padding (pad >= 12 to avoid crowding content)
    ax.set_title(
        "Diagram Title",
        color=STYLE["text"],
        fontsize=14,
        fontweight="bold",
        pad=12,
    )

    fig.tight_layout()
    save(fig, "category/NN-lesson-name", "diagram_name.png")
```

**Common figure sizes:**

- Vector/math diagrams: `(7, 7)` — square
- Comparison (side-by-side): `(10, 5)` — landscape
- Memory/system layouts: `(10, 8)` — tall
- General concepts: `(8, 7)` to `(10, 7)` — balanced

### 3. Quality checks before saving

After writing the diagram function, verify these requirements:

#### No overlapping labels

Labels must not overlap each other or be drawn on top of lines/arrows. To
prevent overlap:

- Use `label_offset` parameter in `draw_vector()` to shift labels away from
  arrows and other text
- For manually placed `ax.text()` calls, compute positions that avoid other
  text elements
- When labels are dense, reduce `fontsize` or increase figure dimensions
- Test with the actual data — positions that look fine in pseudocode may
  overlap when rendered at the final DPI
- Use `ha` (horizontal alignment) and `va` (vertical alignment) parameters
  to anchor text away from crowded areas
- If two labels would land in the same region, offset one of them and
  optionally add a thin leader line connecting the label to its element

#### No lines drawn across labels

Lines, arrows, and grid elements must not pass through text:

- Draw text elements with `zorder=5` or higher so they render above lines
- Use `path_effects=[pe.withStroke(linewidth=3, foreground=STYLE["bg"])]`
  on all text to create a background halo that visually separates text from
  crossing lines
- Where possible, route lines around label regions rather than through them
- For grid lines that pass behind text, the stroke effect provides sufficient
  clearance

#### Title-to-content vertical padding

There must be visible vertical space between the title and the topmost content
element (data points, arrows, labels, boxes). Crowded titles make diagrams
feel cramped and reduce readability.

- Use `pad=12` or greater in `ax.set_title()` — this adds points of space
  between the title baseline and the axes top edge
- If using `fig.suptitle()` instead, set `y=0.97` or lower and ensure the
  subplot top margin accommodates it (via `fig.subplots_adjust(top=0.90)` or
  `fig.tight_layout(rect=[0, 0, 1, 0.95])`)
- After generating the diagram, visually confirm that the title does not
  touch or crowd the top of the content area

#### Use theme colors exclusively

Every color in the diagram must come from the `STYLE` dictionary:

- Never use hardcoded color strings like `"red"`, `"blue"`, `"#ff0000"`
- Never use matplotlib default colors
- Use accent colors semantically: `accent1` for the primary subject,
  `accent2` for secondary/comparison, `accent3` for tertiary/reference,
  `accent4` for special highlights
- Use `text` for primary labels and `text_dim` for secondary annotations
- Use `surface` for filled regions and `grid` for subtle structural elements

### 4. Register the diagram

Wire up the function so the CLI can find it. Three files need changes:

1. **Per-lesson file** — already done in step 2
2. **Track `__init__.py`** — re-export the function
3. **`__main__.py`** — import and register in `DIAGRAMS` dict

**Example for a new math lesson (math/NN):**

```python
# 1. Function is in scripts/forge_diagrams/math/lesson_NN.py (already written)

# 2. In scripts/forge_diagrams/math/__init__.py — add to __all__ and imports:
from .lesson_NN import diagram_new_concept
# ... and add "diagram_new_concept" to the __all__ list

# 3. In scripts/forge_diagrams/__main__.py:
# Import section:
from .math import diagram_new_concept

# DIAGRAMS dict:
"math/NN": [
    ("new_concept.png", diagram_new_concept),
],

# LESSON_NAMES:
"math/NN": "math/NN-concept-name",
```

### 5. Generate the diagram

Run the diagram generator to produce the PNG:

```bash
python scripts/forge_diagrams --lesson category/NN
```

The output goes to `lessons/category/NN-name/assets/diagram_name.png` at
200 DPI.

### 6. Verify the output

After generating, inspect the diagram for:

- [ ] **No overlapping labels** — all text is readable and distinct
- [ ] **No lines across labels** — text has clear background separation
- [ ] **Title padding** — visible gap between title and content below it
- [ ] **Theme colors** — dark background, no default matplotlib colors visible
- [ ] **Readability** — text is large enough (>= 9pt), contrast is sufficient
- [ ] **Correct content** — the diagram accurately represents the concept

### 7. Reference in the README

Add the diagram to the lesson's `README.md`:

```markdown
![Description of what the diagram shows](assets/diagram_name.png)
```

Place diagrams near the text that explains the concept they illustrate —
before the detailed explanation, not after it. Seeing the visual first helps
the reader build intuition before reading the technical details.

### 8. Run Python linting

Verify the new code passes linting:

```bash
uv run ruff check scripts/forge_diagrams/
uv run ruff format --check scripts/forge_diagrams/
```

Auto-fix if needed:

```bash
uv run ruff check --fix scripts/forge_diagrams/
uv run ruff format scripts/forge_diagrams/
```

## Shared helpers reference

### `setup_axes(ax, xlim=None, ylim=None, grid=True, aspect="equal")`

Applies the dark theme to axes: background color, grid styling, tick colors,
spine colors. Call this on every axes object before drawing.

### `draw_vector(ax, origin, vec, color, label=None, label_offset=(0.15, 0.15), lw=2.5)`

Draws a labeled arrow from `origin` to `origin + vec`. The label gets a
background stroke for readability. Use `label_offset` to prevent overlap with
nearby elements.

### `save(fig, lesson_path, filename)`

Saves the figure to `lessons/{lesson_path}/assets/{filename}` at 200 DPI with
the dark background. Creates the assets directory if needed. Always call this
as the last step — it also closes the figure.

### `FORGE_CMAP`

A custom 4-color colormap (`bg -> accent1 -> accent2 -> warn`) for heatmaps
and gradient visualizations. Use with `imshow()`, `pcolormesh()`, etc.

## Common patterns

### Text with readability stroke

All text over diagram content should use a background stroke:

```python
ax.text(
    x, y, "Label",
    color=STYLE["accent1"],
    fontsize=11,
    fontweight="bold",
    ha="center", va="center",
    path_effects=[pe.withStroke(linewidth=3, foreground=STYLE["bg"])],
)
```

### Legend styling

```python
leg = ax.legend(loc="upper right", fontsize=10, framealpha=0.3,
                edgecolor=STYLE["grid"])
for text in leg.get_texts():
    text.set_color(STYLE["text"])
```

### Multi-panel figures

For side-by-side comparisons, use subplots and apply `setup_axes` to each:

```python
fig = plt.figure(figsize=(10, 5), facecolor=STYLE["bg"])
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
setup_axes(ax1, ...)
setup_axes(ax2, ...)
```

### Filled regions

```python
from matplotlib.patches import Polygon, Rectangle, FancyBboxPatch
# Use STYLE["surface"] for fills, STYLE["accent*"] for borders
```

## Post-creation validation (MANDATORY)

After writing the diagram function, before committing:

1. Read the lesson README section that references this diagram
2. Verify every visual element matches the README's description:
   - If README says "oriented bounding box", the diagram must rotate the box
   - If README shows equation `y = f(x)`, the diagram must plot that exact
     function
   - If README describes 3 pipeline stages, the diagram must show all 3
3. Run the diagram and visually inspect the output
4. Verify the docstring matches what was actually plotted (not copy-pasted
   from a different diagram)

For a thorough cross-check, invoke `/dev-review-diagrams` with the lesson key.

## Common mistakes

- **Hardcoded colors** — Using `"red"` or `"#ff0000"` instead of
  `STYLE["accent2"]`. Every color must come from the theme.
- **Missing stroke on text** — Text without `path_effects` becomes unreadable
  when grid lines or other elements pass behind it.
- **Crowded title** — Using `pad=0` or omitting `pad` in `set_title()`,
  causing the title to sit directly on top of the data.
- **Overlapping labels** — Placing two labels at similar coordinates without
  adjusting offsets. Always check label positions against each other.
- **Wrong module** — Adding a math diagram to a GPU lesson file or vice versa.
  Match the track directory and lesson number to the lesson category.
- **Forgetting to register** — Writing the function but not adding it to the
  `DIAGRAMS` dict in `__main__.py`. The CLI won't find unregistered diagrams.
- **Forgetting to re-export** — Adding the function to `lesson_NN.py` but not
  adding it to the track's `__init__.py` `__all__` list and imports.
- **Forgetting the import** — Adding the entry to `DIAGRAMS` but not importing
  the function at the top of `__main__.py`.
- **Not running linting** — The diagram scripts must pass `ruff check` and
  `ruff format` before committing.
