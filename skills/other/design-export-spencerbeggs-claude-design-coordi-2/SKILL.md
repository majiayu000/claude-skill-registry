---
name: design-export
description: Export to PDF/HTML/markdown. Use when distributing documentation, creating presentations, or archiving design docs.
allowed-tools: Read, Glob, Bash
context: fork
agent: design-doc-agent
---

# Design Documentation Export

Exports design documentation to various formats (PDF, HTML, markdown) for
distribution, presentation, or archival purposes.

## Overview

This skill exports design docs by collecting documents across modules,
preparing content with resolved links and processed images, generating
exports in requested formats using Pandoc, applying styling and theming,
creating table of contents, and producing professional output files.

## Quick Start

**Export to PDF:**

```bash
/design-export --format=pdf
```

**Export specific module to HTML:**

```bash
/design-export effect-type-registry --format=html
```

**Export to multiple formats:**

```bash
/design-export --format=pdf,html,markdown
```

## Parameters

### Optional

- `module`: Specific module to export (default: all modules)
- `format`: Output format - pdf, html, markdown, or comma-separated list
  (default: pdf)
- `output`: Custom output path (default: `.claude/exports/design-docs-{date}.{ext}`)
- `include-archived`: Include archived docs (default: false)
- `standalone`: Create self-contained file (default: true)

## Workflow

High-level export process:

1. **Parse parameters** to determine module scope, format, and options
2. **Load design.config.json** to get module paths and export settings
3. **Collect documents** based on scope and filters
4. **Prepare content** (process frontmatter, resolve links, handle images)
5. **Generate export** using Pandoc or direct markdown processing
6. **Apply styling** (format-specific themes and layouts)
7. **Generate table of contents** with navigation structure
8. **Write export file** to output path
9. **Generate metadata** file with export details
10. **Report results** with summary and file location

For detailed implementation steps, see supporting documentation below.

## Supporting Documentation

When you need detailed information, load the appropriate supporting file:

### For Detailed Workflow

See [instructions.md](instructions.md) for:

- Complete step-by-step export workflow
- Document collection and filtering
- Content preparation (links, images, frontmatter)
- Export generation for each format
- Styling application
- TOC generation algorithms
- Metadata creation
- Advanced features (batch export, selective export, incremental,
  templates)

**Load when:** Performing exports or need implementation details

### For Export Formats

See [export-formats.md](export-formats.md) for:

- PDF format specifications (Pandoc commands, LaTeX templates, options)
- HTML format specifications (structure, CSS, JavaScript)
- Markdown format specifications (organization, frontmatter handling)
- Format comparison and selection guidelines
- Requirements and dependencies

**Load when:** Need format specifications or Pandoc command details

### For Usage Examples

See [examples.md](examples.md) for:

- Export all modules to PDF
- Export specific module to HTML
- Multi-format export
- Standalone markdown export
- Custom output path
- Error scenarios (Pandoc not found, invalid format)

**Load when:** User needs examples or clarification

## Error Handling

### Pandoc Not Found

```text
ERROR: Pandoc not installed

PDF and HTML export require Pandoc.

Install: brew install pandoc (macOS)
or visit https://pandoc.org/installing.html
```

### LaTeX Engine Missing

```text
ERROR: LaTeX engine not found

PDF export requires XeLaTeX or PDFLaTeX.

Install: brew install --cask mactex (macOS)
```

### Invalid Format

```text
ERROR: Invalid export format: {format}

Valid formats: pdf, html, markdown

Example: /design-export --format=pdf
```

## Integration

Works well with:

- `/design-review` - Review docs before exporting
- `/design-validate` - Ensure docs valid before export
- `/design-sync` - Sync docs before exporting
- `/design-prune` - Clean docs before exporting

## Success Criteria

A successful export:

- ✅ All target documents collected
- ✅ Content properly prepared (links resolved, images handled)
- ✅ Export generated in requested format(s)
- ✅ Styling applied correctly
- ✅ Table of contents included
- ✅ Metadata file created
- ✅ Output file created at specified location
- ✅ Clear export summary provided
