---
name: pandoc
description: Universal document converter for transforming Markdown to PDF, DOCX, HTML, LaTeX, and 40+ other formats. Covers templates, filters, citations with BibTeX/CSL, and batch conversion automation scripts.
version: 1.0.0
category: documentation
type: skill
capabilities:
  - Markdown to PDF conversion
  - Markdown to DOCX (Word) conversion
  - Markdown to HTML conversion
  - Markdown to LaTeX conversion
  - Custom LaTeX templates
  - Custom DOCX reference documents
  - Lua filters for content transformation
  - Citation processing with BibTeX/CSL
  - Batch conversion scripts
  - Cross-reference support
  - Table of contents generation
  - Syntax highlighting
tools:
  - pandoc
  - pandoc-crossref
  - pandoc-citeproc
  - latexmk
  - xelatex
  - wkhtmltopdf
tags:
  - documentation
  - conversion
  - pdf
  - docx
  - latex
  - markdown
  - citations
  - templates
platforms:
  - linux
  - macos
  - windows
related_skills:
  - mkdocs
  - sphinx
  - marp
  - latex
---

# Pandoc Universal Document Converter Skill

Convert documents between 40+ formats with Pandoc. This skill covers Markdown to PDF/DOCX/HTML conversions, custom templates, citation management, and batch processing automation.

## When to Use This Skill

### USE When

- Converting Markdown to PDF with professional formatting
- Creating Word documents from Markdown sources
- Need reproducible document builds from plain text
- Managing academic papers with citations (BibTeX/CSL)
- Batch converting multiple documents
- Need custom templates for consistent branding
- Converting between multiple documentation formats
- Creating LaTeX documents from Markdown
- Need cross-references (figures, tables, equations)
- Building automated document pipelines

### DON'T USE When

- Building documentation websites (use MkDocs or Sphinx)
- Need interactive documentation (use web frameworks)
- Require real-time collaborative editing (use Google Docs)
- Building slide presentations (use Marp)
- Need WYSIWYG editing (use Word directly)
- Converting complex nested HTML (may lose formatting)

## Prerequisites

### Installation

```bash
# macOS (Homebrew)
brew install pandoc
brew install pandoc-crossref  # For cross-references
brew install basictex         # Minimal LaTeX for PDF
# Or full LaTeX: brew install --cask mactex

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install pandoc pandoc-citeproc
sudo apt-get install texlive-xetex texlive-fonts-recommended
sudo apt-get install texlive-latex-extra  # For additional packages

# Fedora/RHEL
sudo dnf install pandoc pandoc-citeproc
sudo dnf install texlive-xetex texlive-collection-fontsrecommended

# Windows (Chocolatey)
choco install pandoc
choco install miktex  # LaTeX distribution

# Windows (Scoop)
scoop install pandoc
scoop install latex

# Verify installation
pandoc --version
```

### System Requirements

- Pandoc 2.19 or higher (3.x recommended)
- LaTeX distribution (for PDF output)
- Python 3.8+ (for pandoc-filters)

## Core Capabilities

### 1. Basic Format Conversion

```bash
# Markdown to PDF
pandoc document.md -o document.pdf

# Markdown to DOCX
pandoc document.md -o document.docx

# Markdown to HTML
pandoc document.md -o document.html --standalone

# Markdown to LaTeX
pandoc document.md -o document.tex

# HTML to Markdown
pandoc page.html -o page.md

# DOCX to Markdown
pandoc document.docx -o document.md

# Multiple input files
pandoc chapter1.md chapter2.md chapter3.md -o book.pdf

# Specify input format explicitly
pandoc -f markdown -t pdf document.md -o document.pdf
```

### 2. PDF Generation with Options

```bash
# Basic PDF with table of contents
pandoc document.md -o document.pdf --toc

# PDF with XeLaTeX engine (better font support)
pandoc document.md -o document.pdf \
    --pdf-engine=xelatex \
    --toc \
    --toc-depth=3

# PDF with custom margins
pandoc document.md -o document.pdf \
    --pdf-engine=xelatex \
    -V geometry:margin=1in

# PDF with custom fonts
pandoc document.md -o document.pdf \
    --pdf-engine=xelatex \
    -V mainfont="Georgia" \
    -V sansfont="Helvetica" \
    -V monofont="Menlo"

# PDF with paper size and font size
pandoc document.md -o document.pdf \
    --pdf-engine=xelatex \
    -V papersize=a4 \
    -V fontsize=11pt

# PDF with numbered sections
pandoc document.md -o document.pdf \
    --number-sections \
    --toc

# PDF with syntax highlighting style
pandoc document.md -o document.pdf \
    --highlight-style=tango

# List available highlighting styles
pandoc --list-highlight-styles
```

