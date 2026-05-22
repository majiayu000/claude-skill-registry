---
name: reportlab
description: Python library for programmatic PDF generation and creation. Use when user wants to generate PDFs from scratch, create invoices, reports, certificates, labels, or custom documents with precise control over layout, fonts, graphics, tables, and charts. Supports both low-level drawing (Canvas) and high-level documents (Platypus).
---

# ReportLab

## Overview

ReportLab is a powerful open-source Python library for creating PDF documents programmatically. Generate professional PDFs with precise control over layout, typography, graphics, tables, and charts. Perfect for automated report generation, invoices, certificates, and custom documents.

## When to Use This Skill

Activate when the user:
- Wants to generate PDF documents programmatically
- Needs to create invoices, reports, or receipts
- Asks to create certificates, labels, or forms
- Mentions ReportLab explicitly
- Wants custom PDF layouts with tables, charts, or graphics
- Needs to automate document generation
- Wants precise control over PDF layout and styling

## Installation

Check if ReportLab is installed:

```bash
python3 -c "import reportlab; print(reportlab.Version)"
```

If not installed:

```bash
pip3 install reportlab
```

For additional fonts and features:

```bash
pip3 install reportlab[renderPM,rlPyCairo]
```

## Two Approaches: Canvas vs Platypus

ReportLab provides two APIs:

**Canvas API (Low-Level)**
- Direct drawing on PDF pages
- Precise positioning with x, y coordinates
- Like painting on a canvas
- Best for: Simple documents, custom layouts, graphics-heavy PDFs

**Platypus API (High-Level)**
- Flowable document elements
- Automatic layout and pagination
- Easier for complex multi-page documents
- Best for: Reports, articles, documents with lots of text

## Canvas API (Low-Level Drawing)

### Basic Canvas Usage

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch

# Create PDF
c = canvas.Canvas("output.pdf", pagesize=letter)
width, height = letter

# Draw text
c.drawString(100, height - 100, "Hello, World!")

# Set font
c.setFont("Helvetica-Bold", 24)
c.drawString(100, height - 150, "Large Bold Text")

# Save PDF
c.save()
```

### Drawing Shapes and Lines

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

c = canvas.Canvas("shapes.pdf", pagesize=letter)
width, height = letter

# Line
c.line(50, height - 50, width - 50, height - 50)

# Rectangle
c.rect(50, height - 200, 200, 100, stroke=1, fill=0)

# Filled rectangle with color
c.setFillColor(colors.lightblue)
c.setStrokeColor(colors.blue)
c.rect(300, height - 200, 200, 100, stroke=1, fill=1)

# Circle
c.circle(150, height - 350, 50, stroke=1, fill=0)

# Rounded rectangle
c.roundRect(300, height - 400, 200, 100, 10, stroke=1, fill=0)

c.save()
```

### Working with Text

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

c = canvas.Canvas("text.pdf", pagesize=letter)
width, height = letter

# Different fonts and sizes
c.setFont("Helvetica", 12)
c.drawString(50, height - 50, "Helvetica 12pt")

c.setFont("Helvetica-Bold", 16)
c.drawString(50, height - 80, "Helvetica Bold 16pt")

c.setFont("Times-Roman", 14)
c.drawString(50, height - 110, "Times Roman 14pt")

# Colored text
c.setFillColor(colors.red)
c.drawString(50, height - 140, "Red text")

c.setFillColor(colors.blue)
c.drawString(50, height - 170, "Blue text")

# Text alignment
text = "Right-aligned text"
text_width = c.stringWidth(text, "Helvetica", 12)
c.setFont("Helvetica", 12)
c.setFillColor(colors.black)
c.drawString(width - text_width - 50, height - 200, text)

# Multi-line text with textobject
textobject = c.beginText(50, height - 250)
textobject.setFont("Helvetica", 12)
textobject.textLines("""This is multi-line text.
Each line will be rendered separately.
Great for paragraphs!""")
c.drawText(textobject)

c.save()
```

### Adding Images

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

c = canvas.Canvas("images.pdf", pagesize=letter)
width, height = letter

# Draw image
c.drawImage("logo.png", 50, height - 200, width=2*inch, height=1*inch)

# Image with preserved aspect ratio
c.drawImage("photo.jpg", 50, height - 400, width=3*inch, preserveAspectRatio=True)

c.save()
```

## Platypus API (High-Level Documents)

### Basic Document Structure

```python
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# Create document
doc = SimpleDocTemplate("document.pdf", pagesize=letter)
story = []  # Container for flowable elements

# Get styles
styles = getSampleStyleSheet()

# Add content
story.append(Paragraph("Document Title", styles['Title']))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("This is a paragraph of text.", styles['Normal']))
story.append(Paragraph("This is another paragraph.", styles['Normal']))

# Build PDF
doc.build(story)
```

### Working with Paragraphs and Styles

