---
context: fork
---

# /pdf-to-page

Convert PDF documents into Page notes with extracted images saved as PNG files in +Attachments/.

**Updated**: 2026-01-08 - Now uses docling for faster, more accurate PDF processing with native table recognition and reading order detection. User can choose between Sonnet (concise) or Opus (comprehensive) analysis.

## Usage

```
/pdf-to-page <pdf-path>
/pdf-to-page +Attachments/architecture-spec.pdf
/pdf-to-page +Attachments/meeting-presentation.pdf --title "Custom Title"
```

## Instructions

This skill uses **docling** for PDF structure extraction + **1 agent** for visual analysis and YourOrg entity extraction.

### Phase 1: PDF Loading & Validation

1. Verify the PDF file exists at the specified path
2. Check file extension is `.pdf`
3. Note any custom title provided by user (otherwise derive from filename)
4. Prepare output directory: `+Attachments/` for PNG files

### Phase 1.5: Analysis Depth Selection

**Use AskUserQuestion** to ask the user which analysis depth they prefer:

```
Question: "What level of analysis do you want for this PDF?"
Header: "Analysis"
Options:
  1. "Sonnet - Concise" (Recommended)
     Description: "Faster processing, concise overview. Best for straightforward documents."
  2. "Opus - Comprehensive"
     Description: "Deeper analysis with detailed YourOrg context. Best for complex technical documents."
```

**When to recommend each**:
- **Sonnet**: Default choice. Fast, cost-effective, good for most documents
- **Opus**: Use for complex technical documents, architecture specs, or when comprehensive YourOrg entity extraction is critical

Store the selection for use in Phase 3.

### Phase 2: Docling Processing (Fast & Accurate)

Use docling to extract PDF structure with native table recognition and reading order detection:

```python
from docling.document_converter import DocumentConverter
import json

# Initialize converter
converter = DocumentConverter()

# Process PDF
result = converter.convert(pdf_path)

# Extract structured outputs
markdown_content = result.document.export_to_markdown()
doc_dict = result.document.export_to_dict()
json_data = json.dumps(doc_dict, indent=2)

# Get statistics
page_count = len(result.document.pages)
table_count = len(result.document.tables) if hasattr(result.document, 'tables') else 0
image_count = len(result.document.images) if hasattr(result.document, 'images') else 0
```

**What docling provides**:
- ✅ Native table structure recognition (much better than text extraction)
- ✅ Reading order detection (handles multi-column layouts)
- ✅ Code and formula identification
- ✅ Image position markers (`<!-- image -->` in markdown)
- ✅ Heading hierarchy preservation
- ✅ Bullet/numbered list structure
- ✅ Apple Silicon acceleration (MLX on M-series Macs)

**Processing time**: ~0.85 seconds per page (with MLX acceleration)

**Save docling outputs** (for debugging/verification):
```python
# Save to temp directory for verification
output_dir = Path(pdf_path).parent / "docling_output"
output_dir.mkdir(exist_ok=True)

md_file = output_dir / f"{Path(pdf_path).stem}_docling.md"
json_file = output_dir / f"{Path(pdf_path).stem}_docling.json"

with open(md_file, 'w', encoding='utf-8') as f:
    f.write(markdown_content)

with open(json_file, 'w', encoding='utf-8') as f:
    f.write(json_data)
```

### Phase 3: Visual Analysis & YourOrg Entity Extraction

Launch **one agent** using the model selected in Phase 1.5:

- **If Sonnet selected**: Use `model="sonnet"` - faster, concise analysis
- **If Opus selected**: Use `model="opus"` - comprehensive, detailed analysis

**Agent: Visual Analysis & YourOrg Entity Extraction** (Sonnet or Opus based on selection)
```
Task: Analyze PDF visually and extract organization-specific entities

1. VISUAL ANALYSIS:
   - Read the PDF file (Claude can view PDFs visually)
   - Identify all diagrams, charts, graphs, and images on each page
   - Create descriptive names for each image based on content
   - Note which images should be extracted as PNGs
   - Assess image types (architecture diagrams, flowcharts, screenshots, photos, logos)
   - Count pages with significant visual content

2. YourOrg ENTITY EXTRACTION:
   - Identify YourOrg projects mentioned (MyDataIntegration, ModernizationProject, NewProductLine, MaintenanceSystem, etc.)
   - Find YourOrg people and roles (architects, PMs, stakeholders)
   - Identify YourOrg systems and technologies (SAP, AWS, MROPlatform, etc.)
   - Extract YourOrg organizations (VendorA, SAP, VendorB, VendorC, etc.)
   - Find dates, deadlines, milestones
   - Identify action items, decisions, recommendations

3. CONTENT CLASSIFICATION:
   - Determine document type (spec, presentation, report, guide, training, compliance)
   - Identify key topics and themes
   - Note any sections that need special formatting
   - Assess document purpose and audience

Return:
- Image inventory with page numbers, descriptions, and suggested filenames
- YourOrg entity list (projects, people, systems, organizations)
- Document classification and topics
- Action items and key dates
```