### 3. Word Document (DOCX) Generation

```bash
# Basic DOCX
pandoc document.md -o document.docx

# DOCX with table of contents
pandoc document.md -o document.docx --toc

# DOCX with reference document (template)
pandoc document.md -o document.docx \
    --reference-doc=template.docx

# DOCX with syntax highlighting
pandoc document.md -o document.docx \
    --highlight-style=kate

# Creating a reference document template
pandoc --print-default-data-file reference.docx > template.docx
# Edit template.docx in Word to customize styles
```

### 4. HTML Generation

```bash
# Standalone HTML (includes head, body)
pandoc document.md -o document.html --standalone

# HTML with custom CSS
pandoc document.md -o document.html \
    --standalone \
    --css=styles.css

# HTML with embedded CSS
pandoc document.md -o document.html \
    --standalone \
    --css=styles.css \
    --embed-resources \
    --self-contained

# HTML with syntax highlighting
pandoc document.md -o document.html \
    --standalone \
    --highlight-style=pygments

# HTML with table of contents
pandoc document.md -o document.html \
    --standalone \
    --toc \
    --toc-depth=2

# HTML with math rendering (MathJax)
pandoc document.md -o document.html \
    --standalone \
    --mathjax

# HTML5 output
pandoc document.md -o document.html \
    --standalone \
    -t html5
```

### 5. Custom LaTeX Templates

```latex
%% template.tex - Custom Pandoc LaTeX template
\documentclass[$if(fontsize)$$fontsize$,$endif$$if(papersize)$$papersize$paper,$endif$]{article}

%% Packages
\usepackage{geometry}
\geometry{margin=1in}
\usepackage{fontspec}
\usepackage{hyperref}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{listings}

%% Fonts
$if(mainfont)$
\setmainfont{$mainfont$}
$endif$
$if(sansfont)$
\setsansfont{$sansfont$}
$endif$
$if(monofont)$
\setmonofont{$monofont$}
$endif$

%% Colors
\definecolor{linkcolor}{RGB}{0, 102, 204}
\definecolor{codebackground}{RGB}{248, 248, 248}

%% Hyperlinks
\hypersetup{
    colorlinks=true,
    linkcolor=linkcolor,
    urlcolor=linkcolor,
    pdfauthor={$author$},
    pdftitle={$title$}
}

%% Headers and footers
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{$title$}
\fancyhead[R]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}

%% Code blocks
\lstset{
    backgroundcolor=\color{codebackground},
    basicstyle=\ttfamily\small,
    breaklines=true,
    frame=single,
    numbers=left,
    numberstyle=\tiny\color{gray}
}

%% Section formatting
\titleformat{\section}
    {\Large\bfseries\color{linkcolor}}
    {\thesection}{1em}{}
\titleformat{\subsection}
    {\large\bfseries}
    {\thesubsection}{1em}{}

%% Title
$if(title)$
\title{$title$}
$endif$
$if(author)$
\author{$author$}
$endif$
$if(date)$
\date{$date$}
$endif$

\begin{document}

$if(title)$
\maketitle
$endif$

$if(abstract)$
\begin{abstract}
$abstract$
\end{abstract}
$endif$

$if(toc)$
\tableofcontents
\newpage
$endif$

$body$

\end{document}
```

```bash
# Use custom template
pandoc document.md -o document.pdf \
    --template=template.tex \
    --pdf-engine=xelatex \
    -V title="My Document" \
    -V author="Your Name" \
    -V date="2026-01-17" \
    --toc
```

### 6. YAML Metadata in Documents

```markdown
---
title: "Technical Report"
author:
  - name: "John Smith"
    affiliation: "University of Example"
    email: "john@example.edu"
  - name: "Jane Doe"
    affiliation: "Tech Corp"
date: "January 17, 2026"
abstract: |
  This document demonstrates advanced Pandoc features
  including custom metadata, citations, and formatting.
keywords:
  - documentation
  - pandoc
  - markdown
lang: en-US
toc: true
toc-depth: 3
numbersections: true
geometry: margin=1in
fontsize: 11pt
mainfont: "Georgia"
monofont: "Fira Code"
linkcolor: blue
bibliography: references.bib
csl: ieee.csl
---

# Introduction

Your document content starts here...
```

