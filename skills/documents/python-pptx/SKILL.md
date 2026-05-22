---
name: python-pptx
description: Create and manipulate PowerPoint presentations programmatically. Build slide decks with layouts, shapes, charts, tables, and images. Generate data-driven presentations from templates.
version: 1.0.0
category: office-docs
type: skill
capabilities:
  - presentation_creation
  - slide_layouts
  - shape_manipulation
  - chart_generation
  - table_creation
  - image_insertion
  - template_based_generation
  - master_slide_customization
tools:
  - python
  - python-pptx
  - Pillow
tags: [powerpoint, pptx, presentation, slides, charts, office-automation]
platforms: [windows, macos, linux]
related_skills:
  - python-docx
  - openpyxl
  - plotly
---

# Python-pptx PowerPoint Automation Skill

## Overview

Python-pptx is a Python library for creating and updating PowerPoint (.pptx) presentations. This skill covers comprehensive patterns for presentation automation including:

- **Presentation creation** with multiple slide layouts
- **Shape manipulation** including text boxes, images, and geometric shapes
- **Chart generation** for data visualization within slides
- **Table creation** for structured data display
- **Master slide customization** for branding consistency
- **Template-based generation** for consistent presentations
- **Placeholder management** for dynamic content insertion

## When to Use This Skill

### USE when:
- Generating presentations from data automatically
- Creating standardized report presentations
- Building slide decks with consistent branding
- Automating dashboard presentations
- Creating training materials from templates
- Generating client presentations from databases
- Building presentation pipelines for regular reports
- Creating slides with charts and tables from data
- Mass-producing presentations with variable content

### DON'T USE when:
- Need real-time presentation editing (use PowerPoint)
- Creating presentations with complex animations
- Need advanced transitions (limited support)
- Require embedded videos with playback controls
- Need to preserve complex PowerPoint features
- Creating presentations from scratch without Python (use PowerPoint)

## Prerequisites

### Installation

```bash
# Basic installation
pip install python-pptx

# Using uv (recommended)
uv pip install python-pptx

# With image support
pip install python-pptx Pillow

# Full installation for charts
pip install python-pptx Pillow lxml
```

### Verify Installation

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

