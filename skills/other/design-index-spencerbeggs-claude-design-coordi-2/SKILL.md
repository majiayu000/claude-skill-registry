---
name: design-index
description: Generate table of contents for design documentation. Use when creating navigation, documentation overview, or module index pages.
allowed-tools: Read, Glob, Bash
context: fork
agent: design-doc-agent
---

# Design Documentation Index Generator

Generates comprehensive table of contents and index pages for design
documentation.

## Overview

This skill scans design documentation, extracts metadata and headings,
organizes documents by category/status/date, and generates indexes in
various formats (Markdown, HTML, JSON). Use it to create navigation
pages, documentation overviews, or structured indexes for design docs.

## Quick Start

**Generate module index:**

```bash
/design-index effect-type-registry
```

**HTML navigation:**

```bash
/design-index all --format=html
```

**Organize by status:**

```bash
/design-index module --organize-by=status
```

## Parameters

### Required

- `module`: Module name to index (or "all" for all modules)

### Optional

- `format`: Output format (markdown, html, json) (default: markdown)
- `organize-by`: Organization method (category, status, alphabetical, date)
  (default: category)
- `output`: Output file path (default: stdout or INDEX.md)
- `include-sections`: Include document sections (default: false)
- `depth`: Heading depth to include (default: 2)

## Workflow

High-level index generation process:

1. **Parse parameters** to determine module, format, and organization
2. **Load design.config.json** to get module paths
3. **Scan documentation** files using Glob
4. **Extract metadata** from frontmatter (status, category, completeness, dates)
5. **Parse headings** up to specified depth
6. **Calculate statistics** (lines, words, sections, code blocks)
7. **Organize documents** by category/status/date/alphabetical
8. **Generate index** in requested format with statistics
9. **Output to file** or stdout

For detailed implementation steps, see supporting documentation below.

## Supporting Documentation

When you need detailed information, load the appropriate supporting file:

### For Detailed Workflow

See [instructions.md](instructions.md) for:

- Complete step-by-step index generation workflow
- Metadata extraction and frontmatter parsing
- Heading extraction algorithms
- Statistics calculation methods
- Organization strategies (category, status, alphabetical, date)
- Format generation for Markdown, HTML, JSON
- Output path resolution
- Advanced features (cross-module indexes, filtering, auto-regeneration)

**Load when:** Generating indexes or need implementation details

### For Templates

See [templates.md](templates.md) for:

- Markdown templates (minimal, standard, detailed)
- HTML template with embedded CSS
- JSON schema and structure
- Statistics section templates
- Format selection guidelines

**Load when:** Need output format specifications or template structure

### For Usage Examples

See [examples.md](examples.md) for:

- Generate module index
- HTML navigation for all modules
- JSON index by status
- Index with sections included
- Alphabetical and date-based organization
- Error scenarios (no docs, invalid organization)

**Load when:** User needs examples or clarification

## Error Handling

### No Documents Found

```text
INFO: No design documents found in {module}

This module has no design documentation yet.
Run /design-init to create your first design doc.
```

### Invalid Organization Method

```text
ERROR: Invalid organization method: {method}
Valid options: category, status, alphabetical, date
```

## Integration

Works well with:

- `/design-review` - Review docs before indexing
- `/design-validate` - Ensure docs are valid
- `/design-export` - Export index with docs
- `/design-update` - Update docs then regenerate index

## Success Criteria

A successful index:

- ✅ All documents discovered
- ✅ Metadata extracted correctly
- ✅ Proper organization applied
- ✅ Valid output format
- ✅ Statistics accurate
- ✅ Links working (for markdown/HTML)
- ✅ Output file created (if specified)
