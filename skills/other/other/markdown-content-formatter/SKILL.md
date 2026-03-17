---
name: markdown-content-formatter
description: Format and validate markdown documents with auto-generated TOC, frontmatter, structure validation, and cross-reference linking. Export to GitHub/CommonMark/Jekyll/Hugo.
---

# Markdown Content Formatter

Structure, validate, and format long-form markdown content for documentation, blogs, and static site generators. Auto-generate tables of contents, add frontmatter, validate structure, and convert between markdown flavors.

## Workflow

The markdown formatting process follows these steps:

1. **Load** - Read markdown file or content
2. **Validate** - Check heading hierarchy, broken links, structure issues
3. **Format** - Apply formatting rules (spacing, code blocks, etc.)
4. **Generate** - Add TOC, frontmatter, cross-references
5. **Export** - Save in target markdown flavor

## Quick Start

```python
from scripts.markdown_formatter import MarkdownFormatter

# Load and format markdown
formatter = MarkdownFormatter(file_path='document.md')

# Generate table of contents
toc = formatter.generate_toc(max_depth=3)

# Validate structure
validation = formatter.validate_structure()
if not validation['valid']:
    print("Issues found:")
    for error in validation['errors']:
        print(f"  - {error['message']}")

# Add frontmatter
formatter.add_frontmatter({
    'title': 'My Document',
    'author': 'John Doe',
    'date': '2024-01-15'
})

# Export formatted version
formatter.export(
    output_path='formatted.md',
    include_toc=True,
    target_flavor='github'
)
```

## Formatting Operations

### 1. Table of Contents Generation

Auto-generate TOC from document heading structure:
- Customizable depth (H2, H3, etc.)
- GitHub-style anchor links
- Numbered or bulleted format
- Smart indentation based on heading levels

### 2. Frontmatter Management

Add YAML/TOML/JSON frontmatter for static site generators:
- YAML (`---`) for Jekyll/Hugo
- TOML (`+++`) for Hugo
- JSON for custom parsers
- Structured metadata (title, author, date, tags, etc.)

### 3. Structure Validation