### 7. Citations and Bibliography

```bibtex
%% references.bib
@article{smith2024,
    author = {Smith, John and Doe, Jane},
    title = {Advanced Documentation Techniques},
    journal = {Journal of Technical Writing},
    year = {2024},
    volume = {15},
    number = {3},
    pages = {42--58},
    doi = {10.1234/jtw.2024.001}
}

@book{johnson2023,
    author = {Johnson, Robert},
    title = {The Complete Guide to Markdown},
    publisher = {Tech Press},
    year = {2023},
    address = {New York},
    isbn = {978-0-123456-78-9}
}

@inproceedings{williams2025,
    author = {Williams, Sarah},
    title = {Document Automation Best Practices},
    booktitle = {Proceedings of DocCon 2025},
    year = {2025},
    pages = {100--115},
    organization = {Documentation Society}
}

@online{pandocmanual,
    author = {{Pandoc Contributors}},
    title = {Pandoc User's Guide},
    year = {2024},
    url = {https://pandoc.org/MANUAL.html},
    urldate = {2024-01-15}
}
```

```markdown
<!-- document.md with citations -->
---
title: "Research Paper"
bibliography: references.bib
csl: apa.csl
---

# Literature Review

According to @smith2024, documentation is essential for
project success. This aligns with earlier findings
[@johnson2023; @williams2025].

The standard approach uses markdown formatting
[see @pandocmanual, chapter 3].

Multiple citations can be grouped together
[@smith2024; @johnson2023, pp. 15-20].

# References

::: {#refs}
:::
```

```bash
# Generate PDF with citations
pandoc document.md -o document.pdf \
    --citeproc \
    --bibliography=references.bib \
    --csl=apa.csl \
    --pdf-engine=xelatex

# Download CSL styles
# https://github.com/citation-style-language/styles
curl -O https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl
curl -O https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl
curl -O https://raw.githubusercontent.com/citation-style-language/styles/master/chicago-author-date.csl
```

### 8. Cross-References with pandoc-crossref

```bash
# Install pandoc-crossref
# macOS
brew install pandoc-crossref

# Or download from releases
# https://github.com/lierdakil/pandoc-crossref/releases
```

```markdown
<!-- document.md with cross-references -->
---
title: "Document with Cross-References"
---

# Introduction

See @fig:architecture for the system overview.
The data flow is described in @sec:dataflow.
Results are shown in @tbl:results.
The equation @eq:formula describes the relationship.

# System Architecture {#sec:architecture}

![System Architecture Diagram](images/architecture.png){#fig:architecture}

# Data Flow {#sec:dataflow}

The process follows these steps...

# Results

| Metric | Value | Unit |
|--------|-------|------|
| Speed  | 100   | ms   |
| Memory | 256   | MB   |

: Performance metrics {#tbl:results}

# Mathematical Model

The core formula is:

$$ E = mc^2 $$ {#eq:formula}

Equation @eq:formula shows Einstein's famous equation.
```

```bash
# Generate PDF with cross-references
pandoc document.md -o document.pdf \
    --filter pandoc-crossref \
    --citeproc \
    --pdf-engine=xelatex \
    --number-sections

# pandoc-crossref options in YAML
# ---
# figureTitle: "Figure"
# tableTitle: "Table"
# listingTitle: "Listing"
# figPrefix: "Fig."
# tblPrefix: "Table"
# eqnPrefix: "Eq."
# secPrefix: "Section"
# ---
```

### 9. Lua Filters

```lua
-- filters/word-count.lua
-- Count words in document

local word_count = 0

function Str(el)
    word_count = word_count + 1
    return el
end

function Pandoc(doc)
    print("Word count: " .. word_count)
    return doc
end
```

```lua
-- filters/uppercase-headers.lua
-- Convert all headers to uppercase

function Header(el)
    return pandoc.walk_block(el, {
        Str = function(s)
            return pandoc.Str(string.upper(s.text))
        end
    })
end
```

```lua
-- filters/remove-links.lua
-- Remove all hyperlinks, keeping text

function Link(el)
    return el.content
end
```

