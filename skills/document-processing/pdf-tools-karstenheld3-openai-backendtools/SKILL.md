---
name: pdf-tools
description: Apply when converting, processing, or analyzing PDF files
---

# PDF Tools Guide

Rules and usage for PDF tools in `[WORKSPACE_FOLDER]/.tools/`.

## MUST-NOT-FORGET

- Check existing conversions before converting
- Default output: `.tools/_pdf_to_jpg_converted/[PDF_FILENAME]/`
- Use 150 DPI for screen, 300 DPI for OCR
- Two-pass downsizing: Ghostscript (images) then QPDF (structure)

## PDF to JPG Conversion

### Script: `DevSystemV2/skills/pdf-tools/convert-pdf-to-jpg.py`

Converts PDF pages to JPG images for vision analysis.

**Usage:**
```powershell
python DevSystemV2/skills/pdf-tools/convert-pdf-to-jpg.py <input.pdf> [--output <dir>] [--dpi <dpi>] [--pages <range>]
```

**Examples:**
```powershell
python DevSystemV2/skills/pdf-tools/convert-pdf-to-jpg.py invoice.pdf
python DevSystemV2/skills/pdf-tools/convert-pdf-to-jpg.py invoice.pdf --dpi 200 --pages 1-2
python DevSystemV2/skills/pdf-tools/convert-pdf-to-jpg.py invoice.pdf --pages 1
```

**Output Convention:**
- Default output: `.tools/_pdf_to_jpg_converted/[PDF_FILENAME]/`
- Each PDF gets its own subfolder named after the PDF file (without extension)
- Files named: `[PDF_FILENAME]_page001.jpg`, `[PDF_FILENAME]_page002.jpg`, etc.
- Check for existing subfolder to skip re-conversion

**Parameters:**
- `--output`: Output directory (default: `.tools/_pdf_to_jpg_converted/`)
- `--dpi`: Resolution (default: 150)
- `--pages`: Page range - "1", "1-3", or "all" (default: all)

## 7-Zip CLI Tools

Location: `.tools/7z/`

7-Zip is required to extract Ghostscript from its NSIS installer. The standalone `7za.exe` cannot extract NSIS archives.

### Extract archive
```powershell
& ".tools/7z/7z.exe" x -y -o"output_folder" "archive.zip"
```

### Extract NSIS installer (like Ghostscript)
```powershell
& ".tools/7z/7z.exe" x -y -o"output_folder" "installer.exe"
```

### List archive contents
```powershell
& ".tools/7z/7z.exe" l "archive.zip"
```

## Poppler CLI Tools

Location: `.tools/poppler/Library/bin/`

### pdftoppm - PDF to Image
```powershell
& ".tools/poppler/Library/bin/pdftoppm.exe" -jpeg -r 150 "input.pdf" "output_prefix"
```

### pdftotext - Extract Text
```powershell
& ".tools/poppler/Library/bin/pdftotext.exe" "input.pdf" "output.txt"
```

### pdfinfo - Get PDF Metadata
```powershell
& ".tools/poppler/Library/bin/pdfinfo.exe" "input.pdf"
```

### pdfseparate - Split PDF Pages
```powershell
& ".tools/poppler/Library/bin/pdfseparate.exe" "input.pdf" "output_%d.pdf"
```

### pdfunite - Merge PDFs
```powershell
& ".tools/poppler/Library/bin/pdfunite.exe" "page1.pdf" "page2.pdf" "merged.pdf"
```

## QPDF CLI Tools

Location: `.tools/qpdf/bin/`

### Merge PDFs
```powershell
& ".tools/qpdf/bin/qpdf.exe" --empty --pages file1.pdf file2.pdf -- merged.pdf
```

### Split PDF (extract pages)
```powershell
& ".tools/qpdf/bin/qpdf.exe" input.pdf --pages . 1-5 -- output.pdf
```

### Decrypt PDF
```powershell
& ".tools/qpdf/bin/qpdf.exe" --decrypt --password=secret encrypted.pdf decrypted.pdf
```

