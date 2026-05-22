---
name: pptx
description: >-
  Create, edit, and analyze PowerPoint presentations (.pptx). Supports three
  workflows: (1) creating new presentations from scratch using HTML-to-PPTX
  conversion via html2pptx.js, (2) editing existing presentations by
  unpacking and modifying Office Open XML, and (3) creating presentations
  from templates with slide rearrangement and text replacement. Trigger when
  the user asks to build, modify, or inspect any .pptx file.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - WebFetch
  - WebSearch
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - builder
    - presentation
    - pptx
    - office
  provenance:
    upstream_source: "pptx"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T22:00:00+00:00"
    generator_version: "1.0.0"
    intent_confidence: 0.61
---

# PPTX Builder

Create, edit, and analyze PowerPoint presentations with three distinct workflows and bundled helper scripts.

## Overview

This skill provides everything needed to work with `.pptx` files. A PPTX file is a ZIP archive of XML files and resources. Depending on the task, choose one of three workflows below.

**What it creates:**
- New presentations from scratch (HTML-to-PPTX pipeline)
- Modified versions of existing presentations (OOXML editing)
- Template-based presentations (slide rearrangement and text replacement)

**Key features:**
- Bundled `html2pptx.js` for pixel-accurate HTML-to-slide conversion
- OOXML validation after every edit to prevent corrupt files
- Visual thumbnail generation for quality checking
- Text inventory extraction and batch replacement for templates

## Workflow 1: Create From Scratch (html2pptx)

Use this when building a new presentation without an existing template.

### Step 1: Read the html2pptx Guide

Read [`references/html2pptx-guide.md`](references/html2pptx-guide.md) completely before proceeding.

### Step 2: Design the Presentation

Before writing code, analyze content and choose design elements:

1. **Consider the subject matter** -- what tone, industry, or mood?
2. **Check for branding** -- user-mentioned company/organization colors
3. **Match palette to content** -- pick 3-5 colors (dominant + supporting + accent)
4. **State your approach** -- explain design choices before writing code

Requirements:
- Use web-safe fonts only: Arial, Helvetica, Times New Roman, Georgia, Courier New, Verdana, Tahoma, Trebuchet MS, Impact
- Ensure strong contrast and clear visual hierarchy
- Be consistent across slides

See [`references/design-reference.md`](references/design-reference.md) for color palettes and layout options.

### Step 3: Create HTML Slides

Create one HTML file per slide with proper dimensions:
- **16:9**: `width: 720pt; height: 405pt`
- **4:3**: `width: 720pt; height: 540pt`

Critical rules:
- ALL text must be in `<p>`, `<h1>`-`<h6>`, `<ul>`, or `<ol>` tags -- bare `<div>` text is silently dropped
- Never use manual bullet symbols -- use `<ul>`/`<ol>` lists
- Never use CSS gradients -- rasterize to PNG with Sharp first
- Backgrounds/borders/shadows only work on `<div>` elements, not text tags
- Use `class="placeholder"` for areas where charts/tables will be added later

### Step 4: Convert and Assemble

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';

