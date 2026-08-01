---
name: pdf-leadmagnet
description: Generate professional PDF lead magnets (ebooks, checklists, cheatsheets)
  with consistent branding and high-quality typography.
---

# PDF Lead Magnet Generator

Generate professional PDF lead magnets (ebooks, checklists, cheatsheets) with consistent branding and high-quality typography.

## Agent Integration

**Which agents can use this skill:**

| Agent | Usage |
| ----- | ----- |
| **drafting** | When an idea has `lead_magnet` specified, can create companion PDF content |
| **projection-blog** | Reference lead magnets in blog CTAs |
| **projection-newsletter** | Include lead magnets in newsletter issues |
| **editorial** | Review lead magnet content quality |

**Primary usage**: Manual invocation via `generate.py` script. Future: Dedicated lead-magnet agent for automated PDF creation from idea files.

## When to Use Each Template

| Template | Use For | Pages | Example |
|----------|---------|-------|---------|
| **ebook** | Long-form guides, multi-chapter content | 5-30+ | "The Complete Guide to Technical Due Diligence" |
| **checklist** | Actionable step-by-step lists | 1-3 | "First 90 Days as CTO Checklist" |
| **cheatsheet** | Quick reference, condensed info | 1-2 | "Build vs Buy Decision Framework" |

## How PDFs Are Created

**The workflow**: Markdown content → HTML (via templates) → PDF

```
your-content.md  →  template.html + CSS  →  weasyprint/pdfkit  →  output.pdf
```

**What you control**:
- **Content**: Write in Markdown with special syntax for callouts/checkboxes
- **Structure**: Use Markdown headings (H1, H2, H3) to define sections
- **Page breaks**: Use HTML tags or heading levels to force breaks
- **Styling**: Choose template type (ebook/checklist/cheatsheet), colours via CLI args

**What the templates handle**:
- Cover page (auto-generated from title/subtitle/author)
- Typography and spacing
- Callout box styling
- Page headers/footers
- Print-optimised CSS

## Content Structure Guide

### Markdown → PDF Mapping

| Markdown | PDF Result |
| -------- | ---------- |
| `# Heading 1` | Chapter title (forces page break in ebook) |
| `## Heading 2` | Section heading with accent border |
| `### Heading 3` | Subsection heading |
| `- [ ] Item` | Styled checkbox (empty) |
| `- [x] Item` | Styled checkbox (checked) |
| `::: tip ... :::` | Golden accent callout box |
| `::: warning ... :::` | Orange warning box |
| `::: key-takeaway ... :::` | Full-width dark box |
| `> Quote text` | Pull quote with accent styling |
| Tables | Styled tables with header row |

### Controlling Pages and Layout

**1. Force a page break:**
```markdown
<div class="page-break-before">

## New Section

This starts on a fresh page.

</div>
```

