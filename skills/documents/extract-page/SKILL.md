---
name: extract-page
description: Extract a single page from a PDF as a PNG image for quick preview.
argument-hint: <file.pdf> <page-number>
allowed-tools: Bash, Read
---

# Extract PDF Page Tool

Use `tools/extract_page.py` to extract a single page from a PDF as a PNG image.

## Usage

**Basic usage:**
```bash
python tools/extract_page.py $ARGUMENTS[0] $ARGUMENTS[1]
```

**With custom output path:**
```bash
python tools/extract_page.py <file>.pdf <page> -o output.png
```

## Examples

```bash
# Extract page 5 from build/lecture.pdf
python tools/extract_page.py build/lecture.pdf 5

# Output will be: build/lecture.page5.png
```

## Notes

- Page numbers are 1-indexed
- Default output: `<file>.page<N>.png`
- Uses pdftoppm (poppler), sips (macOS), or ImageMagick convert
