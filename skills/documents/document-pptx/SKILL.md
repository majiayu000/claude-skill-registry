---
name: document-pptx
description: Create, edit, and analyze PowerPoint presentations with slides, layouts, charts, images, animations, and speaker notes. Supports python-pptx and pptxgenjs for automated presentation generation in Python and Node.js.
---

# Document PPTX Skill — Quick Reference

This skill enables creation and editing of PowerPoint presentations programmatically. Claude should apply these patterns when users need to generate pitch decks, reports, training materials, or automate presentation workflows.

**Modern Best Practices (Dec 2025)**:
- One slide = one takeaway; design the deck around a decision or audience goal.
- Cite numbers (definition + timeframe + source) and keep a single source of truth for charts.
- Accessibility basics: reading order, contrast, and not color-only meaning.
- Version decks and enforce review loops (avoid “final_final_v7.pptx”).

---

## Quick Reference

| Task | Tool/Library | Language | When to Use |
|------|--------------|----------|-------------|
| Create PPTX | python-pptx | Python | Presentations, slide decks |
| Create PPTX | pptxgenjs | Node.js | Server-side generation |
| Templates | python-pptx | Python | Master slides, themes |
| Charts | python-pptx | Python | Data visualizations |
| Extract content | python-pptx | Python | Parse existing decks |

## When to Use This Skill

Claude should invoke this skill when a user requests:

- Generate PowerPoint presentations from data
- Create slide decks with charts and images
- Automate report generation as slides
- Extract content from existing presentations
- Apply consistent branding/templates
- Generate speaker notes
- Create training or educational materials

---

## Core Operations

### Create Presentation (Python)

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RgbColor

prs = Presentation()

# Title slide
title_layout = prs.slide_layouts[0]  # Title Slide layout
slide = prs.slides.add_slide(title_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = "Q4 2025 Business Review"
subtitle.text = "Presented by Product Team"

# Content slide with bullets
bullet_layout = prs.slide_layouts[1]  # Title and Content
slide = prs.slides.add_slide(bullet_layout)
slide.shapes.title.text = "Key Highlights"
body = slide.placeholders[1]
tf = body.text_frame
tf.text = "Revenue grew 25% YoY"

p = tf.add_paragraph()
p.text = "Customer base expanded to 10,000+"
p.level = 0

p = tf.add_paragraph()
p.text = "New enterprise tier launched"
p.level = 1  # Indented bullet

# Add speaker notes
notes_slide = slide.notes_slide
notes_slide.notes_text_frame.text = "Emphasize the enterprise growth story here."

prs.save('presentation.pptx')
```

### Create Presentation (Node.js)

```typescript
import pptxgen from 'pptxgenjs';

const pptx = new pptxgen();
pptx.author = 'Product Team';
pptx.title = 'Q4 Business Review';

// Title slide
let slide = pptx.addSlide();
slide.addText('Q4 2025 Business Review', {
  x: 1, y: 2, w: '80%',
  fontSize: 36, bold: true, color: '363636',
  align: 'center'
});
slide.addText('Presented by Product Team', {
  x: 1, y: 3.5, w: '80%',
  fontSize: 18, color: '666666',
  align: 'center'
});

// Content slide with bullets
slide = pptx.addSlide();
slide.addText('Key Highlights', {
  x: 0.5, y: 0.5, w: '90%',
  fontSize: 28, bold: true
});
slide.addText([
  { text: 'Revenue grew 25% YoY', options: { bullet: true } },
  { text: 'Customer base expanded to 10,000+', options: { bullet: true } },
  { text: 'New enterprise tier launched', options: { bullet: true, indentLevel: 1 } },
], { x: 0.5, y: 1.5, w: '90%', fontSize: 18 });

// Add chart
slide = pptx.addSlide();
slide.addChart(pptx.ChartType.bar, [
  { name: 'Q1', labels: ['Sales'], values: [100] },
  { name: 'Q2', labels: ['Sales'], values: [150] },
  { name: 'Q3', labels: ['Sales'], values: [180] },
  { name: 'Q4', labels: ['Sales'], values: [225] },
], { x: 1, y: 1.5, w: 8, h: 4 });

await pptx.writeFile({ fileName: 'presentation.pptx' });
```

### Add Charts (Python)

```python
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

# Add slide with chart
chart_layout = prs.slide_layouts[5]  # Blank
slide = prs.slides.add_slide(chart_layout)

# Chart data
chart_data = CategoryChartData()
chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
chart_data.add_series('Revenue', (100, 150, 180, 225))
chart_data.add_series('Expenses', (80, 90, 100, 110))

# Add chart
x, y, cx, cy = Inches(1), Inches(1.5), Inches(8), Inches(5)
chart = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    x, y, cx, cy,
    chart_data
).chart

