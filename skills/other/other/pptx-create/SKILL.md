---
name: pptx-create
context: fork
description: Create PowerPoint presentations from the template library
model: opus
---

# /pptx-create

Create a new PowerPoint presentation using a template from the extracted library. Populate slides from an outline, vault notes, or a JSON content specification.

## Usage

```
/pptx-create <title> [--template <slug>]
/pptx-create <title> --template <slug> --from <note-path>
/pptx-create --template <slug> --content <content.json>
```

## Examples

```
/pptx-create "Q1 Architecture Review" --template baae-community-day-feb2026
/pptx-create "Alpha Programme Update" --from "Projects/Project - Alpha.md"
/pptx-create --template baae-community-day-feb2026 --content slides.json
```

## Instructions

### Phase 1: Select Template

1. If `--template` provided, load that template
2. If not provided, list available templates and ask user to choose:

```bash
python3 .claude/scripts/pptx_create.py --list-templates
```

Use **AskUserQuestion** to select:

```
Question: "Which template should be used?"
Header: "Template"
Options:
  1. "<most recent template>" (Recommended)
  2. "<other template>"
  3. "List all layouts first"
```

### Phase 2: Define Content

Determine the content source based on user input:

**Option A: Interactive Outline**

If user provides just a title, help them build an outline interactively:

1. Ask for the presentation structure (sections/topics)
2. For each section, ask for key points
3. Map each section to an appropriate layout

**Option B: From Vault Note**

If `--from <note-path>` is provided:

1. Read the vault note
2. Extract headings, key points, and relationships
3. Map sections to slides automatically:
   - H1 → Title slide
   - H2 → Section headers
   - H3 + bullets → Content slides
   - Tables → Content slides with table data
   - Images → Image layout slides

**Option C: JSON Content Specification**

If `--content <file>` is provided, use the JSON directly. Format:

```json
{
  "title": "Presentation Title",
  "slides": [
    {
      "layout": "title-slide",
      "content": {
        "title": "Presentation Title",
        "subtitle": "Author — Date"
      }
    },
    {
      "layout": "section-divider-dark-blue",
      "content": {
        "title": "Section Name"
      }
    },
    {
      "layout": "single-column-text",
      "content": {
        "title": "Slide Title",
        "body": ["Bullet 1", "Bullet 2", "Bullet 3"]
      },
      "notes": "Speaker notes here"
    },
    {
      "layout": "two-column-text",
      "content": {
        "title": "Comparison",
        "left": ["Before item 1", "Before item 2"],
        "right": ["After item 1", "After item 2"]
      }
    },
    {
      "layout": "large-image-large-text",
      "content": {
        "title": "Architecture Diagram",
        "image": "Attachments/diagram.png",
        "body": "Key architecture overview"
      }
    }
  ]
}
```

### Phase 3: Layout Mapping

Show available layouts for the selected template:

```bash
python3 .claude/scripts/pptx_create.py --list-layouts <slug>
```

Map content to layouts using these guidelines:

| Content Type | Suggested Layouts |
|-------------|-------------------|
| Title/opening | `title-slide`, `title-slide-abba-confident-blue` |
| Section break | `section-divider-dark-blue`, `section-divider-corporate-blue` |
| Bullet points | `single-column-text`, `1-single-column-text` |
| Two columns | `two-column-text`, `5050-text-and-image` |
| Image + text | `large-image-large-text`, `wide-image-and-text` |
| Multiple images | `4x-images`, `6x-images`, `8x-images` |
| Chart/data | `1x-chart-white`, `5-two-content` |
| Thank you/close | `thank-you-image`, `1-thank-you-image` |
| Agenda | `8x-agenda` |

### Phase 4: Preview Plan

Before generating, show the plan:

```bash
python3 .claude/scripts/pptx_create.py --template <slug> --content <spec.json> --dry-run
```

Present as:

```
Planned Presentation: "Q1 Architecture Review"
Template: BAAE Community Day Feb2026

  1. [title-slide] Q1 2026 Architecture Review
  2. [section-divider-dark-blue] Programme Updates
  3. [single-column-text] Alpha Status
  4. [two-column-text] Before / After
  5. [large-image-large-text] Architecture Diagram
  6. [thank-you-image] Thank You

Proceed with generation?
```

### Phase 5: Generate PPTX

Write the content specification to a temporary JSON file, then run:

```bash
python3 .claude/scripts/pptx_create.py --template <slug> --content /tmp/claude/slides.json --output "Attachments/<title>.pptx"
```

### Phase 6: Create Vault Note (Optional)

Ask if the user wants a Concept note linking to the presentation:

```markdown
---
type: Concept
title: <Presentation Title>
created: YYYY-MM-DD
modified: YYYY-MM-DD
tags:
  - presentation
  - slides
sourceType: PPTX
template: <template-slug>
slides: <count>
---

# <Presentation Title>

**Template:** <template name>
**Created:** YYYY-MM-DD
**Slides:** <count>

**File:** [[<filename>.pptx]]

## Slide Outline

1. **<slide title>** — <layout name>
2. **<slide title>** — <layout name>
...

## Related

- [[<linked project/meeting if applicable>]]
```

### Phase 7: Report

```
Presentation created successfully!

  Title:     <title>
  Template:  <template name>
  Slides:    <count>
  Output:    Attachments/<filename>.pptx

Link in vault: [[<filename>.pptx]]

Next steps:
  - Open in PowerPoint to review and refine
  - Add to meeting note: [[Concept - <title>]]
```

## Content Key Reference

| Key | Placeholder Target | Value Type |
|-----|-------------------|------------|
| `title` | Title placeholder (idx 0/1) | String |
| `subtitle` | Subtitle placeholder (idx 1/4) | String |
| `body` | First body placeholder | String or list of bullets |
| `left` | First body (two-column) | String or list |
| `right` | Second body (two-column) | String or list |
| `image` | First picture placeholder | File path |
| `image_1`, `image_2`... | Nth picture placeholder | File path |
| `notes` | Speaker notes | String |

## Error Handling

| Error | Solution |
|-------|----------|
| Template not found | Run `/pptx-templates` to see available templates |
| Layout not found | Check layout slugs with `--list-layouts` |
| Image not found | Verify path relative to vault root |
| Output path issue | Check Attachments/ directory exists |

## Integration with Other Skills

- **`/pptx-extract-template`** — Extract templates from existing presentations
- **`/pptx-templates`** — Browse the template library
- **`/architecture-report`** — Generate architecture reports as presentations
- **`/project-report`** — Create project status presentations

## Dependencies

- `python-pptx` — PPTX creation
- Template must be extracted first with `/pptx-extract-template`