print("python-pptx installed successfully!")
```

## Core Capabilities

### 1. Basic Presentation Creation

```python
"""
Create a basic PowerPoint presentation with common slide types.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RgbColor
from pptx.enum.shapes import MSO_SHAPE

def create_basic_presentation(output_path: str) -> None:
    """Create a basic presentation with various slide types."""
    # Create presentation
    prs = Presentation()

    # Set slide dimensions (16:9 widescreen)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Slide 1: Title Slide
    title_layout = prs.slide_layouts[0]  # Title slide layout
    slide1 = prs.slides.add_slide(title_layout)

    title = slide1.shapes.title
    subtitle = slide1.placeholders[1]

    title.text = "Q1 2026 Business Review"
    subtitle.text = "Strategic Planning and Performance Analysis"

    # Format title
    for paragraph in title.text_frame.paragraphs:
        paragraph.font.size = Pt(44)
        paragraph.font.bold = True

    # Slide 2: Title and Content
    bullet_layout = prs.slide_layouts[1]  # Title and content
    slide2 = prs.slides.add_slide(bullet_layout)

    title2 = slide2.shapes.title
    body2 = slide2.placeholders[1]

    title2.text = "Key Highlights"

    tf = body2.text_frame
    tf.text = "Revenue grew 15% year-over-year"

    p1 = tf.add_paragraph()
    p1.text = "Customer satisfaction reached 92%"
    p1.level = 0

    p2 = tf.add_paragraph()
    p2.text = "Expanded to 3 new markets"
    p2.level = 0

    p3 = tf.add_paragraph()
    p3.text = "North America"
    p3.level = 1

    p4 = tf.add_paragraph()
    p4.text = "Europe"
    p4.level = 1

    p5 = tf.add_paragraph()
    p5.text = "Asia Pacific"
    p5.level = 1

    # Slide 3: Two Content Slide
    two_content_layout = prs.slide_layouts[3]  # Two content
    slide3 = prs.slides.add_slide(two_content_layout)

    title3 = slide3.shapes.title
    title3.text = "Comparison Overview"

    # Left content
    left_placeholder = slide3.placeholders[1]
    tf_left = left_placeholder.text_frame
    tf_left.text = "Before"
    p = tf_left.add_paragraph()
    p.text = "Manual processes"
    p = tf_left.add_paragraph()
    p.text = "Limited scalability"
    p = tf_left.add_paragraph()
    p.text = "Higher costs"

    # Right content
    right_placeholder = slide3.placeholders[2]
    tf_right = right_placeholder.text_frame
    tf_right.text = "After"
    p = tf_right.add_paragraph()
    p.text = "Automated workflows"
    p = tf_right.add_paragraph()
    p.text = "Unlimited scale"
    p = tf_right.add_paragraph()
    p.text = "Cost reduction"

    # Slide 4: Section Header
    section_layout = prs.slide_layouts[2]  # Section header
    slide4 = prs.slides.add_slide(section_layout)

    title4 = slide4.shapes.title
    title4.text = "Financial Overview"

    # Slide 5: Blank slide with custom shapes
    blank_layout = prs.slide_layouts[6]  # Blank
    slide5 = prs.slides.add_slide(blank_layout)

    # Add custom text box
    left = Inches(0.5)
    top = Inches(0.5)
    width = Inches(12)
    height = Inches(1)

    textbox = slide5.shapes.add_textbox(left, top, width, height)
    tf = textbox.text_frame
    p = tf.paragraphs[0]
    p.text = "Custom Content Slide"
    p.font.size = Pt(32)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER

    # Add shapes
    shapes = slide5.shapes

    # Rectangle
    rect = shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(1), Inches(2),
        Inches(3), Inches(2)
    )
    rect.fill.solid()
    rect.fill.fore_color.rgb = RgbColor(0x44, 0x72, 0xC4)
    rect.text = "Feature A"

    # Rounded rectangle
    rounded = shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(5), Inches(2),
        Inches(3), Inches(2)
    )
    rounded.fill.solid()
    rounded.fill.fore_color.rgb = RgbColor(0x70, 0xAD, 0x47)
    rounded.text = "Feature B"

    # Oval
    oval = shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(9), Inches(2),
        Inches(3), Inches(2)
    )
    oval.fill.solid()
    oval.fill.fore_color.rgb = RgbColor(0xED, 0x7D, 0x31)
    oval.text = "Feature C"

    # Save presentation
    prs.save(output_path)
    print(f"Presentation saved to {output_path}")


create_basic_presentation("basic_presentation.pptx")
```

### 2. Advanced Text Formatting

```python
"""
Advanced text formatting with runs, fonts, and paragraph styles.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RgbColor
from pptx.oxml.ns import nsmap

def create_formatted_presentation(output_path: str) -> None:
    """Create presentation with advanced text formatting."""
    prs = Presentation()

    # Slide with formatted text
    slide_layout = prs.slide_layouts[6]  # Blank
    slide = prs.slides.add_slide(slide_layout)

    # Title with formatting
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.3),
        Inches(12), Inches(1)
    )
    tf = title_box.text_frame

    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER

    # Multiple runs with different formatting
    run1 = p.add_run()
    run1.text = "Quarterly "
    run1.font.size = Pt(40)
    run1.font.bold = True
    run1.font.color.rgb = RgbColor(0x2F, 0x54, 0x96)

    run2 = p.add_run()
    run2.text = "Performance"
    run2.font.size = Pt(40)
    run2.font.bold = True
    run2.font.color.rgb = RgbColor(0x70, 0xAD, 0x47)

    run3 = p.add_run()
    run3.text = " Report"
    run3.font.size = Pt(40)
    run3.font.bold = True
    run3.font.color.rgb = RgbColor(0x2F, 0x54, 0x96)

    # Formatted paragraph with various styles
    content_box = slide.shapes.add_textbox(
        Inches(0.75), Inches(1.5),
        Inches(11.5), Inches(5)
    )
    tf = content_box.text_frame
    tf.word_wrap = True

    # Paragraph 1: Bold heading
    p1 = tf.paragraphs[0]
    p1.text = "Executive Summary"
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.space_after = Pt(12)

    # Paragraph 2: Normal text
    p2 = tf.add_paragraph()
    p2.text = (
        "This quarter demonstrated strong performance across all metrics. "
        "Revenue increased by 15% year-over-year, driven by expansion in "
        "key markets and improved customer retention."
    )
    p2.font.size = Pt(16)
    p2.space_after = Pt(18)
    p2.line_spacing = 1.5

    # Paragraph 3: Highlighted text
    p3 = tf.add_paragraph()
    p3.text = "Key Achievement: "
    p3.font.size = Pt(18)
    p3.font.bold = True
    p3.font.color.rgb = RgbColor(0xC0, 0x00, 0x00)

    run = p3.add_run()
    run.text = "Achieved 120% of quarterly target"
    run.font.size = Pt(18)
    run.font.italic = True

    # Paragraph 4: Subscript and superscript
    p4 = tf.add_paragraph()
    p4.space_before = Pt(18)

    run = p4.add_run()
    run.text = "Formula example: H"
    run.font.size = Pt(16)

    sub = p4.add_run()
    sub.text = "2"
    sub.font.size = Pt(12)
    sub.font._element.set(
        '{http://schemas.openxmlformats.org/drawingml/2006/main}baseline', '-25000'
    )

    run = p4.add_run()
    run.text = "O and E=mc"
    run.font.size = Pt(16)

    sup = p4.add_run()
    sup.text = "2"
    sup.font.size = Pt(12)
    sup.font._element.set(
        '{http://schemas.openxmlformats.org/drawingml/2006/main}baseline', '30000'
    )

    # Bullet list with custom formatting
    bullet_box = slide.shapes.add_textbox(
        Inches(0.75), Inches(5),
        Inches(11.5), Inches(2)
    )
    tf = bullet_box.text_frame

    p = tf.paragraphs[0]
    p.text = "Key Metrics:"
    p.font.size = Pt(18)
    p.font.bold = True

    bullets = [
        ("Revenue", "$12.5M", "up 15%"),
        ("Customers", "45,000", "up 8%"),
        ("NPS Score", "72", "up 5 points"),
    ]

    for metric, value, change in bullets:
        p = tf.add_paragraph()
        p.level = 0

        run = p.add_run()
        run.text = f"{metric}: "
        run.font.size = Pt(14)
        run.font.bold = True

        run = p.add_run()
        run.text = f"{value} "
        run.font.size = Pt(14)

        run = p.add_run()
        run.text = f"({change})"
        run.font.size = Pt(14)
        run.font.color.rgb = RgbColor(0x00, 0x80, 0x00)

    prs.save(output_path)
    print(f"Formatted presentation saved to {output_path}")


