---
name: extractor
description: >
  Extract content from any document using the Preset-First Agentic Pipeline.
  Auto-detects format and document type (scientific papers, requirements specs, etc.).
  Supports PDF, DOCX, HTML, XML, PPTX, XLSX, EPUB, Markdown, images.
  Use when user says "extract this", "convert to markdown", "process pdf", or provides a document.
allowed-tools: Bash, Read
triggers:
  - extract this
  - extract document
  - extract pdf
  - extract text
  - convert to markdown
  - convert to text
  - parse this file
  - process document
  - process pdf
  - get sections from
  - extract sections
  - run extractor
  - pdf to markdown
  - docx to markdown
  - document to json
metadata:
  short-description: Preset-First document extraction (PDF/DOCX/HTML/XML)
  project-path: /home/graham/workspace/experiments/extractor
---

# Extractor

Self-correcting agentic document extraction using a **Preset-First Methodology**.
Auto-detects document type and applies calibrated extraction settings.

## Quick Start

```bash
# Auto mode (recommended) - detects document type automatically
.pi/skills/extractor/run.sh paper.pdf

# Specify output directory
.pi/skills/extractor/run.sh paper.pdf --out ./results

# Get markdown output directly
.pi/skills/extractor/run.sh paper.pdf --markdown
```

## Extraction Modes

| Mode | Flag | Description |
|------|------|-------------|
| **Auto** | (default) | Profile detector picks best settings |
| **Fast** | `--fast` | PyMuPDF only, no ML/LLM (fastest) |
| **Accurate** | `--accurate` | Full pipeline with LLM enhancements |
| **Offline** | `--offline` | Deterministic, no network calls |

```bash
# Fast mode - quick extraction, no LLM
.pi/skills/extractor/run.sh report.pdf --fast

# Accurate mode - full pipeline with LLM for tables/math
.pi/skills/extractor/run.sh paper.pdf --accurate

# Offline smoke test (deterministic)
.pi/skills/extractor/run.sh doc.pdf --offline
```

## Collaboration Flow

For PDFs without `--preset`, the skill runs an intelligent collaboration flow:

1. **Profile Detection**: Analyzes document (layout, tables, formulas, requirements)
2. **High Confidence Match**: If confidence >= 8, auto-extracts with detected preset
3. **Low Confidence / Unknown**:
   - **Interactive (TTY)**: Prompts user to select preset
   - **Non-interactive**: Uses auto mode with warning

```bash
# See what the detector finds (no extraction)
.pi/skills/extractor/run.sh paper.pdf --profile-only

# Output:
# {
#   "preset": "arxiv",
#   "confidence": 12,
#   "tables": true,
#   "figures": true,
#   "formulas": true,
#   "recommended_mode": "accurate"
# }

# Interactive prompt (in terminal)
.pi/skills/extractor/run.sh unknown_paper.pdf
# Analyzing: unknown_paper.pdf
# Detected: multi-column layout, 12 pages
# Contains: tables, figures, formulas
#
# Select extraction preset:
#   [1] arxiv - Academic papers [RECOMMENDED]
#   [2] requirements_spec - Engineering specs
#   [3] auto - Let pipeline decide
#   [4] fast - Quick extraction, no LLM
# Enter choice [1-4]:

# Non-interactive (batch/CI) - auto-selects
echo | .pi/skills/extractor/run.sh paper.pdf --no-interactive
```

## Preset Selection

The pipeline auto-detects document type via `s00_profile_detector`:

| Preset | Detected When | Confidence Points |
|--------|---------------|-------------------|
| **arxiv** | Academic papers (2-column, math, "Abstract/References") | +5 filename, +4 sections, +3 layout |
| **requirements_spec** | Engineering specs (REQ-xxx, "Shall", nested sections) | +5 filename, +4 REQ pattern |
| **auto** | Unknown documents | Fallback when confidence < 8 |

```bash
# Force a specific preset (skip detection)
.pi/skills/extractor/run.sh paper.pdf --preset arxiv
.pi/skills/extractor/run.sh spec.pdf --preset requirements_spec

# Let collaboration flow decide
.pi/skills/extractor/run.sh paper.pdf
```

## Output Options

