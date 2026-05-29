---
name: upload-chapter-slides
description: |
  Upload PDF slides to CDN and configure chapter README with slides metadata.
  This skill should be used when adding teaching presentation slides to a chapter.
  Handles: PDF upload, part/chapter resolution, README frontmatter update, Teaching Aid heading.
allowed-tools: Bash, Read, Edit, Glob
---

# Upload Chapter Slides

Upload PDF teaching slides to CDN and update chapter README with proper metadata.

## Usage

```
/upload-chapter-slides <pdf-path> <chapter-number> [--title "Custom Title"] [--name custom-filename]
```

## Examples

```bash
# Basic usage - chapter number only
/upload-chapter-slides /path/to/slides.pdf 4

# With custom title
/upload-chapter-slides /path/to/slides.pdf 3 --title "Agentic AI - The Digital FTE"

# With custom filename (for CDN URL)
/upload-chapter-slides /path/to/slides.pdf 4 --name context-engineering-blueprint
```

## Workflow

### Step 1: Parse Arguments

Extract from user input:
- `pdf_path`: Absolute path to PDF file (required)
- `chapter_num`: Chapter number (required)
- `title`: Optional custom title for slides
- `name`: Optional custom filename for CDN

### Step 2: Resolve Chapter Path

```bash
# Find chapter folder by number
ls -d apps/learn-app/docs/*/[0-9][0-9]-*/ | grep "/${CHAPTER_NUM}-\|/${CHAPTER_NUM}[0-9]-"
```

Extract from path:
- Part number: First segment number (e.g., `01` from `01-General-Agents-Foundations`)
- Chapter folder: Full path to chapter directory

**Pattern**: `apps/learn-app/docs/{NN}-{PartName}/{NN}-{ChapterName}/`

### Step 3: Upload PDF

Run from project root:

```bash
cd apps/panaversity-fs-py && uv run python scripts/upload_asset.py \
  --file "{pdf_path}" \
  --type slides \
  --part {part_num} \
  --chapter {chapter_num} \
  --name {name_or_default}
```

Capture the CDN URL from output (format: `https://pub-*.r2.dev/books/ai-native-dev/static/slides/part-{N}/chapter-{NN}/{filename}.pdf`)

### Step 4: Update README Frontmatter

Read `{chapter_path}/README.md` and update YAML frontmatter:

**If `slides:` exists**: Replace the entire slides block
**If `slides:` missing**: Add after `title:` line

```yaml
slides:
  source: "{cdn_url}"
  title: "{title_or_chapter_title}"
  height: 700
```

### Step 5: Ensure Teaching Aid Heading

Check if `## 📚 Teaching Aid` exists in README.

**If missing**: Add before `## What You'll Learn` (or first `##` heading if no What You'll Learn):

```markdown
## 📚 Teaching Aid

## What You'll Learn
```

**If exists**: No change needed.

### Step 6: Report Success

```
✅ Chapter {N} slides uploaded

CDN URL: {cdn_url}
README:  {chapter_path}/README.md
Title:   {slides_title}
```

## Error Handling

| Error | Resolution |
|-------|------------|
| PDF file not found | Verify path exists |
| Chapter not found | Run `ls -d apps/learn-app/docs/*/` to list valid chapters |
| Upload failed | Check `apps/panaversity-fs-py/.env` configuration |
| README missing | Chapter may not be initialized |

## Path Constants

```
PROJECT_ROOT: /Users/mjs/Documents/code/panaversity-official/tutorsgpt/agentfactory
DOCS_PATH:    apps/learn-app/docs
UPLOAD_SCRIPT: apps/panaversity-fs-py/scripts/upload_asset.py
```

## README Structure Reference

Correct structure after skill runs:

```yaml
---
sidebar_position: N
title: "Chapter N: Title"
slides:
  source: "https://pub-*.r2.dev/books/ai-native-dev/static/slides/part-N/chapter-NN/filename.pdf"
  title: "Slide Title"
  height: 700
---

# Chapter N: Title

[intro paragraphs]

## 📚 Teaching Aid

## What You'll Learn

[content]
```
