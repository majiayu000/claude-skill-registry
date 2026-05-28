---
name: file-converter
description: Convert & transform files - images (resize, format, HEIC), markdown (PDF/HTML), data (CSV/JSON/YAML/TOML/XML), SVG, base64, text encoding. Cross-platform, single & batch mode. This skill should be used when converting file formats, resizing images, generating PDFs from markdown, or transforming data between formats.
author: George Khananaev
---

# File Converter

Convert files between formats w/ single & batch support. All scripts use consistent CLI patterns.

## When to Use

- Convert images between PNG, JPG, WEBP, BMP, TIFF, GIF, ICO, AVIF, HEIC/HEIF
- Resize/crop images w/ fit modes (contain, cover, fill, inside, outside)
- Convert markdown -> PDF or HTML w/ themes
- Convert HTML -> markdown (w/ tag stripping control)
- Transform CSV <-> JSON <-> YAML <-> TOML <-> XML
- SVG <-> raster conversion (PNG, JPG, WEBP, BMP, TIFF)
- Base64 encode/decode files (w/ data URI support, stdin)
- Fix text encoding issues (detect, convert w/ error handling strategies)

## Quick Routing

| Task | Script | Deps |
|------|--------|------|
| Image convert/resize | `convert_image.py` | Pillow, pillow-heif (opt) |
| Markdown -> HTML | `md_to_html.py` | markdown, pygments |
| Markdown -> PDF | `md_to_pdf.py` | markdown + weasyprint\|pdfkit |
| HTML -> Markdown | `html_to_md.py` | markdownify, bs4 |
| CSV/JSON/YAML/TOML/XML | `csv_json_yaml.py` | pyyaml, tomli-w, xmltodict, dicttoxml (per format) |
| SVG convert | `svg_convert.py` | cairosvg, Pillow |
| Base64 encode/decode | `base64_codec.py` | (none) |
| Text encoding | `text_encoding.py` | chardet (opt) |
| Cross-platform utils | `platform_utils.py` | (none) - shared by pdf/svg scripts |

## Install Deps

```bash
# All deps (recommended)
pip install Pillow markdown pygments weasyprint markdownify beautifulsoup4 cairosvg pyyaml chardet tomli-w xmltodict dicttoxml

# Optional
pip install pillow-heif                    # HEIC/HEIF support

# Minimal (per task)
pip install Pillow                          # Images only
pip install markdown pygments               # MD -> HTML only
pip install markdown weasyprint             # MD -> PDF only (macOS: brew install pango)
pip install markdownify beautifulsoup4      # HTML -> MD only
pip install pyyaml                          # YAML support
pip install tomli-w                         # TOML write (read: Python 3.11+ built-in)
pip install xmltodict dicttoxml             # XML support
pip install cairosvg                        # SVG -> raster (macOS: brew install cairo)
pip install chardet                         # Encoding detection
```

## CLI Patterns

All scripts share consistent arg patterns:

```bash
# Single file
python3 scripts/<script>.py input.ext output.ext

# Batch (directory or glob)
python3 scripts/<script>.py *.ext --output-dir ./out
python3 scripts/<script>.py ./dir/ --output-dir ./out --format ext
```

## 1. Image Convert & Resize

```bash
# Format conversion
python3 scripts/convert_image.py photo.png photo.webp
python3 scripts/convert_image.py photo.jpg photo.avif --quality 80

# Resize
python3 scripts/convert_image.py photo.jpg thumb.jpg --width 300
python3 scripts/convert_image.py photo.png banner.png --width 1200 --height 400 --fit cover

# Batch convert directory
python3 scripts/convert_image.py ./photos/ --output-dir ./webp --format webp --width 1200 --quality 85
python3 scripts/convert_image.py *.png --output-dir ./thumbs --format jpg --width 300 --height 300 --fit cover
```

**Fit modes:**

| Mode | Behavior |
|------|----------|
| contain | Fit inside bounds, preserve ratio (def) |
| cover | Fill bounds, crop overflow |
| fill | Stretch to exact dimensions |
| inside | Like contain, but only shrink (never enlarge) |
| outside | Like cover, but never crop |

**Supported:** PNG, JPG, WEBP, BMP, TIFF, GIF, ICO, AVIF, HEIC/HEIF (w/ pillow-heif)

Auto-fixes EXIF orientation. Guards against decompression bombs (300M pixel limit).

## 2. Markdown -> HTML

```bash
# Single file
python3 scripts/md_to_html.py README.md readme.html
python3 scripts/md_to_html.py doc.md doc.html --theme dark

# Batch
python3 scripts/md_to_html.py ./docs/ --output-dir ./site --theme github
```

**Themes:** github (def), dark, minimal, print

Features: fenced code blocks, syntax highlighting, tables, TOC w/ permalinks, responsive CSS.

## 3. Markdown -> PDF

```bash
# Single file
python3 scripts/md_to_pdf.py report.md report.pdf
python3 scripts/md_to_pdf.py spec.md spec.pdf --theme report

# Batch
python3 scripts/md_to_pdf.py ./docs/ --output-dir ./pdfs --theme report
```

**Themes:** default, report (formal w/ serif), minimal

