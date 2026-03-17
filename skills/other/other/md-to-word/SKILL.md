---
name: "md-to-word"
description: "Convert Markdown with Mermaid diagrams to professional Word documents"
version: "2.0.0"
---

# Markdown to Word Conversion

> One command to professional Word documents with perfect diagram sizing

Convert any Markdown document, including complex Mermaid diagrams, into polished Word (.docx) files ready for stakeholders, executives, and external audiences.

## Document Publishing Workflow

The complete workflow from Markdown to final PDF:

1. **Convert to Word**: run `md-to-word.py` to generate a .docx with styled tables, centered diagrams, and formatted headings
2. **Manual formatting**: open in Word and make final adjustments (page breaks, margins, headers/footers, custom styling)
3. **Save as PDF**: use Word's File > Save As > PDF to produce the final PDF with full fidelity

This skill handles step 1. Steps 2 and 3 are manual because Word provides superior PDF rendering, font embedding, and layout control compared to automated Markdown-to-PDF pipelines.

## Why This Skill?

| Challenge | Solution |
|-----------|----------|
| Mermaid diagrams don't render in Word | Auto-converted to PNG with optimal sizing |
| Tables lack professional styling | Blue headers, borders, alternating rows |
| Tables break awkwardly across pages | Smart pagination (cantSplit + keepWithNext) |
| Images overflow page boundaries | 90% coverage constraint (H+V) preserves fit |
| Bullet lists merge into paragraphs | Markdown preprocessing fixes spacing |
| SVG banners not supported | Auto-converted to PNG |

---

## Quick Start

### One-Command Conversion

```powershell
# From your project root
python .github/muscles/md-to-word.py docs/spec.md

# With custom output name
python .github/muscles/md-to-word.py README.md output.docx

# Keep intermediate files for debugging
python .github/muscles/md-to-word.py docs/plan.md --keep-temp
```

### What It Does

1. **Preprocesses Markdown** — fixes bullet lists, checkbox syntax, spacing
2. **Converts Mermaid to PNG** — renders diagrams with white backgrounds
3. **Calculates optimal sizing** — reads actual PNG dimensions, fits 90% of page
4. **Converts SVG to PNG** — handles banner images
5. **Generates Word via pandoc** — clean markdown-to-docx conversion
6. **Formats tables** — Microsoft blue headers, borders, alternating rows
7. **Centers images** — all diagrams centered on page
8. **Styles headings** — consistent colors and spacing

---

## Installation

### Prerequisites

| Tool | Install Command | Purpose |
|------|-----------------|---------|
| **Python 3.10+** | (system) | Script runtime |
| **pandoc** | `winget install pandoc` | Markdown to Word |
| **mermaid-cli** | `npm install -g @mermaid-js/mermaid-cli` | Mermaid to PNG |
| **python-docx** | `pip install python-docx` | Table formatting |
| **svgexport** | `npm install -g svgexport` | SVG to PNG (optional) |

### Quick Install (All Dependencies)

```powershell
winget install pandoc
npm install -g @mermaid-js/mermaid-cli svgexport
pip install python-docx
```

---

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--images-dir` | `images` | Directory for generated PNG files |
| `--no-format-tables` | false | Skip table styling (faster) |
| `--keep-temp` | false | Keep temporary markdown file |

---

## Image Sizing Algorithm

The script automatically fits images to 90% of page bounds:

```
Page: 8.5" x 11" (Letter)
Margins: 1" each side
Usable: 6.5" x 9.0"
Max image: 5.85" x 8.1" (90%)
```

### How It Works

1. **Read PNG dimensions** from file header (no Pillow needed)
2. **Calculate scale factors** for width and height constraints
3. **Apply most restrictive** — ensures fit in both dimensions
4. **Specify one dimension** — pandoc preserves aspect ratio

| Diagram Type | Typical Constraint |
|--------------|-------------------|
| Gantt (wide) | `{width=5.8in}` |
| Flowchart TB (tall) | `{height=8.1in}` |
| Architecture layers | `{width=5.8in}` |
| Escalation maps | `{height=8.1in}` |

---

## Table Formatting

All tables receive professional styling:

| Element | Style |
|---------|-------|
| **Header row** | Microsoft blue (#0078D4), white text, bold |
| **Even rows** | Light gray (#F0F0F0) |
| **Odd rows** | White (#FFFFFF) |
| **Borders** | Gray outer (#666666), light inner (#AAAAAA) |
| **Font** | 10pt headers, 9pt data |
| **Pagination** | Rows don't split; headers stay with data |

---

## Supported Diagram Types

| Type | Detection | Sizing Strategy |
|------|-----------|-----------------|
| Gantt | `gantt` keyword | Width priority |
| Flowchart LR | `flowchart lr` | Width priority |
| Flowchart TB | `flowchart tb` | Height priority |
| Sequence | `sequenceDiagram` | Width priority |
| Class | `classDiagram` | Auto |
| ER | `erDiagram` | Auto |
| Pie | `pie` | Smaller width |

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| "mmdc not found" | mermaid-cli not installed | `npm install -g @mermaid-js/mermaid-cli` |
| "pandoc not found" | pandoc not in PATH | `winget install pandoc`, restart terminal |
| Tables not styled | python-docx missing | `pip install python-docx` |
| Diagrams too large | Old script version | Update to v2.0.0 with 90% H+V |
| Bullet lists merged | Markdown spacing | Script auto-fixes (v2.0.0+) |

### Debug Mode

```powershell
python .github/muscles/md-to-word.py doc.md --keep-temp
# Check _temp_word.md for transformed content
```

---

## For Heir Projects

### Setup

1. Copy `.github/muscles/md-to-word.py` to your project
2. Install prerequisites (see Installation)
3. Run on any markdown file

### Example Integration

```powershell
# Convert entire docs folder
Get-ChildItem docs/*.md | ForEach-Object {
    python .github/muscles/md-to-word.py $_.FullName
}
```

---

## Version History

| Version | Changes |
|---------|---------|
| **2.1.0** | Table pagination (cantSplit, keepWithNext) prevents orphan headers |
| **2.0.0** | 90% H+V coverage, actual PNG dimension reading, markdown preprocessing |
| **1.1.0** | Centered images, heading colors, paragraph spacing |
| **1.0.0** | Initial: pandoc + mermaid + table formatting |

---

## Related Skills

- **markdown-mermaid** — Mermaid syntax and ATACCU compliance
- **brand-asset-management** — SVG banner guidelines
- **pptx-generation** — Similar workflow for PowerPoint
- **svg-graphics** — Vector graphics for documentation
