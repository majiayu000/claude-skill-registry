---
name: branded-document-suite
version: 1.0.0
description: |
  Unified document generation system producing professionally styled PDF, DOCX, PPTX,
  and XLSX files with consistent branding through a single configuration.
author: QuantQuiver AI R&D
license: MIT

category: tooling
tags:
  - documents
  - pdf
  - docx
  - pptx
  - xlsx
  - branding
  - reports
  - presentations

dependencies:
  skills: []
  python: ">=3.9"
  packages:
    - reportlab
    - python-docx
    - openpyxl
    - pyyaml
  tools:
    - code_execution
    - bash

triggers:
  - "create branded PDF"
  - "generate document"
  - "make presentation"
  - "create report"
  - "branded slides"
  - "company document"
  - "export to Excel"
  - "professional document"
---

# Branded Document Suite

## Purpose

A unified document generation system producing professionally styled PDF, DOCX, PPTX, and XLSX files with consistent branding, configurable through a single brand configuration file.

**Problem Space:**
- Inconsistent branding across document types
- Manual formatting overhead
- Difficulty maintaining style guides
- No version control for document templates

**Solution Approach:**
- Single brand configuration drives all formats
- Template-based generation with content injection
- Support for complex layouts (tables, charts, diagrams)
- Export to multiple formats from single source

## When to Use

- Company reports and documentation
- Client deliverables
- Internal presentations
- Automated report generation in pipelines
- White-label document generation
- Any document requiring consistent brand identity

## When NOT to Use

- Quick notes or scratch documents
- Documents that require complex interactive elements
- Real-time collaborative editing
- Documents requiring specific proprietary format features

---

## Core Instructions

### Brand Configuration Schema

Always establish brand configuration first. This drives all document styling.

```yaml
# brand-config.yaml
brand:
  name: "Company Name"
  tagline: "Your tagline here"

colors:
  primary: "#3AA7F9"
  primary_dark: "#2A7BC4"
  primary_light: "#E8F4FD"
  secondary: "#211644"
  accent: "#F59E0B"

  # Semantic colors
  success: "#22C55E"
  warning: "#F59E0B"
  danger: "#EF4444"
  info: "#0EA5E9"

  # Text hierarchy
  text_primary: "#0F172A"
  text_secondary: "#334155"
  text_muted: "#94A3B8"

  # Surfaces
  surface_primary: "#FFFFFF"
  surface_secondary: "#F8FAFC"
  surface_tertiary: "#F1F5F9"
  border: "#E2E8F0"

typography:
  display:
    family: "Montserrat"
    weights: [600, 700]
    fallback: "Arial, sans-serif"
  body:
    family: "Inter"
    weights: [400, 500, 600]
    fallback: "system-ui, sans-serif"
  mono:
    family: "JetBrains Mono"
    weights: [400, 500]
    fallback: "monospace"

  # Type scale (px)
  scale:
    h1: 32
    h2: 24
    h3: 20
    h4: 16
    body: 14
    small: 12
    caption: 10

spacing:
  base: 4  # px
  scale: [0, 4, 8, 12, 16, 24, 32, 48, 64]

assets:
  logo_primary: "./assets/logo-primary.svg"
  logo_icon: "./assets/logo-icon.svg"
  logo_white: "./assets/logo-white.svg"
```

### Standard Procedures

#### 1. PDF Generation (ReportLab)

```python
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, Image
import yaml

class BrandedPDFGenerator:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.styles = self._build_styles()

    def _build_styles(self) -> dict:
        c = self.config['colors']
        t = self.config['typography']

        return {
            'Title': ParagraphStyle(
                'Title',
                fontName='Helvetica-Bold',
                fontSize=t['scale']['h1'],
                textColor=HexColor(c['text_primary']),
                spaceAfter=24
            ),
            'Heading1': ParagraphStyle(
                'Heading1',
                fontName='Helvetica-Bold',
                fontSize=t['scale']['h2'],
                textColor=HexColor(c['primary_dark']),
                spaceBefore=20,
                spaceAfter=12
            ),
            'Body': ParagraphStyle(
                'Body',
                fontName='Helvetica',
                fontSize=t['scale']['body'],
                textColor=HexColor(c['text_secondary']),
                spaceAfter=8
            )
        }

    def create_report(self, title: str, sections: list, output_path: str):
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []

        # Title
        story.append(Paragraph(title, self.styles['Title']))

        # Sections
        for section in sections:
            story.append(Paragraph(section['title'], self.styles['Heading1']))
            for para in section.get('content', []):
                story.append(Paragraph(para, self.styles['Body']))
            if 'table' in section:
                story.append(self._create_branded_table(section['table']))

        doc.build(story)
        return output_path
```

#### 2. DOCX Generation (python-docx)

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

class BrandedDocxGenerator:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

    def create_document(self, title: str, sections: list, output_path: str):
        doc = Document()

        # Title
        title_para = doc.add_heading(title, level=0)
        self._apply_brand_style(title_para)

        # Sections
        for section in sections:
            heading = doc.add_heading(section['title'], level=1)
            for para in section.get('content', []):
                doc.add_paragraph(para)

        doc.save(output_path)
        return output_path

    def _apply_brand_style(self, paragraph):
        c = self.config['colors']
        for run in paragraph.runs:
            run.font.color.rgb = RGBColor.from_string(c['primary_dark'][1:])
