---
name: md2pdf
description: "Convert Markdown files to beautifully styled PDFs with full Chinese font support. Use when: (1) Converting .md files to PDF format, (2) Creating printable documents from Markdown, (3) Generating book chapters or story PDFs, (4) Needing PDF output with custom styling (colors, fonts, backgrounds), (5) Working with Chinese text that needs proper rendering in PDF."
---

# Markdown to PDF Converter

Convert Markdown to PDF with Chinese font support and customizable styling.

## Quick Start

The script uses uv inline metadata - no manual dependency installation needed:

```bash
# Basic conversion (uv auto-installs dependencies)
uv run scripts/md2pdf.py input.md output.pdf

# With custom CSS
uv run scripts/md2pdf.py input.md output.pdf --style assets/vintage-paper.css

# With custom title
uv run scripts/md2pdf.py input.md output.pdf --title "Chapter Title"

# Or make executable and run directly
chmod +x scripts/md2pdf.py
./scripts/md2pdf.py input.md output.pdf
```

> **Note**: On macOS, the script automatically configures Homebrew library paths.

## Available Styles

Two pre-built styles in `assets/`:

| Style | File | Description |
|-------|------|-------------|
| Vintage Paper | `vintage-paper.css` | Warm cream background, brown text, serif fonts. Ideal for stories and literature. |
| Modern Clean | `modern-clean.css` | White background, dark text, sans-serif fonts. Ideal for technical documents. |

## Default Style Features

The built-in default style (vintage paper) includes:
- **Background**: Warm cream (#FAF6F0)
- **Text color**: Dark brown (#4A3728)
- **Heading color**: Darker brown (#3D2B1F)
- **Font**: Chinese serif (Noto Serif SC, Songti SC)
- **Line height**: 1.8
- **Paragraph indent**: 2em (Chinese style)
- **Page footer**: Page numbers

## Customization

To customize styling, copy an existing CSS file and modify:

```css
@page {
    size: A4;                        /* Paper size */
    margin: 2.5cm 2cm;               /* Page margins */
    background-color: #FAF6F0;       /* Page background */
}

body {
    font-family: "Noto Serif SC", serif;  /* Font stack */
    font-size: 12pt;                      /* Base font size */
    line-height: 1.8;                     /* Line spacing */
    color: #4A3728;                       /* Text color */
}
```

### Chinese Font Priority

The converter uses this font fallback chain:
1. Noto Serif SC (Google Noto fonts)
2. Source Han Serif SC (Adobe fonts)
3. Songti SC (macOS)
4. STSong (macOS)
5. SimSun (Windows)

Ensure at least one of these fonts is installed on the system.

## Script API

```python
from md2pdf import convert_md_to_pdf

convert_md_to_pdf(
    input_path="chapter.md",
    output_path="chapter.pdf",
    custom_css="assets/vintage-paper.css",  # Optional
    title="Chapter 1"                        # Optional
)
```

## Troubleshooting

### WeasyPrint system dependencies
```bash
# macOS (library path is auto-configured by script)
brew install pango

# Ubuntu/Debian
sudo apt install libpango-1.0-0 libpangocairo-1.0-0
```

### Missing Chinese fonts
```bash
# macOS
brew install font-noto-serif-cjk-sc

# Ubuntu/Debian
sudo apt install fonts-noto-cjk
```