```lua
-- filters/custom-blocks.lua
-- Convert custom div blocks to styled output

function Div(el)
    if el.classes:includes("warning") then
        -- For LaTeX output
        local latex_begin = pandoc.RawBlock('latex',
            '\\begin{tcolorbox}[colback=yellow!10,colframe=orange]')
        local latex_end = pandoc.RawBlock('latex', '\\end{tcolorbox}')

        table.insert(el.content, 1, latex_begin)
        table.insert(el.content, latex_end)
        return el.content
    end

    if el.classes:includes("info") then
        local latex_begin = pandoc.RawBlock('latex',
            '\\begin{tcolorbox}[colback=blue!5,colframe=blue!50]')
        local latex_end = pandoc.RawBlock('latex', '\\end{tcolorbox}')

        table.insert(el.content, 1, latex_begin)
        table.insert(el.content, latex_end)
        return el.content
    end
end
```

```lua
-- filters/include-files.lua
-- Include content from external files

function CodeBlock(el)
    if el.classes:includes("include") then
        local file = io.open(el.text, "r")
        if file then
            local content = file:read("*all")
            file:close()

            -- Get file extension for syntax highlighting
            local ext = el.text:match("%.(%w+)$")
            local lang = ext or ""

            return pandoc.CodeBlock(content, {class = lang})
        end
    end
end
```

```bash
# Use Lua filters
pandoc document.md -o document.pdf \
    --lua-filter=filters/uppercase-headers.lua \
    --lua-filter=filters/custom-blocks.lua

# Chain multiple filters
pandoc document.md -o document.pdf \
    --filter pandoc-crossref \
    --lua-filter=filters/custom-blocks.lua \
    --citeproc
```

### 10. Batch Conversion Scripts

```bash
#!/bin/bash
# scripts/batch-convert.sh
# Convert all Markdown files to PDF

set -euo pipefail

# Configuration
INPUT_DIR="${1:-./docs}"
OUTPUT_DIR="${2:-./output}"
TEMPLATE="${3:-}"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Find and convert all markdown files
find "$INPUT_DIR" -name "*.md" -type f | while read -r file; do
    # Get relative path and create output path
    relative="${file#$INPUT_DIR/}"
    output_file="$OUTPUT_DIR/${relative%.md}.pdf"
    output_dir=$(dirname "$output_file")

    # Create output subdirectory
    mkdir -p "$output_dir"

    echo "Converting: $file -> $output_file"

    # Build pandoc command
    cmd=(pandoc "$file" -o "$output_file"
        --pdf-engine=xelatex
        --toc
        --number-sections
        --highlight-style=tango)

    # Add template if specified
    if [[ -n "$TEMPLATE" ]]; then
        cmd+=(--template="$TEMPLATE")
    fi

    # Execute conversion
    "${cmd[@]}"
done

echo "Batch conversion complete!"
echo "Output: $OUTPUT_DIR"
```

```bash
#!/bin/bash
# scripts/convert-to-all-formats.sh
# Convert a document to multiple formats

set -euo pipefail

INPUT_FILE="${1:?Usage: $0 <input.md>}"
BASE_NAME="${INPUT_FILE%.md}"

echo "Converting $INPUT_FILE to multiple formats..."

# PDF
echo "  -> PDF"
pandoc "$INPUT_FILE" -o "${BASE_NAME}.pdf" \
    --pdf-engine=xelatex \
    --toc \
    --number-sections

# DOCX
echo "  -> DOCX"
pandoc "$INPUT_FILE" -o "${BASE_NAME}.docx" \
    --toc

# HTML
echo "  -> HTML"
pandoc "$INPUT_FILE" -o "${BASE_NAME}.html" \
    --standalone \
    --toc \
    --embed-resources

# LaTeX
echo "  -> LaTeX"
pandoc "$INPUT_FILE" -o "${BASE_NAME}.tex"

# EPUB
echo "  -> EPUB"
pandoc "$INPUT_FILE" -o "${BASE_NAME}.epub" \
    --toc

echo "Done! Created:"
ls -la "${BASE_NAME}".*
```

