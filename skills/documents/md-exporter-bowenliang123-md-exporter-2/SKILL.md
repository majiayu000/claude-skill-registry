---
name: markdown-exporter
description: Markdown exporter for export Markdown text to DOCX, PPTX, XLSX, PDF, PNG, HTML, IPYNB, MD, CSV, JSON, JSONL, XML files, and extract code blocks in Markdown to Python, Bash,JS and etc files. Also known as the md_exporter skill.
disable: false
metadata:
  openclaw:
    homepage: https://github.com/bowenliang123/md_exporter/
    emoji: 🖨
    requires:
      bins: [markdown-exporter]
    install:
      - kind: uv
        package: md-exporter
        bins: [markdown-exporter]
---


## ✨ What is Markdown Exporter?

**Markdown Exporter** is a Agent Skill that transforms your Markdown text into a wide variety of professional formats. Whether you need to create polished reports, stunning presentations, organized spreadsheets, or code files—this tool has you covered.

### Tools and Supported Formats

| Tool | Input (File path of Markdown text or styles) | Output (File path of exported file) |
|------|-------|--------|
| `md_to_docx` | 📝 Markdown text | 📄 Word document (.docx) |
| `md_to_html` | 📝 Markdown text | 🌐 HTML file (.html) |
| `md_to_html_text` | 📝 Markdown text | 🌐 HTML text string |
| `md_to_pdf` | 📝 Markdown text | 📑 PDF file (.pdf) |
| `md_to_png` | 📝 Markdown text | 🖼️ PNG image(s) of PDF pages |
| `md_to_md` | 📝 Markdown text | 📝 Markdown file (.md) |
| `md_to_ipynb` | 📝 Markdown text | 📓 Jupyter Notebook (.ipynb) |
| `md_to_pptx` | 📝 Markdown slides in [Pandoc style](https://pandoc.org/MANUAL.html#slide-shows) | 🎯 PowerPoint (.pptx) |
| `md_to_xlsx` | 📋 [Markdown tables](https://www.markdownguide.org/extended-syntax/#tables) | 📊 Excel spreadsheet (.xlsx) |
| `md_to_csv` | 📋 [Markdown tables](https://www.markdownguide.org/extended-syntax/#tables) | 📋 CSV file (.csv) |
| `md_to_json` | 📋 [Markdown tables](https://www.markdownguide.org/extended-syntax/#tables) | 📦 JSON/JSONL file (.json) |
| `md_to_xml` | 📋 [Markdown tables](https://www.markdownguide.org/extended-syntax/#tables) | 🏷️ XML file (.xml) |
| `md_to_latex` | 📋 [Markdown tables](https://www.markdownguide.org/extended-syntax/#tables) | 📝 LaTeX file (.tex) |
| `md_to_codeblock` | 💻 [Code blocks in Markdown](https://www.markdownguide.org/extended-syntax/#fenced-code-blocks) | 📁 Code files by language (.py, .js, .sh, etc.) |

## Prerequisites

To use the Markdown Exporter skill, ensure you have the following prerequisites installed:
- Python 3.11 or higher
- (optional) uv package manager


## 📦 Usage

### Overview
Markdown Exporter is now available as a PyPI package, which provides a seamless command-line interface for all its functionality.

### Installation
You can install the package directly from PyPI using pip:

```bash
pip install md-exporter
```

### Basic Usage
After installation, you can use the `markdown-exporter` command to access all the tools:

```bash
markdown-exporter <subcommand> <args> [options]
```

### Important Notes
- All commands only support file paths as input
- The package handles all dependency management automatically
- You can run the command from anywhere in your system, no need to navigate to the project directory


## 🔧 Scripts

### md_to_csv - Convert Markdown tables to CSV

Converts Markdown tables to CSV format.

**Usage:**
```bash
markdown-exporter md_to_csv <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path
- `output` - Output CSV file path

**Options:**
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
markdown-exporter md_to_csv /path/input.md /path/output.csv
```


### md_to_pdf - Convert Markdown to PDF

Converts Markdown text to PDF format with support for Chinese, Japanese, and other languages.

**Usage:**
```bash
markdown-exporter md_to_pdf <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path
- `output` - Output PDF file path

**Options:**
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
markdown-exporter md_to_pdf /path/input.md /path/output.pdf
```


### md_to_docx - Convert Markdown to DOCX

Converts Markdown text to DOCX format using pandoc.

**Usage:**
```bash
markdown-exporter md_to_docx <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path
- `output` - Output DOCX file path

**Options:**
- `--template` - Path to DOCX template file (optional)
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
markdown-exporter md_to_docx /path/input.md /path/output.docx
markdown-exporter md_to_docx /path/input.md /path/output.docx --template /path/template.docx
```


### md_to_xlsx - Convert Markdown tables to XLSX

Converts Markdown tables to XLSX format with multiple sheets support.

**Usage:**
```bash
markdown-exporter md_to_xlsx <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path
- `output` - Output XLSX file path

**Options:**
- `--force-text` - Convert cell values to text type (default: True)
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
markdown-exporter md_to_xlsx /path/input.md /path/output.xlsx
```


### md_to_pptx - Convert Markdown to PPTX

Converts Markdown text to PPTX format using pandoc.

**Usage:**
```bash
markdown-exporter md_to_pptx <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path
- `output` - Output PPTX file path

**Options:**
- `--template` - Path to PPTX template file (optional)

**Example:**
```bash
markdown-exporter md_to_pptx /path/input.md /path/output.pptx
```


### md_to_codeblock - Extract Codeblocks to Files

Extracts code blocks from Markdown and saves them as individual files.

**Usage:**
```bash
markdown-exporter md_to_codeblock <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path
- `output` - Output file or directory path

**Options:**
- `--compress` - Compress all code blocks into a ZIP file

**Example:**
```bash
markdown-exporter md_to_codeblock /path/input.md /path/output_dir
markdown-exporter md_to_codeblock /path/input.md /path/output.zip --compress
```


### md_to_json - Convert Markdown Tables to JSON

Converts Markdown tables to JSON or JSONL format.

**Usage:**
```bash
markdown-exporter md_to_json <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path
- `output` - Output JSON file path

**Options:**
- `--style` - JSON output style: `jsonl` (default) or `json_array`
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
markdown-exporter md_to_json /path/input.md /path/output.json
markdown-exporter md_to_json /path/input.md /path/output.json --style json_array
```


### md_to_xml - Convert Markdown to XML

Converts Markdown text to XML format.

**Usage:**
```bash
markdown-exporter md_to_xml <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path
- `output` - Output XML file path

**Options:**
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
markdown-exporter md_to_xml /path/input.md /path/output.xml
```


### md_to_latex - Convert Markdown Tables to LaTeX

Converts Markdown tables to LaTeX format.

**Usage:**
```bash
markdown-exporter md_to_latex <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path
- `output` - Output LaTeX file path

**Options:**
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
markdown-exporter md_to_latex /path/input.md /path/output.tex
```


### md_to_html - Convert Markdown to HTML

Converts Markdown text to HTML format using pandoc.

**Usage:**
```bash
markdown-exporter md_to_html <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path
- `output` - Output HTML file path

**Options:**
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
markdown-exporter md_to_html /path/input.md /path/output.html
```


### md_to_html_text - Convert Markdown to HTML Text

Converts Markdown text to HTML and outputs to stdout.

**Usage:**
```bash
markdown-exporter md_to_html_text <input>
```

**Arguments:**
- `input` - Input Markdown file path

**Example:**
```bash
markdown-exporter md_to_html_text /path/input.md
```


### md_to_png - Convert Markdown to PNG Images

Converts Markdown text to PNG images (one per page).

**Usage:**
```bash
markdown-exporter md_to_png <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path
- `output` - Output PNG file path or directory path

**Options:**
- `--compress` - Compress all PNG images into a ZIP file
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
markdown-exporter md_to_png /path/input.md /path/output.png
markdown-exporter md_to_png /path/input.md /path/output.png --compress
```


### md_to_md - Convert Markdown to MD File

Saves Markdown text to a .md file.

**Usage:**
```bash
markdown-exporter md_to_md <input> <output>
```

**Arguments:**
- `input` - Input Markdown file path
- `output` - Output MD file path

**Example:**
```bash
markdown-exporter md_to_md /path/input.md /path/output.md
```



### md_to_ipynb - Convert Markdown to IPYNB

Converts Markdown text to Jupyter Notebook (.ipynb) format.

**Usage:**
```bash
markdown-exporter md_to_ipynb <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path
- `output` - Output IPYNB file path

**Options:**
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
markdown-exporter md_to_ipynb /path/input.md /path/output.ipynb
```


## 📝 Notes

- All scripts only support file paths as input
- For scripts that generate multiple files (e.g., multiple tables, multiple code blocks), the output filename will be automatically numbered
- Use the `--strip-wrapper` option to remove code block wrappers (```) from the input Markdown
