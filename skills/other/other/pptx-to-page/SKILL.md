---
context: fork
---

# Skill: PowerPoint to Page

Convert PowerPoint presentations to Obsidian Page notes with text extraction, tables, and images.

## When to Use

This skill should be invoked when the user:
- Asks to "convert a PowerPoint to a page note"
- Mentions "/pptx-to-page" explicitly
- Wants to import a presentation into the vault
- Needs to extract slides as images for viewing in Obsidian
- Has a .pptx or .ppt file to process

## Parameters

- **PPTX Path**: Path to the PowerPoint file (can be in Downloads, vault, or anywhere)
- **Page Title** (optional): Custom title for the Page note (defaults to presentation filename)
- **Mode** (optional): `quick` (default) or `visual`
  - `quick`: Fast docling extraction with text, tables, embedded images
  - `visual`: Full slide rendering as PNG images (requires LibreOffice)

## Process

### Step 1: Locate the PowerPoint File

If the user provides a partial path or just a filename:
1. Check `~/Downloads/` first
2. Check vault `+Attachments/` folder
3. Ask user for full path if not found

### Step 2: Choose Processing Mode

Ask the user (or infer from context):

**Quick Mode** (default - recommended for most uses):
- Uses docling for fast text/table extraction
- Uses python-pptx for speaker notes and embedded images
- Processing time: ~1 second for 50 slides
- Best for: searchable content, meeting notes, documentation

**Visual Mode** (when visual fidelity needed):
- Uses LibreOffice to render full slide images
- Processing time: 1-2 minutes for 50 slides
- Best for: design reviews, exact visual reference

### Step 3: Quick Mode Processing (Docling)

```python
from pathlib import Path
from docling.document_converter import DocumentConverter
from pptx import Presentation
import os

def process_pptx_quick(pptx_path, output_dir, title):
    """Quick mode: docling + python-pptx extraction"""

    # 1. Docling for text and tables
    converter = DocumentConverter()
    result = converter.convert(pptx_path)
    doc = result.document

    markdown_content = doc.export_to_markdown()
    tables_count = len(doc.tables) if hasattr(doc, 'tables') else 0
    pictures_count = len(doc.pictures) if hasattr(doc, 'pictures') else 0

    # 2. python-pptx for speaker notes and embedded images
    prs = Presentation(pptx_path)
    speaker_notes = []
    embedded_images = []

    for slide_num, slide in enumerate(prs.slides, 1):
        # Extract speaker notes
        if slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame.text.strip()
            if notes:
                speaker_notes.append((slide_num, notes))

        # Extract embedded images
        for shape in slide.shapes:
            if hasattr(shape, "image"):
                img = shape.image
                img_filename = f"{title} - Slide {slide_num:02d} - Image {len(embedded_images)+1}.{img.ext}"
                img_path = output_dir / img_filename
                with open(img_path, "wb") as f:
                    f.write(img.blob)
                embedded_images.append((slide_num, img_filename))

    return {
        'markdown': markdown_content,
        'tables_count': tables_count,
        'pictures_count': pictures_count,
        'speaker_notes': speaker_notes,
        'embedded_images': embedded_images,
        'slide_count': len(prs.slides)
    }
```

### Step 4: Visual Mode Processing (LibreOffice)

Only use if visual mode requested. Check dependencies first:

```bash
# Check for LibreOffice (for PPTX to PDF conversion)
which soffice || brew install --cask libreoffice

# Check for poppler (for PDF to image conversion)
which pdftoppm || brew install poppler

# Check for Python libraries
python3 -c "import pdf2image" 2>&1 || pip3 install pdf2image
```

Then convert PPTX → PDF → PNG images at 200 DPI.

### Step 5: Create Page Note

**Quick Mode Output Format:**

```markdown
---
type: Page
title: <Presentation Title>
created: YYYY-MM-DD
modified: YYYY-MM-DD
tags:
  - presentation
  - slides
  - pdf-import
sourceType: PPTX
processedWith: docling
slides: <count>
tables: <count>
---

# <Presentation Title>

> Extracted from `<original-filename.pptx>` using docling

**Slides**: <count> | **Tables**: <count> | **Images**: <count>

---

## Content

<docling markdown output - includes headings, text, tables>

---

## Speaker Notes

### Slide 3
<notes content>

### Slide 7
<notes content>

---

## Embedded Images

### Slide 1
![[<title> - Slide 01 - Image 1.png]]

### Slide 4
![[<title> - Slide 04 - Image 1.jpg]]
![[<title> - Slide 04 - Image 2.png]]

---

## Related

- [[<linked meeting note if applicable>]]
```

