---
name: debug-pdf
description: >
  Automated PDF failure analysis and fixture generation. Takes failed PDF URLs,
  identifies breaking patterns, and generates minimal fixtures via fixture-tricky
  for regression testing. Supports batch mode and combined stress test generation.
allowed-tools: Bash, Read, Write, Web
triggers:
  - debug pdf
  - analyze pdf failure
  - create pdf fixture from url
  - why did extraction fail
  - batch analyze pdf failures
  - combine pdf fixtures
metadata:
  short-description: Failure-to-fixture automation for PDF extractors
---

# Debug PDF Skill

Automate the lifecycle of an extraction failure: **Failure -> Analysis -> Fixture -> Test**

## Why This Exists

Extractors (Marker, Surya, Camelot) break on specific PDF patterns (scanned pages, TOC dots, cursed fonts, watermarks).
Manually reproducing these bugs is slow. `/debug-pdf` fast-tracks this by:

1. Downloading the failed artifact
2. Identifying structural "traps" (TOC dots, watermarks, ligatures, etc.)
3. Generating minimal reproduction fixtures using `fixture-tricky`
4. Combining multiple failures into a single stress test PDF

## Quick Start

```bash
# Analyze a single failed URL
./run.sh analyze "https://example.com/broken.pdf"

# Process multiple failures in batch
./run.sh batch failed_urls.txt --output report.json

# Combine all fixtures into one stress test PDF
./run.sh combine stress_test.pdf --max-pages 20

# List known failure patterns
./run.sh list-patterns

# Check session status
./run.sh status
```

## Commands

### analyze <url>
Analyze a single PDF URL and optionally generate a reproduction fixture.

```bash
./run.sh analyze "https://example.com/broken.pdf"
./run.sh analyze "https://example.com/broken.pdf" --no-repro
./run.sh analyze "https://example.com/broken.pdf" --send-inbox
```

### batch <url-file>
Process multiple URLs from a file (one URL per line).

```bash
# Create URL file
echo "https://example.com/doc1.pdf" > failed.txt
echo "https://example.com/doc2.pdf" >> failed.txt

# Run batch analysis
./run.sh batch failed.txt --output analysis.json --send-inbox
```

### combine [output.pdf]
Merge all generated fixtures into a single stress test PDF.

```bash
./run.sh combine stress_test.pdf --max-pages 15
```

### list-patterns
Display all known failure patterns and their descriptions.

### status
Show current debug session status and fixture count.

## Detected Patterns (14/17 = 82%)

**Structural (4/4 detected):**
- `scanned_no_ocr` - Scanned image PDF without text layer
- `sparse_content_slides` - Slide deck with minimal text per page
- `multi_column` - Complex multi-column layouts (via text block analysis)
- `watermarks` - Text obscured by watermark overlays

**Encoding (5/5 detected):**
- `toc_noise` - Table of contents with dotted leaders
- `metadata_artifacts` - Print metadata (Jkt/PO/Frm) in content
- `invisible_chars` - Zero-width spaces, direction markers
- `curly_quotes` - Windows-1252 encoded smart quotes
- `ligatures` - fi/fl/ff ligature characters

**Layout (4/4 detected):**
- `footnotes_inline` - Footnotes merged into body text (via font size/position heuristics)
- `split_tables` - Tables spanning multiple pages (flag only, no merging)
- `header_footer_bleed` - Headers/footers mixed into content (via PyMuPDF4LLM Layout)
- `diagram_heavy` - Many embedded diagrams/charts

**Network (1/3 detected locally):**
- `archive_org_wrap` - Wayback Machine URL wrapper (detected via URL pattern)
- `auth_required` - Marketing platform cookie gates (network-level, not detectable locally)
- `access_restricted` - Government/defense access controls (network-level, not detectable locally)

## Workflow Integration

When `memory` or `extractor` agent reports failures:

1. Collect failed URLs in a text file
2. Run batch analysis: `./run.sh batch failed_urls.txt`
3. Review pattern distribution in output
4. Generate combined stress test: `./run.sh combine stress_test.pdf`
5. Add stress test to extractor's regression suite
6. New patterns get added to `fixture-tricky` for future testing

## Data Storage

All data is stored in `~/.pi/debug-pdf/`:
- `sessions/` - Individual analysis session JSON files
- `fixtures/` - Generated reproduction PDFs
- `last_analysis.json` - Quick reference to most recent analysis

## Dependencies

- `pymupdf` (fitz) - PDF structure analysis
- `pymupdf4llm` - ML-based layout detection for header/footer bleed
- `httpx` - HTTP downloads with redirect handling
- `typer` - CLI interface
- `loguru` - Logging

Sibling skills used:
- `fetcher` - Robust URL downloading with Playwright support
- `fixture-tricky` - Adversarial PDF generation
- `extractor` - Verification of generated fixtures
- `agent-inbox` - Cross-agent notifications

## Testing

```bash
# Run test suite (24 tests)
python -m pytest tests/test_debug_pdf.py -v

# Generate test fixtures only
python tests/test_debug_pdf.py
```

Test coverage includes:
- URL validation (security hardening)
- Wayback URL detection and extraction
- Multi-column layout detection
- Header/footer bleed detection
- Split table detection
- Footnote detection
- Full PDF analysis integration

## Sanity Check

```bash
./sanity.sh
```

Verifies:
- Python dependencies installed
- Sibling skills available
- Data directory accessible
- CLI commands functional