Check document structure for common issues:
- **Heading hierarchy** - Detect skipped levels (H2 → H4)
- **Broken links** - Find invalid internal (#anchors) and external links
- **Duplicate headings** - Identify heading ID conflicts
- **Missing elements** - Check for required sections

### 4. Code Block Formatting

Enhance code blocks with syntax highlighting markers:
- Add language tags to fenced code blocks
- Convert indented code to fenced blocks
- Default language specification
- Consistent formatting

### 5. Cross-Reference Linking

Auto-link headings and create cross-references:
- Generate unique heading IDs
- Link section mentions (e.g., "see Introduction")
- Create anchor links for internal navigation
- Handle duplicate heading names

### 6. Spacing and Consistency

Apply consistent formatting rules:
- Line breaks around headings
- List formatting (bullets, numbers)
- Code block spacing
- Paragraph breaks
- Horizontal rules

### 7. Flavor Conversion

Convert between markdown flavors:
- **GitHub Flavored Markdown** - Task lists, tables, syntax highlighting
- **CommonMark** - Standard specification
- **Jekyll** - Liquid templates, includes
- **Hugo** - Shortcodes, taxonomies

## Validation Checks

The validator identifies these common issues:

| Issue Type | Description | Example |
|------------|-------------|---------|
| Heading Skip | Level jumps (H2 → H4) | Missing H3 between H2 and H4 |
| Broken Link | Invalid internal/external link | `[link](#missing-section)` |
| Duplicate Heading | Same heading appears multiple times | Two "Introduction" headings |
| Missing ID | Heading lacks unique identifier | Anchor link fails |
| Invalid Structure | Incorrect nesting or formatting | List inside heading |

## API Reference

### MarkdownFormatter

**Initialization**:
```python
formatter = MarkdownFormatter(
    file_path='document.md',  # OR
    content='# Markdown text...'
)
```

**Parameters**:
- `file_path` (str): Path to markdown file (optional)
- `content` (str): Direct markdown content (optional)

One of `file_path` or `content` must be provided.

### Table of Contents

#### generate_toc()
```python
toc = formatter.generate_toc(
    max_depth=3,        # Max heading level (1-6)
    start_level=2,      # Start from H2 (skip H1)
    style='github'      # 'github', 'numbered', 'bullets'
)
```

**Returns**: TOC markdown string

**Styles**:
- `github` - Bulleted list with anchor links
- `numbered` - Numbered outline
- `bullets` - Simple bullet list

**Example Output (github style)**:
```markdown
## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Advanced Topics](#advanced-topics)
```

### Frontmatter

#### add_frontmatter()
```python
content = formatter.add_frontmatter(
    metadata={
        'title': 'Document Title',
        'author': 'John Doe',
        'date': '2024-01-15',
        'tags': ['markdown', 'documentation']
    },
    format='yaml'  # 'yaml', 'toml', or 'json'
)
```

**Returns**: Markdown content with frontmatter prepended

**Example Output (YAML)**:
```yaml
---
title: Document Title
author: John Doe
date: 2024-01-15
tags:
  - markdown
  - documentation
---
```

### Validation

#### validate_structure()
```python
result = formatter.validate_structure()
```

**Returns**: Dictionary with validation results
```python
{
    'valid': bool,
    'errors': [
        {
            'type': 'heading_skip',
            'line': 45,
            'message': 'Heading level jumps from H2 to H4'
        }
    ],
    'warnings': [
        {
            'type': 'duplicate_heading',
            'line': 120,
            'message': 'Heading "Introduction" appears multiple times'
        }
    ]
}
```

### Code Blocks

#### format_code_blocks()
```python
content = formatter.format_code_blocks(
    add_language_tags=True,
    default_language='text'
)
```

**Returns**: Markdown with formatted code blocks

Converts:
```
    code here
```

To:
````
```text
code here
```
````

### Cross-References

#### auto_link_headings()
```python
content = formatter.auto_link_headings()
```

**Returns**: Markdown with heading IDs and cross-reference links

Generates GitHub-style anchors:
- `# Getting Started` → `<a id="getting-started"></a>`
- Links "see Getting Started" → `[Getting Started](#getting-started)`

### Spacing

#### fix_spacing()
```python
content = formatter.fix_spacing()
```

**Returns**: Markdown with consistent spacing

Applies rules:
- 2 blank lines before H1
- 1 blank line before H2-H6
- 1 blank line around code blocks
- 1 blank line around lists

### Flavor Conversion

#### convert_to_flavor()
```python
content = formatter.convert_to_flavor(target='jekyll')
```

**Parameters**:
- `target` (str): 'github', 'commonmark', 'jekyll', or 'hugo'

**Returns**: Converted markdown string

### Export

#### export()
```python
formatter.export(
    output_path='formatted.md',
    include_toc=True,
    include_frontmatter=True,
    target_flavor='github'
)
```

**Parameters**:
- `output_path` (str): Output file path
- `include_toc` (bool): Add TOC at beginning
- `include_frontmatter` (bool): Preserve/add frontmatter
- `target_flavor` (str): Target markdown flavor

## CLI Usage

### Generate TOC

```bash
python scripts/markdown_formatter.py \
    --input document.md \
    --toc \
    --toc-depth 3 \
    --toc-style github \
    --output formatted.md
```

### Add Frontmatter

```bash
# From command line
python scripts/markdown_formatter.py \
    --input document.md \
    --frontmatter title="My Doc" author="John Doe" date="2024-01-15" \
    --output formatted.md

# From file
python scripts/markdown_formatter.py \
    --input document.md \
    --frontmatter-file metadata.yaml \
    --output formatted.md
```

### Validate Structure

```bash
python scripts/markdown_formatter.py \
    --input document.md \
    --validate \
    --format json
```

**Output**:
```json
{
  "valid": false,
  "errors": [
    {
      "type": "heading_skip",
      "line": 45,
      "message": "Heading level jumps from H2 to H4"
    }
  ],
  "warnings": []
}
```

### Full Formatting

```bash
python scripts/markdown_formatter.py \
    --input document.md \
    --toc \
    --frontmatter title="My Doc" \
    --auto-link \
    --fix-spacing \
    --flavor github \
    --output formatted.md
```

### Batch Processing

```bash
# Format all markdown files in directory
for file in docs/*.md; do
    python scripts/markdown_formatter.py \
        --input "$file" \
        --toc \
        --fix-spacing \
        --output "formatted/$file"
done
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input`, `-i` | Input markdown file | Required |
| `--output`, `-o` | Output file path | stdout |
| `--toc` | Generate table of contents | False |
| `--toc-depth` | Max TOC depth (1-6) | 3 |
| `--toc-style` | TOC style (github/numbered/bullets) | github |
| `--frontmatter` | Key=value pairs for frontmatter | - |
| `--frontmatter-file` | YAML file with frontmatter | - |
| `--auto-link` | Auto-link headings | False |
| `--fix-spacing` | Fix spacing and formatting | False |
| `--flavor` | Target markdown flavor | github |
| `--validate` | Validate structure only | False |
| `--format` | Output format for validation (json/text) | text |

## Examples

### Example 1: Auto-Generate TOC

```python
formatter = MarkdownFormatter(file_path='guide.md')
toc = formatter.generate_toc(max_depth=3, style='github')

print(toc)
# ## Table of Contents
# - [Introduction](#introduction)
# - [Setup](#setup)
#   - [Installation](#installation)
#   - [Configuration](#configuration)
```

### Example 2: Add Jekyll Frontmatter

```python
formatter = MarkdownFormatter(file_path='post.md')

formatter.add_frontmatter({
    'layout': 'post',
    'title': 'Getting Started with Markdown',
    'date': '2024-01-15',
    'categories': ['tutorial', 'markdown'],
    'tags': ['beginner', 'documentation']
}, format='yaml')

formatter.export('_posts/2024-01-15-getting-started.md')
```

### Example 3: Validate Document Structure

```python
formatter = MarkdownFormatter(file_path='documentation.md')
result = formatter.validate_structure()

if not result['valid']:
    print("Errors found:")
    for error in result['errors']:
        print(f"Line {error['line']}: {error['message']}")

    print("\nWarnings:")
    for warning in result['warnings']:
        print(f"Line {warning['line']}: {warning['message']}")
else:
    print("Document structure is valid!")
```

### Example 4: Fix Common Issues

```python
formatter = MarkdownFormatter(file_path='messy.md')

# Fix spacing issues
formatter.fix_spacing()

# Format code blocks
formatter.format_code_blocks(default_language='python')

# Add heading IDs
formatter.auto_link_headings()

# Export cleaned version
formatter.export('clean.md', target_flavor='github')
```

### Example 5: Convert for Hugo Static Site

```python
formatter = MarkdownFormatter(file_path='article.md')

# Add Hugo frontmatter
formatter.add_frontmatter({
    'title': 'My Article',
    'date': '2024-01-15T10:00:00Z',
    'draft': False,
    'tags': ['hugo', 'static-site'],
    'categories': ['web-development']
}, format='toml')

# Generate TOC
toc = formatter.generate_toc(max_depth=2)

# Convert to Hugo flavor
formatter.convert_to_flavor('hugo')

# Export
formatter.export(
    output_path='content/posts/my-article.md',
    include_toc=True,
    target_flavor='hugo'
)
```

### Example 6: Batch Validation

```bash
# Validate all markdown files
for file in docs/**/*.md; do
    echo "Validating $file..."
    python scripts/markdown_formatter.py \
        --input "$file" \
        --validate \
        --format json > "${file}.validation.json"
done

# Find files with errors
jq -r 'select(.valid == false) | input_filename' docs/**/*.validation.json
```

## Dependencies

```
markdown>=3.5.0
pyyaml>=6.0.0
beautifulsoup4>=4.12.0
pandas>=2.0.0
```

Install dependencies:
```bash
pip install -r scripts/requirements.txt
```

## Limitations

- **Link Validation**: External link checking requires network requests (not performed by default)
- **Markdown Parsing**: Uses Python-Markdown library; some edge cases may differ from other parsers
- **Flavor Differences**: Not all flavor-specific features are converted (e.g., Hugo shortcodes)
- **Heading Anchors**: Anchor generation follows GitHub algorithm but may differ from other platforms
- **Code Language Detection**: Automatic language detection is limited; manual tags recommended
- **Large Files**: Very large files (>10MB) may be slow to process
- **Unicode**: Some unicode characters in heading anchors may cause issues
- **Nested Lists**: Complex nested list structures may not format perfectly
- **HTML in Markdown**: Raw HTML blocks are preserved but not validated
- **Math Equations**: LaTeX math equations are not parsed or validated

## Markdown Flavor Notes

### GitHub Flavored Markdown (GFM)
- Task lists: `- [ ] Task` / `- [x] Done`
- Tables with alignment
- Strikethrough: `~~text~~`
- Automatic link detection

### CommonMark
- Strict specification adherence
- No extensions (no task lists, no tables)
- Predictable parsing

### Jekyll
- Liquid templating: `{{ variable }}`
- Includes: `{% include file.html %}`
- Frontmatter required

### Hugo
- Shortcodes: `{{< shortcode >}}`
- TOML frontmatter preferred
- Taxonomies (tags, categories)
- Nested sections