**Visual Mode Output Format:**

```markdown
---
type: Page
title: <Presentation Title>
created: YYYY-MM-DD
modified: YYYY-MM-DD
tags:
  - presentation
  - slides
sourceType: PPTX
processedWith: libreoffice
slides: <count>
---

# <Presentation Title>

Source: `<original-pptx-filename>`

Total Slides: <count>

---

## Slide 1

![[<title> - Slide 01.png]]

---

## Slide 2

![[<title> - Slide 02.png]]

---

...
```

### Step 6: Link to Context (if applicable)

Ask the user if they want to link this page to:
- A specific meeting note (most common for presentations)
- A project note
- An ADR (if it's architecture-related)

Suggest adding it to the meeting note's "Slides" section.

## Mode Selection Guide

| Use Case | Recommended Mode |
|----------|-----------------|
| Meeting notes reference | Quick |
| Technical documentation | Quick |
| Searchable archive | Quick |
| Design review | Visual |
| Exact visual reference needed | Visual |
| Large presentations (50+ slides) | Quick |
| Offline/slow machine | Quick |

## Success Message

**Quick Mode:**
```
✅ Page note created: `Page - <title>.md`
📊 Slides processed: <count>
📋 Tables extracted: <count>
🖼️ Embedded images saved: <count> to +Attachments/
💬 Speaker notes captured: <count> slides
⚡ Processing time: <X.XX> seconds
🔗 Link in meeting notes with: `[[Page - <title>]]`
```

**Visual Mode:**
```
✅ Page note created: `Page - <title>.md`
📊 Total slides rendered: <count>
🖼️ Slide images saved to: +Attachments/
⏱️ Processing time: <X> minutes
🔗 Link in meeting notes with: `[[Page - <title>]]`
```

## Error Handling

Common errors and solutions:

1. **PPTX not found**: Ask user for correct path
2. **Docling import error**: `pip3 install docling`
3. **python-pptx import error**: `pip3 install python-pptx`
4. **LibreOffice missing** (visual mode): `brew install --cask libreoffice`
5. **poppler missing** (visual mode): `brew install poppler`
6. **Corrupted PPTX**: Inform user, suggest opening in PowerPoint first
7. **Password-protected**: Cannot process, ask user to remove password

## Performance Comparison

| Presentation Size | Quick Mode | Visual Mode |
|------------------|------------|-------------|
| 10 slides | ~0.2 sec | ~20 sec |
| 25 slides | ~0.4 sec | ~50 sec |
| 50 slides | ~0.8 sec | ~2 min |
| 100 slides | ~1.5 sec | ~4 min |

## Examples

### Example 1: Quick Mode (Default)
```
User: /pptx-to-page ~/Downloads/Project_Update.pptx
```

### Example 2: Visual Mode
```
User: /pptx-to-page SAP_Architecture.pptx visual
```

### Example 3: With Meeting Link
```
User: Convert the Datasphere presentation and add it to today's meeting note
```

### Example 4: With Custom Title
```
User: Convert SAP_BTP_2026.pptx to a page called "Cloud Platform Architecture 2026"
```

## Integration with Other Skills

This skill works well with:
- `/meeting` - Add presentation to meeting notes
- `/project-status` - Include project presentations
- `/adr` - Attach architecture diagrams from slides
- `/weekly-summary` - Reference key slides in summaries

## Dependencies

**Quick Mode (minimal)**:
- `docling` - Text and table extraction
- `python-pptx` - Speaker notes and embedded images

**Visual Mode (additional)**:
- LibreOffice - PPTX to PDF conversion
- poppler (pdftoppm) - PDF to PNG conversion
- `pdf2image` - Python wrapper for poppler

## Notes

- Quick mode is **~100x faster** than visual mode
- Quick mode extracts actual text (searchable, copyable)
- Visual mode preserves exact slide appearance
- Always copy the original PPTX to `+Attachments/` for reference
- Speaker notes are only available via python-pptx (both modes can include them)
- Consider using quick mode first, then visual mode for specific slides if needed
