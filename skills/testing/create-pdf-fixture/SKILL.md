---
name: create-pdf-fixture
description: >
  Create complete PDF test fixtures combining ReportLab tables and AI-generated
  images. Orchestrates create-table and create-image skills. Creates PDFs designed
  to test/expose extractor bugs.
allowed-tools: Bash, Read, Write
triggers:
  - create pdf fixture
  - create test pdf
  - generate pdf fixture
  - make test pdf
  - pdf for testing
  - extractor test fixture
  - bug reproduction pdf
metadata:
  short-description: "Create PDF test fixtures (tables + images)"
---

# create-pdf-fixture

Generate complete PDF test fixtures that combine:
- **Proper ReportLab tables** via `create-table` (detectable by Marker/Camelot)
- **AI-generated images** via `create-image` (diagrams, decorative elements)
- **Text content** with various formatting challenges

## Why This Exists

Creating test PDFs that properly exercise extractors requires:
1. Tables built with ReportLab (not raw drawing commands)
2. Images that test VLM classification (decorative vs data)
3. Edge cases: empty sections, malformed titles, nested structures

This skill orchestrates sibling skills for modular, reusable fixtures.

## Quick Start

```bash
cd .pi/skills/create-pdf-fixture

# Generate the extractor bug reproduction fixture
uv run generate.py extractor-bugs --output test.pdf

# Generate a simple fixture
uv run generate.py simple --output simple_test.pdf

# List available presets
uv run generate.py list-presets

# Verify table detection
uv run generate.py verify test.pdf
```

## Presets

| Preset | Description | Tests |
|--------|-------------|-------|
| `extractor-bugs` | Reproduces known extractor issues | Empty sections, false tables, malformed titles |
| `simple` | Basic PDF with table and text | Basic extraction |

## Sibling Skills Used

| Skill | Purpose |
|-------|---------|
| `create-table` | Creates ReportLab tables (Marker-detectable) |
| `create-image` | AI-generated images with caching |

Cached images from `create-image/cached_images/`:
- `decorative.png` - Cover illustration
- `flowchart.png` - Process diagram
- `network_arch.png` - Architecture diagram

## Legacy Usage (Still Supported)

```bash
# Via wrapper (uses extractor project)
./run.sh --example --name test_fixture
./run.sh --spec content_spec.json --name my_fixture
```

## JSON Spec Format (Legacy)

```json
{
  "style": "standard",
  "sections": [
    {
      "title": "1. Requirements",
      "level": 1,
      "content": [
        {"type": "text", "text": "This document describes requirements."},
        {"type": "table", "columns": ["ID", "Name"], "rows": [["1", "Alice"]]},
        {"type": "figure", "description": "Architecture diagram"}
      ]
    }
  ]
}
```

## Output

- `extractor_bugs_fixture.pdf` - Cached in `cached_fixtures/`
- Custom output via `--output` flag

## Dependencies

```toml
dependencies = [
    "pymupdf>=1.23.0",
    "reportlab>=4.0.0",
    "typer>=0.9.0",
    "pillow>=10.0.0",
]
```
