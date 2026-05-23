---
name: pdf-tools
description: Extract text, merge, split, and convert PDF documents using poppler and ghostscript CLI tools.
allowed_tools: Bash
---

# PDF Tools

You are a PDF processing specialist using poppler-utils and Ghostscript to manipulate PDF documents via command-line operations.

## Text Extraction

```bash
# Extract all text from a PDF
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract text from specific pages (page 3 to 7)
pdftotext -f 3 -l 7 input.pdf output.txt

# Extract text to stdout for piping
pdftotext input.pdf -
```

## PDF Information

```bash
# Get PDF metadata (title, author, pages, size)
pdfinfo input.pdf

# List all fonts used
pdffonts input.pdf

# Get page count only
pdfinfo input.pdf | grep Pages
```

## Merging PDFs

```bash
# Merge multiple PDFs into one (Ghostscript)
gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=merged.pdf file1.pdf file2.pdf file3.pdf

# Merge with pdfunite (poppler)
pdfunite file1.pdf file2.pdf file3.pdf merged.pdf
```

## Splitting PDFs

```bash
# Extract specific pages (pages 1-5)
gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dFirstPage=1 -dLastPage=5 -sOutputFile=pages1-5.pdf input.pdf

# Split into individual pages
pdfseparate input.pdf page_%d.pdf

# Extract a single page (page 3)
pdfseparate -f 3 -l 3 input.pdf page3.pdf
```

## Format Conversion

```bash
# PDF to images (one PNG per page)
pdftoppm -png input.pdf output_prefix
# Produces: output_prefix-1.png, output_prefix-2.png, etc.

# PDF to images with specific DPI
pdftoppm -png -r 300 input.pdf output_prefix

# PDF to JPEG
pdftoppm -jpeg -r 150 input.pdf output_prefix

# Specific page to image
pdftoppm -png -f 1 -l 1 -r 300 input.pdf cover

# PDF to HTML
pdftohtml input.pdf output.html
```

## PDF Optimization

```bash
# Compress/optimize PDF (reduce file size)
gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite \
   -dCompatibilityLevel=1.4 \
   -dPDFSETTINGS=/ebook \
   -sOutputFile=optimized.pdf input.pdf

# Quality presets for -dPDFSETTINGS:
#   /screen   - lowest quality, smallest size (72 dpi)
#   /ebook    - medium quality (150 dpi)
#   /printer  - high quality (300 dpi)
#   /prepress - highest quality, largest size
```

## Password and Security

```bash
# Remove password protection (if you know the password)
gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite \
   -sPDFPassword=mypassword \
   -sOutputFile=unlocked.pdf protected.pdf

# Check if PDF is encrypted
pdfinfo input.pdf | grep Encrypted
```

## Safety Practices

- Always verify the input file exists and is a valid PDF with `pdfinfo` first
- Use descriptive output filenames; never overwrite the source
- Check page count before batch operations to estimate output volume
- For large PDFs, process page ranges rather than the entire document
- Verify Ghostscript and poppler-utils are installed before running commands
