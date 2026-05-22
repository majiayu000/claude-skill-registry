---
name: python-docx
description: Create and manipulate Microsoft Word documents programmatically. Build reports, contracts, and documentation with full control over paragraphs, tables, headers, styles, and images.
version: 1.0.0
category: office-docs
type: skill
capabilities:
  - document_creation
  - paragraph_formatting
  - table_generation
  - header_footer_management
  - style_customization
  - image_insertion
  - template_manipulation
  - mail_merge_patterns
tools:
  - python
  - python-docx
  - lxml
tags: [word, docx, document-generation, reports, templates, office-automation]
platforms: [windows, macos, linux]
related_skills:
  - docx-templates
  - pypdf
  - openpyxl
---

# Python-docx Word Document Automation Skill

## Overview

Python-docx is a Python library for creating and manipulating Microsoft Word (.docx) documents. This skill covers comprehensive patterns for document automation including:

- **Document creation** from scratch or templates
- **Paragraph formatting** with styles, fonts, and alignment
- **Table generation** with merged cells, styles, and formatting
- **Headers and footers** with page numbers and dynamic content
- **Image insertion** with sizing and positioning
- **Style management** for consistent document appearance
- **Template manipulation** for document workflows
- **Mail merge patterns** for bulk document generation

## When to Use This Skill

### USE when:
- Creating Word documents programmatically from data
- Generating reports with consistent formatting
- Building contracts, invoices, or legal documents
- Automating template-based document creation
- Modifying existing Word documents
- Creating documents with complex table structures
- Generating technical documentation with code blocks
- Building multi-section documents with headers/footers
- Creating documents with embedded images and charts
- Batch processing document generation

### DON'T USE when:
- Simple template filling (use docx-templates instead)
- PDF generation is the final output (use pypdf or reportlab)
- Need real-time collaborative editing
- Document requires complex macros or VBA
- Need to preserve complex Word features (use COM automation on Windows)
- Only need to extract text from documents (use python-docx2txt)

## Prerequisites

### Installation

```bash
# Using pip
pip install python-docx

# Using uv (recommended)
uv pip install python-docx

# With image support
pip install python-docx Pillow

# Full installation with all optional dependencies
pip install python-docx Pillow lxml
```

### Verify Installation

```python
from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

print("python-docx installed successfully!")
```

## Core Capabilities

### 1. Basic Document Creation

```python
"""
Create a basic Word document with title, paragraphs, and formatting.
"""
from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def create_basic_document(output_path: str) -> None:
    """Create a basic document with common elements."""
    # Create new document
    doc = Document()

    # Set document properties
    core_properties = doc.core_properties
    core_properties.author = "Document Generator"
    core_properties.title = "Sample Report"
    core_properties.subject = "Automated Document Generation"

    # Add title with formatting
    title = doc.add_heading('Monthly Performance Report', level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Add subtitle paragraph
    subtitle = doc.add_paragraph()
    subtitle_run = subtitle.add_run('January 2026')
    subtitle_run.font.size = Pt(14)
    subtitle_run.font.italic = True
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Add section heading
    doc.add_heading('Executive Summary', level=1)

    # Add paragraph with multiple runs (different formatting)
    para = doc.add_paragraph()
    para.add_run('This report summarizes ').font.size = Pt(11)
    bold_run = para.add_run('key performance metrics')
    bold_run.bold = True
    bold_run.font.size = Pt(11)
    para.add_run(' for the month of January 2026.')

    # Add bullet points
    doc.add_heading('Key Highlights', level=2)

    bullets = [
        'Revenue increased by 15% compared to last month',
        'Customer satisfaction score reached 92%',
        'New user registrations up 25%',
        'Support ticket resolution time reduced by 10%'
    ]

    for bullet in bullets:
        para = doc.add_paragraph(bullet, style='List Bullet')

    # Add numbered list
    doc.add_heading('Action Items', level=2)

    actions = [
        'Review Q1 budget allocation',
        'Schedule team performance reviews',
        'Finalize marketing campaign for Q2'
    ]

    for action in actions:
        doc.add_paragraph(action, style='List Number')

    # Save document
    doc.save(output_path)
    print(f"Document saved to {output_path}")


# Usage
create_basic_document('basic_report.docx')
```

### 2. Advanced Paragraph Formatting

