---
name: pptx-templates
context: fork
description: Browse and manage the PowerPoint template library
model: haiku
---

# /pptx-templates

List, inspect, and manage the extracted PowerPoint template library.

## Usage

```
/pptx-templates                    # List all templates
/pptx-templates info <slug>        # Show template details
/pptx-templates layouts <slug>     # List layouts for a template
/pptx-templates delete <slug>      # Remove a template
```

## Examples

```
/pptx-templates
/pptx-templates info baae-community-day-feb2026
/pptx-templates layouts baae-community-day-feb2026
/pptx-templates delete old-template
```

## Instructions

### List All Templates

Default when no argument provided. Read `.claude/templates/pptx/_catalogue.json` and display:

```
PPTX Template Library (<count> templates)
─────────────────────────────────────────

  <template name>
    Slug:     <slug>
    Source:   <filename>
    Layouts:  <count>
    Fonts:    <major> / <minor>
    Tags:     <tag1>, <tag2>
    Extracted: <date>

  <template name>
    ...
```

### Show Template Details

When `info <slug>` is provided:

1. Read `.claude/templates/pptx/<slug>/template.json`
2. Display full details including:
   - Slide dimensions
   - All theme colours with hex values
   - Font scheme
   - Number of layouts grouped by type (title, content, section, image, etc.)
   - Preview thumbnails if available

### List Layouts

When `layouts <slug>` is provided:

```bash
python3 .claude/scripts/pptx_create.py --list-layouts <slug>
```

Or read the template JSON directly and display:

```
Layouts for '<template name>' (<count>)
───────────────────────────────────────

  Category: Title Slides
    title-slide                    Title Slide                    3 placeholders
    title-slide-abba-confident-blue Title Slide (ABBA Confident)  3 placeholders

  Category: Section Dividers
    section-divider-dark-blue      Section Divider_Dark Blue      5 placeholders
    section-divider-corporate-blue Section Divider_Corporate Blue 5 placeholders

  Category: Content
    single-column-text             Single Column Text             3 placeholders
    two-column-text                Two Column Text                4 placeholders
    ...
```

### Delete Template

When `delete <slug>` is provided:

1. Confirm with user before deleting
2. Remove the directory `.claude/templates/pptx/<slug>/`
3. Update `_catalogue.json` to remove the entry
4. Report success

## Error Handling

| Error | Solution |
|-------|----------|
| No templates found | Run `/pptx-extract-template` first |
| Template slug not found | Check slug with `/pptx-templates` |
| Catalogue corrupted | Delete `_catalogue.json` and re-extract |

## Integration with Other Skills

- **`/pptx-extract-template`** — Add new templates to the library
- **`/pptx-create`** — Use templates to create presentations