```python
#!/usr/bin/env python3
"""
scripts/smart_convert.py
Smart document converter with configuration file support.
"""

import subprocess
import sys
from pathlib import Path
import yaml


def load_config(config_path: Path) -> dict:
    """Load conversion configuration from YAML."""
    with open(config_path) as f:
        return yaml.safe_load(f)


def convert_document(
    input_file: Path,
    output_file: Path,
    config: dict
) -> bool:
    """Convert a single document using pandoc."""
    cmd = ['pandoc', str(input_file), '-o', str(output_file)]

    # Add common options
    if config.get('toc'):
        cmd.append('--toc')
        if toc_depth := config.get('toc_depth'):
            cmd.extend(['--toc-depth', str(toc_depth)])

    if config.get('number_sections'):
        cmd.append('--number-sections')

    if template := config.get('template'):
        cmd.extend(['--template', template])

    if pdf_engine := config.get('pdf_engine'):
        cmd.extend(['--pdf-engine', pdf_engine])

    if highlight := config.get('highlight_style'):
        cmd.extend(['--highlight-style', highlight])

    if bibliography := config.get('bibliography'):
        cmd.append('--citeproc')
        cmd.extend(['--bibliography', bibliography])

    if csl := config.get('csl'):
        cmd.extend(['--csl', csl])

    # Add variables
    for key, value in config.get('variables', {}).items():
        cmd.extend(['-V', f'{key}={value}'])

    # Add filters
    for filter_name in config.get('filters', []):
        if filter_name.endswith('.lua'):
            cmd.extend(['--lua-filter', filter_name])
        else:
            cmd.extend(['--filter', filter_name])

    print(f"Running: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return False

    return True


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input.md> <output.pdf> [config.yaml]")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    config_file = Path(sys.argv[3]) if len(sys.argv) > 3 else None

    config = {}
    if config_file and config_file.exists():
        config = load_config(config_file)

    success = convert_document(input_file, output_file, config)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
```

```yaml
# config/pandoc-config.yaml
# Configuration for smart_convert.py

toc: true
toc_depth: 3
number_sections: true
pdf_engine: xelatex
highlight_style: tango

template: templates/report.tex
bibliography: references/main.bib
csl: styles/ieee.csl

variables:
  geometry: margin=1in
  fontsize: 11pt
  mainfont: Georgia
  monofont: Fira Code
  linkcolor: blue

filters:
  - pandoc-crossref
  - filters/custom-blocks.lua
```

### 11. Makefile for Document Projects

```makefile
# Makefile for document conversion project

# Configuration
PANDOC = pandoc
PDF_ENGINE = xelatex
TEMPLATE = templates/report.tex
BIBLIOGRAPHY = references/main.bib
CSL = styles/ieee.csl

# Directories
SRC_DIR = src
OUT_DIR = output
BUILD_DIR = build

# Source files
MD_FILES := $(wildcard $(SRC_DIR)/*.md)
PDF_FILES := $(patsubst $(SRC_DIR)/%.md,$(OUT_DIR)/%.pdf,$(MD_FILES))
DOCX_FILES := $(patsubst $(SRC_DIR)/%.md,$(OUT_DIR)/%.docx,$(MD_FILES))
HTML_FILES := $(patsubst $(SRC_DIR)/%.md,$(OUT_DIR)/%.html,$(MD_FILES))

# Common options
PANDOC_OPTS = --toc --number-sections --highlight-style=tango
PDF_OPTS = --pdf-engine=$(PDF_ENGINE) --template=$(TEMPLATE)
CITE_OPTS = --citeproc --bibliography=$(BIBLIOGRAPHY) --csl=$(CSL)

# Phony targets
.PHONY: all pdf docx html clean help

# Default target
all: pdf

# Build all PDFs
pdf: $(PDF_FILES)

# Build all DOCX
docx: $(DOCX_FILES)

# Build all HTML
html: $(HTML_FILES)

# Pattern rules
$(OUT_DIR)/%.pdf: $(SRC_DIR)/%.md $(TEMPLATE) $(BIBLIOGRAPHY) | $(OUT_DIR)
	@echo "Building PDF: $@"
	$(PANDOC) $< -o $@ $(PANDOC_OPTS) $(PDF_OPTS) $(CITE_OPTS)

$(OUT_DIR)/%.docx: $(SRC_DIR)/%.md $(BIBLIOGRAPHY) | $(OUT_DIR)
	@echo "Building DOCX: $@"
	$(PANDOC) $< -o $@ $(PANDOC_OPTS) $(CITE_OPTS)

$(OUT_DIR)/%.html: $(SRC_DIR)/%.md $(BIBLIOGRAPHY) | $(OUT_DIR)
	@echo "Building HTML: $@"
	$(PANDOC) $< -o $@ --standalone $(PANDOC_OPTS) $(CITE_OPTS) --embed-resources

# Create output directory
$(OUT_DIR):
	mkdir -p $(OUT_DIR)

# Clean build artifacts
clean:
	rm -rf $(OUT_DIR)/*
	rm -rf $(BUILD_DIR)/*

# Watch for changes (requires entr)
watch:
	find $(SRC_DIR) -name "*.md" | entr -c make pdf

# Help
help:
	@echo "Available targets:"
	@echo "  all    - Build all PDFs (default)"
	@echo "  pdf    - Build PDF files"
	@echo "  docx   - Build DOCX files"
	@echo "  html   - Build HTML files"
	@echo "  clean  - Remove built files"
	@echo "  watch  - Watch for changes and rebuild"
	@echo ""
	@echo "Source files: $(MD_FILES)"
```