```python
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import inch
from reportlab.lib import colors

doc = SimpleDocTemplate("styled_doc.pdf", pagesize=letter)
story = []
styles = getSampleStyleSheet()

# Built-in styles
story.append(Paragraph("Title Style", styles['Title']))
story.append(Paragraph("Heading 1", styles['Heading1']))
story.append(Paragraph("Heading 2", styles['Heading2']))
story.append(Paragraph("Normal paragraph text.", styles['Normal']))
story.append(Spacer(1, 0.2*inch))

# Custom style
custom_style = ParagraphStyle(
    'CustomStyle',
    parent=styles['Normal'],
    fontSize=14,
    textColor=colors.blue,
    alignment=TA_CENTER,
    spaceAfter=10,
)
story.append(Paragraph("Centered blue text", custom_style))

# Justified paragraph
justified_style = ParagraphStyle(
    'Justified',
    parent=styles['Normal'],
    alignment=TA_JUSTIFY,
)
long_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 10
story.append(Paragraph(long_text, justified_style))

doc.build(story)
```

### Creating Tables

```python
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("table.pdf", pagesize=letter)
story = []
styles = getSampleStyleSheet()

story.append(Paragraph("Sales Report", styles['Title']))

# Table data
data = [
    ['Product', 'Q1', 'Q2', 'Q3', 'Q4'],
    ['Widget A', '$1,000', '$1,200', '$1,100', '$1,300'],
    ['Widget B', '$800', '$900', '$950', '$1,000'],
    ['Widget C', '$1,500', '$1,600', '$1,700', '$1,800'],
    ['Total', '$3,300', '$3,700', '$3,750', '$4,100'],
]

# Create table
table = Table(data)

# Style table
table.setStyle(TableStyle([
    # Header row
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

    # Data rows
    ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
    ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),

    # Total row
    ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
]))

story.append(table)
doc.build(story)
```

### Adding Charts

```python
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib import colors

doc = SimpleDocTemplate("charts.pdf", pagesize=letter)
story = []
styles = getSampleStyleSheet()

story.append(Paragraph("Sales Charts", styles['Title']))

# Bar chart
drawing = Drawing(400, 200)
bar_chart = VerticalBarChart()
bar_chart.x = 50
bar_chart.y = 50
bar_chart.height = 125
bar_chart.width = 300
bar_chart.data = [[100, 150, 200, 175, 225]]
bar_chart.categoryAxis.categoryNames = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
bar_chart.bars[0].fillColor = colors.blue
drawing.add(bar_chart)
story.append(drawing)

# Pie chart
drawing2 = Drawing(400, 200)
pie = Pie()
pie.x = 150
pie.y = 50
pie.width = 100
pie.height = 100
pie.data = [30, 25, 20, 15, 10]
pie.labels = ['Product A', 'Product B', 'Product C', 'Product D', 'Other']
pie.slices.strokeWidth = 0.5
drawing2.add(pie)
story.append(drawing2)

doc.build(story)
```

## Common Patterns

### Pattern 1: Invoice Generator

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from datetime import datetime

def create_invoice(invoice_number, customer_name, items, output_file="invoice.pdf"):
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Header
    story.append(Paragraph("INVOICE", styles['Title']))
    story.append(Spacer(1, 0.2*inch))

    # Invoice details
    invoice_info = [
        ['Invoice Number:', invoice_number],
        ['Date:', datetime.now().strftime('%Y-%m-%d')],
        ['Customer:', customer_name],
    ]
    info_table = Table(invoice_info, colWidths=[2*inch, 3*inch])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))

    # Items table
    table_data = [['Description', 'Quantity', 'Unit Price', 'Total']]
    subtotal = 0

    for item in items:
        total = item['quantity'] * item['price']
        subtotal += total
        table_data.append([
            item['description'],
            str(item['quantity']),
            f"${item['price']:.2f}",
            f"${total:.2f}"
        ])

    # Add totals
    tax = subtotal * 0.1  # 10% tax
    total = subtotal + tax

    table_data.append(['', '', 'Subtotal:', f"${subtotal:.2f}"])
    table_data.append(['', '', 'Tax (10%):', f"${tax:.2f}"])
    table_data.append(['', '', 'Total:', f"${total:.2f}"])

    items_table = Table(table_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
    items_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        # Data
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -4), 1, colors.black),

        # Totals
        ('FONTNAME', (2, -3), (-1, -1), 'Helvetica-Bold'),
        ('LINEABOVE', (2, -3), (-1, -3), 1, colors.black),
        ('LINEABOVE', (2, -1), (-1, -1), 2, colors.black),
    ]))

    story.append(items_table)
    doc.build(story)