**Why only 1 agent now?**
- Docling already extracted the text structure (Phase 2)
- Only need visual understanding and YourOrg domain knowledge
- 67% reduction in API costs (3 agents → 1 agent)
- Faster processing time

**Model selection impact**:
- **Sonnet**: ~10 seconds agent time, cost-effective, good quality
- **Opus**: ~30-60 seconds agent time, higher cost, comprehensive analysis with richer YourOrg context

### Phase 4: Image Extraction

For each image identified by the agent:

1. **Extract visuals from PDF**:
   ```bash
   # Use pdfimages (from poppler-utils) to extract embedded images
   pdfimages -png <pdf-file> <output-prefix>

   # OR use pdftoppm for full-page diagrams
   pdftoppm -png -r 150 -f <page-num> -l <page-num> <pdf-file> <output-prefix>
   ```

2. **Save as PNG files** in `+Attachments/`:
   - Naming convention: `{pdf-basename} - Page {N} - {description}.png`
   - Example: `MROPlatform Architecture - Page 3 - System Diagram.png`
   - Use descriptive names from Sonnet agent's visual analysis

3. **Track all created files** for linking in the final Page note

### Phase 5: Create Page Note

Generate filename from title:
- Pattern: `Page - {title}.md`
- If no custom title: derive from PDF filename (remove extension, clean up)

Create the Page note with this structure:

```markdown
---
type: Page
title: {title}
created: {YYYY-MM-DD}
modified: {YYYY-MM-DD}
tags: [pdf-import, {auto-generated tags from agent classification}]
source: "{PDF filename}"
sourceType: PDF
processedWith: docling
---

# {title}

> **Source**: [[{PDF filename}]]
> **Imported**: {YYYY-MM-DD}
> **Pages**: {page count from docling}
> **Tables**: {table count from docling}
> **Processed with**: [docling](https://github.com/docling-project/docling) + Claude {Sonnet|Opus}

## Overview

{2-3 paragraph summary from agent's classification}

## Document Information

| Property | Value |
|----------|-------|
| **Document Type** | {type from agent classification} |
| **Source File** | `{PDF filename}` |
| **Pages** | {count from docling} |
| **Tables Detected** | {table count from docling} |
| **Images Detected** | {image count from docling} |
| **Processing Time** | {docling processing time} seconds |
| **Creation Date** | {if found in PDF metadata} |
| **Author** | {if found in PDF metadata} |

## Content

{Use docling's markdown output directly - already has proper structure}

{The markdown_content from docling includes:}
- Heading hierarchy (##, ###)
- Bullet and numbered lists
- Paragraphs with preserved reading order
- Image markers (<!-- image -->) at correct positions
- Tables (if detected)
- Code blocks and formulas (if detected)

{Replace <!-- image --> markers with actual embedded images if available}

## Diagrams & Visual Content

{For each extracted PNG from Phase 4:}

### {Image description from agent} (Page {N})

![[{image filename}.png]]

{Brief description from agent's visual analysis}

---

## Tables

{If docling detected tables, they're already in the markdown content above}
{If tables are in images, note from agent's visual analysis}

## Key Information

### Projects Referenced

{List from agent's YourOrg entity extraction with [[Project]] links}

### People Mentioned

{List from agent's YourOrg entity extraction with [[Person]] links}

### Systems & Technologies

{List from agent's YourOrg entity extraction}

### Organizations Referenced

{List from agent's YourOrg entity extraction with [[Organisation]] links}

### Dates & Deadlines

| Date | Context |
|------|---------|
{Dates from agent's analysis}

## Action Items

{Action items from agent's analysis}

- [ ] {item 1}
- [ ] {item 2}

## Related

- {Auto-link to related Project, Meeting, or other notes from agent's entity extraction}
- [[{PDF filename}|Original PDF]]

## Processing Notes

**Extraction Method**: Docling v2.66.0 with MLX acceleration
**Processing Time**: {docling time} seconds
**Visual Analysis**: Claude {Sonnet|Opus} agent
**Analysis Depth**: {Concise|Comprehensive}
**Quality**: {any notes from agent about extraction quality}

{Any extraction notes, quality issues, or recommendations from agent}
```

