---
name: fixture-tricky
description: >
  Generate adversarial PDF content that breaks extractors. Creates false-positive
  tables, malformed tables, cursed text, and layout traps. Extensible registry
  for adding new edge cases discovered from real-world PDFs.
allowed-tools: Bash, Read, Write
triggers:
  - create tricky pdf
  - false positive table
  - malformed table
  - broken table
  - extractor edge case
  - adversarial pdf
  - cursed text
metadata:
  short-description: Adversarial PDF content for extractor stress testing
---

# Fixture Tricky Skill

Generate adversarial PDF content designed to expose extractor bugs. Continuously
extensible as new edge cases are discovered from real-world PDFs.

## Why This Exists

Real-world PDFs contain patterns that reliably break extractors:
- Text that Camelot/Marker falsely detect as tables
- Tables corrupted by Word/PDF conversions
- Text with ligatures, special characters, mixed directions
- Layout patterns that confuse section detection

This skill creates reproducible test cases for these issues.

## Quick Start

```bash
cd .pi/skills/fixture-tricky

# Generate false-positive table content
uv run generate.py false-tables --output false_tables.pdf

# Generate malformed/corrupted tables
uv run generate.py malformed-tables --output malformed.pdf

# Generate text extraction nightmares
uv run generate.py cursed-text --output cursed.pdf

# Generate layout traps
uv run generate.py layout-traps --output layout.pdf

# All-in-one stress test
uv run generate.py gauntlet --output gauntlet.pdf

# List all available tricks
uv run generate.py list-tricks
```

## Trick Categories

### False-Positive Tables (`false-tables`)

Text patterns that extractors incorrectly identify as tables:

| Trick | Description |
|-------|-------------|
| `numbered-list` | "1. Item one\n2. Item two" with aligned numbers |
| `address-block` | Multi-line addresses with aligned fields |
| `code-block` | Indented code with column-like alignment |
| `signature-block` | Name/title/date aligned like table rows |
| `key-value-pairs` | "Key: Value" patterns in sequence |
| `multi-column` | Two-column text layout |
| `toc-entries` | Table of contents with dotted leaders |

### Malformed Tables (`malformed-tables`)

Real tables with structural problems:

| Trick | Description |
|-------|-------------|
| `missing-columns` | Rows with fewer cells than header (Word import bug) |
| `ragged-rows` | Inconsistent column counts across rows |
| `merged-chaos` | Excessive cell merging breaking structure |
| `split-table` | Table split across page break |
| `nested-tables` | Tables inside table cells |
| `borderless` | No visible borders (detection challenge) |
| `partial-borders` | Some borders missing |
| `misaligned-columns` | Columns that don't line up |

### Cursed Text (`cursed-text`)

Text extraction nightmares:

| Trick | Description |
|-------|-------------|
| `ligatures` | fi, fl, ff, ffi, ffl characters |
| `math-symbols` | Equations with special notation |
| `mixed-scripts` | Latin + Greek + Cyrillic |
| `rtl-mixed` | Right-to-left text mixed with LTR |
| `subscript-superscript` | Chemical formulas, footnote markers |
| `invisible-chars` | Zero-width spaces, soft hyphens |
| `encoding-hell` | Characters that look alike but aren't |

### Layout Traps (`layout-traps`)

Structure/layout patterns that confuse extractors:

| Trick | Description |
|-------|-------------|
| `deep-nesting` | 10+ levels of section hierarchy |
| `footnote-sections` | Footnotes that look like new sections |
| `sidebar` | Marginal notes alongside main text |
| `pull-quote` | Large quoted text in middle of content |
| `watermark` | Text overlaid with watermark |
| `rotated-text` | 90° rotated text blocks |
| `floating-elements` | Content out of reading order |

## Adding New Tricks

Tricks are registered in `tricks/registry.py`. To add a new trick:

```python
# In tricks/registry.py
from .my_new_trick import generate_my_trick

TRICKS["my-new-trick"] = {
    "category": "false-tables",  # or malformed-tables, cursed-text, layout-traps
    "description": "Description of what this trick tests",
    "generator": generate_my_trick,
}
```

Or add directly to `generate.py` in the appropriate category dict.

## Integration with pdf-fixture

Use with `pdf-fixture` to create comprehensive test suites:

```bash
# Generate clean fixture
cd ../pdf-fixture && uv run generate.py simple --output clean.pdf

# Generate tricky fixture
cd ../fixture-tricky && uv run generate.py gauntlet --output tricky.pdf

# Compare extractor results on both
```

## Real-World Discovery Workflow

When you find a PDF that breaks the extractor:

1. Identify the problematic pattern
2. Add a new trick that reproduces it minimally
3. Run `skills-sync` to broadcast
4. Use the trick in regression testing

```bash
# Example: Found a PDF where Camelot detects email signatures as tables
uv run generate.py add-trick \
  --name "email-signature" \
  --category "false-tables" \
  --description "Email signature blocks with name/title/phone"
```

## Dependencies

```toml
dependencies = [
    "pymupdf>=1.23.0",
    "reportlab>=4.0.0",
    "typer>=0.9.0",
]
```