```python
"""
Advanced paragraph formatting with custom styles, spacing, and indentation.
"""
from docx import Document
from docx.shared import Pt, Inches, Cm, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

def create_formatted_document(output_path: str) -> None:
    """Create document with advanced paragraph formatting."""
    doc = Document()

    # Create custom style
    styles = doc.styles

    # Create paragraph style
    custom_style = styles.add_style('CustomBody', WD_STYLE_TYPE.PARAGRAPH)
    custom_style.font.name = 'Calibri'
    custom_style.font.size = Pt(11)
    custom_style.paragraph_format.space_before = Pt(6)
    custom_style.paragraph_format.space_after = Pt(6)
    custom_style.paragraph_format.line_spacing = 1.15

    # Create character style for highlighting
    highlight_style = styles.add_style('Highlight', WD_STYLE_TYPE.CHARACTER)
    highlight_style.font.bold = True
    highlight_style.font.color.rgb = None  # Will use theme color

    # Add heading
    doc.add_heading('Document Formatting Examples', level=0)

    # Paragraph with custom alignment and spacing
    doc.add_heading('Text Alignment', level=1)

    # Left aligned (default)
    para_left = doc.add_paragraph('Left aligned text (default)')
    para_left.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # Center aligned
    para_center = doc.add_paragraph('Center aligned text')
    para_center.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Right aligned
    para_right = doc.add_paragraph('Right aligned text')
    para_right.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Justified
    para_justified = doc.add_paragraph(
        'Justified text spreads evenly across the line width. '
        'This is useful for formal documents and reports where '
        'a clean, professional appearance is desired.'
    )
    para_justified.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Line spacing examples
    doc.add_heading('Line Spacing', level=1)

    # Single spacing
    single_para = doc.add_paragraph(
        'Single spaced paragraph. Line spacing is set to 1.0 '
        'which means the lines are close together.'
    )
    single_para.paragraph_format.line_spacing = 1.0

    # 1.5 spacing
    one_half_para = doc.add_paragraph(
        'One and a half spaced paragraph. Line spacing is set to 1.5 '
        'which provides moderate spacing between lines.'
    )
    one_half_para.paragraph_format.line_spacing = 1.5

    # Double spacing
    double_para = doc.add_paragraph(
        'Double spaced paragraph. Line spacing is set to 2.0 '
        'which is common for academic and legal documents.'
    )
    double_para.paragraph_format.line_spacing = 2.0

    # Indentation examples
    doc.add_heading('Indentation', level=1)

    # First line indent
    first_indent = doc.add_paragraph(
        'This paragraph has a first line indent. The first line starts '
        'further to the right than subsequent lines, which is a common '
        'style for body text in books and formal documents.'
    )
    first_indent.paragraph_format.first_line_indent = Inches(0.5)

    # Left indent (block indent)
    left_indent = doc.add_paragraph(
        'This paragraph has a left indent applied. The entire paragraph '
        'is shifted to the right, which is useful for quotations or '
        'secondary information.'
    )
    left_indent.paragraph_format.left_indent = Inches(0.75)

    # Right indent
    right_indent = doc.add_paragraph(
        'This paragraph has a right indent. The right edge of the text '
        'is moved inward from the page margin.'
    )
    right_indent.paragraph_format.right_indent = Inches(0.75)

    # Hanging indent (for references/bibliography)
    hanging = doc.add_paragraph(
        'Smith, J. (2026). The Complete Guide to Document Automation. '
        'Publisher Name. This is an example of a hanging indent commonly '
        'used in bibliographies and reference lists.'
    )
    hanging.paragraph_format.left_indent = Inches(0.5)
    hanging.paragraph_format.first_line_indent = Inches(-0.5)

    # Font formatting examples
    doc.add_heading('Font Formatting', level=1)

    font_para = doc.add_paragraph()

    # Normal text
    font_para.add_run('Normal text, ')

    # Bold
    bold_run = font_para.add_run('bold text, ')
    bold_run.bold = True

    # Italic
    italic_run = font_para.add_run('italic text, ')
    italic_run.italic = True

    # Underline
    underline_run = font_para.add_run('underlined text, ')
    underline_run.underline = True

    # Strikethrough
    strike_run = font_para.add_run('strikethrough text, ')
    strike_run.font.strike = True

    # Subscript
    font_para.add_run('H')
    sub_run = font_para.add_run('2')
    sub_run.font.subscript = True
    font_para.add_run('O, ')

    # Superscript
    font_para.add_run('E=mc')
    sup_run = font_para.add_run('2')
    sup_run.font.superscript = True

    # Different font sizes
    doc.add_heading('Font Sizes', level=2)

    sizes_para = doc.add_paragraph()
    for size in [8, 10, 12, 14, 16, 18, 24]:
        run = sizes_para.add_run(f'{size}pt ')
        run.font.size = Pt(size)

    # Save document
    doc.save(output_path)
    print(f"Formatted document saved to {output_path}")


create_formatted_document('formatted_document.docx')
```