create_formatted_presentation("formatted_presentation.pptx")
```

### 3. Chart Generation

```python
"""
Create various chart types in PowerPoint presentations.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.chart.data import CategoryChartData, ChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.dml.color import RgbColor

def create_chart_presentation(output_path: str) -> None:
    """Create presentation with various chart types."""
    prs = Presentation()

    # Slide 1: Column Chart
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title only
    slide.shapes.title.text = "Quarterly Revenue"

    # Chart data
    chart_data = CategoryChartData()
    chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
    chart_data.add_series('2025', (1200, 1400, 1600, 1800))
    chart_data.add_series('2026', (1500, 1750, 2000, 2200))

    # Add chart
    x, y, cx, cy = Inches(1), Inches(1.5), Inches(11), Inches(5.5)
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        x, y, cx, cy,
        chart_data
    ).chart

    # Customize chart
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM
    chart.legend.include_in_layout = False

    # Style the chart
    plot = chart.plots[0]
    plot.has_data_labels = True
    data_labels = plot.data_labels
    data_labels.font.size = Pt(10)
    data_labels.number_format = '$#,##0'

    # Slide 2: Line Chart
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Monthly Trend Analysis"

    chart_data = CategoryChartData()
    chart_data.categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    chart_data.add_series('Sales', (100, 120, 140, 135, 160, 180))
    chart_data.add_series('Target', (110, 120, 130, 140, 150, 160))

    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.LINE_MARKERS,
        Inches(1), Inches(1.5), Inches(11), Inches(5.5),
        chart_data
    ).chart

    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM

    # Slide 3: Pie Chart
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Market Share Distribution"

    chart_data = CategoryChartData()
    chart_data.categories = ['Product A', 'Product B', 'Product C', 'Other']
    chart_data.add_series('Share', (35, 30, 25, 10))

    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.PIE,
        Inches(3), Inches(1.5), Inches(7), Inches(5.5),
        chart_data
    ).chart

    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.RIGHT

    plot = chart.plots[0]
    plot.has_data_labels = True
    data_labels = plot.data_labels
    data_labels.show_percentage = True
    data_labels.show_value = False
    data_labels.font.size = Pt(12)

    # Slide 4: Bar Chart (Horizontal)
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Regional Performance"

    chart_data = CategoryChartData()
    chart_data.categories = ['North', 'South', 'East', 'West', 'Central']
    chart_data.add_series('Revenue', (450, 380, 520, 420, 310))

    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED,
        Inches(1), Inches(1.5), Inches(11), Inches(5.5),
        chart_data
    ).chart

    chart.has_legend = False
    plot = chart.plots[0]
    plot.has_data_labels = True
    plot.data_labels.font.size = Pt(11)
    plot.data_labels.number_format = '$#,##0K'

    # Slide 5: Stacked Column Chart
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Product Mix by Quarter"

    chart_data = CategoryChartData()
    chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
    chart_data.add_series('Hardware', (400, 450, 500, 550))
    chart_data.add_series('Software', (300, 350, 400, 450))
    chart_data.add_series('Services', (200, 250, 300, 350))

    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_STACKED,
        Inches(1), Inches(1.5), Inches(11), Inches(5.5),
        chart_data
    ).chart

    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM

    # Slide 6: Doughnut Chart
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Budget Allocation"

    chart_data = CategoryChartData()
    chart_data.categories = ['R&D', 'Marketing', 'Operations', 'Admin']
    chart_data.add_series('Budget', (40, 25, 25, 10))

    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.DOUGHNUT,
        Inches(3), Inches(1.5), Inches(7), Inches(5.5),
        chart_data
    ).chart

    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.RIGHT

    prs.save(output_path)
    print(f"Chart presentation saved to {output_path}")


create_chart_presentation("chart_presentation.pptx")
```

### 4. Table Creation

```python
"""
Create and format tables in PowerPoint presentations.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RgbColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml
from typing import List, Any

