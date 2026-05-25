---
name: paper-analyzer
description: |
  Transform academic papers into in-depth technical articles with multiple writing style options.
  Use the MinerU Cloud API for high-precision PDF parsing, automatically extracting images, tables, and formulas.
  Optional formula explanations and GitHub code analysis, generating Markdown and HTML formats.
---

# Academic Paper Analyzer – In-Depth Analysis of Academic Papers

## Core Capabilities

- **MinerU Cloud API** for high-precision PDF parsing
- Automatic extraction of images, tables, and LaTeX formulas
- **Multiple writing styles**: storytelling / academic / concise
- **Optional formula explanations**: insert formula images with detailed symbol explanations
- **Optional code analysis**: combine explanations with GitHub open-source code
- Output Markdown + HTML (base64-embedded images)

## Prerequisites

### MinerU API Token

1. Visit https://mineru.net and register an account
2. Obtain an API Token
3. Set an environment variable (recommended):
   ```bash
   export MINERU_TOKEN="your_token_here"
   ```

### Dependency Installation

```bash
pip install requests markdown
```

## Workflow

### Step 1: PDF Parsing (Using MinerU API)

```bash
python scripts/mineru_api.py <pdf_path> <output_dir>
```

Or pass the token directly:
```bash
python scripts/mineru_api.py paper.pdf ./output YOUR_TOKEN
```

**Output:**
- `output_dir/*.md` – Markdown files (including formulas and tables)
- `output_dir/images/` – High-quality extracted images

### Step 2: Extract Paper Metadata

```bash
python scripts/extract_paper_info.py <output_dir>/*.md paper_info.json
```

### Step 3: Style Selection (Ask the User)

Before generating the article, **you must ask the user** to choose the following options:

#### 1. Writing Style (Required)

| Style | Characteristics | Use Cases |
|------|-----------------|-----------|
| **storytelling** | Starts from intuition, uses metaphors and examples, narrative-driven | Blogs, tech columns, popular science |
| **academic** | Professional terminology, rigorous expression, preserves original concepts | Academic reports, surveys, research group sharing |
| **concise** | Straight to the point, tables and lists, high information density | Quick reads, paper overviews, technical research |

#### 2. Formula Option (Optional)

| Option | Description |
|------|-------------|
| **with-formulas** | Insert formula images and explain symbol meanings in detail |
| **no-formulas** (default) | Pure text description, no formula images |

#### 3. Code Option (Optional, only if the paper has GitHub)

| Option | Description |
|------|-------------|
| **with-code** | Clone the repository, include key source code, and explain it alongside the paper |
| **no-code** (default) | No code analysis |

### Step 4: Intelligent Article Generation

(...)

## API Limits

- Maximum file size: 200MB
- Maximum pages per file: 600
- Supports PDF, DOC, PPT, images, and more