### 3. Table Creation and Formatting

```python
"""
Create and format tables with merged cells, styles, and custom formatting.
"""
from docx import Document
from docx.shared import Inches, Pt, Cm, Twips
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import nsdecls, qn
from docx.oxml import parse_xml, OxmlElement
from typing import List, Dict, Any, Optional

def set_cell_shading(cell, color: str) -> None:
    """Set cell background color."""
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), color)
    cell._tc.get_or_add_tcPr().append(shading_elm)


def set_cell_borders(cell, border_color: str = "000000", border_size: int = 4) -> None:
    """Set cell borders."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')

    for border_name in ['top', 'left', 'bottom', 'right']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), str(border_size))
        border.set(qn('w:color'), border_color)
        tcBorders.append(border)

    tcPr.append(tcBorders)


def create_data_table(
    doc: Document,
    headers: List[str],
    data: List[List[Any]],
    header_color: str = "4472C4",
    alternate_row_color: Optional[str] = "D9E2F3"
) -> None:
    """Create a formatted data table with headers and styling."""
    # Create table
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Style header row
    header_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        cell = header_cells[i]
        cell.text = header

        # Format header cell
        set_cell_shading(cell, header_color)

        # Format text
        paragraph = cell.paragraphs[0]
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.runs[0]
        run.font.bold = True
        run.font.color.rgb = None  # White text
        run.font.size = Pt(11)

    # Add data rows
    for row_idx, row_data in enumerate(data):
        row = table.add_row()

        for col_idx, value in enumerate(row_data):
            cell = row.cells[col_idx]
            cell.text = str(value)

            # Alternate row shading
            if alternate_row_color and row_idx % 2 == 0:
                set_cell_shading(cell, alternate_row_color)

            # Center align numbers
            if isinstance(value, (int, float)):
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    return table


def create_merged_header_table(doc: Document) -> None:
    """Create table with merged cells for complex headers."""
    # Create 5x4 table
    table = doc.add_table(rows=5, cols=4)
    table.style = 'Table Grid'

    # Merge cells for main header
    top_left = table.cell(0, 0)
    top_right = table.cell(0, 3)
    top_left.merge(top_right)
    top_left.text = "Quarterly Sales Report 2026"
    top_left.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    top_left.paragraphs[0].runs[0].bold = True
    set_cell_shading(top_left, "2F5496")

    # Merge cells for category headers
    # Q1-Q2 header
    q1_q2 = table.cell(1, 1)
    q1_q2_end = table.cell(1, 2)
    q1_q2.merge(q1_q2_end)
    q1_q2.text = "First Half"
    q1_q2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_cell_shading(q1_q2, "5B9BD5")

    # Q3-Q4 header
    table.cell(1, 3).text = "Q3-Q4"
    set_cell_shading(table.cell(1, 3), "5B9BD5")

    # Product header (merged vertically)
    table.cell(1, 0).text = "Product"
    set_cell_shading(table.cell(1, 0), "5B9BD5")

    # Sub-headers
    sub_headers = ['', 'Q1', 'Q2', 'Total']
    for i, header in enumerate(sub_headers):
        cell = table.cell(2, i)
        cell.text = header
        set_cell_shading(cell, "BDD7EE")

    # Data rows
    data = [
        ['Widget A', '100', '150', '250'],
        ['Widget B', '200', '180', '380']
    ]

    for row_idx, row_data in enumerate(data, start=3):
        for col_idx, value in enumerate(row_data):
            table.cell(row_idx, col_idx).text = value


def create_document_with_tables(output_path: str) -> None:
    """Create document with various table examples."""
    doc = Document()

    doc.add_heading('Table Examples', level=0)

    # Simple data table
    doc.add_heading('Sales Data', level=1)

    headers = ['Product', 'Q1 Sales', 'Q2 Sales', 'Q3 Sales', 'Q4 Sales', 'Total']
    data = [
        ['Laptop Pro', 150, 175, 200, 225, 750],
        ['Desktop Ultra', 80, 95, 110, 130, 415],
        ['Monitor HD', 200, 220, 240, 260, 920],
        ['Keyboard Elite', 500, 520, 540, 580, 2140],
    ]

    create_data_table(doc, headers, data)

    doc.add_paragraph()  # Spacing

    # Merged header table
    doc.add_heading('Complex Table with Merged Cells', level=1)
    create_merged_header_table(doc)

    doc.add_paragraph()

    # Table with specific column widths
    doc.add_heading('Table with Custom Column Widths', level=1)

    table = doc.add_table(rows=4, cols=3)
    table.style = 'Table Grid'

    # Set column widths
    widths = [Inches(1.5), Inches(3.0), Inches(1.5)]
    for row in table.rows:
        for idx, (cell, width) in enumerate(zip(row.cells, widths)):
            cell.width = width

    # Add content
    headers = ['ID', 'Description', 'Status']
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = header
        cell.paragraphs[0].runs[0].bold = True
        set_cell_shading(cell, "E7E6E6")

    data = [
        ['001', 'Implement new feature for document generation', 'Complete'],
        ['002', 'Review and approve design specifications', 'In Progress'],
        ['003', 'Deploy to production environment', 'Pending'],
    ]

    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, value in enumerate(row_data):
            table.rows[row_idx].cells[col_idx].text = value

    doc.save(output_path)
    print(f"Table document saved to {output_path}")


create_document_with_tables('table_examples.docx')
```