```bash
# JSON output (default) - full structured data
.pi/skills/extractor/run.sh doc.pdf --json

# Markdown output - human-readable text
.pi/skills/extractor/run.sh doc.pdf --markdown

# Sections only (skip tables/figures)
.pi/skills/extractor/run.sh doc.pdf --sections-only
```

## Supported Formats

Cross-format parity measured against HTML reference (2026-01-17):

| Format | Method | Parity | Notes |
|--------|--------|--------|-------|
| **Markdown** | Direct parse | 100% | Perfect structural match |
| **DOCX** | Native XML (python-docx) | 100% | Perfect structural match |
| **HTML** | BeautifulSoup | Reference | Baseline for comparison |
| **XML** | defusedxml | 90% | Structure preserved, markdown differs |
| **PDF** | 14-stage pipeline | 87% | Varies by document complexity |
| **RST** | docutils | 85% | Section structure varies |
| **EPUB** | ebooklib | 82% | Chapter structure varies |
| **PPTX** | python-pptx | 81% | Slide-based structure |
| **XLSX** | openpyxl | 16% | Expected (spreadsheet format) |
| **Images** | OCR/VLM | 16% | Requires VLM for text extraction |

## Pipeline Stages

The full pipeline runs 14+ stages:

```
00_profile_detector     Detect document type, select preset
01_annotation_processor Strip PDF annotations
02_marker_extractor     Extract blocks (text, tables, figures)
03_suspicious_headers   Verify header classifications with VLM
04_section_builder      Build document sections
05_table_extractor      Extract and describe tables
06_figure_extractor     Extract and describe figures
07_duckdb_ingest        Assemble into queryable DB
08_extract_requirements Mine requirements (if detected)
08b_lean4_theorem_prover Formal proofs (scientific only)
09_section_summarizer   Generate section summaries
10_markdown_exporter    Export to Markdown
14_report_generator     Generate extraction report
```

## Output Structure

```json
{
  "success": true,
  "preset": "arxiv",
  "outputs": {
    "markdown": "results/10_markdown_exporter/document.md",
    "sections": "results/04_section_builder/json_output/04_sections.json",
    "tables": "results/05_table_extractor/json_output/05_tables.json",
    "figures": "results/06_figure_extractor/json_output/06_figures.json",
    "report": "results/14_report_generator/json_output/final_report.json"
  },
  "counts": {
    "sections": 12,
    "tables": 5,
    "figures": 8
  }
}
```

## Batch Processing

```bash
# Process all PDFs in a directory
.pi/skills/extractor/run.sh ./documents/ --out ./results

# With glob pattern
.pi/skills/extractor/run.sh ./documents/ --glob "**/*.pdf"

# Non-interactive batch (CI/scripts)
.pi/skills/extractor/run.sh ./documents/ --no-interactive

# Force preset for entire batch
.pi/skills/extractor/run.sh ./documents/ --preset arxiv --out ./results
```

## Agent-Friendly Flags

| Flag | Purpose |
|------|---------|
| `--profile-only` | Return profile JSON without extraction |
| `--no-interactive` | Skip prompts, use auto mode |
| `--preset <name>` | Force preset (skip detection) |
| `--fast` | No LLM, quick extraction |
| `--json` | JSON output (default) |

## Environment

Requires the extractor project with its virtual environment:
- **Project**: `/home/graham/workspace/experiments/extractor`
- **Venv**: `.venv/bin/python`
- **Dependencies**: `scillm`, `fetcher` (local paths)

Set `EXTRACTOR_ROOT` to override the project location.

## Sanity Check

```bash
# Verify skill works across all formats
.pi/skills/extractor/sanity.sh
```

Tests: HTML, MD, XML, RST, DOCX, PPTX, EPUB, XLSX, PDF, PNG

## LLM Requirements

For accurate mode (VLM/table descriptions):
- `CHUTES_API_BASE` - Chutes API endpoint
- `CHUTES_API_KEY` - API key
- `CHUTES_VLM_MODEL` - Vision model (default: Qwen/Qwen3-VL-235B-A22B-Instruct)
- `CHUTES_TEXT_MODEL` - Text model (default: moonshotai/Kimi-K2-Instruct-0905)

For Lean4 proving (arxiv preset):
- `lean_runner` container running
- `OPENROUTER_API_KEY` set
