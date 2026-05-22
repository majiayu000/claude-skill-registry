---
name: obsidian-pdf-export
description: Export Obsidian notes to professional PDFs with configurable dimensions, clickable internal links, auto-generated TOC, and PDF bookmarks. Supports single note and batch export modes. Has device presets for Supernote Nomad, reMarkable, and Kindle. Use when user wants to create PDFs from their notes for sharing, printing, e-readers, or archival.
allowed-tools: Bash,Read,Write
---

# Obsidian PDF Export

Export Obsidian markdown notes to professionally formatted PDFs using Docker-based Pandoc/LaTeX.

## When to Use This Skill

Activate when the user:

- Wants to "export notes to PDF" or "generate PDF from notes"
- Asks to "create a PDF" from their Obsidian vault
- Needs to export a folder of notes as a combined document
- Wants printable versions of their notes with working navigation
- Requests specific PDF dimensions (A4, Letter, custom sizes)

## Features

- **Single & Batch Export**: Export one note or combine multiple notes into a single PDF
- **Clickable Internal Links**: `[[wikilinks]]` become clickable anchors within the PDF
- **Auto-Generated TOC**: Table of contents at the beginning based on headings
- **PDF Bookmarks**: Sidebar navigation in PDF readers
- **Configurable Dimensions**: A4, Letter, Legal, or custom width x height
- **Growth Stage Badges**: Preserves seedling/sapling/evergreen indicators

## Prerequisites

### Docker (Required)

The skill uses a Docker container with Pandoc and LaTeX. Build the image first:

```bash
cd /home/tolga/src/tolgaio/neo/skills/obsidian-pdf-export/docker
docker build -t obsidian-pdf-export .
```

### Python Dependencies

For running preprocessing outside Docker:

```bash
pip install PyYAML
```

## Usage

### Single Note Export

```bash
# Basic export (A4, default margins)
bash scripts/export.sh /path/to/note.md

# With output path
bash scripts/export.sh /path/to/note.md output.pdf

# Custom page size and margins
bash scripts/export.sh --page-size letter --margin 1.5in note.md

# Without table of contents
bash scripts/export.sh --no-toc note.md
```

### Batch Export

```bash
# Export all notes in a folder
bash scripts/export.sh --batch "1_Projects/myproject/*.md" project-docs.pdf

# With custom ordering (file lists note paths)
bash scripts/export.sh --batch --order order.txt "*.md" combined.pdf
```

## CLI Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--preset` | nomad, remarkable, kindle, a4, letter | (none) | Device preset (sets page-size & margin) |
| `--page-size` | a4, letter, legal, WxH | a4 | Page dimensions |
| `--margin` | CSS units (1in, 2cm) | 1in | Page margins |
| `--top-margin` | CSS units | (same as margin) | Top margin override |
| `--bottom-margin` | CSS units | (same as margin) | Bottom margin override |
| `--toc-depth` | 1-6 | 3 | Heading levels in TOC |
| `--no-toc` | flag | (toc enabled) | Disable table of contents |
| `--batch` | flag | false | Combine multiple notes |
| `--order` | file path | (none) | Custom note ordering for batch |
| `--title` | text | from frontmatter | Override PDF title |
| `--vault` | path | $BRAIN_HOME | Path to Obsidian vault |

## Device Presets

| Preset | Device | Page Size | Margin |
|--------|--------|-----------|--------|
| `nomad` | Supernote Nomad (1404x1872 @ 300 PPI) | 4.7" x 6.2" | 0.3in |
| `remarkable` | reMarkable 2 (1404x1872 @ 226 PPI) | 6.2" x 8.3" | 0.4in |
| `kindle` | Kindle Paperwhite | 3.5" x 5.5" | 0.2in |
| `a4` | Standard A4 paper | A4 | 1in |
| `letter` | US Letter paper | Letter | 1in |

## How It Works

### Processing Pipeline