### Repair PDF
```powershell
& ".tools/qpdf/bin/qpdf.exe" --replace-input damaged.pdf
```

### Linearize (optimize for web)
```powershell
& ".tools/qpdf/bin/qpdf.exe" --linearize input.pdf output.pdf
```

## Smart PDF Compression Script

### Script: `DevSystemV2/skills/pdf-tools/compress-pdf.py`

Intelligent PDF compression that analyzes content and applies optimal strategy.

**Usage:**
```powershell
python DevSystemV2/skills/pdf-tools/compress-pdf.py <input.pdf> [--compression high|medium|low] [--output output.pdf]
```

**Examples:**
```powershell
python DevSystemV2/skills/pdf-tools/compress-pdf.py report.pdf
python DevSystemV2/skills/pdf-tools/compress-pdf.py report.pdf --compression high
python DevSystemV2/skills/pdf-tools/compress-pdf.py report.pdf --compression low --output archive.pdf
```

**Compression levels:**
- **high**: Target 50%+ reduction, aggressive (72 DPI)
- **medium**: Target 25%+ reduction, balanced (150 DPI)
- **low**: Target 10%+ reduction, preserve quality (300 DPI)

**Features:**
- Analyzes PDF structure (images, DPI, format, optimization status)
- Predicts compression potential before processing
- Escalates to more aggressive strategies if target not reached
- Reverts to previous result if aggressive approach shows insufficient improvement

**Output:** `.tools/_pdf_output/[PDF_FILENAME]_compressed.pdf`

## Simple PDF Downsizing Script

### Script: `DevSystemV2/skills/pdf-tools/downsize-pdf-images.py`

Direct Ghostscript wrapper for manual DPI control.

**Usage:**
```powershell
python DevSystemV2/skills/pdf-tools/downsize-pdf-images.py <input.pdf> [--output <dir>] [--dpi <dpi>] [--preset <preset>]
```

**Parameters:**
- `--output`: Output directory (default: `.tools/_pdf_output/`)
- `--dpi`: Resolution (default: 150)
- `--preset`: Quality preset - screen (72), ebook (150), printer (300), prepress (300)

**Output:** `.tools/_pdf_output/[PDF_FILENAME]_[DPI]dpi.pdf`

## Ghostscript CLI Tools

Location: `.tools/gs/bin/`

### Compress images (downsize PDF)
```powershell
& ".tools/gs/bin/gswin64c.exe" -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dDownsampleColorImages=true -dColorImageResolution=72 -dDownsampleGrayImages=true -dGrayImageResolution=72 -dDownsampleMonoImages=true -dMonoImageResolution=72 -dNOPAUSE -dQUIET -dBATCH -sOutputFile=output.pdf input.pdf
```

### Quality presets (`-dPDFSETTINGS`)
- `/screen` - 72 DPI, smallest file size
- `/ebook` - 150 DPI, medium quality
- `/printer` - 300 DPI, high quality
- `/prepress` - 300 DPI, color preserving

### Remove all images (text only)
```powershell
& ".tools/gs/bin/gswin64c.exe" -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dFILTERIMAGE=true -dNOPAUSE -dQUIET -dBATCH -sOutputFile=output.pdf input.pdf
```

## PDF Downsizing Workflow

Two-pass workflow for maximum compression:

### Pass 1: Ghostscript (image compression)
```powershell
& ".tools/gs/bin/gswin64c.exe" -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dDownsampleColorImages=true -dColorImageResolution=72 -dDownsampleGrayImages=true -dGrayImageResolution=72 -dNOPAUSE -dQUIET -dBATCH -sOutputFile=temp.pdf input.pdf
```

### Pass 2: QPDF (structure optimization)
```powershell
& ".tools/qpdf/bin/qpdf.exe" --linearize --object-streams=generate --stream-data=compress --compress-streams=y --optimize-images --flatten-annotations=screen temp.pdf output.pdf
Remove-Item temp.pdf
```

