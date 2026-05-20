---
name: pptx
description: "Professional PowerPoint presentation creation, editing, and automation with support for layouts, templates, charts, images, and formatting. Use when working with .pptx files for: (1) Creating presentations from scratch, (2) Editing existing presentations, (3) Applying templates and themes, (4) Adding charts and visualizations, (5) Bulk slide generation, (6) Presentation automation"
---

# PowerPoint (PPTX) Skill

## Overview

This skill provides comprehensive PowerPoint presentation creation, editing, and automation capabilities using Python's `python-pptx` library. Create professional presentations programmatically with full control over layouts, themes, content, charts, and visualizations.

## Core Capabilities

- **Presentation Creation**: New presentations, templates, metadata, page configuration
- **Slide Management**: Add, duplicate, delete, reorder slides with predefined layouts
- **Content Types**: Text, shapes, images, tables, charts, SmartArt, hyperlinks
- **Design & Formatting**: Themes, color schemes, fonts, fills, borders, effects
- **Advanced Features**: Transitions, animations, embedded objects, video/audio, comments

## Installation

Install the required library:

```bash
pip install python-pptx
# or with uv
uv pip install python-pptx
```

Basic imports:

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
```

For complete library setup and supporting packages (Pillow, pandas, matplotlib), see `references/library-setup.md`.

## Core Workflows

### Workflow 1: Creating a Business Presentation

**Goal:** Create a professional presentation with title slide, content slides, and conclusion.

**Steps:**

1. **Initialize Presentation**
   - Create new presentation object
   - Set slide dimensions (standard 16:9 or 4:3)
   - Configure metadata (title, author, subject, keywords)

2. **Add Title Slide**
   - Use title slide layout (typically `prs.slide_layouts[0]`)
   - Set title and subtitle text
   - Apply formatting (font size, color, bold)

3. **Add Content Slides**
   - Use appropriate layouts (bullet, two-column, title-only, blank)
   - Populate placeholders or add text boxes
   - Format text with proper hierarchy

4. **Add Visual Elements**
   - Insert images with proper sizing and positioning
   - Add charts with formatted data
   - Create tables with cell styling

5. **Save Presentation**
   - Save to .pptx format
   - Verify file creation

**Quick Example:**

```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

# Title slide
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Q4 Business Review"
slide.placeholders[1].text = "Prepared by: Jane Doe\nDate: October 25, 2025"

prs.save('presentation.pptx')
```

See `examples/business-presentation.md` for complete implementation.

### Workflow 2: Adding Charts

**Goal:** Create data visualizations with bar, line, and pie charts.

**Steps:**

1. Prepare chart data using `CategoryChartData`
2. Define categories and series
3. Add chart to slide with positioning
4. Format chart (legend, gridlines, labels)

**Quick Example:**

```python
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

chart_data = CategoryChartData()
chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
chart_data.add_series('2025', (9.5, 10.8, 11.2, 13.1))

chart = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(1), Inches(2), Inches(8), Inches(4.5),
    chart_data
).chart
```

See `examples/chart-examples.md` for all chart types.

### Workflow 3: Working with Images

**Goal:** Add, position, and format images in presentations.

**Steps:**

1. Add image with `slide.shapes.add_picture()`
2. Specify position (left, top) and size (width, height)
3. Calculate centered positioning if needed
4. Optimize images before adding (use Pillow for preprocessing)

**Quick Example:**

```python
# Add image with auto-scaled aspect ratio
pic = slide.shapes.add_picture('logo.png', Inches(1), Inches(1), height=Inches(2))

# Center image on slide
pic.left = int((prs.slide_width - pic.width) / 2)
pic.top = int((prs.slide_height - pic.height) / 2)
```

See `examples/image-handling.md` for advanced techniques.

### Workflow 4: Creating Tables

**Goal:** Add structured data tables with formatting.

**Steps:**

1. Define table dimensions (rows, cols)
2. Add table with positioning
3. Set column widths
4. Populate headers with bold formatting and background color
5. Fill data cells with proper alignment

**Quick Example:**

```python
table = slide.shapes.add_table(4, 3, Inches(1.5), Inches(2), Inches(7), Inches(3)).table

# Header formatting
cell = table.cell(0, 0)
cell.text = "Product"
cell.text_frame.paragraphs[0].font.bold = True
cell.fill.solid()
cell.fill.fore_color.rgb = RGBColor(0, 51, 102)
```

See `examples/table-examples.md` for advanced formatting.

### Workflow 5: Editing Existing Presentations

**Goal:** Modify existing PowerPoint files.

**Steps:**

1. Open presentation with `Presentation('file.pptx')`
2. Iterate through slides to find content
3. Modify text, shapes, or add new elements
4. Save with same or different filename

**Quick Example:**

```python
prs = Presentation('existing.pptx')

# Find and update text
for slide in prs.slides:
    for shape in slide.shapes:
        if hasattr(shape, "text") and "Old Name" in shape.text:
            shape.text = shape.text.replace("Old Name", "New Name")

prs.save('updated.pptx')
```

See `examples/editing-presentations.md` for slide copying and advanced editing.

### Workflow 6: Using Templates

**Goal:** Apply consistent branding with master slides and templates.

**Steps:**

1. Start with template file: `Presentation('template.pptx')`
2. Examine available layouts
3. Add slides using template layouts
4. Apply brand colors consistently

**Quick Example:**

```python
prs = Presentation('corporate_template.pptx')

# Use template layouts
title_slide = prs.slides.add_slide(prs.slide_layouts[0])
content_slide = prs.slides.add_slide(prs.slide_layouts[1])

