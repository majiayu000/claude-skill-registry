---
name: pdf-merger
description: Merge multiple PDF files into single document with customizable options. Supports page selection, bookmarks, and metadata. Use when combining PDFs, creating documents from multiple sources, or organizing PDF collections.
---

# PDF Merger

## Overview

Merge multiple PDF files into a single document with control over page order, bookmarks, and metadata.

## Quick Start

### Basic Merge

Merge all PDFs in directory:
```bash
python scripts/merge-pdfs.py --input *.pdf --output merged.pdf
```

### Selective Merge

Merge specific files in order:
```bash
python scripts/merge-pdfs.py --input cover.pdf content.pdf appendix.pdf --output document.pdf
```

## Common Use Cases

### Use Case 1: Combine Report Sections

Merge multiple chapter PDFs into complete report:

```bash
python scripts/merge-pdfs.py \
  --input ch1.pdf ch2.pdf ch3.pdf references.pdf \
  --output complete-report.pdf \
  --add-bookmarks
```

### Use Case 2: Extract and Recombine Pages

Merge specific pages from different sources:

```bash
# See references/page-selection.md for syntax
python scripts/merge-pdfs.py \
  --input "doc1.pdf[1-5,10]" "doc2.pdf[3-8]" \
  --output combined.pdf
```

### Use Case 3: Add Metadata

Merge PDFs with custom metadata:

```bash
python scripts/merge-pdfs.py \
  --input *.pdf \
  --output merged.pdf \
  --title "Project Documentation" \
  --author "Your Name" \
  --subject "Technical Documentation"
```

## Features

- ✓ Merge unlimited PDFs
- ✓ Preserve formatting and links
- ✓ Page selection syntax
- ✓ Bookmark generation
- ✓ Metadata customization
- ✓ Progress reporting

## Script Options

```bash
python scripts/merge-pdfs.py [options]

Required:
  --input FILES       PDF files to merge (space-separated)
  --output FILE       Output PDF filename

Optional:
  --add-bookmarks     Create bookmark for each source file
  --title TEXT        Set PDF title metadata
  --author TEXT       Set PDF author metadata
  --subject TEXT      Set PDF subject metadata
  --verbose           Show detailed progress
```

## Advanced Features

For advanced usage including page ranges, rotation, and custom ordering, see [references/advanced-merging.md](references/advanced-merging.md).

For comparison of PDF libraries (PyPDF2, pypdf, pdfrw), see [references/pdf-libraries-comparison.md](references/pdf-libraries-comparison.md).

## Troubleshooting

### Issue: "Corrupted PDF" Error
**Cause**: Source PDF has format issues
**Fix**: Try repairing with `python scripts/repair-pdf.py input.pdf`

### Issue: Large Output File
**Cause**: Images not compressed
**Fix**: Use `--compress` flag to reduce file size

### Issue: Bookmarks Not Created
**Cause**: Missing `--add-bookmarks` flag
**Fix**: Add flag to command

---

**Version**: 1.0
**Last Updated**: October 25, 2025
**Example Type**: Medium skill (SKILL.md + references + script)
