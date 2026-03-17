---
name: generate-import-html
description: Generate structured HTML from authoring analysis for AEM Edge Delivery Services. Creates section structure, applies block tables, handles metadata, and manages images folder.
---

# Generate Import HTML

Create plain HTML file with block structure from authoring analysis.

## When to Use This Skill

Use this skill when:
- You have complete authoring analysis (all sequences have decisions)
- You have section styling validation (from authoring-analysis)
- Ready to generate the HTML file for preview

**Invoked by:** page-import skill (Step 4)

## Prerequisites

From previous skills, you need:
- ✅ Authoring analysis with block selections (from authoring-analysis)
- ✅ Section styling decisions (from authoring-analysis Step 3e)
- ✅ metadata.json with paths and metadata (from scrape-webpage)
- ✅ cleaned.html with content (from scrape-webpage)
- ✅ Block structures fetched (from authoring-analysis Step 3d)

## Related Skills

- **page-import** - Orchestrator that invokes this skill
- **authoring-analysis** - Provides authoring decisions and styling validation
- **scrape-webpage** - Provides metadata, paths, cleaned HTML, images
- **preview-import** - Uses this skill's HTML output

## ⚠️ CRITICAL REQUIREMENT: Complete Content Import

**YOU MUST IMPORT ALL CONTENT FROM THE PAGE. PARTIAL IMPORT IS UNACCEPTABLE.**

- ❌ NEVER truncate or skip sections due to length concerns
- ❌ NEVER summarize or abbreviate content
- ❌ NEVER use placeholders like "<!-- rest of content -->"
- ❌ NEVER omit content because the page is "too long"
- ✅ ALWAYS import every section from authoring analysis
- ✅ ALWAYS include all text, images, and structure from cleaned.html
- ✅ If you encounter length issues, generate the FULL HTML anyway

**Validation requirement:** You MUST verify that the number of sections in your HTML matches the number of sections from identify-page-structure. If they don't match, you have made an error.

---

## HTML Generation Workflow

### Structure Requirements

**IMPORTANT CHANGE:** The AEM CLI now automatically wraps HTML content with headful structure (head, header, footer). You MUST generate ONLY the section content.

**What to generate:**
- ✅ Section divs with content: `<div>...</div>` (one per section)
- ✅ Blocks as `<div class="block-name">` with nested divs
- ✅ Default content (headings, paragraphs, links, images)
- ✅ Section metadata blocks where validated in authoring-analysis