### 4. Headers, Footers, and Page Setup

```python
"""
Configure headers, footers, page numbers, and page setup.
"""
from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def add_page_number(paragraph) -> None:
    """Add page number field to paragraph."""
    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')

    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"

    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')

    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')

    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def add_total_pages(paragraph) -> None:
    """Add total page count field to paragraph."""
    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')

    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "NUMPAGES"

    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')

    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')

    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def create_document_with_headers_footers(output_path: str) -> None:
    """Create document with headers, footers, and page numbers."""
    doc = Document()

    # Access the default section
    section = doc.sections[0]

    # Set page margins
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.25)
    section.right_margin = Inches(1.25)

    # Set page size (Letter)
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)

    # Configure header
    header = section.header
    header_para = header.paragraphs[0]

    # Add company logo placeholder and title
    header_para.text = "ACME Corporation"
    header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    header_run = header_para.runs[0]
    header_run.bold = True
    header_run.font.size = Pt(14)

    # Add subtitle to header
    subtitle_para = header.add_paragraph()
    subtitle_para.text = "Confidential Document"
    subtitle_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle_para.runs[0].font.size = Pt(10)
    subtitle_para.runs[0].italic = True

    # Configure footer with page numbers
    footer = section.footer
    footer_para = footer.paragraphs[0]
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Add "Page X of Y" format
    footer_para.add_run("Page ")
    add_page_number(footer_para)
    footer_para.add_run(" of ")
    add_total_pages(footer_para)

    # Add document content
    doc.add_heading('Document Title', level=0)

    # Add multiple paragraphs to create multiple pages
    for i in range(1, 4):
        doc.add_heading(f'Section {i}', level=1)
        for j in range(5):
            doc.add_paragraph(
                f'This is paragraph {j+1} of section {i}. '
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
                'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. '
                'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.'
            )

        # Add page break after each section (except last)
        if i < 3:
            doc.add_page_break()

    doc.save(output_path)
    print(f"Document with headers/footers saved to {output_path}")


def create_landscape_document(output_path: str) -> None:
    """Create document with landscape orientation."""
    doc = Document()

    section = doc.sections[0]

    # Set landscape orientation
    section.orientation = WD_ORIENT.LANDSCAPE

    # Swap width and height for landscape
    new_width = section.page_height
    new_height = section.page_width
    section.page_width = new_width
    section.page_height = new_height

    # Add content
    doc.add_heading('Wide Format Report', level=0)
    doc.add_paragraph('This document is in landscape orientation, ideal for wide tables.')

    # Add wide table
    table = doc.add_table(rows=5, cols=8)
    table.style = 'Table Grid'

    headers = ['ID', 'Name', 'Q1', 'Q2', 'Q3', 'Q4', 'Total', 'Growth']
    for i, header in enumerate(headers):
        table.rows[0].cells[i].text = header

    doc.save(output_path)
    print(f"Landscape document saved to {output_path}")


create_document_with_headers_footers('headers_footers.docx')
create_landscape_document('landscape_report.docx')
```

### 5. Image Insertion and Positioning

