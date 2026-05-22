---
name: pptx
description: "Presentation creation, editing, and analysis. When Claude needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes, or any other presentation tasks"
---

# PPTX Presentation Skill

## Core Capabilities

**Reading & Analysis**: Extract presentation text via markdown conversion or access raw XML for detailed content like speaker notes, comments, and design elements.

**Creating Presentations**: Two approaches:
- Building from scratch using HTML-to-PowerPoint conversion
- Using existing templates by duplicating, reordering, and replacing content

**Editing Existing Files**: Modify by unpacking OOXML structure, editing XML, validating, and repacking.

## Key Workflows

### Text Extraction
```bash
pandoc presentation.pptx -o output.md
```

### Creating from HTML
1. Design slides in HTML with proper dimensions
2. Convert to PowerPoint format
3. Apply design principles and color palettes

### Template-Based Development
1. Analyze existing template inventory
2. Duplicate and rearrange slides
3. Replace content while preserving formatting

### Editing Existing Files
1. Unpack: `python unpack.py presentation.pptx output_dir/`
2. Edit XML files in `ppt/slides/`
3. Validate: `python validate.py output_dir/`
4. Pack: `python pack.py output_dir/ new_presentation.pptx`

## Color Palettes

Example palettes available:
- Classic Blue
- Teal & Coral
- Bold Red
- Modern Minimalist
- Earth Tones
- And 13 more...

## Technical Tools

- `unpack.py` - Decompress PPTX
- `validate.py` - Check XML validity
- `pack.py` - Recompress to PPTX
- `thumbnail.py` - Generate visual grids
- `rearrange.py` - Slide ordering
- `inventory.py` - Text extraction
- `replace.py` - Content updates
