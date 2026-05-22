---
name: "PPTX Generation"
description: "Programmatic PowerPoint creation via PptxGenJS with data-driven slides and Markdown conversion"
---

# PPTX Generation Skill

**Domain**: Presentation Generation  
**Purpose**: Programmatic PowerPoint creation via PptxGenJS  
**Expertise**: Data-driven slides, Markdown conversion, Alex brand templates  

---

## Capabilities

| Capability | Description |
|------------|-------------|
| **Markdown → PPTX** | Convert `.md` files to branded presentations |
| **Data-Driven Slides** | Generate charts/tables from JSON data |
| **Template System** | Alex brand Slide Masters (title, content, section, chart) |
| **Multi-Format Export** | File output or base64 for web delivery |

---

## Activation Triggers

- "create presentation", "generate slides", "make pptx"
- "convert markdown to powerpoint", "md to pptx"
- "data visualization slides", "chart presentation"
- "alex branded deck", "presentation template"

---

## Slide Types

| Type | Use Case | Data Shape |
|------|----------|-----------|
| `title` | Opening slide with main title + subtitle | `{ title, subtitle?, notes? }` |
| `content` | Bullet list slide | `{ title, bullets[], notes? }` |
| `section` | Section divider | `{ title, subtitle? }` |
| `chart` | Data visualization | `{ chartType, series[], title? }` |
| `table` | Tabular data | `{ headers[], rows[][] }` |
| `image` | Image slide | `{ path\|base64, caption? }` |
| `twoColumn` | Side-by-side content | `{ left: {title, bullets}, right: {title, bullets} }` |

---

## Chart Types

- `bar` — Category comparison
- `line` — Trend over time
- `pie` — Part-of-whole (use ≤6 segments)
- `doughnut` — Pie variant with center hole
- `area` — Volume over time
- `scatter` — Correlation analysis

---

## Alex Brand Colors

| Name | Fill | Text | Border |
|------|------|------|--------|
| Blue | `ddf4ff` | `0550ae` | `80ccff` |
| Green | `d3f5db` | `1a7f37` | `6fdd8b` |
| Purple | `d8b9ff` | `6639ba` | `bf8aff` |
| Gold | `fff8c5` | `9a6700` | `d4a72c` |
| Gray | `eaeef2` | `24292f` | `afb8c1` |

---

## Example: Markdown Input

```markdown
# Quarterly Review

## Executive Summary

---

# Q4 2024 Results

## Performance Overview

- Revenue up 23% YoY
- Customer acquisition: 1,200 new accounts
- NPS improved from 45 to 62

> Speaker notes: Highlight the NPS improvement as key win

---

## Next Quarter [section]

Focus areas for Q1 2025

---

# Strategic Priorities

- Expand enterprise segment
- Launch self-serve tier
- Hire 15 engineers
```

---

## Example: Programmatic API

```typescript
import { generateAndSavePresentation, SlideContent } from './pptxGenerator';

const slides: SlideContent[] = [
    { type: 'title', title: 'Q4 Review', subtitle: 'Performance & Strategy' },
    { type: 'content', title: 'Highlights', bullets: ['Revenue +23%', 'NPS 62'] },
    { type: 'chart', title: 'Revenue Trend', data: {
        chartType: 'line',
        series: [{ name: 'Revenue', labels: ['Q1','Q2','Q3','Q4'], values: [100,120,115,146] }]
    }}
];

await generateAndSavePresentation(slides, { title: 'Q4 Review' }, 'review.pptx');
```

---

## CLI Usage

```bash
# From markdown
npx ts-node .github/muscles/pptxgen-cli.ts --input slides.md --output deck.pptx

# Quick content
npx ts-node .github/muscles/pptxgen-cli.ts --content "Welcome to Alex|Point 1|Point 2" -o quick.pptx
```

---

## Integration Points

| Integration | Description |
|-------------|-------------|
| **Chat command** | `/pptx <topic>` to generate slides from topic |
| **Memory export** | Convert episodic memories to slides |
| **Skill output** | Any skill can request PPTX output |
| **Data connectors** | Azure SQL / Power BI → charts |

---

## Constraints

- Offline-only (no cloud dependencies)
- 16:9 default layout (4:3, 16:10 available)
- Max recommended: 50 slides per deck
- Images: local path, URL, or base64
