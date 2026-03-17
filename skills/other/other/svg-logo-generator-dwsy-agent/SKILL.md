---
name: svg-logo-generator
description: Generate high-quality, minimalistic, and geometric SVG logos using Python scripts. Use this skill when users need to create logos, icons, or visual identities with geometric primitives (circles, rects, paths) and specific color schemes. Applies generative design principles with standardized workflows for scalable SVG output.
---

# SVG Logo Generator

## Workflow

Before writing any code, follow these steps:

### 1. Design Analysis
- Analyze the user's request to determine key visual metaphors
- Decide on a color palette using Hex codes
- Plan geometric composition (primitives: circles, rects, paths)

### 2. SVG Configuration
- Define standard canvas size (e.g., 512x512)
- **Always use `viewBox`** for scalability and responsiveness
- Ensure correct XML namespace: `xmlns="http://www.w3.org/2000/svg"`

### 3. Python Implementation
- Write self-contained Python scripts
- **Constraint**: Do NOT rely on external non-standard libraries (like `cairo` or `svgwrite`). Use standard string formatting or `xml.etree.ElementTree`
- Separate styles (CSS within SVG or inline styles) from geometry
- Output/save file as `logo.svg`

## Code Structure

Follow this pattern:

```python
import textwrap

def generate_logo():
    # 1. Configuration
    width, height = 512, 512
    primary_color = "#YOUR_COLOR"
    secondary_color = "#YOUR_COLOR"

    # 2. SVG Header with ViewBox
    svg_header = f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'

    # 3. Geometric Elements
    # Use formatted strings for shapes (Circle, Rect, Path, Polygon)
    shapes = f'<circle cx="{width/2}" cy="{height/2}" r="100" fill="{primary_color}" />'

    # 4. Assembly & Output
    svg_content = f"{svg_header}\n{shapes}\n</svg>"

    with open("logo.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Logo generated: logo.svg")

if __name__ == "__main__":
    generate_logo()
```

## Key Principles

- **Scalability**: Always use `viewBox` instead of fixed `width/height` alone
- **Minimal dependencies**: Use Python standard library only
- **Separation of concerns**: Define styles separately from geometry
- **Geometric primitives**: Focus on circles, rects, paths, polygons
- **Color consistency**: Use defined palette with Hex codes