```
┌─────────────────┐    ┌────────────────────┐    ┌──────────────────┐
│  Input Notes    │ -> │  Preprocess        │ -> │  Docker/Pandoc   │
│  (markdown)     │    │  (resolve links)   │    │  (LaTeX → PDF)   │
└─────────────────┘    └────────────────────┘    └──────────────────┘
```

### Wikilink Conversion

| Input | Single Mode | Batch Mode |
|-------|-------------|------------|
| `[[note]]` | "note" (text) | `[note](#note)` (clickable) |
| `[[note\|Display]]` | "Display" | `[Display](#note)` |
| `[[note#heading]]` | "note" | `[note](#note-heading)` |
| `[text](https://...)` | preserved | preserved |
| `![[image.png]]` | `![](image.png)` | `![](image.png)` |

In batch mode, wikilinks to notes included in the export become clickable anchors that jump to that section. Links to notes NOT in the export become plain text.

### TOC and Bookmarks

- **Table of Contents**: Auto-generated from H1-H3 headings (configurable with `--toc-depth`)
- **PDF Bookmarks**: Sidebar navigation automatically created from headings
- **Page Numbers**: Added to footer

## File Structure

```
obsidian-pdf-export/
├── SKILL.md                    # This file
├── scripts/
│   ├── preprocess.py           # Wikilink resolution
│   ├── merge_notes.py          # Batch: combine notes
│   └── export.sh               # Main orchestration
├── docker/
│   ├── Dockerfile              # pandoc/latex image
│   └── templates/
│       └── obsidian.latex      # PDF styling
└── references/
    └── page-sizes.md           # Dimension reference
```

## Examples

### Example 1: Export a Project README

```bash
# User: "Export my homelab project notes to PDF"
bash scripts/export.sh 1_Projects/Homelab/README.md ~/Desktop/homelab-docs.pdf
```

### Example 2: Create a Book from Multiple Notes

```bash
# User: "Combine all my psychology notes into one PDF"
bash scripts/export.sh --batch --page-size 6x9 --title "Psychology Notes" \
    "3_Resources/Psychology/*.md" psychology-collection.pdf
```

### Example 3: Letter-Size with Wide Margins

```bash
# User: "Export for US Letter paper with room for annotations"
bash scripts/export.sh --page-size letter --margin 1.5in note.md
```

### Example 4: Export for Supernote Nomad

```bash
# User: "Create a PDF for my Nomad" or "Export notes for nomad"
bash scripts/export.sh --batch --preset nomad --title "My Notes" \
    "1_Projects/MyProject/*.md" notes-for-nomad.pdf
```

### Example 5: Export for reMarkable

```bash
# User: "Export for reMarkable tablet"
bash scripts/export.sh --preset remarkable note.md
```

## Troubleshooting

### Docker Image Not Found

Build the image first:
```bash
cd /home/tolga/src/tolgaio/neo/skills/obsidian-pdf-export/docker
docker build -t obsidian-pdf-export .
```

### Broken Internal Links

Links to notes not in the vault appear in the `broken_links` output. In single mode, all wikilinks become plain text. In batch mode, only links to included notes become clickable.

### Images Not Appearing

Ensure images are in the vault and use standard paths. The script copies images to a temp directory for Docker access.

### LaTeX Errors

Usually caused by special characters. The preprocessor escapes most, but unusual Unicode may cause issues. Check the console output for specific errors.

## Technical Details

### Docker Image

Based on `pandoc/latex:3.1` with:
- XeLaTeX PDF engine (Unicode support)
- Python 3 + PyYAML
- LaTeX packages: bookmark, hyperref, geometry, fancyhdr, tocloft

### LaTeX Template

Custom template (`docker/templates/obsidian.latex`) provides:
- Obsidian-inspired purple link colors
- Clean heading hierarchy
- Automatic PDF bookmarks
- Configurable geometry

## Resources

- `scripts/preprocess.py` - Wikilink parsing and anchor generation
- `scripts/merge_notes.py` - Batch note merging with page breaks
- `scripts/export.sh` - Main CLI orchestration
- `references/page-sizes.md` - Standard page dimension reference