# Layouts inherit master formatting
prs.save('branded_presentation.pptx')
```

See `references/templates-and-themes.md` for master slide customization.

### Workflow 7: Bulk Slide Generation

**Goal:** Generate multiple slides automatically from data.

**Steps:**

1. Load data from CSV, JSON, or database
2. Create presentation object
3. Iterate through data records
4. Generate one slide per record
5. Populate slide with record data

**Quick Example:**

```python
import pandas as pd

df = pd.read_csv('employee_data.csv')
prs = Presentation()

for _, row in df.iterrows():
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = row['Name']
    # Add employee details to slide body

prs.save('employee_directory.pptx')
```

See `examples/bulk-generation.md` for complete implementations.

## Design Principles

### Color & Typography
- Use 60-30-10 color rule (60% primary, 30% secondary, 10% accent)
- Ensure WCAG AA contrast ratios (4.5:1 minimum)
- Limit to 2 font families maximum
- Minimum body text: 18pt for readability

### Layout & Composition
- Follow rule of thirds for element placement
- Maintain minimum 0.5" margins on all sides
- Limit to 5-7 elements per slide
- Use consistent alignment (snap to grid)

### Visual Hierarchy
- Size indicates importance (larger = more important)
- Use color contrast for emphasis
- Follow Z-pattern for content flow

### Chart Best Practices
- Choose appropriate chart type (bar for comparison, line for trends, pie for parts-of-whole)
- Limit to 3-5 colors maximum
- Always label axes and include data labels
- Use gridlines sparingly

For complete design guidelines, see `references/design-best-practices.md`.

## Common Patterns

### Brand Color Application

```python
BRAND_COLORS = {
    'primary': RGBColor(0, 51, 102),
    'secondary': RGBColor(0, 153, 204),
    'accent': RGBColor(255, 102, 0)
}

# Apply to text
shape.text_frame.paragraphs[0].font.color.rgb = BRAND_COLORS['primary']

# Apply to fill
shape.fill.solid()
shape.fill.fore_color.rgb = BRAND_COLORS['secondary']
```

### Centered Element

```python
def center_shape(shape, prs):
    """Center shape on slide."""
    shape.left = int((prs.slide_width - shape.width) / 2)
    shape.top = int((prs.slide_height - shape.height) / 2)
```

### Text Auto-Fit

```python
from pptx.enum.text import MSO_AUTO_SIZE

text_frame = shape.text_frame
text_frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE  # Shrink text
# or
text_frame.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT  # Expand shape
```

## Troubleshooting Quick Reference

**"ModuleNotFoundError: No module named 'pptx'"**
```bash
pip install python-pptx
```

**"AttributeError: 'NoneType' object has no attribute..."**
- Check placeholder indices: `[p.placeholder_format.idx for p in slide.placeholders]`
- Verify layout has expected placeholders

**Images not found**
- Use absolute paths: `os.path.abspath('image.png')`
- Verify file exists: `os.path.exists(img_path)`

**Text doesn't fit**
- Enable auto-fit: `text_frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE`
- Truncate long text with ellipsis

**File size too large**
- Compress images before adding (use Pillow)
- Resize images to presentation dimensions (1920x1080 max)

For complete troubleshooting, see `references/troubleshooting.md`.

## Helper Scripts

The `scripts/pptx_helper.py` module provides utility functions:

- `create_presentation()`: Initialize with defaults
- `add_title_slide()`: Add formatted title slide
- `add_bullet_slide()`: Add slide with bullet points
- `add_image_slide()`: Add slide with centered image
- `add_chart_slide()`: Add slide with chart
- `add_table_slide()`: Add formatted table
- `apply_brand_colors()`: Apply consistent color scheme
- `optimize_images()`: Batch optimize images

**Usage:**

```python
from scripts.pptx_helper import create_presentation, add_title_slide, add_chart_slide

prs = create_presentation(title="My Presentation")
add_title_slide(prs, "Main Title", "Subtitle")
add_chart_slide(prs, "Sales Data", chart_type='bar',
                categories=['Q1', 'Q2', 'Q3', 'Q4'],
                values=[10, 20, 15, 25])
prs.save('output.pptx')
```

## Additional Resources

### Documentation
- python-pptx: https://python-pptx.readthedocs.io/
- API Reference: https://python-pptx.readthedocs.io/en/latest/api/
- GitHub: https://github.com/scanny/python-pptx

### Detailed References
- [Library Setup & Installation](./references/library-setup.md)
- [Design Best Practices](./references/design-best-practices.md)
- [Templates & Themes](./references/templates-and-themes.md)
- [Advanced Techniques](./references/advanced-techniques.md)
- [Common Pitfalls](./references/troubleshooting.md)

### Examples
- [Complete Business Presentation](./examples/business-presentation.md)
- [Chart Examples (Bar, Line, Pie)](./examples/chart-examples.md)
- [Image Handling](./examples/image-handling.md)
- [Table Examples](./examples/table-examples.md)
- [Editing Existing Presentations](./examples/editing-presentations.md)
- [Bulk Generation from Data](./examples/bulk-generation.md)

### Design Resources
- Microsoft Design Templates: https://templates.office.com/powerpoint
- Color Palette Tools: Coolors.co, Adobe Color
- Free Stock Images: Unsplash, Pexels

## Best Practices Summary

1. Always use templates for consistent branding
2. Optimize images before adding to presentation
3. Limit text on each slide (5-7 bullet points max)
4. Use high contrast for readability
5. Test on target device before presenting
6. Keep file size manageable (<20MB for email)
7. Use speaker notes for detailed talking points
8. Follow 6x6 rule: Max 6 bullets, max 6 words per bullet
9. Validate data before creating charts
10. Use consistent spacing and alignment

---

**When to Use This Skill:**
- Creating business presentations from data
- Automating report generation
- Bulk slide creation from databases
- Template-based presentations
- Educational content with charts/images
- Converting documents to slides