**PDF engines:** weasyprint (preferred, no external deps on macOS) or pdfkit (requires wkhtmltopdf). Script auto-detects available engine.

## 4. HTML -> Markdown

```bash
# Single file
python3 scripts/html_to_md.py page.html page.md

# Strip unwanted tags (default: script, style, noscript)
python3 scripts/html_to_md.py page.html page.md --strip script style nav footer

# Keep all HTML tags (no stripping)
python3 scripts/html_to_md.py page.html page.md --keep-all

# Batch
python3 scripts/html_to_md.py ./site/ --output-dir ./docs
```

## 5. Data Formats (CSV/JSON/YAML/TOML/XML)

```bash
# Any direction
python3 scripts/csv_json_yaml.py data.csv data.json
python3 scripts/csv_json_yaml.py data.json data.yaml
python3 scripts/csv_json_yaml.py config.yaml config.json
python3 scripts/csv_json_yaml.py config.toml config.json
python3 scripts/csv_json_yaml.py data.json data.xml

# Batch
python3 scripts/csv_json_yaml.py *.csv --output-dir ./json --format json
```

**Supported:** CSV, JSON, YAML (.yaml/.yml), TOML (.toml), XML (.xml). All directions supported where deps are installed.

## 6. SVG Conversion

```bash
# SVG -> raster
python3 scripts/svg_convert.py icon.svg icon.png --width 512
python3 scripts/svg_convert.py logo.svg logo.jpg --width 1024 --quality 90

# Raster -> SVG (embedded image wrapper)
python3 scripts/svg_convert.py photo.png photo.svg

# Batch
python3 scripts/svg_convert.py *.svg --output-dir ./png --format png --width 256
```

## 7. Base64 Encode/Decode

```bash
# Encode to stdout
python3 scripts/base64_codec.py encode image.png

# Encode to data URI (for HTML/CSS embedding)
python3 scripts/base64_codec.py encode image.png --data-uri

# Encode to file
python3 scripts/base64_codec.py encode image.png -o image.b64

# Decode
python3 scripts/base64_codec.py decode image.b64 -o image.png

# Batch
python3 scripts/base64_codec.py encode *.png --output-dir ./b64
```

## 8. Text Encoding

```bash
# Detect encoding
python3 scripts/text_encoding.py detect file.txt
python3 scripts/text_encoding.py detect *.txt

# Convert encoding (single mode requires -o to prevent accidental overwrite)
python3 scripts/text_encoding.py convert file.txt --to utf-8 -o output.txt
python3 scripts/text_encoding.py convert file.txt --from latin-1 --to utf-8 -o output.txt

# Handle unmappable characters
python3 scripts/text_encoding.py convert file.txt --to ascii --errors replace -o clean.txt
python3 scripts/text_encoding.py convert file.txt --to ascii --errors ignore -o clean.txt

# Batch convert to UTF-8
python3 scripts/text_encoding.py convert *.txt --to utf-8 --output-dir ./utf8
```

**Error modes:** strict (default, fail on unmappable), replace (use ? placeholder), ignore (skip unmappable chars).

## Common Workflows

### Web optimization pipeline

```bash
# Convert photos to WEBP, resize for web, generate thumbnails
python3 scripts/convert_image.py ./photos/ --output-dir ./web --format webp --width 1200 --quality 80
python3 scripts/convert_image.py ./photos/ --output-dir ./thumbs --format webp --width 300 --height 300 --fit cover --quality 75
```

### Documentation pipeline

```bash
# Generate HTML site from markdown docs
python3 scripts/md_to_html.py ./docs/ --output-dir ./site --theme github

# Generate PDF reports
python3 scripts/md_to_pdf.py ./docs/ --output-dir ./pdfs --theme report
```

### Data migration pipeline

```bash
# CSV -> JSON for API import
python3 scripts/csv_json_yaml.py ./exports/ --output-dir ./json --format json

# JSON config -> YAML
python3 scripts/csv_json_yaml.py config.json config.yaml
```

### Icon generation pipeline

```bash
# SVG -> multiple PNG sizes for app icons
for size in 16 32 64 128 256 512; do
  python3 scripts/svg_convert.py icon.svg "icon-${size}.png" --width $size
done
```

## Error Handling

All scripts:
- Print errors per-file in batch mode, continue w/ remaining files
- Exit 1 on fatal errors (missing deps, no input)
- Print size before/after for each conversion
- Create output directories automatically
- Handle KeyboardInterrupt gracefully (exit 130)

## Cross-Platform Support

Scripts work on macOS, Linux, and Windows. Native library paths (cairo, pango, gobject) are auto-configured via `platform_utils.py`:
- **macOS:** `/opt/homebrew/lib`, `/usr/local/lib`
- **Linux:** `/usr/local/lib`, `/usr/lib/x86_64-linux-gnu`
- **Windows:** GTK runtime, MSYS2, Conda paths + `os.add_dll_directory()`

## Stdin Support

`md_to_html.py` and `base64_codec.py` accept `-` for stdin input:

```bash
cat README.md | python3 scripts/md_to_html.py - output.html
cat file.bin | python3 scripts/base64_codec.py encode - -o file.b64
```

## Integration

**Pairs with:** `token-optimizer` (compress markdown before PDF), `code-quality` (validate scripts)