def set_cell_color(cell, color_hex: str) -> None:
    """Set cell background color."""
    cell.fill.solid()
    cell.fill.fore_color.rgb = RgbColor(
        int(color_hex[0:2], 16),
        int(color_hex[2:4], 16),
        int(color_hex[4:6], 16)
    )


def create_table_slide(
    prs: Presentation,
    title: str,
    headers: List[str],
    data: List[List[Any]],
    col_widths: List[float] = None
) -> None:
    """Create a slide with a formatted table."""
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title only
    slide.shapes.title.text = title

    rows = len(data) + 1  # +1 for header
    cols = len(headers)

    # Default column widths
    if col_widths is None:
        total_width = 11
        col_widths = [total_width / cols] * cols

    # Create table
    table_width = sum(col_widths)
    left = Inches((13.333 - table_width) / 2)  # Center table
    top = Inches(1.8)
    width = Inches(table_width)
    height = Inches(0.5 * rows)

    table = slide.shapes.add_table(rows, cols, left, top, width, height).table

    # Set column widths
    for i, w in enumerate(col_widths):
        table.columns[i].width = Inches(w)

    # Style header row
    for i, header in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = header
        set_cell_color(cell, '2F5496')

        # Format text
        para = cell.text_frame.paragraphs[0]
        para.font.bold = True
        para.font.size = Pt(12)
        para.font.color.rgb = RgbColor(255, 255, 255)
        para.alignment = PP_ALIGN.CENTER
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE

    # Add data rows
    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, value in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.text = str(value)

            # Alternate row colors
            if row_idx % 2 == 0:
                set_cell_color(cell, 'D6DCE5')

            # Format text
            para = cell.text_frame.paragraphs[0]
            para.font.size = Pt(11)
            para.alignment = PP_ALIGN.CENTER
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE


def create_table_presentation(output_path: str) -> None:
    """Create presentation with various table examples."""
    prs = Presentation()

    # Simple data table
    headers = ['Product', 'Q1', 'Q2', 'Q3', 'Q4', 'Total']
    data = [
        ['Widget A', '$150K', '$180K', '$220K', '$250K', '$800K'],
        ['Widget B', '$80K', '$95K', '$110K', '$130K', '$415K'],
        ['Widget C', '$200K', '$220K', '$260K', '$290K', '$970K'],
        ['Total', '$430K', '$495K', '$590K', '$670K', '$2.19M'],
    ]

    create_table_slide(
        prs,
        "Quarterly Sales Summary",
        headers,
        data,
        col_widths=[2, 1.5, 1.5, 1.5, 1.5, 1.5]
    )

    # Comparison table
    headers = ['Feature', 'Basic Plan', 'Pro Plan', 'Enterprise']
    data = [
        ['Users', '5', '25', 'Unlimited'],
        ['Storage', '10 GB', '100 GB', '1 TB'],
        ['Support', 'Email', '24/7 Chat', 'Dedicated'],
        ['Price/mo', '$9', '$29', '$99'],
    ]

    create_table_slide(
        prs,
        "Pricing Comparison",
        headers,
        data,
        col_widths=[3, 2.5, 2.5, 2.5]
    )

    # Schedule/Timeline table
    headers = ['Phase', 'Start', 'End', 'Status', 'Owner']
    data = [
        ['Planning', 'Jan 1', 'Jan 15', 'Complete', 'Team A'],
        ['Development', 'Jan 16', 'Mar 31', 'In Progress', 'Team B'],
        ['Testing', 'Apr 1', 'Apr 30', 'Pending', 'Team C'],
        ['Launch', 'May 1', 'May 15', 'Pending', 'Team D'],
    ]

    create_table_slide(
        prs,
        "Project Timeline",
        headers,
        data,
        col_widths=[2.5, 1.5, 1.5, 2, 2]
    )

    prs.save(output_path)
    print(f"Table presentation saved to {output_path}")


