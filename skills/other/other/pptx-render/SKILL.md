---
name: pptx-render
description: >
  Use when the user asks to "render pptx", "show pptx slide",
  "compare with pptx", "pptx to image", "export pptx slide",
  "original slide", "show me the original", "what does the pptx look like",
  or needs to extract a specific PPTX slide's content for visual comparison.
user-invocable: false
---

**Announce:** "I'm using pptx-render to extract PPTX slide content."

# PPTX Slide Inspector

Extracts content from PPTX slides using `python-pptx`. Primary use case: understanding what a PPTX slide contains (shapes, text, positions, images) for comparison against Typst slides, especially diagrams and visual items (VIS-* in content inventories).

## Prerequisites

| Tool | Source |
|------|--------|
| `python-pptx` | pixi project dependency |

## Step 1: Identify the PPTX File and Slide Number

If the user references a content inventory item (e.g., VIS-3, DQ-7), look up its PPTX slide number:

```bash
grep "VIS-3\|the-item-id" inventory/content-inventory-XX.md
```

## Step 2: Extract Slide Shapes

```python
from pptx import Presentation
import json

prs = Presentation('path/to/slides.pptx')
slide = prs.slides[SLIDE_NUM - 1]  # 0-indexed

for shape in slide.shapes:
    info = {
        'name': shape.name,
        'left_in': round(shape.left / 914400, 2),
        'top_in': round(shape.top / 914400, 2),
        'width_in': round(shape.width / 914400, 2),
        'height_in': round(shape.height / 914400, 2),
    }
    if shape.has_text_frame:
        info['text'] = shape.text_frame.text
    if shape.shape_type == 13:  # MSO_SHAPE_TYPE.PICTURE
        info['is_image'] = True
    if shape.has_table:
        info['is_table'] = True
        info['rows'] = len(shape.table.rows)
        info['cols'] = len(shape.table.columns)
    print(json.dumps(info))
```

## Step 3: Extract Images (if needed)

To save embedded images from a slide:

```python
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

prs = Presentation('path/to/slides.pptx')
slide = prs.slides[SLIDE_NUM - 1]

for i, shape in enumerate(slide.shapes):
    if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
        image = shape.image
        ext = image.content_type.split('/')[-1]
        with open(f'/tmp/pptx-slide-{SLIDE_NUM}-img-{i}.{ext}', 'wb') as f:
            f.write(image.blob)
        print(f'Saved image {i}: {image.content_type} ({shape.width/914400:.1f}x{shape.height/914400:.1f} in)')
```

## Step 4: Interpret the Layout

Shape positions use inches from top-left corner:
- `left_in` / `top_in`: position of shape's top-left corner
- Standard slide is 10" × 7.5" (widescreen) or 10" × 5.63" (16:9)
- Shapes with `is_image: true` and generic names ("Picture 5") are usually clipart
- Group shapes may contain sub-shapes (connectors, arrows) — inspect `.shapes` on groups

## Classifying Slide Content

| Shape Pattern | Likely Content |
|--------------|----------------|
| Multiple text boxes + arrows/lines at specific positions | **Substantive diagram** — reproduce in Typst |
| Single large `Picture` shape filling the slide | **Clipart/stock photo** — skip or replace |
| `Table` shape | **Data table** — reproduce as Typst `#table` |
| Text boxes only, no connectors | **Text slide** — no diagram needed |
| Group shapes with AutoShapes inside | **Flow diagram** — extract sub-shapes |

## Quick Reference

```python
# One-liner to dump all shapes from slide N
python3 -c "
from pptx import Presentation; import json
prs = Presentation('PPTX_PATH')
for s in prs.slides[N-1].shapes:
    d = {'name': s.name, 'text': s.text_frame.text if s.has_text_frame else None,
         'pos': f'{s.left/914400:.1f},{s.top/914400:.1f}',
         'size': f'{s.width/914400:.1f}x{s.height/914400:.1f}'}
    print(json.dumps(d))
"
```

## Note on soffice

`soffice --headless` (LibreOffice via nix-darwin) is available but unreliable — it silently fails (returns 0, no output) due to profile lock issues. Use `python-pptx` instead.