# Usage
items = [
    {'description': 'Widget A', 'quantity': 5, 'price': 29.99},
    {'description': 'Widget B', 'quantity': 2, 'price': 49.99},
    {'description': 'Service Fee', 'quantity': 1, 'price': 100.00},
]
create_invoice("INV-2025-001", "Acme Corporation", items)
```

### Pattern 2: Certificate Generator

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_certificate(name, course, date, output_file="certificate.pdf"):
    c = canvas.Canvas(output_file, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Border
    c.setStrokeColor(colors.gold)
    c.setLineWidth(5)
    c.rect(0.5*inch, 0.5*inch, width - inch, height - inch)

    # Decorative inner border
    c.setStrokeColor(colors.darkgoldenrod)
    c.setLineWidth(2)
    c.rect(0.75*inch, 0.75*inch, width - 1.5*inch, height - 1.5*inch)

    # Title
    c.setFont("Helvetica-Bold", 48)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width/2, height - 2*inch, "Certificate of Completion")

    # Body text
    c.setFont("Helvetica", 20)
    c.setFillColor(colors.black)
    c.drawCentredString(width/2, height - 3*inch, "This is to certify that")

    # Name (large and prominent)
    c.setFont("Helvetica-Bold", 36)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width/2, height - 4*inch, name)

    # Course info
    c.setFont("Helvetica", 18)
    c.setFillColor(colors.black)
    c.drawCentredString(width/2, height - 5*inch, "has successfully completed the course")

    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 5.75*inch, course)

    # Date
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height - 6.5*inch, f"Date: {date}")

    c.save()

# Usage
create_certificate("John Doe", "Advanced Python Programming", "2025-10-27")
```

### Pattern 3: Multi-Page Report

```python
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

def header_footer(canvas, doc):
    """Add header and footer to each page"""
    canvas.saveState()

    # Header
    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(inch, letter[1] - 0.5*inch, "Company Report - Confidential")

    # Footer
    canvas.setFont('Helvetica', 9)
    canvas.drawString(inch, 0.5*inch, f"Page {doc.page}")
    canvas.drawRightString(letter[0] - inch, 0.5*inch, "© 2025 Company Name")

    canvas.restoreState()

def create_report(output_file="report.pdf"):
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Cover page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("Annual Report 2025", styles['Title']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Company Performance Analysis", styles['Heading1']))
    story.append(PageBreak())

    # Executive Summary
    story.append(Paragraph("Executive Summary", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))
    summary_text = "This report provides a comprehensive analysis of company performance..." * 5
    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))

    # Financial Data
    story.append(Paragraph("Financial Performance", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))

    financial_data = [
        ['Metric', 'Q1', 'Q2', 'Q3', 'Q4'],
        ['Revenue', '$2.5M', '$2.8M', '$3.1M', '$3.5M'],
        ['Expenses', '$1.8M', '$1.9M', '$2.0M', '$2.1M'],
        ['Profit', '$0.7M', '$0.9M', '$1.1M', '$1.4M'],
    ]

    table = Table(financial_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    story.append(table)

    # Build with header/footer
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)

create_report()
```

### Pattern 4: Data-Driven PDF from DataFrame

```python
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd

def dataframe_to_pdf(df, title, output_file="data_report.pdf"):
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Title
    story.append(Paragraph(title, styles['Title']))

    # Convert DataFrame to list
    data = [df.columns.tolist()] + df.values.tolist()

    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    story.append(table)
    doc.build(story)

# Usage
df = pd.DataFrame({
    'Product': ['A', 'B', 'C'],
    'Sales': [100, 150, 200],
    'Revenue': [1000, 1500, 2000]
})
dataframe_to_pdf(df, "Sales Report", "sales_report.pdf")
```

## Best Practices

1. **Choose the right API** - Use Canvas for simple layouts, Platypus for complex documents
2. **Use constants for measurements** - Use `inch`, `cm` from `reportlab.lib.units`
3. **Define styles once** - Create custom styles and reuse them
4. **Test page sizes** - Verify output on different page sizes (letter, A4, etc.)
5. **Handle images carefully** - Check image paths exist before adding to PDF
6. **Use tables for layouts** - Tables are great for structured layouts
7. **Cache fonts** - Register custom fonts once at module level

## Common Issues

### Issue: Text going off page

Calculate available space before drawing:

```python
from reportlab.lib.pagesizes import letter

width, height = letter
margin = 50  # pixels
usable_width = width - 2 * margin
usable_height = height - 2 * margin
```

### Issue: Images not found

Use absolute paths or verify file existence:

```python
import os

image_path = "logo.png"
if os.path.exists(image_path):
    c.drawImage(image_path, x, y, width=w, height=h)
```

### Issue: Unicode characters not displaying

Register and use TrueType fonts:

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
c.setFont('Arial', 12)
```

## Resources

- **references/api_reference.md**: Quick reference for common ReportLab operations
- Official docs: https://docs.reportlab.com/
- User guide (PDF): https://www.reportlab.com/docs/reportlab-userguide.pdf
- PyPI: https://pypi.org/project/reportlab/