create_table_presentation("table_presentation.pptx")
```

### 5. Image and Shape Manipulation

```python
"""
Add and manipulate images and shapes in presentations.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RgbColor
from pathlib import Path
from io import BytesIO
from typing import Tuple

def add_image_with_border(
    slide,
    image_path: str,
    left: float,
    top: float,
    width: float = None,
    height: float = None
) -> None:
    """Add image with optional border effect."""
    if Path(image_path).exists():
        pic = slide.shapes.add_picture(
            image_path,
            Inches(left), Inches(top),
            Inches(width) if width else None,
            Inches(height) if height else None
        )
        # Add line border
        pic.line.color.rgb = RgbColor(0, 0, 0)
        pic.line.width = Pt(1)


def create_arrow_connector(
    slide,
    start: Tuple[float, float],
    end: Tuple[float, float],
    color: str = "4472C4"
) -> None:
    """Create an arrow connector between two points."""
    connector = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT,
        Inches(start[0]), Inches(start[1]),
        Inches(end[0]), Inches(end[1])
    )

    connector.line.color.rgb = RgbColor(
        int(color[0:2], 16),
        int(color[2:4], 16),
        int(color[4:6], 16)
    )
    connector.line.width = Pt(2)


def create_shape_presentation(output_path: str) -> None:
    """Create presentation with shapes and connectors."""
    prs = Presentation()

    # Slide 1: Process Flow with Shapes
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank

    # Add title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.3),
        Inches(12), Inches(0.8)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Development Process Flow"
    p.font.size = Pt(32)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER

    # Process steps
    steps = [
        ("Requirements", "4472C4"),
        ("Design", "70AD47"),
        ("Development", "ED7D31"),
        ("Testing", "5B9BD5"),
        ("Deployment", "7030A0"),
    ]

    y_pos = 2.5
    x_positions = [1, 3.5, 6, 8.5, 11]

    for i, (step, color) in enumerate(steps):
        # Add shape
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x_positions[i]), Inches(y_pos),
            Inches(2), Inches(1)
        )

        shape.fill.solid()
        shape.fill.fore_color.rgb = RgbColor(
            int(color[0:2], 16),
            int(color[2:4], 16),
            int(color[4:6], 16)
        )

        # Add text
        tf = shape.text_frame
        p = tf.paragraphs[0]
        p.text = step
        p.font.color.rgb = RgbColor(255, 255, 255)
        p.font.bold = True
        p.font.size = Pt(14)
        p.alignment = PP_ALIGN.CENTER
        shape.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

        # Add arrow to next step
        if i < len(steps) - 1:
            arrow = slide.shapes.add_shape(
                MSO_SHAPE.RIGHT_ARROW,
                Inches(x_positions[i] + 2.1), Inches(y_pos + 0.35),
                Inches(0.3), Inches(0.3)
            )
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = RgbColor(128, 128, 128)

    # Slide 2: Organization Chart Style
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.3),
        Inches(12), Inches(0.8)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Team Structure"
    p.font.size = Pt(32)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER

    # CEO box
    ceo = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(5.5), Inches(1.5),
        Inches(2.5), Inches(1)
    )
    ceo.fill.solid()
    ceo.fill.fore_color.rgb = RgbColor(0x2F, 0x54, 0x96)
    ceo.text = "CEO\nJohn Smith"
    for para in ceo.text_frame.paragraphs:
        para.font.color.rgb = RgbColor(255, 255, 255)
        para.font.size = Pt(12)
        para.alignment = PP_ALIGN.CENTER

    # Department heads
    departments = [
        ("Engineering\nAlice Chen", 1.5),
        ("Marketing\nBob Wilson", 4.5),
        ("Sales\nCarol Davis", 7.5),
        ("Operations\nDave Brown", 10.5),
    ]

    for name, x_pos in departments:
        box = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(x_pos), Inches(3.5),
            Inches(2.5), Inches(1)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = RgbColor(0x5B, 0x9B, 0xD5)
        box.text = name
        for para in box.text_frame.paragraphs:
            para.font.color.rgb = RgbColor(255, 255, 255)
            para.font.size = Pt(11)
            para.alignment = PP_ALIGN.CENTER

    # Slide 3: Callout Shapes
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.3),
        Inches(12), Inches(0.8)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Key Callouts"
    p.font.size = Pt(32)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER

    # Callout shapes
    callout1 = slide.shapes.add_shape(
        MSO_SHAPE.OVAL_CALLOUT,
        Inches(1), Inches(2),
        Inches(3.5), Inches(2)
    )
    callout1.fill.solid()
    callout1.fill.fore_color.rgb = RgbColor(0xFF, 0xEB, 0x84)
    callout1.text = "Important!\nReview by Friday"
    for para in callout1.text_frame.paragraphs:
        para.font.size = Pt(14)
        para.alignment = PP_ALIGN.CENTER

    callout2 = slide.shapes.add_shape(
        MSO_SHAPE.CLOUD_CALLOUT,
        Inches(5), Inches(2),
        Inches(3.5), Inches(2)
    )
    callout2.fill.solid()
    callout2.fill.fore_color.rgb = RgbColor(0xC6, 0xEF, 0xCE)
    callout2.text = "Great idea!\nLet's discuss"
    for para in callout2.text_frame.paragraphs:
        para.font.size = Pt(14)
        para.alignment = PP_ALIGN.CENTER

    callout3 = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGULAR_CALLOUT,
        Inches(9), Inches(2),
        Inches(3.5), Inches(2)
    )
    callout3.fill.solid()
    callout3.fill.fore_color.rgb = RgbColor(0xFF, 0xC7, 0xCE)
    callout3.text = "Warning!\nDeadline approaching"
    for para in callout3.text_frame.paragraphs:
        para.font.size = Pt(14)
        para.alignment = PP_ALIGN.CENTER

    prs.save(output_path)
    print(f"Shape presentation saved to {output_path}")


create_shape_presentation("shape_presentation.pptx")
```

### 6. Template-Based Generation

```python
"""
Generate presentations from templates with placeholder replacement.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE_TYPE
from typing import Dict, Any, List
from pathlib import Path
from copy import deepcopy

