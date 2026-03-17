---
name: markdown-toc
description: Use when generating or updating Table of Contents in markdown files. Supports multiple files, glob patterns, configurable header levels, and various insertion modes. Triggered by "generate toc", "update toc", "table of contents", "add toc to markdown".
---

# Markdown Table of Contents Generator

A universal TOC generator that works with any markdown file. Supports batch processing, configurable header levels, and smart insertion.

## Quick Start

```bash
# Single file
python "${CLAUDE_PLUGIN_ROOT}/scripts/generate_toc.py" README.md

# Preview without changes
python "${CLAUDE_PLUGIN_ROOT}/scripts/generate_toc.py" --dry-run README.md

# All markdown files in docs/
python "${CLAUDE_PLUGIN_ROOT}/scripts/generate_toc.py" docs/*.md

# Recursive processing
python "${CLAUDE_PLUGIN_ROOT}/scripts/generate_toc.py" --recursive .
```

**Note**: You can also copy the script to your project and run it locally.

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--dry-run` | false | Preview TOC without modifying files |
| `--min-level N` | 2 | Minimum header level (1-6) |
| `--max-level N` | 3 | Maximum header level (1-6) |
| `--title TEXT` | "Table of Contents" | Custom TOC title |
| `--no-title` | false | Omit TOC title |
| `--recursive, -r` | false | Process .md files recursively |
| `--insert MODE` | auto | Insertion mode: auto, top, marker |
| `--marker TEXT` | `<!-- TOC -->` | Custom marker for marker mode |

## Insertion Modes

### Auto Mode (default)

Smart detection in this order:
1. Replace existing `## Table of Contents` section
2. Insert after first `---` separator (common README pattern)
3. Insert after YAML frontmatter
4. Insert after first header
5. Insert at top of file

```bash
python scripts/generate_toc.py README.md
```

### Top Mode

Insert at top of file, respecting YAML frontmatter:

```bash
python scripts/generate_toc.py --insert top README.md
```

### Marker Mode

Insert/replace between marker pairs:

```bash
python scripts/generate_toc.py --insert marker README.md
```

In your markdown file:
```markdown
<!-- TOC -->
(TOC will be inserted/updated here)
<!-- /TOC -->
```

Custom markers:
```bash
python scripts/generate_toc.py --insert marker --marker "<!-- INDEX -->" README.md
```

## Header Level Control

Include only H2-H3 (default):
```bash
python scripts/generate_toc.py README.md
```

Include H1-H4:
```bash
python scripts/generate_toc.py --min-level 1 --max-level 4 README.md
```

Include only H2:
```bash
python scripts/generate_toc.py --min-level 2 --max-level 2 README.md
```

## Batch Processing

### Glob Patterns

```bash
# All .md in current directory
python scripts/generate_toc.py *.md

# All .md in docs/
python scripts/generate_toc.py docs/*.md

# Specific pattern
python scripts/generate_toc.py docs/guide-*.md
```

### Recursive

```bash
# All .md files recursively
python scripts/generate_toc.py --recursive .

# Recursive in specific directory
python scripts/generate_toc.py --recursive docs/
```

### Multiple Paths

```bash
python scripts/generate_toc.py README.md CONTRIBUTING.md docs/
```

## Output Examples

### With Title (default)

```markdown
## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Advanced Usage](#advanced-usage)
- [Contributing](#contributing)
```

### Without Title

```bash
python scripts/generate_toc.py --no-title README.md
```

```markdown
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
```

### Custom Title

```bash
python scripts/generate_toc.py --title "Contents" README.md
```

```markdown
## Contents

- [Installation](#installation)
```

## Anchor Generation

GitHub-compatible anchors:
- Lowercase conversion
- Spaces to hyphens
- Special characters removed
- Markdown formatting stripped (`**bold**`, `` `code` ``)
- Emoji removed
- Multiple hyphens collapsed

| Header | Anchor |
|--------|--------|
| `## Getting Started` | `#getting-started` |
| `## **Bold** Header` | `#bold-header` |
| `## Header with `code`` | `#header-with-code` |
| `## Header #1` | `#header-1` |

## Skipped Content

The script automatically skips:
- YAML frontmatter (between `---` markers)
- Code blocks (``` or ~~~)
- Existing "Table of Contents" headers
- Headers outside configured level range

## Dry Run Preview

Always preview first with `--dry-run`:

```bash
python scripts/generate_toc.py --dry-run README.md
```

Output:
```
[INFO] Found 1 markdown file(s)

============================================================
File: README.md
============================================================
## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
...

Found 15 headers (levels 2-3)
```

## Common Workflows

### Update All Project Documentation

```bash
python scripts/generate_toc.py --recursive --dry-run .
# Review output, then:
python scripts/generate_toc.py --recursive .
```

### Standardize TOC Markers

```bash
# Add markers to files, then:
python scripts/generate_toc.py --insert marker --recursive docs/
```

### Different Levels for Different Files

```bash
# Deep TOC for main README
python scripts/generate_toc.py --max-level 4 README.md

# Shallow TOC for guides
python scripts/generate_toc.py --max-level 2 docs/guides/*.md
```

## Troubleshooting

### "No headers found"
File may only have H1 headers. Use `--min-level 1`.

### TOC inserted in wrong place
Use `--insert marker` with explicit markers for precise control.

### Anchors don't work
Check for duplicate headers (GitHub appends `-1`, `-2`, etc.).

## Portability

This script is fully portable:
- No hardcoded paths or project-specific values
- Works with any markdown file
- Standard Python 3 with no dependencies
- Can be copied to any project