## PDF Analysis

Before optimizing, analyze the PDF to understand what's consuming space.

### Get PDF info
```powershell
& ".tools/poppler/Library/bin/pdfinfo.exe" "input.pdf"
```

### List all images with details
```powershell
& ".tools/poppler/Library/bin/pdfimages.exe" -list "input.pdf"
```

Shows: page, dimensions, color space, compression, DPI, size. Use to determine if images can be further compressed.

### Count images
```powershell
& ".tools/poppler/Library/bin/pdfimages.exe" -list "input.pdf" | Measure-Object
```

## Optimization Strategies (by effectiveness)

Tested on 6 real-world annual reports (50-100 MB each):

**High compression (>50% reduction):**
- JPEG2000 at 200 DPI: 77 MB → 4.5 MB (94% with screen, 86% with ebook)
- Mixed content, not optimized: 84 MB → 34 MB (59%)
- Mixed content: 49 MB → 21 MB (57%)

**Moderate compression (10-50%):**
- Already optimized PDF: 47 MB → 42 MB (10%)

**Low compression (<10%):**
- PDF with 10552 tiny images: 58 MB → 56 MB (4%) - many small UI elements
- Image-only PDF at 115 DPI: 101 MB → 97 MB (4% at 100 DPI, 77% at 72 DPI)

**Key factors affecting compression:**
- **Image format**: JPEG2000 (jpx) compresses dramatically when converted to JPEG
- **Image DPI**: High DPI (200+) benefits most from downsampling
- **Already optimized**: PDFs marked "Optimized: yes" compress less
- **Many small images**: Thousands of tiny icons/UI elements resist compression

### Strategy 1: Aggressive (best for large reductions)
```powershell
cmd /c "& '.tools/gs/bin/gswin64c.exe' -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dDetectDuplicateImages=true -dCompressFonts=true -dSubsetFonts=true -dConvertCMYKImagesToRGB=true -dColorImageDownsampleType=/Bicubic -dNOPAUSE -dBATCH -sOutputFile=output.pdf input.pdf"
```

### Strategy 2: Balanced (preserves more quality)
```powershell
cmd /c "& '.tools/gs/bin/gswin64c.exe' -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dDetectDuplicateImages=true -dCompressFonts=true -dSubsetFonts=true -dConvertCMYKImagesToRGB=true -dNOPAUSE -dBATCH -sOutputFile=output.pdf input.pdf"
```

### Strategy 3: Structure only (no quality loss)
```powershell
& ".tools/qpdf/bin/qpdf.exe" --linearize --object-streams=generate --compress-streams=y --recompress-flate input.pdf output.pdf
```

## Key Optimization Flags

- `-dDetectDuplicateImages=true` - Replace duplicate images with references
- `-dCompressFonts=true` - Compress font data
- `-dSubsetFonts=true` - Include only used glyphs
- `-dConvertCMYKImagesToRGB=true` - Convert CMYK to RGB (smaller)
- `-dColorImageDownsampleType=/Bicubic` - Better quality downsampling

## Best Practices

1. **Analyze first**: Use `pdfimages -list` to understand image content before optimizing
2. **Check existing conversions**: Before converting, check if subfolder exists in `_pdf_to_jpg_converted/`
3. **Use appropriate DPI**: 72 for web/archive, 150 for screen, 300 for print/OCR
4. **Convert specific pages**: Use `--pages` to avoid converting entire large PDFs
5. **Clean up**: Delete old conversions when no longer needed
6. **Two-pass for maximum compression**: Ghostscript (images) then QPDF (structure)

## Setup

For initial installation, see `SETUP.md` in this skill folder.

**Tool locations:**
- 7-Zip: `.tools/7z/`
- Poppler: `.tools/poppler/`
- QPDF: `.tools/qpdf/`
- Ghostscript: `.tools/gs/`
- Installers: `.tools/_installer/`
- JPG output: `.tools/_pdf_to_jpg_converted/`
- PDF output: `.tools/_pdf_output/`
