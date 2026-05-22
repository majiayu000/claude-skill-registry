---
name: pdf-author
description: Generate professional PDF documents using Typst with proper Chinese font rendering (Source Han Serif/Sans) and syntax-highlighted code blocks that break across pages naturally. Includes visual validation by converting PDFs to PNG and inspecting with multimodal capabilities. Use when the user requests PDF generation, document creation with Chinese text, Typst compilation, or when working with Chinese fonts and long code examples that need proper page breaks.
---

# PDF Author Skill

A skill for generating professional PDFs using Typst with proper Chinese font support and code block handling, with built-in validation using multimodal capabilities.

## Purpose

Generate PDF documents with:
- Proper Chinese character rendering (Source Han Serif/Sans fonts)
- Syntax-highlighted code blocks with frames
- Breakable code blocks that span multiple pages
- Visual validation by converting to PNG and inspecting

## Usage

When the user requests PDF generation with Chinese content or code examples, use this skill to:

1. Create/update Typst (.typ) files with proper configuration
2. Compile to PDF using Docker
3. Convert PDF to PNG for validation
4. Inspect the rendered output to verify quality

## Typst Template Configuration

### Quick Start

A complete template is available at `.claude/skills/pdf-author/template.typ` that you can copy and modify.

### Required Setup

Always include this header in Typst files for Chinese support and proper code block styling:

```typst
#set page(paper: "a4", margin: 2.5cm)
#set text(font: "Source Han Serif SC", lang: "zh")

// Code block styling with breakable frames
#show raw.where(block: true): it => block(
  width: 100%,
  fill: luma(245),
  stroke: 1pt + luma(180),
  radius: 4pt,
  inset: 10pt,
  breakable: true
)[#it]
```

### Font Options

- **Source Han Serif SC** (思源宋体): Serif font with traditional decorative strokes
- **Source Han Sans SC** (思源黑体): Modern sans-serif font

### Including External Code Files

Instead of inline code blocks, use external file inclusion:

```typst
// For any programming language
#raw(read("example.py"), lang: "python", block: true)
#raw(read("script.sh"), lang: "bash", block: true)
#raw(read("main.cpp"), lang: "cpp", block: true)
```

## Workflow

### Step 1: Create Typst Document

Create a `.typ` file with:
- Proper page and font settings
- Code block styling (breakable frames)
- Content structure using headings, paragraphs, code examples

### Step 2: Compile to PDF

Use the Docker-based compilation:

```bash
docker run -v $(CURDIR):/workspace -w /workspace typst_cn typst compile <filename>.typ
```

Or if a Makefile exists with a `compile` target:

```bash
make compile
```

### Step 3: Convert PDF to PNG

Convert the PDF to PNG images for visual inspection:

```bash
docker run --rm -v /home/wr/tmp/try_typst:/workspace -w /workspace minidocks/poppler pdftoppm <filename>.pdf output-page -png
```

**Important**: Use the full absolute path for the volume mount, not `$(CURDIR)` which doesn't work in bash.

### Step 4: Validate Output

Read the generated PNG files using the Read tool to visually inspect:
- Chinese character rendering quality
- Code block frames and formatting
- Page breaks and content flow
- Syntax highlighting

Check for common issues:
- Blank pages (indicates non-breakable blocks)
- Missing borders on code blocks
- Poor Chinese font rendering
- Code blocks not breaking across pages properly

### Step 5: Iterate if Needed

If issues are found:
- Adjust the Typst configuration
- Recompile
- Re-validate

## Common Patterns

### Creating a Multi-Section Document

```typst
= Section Title

Regular paragraph content with 中文支持.

== Subsection with Code

#raw(read("example.py"), lang: "python", block: true)

== Another Subsection

More content here.
```

### Mixing Chinese and English

Typst handles mixed content automatically when `lang: "zh"` is set.

### Math Formulas

```typst
数学公式测试：$E = m c^2$
```

### Lists

```typst
- 项目一 (Item 1)
- 项目二 (Item 2)
- 项目三 (Item 3)
```

## Docker Images Required

1. **typst_cn**: Custom image with Typst and Chinese fonts
   - Build from Dockerfile in this skills folder
   - Contains Source Han Serif and Sans fonts
   - Build command: `docker build -t typst_cn -f .claude/skills/pdf-author/Dockerfile .`
   - Or use Makefile: `make build_docker` (if Makefile exists)

2. **minidocks/poppler**: For PDF to PNG conversion
   - Pulled automatically when first used
   - Provides `pdftoppm` utility

### Building the Typst Docker Image

The Dockerfile in this skills folder creates an Alpine-based image with:
- Typst v0.12.0 compiler
- Source Han Sans SC fonts (思源黑体)
- Source Han Serif SC fonts (思源宋体)
- Required font rendering libraries

To build:
```bash
docker build -t typst_cn -f .claude/skills/pdf-author/Dockerfile .
```

Or if a Makefile with `build_docker` target exists:
```bash
make build_docker
```

## Troubleshooting

### Issue: Blank pages before long code blocks

**Cause**: Using `rect()` instead of `block(breakable: true)`

**Solution**: Ensure the show rule uses:
```typst
#show raw.where(block: true): it => block(
  breakable: true,
  ...
)[#it]
```

### Issue: Chinese characters not rendering

**Cause**: Missing fonts in Docker image or wrong font name

**Solution**:
- Verify Docker image includes Source Han fonts
- Check font name spelling: "Source Han Serif SC" (exact case)

### Issue: Code has no frame/background

**Cause**: Show rule not applied or incorrect

**Solution**: Ensure show rule is defined before any content

### Issue: PDF not updating

**Cause**: Docker volume mount issue or compilation error

**Solution**:
- Check Docker volume path is absolute
- Look for Typst compilation errors in output

## Best Practices

1. **Always validate visually**: Don't trust that compilation succeeded - actually look at the PNG output
2. **Use external files for code**: Easier to maintain than inline code blocks
3. **Test with long content**: Generate at least one long code file (300+ lines) to verify page breaks
4. **Specify absolute paths**: When using Docker, always use full paths for volume mounts
5. **Check multiple pages**: Don't just look at page 1 - check pages where content should break

## Example Complete Workflow

```bash
# 1. Create document
# (Use Write tool to create .typ file with proper header)

# 2. Create code examples
# (Use Write tool to create external .py, .sh, .cpp files)

# 3. Compile
make compile

# 4. Convert to PNG
docker run --rm -v /home/wr/tmp/try_typst:/workspace -w /workspace minidocks/poppler pdftoppm output.pdf page -png

# 5. Validate
# (Use Read tool on page-01.png, page-02.png, etc.)

# 6. Report findings to user
```

## Success Criteria

A successful PDF generation includes:
- ✓ Chinese characters render clearly with proper fonts
- ✓ Code blocks have visible frames with gray background
- ✓ Long code blocks break across pages naturally
- ✓ Syntax highlighting is applied
- ✓ No unexpected blank pages
- ✓ Headers, sections, and content flow logically
- ✓ Mixed Chinese/English content renders correctly
