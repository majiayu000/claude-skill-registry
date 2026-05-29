---
name: pdf-fixture
description: >
  Generate test PDF fixtures with known, extractable content. Creates PDFs with
  sections, tables, figures, requirements, equations, and annotations. Use when
  user needs "create test PDF", "generate PDF fixture", "make sample PDF for testing".
allowed-tools: Bash, Read, Write
triggers:
  - create test PDF
  - generate PDF fixture
  - make sample PDF
  - PDF for testing
  - create PDF with tables
metadata:
  short-description: Create test PDF fixtures from JSON specs
---

# PDF Fixture Generator

Generate deterministic test PDFs with known, extractable content for testing extraction pipelines.

**Self-contained skill** - auto-installs via `uv run` from git (no pre-installation needed).

## Simplest Usage

```bash
# Via wrapper (recommended - auto-installs)
.agents/skills/pdf-fixture/run.sh --example --name test_fixture
```

## Common Patterns

### Create from JSON spec file
```bash
./run.sh --spec content_spec.json --name my_fixture
```

### Create from inline JSON
```bash
./run.sh \
  --inline '{"sections": [{"title": "Introduction", "content": [{"type": "text", "text": "Hello world"}]}]}' \
  --name inline_test
```

## JSON Spec Format

```json
{
  "style": "standard",
  "sections": [
    {
      "title": "1. Requirements",
      "level": 1,
      "content": [
        {"type": "text", "text": "This document describes requirements."},
        {"type": "requirement", "id": "REQ-001", "text": "System shall process in 1s"},
        {"type": "table", "columns": ["ID", "Name"], "rows": [["1", "Alice"], ["2", "Bob"]]},
        {"type": "equation", "latex": "E = mc^2", "label": "energy"},
        {"type": "figure", "description": "Architecture diagram"}
      ]
    }
  ]
}
```

## Content Types

| Type | Required Fields | Optional |
|------|-----------------|----------|
| `text` | `text` | - |
| `requirement` | `id`, `text` | `type` (Functional/NonFunctional) |
| `table` | `columns` | `rows` (list or count) |
| `equation` | `latex` or `equation` | `label` |
| `figure` | `description` | `width`, `height` |
| `annotation` | `annot_type` (highlight/note/box) | `content` |

## Output

Creates in `fixtures/{name}/`:
- `source.pdf` - Generated PDF with known content
- `SPEC.md` - Auto-generated with expected extraction values

## Notes

The wrapper script (`run.sh`) automatically:
- Installs extractor from git via `uv run`
- Handles all dependencies (PyMuPDF, etc.)
- No manual venv activation needed