### Phase 6: Summary Report

After creation, provide user with:

```markdown
## PDF Import Complete

**Created**: `Page - {title}.md`

**Processing Statistics**:
- Processing time: {docling time}s (docling) + {agent time}s (visual analysis) = {total}s
- Pages processed: {count}
- Tables detected: {count}
- Images detected: {count}

**Extracted Images**: {count} PNG files
- `{image1.png}` - {description}
- `{image2.png}` - {description}
- ...

**YourOrg Entities Identified**:
- Projects: {count} ({list})
- People: {count} ({list})
- Systems: {count} ({list})
- Organizations: {count} ({list})

**Content Classification**:
- Document type: {type}
- Key topics: {topics}
- Action items: {count}

**Suggested Actions**:
1. Review extracted content for accuracy
2. Verify YourOrg entity links are correct
3. Add additional tags if needed: {suggestions}
4. Create tasks from action items: {task suggestions}
5. Link to related projects: {suggestions}
```

### Phase 7: Optional Cleanup

Ask user if they want to:
1. Move the original PDF to `+Attachments/` if not already there
2. Delete docling debug output directory (keep or remove)
3. Add additional tags based on content
4. Create tasks from any action items found
5. Create links to related existing notes

## Technical Notes

### Docling Installation

**Required**:
```bash
pip install docling
```

**Size**: ~250 MB installed (includes models)
**Platform**: macOS (arm64), Linux (x86_64, arm64), Windows
**License**: MIT

### Image Extraction Tools

**pdfimages** (from poppler-utils): Best for extracting embedded images
```bash
brew install poppler  # Install if not available
pdfimages -png input.pdf output-prefix
```

**pdftoppm**: Convert PDF pages to images if diagrams span full pages
```bash
pdftoppm -png -r 150 -f 3 -l 3 input.pdf output-prefix  # Page 3 only
```

**Fallback**: If extraction fails, use Sonnet agent's visual descriptions

### Image Quality

- Save PNGs at 150-300 DPI for good quality
- Compress images if very large (>5MB)
- Prefer vector diagrams when possible

### Error Handling

**Password-Protected PDFs**:
```python
# Docling doesn't handle password-protected PDFs
# Prompt user to unlock PDF first or use:
# qpdf --decrypt --password=<pwd> input.pdf output.pdf
```

**Scanned PDFs** (image-based):
```python
# Docling handles OCR automatically with ocrmac (on macOS)
# Uses Vision framework for high-quality text extraction
# For better results, can use VLM pipeline:
# converter = DocumentConverter(
#     format_options={"pdf_options": {"use_vlm": True}}
# )
```

**Very Large PDFs** (>100 pages):
- Process in chunks if needed
- Show progress to user
- Consider processing only specific page ranges

**Extraction Failures**:
- If docling fails, fall back to old 3-agent workflow
- Create Page note with manual instructions
- Log error for debugging

### Performance Benchmarks

Based on MROPlatform System Architecture & Roadmap (29 pages):

| Metric | Value |
|--------|-------|
| **Processing time** | 24.6 seconds |
| **Throughput** | 0.85 seconds/page |
| **First run** | 41.1 seconds (includes model loading) |
| **Subsequent runs** | 24.6 seconds (models cached) |
| **Acceleration** | MPS (Metal Performance Shaders on Apple Silicon) |

**Comparison with old workflow**:
- Old: 30-60 seconds (3 Sonnet agents)
- New with Sonnet: ~35 seconds total (24.6s docling + ~10s agent)
- New with Opus: ~55-85 seconds total (24.6s docling + ~30-60s agent)
- API cost: 67% reduction with Sonnet (1 agent vs 3 agents)
- API cost: Higher with Opus, but more comprehensive analysis

## Example Workflow

```
User: /pdf-to-page +Attachments/MROPlatform-Architecture-Overview.pdf