---
name: export-html
description: "Convert a published or drafted article markdown file into a beautiful self-contained HTML file with all images embedded as base64. Use after write-article or publish is complete, when user wants a single HTML file for easy copy-paste to Substack or Medium."
allowed-tools: Bash, Read, Write, Glob
---

# Export to Self-Contained HTML Skill

## Input
$ARGUMENTS = topic name (must have drafts/<topic-slug>.md or published/<topic-slug>.md)

## Process

### Step 1: Find the Article
Check for the article in this order:
1. published/<topic-slug>.md (preferred, final version)
2. drafts/<topic-slug>.md (fallback)

Read the markdown file completely.

### Step 2: Collect All Images
Find every image reference in the markdown:
- Pattern: `![caption](path/to/image.png)`
- Extract all image file paths
- Read each image from figures/output/ and convert to base64

Use this bash command for each image:
```bash
base64 -w 0 figures/output/<fig_name>.png
```

On Windows (if base64 command fails), use Python:
```bash
python -c "import base64; print(base64.b64encode(open('figures/output/<fig_name>.png','rb').read()).decode())"
```

### Step 3: Generate the HTML File
Create a single .html file with ALL images embedded as base64 data URIs.

The HTML must follow this exact template structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{ARTICLE TITLE}</title>
    <style>
        /* Import clean fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 18px;
            line-height: 1.75;
            color: #1a1a1a;
            background: #ffffff;
            max-width: 760px;
            margin: 0 auto;
            padding: 40px 24px 80px;
        }

        /* Title */
        h1 {
            font-size: 2.2em;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 8px;
            color: #111111;
            letter-spacing: -0.02em;
        }

        /* Subtitle */
        .subtitle {
            font-size: 1.2em;
            color: #555555;
            margin-bottom: 32px;
            line-height: 1.5;
        }

        /* Section headings */
        h2 {
            font-size: 1.6em;
            font-weight: 700;
            margin-top: 48px;
            margin-bottom: 16px;
            color: #111111;
            letter-spacing: -0.01em;
        }

        h3 {
            font-size: 1.25em;
            font-weight: 600;
            margin-top: 32px;
            margin-bottom: 12px;
            color: #222222;
        }

        /* Body text */
        p {
            margin-bottom: 16px;
        }

        /* Bold text */
        strong {
            font-weight: 600;
            color: #111111;
        }

        /* Links */
        a {
            color: #2563eb;
            text-decoration: underline;
            text-underline-offset: 2px;
        }

        /* Bullet lists */
        ul, ol {
            margin-bottom: 16px;
            padding-left: 28px;
        }

        li {
            margin-bottom: 8px;
        }

        /* Figures and images */
        figure {
            margin: 32px 0;
            text-align: center;
        }

        figure img {
            max-width: 100%;
            height: auto;
            border: 1px solid #e5e5e5;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }

        figcaption {
            font-size: 0.88em;
            color: #666666;
            margin-top: 12px;
            line-height: 1.5;
            text-align: center;
            font-style: italic;
        }

        /* Callout boxes */
        blockquote {
            background: #f0f7ff;
            border-left: 4px solid #2563eb;
            padding: 20px 24px;
            margin: 24px 0;
            border-radius: 0 8px 8px 0;
            font-size: 0.95em;
        }

        blockquote p {
            margin-bottom: 8px;
        }

        blockquote p:last-child {
            margin-bottom: 0;
        }

        /* Code blocks */
        pre {
            background: #1e1e2e;
            color: #cdd6f4;
            padding: 24px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 24px 0;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.85em;
            line-height: 1.6;
        }

        code {
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.88em;
        }

        /* Inline code */
        p code, li code {
            background: #f3f4f6;
            padding: 2px 6px;
            border-radius: 4px;
            color: #d63384;
            font-size: 0.85em;
        }

        /* Horizontal rule (section divider) */
        hr {
            border: none;
            border-top: 1px solid #e5e5e5;
            margin: 48px 0;
        }

        /* Equation blocks */
        .equation {
            text-align: center;
            font-size: 1.1em;
            margin: 24px 0;
            padding: 16px;
            background: #fafafa;
            border-radius: 8px;
        }

        /* "This article covers" box */
        .covers-box {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 24px;
            margin: 24px 0;
        }

        .covers-box strong {
            font-size: 1.05em;
        }

        /* CTA at the end */
        .cta {
            background: #f0f7ff;
            border-radius: 12px;
            padding: 32px;
            margin-top: 48px;
            text-align: center;
        }

        .cta p {
            margin-bottom: 0;
            font-size: 1.05em;
        }

        /* Further reading */
        .further-reading {
            background: #fafafa;
            border-radius: 8px;
            padding: 24px;
            margin-top: 32px;
        }

        .further-reading h2 {
            margin-top: 0;
            font-size: 1.3em;
        }

        /* Print styles */
        @media print {
            body {
                max-width: 100%;
                padding: 0;
                font-size: 14px;
            }
            pre {
                white-space: pre-wrap;
            }
        }
    </style>
</head>
<body>
    {CONVERTED HTML CONTENT WITH BASE64 IMAGES}
</body>
</html>
```

### Step 4: Convert Markdown to HTML Content

Process the markdown into HTML:

1. **Title (# heading)** becomes `<h1>` at the top
2. **Section headings (## heading)** become `<h2>`
3. **Subsection headings (### heading)** become `<h3>`
4. **Paragraphs** become `<p>` tags
5. **Bold text (**text**)** becomes `<strong>`
6. **Inline code (`code`)** becomes `<code>`
7. **Code blocks (```)** become `<pre><code>` with dark theme
8. **Bullet lists** become `<ul><li>`
9. **Numbered lists** become `<ol><li>`
10. **Blockquotes (> text)** become `<blockquote>`
11. **Images** become `<figure>` with embedded base64:

```html
<figure>
    <img src="data:image/png;base64,{BASE64_DATA}" alt="{caption}">
    <figcaption>{caption}</figcaption>
</figure>
```

12. **Horizontal rules (---)** become `<hr>`

### Step 5: Write the HTML Using Python
Since the HTML will be large (base64 images), use a Python script to:
1. Read the markdown
2. Convert to HTML (use Python's markdown library if available,
   or do manual conversion)
3. Replace image paths with base64 data URIs
4. Wrap in the HTML template
5. Save to published/<topic-slug>.html

```bash
pip install markdown --break-system-packages 2>/dev/null
python build_html.py
```

If the markdown library is not available, do manual regex-based conversion.
The most important thing is that images are base64 embedded and the styling
is clean and professional.

### Step 6: Verify the Output
1. Check the HTML file size (should be large due to base64 images)
2. Count the number of embedded images (should match figure count)
3. Open the HTML file in a browser to visually verify rendering

Report to the user:
```
HTML Export Complete
=====================
File: published/<topic-slug>.html
Size: X MB
Images embedded: 35 of 35
Word count: X words

To use:
1. Open the HTML file in your browser
2. Ctrl+A to select all content
3. Ctrl+C to copy
4. Paste into Substack editor
   OR
   Open in browser and use as standalone article
```

## Important Rules
- ALL images must be embedded as base64. No external file references.
- The HTML must be self-contained. Opening it in any browser should
  render the complete article with all images, no internet needed.
- Use clean, modern styling that looks good on Substack.
- Maintain the exact order of content from the markdown.
- Every figure must have a visible caption below it.
- Code blocks must use dark theme for readability.
- The file will be large (likely 10-30 MB) due to base64 images.
  This is expected and fine.

## Output
Save to published/<topic-slug>.html
Report file size and image count to user.