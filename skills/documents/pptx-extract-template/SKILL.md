---
name: pptx-extract-template
context: fork
description: Extract reusable templates from PowerPoint presentations into the template library
model: opus
---

# /pptx-extract-template

Extract the design system (slide masters, layouts, colour themes, font themes, placeholder configurations) from a PowerPoint presentation and save it as a reusable template.

## Usage

```
/pptx-extract-template <path-to-pptx>
/pptx-extract-template <path-to-pptx> --name "Template Name"
/pptx-extract-template <path-to-pptx> --previews
```

## Examples

```
/pptx-extract-template ~/Downloads/BAAE Community Day Feb2026.pptx
/pptx-extract-template Attachments/SAP Architecture.pptx --name "SAP Branded" --previews
/pptx-extract-template quarterly-review.pptx --name "BA Quarterly Review"
```

## Instructions

### Phase 1: Locate the PowerPoint File

1. Parse the argument for a file path
2. If partial or just a filename, search in this order:
   - `~/Downloads/`
   - Vault `Attachments/` folder
   - Current directory
3. Verify the file exists and has a `.pptx` extension
4. If not found, ask user for the correct path

### Phase 2: Dry-Run Analysis

Run the extraction script in dry-run mode to show what will be extracted:

```bash
python3 .claude/scripts/pptx_extract_template.py "<pptx-path>" --dry-run --verbose
```

Review the output and present a summary to the user:
- Number of slide masters and layouts
- Theme colours and fonts
- Notable layout names

### Phase 3: Confirm Name and Tags

Use **AskUserQuestion** to confirm:

```
Question: "What should this template be called?"
Header: "Template"
Options:
  1. "<inferred name from filename>" (Recommended)
  2. "Custom name"
```

Then ask for tags:

```
Question: "Which tags apply to this template?"
Header: "Tags"
Options:
  1. "ba, corporate" (Recommended for BA presentations)
  2. "ba, engineering"
  3. "ba, community-day"
  4. "Custom tags"
multiSelect: true
```

### Phase 4: Extract and Save

Run the full extraction:

```bash
python3 .claude/scripts/pptx_extract_template.py "<pptx-path>" --name "<name>" --tags <tag1> <tag2>
```

Add `--previews` if the user requested layout preview thumbnails (requires LibreOffice).

### Phase 5: Verify

After extraction, verify the output:

1. Check `.claude/templates/pptx/<slug>/template.json` exists and is valid JSON
2. Check `_catalogue.json` has been updated
3. Confirm the source PPTX was copied

### Phase 6: Report

```
Template extracted successfully!

  Name:     <name>
  Slug:     <slug>
  Layouts:  <count> unique layouts
  Theme:    <colour scheme name> (<major font> / <minor font>)
  Saved to: .claude/templates/pptx/<slug>/

Use this template with:
  /pptx-create "Title" --template <slug>

View all templates with:
  /pptx-templates
```

## What Gets Extracted

| Element | Description | Stored As |
|---------|-------------|-----------|
| Slide Masters | Base design with backgrounds, logos | `template.json` |
| Slide Layouts | Named layouts with placeholder positions | `layouts/*.json` |
| Colour Theme | Brand colours (dk1, lt1, accent1-6, etc.) | `theme/colours.json` |
| Font Theme | Heading and body font families | `theme/fonts.json` |
| Placeholders | Type, position, size, default formatting per layout | `layouts/*.json` |
| Source PPTX | Original file for use as creation template | `source.pptx` |

## Error Handling

| Error | Solution |
|-------|----------|
| File not found | Ask user for correct path |
| Not a PPTX file | Inform user, suggest conversion |
| python-pptx import error | `pip3 install python-pptx` |
| Corrupted PPTX | Suggest opening in PowerPoint first |
| Permission denied | Check file permissions |

## Template Storage

Templates are stored in `.claude/templates/pptx/`:

```
.claude/templates/pptx/
├── _catalogue.json           # Master index
├── <template-slug>/
│   ├── template.json         # Full metadata
│   ├── source.pptx           # Original PPTX (used for creation)
│   ├── layouts/              # Per-layout JSON files
│   │   ├── title-slide.json
│   │   ├── section-header.json
│   │   └── ...
│   ├── theme/
│   │   ├── colours.json
│   │   └── fonts.json
│   └── previews/             # Optional layout thumbnails
│       └── *.png
```

## Integration with Other Skills

- **`/pptx-create`** — Use extracted templates to create new presentations
- **`/pptx-templates`** — Browse and manage the template library
- **`/pptx-to-page`** — Extract content (not design) from presentations

## Dependencies

- `python-pptx` — PPTX parsing and introspection
- `lxml` — Theme XML extraction
- LibreOffice (optional) — Layout preview generation