def replace_text_in_shapes(slide, replacements: Dict[str, str]) -> None:
    """Replace placeholder text in all shapes on a slide."""
    for shape in slide.shapes:
        if shape.has_text_frame:
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    for key, value in replacements.items():
                        if f'{{{{{key}}}}}' in run.text:
                            run.text = run.text.replace(f'{{{{{key}}}}}', str(value))

        if shape.has_table:
            for row in shape.table.rows:
                for cell in row.cells:
                    for paragraph in cell.text_frame.paragraphs:
                        for run in paragraph.runs:
                            for key, value in replacements.items():
                                if f'{{{{{key}}}}}' in run.text:
                                    run.text = run.text.replace(
                                        f'{{{{{key}}}}}',
                                        str(value)
                                    )


def generate_from_template(
    template_path: str,
    output_path: str,
    data: Dict[str, Any]
) -> None:
    """Generate presentation from template with data substitution."""
    prs = Presentation(template_path)

    for slide in prs.slides:
        replace_text_in_shapes(slide, data)

    prs.save(output_path)
    print(f"Generated presentation: {output_path}")


def create_monthly_report_template(output_path: str) -> None:
    """Create a template for monthly reports."""
    prs = Presentation()

    # Title slide with placeholders
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Title placeholder
    title = slide.shapes.add_textbox(
        Inches(0.5), Inches(2.5),
        Inches(12), Inches(1.5)
    )
    tf = title.text_frame
    p = tf.paragraphs[0]
    p.text = "{{report_title}}"
    p.font.size = Pt(44)
    p.font.bold = True
    p.alignment = 1  # Center

    # Subtitle
    subtitle = slide.shapes.add_textbox(
        Inches(0.5), Inches(4),
        Inches(12), Inches(1)
    )
    tf = subtitle.text_frame
    p = tf.paragraphs[0]
    p.text = "{{report_period}}"
    p.font.size = Pt(24)
    p.alignment = 1

    # Summary slide
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    title = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.5),
        Inches(12), Inches(1)
    )
    tf = title.text_frame
    p = tf.paragraphs[0]
    p.text = "Executive Summary"
    p.font.size = Pt(32)
    p.font.bold = True

    # Key metrics boxes
    metrics = [
        ("Revenue", "{{revenue}}"),
        ("Customers", "{{customers}}"),
        ("Growth", "{{growth}}"),
    ]

    for i, (label, placeholder) in enumerate(metrics):
        x = 1 + (i * 4)

        # Label
        label_box = slide.shapes.add_textbox(
            Inches(x), Inches(2),
            Inches(3), Inches(0.5)
        )
        tf = label_box.text_frame
        p = tf.paragraphs[0]
        p.text = label
        p.font.size = Pt(14)
        p.alignment = 1

        # Value box
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(2.5),
            Inches(3), Inches(1.5)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = RgbColor(0x44, 0x72, 0xC4)
        tf = shape.text_frame
        p = tf.paragraphs[0]
        p.text = placeholder
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = RgbColor(255, 255, 255)
        p.alignment = 1

    prs.save(output_path)
    print(f"Template saved: {output_path}")