chart.has_legend = True
chart.legend.include_in_layout = False
```

### Add Images and Tables

```python
# Add image
slide = prs.slides.add_slide(prs.slide_layouts[5])
slide.shapes.add_picture('logo.png', Inches(0.5), Inches(0.5), width=Inches(2))

# Add table
rows, cols = 4, 3
table = slide.shapes.add_table(rows, cols, Inches(1), Inches(2), Inches(8), Inches(3)).table

# Set column headers
table.cell(0, 0).text = 'Product'
table.cell(0, 1).text = 'Sales'
table.cell(0, 2).text = 'Growth'

# Fill data
data = [
    ('Widget A', '$1.2M', '+25%'),
    ('Widget B', '$800K', '+15%'),
    ('Widget C', '$500K', '+40%'),
]
for row_idx, (product, sales, growth) in enumerate(data, 1):
    table.cell(row_idx, 0).text = product
    table.cell(row_idx, 1).text = sales
    table.cell(row_idx, 2).text = growth
```

### Extract Content

```python
from pptx import Presentation

prs = Presentation('existing.pptx')

for slide_num, slide in enumerate(prs.slides, 1):
    print(f"\n--- Slide {slide_num} ---")
    for shape in slide.shapes:
        if shape.has_text_frame:
            for paragraph in shape.text_frame.paragraphs:
                print(paragraph.text)
        if shape.has_table:
            table = shape.table
            for row in table.rows:
                row_text = [cell.text for cell in row.cells]
                print(row_text)
```

---

## Slide Layout Reference

| Layout Index | Name | Use Case |
|--------------|------|----------|
| 0 | Title Slide | Opening, section dividers |
| 1 | Title and Content | Standard bullet slides |
| 2 | Section Header | Section transitions |
| 3 | Two Content | Side-by-side comparison |
| 4 | Comparison | Pros/cons, before/after |
| 5 | Title Only | Custom content placement |
| 6 | Blank | Full creative control |
| 7 | Content with Caption | Image + description |

---

## Presentation Structure Patterns

### Pitch Deck (10 slides)

```text
PITCH DECK STRUCTURE
1. Title (company, tagline)
2. Problem (pain point)
3. Solution (your product)
4. Market Size (TAM/SAM/SOM)
5. Business Model (how you make money)
6. Traction (metrics, growth)
7. Team (founders, advisors)
8. Competition (landscape)
9. Financials (projections)
10. Ask (funding, next steps)
```

### Quarterly Review (8 slides)

```text
QUARTERLY REVIEW STRUCTURE
1. Title + Agenda
2. Executive Summary (KPIs dashboard)
3. Revenue & Growth
4. Product Updates
5. Customer Highlights
6. Challenges & Learnings
7. Next Quarter Goals
8. Q&A
```

---

## Do / Avoid (Dec 2025)

### Do

- Use a slide narrative plan (title + 1-sentence takeaway + supporting visual).
- Put the executive summary up front for decision decks.
- Keep speaker notes aligned with slide takeaways.

### Avoid

- Dense slides with multiple messages.
- Uncited numbers or charts without definitions.
- Pixelated screenshots and unreadable tables.

## What Good Looks Like

- Narrative: each slide has a 1-sentence takeaway and supports a single decision or insight.
- Structure: opening executive summary + clear arc (problem → insight → recommendation → next steps).
- Data hygiene: charts show units, timeframes, sources, and consistent axes.
- Design: consistent typography, spacing, and contrast; no “wall of text” slides.
- Accessibility: reading order set and meaningful alt text where needed.

## Optional: AI / Automation

Use only when explicitly requested and policy-compliant.

- Draft slide headlines and speaker notes; humans verify accuracy and tone.
- Generate chart code from data; humans verify labels, units, and sources.

## Navigation

**Resources**
- [resources/pptx-layouts.md](resources/pptx-layouts.md) — Master slides, themes, templates
- [resources/pptx-charts.md](resources/pptx-charts.md) — Chart types, data visualization
- [data/sources.json](data/sources.json) — Library documentation links

**Templates**
- [templates/pitch-deck.md](templates/pitch-deck.md) — Startup pitch structure
- [templates/quarterly-review.md](templates/quarterly-review.md) — Business review template
- [templates/slide-narrative-template.md](templates/slide-narrative-template.md) — 1-sentence takeaway per slide

**Related Skills**
- [../document-pdf/SKILL.md](../document-pdf/SKILL.md) — Export presentations to PDF
- [../document-xlsx/SKILL.md](../document-xlsx/SKILL.md) — Data source for charts
- [../product-management/SKILL.md](../product-management/SKILL.md) — Product strategy decks
