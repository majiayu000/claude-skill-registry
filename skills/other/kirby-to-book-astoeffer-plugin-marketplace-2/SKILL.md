---
name: kirby-to-book
description: Convert Kirby CMS content to book/document formats. Use when generating PDFs, ebooks, or structured documents from CMS content.
allowed-tools: Read, Write, Grep, Glob
---

# Kirby to Moodle Book Skill

Export Kirby content as native Moodle Book chapters.

## Trigger
- Content export to Moodle requests
- Book module creation
- Multi-page content conversion

## Book XML Structure
```xml
<?xml version="1.0" encoding="UTF-8"?>
<book>
    <name>Book Title</name>
    <intro><![CDATA[<p>Description</p>]]></intro>
    <chapters>
        <chapter>
            <pagenum>1</pagenum>
            <subchapter>0</subchapter>
            <title>Chapter Title</title>
            <content><![CDATA[<p>HTML content</p>]]></content>
        </chapter>
    </chapters>
</book>
```

## Kirby Block to HTML Mapping
| Kirby Block | HTML Output |
|-------------|-------------|
| `heading` | `<h2>` or `<h3>` |
| `text` | `<div class="cloodle-text">` |
| `image` | `<figure><img><figcaption>` |
| `quote` | `<blockquote>` |
| `list` | `<ul>` or `<ol>` |

## Export Process
1. Fetch Kirby page via API or walker
2. Transform blocks to HTML
3. Apply Cloodle CSS classes
4. Generate Book XML
5. Package with images

## Cloodle Styling Classes
```html
<div class="cloodle-content">
    <h2 class="cloodle-heading">Title</h2>
    <div class="cloodle-text">
        <p>Content styled with Cloodle theme</p>
    </div>
</div>
```

## Existing Tools
- `/opt/cloodle/tools/content-pipeline/pptx_to_moodle.py`
- Supports: `--format book`