```python
"""
Insert and position images in Word documents.
"""
from docx import Document
from docx.shared import Inches, Pt, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pathlib import Path
from io import BytesIO
from typing import Optional, Tuple
import requests

def add_image_from_url(doc: Document, url: str, width: Optional[float] = None) -> None:
    """Add image from URL to document."""
    response = requests.get(url)
    image_stream = BytesIO(response.content)

    if width:
        doc.add_picture(image_stream, width=Inches(width))
    else:
        doc.add_picture(image_stream)


def add_image_with_caption(
    doc: Document,
    image_path: str,
    caption: str,
    width: float = 4.0,
    figure_num: int = 1
) -> None:
    """Add image with centered caption below."""
    # Add image
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run()
    run.add_picture(image_path, width=Inches(width))

    # Add caption
    caption_para = doc.add_paragraph()
    caption_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption_run = caption_para.add_run(f'Figure {figure_num}: {caption}')
    caption_run.italic = True
    caption_run.font.size = Pt(10)


def add_inline_image(paragraph, image_path: str, width: float = 1.0) -> None:
    """Add image inline with text."""
    run = paragraph.add_run()
    run.add_picture(image_path, width=Inches(width))


def create_document_with_images(output_path: str, sample_image_path: str) -> None:
    """Create document with various image placements."""
    doc = Document()

    doc.add_heading('Image Examples', level=0)

    # Check if sample image exists
    if not Path(sample_image_path).exists():
        # Create a placeholder message if no image
        doc.add_paragraph(
            'Note: Sample image not found. Replace with actual image path.'
        )
        doc.save(output_path)
        return

    # Simple centered image
    doc.add_heading('Centered Image', level=1)
    doc.add_paragraph('The image below is centered on the page:')

    img_para = doc.add_paragraph()
    img_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = img_para.add_run()
    run.add_picture(sample_image_path, width=Inches(4))

    # Image with caption
    doc.add_heading('Image with Caption', level=1)
    doc.add_paragraph('Images can include descriptive captions:')
    add_image_with_caption(
        doc,
        sample_image_path,
        'Sample chart showing quarterly results',
        width=4.0,
        figure_num=1
    )

    # Multiple images in a row (using table)
    doc.add_heading('Multiple Images Side by Side', level=1)
    doc.add_paragraph('Use tables to arrange images side by side:')

    # Create 1x3 table for images
    table = doc.add_table(rows=2, cols=3)

    for i in range(3):
        cell = table.cell(0, i)
        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run()
        run.add_picture(sample_image_path, width=Inches(1.8))

        # Add caption below each image
        caption_cell = table.cell(1, i)
        caption_cell.paragraphs[0].text = f'Image {i + 1}'
        caption_cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Inline image with text
    doc.add_heading('Inline Images', level=1)
    para = doc.add_paragraph('You can include small images ')
    run = para.add_run()
    run.add_picture(sample_image_path, width=Inches(0.5))
    para.add_run(' inline with your text for icons or small graphics.')

    doc.save(output_path)
    print(f"Document with images saved to {output_path}")


# Usage (provide path to actual image)
# create_document_with_images('image_document.docx', 'sample_chart.png')
```

### 6. Style Management and Custom Styles