def batch_generate_presentations(
    template_path: str,
    data_list: List[Dict[str, Any]],
    output_dir: str
) -> List[str]:
    """Generate multiple presentations from template."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    generated = []

    for data in data_list:
        filename = f"{data.get('filename', 'presentation')}.pptx"
        file_path = output_path / filename

        generate_from_template(template_path, str(file_path), data)
        generated.append(str(file_path))

    return generated


# Example usage:
# create_monthly_report_template('monthly_template.pptx')
#
# data = {
#     'report_title': 'Monthly Performance Report',
#     'report_period': 'January 2026',
#     'revenue': '$12.5M',
#     'customers': '45,000',
#     'growth': '+15%'
# }
# generate_from_template('monthly_template.pptx', 'january_report.pptx', data)
```

## Integration Examples

### Data-Driven Presentation from Database

```python
"""
Generate presentations from database queries.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
import sqlite3
from datetime import datetime

def generate_database_presentation(
    db_path: str,
    output_path: str
) -> None:
    """Generate presentation from database data."""
    conn = sqlite3.connect(db_path)
    prs = Presentation()

    # Title slide
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "Sales Analysis Report"
    slide.placeholders[1].text = f"Generated: {datetime.now().strftime('%Y-%m-%d')}"

    # Query 1: Sales by region
    cursor = conn.execute("""
        SELECT region, SUM(amount) as total
        FROM sales
        GROUP BY region
        ORDER BY total DESC
    """)
    regions = cursor.fetchall()

    # Create chart slide
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Sales by Region"

    chart_data = CategoryChartData()
    chart_data.categories = [r[0] for r in regions]
    chart_data.add_series('Sales', [r[1] for r in regions])

    slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED,
        Inches(1), Inches(1.5), Inches(11), Inches(5.5),
        chart_data
    )

    # Query 2: Monthly trend
    cursor = conn.execute("""
        SELECT strftime('%Y-%m', date) as month, SUM(amount)
        FROM sales
        GROUP BY month
        ORDER BY month
    """)
    monthly = cursor.fetchall()

    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Monthly Sales Trend"

    chart_data = CategoryChartData()
    chart_data.categories = [m[0] for m in monthly]
    chart_data.add_series('Sales', [m[1] for m in monthly])

    slide.shapes.add_chart(
        XL_CHART_TYPE.LINE_MARKERS,
        Inches(1), Inches(1.5), Inches(11), Inches(5.5),
        chart_data
    )

    conn.close()
    prs.save(output_path)
    print(f"Database presentation saved: {output_path}")
```

### Pandas DataFrame to Presentation

```python
"""
Generate presentations from pandas DataFrames.
"""
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RgbColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

def dataframe_to_slide(
    prs: Presentation,
    df: pd.DataFrame,
    title: str,
    max_rows: int = 15
) -> None:
    """Add DataFrame as table to presentation."""
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = title

    # Limit rows if necessary
    display_df = df.head(max_rows)
    rows, cols = display_df.shape
    rows += 1  # For header

    # Calculate dimensions
    table_width = min(cols * 1.5, 12)
    left = Inches((13.333 - table_width) / 2)

    table = slide.shapes.add_table(
        rows, cols,
        left, Inches(1.5),
        Inches(table_width), Inches(0.4 * rows)
    ).table

    # Headers
    for i, col_name in enumerate(display_df.columns):
        cell = table.cell(0, i)
        cell.text = str(col_name)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RgbColor(0x2F, 0x54, 0x96)
        para = cell.text_frame.paragraphs[0]
        para.font.bold = True
        para.font.color.rgb = RgbColor(255, 255, 255)
        para.font.size = Pt(10)
        para.alignment = PP_ALIGN.CENTER

    # Data
    for row_idx, (_, row) in enumerate(display_df.iterrows(), start=1):
        for col_idx, value in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.text = str(value)
            para = cell.text_frame.paragraphs[0]
            para.font.size = Pt(9)
            para.alignment = PP_ALIGN.CENTER