**What NOT to generate:**
- ❌ NO `<html>`, `<head>`, or `<body>` tags
- ❌ NO `<header>` or `<footer>` elements
- ❌ NO `<main>` wrapper element
- ❌ NO head content (meta tags, title, etc. - this comes from project's head.html)

**Structure format:**
```html
<div>
  <!-- Section 1 content -->
</div>
<div>
  <!-- Section 2 content with section-metadata if needed -->
  <div class="section-metadata">
    <div>
      <div>Style</div>
      <div>grey</div>
    </div>
  </div>
  <!-- Section 2 blocks/content -->
</div>
<div>
  <!-- Section 3 content -->
</div>
```

**For detailed block structure patterns:** See `../page-import/resources/html-structure.md`

---

### Section Metadata Application

**Apply validated decisions from authoring-analysis Step 3e:**

**WITH section-metadata** (section provides container styling):
```html
<div>
  <div class="section-metadata">
    <div>
      <div>Style</div>
      <div>dark</div>
    </div>
  </div>
  <div class="tabs">
    <!-- Tabs block content -->
  </div>
</div>
```

**WITHOUT section-metadata** (background is block-specific):
```html
<div>
  <div class="hero">
    <!-- Hero block content with its own dark background -->
  </div>
</div>
```

**Important:**
- Only migrate visible body content sections (skip header, navigation, footer - auto-generated)
- Use consistent style names from identify-page-structure
- **Apply validated decisions from authoring-analysis Step 3e** - Skip section-metadata for single-block sections where background is block-specific
- Place `section-metadata` div at the start of each section that needs styling
- The metadata div will be processed and removed by the platform
- Each section is a separate top-level `<div>` element

---

### Page Metadata Block

**Unless user explicitly requested to skip metadata**, use the metadata extracted from scrape-webpage to generate a metadata block.

**Process:**

**1. Review extracted metadata from metadata.json**

**2. Map each property to standard format:**

**Title:**
- Compare source `title` (or `og:title`) with first H1 on page
- If matches first H1 → Omit (platform defaults to H1)
- If differs → Include as `title` property

**Description:**
- Compare source `description` (or `og:description`) with first paragraph
- If matches first paragraph → Consider omitting (platform defaults to first paragraph)
- If differs OR more descriptive → Include as `description` property
- Check: 150-160 characters ideal

**Image:**
- Check source `og:image`
- If matches first content image → Consider omitting (platform defaults to first image)
- If custom social image → Include as `image` property
- Ensure absolute URL or correct relative path
- Check: 1200x630 pixels recommended

**Canonical:**
- If points to same page URL → Omit (platform auto-generates)
- If points to different page → Include as `canonical` property

**Tags:**
- Map `article:tag` or `keywords` → comma-separated `tags` property

**Properties to SKIP** (platform auto-populates):
- `og:url`, `og:title`, `og:description`, `twitter:title`, `twitter:description`, `twitter:image`
- `viewport`, `charset`, `X-UA-Compatible` (belong in head.html)

**3. Generate metadata block HTML:**

```html
<div>
  <div class="metadata">
    <div>
      <div>title</div>
      <div>[Your mapped title]</div>
    </div>
    <div>
      <div>description</div>
      <div>[Your mapped description]</div>
    </div>
    <!-- Only include image if custom -->
    <!-- Only include canonical if differs from page URL -->
    <!-- Only include tags if present -->
  </div>
</div>
```

**Append metadata block as the last section div at the end of the HTML file.**

**Detailed guidance:** See `resources/metadata-extraction.md` and `resources/metadata-mapping.md`

---

### Images Folder Management (CRITICAL)

The images are currently in `./import-work/images/` and the HTML references them as `./images/...`. You MUST handle the images folder correctly:

**Step 1: Determine the correct images folder location**

Based on `paths.htmlFilePath` from metadata.json:
- HTML file: `us/en/about.plain.html` → Images should be at: `us/en/images/`
- HTML file: `products/widget.plain.html` → Images should be at: `products/images/`
- HTML file: `index.plain.html` → Images should be at: `images/`

**Rule:** Images folder goes in the same directory as the HTML file.

**Step 2: Copy the images folder**

```bash
# Example: If HTML is at us/en/about.plain.html
mkdir -p us/en/images
cp -r ./import-work/images/* us/en/images/
```

**Step 3: Verify image paths in HTML are correct**

The HTML should already reference images as `./images/...` which is correct for files in the same directory. No path changes needed in the HTML.

**Example:**
```
HTML location: us/en/about.plain.html
Images location: us/en/images/
Image reference in HTML: <img src="./images/abc123.jpg">
Result: ✅ Correct - browser resolves to us/en/images/abc123.jpg
```

---

### Save HTML File

**Save to:** Use `paths.htmlFilePath` from metadata.json (e.g., `us/en/about.plain.html`)

Read the metadata.json file from scrape-webpage to get the correct file path.

---

## Validation Checklist (MANDATORY)

Before proceeding to preview-import skill, verify:
- ✅ Section count: HTML has the same number of top-level `<div>` sections as identified in identify-page-structure
- ✅ All sequences: Every content sequence from authoring-analysis appears in the HTML
- ✅ No truncation: No "..." or "<!-- more content -->" or similar placeholders
- ✅ Complete text: All headings, paragraphs, and text from cleaned.html are present
- ✅ All images: Every image reference from the scraped page is included
- ✅ HTML file saved: HTML file written to disk at the correct path
- ✅ Images folder copied: Images folder exists in the same directory as the HTML file
- ✅ Images accessible: Verify that at least one image file exists in the copied images folder

**If any validation check fails, STOP and fix before proceeding.**

---

## Output

This skill provides:
- ✅ HTML file at correct path (e.g., `us/en/about.plain.html`)
- ✅ Images folder in same directory (e.g., `us/en/images/`)
- ✅ Complete content import (all sections)
- ✅ Proper block structure
- ✅ Section metadata applied per validation
- ✅ Page metadata block included

**Next step:** Pass HTML file path to preview-import skill