**2. Keep content together (don't split):**
```markdown
<div class="avoid-break">

This entire block stays on one page if possible.

- Item 1
- Item 2
- Item 3

</div>
```

**3. Heading levels determine breaks:**
- `# H1` → Always starts new page (ebook template)
- `## H2` → Stays with following content
- Callout boxes → Never split across pages

### Example: Checklist Structure

```markdown
# First 90 Days Checklist

Brief intro paragraph...

## Phase 1: Deep Listening (Weeks 1-4)

Your job is to understand, not to act.

- [ ] Schedule 1:1s with every direct report
- [ ] Shadow key meetings without contributing
- [ ] Read all post-mortems from last 12 months

::: tip
The moment you start offering opinions, people stop telling you the truth.
:::

## Phase 2: Mapping (Weeks 5-8)

<div class="page-break-before">

Now form your internal picture.

- [ ] Identify what's actually working
- [ ] Map the political landscape
- [ ] Document constraints that shaped decisions

</div>

::: warning
Don't share your conclusions yet — you're still learning.
:::
```

### Example: Ebook Structure

```markdown
# Chapter 1: The Problem

Opening hook that grabs attention...

## Why Most Teams Fail

Body content explaining the core issue...

::: key-takeaway
The single most important insight from this chapter.
:::

<div class="page-break-before">

# Chapter 2: The Framework

</div>

## Step 1: Assess

Detailed explanation...

## Step 2: Decide

More content...
```

## Required Inputs (CLI Arguments)

```bash
python generate.py \
  --template ebook        # ebook | checklist | cheatsheet
  --title "Title"         # Cover page title
  --subtitle "Subtitle"   # Cover page subtitle (optional)
  --author "Name"         # Default: Xavier Fuentes
  --content file.md       # Your Markdown content file
  --output output.pdf     # Where to save the PDF
  --brand-colour "#hex"   # Default: #0d2818 (Deep Jungle)
  --accent-colour "#hex"  # Default: #d4a05e (Golden Amber)
  --logo path/to/logo     # Optional logo file
  --debug                 # Save intermediate HTML for debugging
```

## Generation Process

### 1. Prepare Content

Create a markdown file with your content:

```markdown
# Section Title

Introduction paragraph...

## Subsection

Content with **bold** and *italic* formatting.

::: tip
This is a tip callout box.
:::

::: warning
This is a warning callout box.
:::

::: key-takeaway
This is a key takeaway box.
:::

- [ ] Checklist item one
- [ ] Checklist item two
- [x] Completed item
```

### 2. Generate PDF

```bash
python .claude/skills/pdf-leadmagnet/scripts/generate.py \
  --template ebook \
  --title "Your Title" \
  --subtitle "Your Subtitle" \
  --author "Xavier Fuentes" \
  --brand-colour "#1a1a2e" \
  --accent-colour "#e94560" \
  --content content.md \
  --output output/my-leadmagnet.pdf
```

### 3. Output

PDFs are generated to the specified output path. Default naming convention:
- `{slug}-leadmagnet.pdf` (e.g., `first-90-days-checklist.pdf`)

Output location: `content/assets/` for production files.

## Brand Reference

See `docs/guides/brand-guide.md` for the full Mad Monkey Club visual system.

**Default colours** (jungle palette):

| Colour | Hex | Usage |
| ------ | --- | ----- |
| Deep Jungle | `#0d2818` | Cover backgrounds, headers |
| Forest | `#1a3c34` | Secondary backgrounds |
| Golden Amber | `#d4a05e` | Accents, CTAs, highlights |
| Warm White | `#faf9f7` | Page backgrounds |

**Typography**: Sora (headings) + Source Sans 3 (body)

Override via CLI args: `--brand-colour "#hex" --accent-colour "#hex"`

## Template Features

### All Templates Include

- Professional cover page with title, subtitle, author
- Consistent header/footer with page numbers
- Styled callout boxes (tip, warning, note, key-takeaway)
- Custom checkbox styling for checklists
- Pull quote styling
- Code block formatting
- Page break controls

### Ebook Template

- Multi-page support with automatic pagination
- Table of contents (optional)
- Chapter dividers
- Welcome/intro section template
- CTA section at the end

### Checklist Template

- Large, prominent checkboxes
- Step numbering with visual hierarchy
- Compact single/double-page layout
- Space for notes

### Cheatsheet Template

- Dense information layout
- Multi-column support
- Quick reference tables
- Condensed typography

## Page Break Control

Use these classes in your content:

```html
<div class="page-break-before">
  Content that starts on a new page
</div>

<div class="page-break-after">
  Content followed by a page break
</div>

<div class="avoid-break">
  Content that should stay together
</div>
```

## Setup

### Quick Setup (using virtual environment)

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r .claude/skills/pdf-leadmagnet/requirements.txt

# Install wkhtmltopdf (recommended PDF engine)
brew install wkhtmltopdf
```

### Dependencies

The generate script tries multiple PDF engines in order:

1. **pdfkit** (wkhtmltopdf) — Best CSS support, recommended
2. **weasyprint** — Good fallback, pure Python

Required Python packages (in `requirements.txt`):
- `markdown` — Markdown to HTML conversion
- `jinja2` — Template rendering
- `pdfkit` — PDF generation (requires wkhtmltopdf)

Install the recommended option:

```bash
# macOS
brew install wkhtmltopdf
pip install markdown jinja2 pdfkit

# Or use weasyprint (no system deps)
pip install markdown jinja2 weasyprint
```

## Context Files

- `context/design-principles.md` — Visual design guidelines
- `context/typography.md` — Font pairings and sizing rules
- `context/structure.md` — Content structure patterns

## Examples

### Generate a Checklist

```bash
python .claude/skills/pdf-leadmagnet/scripts/generate.py \
  --template checklist \
  --title "First 90 Days as CTO" \
  --subtitle "A Restraint-First Checklist" \
  --content first-90-days-checklist.md \
  --output content/assets/first-90-days-checklist.pdf
```

### Generate an Ebook

```bash
python .claude/skills/pdf-leadmagnet/scripts/generate.py \
  --template ebook \
  --title "Build vs Buy" \
  --subtitle "A Decision Framework for Technical Leaders" \
  --content build-vs-buy-guide.md \
  --output content/assets/build-vs-buy-framework.pdf
```