```python
"""
Create and manage document styles for consistent formatting.
"""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from typing import Dict, Any

def create_custom_styles(doc: Document) -> Dict[str, Any]:
    """Create a set of custom styles for the document."""
    styles = doc.styles
    created_styles = {}

    # Custom Heading 1
    if 'CustomHeading1' not in [s.name for s in styles]:
        h1_style = styles.add_style('CustomHeading1', WD_STYLE_TYPE.PARAGRAPH)
        h1_style.base_style = styles['Heading 1']
        h1_style.font.name = 'Georgia'
        h1_style.font.size = Pt(18)
        h1_style.font.bold = True
        h1_style.font.color.rgb = RGBColor(0x2E, 0x74, 0xB5)
        h1_style.paragraph_format.space_before = Pt(24)
        h1_style.paragraph_format.space_after = Pt(12)
        created_styles['heading1'] = h1_style

    # Custom Heading 2
    if 'CustomHeading2' not in [s.name for s in styles]:
        h2_style = styles.add_style('CustomHeading2', WD_STYLE_TYPE.PARAGRAPH)
        h2_style.base_style = styles['Heading 2']
        h2_style.font.name = 'Georgia'
        h2_style.font.size = Pt(14)
        h2_style.font.bold = True
        h2_style.font.color.rgb = RGBColor(0x2E, 0x74, 0xB5)
        h2_style.paragraph_format.space_before = Pt(18)
        h2_style.paragraph_format.space_after = Pt(6)
        created_styles['heading2'] = h2_style

    # Custom Body Text
    if 'CustomBody' not in [s.name for s in styles]:
        body_style = styles.add_style('CustomBody', WD_STYLE_TYPE.PARAGRAPH)
        body_style.font.name = 'Calibri'
        body_style.font.size = Pt(11)
        body_style.paragraph_format.space_after = Pt(8)
        body_style.paragraph_format.line_spacing = 1.15
        body_style.paragraph_format.first_line_indent = Inches(0.25)
        created_styles['body'] = body_style

    # Custom Quote
    if 'CustomQuote' not in [s.name for s in styles]:
        quote_style = styles.add_style('CustomQuote', WD_STYLE_TYPE.PARAGRAPH)
        quote_style.font.name = 'Calibri'
        quote_style.font.size = Pt(11)
        quote_style.font.italic = True
        quote_style.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
        quote_style.paragraph_format.left_indent = Inches(0.5)
        quote_style.paragraph_format.right_indent = Inches(0.5)
        quote_style.paragraph_format.space_before = Pt(12)
        quote_style.paragraph_format.space_after = Pt(12)
        created_styles['quote'] = quote_style

    # Code Block Style
    if 'CodeBlock' not in [s.name for s in styles]:
        code_style = styles.add_style('CodeBlock', WD_STYLE_TYPE.PARAGRAPH)
        code_style.font.name = 'Consolas'
        code_style.font.size = Pt(10)
        code_style.paragraph_format.space_before = Pt(6)
        code_style.paragraph_format.space_after = Pt(6)
        code_style.paragraph_format.left_indent = Inches(0.25)
        created_styles['code'] = code_style

    # Highlight Character Style
    if 'Highlight' not in [s.name for s in styles]:
        highlight_style = styles.add_style('Highlight', WD_STYLE_TYPE.CHARACTER)
        highlight_style.font.bold = True
        highlight_style.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
        created_styles['highlight'] = highlight_style

    return created_styles


def create_styled_document(output_path: str) -> None:
    """Create document using custom styles."""
    doc = Document()

    # Create custom styles
    create_custom_styles(doc)

    # Use custom styles
    doc.add_paragraph('Technical Report', style='CustomHeading1')

    doc.add_paragraph('Introduction', style='CustomHeading2')

    intro = doc.add_paragraph(
        'This document demonstrates the use of custom styles for consistent '
        'formatting throughout the document. Custom styles allow you to define '
        'formatting once and apply it consistently.',
        style='CustomBody'
    )

    doc.add_paragraph('Key Concepts', style='CustomHeading2')

    doc.add_paragraph(
        'Style management is essential for professional documents. '
        'It ensures consistency and makes global formatting changes easy.',
        style='CustomBody'
    )

    # Add quote
    doc.add_paragraph(
        '"Good typography is invisible. Bad typography is everywhere." - Oliver Reichenstein',
        style='CustomQuote'
    )

    doc.add_paragraph('Code Example', style='CustomHeading2')

    # Add code block
    code = """def hello_world():
    print("Hello, World!")
    return True"""

    doc.add_paragraph(code, style='CodeBlock')

    doc.add_paragraph('Conclusion', style='CustomHeading2')

    conclusion = doc.add_paragraph(style='CustomBody')
    conclusion.add_run('Custom styles provide ')
    highlight_run = conclusion.add_run('powerful formatting control')
    highlight_run.style = 'Highlight'
    conclusion.add_run(' for document automation.')

    doc.save(output_path)
    print(f"Styled document saved to {output_path}")


create_styled_document('styled_document.docx')
```

## Integration Examples

### Report Generation from Database

```python
"""
Generate reports from database query results.
"""
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
from typing import List, Dict, Any
import sqlite3

def generate_database_report(
    db_path: str,
    query: str,
    output_path: str,
    title: str = "Database Report"
) -> None:
    """Generate Word report from database query."""
    # Connect and fetch data
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()

    # Create document
    doc = Document()

    # Title
    title_para = doc.add_heading(title, level=0)
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Metadata
    meta_para = doc.add_paragraph()
    meta_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta_para.add_run(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    meta_para.add_run(f' | Records: {len(rows)}')

    doc.add_paragraph()  # Spacing

    # Create table
    if rows:
        table = doc.add_table(rows=len(rows) + 1, cols=len(columns))
        table.style = 'Table Grid'

        # Headers
        for i, col in enumerate(columns):
            cell = table.rows[0].cells[i]
            cell.text = col.replace('_', ' ').title()
            cell.paragraphs[0].runs[0].bold = True

        # Data
        for row_idx, row in enumerate(rows, start=1):
            for col_idx, col in enumerate(columns):
                table.rows[row_idx].cells[col_idx].text = str(row[col])
    else:
        doc.add_paragraph('No records found.')

    doc.save(output_path)
    print(f"Report saved to {output_path}")
```

### Template-Based Document Generation