### 12. GitHub Actions Workflow

```yaml
# .github/workflows/build-docs.yml
name: Build Documents

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'templates/**'
      - '.github/workflows/build-docs.yml'
  pull_request:
    paths:
      - 'docs/**'
      - 'templates/**'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install Pandoc
        run: |
          wget https://github.com/jgm/pandoc/releases/download/3.1.11/pandoc-3.1.11-linux-amd64.tar.gz
          tar xzf pandoc-3.1.11-linux-amd64.tar.gz
          sudo mv pandoc-3.1.11/bin/* /usr/local/bin/

      - name: Install pandoc-crossref
        run: |
          wget https://github.com/lierdakil/pandoc-crossref/releases/download/v0.3.17.0/pandoc-crossref-Linux.tar.xz
          tar xf pandoc-crossref-Linux.tar.xz
          sudo mv pandoc-crossref /usr/local/bin/

      - name: Install LaTeX
        run: |
          sudo apt-get update
          sudo apt-get install -y texlive-xetex texlive-fonts-recommended \
            texlive-latex-extra texlive-fonts-extra

      - name: Build PDF documents
        run: |
          mkdir -p output
          for file in docs/*.md; do
            output="output/$(basename "${file%.md}.pdf")"
            echo "Building: $file -> $output"
            pandoc "$file" -o "$output" \
              --pdf-engine=xelatex \
              --toc \
              --number-sections \
              --filter pandoc-crossref \
              --template=templates/report.tex
          done

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: documents
          path: output/*.pdf

  release:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: documents
          path: output

      - name: Create release
        uses: softprops/action-gh-release@v1
        if: startsWith(github.ref, 'refs/tags/')
        with:
          files: output/*.pdf
```

## Integration Examples

### Integration with Git Hooks

```bash
#!/bin/bash
# .git/hooks/pre-commit
# Rebuild PDFs before commit

set -e

# Check if any markdown files changed
changed_md=$(git diff --cached --name-only --diff-filter=ACM | grep '\.md$' || true)

if [[ -n "$changed_md" ]]; then
    echo "Rebuilding PDF documents..."

    for file in $changed_md; do
        if [[ -f "$file" ]]; then
            output="${file%.md}.pdf"
            echo "  Converting: $file -> $output"
            pandoc "$file" -o "$output" --pdf-engine=xelatex --toc
            git add "$output"
        fi
    done
fi
```

### Integration with VS Code Tasks

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Pandoc: Build PDF",
            "type": "shell",
            "command": "pandoc",
            "args": [
                "${file}",
                "-o",
                "${fileDirname}/${fileBasenameNoExtension}.pdf",
                "--pdf-engine=xelatex",
                "--toc",
                "--number-sections"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "presentation": {
                "echo": true,
                "reveal": "always"
            }
        },
        {
            "label": "Pandoc: Build DOCX",
            "type": "shell",
            "command": "pandoc",
            "args": [
                "${file}",
                "-o",
                "${fileDirname}/${fileBasenameNoExtension}.docx",
                "--toc"
            ]
        },
        {
            "label": "Pandoc: Watch and Build",
            "type": "shell",
            "command": "find . -name '*.md' | entr -c pandoc ${file} -o ${fileDirname}/${fileBasenameNoExtension}.pdf --pdf-engine=xelatex",
            "isBackground": true,
            "problemMatcher": []
        }
    ]
}
```

## Best Practices

### 1. Document Structure

```markdown
---
title: "Document Title"
author: "Author Name"
date: "2026-01-17"
abstract: |
  Brief summary of the document content.
