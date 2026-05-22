---
name: pdf-screenshot
description: Render PDF pages or cropped regions to PNG images for visual verification.
triggers:
  - screenshot pdf
  - snapshot pdf
  - render pdf page
  - show me the pdf
  - verify pdf element
  - calibrate pdf extraction
  - pdf visual check
  - screenshot page
  - capture pdf region
---

# PDF Screenshot

This skill renders pages or specific regions (bounding boxes) of a PDF into PNG images. It is designed for human-agent collaboration workflows where the agent needs to show the human what it has detected (e.g., tables, figures) for verification or calibration.

## Usage

### Full Page Screenshot

```bash
/pdf-screenshot /path/to/doc.pdf --page 5
```

Saves to `/tmp/pdf-screenshot/doc_page5.png` (or custom path).

### Cropped Region (Bounding Box)

```bash
/pdf-screenshot /path/to/doc.pdf --page 5 --bbox "72,200,540,400"
```

Saves to `/tmp/pdf-screenshot/doc_page5_crop.png`.
Bounding box format: `x0, y0, x1, y1`.
A default padding of 20px is added to the crop.

### Custom Output Path

```bash
/pdf-screenshot /path/to/doc.pdf --page 5 --out /tmp/my_screenshot.png
```

### Highlight Region

```bash
/pdf-screenshot doc.pdf --page 5 --highlight "72,200,540,400"
```

Draws a red rectangle around the specified region. Useful for visual verification without cropping.

### Batch Processing

```bash
# Specific pages
/pdf-screenshot doc.pdf --pages 1,3,5 --out ./screenshots/

# All pages
/pdf-screenshot doc.pdf --all --out ./screenshots/
```

If `--out` is a directory (ends in `/`), files are named automatically (e.g., `doc_page1.png`).

## Arguments

- `pdf_path`: Path to the input PDF file.
- `--page`: Single page number (0-indexed).
- `--pages`: Comma-separated list of page numbers (e.g. `1,3,5`).
- `--all`: Process all pages in the document.
- `--bbox`: Optional crop bounding box `x0,y0,x1,y1`.
- `--highlight`: Optional highlight bounding box `x0,y0,x1,y1` (red stroke).
- `--out`: Optional output path or directory.
- `--dpi`: Rendering DPI (default 150).

## Dependencies

- `pymupdf` (fitz)