```python
"""
Generate documents by modifying a template.
"""
from docx import Document
from docx.shared import Pt
from typing import Dict, Any
from pathlib import Path
import re

def replace_placeholders(doc: Document, replacements: Dict[str, str]) -> None:
    """Replace {{placeholder}} patterns in document."""
    # Process paragraphs
    for para in doc.paragraphs:
        for key, value in replacements.items():
            placeholder = f'{{{{{key}}}}}'
            if placeholder in para.text:
                for run in para.runs:
                    if placeholder in run.text:
                        run.text = run.text.replace(placeholder, str(value))

    # Process tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for key, value in replacements.items():
                        placeholder = f'{{{{{key}}}}}'
                        if placeholder in para.text:
                            for run in para.runs:
                                if placeholder in run.text:
                                    run.text = run.text.replace(placeholder, str(value))


def generate_from_template(
    template_path: str,
    output_path: str,
    data: Dict[str, Any]
) -> None:
    """Generate document from template with data substitution."""
    # Load template
    doc = Document(template_path)

    # Replace placeholders
    replace_placeholders(doc, data)

    # Save generated document
    doc.save(output_path)
    print(f"Generated document saved to {output_path}")


# Usage example
data = {
    'client_name': 'Acme Corporation',
    'date': '2026-01-17',
    'contract_value': '$50,000',
    'project_duration': '6 months',
    'contact_person': 'John Smith'
}

# generate_from_template('contract_template.docx', 'acme_contract.docx', data)
```

### Batch Document Generation

```python
"""
Generate multiple documents from a data source.
"""
from docx import Document
from docx.shared import Pt, Inches
from typing import List, Dict, Any
from pathlib import Path
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

def generate_single_document(
    template_path: str,
    output_dir: Path,
    data: Dict[str, Any],
    filename_field: str = 'id'
) -> str:
    """Generate a single document from template."""
    doc = Document(template_path)

    # Replace placeholders
    for para in doc.paragraphs:
        for key, value in data.items():
            placeholder = f'{{{{{key}}}}}'
            if placeholder in para.text:
                for run in para.runs:
                    if placeholder in run.text:
                        run.text = run.text.replace(placeholder, str(value))

    # Generate filename
    filename = f"{data.get(filename_field, 'document')}.docx"
    output_path = output_dir / filename

    doc.save(str(output_path))
    return str(output_path)


def batch_generate_documents(
    template_path: str,
    csv_data_path: str,
    output_dir: str,
    max_workers: int = 4
) -> List[str]:
    """Generate multiple documents from CSV data."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Read CSV data
    with open(csv_data_path, 'r') as f:
        reader = csv.DictReader(f)
        records = list(reader)

    generated_files = []

    # Generate documents in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                generate_single_document,
                template_path,
                output_path,
                record
            ): record
            for record in records
        }

        for future in as_completed(futures):
            try:
                result = future.result()
                generated_files.append(result)
                print(f"Generated: {result}")
            except Exception as e:
                print(f"Error generating document: {e}")

    return generated_files


# Usage
# batch_generate_documents(
#     'invoice_template.docx',
#     'clients.csv',
#     'generated_invoices/'
# )
```

## Best Practices

### 1. Document Structure

```python
"""Best practices for document organization."""

# DO: Create reusable document builders
class ReportBuilder:
    def __init__(self, template_path=None):
        self.doc = Document(template_path) if template_path else Document()

    def add_title(self, text):
        self.doc.add_heading(text, level=0)
        return self

    def add_section(self, title, content):
        self.doc.add_heading(title, level=1)
        self.doc.add_paragraph(content)
        return self

    def save(self, output_path):
        self.doc.save(output_path)

# DO: Use context managers for cleanup
from contextlib import contextmanager

@contextmanager
def document_context(output_path):
    doc = Document()
    try:
        yield doc
    finally:
        doc.save(output_path)

# Usage
with document_context('report.docx') as doc:
    doc.add_heading('Title', level=0)
    doc.add_paragraph('Content')
```

### 2. Style Consistency

```python
"""Maintain consistent styling across documents."""

# DO: Define style constants
class DocumentStyles:
    FONT_HEADING = 'Georgia'
    FONT_BODY = 'Calibri'
    SIZE_TITLE = Pt(24)
    SIZE_HEADING1 = Pt(18)
    SIZE_HEADING2 = Pt(14)
    SIZE_BODY = Pt(11)
    COLOR_PRIMARY = RGBColor(0x2E, 0x74, 0xB5)
    COLOR_SECONDARY = RGBColor(0x59, 0x59, 0x59)

# DO: Create style factory functions
def apply_heading_style(paragraph, level=1):
    run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
    run.font.name = DocumentStyles.FONT_HEADING
    run.font.bold = True
    run.font.color.rgb = DocumentStyles.COLOR_PRIMARY

    if level == 1:
        run.font.size = DocumentStyles.SIZE_HEADING1
    elif level == 2:
        run.font.size = DocumentStyles.SIZE_HEADING2
```

### 3. Error Handling

