---
name: fixture-table
description: >
  Generate PDF tables using ReportLab Table class for proper structure detection.
  Creates tables that Marker and other extractors can actually parse, unlike raw
  PDF drawing commands. Use when user needs detectable tables in test fixtures.
allowed-tools: Bash, Read, Write
triggers:
  - create detectable table
  - generate reportlab table
  - fixture table
  - table that marker can detect
  - proper pdf table
  - scanned table image
metadata:
  short-description: ReportLab tables for extraction testing (Marker-detectable)
---

# Fixture Table Skill

Generate PDF tables using ReportLab's `Table` class that extractors (Marker, Camelot) can detect.

## Why This Exists

PyMuPDF raw drawing commands (`draw_line`, `insert_text`) create visual tables but **not** proper PDF table structures. Marker and other extractors cannot detect these as tables.

ReportLab's `Table` class creates proper PDF table structures with cell boundaries that extraction tools recognize.

## Quick Start

```bash
cd .codex/skills/fixture-table

# Generate from preset (simple, medium, complex)
uv run generate.py preset simple
uv run generate.py preset complex --output my_table.pdf

# Generate with custom data
uv run generate.py generate --output custom.pdf \
  --columns "ID,Name,Status" \
  --rows '[["1","Alice","Active"],["2","Bob","Pending"]]'

# Borderless table
uv run generate.py generate --no-border --output borderless.pdf

# Thick borders (3pt)
uv run generate.py generate --line-width 3 --output thick.pdf

# Render as image (for scanned document testing)
uv run generate.py preset medium --as-image --dpi 200

# Generate all examples
uv run generate.py example
```

## Commands

### `preset` - Generate from preset complexity

```bash
uv run generate.py preset <name> [options]
```

| Preset | Description |
|--------|-------------|
| `simple` | 3x3 basic table |
| `medium` | 8-row requirements matrix with 6 columns |
| `complex` | Multi-index headers with column spans |

### `generate` - Create custom table

```bash
uv run generate.py generate [options]
```

**Options:**
| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output PDF/PNG path | `table_fixture.pdf` |
| `--columns` | `-c` | Comma-separated column headers | `ID,Name,Value` |
| `--rows` | `-r` | JSON array of row data | 3 sample rows |
| `--spec` | `-s` | JSON spec file path | - |
| `--title` | `-t` | Table title text | - |
| `--style` | | `grid`, `plain`, `colored` | `grid` |
| `--border/--no-border` | | Enable or disable borders | `--border` |
| `--line-width` | `-w` | Border thickness in points | `1.0` |
| `--multi-index` | `-m` | JSON multi-index headers | - |
| `--as-image` | `-i` | Render as PNG image | `False` |
| `--dpi` | | Image resolution | `150` |

### `example` - Generate all examples

```bash
uv run generate.py example
```

Creates `examples/` directory with all presets, styles, and border variations.

## Multi-Index Tables

For hierarchical headers that span columns:

```bash
uv run generate.py generate \
  --columns "ID,Q1,Q2,Q3,Q4,Total" \
  --rows '[["A","10","20","30","40","100"]]' \
  --multi-index '[[{"text":"","span":1},{"text":"2024 Quarters","span":4},{"text":"","span":1}]]'
```

Or in JSON spec:
```json
{
  "columns": ["ID", "Q1", "Q2", "Q3", "Q4", "Total"],
  "rows": [["A", "10", "20", "30", "40", "100"]],
  "multi_index": [
    [{"text": "", "span": 1}, {"text": "2024 Quarters", "span": 4}, {"text": "", "span": 1}]
  ]
}
```

## Scanned Document Simulation

Generate table as a rasterized PNG image (for testing OCR/VLM extraction):

```bash
# 150 DPI (default)
uv run generate.py preset medium --as-image

# Higher quality (300 DPI)
uv run generate.py preset complex --as-image --dpi 300 --output scanned_table.png
```

## Verification

Test that Camelot detects the table:

```bash
uv run generate.py preset simple --output test.pdf

python -c "
import camelot
tables = camelot.read_pdf('test.pdf', pages='1', flavor='lattice')
print(f'Tables found: {len(tables)}')
if tables:
    print(tables[0].df)
"
```

## Dependencies

Self-contained via `uv run` - no pre-installation needed.

```toml
[project]
dependencies = [
    "reportlab>=4.0.0",
    "typer>=0.9.0",
    "pymupdf>=1.23.0",
]
```
