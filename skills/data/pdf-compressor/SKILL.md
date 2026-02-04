---
name: pdf-compressor
description: Compress large PDF files by resizing pages and optimizing images. Use when PDF file size is too large for sharing, uploading, or when Gemini generates oversized slides. Reduces file size by up to 98% while maintaining acceptable quality.
---

# PDF Compressor

Compress PDF files by converting pages to optimized images and rebuilding the PDF.

## Workflow

1. Convert PDF pages to images at specified DPI
2. Resize images to target width (maintaining aspect ratio)
3. Compress as JPEG with quality setting
4. Rebuild PDF from compressed images

## Usage

```bash
python scripts/compress.py "{pdf_path}" --width {width} --quality {quality} --output "{output_path}"
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| pdf_path | Yes | - | Path to PDF file to compress |
| --width | No | 1920 | Page width in pixels |
| --quality | No | 85 | JPEG quality (1-100) |
| --dpi | No | 150 | DPI for PDF to image conversion |
| --output, -o | No | auto | Output path (default: {filename}_compressed.pdf) |

## Quality Presets

| Use Case | Width | Quality | Expected Reduction |
|----------|-------|---------|-------------------|
| Web/Email | 1280 | 75 | ~95% |
| Standard | 1920 | 85 | ~90% |
| High Quality | 2560 | 90 | ~80% |
| Print | 3840 | 95 | ~60% |

## Examples

```bash
# Basic compression (default settings)
python scripts/compress.py "large_presentation.pdf"

# Web-optimized (smaller file)
python scripts/compress.py "slides.pdf" --width 1280 --quality 75

# High quality for presentations
python scripts/compress.py "report.pdf" --width 2560 --quality 90

# Custom output path
python scripts/compress.py "document.pdf" -o "document_small.pdf"
```

## Requirements

- Python packages: pdf2image, Pillow, img2pdf
- System: poppler (for pdf2image)
  - macOS: `brew install poppler`
  - Ubuntu: `apt-get install poppler-utils`

## Notes

- Original PDF is not modified
- Text becomes rasterized (not searchable)
- Best for image-heavy presentations and slides
- For text-heavy documents, consider Ghostscript instead