const { slide, placeholders } = await html2pptx('slide1.html', pptx);
// Add charts/tables to placeholder areas using PptxGenJS API
await pptx.writeFile('output.pptx');
```

### Step 5: Visual Validation

```bash
python scripts/thumbnail.py output.pptx workspace/thumbnails --cols 4
```

Read the thumbnail image and check for text cutoff, overlap, positioning issues, and contrast problems. Adjust HTML and regenerate until all slides are visually correct.

## Workflow 2: Edit Existing Presentation (OOXML)

Use this when modifying slides in an existing `.pptx` file.

### Step 1: Read the OOXML Reference

Read [`references/ooxml-reference.md`](references/ooxml-reference.md) completely before proceeding.

### Step 2: Unpack

```bash
python ooxml/scripts/unpack.py <file.pptx> <output_dir>
```

### Step 3: Edit XML

Edit files in `ppt/slides/slide{N}.xml` and related files. Key paths:
- `ppt/presentation.xml` -- slide references and metadata
- `ppt/slides/slide{N}.xml` -- individual slide content
- `ppt/notesSlides/notesSlide{N}.xml` -- speaker notes
- `ppt/theme/theme1.xml` -- colors and fonts
- `ppt/media/` -- images and media

### Step 4: Validate After Each Edit

```bash
python ooxml/scripts/validate.py <dir> --original <file.pptx>
```

Fix all validation errors before proceeding to the next edit.

### Step 5: Repack

```bash
python ooxml/scripts/pack.py <dir> <output.pptx>
```

## Workflow 3: Create From Template

Use this when creating a presentation that follows an existing template design.

### Step 1: Analyze Template

```bash
python -m markitdown template.pptx > template-content.md
python scripts/thumbnail.py template.pptx
```

Read both outputs. Create a `template-inventory.md` documenting every slide with its index (0-based), layout type, and description.

### Step 2: Plan Outline

Choose appropriate template slides for your content. Match layout structure to actual content -- never use layouts with more placeholders than you have content. Save `outline.md` with a template mapping array.

### Step 3: Rearrange Slides

```bash
python scripts/rearrange.py template.pptx working.pptx 0,34,34,50,52
```

### Step 4: Extract Text Inventory

```bash
python scripts/inventory.py working.pptx text-inventory.json
```

Read `text-inventory.json` to understand all shapes, positions, and formatting.

### Step 5: Generate Replacement Text

Create `replacement-text.json` with new content for each shape. Rules:
- Shapes not listed are cleared automatically
- Include paragraph properties (bold, bullet, alignment, color)
- When `bullet: true`, do NOT include bullet symbols in text
- Use `"color": "FF0000"` (no `#` prefix) for colors

### Step 6: Apply Replacements

```bash
python scripts/replace.py working.pptx replacement-text.json output.pptx
```

## Reading and Analyzing Content

### Text Extraction

```bash
python -m markitdown path-to-file.pptx
```

### Typography and Color Extraction

When given an example design to emulate:
1. Unpack the file and read `ppt/theme/theme1.xml` for `<a:clrScheme>` and `<a:fontScheme>`
2. Examine `ppt/slides/slide1.xml` for actual font usage (`<a:rPr>`) and colors
3. Use grep to find color and font references across all XML files

## Creating Thumbnail Grids

```bash
python scripts/thumbnail.py presentation.pptx [output_prefix] [--cols N]
```

- Default: 5 columns, max 30 slides per grid
- Multiple grids auto-created for large decks
- Slides are zero-indexed

## Converting Slides to Images

```bash
soffice --headless --convert-to pdf presentation.pptx
pdftoppm -jpeg -r 150 presentation.pdf slide
```

## Dependencies

Required (should already be installed):
- **markitdown**: `pip install "markitdown[pptx]"` (text extraction)
- **pptxgenjs**: `npm install -g pptxgenjs` (presentation creation)
- **playwright**: `npm install -g playwright` (HTML rendering)
- **sharp**: `npm install -g sharp` (SVG/image rasterization)
- **react-icons**: `npm install -g react-icons react react-dom` (icons)
- **defusedxml**: `pip install defusedxml` (secure XML parsing)
- **LibreOffice**: `sudo apt-get install libreoffice` (PDF conversion)
- **Poppler**: `sudo apt-get install poppler-utils` (PDF to images)

## Code Style

When generating code for PPTX operations: write concise code, avoid verbose variable names and redundant operations, avoid unnecessary print statements.

## Output Checklist

When complete, verify:

- [ ] Presentation opens without errors in PowerPoint/LibreOffice
- [ ] All slides have correct content and formatting
- [ ] Visual thumbnail review shows no text cutoff or overlap
- [ ] OOXML validation passes (if editing XML directly)
- [ ] Color palette matches subject matter and branding
- [ ] Web-safe fonts used exclusively
- [ ] No placeholder or template text remains
