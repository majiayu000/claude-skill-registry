---
name: Document design
description: This skill should be used when the user asks to "create a proposal", "design a report", "make a one-pager", "build a PDF", "create a newsletter", "design slides", "make event materials", "design a flyer", or needs help with print-ready HTML documents. Provides brand configuration, CSS patterns for print layout, and document design best practices.
version: 1.0.0
---

# Document design

Create professional, print-ready HTML documents that export to PDF with customizable branding.

## Brand configuration

Before creating documents, check for brand configuration in `.claude/pdf-playground.local.md`. If found, use those settings. If not, use sensible defaults or ask the user for their brand colors.

### Reading brand config

Look for `.claude/pdf-playground.local.md` in the project root. Parse the YAML frontmatter:

```yaml
---
brand:
  name: "Organization Name"
  tagline: "Tagline"
  website: "https://example.com"
  email: "contact@example.com"

colors:
  primary: "#CA3553"
  secondary: "#000000"
  background: "#FFFFFF"
  text: "#2d2a28"
  muted: "#666666"

fonts:
  heading: "Playfair Display"
  body: "Source Sans 3"

style:
  headingCase: "sentence"
  useOxfordComma: true
---
```

### Default brand values

If no config exists, use these defaults:

- **Primary color**: `#CA3553` (red)
- **Secondary color**: `#000000` (black)
- **Heading font**: Playfair Display
- **Body font**: Source Sans 3
- **Heading case**: sentence case

## Core principles

1. **Print-first design**: All documents target 8.5" × 11" letter size with proper margins
2. **Brand compliance**: Use colors and fonts from brand configuration
3. **Sentence case by default**: Unless brand config specifies "title" case
4. **Clean exports**: Documents must render correctly when printed to PDF

## CSS variables

Generate CSS variables from brand config:

```css
:root {
    --primary: [colors.primary];
    --secondary: [colors.secondary];
    --background: [colors.background];
    --text: [colors.text];
    --muted: [colors.muted];

    /* Derived colors */
    --primary-dark: [darken primary by 15%];
    --gray-100: #f5f4f2;
    --gray-200: #e8e6e3;
}
```

## Print CSS fundamentals

### Page setup

```css
@page {
    size: 8.5in 11in;
    margin: 0;
}

@media print {
    body {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
    .page {
        page-break-after: always;
        page-break-inside: avoid;
    }
}
```

### Fixed page dimensions

```css
.page {
    width: 8.5in;
    height: 11in;
    padding: 0.5in 0.75in;
    padding-bottom: 1in; /* Space for footer */
    position: relative;
    box-sizing: border-box;
    overflow: hidden;
}
```

### Fixed footers

```css
.page-footer {
    position: absolute;
    bottom: 0.4in;
    left: 0.75in;
    right: 0.75in;
    font-size: 9pt;
    border-top: 1px solid var(--gray-200);
    padding-top: 0.1in;
    background: var(--background);
}
```

### Footer clearance (critical)

Content overlapping or touching the footer is a recurring issue.

**Preferred layout — grid rows `auto 1fr auto`:**
```css
.page {
    display: grid;
    grid-template-rows: auto 1fr auto;
    overflow: hidden;
}
```
This makes the header and footer take their natural height, and the content fills the remaining space. No magic-number `calc()` needed — the footer clearance is structural.

**Required safeguards:**
1. Use `grid-template-rows: auto 1fr auto` on the page so content automatically gets the space between header and footer
2. Set `overflow: hidden` on the content container to prevent text bleeding past its bounds
3. Include `padding-bottom: 0.3in` (minimum) inside the content area as a buffer
4. Never use hardcoded `height: calc(...)` with magic numbers for header/footer heights — they drift when padding or font sizes change
5. After rendering, always screenshot and visually verify the bottom of the page before delivering
6. If content overflows, **reduce content** — never shrink the footer gap. Tighten the header first if you need more room.

## Typography patterns

### Font loading

```css
@import url('https://fonts.googleapis.com/css2?family=[heading-font]:wght@400;600;700&family=[body-font]:wght@400;500;600;700&display=swap');

body {
    font-family: '[body-font]', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: var(--text);
}

h1, h2, h3 {
    font-family: '[heading-font]', Georgia, serif;
    font-weight: 700;
}
```

### Heading styles

```css
.section-title {
    font-size: 26pt;
    color: var(--secondary);
    margin-bottom: 0.25in;
}

.section-title::after {
    content: '';
    display: block;
    width: 0.5in;
    height: 3px;
    background: var(--primary);
    margin-top: 0.12in;
}
```

## Common components

### Cover page header

```html
<header class="cover-header">
    <div class="logo-bar">
        <div class="logo-primary">[brand.name]</div>
    </div>
    <div class="cover-title-block">
        <div class="cover-eyebrow">[Document type] • [Date]</div>
        <h1 class="cover-title">[Title in configured case]</h1>
    </div>
</header>
```

### Budget table

```css
.budget-table thead {
    background: var(--secondary);
    color: white;
}

.budget-table tbody tr:last-child {
    background: var(--primary);
    color: white;
    font-weight: 700;
}
```

### Highlight box

```css
.highlight-box {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
    padding: 0.3in;
}
```

## Document creation workflow

1. **Check for brand config** in `.claude/pdf-playground.local.md`
2. **Load template** from `${CLAUDE_PLUGIN_ROOT}/templates/`
3. **Apply brand settings** to CSS variables and content
4. **Customize content** based on user requirements
5. **Save HTML file** in current working directory
6. **Offer preview** with Playwright browser tools

## PDF export instructions

1. Open the HTML file in Chrome
2. Press Ctrl+P (or Cmd+P on Mac)
3. Set "Destination" to "Save as PDF"
4. Set "Margins" to "None"
5. Enable "Background graphics"
6. Save the file

## Additional resources

### Templates

Pre-built templates in `${CLAUDE_PLUGIN_ROOT}/templates/`:
- `proposal-template.html`
- `report-template.html`
- `onepager-template.html`
- `newsletter-template.html`
- `slides-template.html`
- `event-template.html`

### Brand examples

Example brand configurations in `${CLAUDE_PLUGIN_ROOT}/brands/`:
- `default.yaml` - Default brand settings
- `ccm.yaml` - Center for Cooperative Media
- `example-newsroom.yaml` - Sample newsroom config

### Reference files

For detailed CSS patterns: `references/css-patterns.md`