---

# Introduction

Opening paragraph...

## Background

Context and background information...

# Main Content

## Section One

Content...

### Subsection

More detailed content...

## Section Two

Additional content...

# Conclusion

Summary and conclusions...

# References

::: {#refs}
:::

# Appendix A: Additional Data {.appendix}

Supplementary material...
```

### 2. Image Management

```markdown
<!-- Recommended image syntax -->

![Image caption](images/diagram.png){width=80%}

<!-- With cross-reference -->
![System architecture](images/arch.png){#fig:arch width=100%}

See @fig:arch for the overview.

<!-- Multiple images -->
::: {#fig:comparison layout-ncol=2}

![Before](images/before.png){#fig:before}

![After](images/after.png){#fig:after}

Comparison of results
:::
```

### 3. Code Block Best Practices

````markdown
<!-- Named code blocks with line numbers -->
```python {.numberLines startFrom="1"}
def process_data(data: list) -> dict:
    """Process input data and return results."""
    results = {}
    for item in data:
        results[item.id] = transform(item)
    return results
```

<!-- Highlighted lines -->
```python {.numberLines hl_lines=[2,4]}
def calculate(x, y):
    total = x + y  # highlighted
    average = total / 2
    return average  # highlighted
```
````

### 4. Table Formatting

```markdown
<!-- Simple table -->
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |

<!-- Table with caption and reference -->
| Metric | Value | Unit |
|--------|-------|------|
| Speed  | 100   | ms   |
| Memory | 256   | MB   |

: Performance metrics {#tbl:perf}

See @tbl:perf for benchmarks.

<!-- Grid tables (more flexible) -->
+---------------+---------------+
| Column 1      | Column 2      |
+===============+===============+
| Multi-line    | Another cell  |
| content here  |               |
+---------------+---------------+
| More data     | Final cell    |
+---------------+---------------+
```

## Troubleshooting

### Common Issues

#### PDF Engine Not Found

```bash
# Check if xelatex is installed
which xelatex

# Install on Ubuntu
sudo apt-get install texlive-xetex

# Use pdflatex instead
pandoc doc.md -o doc.pdf --pdf-engine=pdflatex
```

#### Missing LaTeX Packages

```bash
# Install specific package (TeX Live)
tlmgr install <package-name>

# Install common packages
sudo apt-get install texlive-latex-extra texlive-fonts-extra

# Check which package provides a file
tlmgr search --file <filename>
```

#### Unicode Characters in PDF

```bash
# Use XeLaTeX for Unicode support
pandoc doc.md -o doc.pdf \
    --pdf-engine=xelatex \
    -V mainfont="DejaVu Sans"
```

#### Images Not Found

```bash
# Use resource path
pandoc doc.md -o doc.pdf \
    --resource-path=.:images:assets

# Or use absolute paths in markdown
![Caption](/absolute/path/to/image.png)
```

#### Citations Not Processing

```bash
# Ensure --citeproc is included
pandoc doc.md -o doc.pdf \
    --citeproc \
    --bibliography=refs.bib

# Check BibTeX file syntax
biber --tool refs.bib
```

### Debug Mode

```bash
# Verbose output
pandoc doc.md -o doc.pdf --verbose

# Show intermediate LaTeX
pandoc doc.md -t latex > debug.tex

# Check Pandoc version and features
pandoc --version

# List supported formats
pandoc --list-input-formats
pandoc --list-output-formats
```

## Version History

### v1.0.0 (2026-01-17)

- Initial skill creation
- PDF, DOCX, HTML conversion workflows
- Custom LaTeX templates
- Citation management with BibTeX/CSL
- Cross-references with pandoc-crossref
- Lua filters documentation
- Batch conversion scripts
- Makefile integration
- GitHub Actions workflows

## Related Resources

- [Pandoc User's Guide](https://pandoc.org/MANUAL.html)
- [Pandoc Lua Filters](https://pandoc.org/lua-filters.html)
- [Citation Style Language](https://citationstyles.org/)
- [pandoc-crossref](https://lierdakil.github.io/pandoc-crossref/)
- [LaTeX Templates](https://www.latextemplates.com/)
- [Zotero Integration](https://www.zotero.org/support/quick_start_guide)

---

*Convert documents between any formats with Pandoc - the universal document converter.*
