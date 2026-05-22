---
name: beautiful-data-viz
description: Create publication-quality, aesthetically refined charts in Python/Jupyter (matplotlib/seaborn): readable axes, tight whitespace, and curated palettes (categorical/sequential/diverging).
argument-hint: "[medium=notebook|paper|slides] [background=light|dark]"
---

# Beautiful Data Viz

Use this skill whenever the user asks to **create, restyle, or “make nicer”** a data visualization in **Python / Jupyter notebooks**.

## Ethos

Toyplot’s ethos is a good North Star for high-quality plots:

> Always look your best.  
> Share your things.  
> Play well with others.  
> Never tell a lie.

(Reference: https://toyplot.readthedocs.io/en/stable/ethos.html)

## Defaults (when the user doesn’t specify)

- Medium: `notebook`
- Background: `light`
- Library: **matplotlib-first**, optionally use seaborn for theme/palettes
- Output: one crisp figure per cell; include a `savefig` line when useful

## Workflow (follow in order)

1) **Clarify intent (or assume):**
   - What is the single takeaway?
   - Audience + medium (`notebook`, `paper`, `slides`) and whether background is `light`/`dark`
   - Categorical vs continuous variables; number of categories

2) **Pick the simplest correct chart**
   - Prefer: line (time), scatter (relationship), bar/dot (ranking), histogram/density (distribution), heatmap (matrix)
   - Avoid: 3D effects, gratuitous decoration, “rainbow” gradients

3) **Choose palette *type* before choosing colors**
   - **Qualitative** → categorical (hue-based)
   - **Sequential** → numeric intensity (luminance ramp)
   - **Diverging** → numeric with a meaningful midpoint (neutral center)
   - (See: https://seaborn.pydata.org/tutorial/color_palettes.html)

4) **Apply a base style, then customize**
   - Use the helper in **[assets/beautiful_style.py](assets/beautiful_style.py)** (recommended).
   - If you can’t import it, copy/paste the functions into the notebook.

5) **Build the plot with “readability first” mechanics**
   - Use human-friendly units, tick formatting, and concise labels.
   - Limit tick count and prevent overlap.
   - Put the legend where it doesn’t create dead space; prefer direct labels when possible.

6) **Polish for maximum clarity + minimal whitespace**
   - Titles: short title; optional subtitle/caption in smaller text
   - Axes: label with units; use sensible limits and a small margin
   - Spines: remove top/right; lighten remaining
   - Grid: subtle, usually y-grid only; never compete with data
   - Whitespace: use `constrained_layout=True` or `fig.tight_layout()`; export with tight bounding box

7) **Validate like a designer**
   - At target size: do labels remain readable?
   - In grayscale / colorblind-safe mode: is meaning preserved?
   - Are you encoding something with color that should be encoded with position/shape instead?

8) **Export cleanly**
   - Notebooks: ensure high-resolution (retina) rendering when possible
   - Files: `bbox_inches="tight"` and small `pad_inches` for minimal outer whitespace

## Color rules (high-aesthetic, high-clarity)

### Categorical palettes
- Prefer **visually equidistant** colors so categories are easy to distinguish and map to a legend/key.
- If you need a custom palette, choose **very different endpoints** (e.g., warm vs cool) so intermediate colors are distinct.
- If using a brand color, adjust saturation/brightness as needed; hue is what people recognize most.
- Tools:
  - LearnUI “Data Visualization Color Picker” (generates equidistant palettes): https://www.learnui.design/tools/data-color-picker.html
  - Seaborn: `colorblind`, ColorBrewer palettes (e.g., `"Set2"`), or `husl` for many categories: https://seaborn.pydata.org/tutorial/color_palettes.html

### Sequential palettes
- Use perceptually uniform sequential maps for numeric magnitude.
- Seaborn includes `"rocket"`, `"mako"`, `"flare"`, `"crest"` and supports matplotlib maps like `"viridis"` / `"magma"`.
- For lines/points on light backgrounds, avoid maps whose extremes approach white (hard to see).
- Reference: https://seaborn.pydata.org/tutorial/color_palettes.html

### Diverging palettes
- Use when values diverge around a meaningful midpoint (0, baseline, target).
- Prefer a **neutral midpoint**; avoid muddy mid-tones.
- Tool: LearnUI Divergent Scale generator: https://www.learnui.design/tools/data-color-picker.html

## Implementation: quick start

If you can, import and apply the helper:

```python
import sys
from pathlib import Path

# Add the skill directory to sys.path if needed:
# sys.path.append(str(Path("path/to/beautiful-data-viz").resolve()))

from assets.beautiful_style import set_beautiful_style, finalize_axes

set_beautiful_style(medium="notebook", background="light")
```

Then create plots normally (matplotlib or seaborn), and finish with:

```python
finalize_axes(ax, title="...", subtitle="...", tight=True)
```

## Internal references (load only when needed)

- **Design & QA checklist:** [references/checklist.md](references/checklist.md)
- **Palette selection + examples:** [references/palettes.md](references/palettes.md)
- **Copy/paste style helpers:** [assets/beautiful_style.py](assets/beautiful_style.py)
- **Plot recipes (line/bar/scatter/heatmap):** [examples/recipes.md](examples/recipes.md)

## External inspiration / guidance

- Information is Beautiful (visual language inspiration): https://informationisbeautiful.net/
- LearnUI Data Viz Color Picker: https://www.learnui.design/tools/data-color-picker.html
- Berkeley Library design guide (reference): https://guides.lib.berkeley.edu/data-visualization/design
- Toyplot ethos: https://toyplot.readthedocs.io/en/stable/ethos.html
- Seaborn aesthetics + palettes: https://seaborn.pydata.org/