```python
"""Robust error handling for document operations."""
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def safe_generate_document(template_path, output_path, data):
    """Generate document with comprehensive error handling."""
    try:
        # Validate inputs
        if not Path(template_path).exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Generate document
        doc = Document(template_path)
        # ... processing ...
        doc.save(output_path)

        logger.info(f"Document generated: {output_path}")
        return {"success": True, "path": output_path}

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return {"success": False, "error": str(e)}

    except PermissionError as e:
        logger.error(f"Permission denied: {e}")
        return {"success": False, "error": "Permission denied"}

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return {"success": False, "error": str(e)}
```

### 4. Performance Optimization

```python
"""Optimize document generation performance."""

# DO: Reuse Document objects when generating similar documents
class DocumentPool:
    def __init__(self, template_path):
        self.template_path = template_path

    def generate(self, data, output_path):
        # Load fresh copy of template for each generation
        doc = Document(self.template_path)
        # Process...
        doc.save(output_path)

# DO: Use streaming for large documents
def generate_large_table(doc, data_generator, chunk_size=1000):
    """Generate large table in chunks to manage memory."""
    table = None
    headers_added = False

    for chunk in data_generator:
        if table is None:
            headers = list(chunk[0].keys())
            table = doc.add_table(rows=1, cols=len(headers))
            for i, header in enumerate(headers):
                table.rows[0].cells[i].text = header
            headers_added = True

        for row_data in chunk:
            row = table.add_row()
            for i, value in enumerate(row_data.values()):
                row.cells[i].text = str(value)
```

## Troubleshooting

### Common Issues

#### 1. Font Not Appearing Correctly

```python
# Problem: Font doesn't display in Word
# Solution: Use fonts available on target system

# Check available fonts
def get_available_fonts():
    """List fonts that should work cross-platform."""
    return [
        'Arial', 'Calibri', 'Times New Roman',
        'Georgia', 'Verdana', 'Tahoma',
        'Consolas', 'Courier New'
    ]

# Use fallback fonts
def set_font_with_fallback(run, preferred_font, fallback='Arial'):
    run.font.name = preferred_font
    # Set East Asian font as fallback
    run._element.rPr.rFonts.set(qn('w:eastAsia'), fallback)
```

#### 2. Table Width Issues

```python
# Problem: Table columns not sized correctly
# Solution: Explicitly set column widths

def set_column_widths(table, widths):
    """Set explicit column widths for table."""
    for row in table.rows:
        for idx, (cell, width) in enumerate(zip(row.cells, widths)):
            cell.width = width

# Usage
widths = [Inches(1), Inches(3), Inches(2)]
set_column_widths(table, widths)
```

#### 3. Image Not Displaying

```python
# Problem: Image doesn't appear in document
# Solution: Verify image path and format

from pathlib import Path
from PIL import Image

def validate_and_add_image(doc, image_path, width=None):
    """Validate image before adding to document."""
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Check format
    supported_formats = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}
    if path.suffix.lower() not in supported_formats:
        raise ValueError(f"Unsupported format: {path.suffix}")

    # Validate image can be opened
    try:
        with Image.open(image_path) as img:
            img.verify()
    except Exception as e:
        raise ValueError(f"Invalid image file: {e}")

    # Add to document
    if width:
        doc.add_picture(str(image_path), width=Inches(width))
    else:
        doc.add_picture(str(image_path))
```

#### 4. Style Not Applied

```python
# Problem: Custom style not appearing
# Solution: Ensure style exists before using

def safe_apply_style(paragraph, style_name, doc):
    """Apply style with fallback if not found."""
    try:
        paragraph.style = style_name
    except KeyError:
        # Style doesn't exist, create it or use default
        if style_name not in [s.name for s in doc.styles]:
            # Create minimal style
            from docx.enum.style import WD_STYLE_TYPE
            doc.styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
        paragraph.style = style_name
```

## Version History

### 1.0.0 (2026-01-17)
- Initial skill creation
- Core capabilities documentation
- 6 complete code examples
- Integration patterns
- Best practices guide
- Troubleshooting section

## Resources

- **Official Documentation**: https://python-docx.readthedocs.io/
- **GitHub Repository**: https://github.com/python-openxml/python-docx
- **PyPI Package**: https://pypi.org/project/python-docx/
- **Open XML SDK Reference**: https://docs.microsoft.com/en-us/office/open-xml/

## Related Skills

- **docx-templates** - Jinja2-style template rendering for Word documents
- **pypdf** - PDF manipulation and generation
- **openpyxl** - Excel file automation
- **python-pptx** - PowerPoint presentation generation

---

*This skill provides comprehensive patterns for Word document automation refined from production document generation systems.*
