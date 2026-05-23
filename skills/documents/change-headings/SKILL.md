---
name: change-headings
description: Converts all headings in a document into normal paragraphs while keeping the original font size, weight, color, and other formatting intact.
---

# Heading-to-Paragraph Normalizer

You specialize in flattening styled headings into standard paragraphs without altering their visual appearance.
Use this when a document needs uniform text styles while preserving the original heading look (size, weight, color, bold/italic, and inline formatting).

## Required Input
- **Document text/content** with headings styled using heading levels (e.g., Heading 1–6).

## Execution Steps
1. **Identify headings**
   - Detect all heading levels in the provided document.
   - Record each heading's font size, weight, color, alignment, and inline formatting (bold, italic, underline, links, etc.).

2. **Convert styles**
   - Change each heading element to normal body/paragraph style.
   - Reapply the captured formatting so the visual appearance (size, weight, color, inline styles) matches the original heading.
   - Maintain spacing, lists, and indentation around converted headings.

3. **Quality checks**
   - Ensure no heading style remains; all are standard paragraphs.
   - Preserve document structure and order; do not rewrite content.
   - Keep hyperlinks and inline formatting unchanged.

## Output
Return the updated document text/content with headings converted to normal paragraphs that retain the original font size and formatting.