```

#### 3. PPTX Generation

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor as PPTXColor

class BrandedPptxGenerator:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

    def create_presentation(self, title: str, subtitle: str, slides: list, output_path: str):
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)

        # Title slide
        self._add_title_slide(prs, title, subtitle)

        # Content slides
        for slide_data in slides:
            self._add_content_slide(prs, slide_data)

        prs.save(output_path)
        return output_path

    def _add_title_slide(self, prs, title, subtitle):
        layout = prs.slide_layouts[6]  # Blank
        slide = prs.slides.add_slide(layout)

        # Background
        c = self.config['colors']
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = PPTXColor.from_string(c['secondary'][1:])

        # Title text
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(12), Inches(1.5))
        title_frame = title_box.text_frame
        title_para = title_frame.paragraphs[0]
        title_para.text = title
        title_para.font.size = Pt(44)
        title_para.font.bold = True
        title_para.font.color.rgb = PPTXColor(255, 255, 255)
```

#### 4. XLSX Generation (openpyxl)

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

class BrandedXlsxGenerator:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

    def create_spreadsheet(self, title: str, sheets: list, output_path: str):
        wb = Workbook()
        wb.remove(wb.active)  # Remove default sheet

        for sheet_data in sheets:
            ws = wb.create_sheet(title=sheet_data['name'])
            self._populate_sheet(ws, sheet_data)

        wb.save(output_path)
        return output_path

    def _populate_sheet(self, ws, sheet_data):
        c = self.config['colors']

        # Header style
        header_fill = PatternFill(start_color=c['primary'][1:], end_color=c['primary'][1:], fill_type='solid')
        header_font = Font(bold=True, color='FFFFFF')

        # Write headers
        for col, header in enumerate(sheet_data['headers'], 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.fill = header_fill
            cell.font = header_font

        # Write data
        for row_idx, row_data in enumerate(sheet_data['data'], 2):
            for col_idx, value in enumerate(row_data, 1):
                cell = ws.cell(row=row_idx, column=col_idx, value=value)
                if row_idx % 2 == 0:
                    cell.fill = PatternFill(start_color=c['surface_secondary'][1:],
                                           end_color=c['surface_secondary'][1:],
                                           fill_type='solid')
```

### Decision Framework

| Document Type | Best For | Key Features |
|---------------|----------|--------------|
| **PDF** | Final deliverables, print | Pixel-perfect, portable |
| **DOCX** | Editable documents | Collaboration-friendly |
| **PPTX** | Presentations | Visual storytelling |
| **XLSX** | Data analysis | Calculations, filtering |

**Format Selection Logic:**
1. Need editing? → DOCX
2. Need calculations? → XLSX
3. Need presenting? → PPTX
4. Final/archival? → PDF

---

## Templates

### Report Structure Template

```yaml
report:
  title: "Quarterly Analysis Report"
  subtitle: "Q4 2025"
  author: "Analytics Team"
  date: "2025-01-11"

  sections:
    - title: "Executive Summary"
      content:
        - "Key findings paragraph 1"
        - "Key findings paragraph 2"

    - title: "Analysis"
      content:
        - "Detailed analysis text"
      table:
        headers: ["Metric", "Q3", "Q4", "Change"]
        rows:
          - ["Revenue", "$1.2M", "$1.5M", "+25%"]
          - ["Users", "10,000", "15,000", "+50%"]

    - title: "Recommendations"
      content:
        - "Recommendation 1"
        - "Recommendation 2"
```

### Presentation Structure Template

```yaml
presentation:
  title: "Project Overview"
  subtitle: "January 2026"
  author: "Team Lead"

  slides:
    - title: "Agenda"
      bullets:
        - "Current State"
        - "Proposed Changes"
        - "Timeline"
        - "Q&A"

    - title: "Current State"
      bullets:
        - "Point 1"
        - "Point 2"
      chart:
        type: "bar"
        data:
          categories: ["Jan", "Feb", "Mar"]
          series:
            - name: "2024"
              values: [100, 120, 140]
            - name: "2025"
              values: [150, 180, 200]
```

---

## Examples

### Example 1: Generate Branded PDF Report

**Input**: "Create a quarterly sales report PDF with our brand styling"

**Output**:
```python
# Using the BrandedPDFGenerator
config = "brand-config.yaml"
generator = BrandedPDFGenerator(config)

sections = [
    {
        "title": "Q4 Sales Summary",
        "content": [
            "Total revenue increased by 25% compared to Q3.",
            "New customer acquisition exceeded targets by 15%."
        ],
        "table": {
            "headers": ["Region", "Q3 Revenue", "Q4 Revenue", "Growth"],
            "rows": [
                ["North", "$500K", "$650K", "+30%"],
                ["South", "$400K", "$480K", "+20%"],
                ["East", "$300K", "$370K", "+23%"]
            ]
        }
    }
]

generator.create_report(
    title="Q4 2025 Sales Report",
    sections=sections,
    output_path="Q4_Sales_Report.pdf"
)
```

### Example 2: Create Branded Presentation

**Input**: "Make a project kickoff presentation with 5 slides"

**Output**: PPTX file with branded title slide, agenda, problem statement, solution overview, and next steps slides, all following brand color palette and typography.

---

## Validation Checklist

Before completing document generation:

- [ ] Brand config file exists and is valid YAML
- [ ] All color codes are valid hex values
- [ ] Output directory is writable
- [ ] All content is provided (no placeholders)
- [ ] Tables have matching header/row column counts
- [ ] Images referenced are accessible
- [ ] Font fallbacks specified for missing fonts
- [ ] Document opens correctly in target application

---

## Related Resources

- Skill: `brand-asset-generator` - Generate logos and visual assets
- Skill: `technical-documentation-generator` - HTML documentation
- ReportLab Documentation: https://docs.reportlab.com/
- python-docx Documentation: https://python-docx.readthedocs.io/

---

## Changelog

### 1.0.0 (January 2026)
- Initial release
- PDF generation with ReportLab
- DOCX generation with python-docx
- PPTX generation with python-pptx
- XLSX generation with openpyxl
- Unified brand configuration system