def create_dataframe_presentation(
    dataframes: dict,
    output_path: str
) -> None:
    """Create presentation from multiple DataFrames."""
    prs = Presentation()

    # Title slide
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "Data Analysis Report"

    for title, df in dataframes.items():
        dataframe_to_slide(prs, df, title)

    prs.save(output_path)
    print(f"DataFrame presentation saved: {output_path}")
```

## Best Practices

### 1. Template Design

```python
"""Best practices for template-based generation."""

# DO: Use consistent placeholder naming
PLACEHOLDERS = {
    'title': '{{title}}',
    'subtitle': '{{subtitle}}',
    'date': '{{date}}',
    'author': '{{author}}'
}

# DO: Create reusable slide builders
class SlideBuilder:
    def __init__(self, prs):
        self.prs = prs

    def add_title_slide(self, title, subtitle):
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[0])
        slide.shapes.title.text = title
        if subtitle:
            slide.placeholders[1].text = subtitle
        return slide

    def add_content_slide(self, title, bullets):
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[1])
        slide.shapes.title.text = title
        tf = slide.placeholders[1].text_frame
        tf.text = bullets[0]
        for bullet in bullets[1:]:
            p = tf.add_paragraph()
            p.text = bullet
        return slide
```

### 2. Performance Optimization

```python
"""Performance tips for large presentations."""

# DO: Reuse color objects
COLORS = {
    'primary': RgbColor(0x2F, 0x54, 0x96),
    'secondary': RgbColor(0x70, 0xAD, 0x47),
    'accent': RgbColor(0xED, 0x7D, 0x31)
}

# DO: Batch similar operations
def add_multiple_charts(prs, chart_data_list):
    for title, data, chart_type in chart_data_list:
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        slide.shapes.title.text = title
        # Add chart...
```

### 3. Error Handling

```python
"""Robust error handling for presentations."""
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def safe_generate_presentation(template_path, output_path, data):
    """Generate presentation with error handling."""
    try:
        if not Path(template_path).exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        prs = Presentation(template_path)
        # Process...
        prs.save(output_path)

        return {"success": True, "path": output_path}

    except Exception as e:
        logger.exception(f"Presentation generation failed: {e}")
        return {"success": False, "error": str(e)}
```

## Troubleshooting

### Common Issues

#### 1. Layout Not Found

```python
# Problem: Slide layout index out of range
# Solution: Check available layouts

prs = Presentation()
for i, layout in enumerate(prs.slide_layouts):
    print(f"{i}: {layout.name}")

# Common layouts:
# 0: Title Slide
# 1: Title and Content
# 5: Title Only
# 6: Blank
```

#### 2. Text Overflow

```python
# Problem: Text doesn't fit in shape
# Solution: Adjust font size or enable auto-fit

tf = shape.text_frame
tf.auto_size = True  # Enable auto-sizing
# Or manually adjust
tf.paragraphs[0].font.size = Pt(10)
```

#### 3. Chart Not Displaying

```python
# Problem: Chart appears empty
# Solution: Verify data structure

# DO: Ensure categories and series match
chart_data = CategoryChartData()
chart_data.categories = ['A', 'B', 'C']  # Must have values
chart_data.add_series('Series 1', (1, 2, 3))  # Same length
```

## Version History

### 1.0.0 (2026-01-17)
- Initial skill creation
- Core capabilities documentation
- 6 complete code examples
- Template-based generation patterns
- Chart and table creation

## Resources

- **Official Documentation**: https://python-pptx.readthedocs.io/
- **GitHub Repository**: https://github.com/scanny/python-pptx
- **PyPI Package**: https://pypi.org/project/python-pptx/

## Related Skills

- **python-docx** - Word document generation
- **openpyxl** - Excel workbook automation
- **plotly** - Interactive chart generation
- **pypdf** - PDF manipulation

---

*This skill provides comprehensive patterns for PowerPoint automation refined from production presentation generation systems.*
